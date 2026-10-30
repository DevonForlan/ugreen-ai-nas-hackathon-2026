"""Small visible-response mirrors; AUTO-003 owns collection, locking and publication."""
import json
from pathlib import Path
import re
from datetime import datetime
import agent_transcripts as h

LIMIT = 24000
PART_LIMIT = 48000


def visible_text(value):
    text = h.clean(value)
    return re.sub(r'''(?i)(\b(?:OTP|MFA|verification[ _-]code|one[- ]time (?:code|password))["']?\s*(?:[:=]|\bis\b)\s*)["']?[A-Za-z0-9][A-Za-z0-9 -]{3,15}["']?''',
                  r'\1[REDACTED]', text)


def brief(text, limit):
    data = text.encode('utf-8')
    if len(data) <= limit:
        return text
    return data[:limit//2].decode('utf-8',errors='ignore')+'\n[EXCERPT: full content linked below]\n'+data[-limit//2:].decode('utf-8',errors='ignore')


def load_index(root):
    path = Path(root)/'collaboration/live-latest/index.json'
    return json.loads(h.regular(path).read_text(encoding='utf-8')) if path.exists() else dict(schema_version=1, agents={}, sessions={})


def available(root, agent, sid):
    record = load_index(root).get('sessions', {}).get(agent+':'+sid)
    return bool(record and record.get('status') == 'SYNC_COMPLETE' and
                (Path(root)/record['turn_path']).exists() and
                (Path(root)/'collaboration/live-latest'/f'{agent}.md').exists())


def units(session):
    """One canonical assistant record = one completed visible response, not one user mega-turn.

    Tool records preceding that response belong to it. Later tool work waits for
    the next response. Streaming deltas/internal events never enter AUTO-002 events.
    """
    pending = []
    for event in h.events(session):
        if event['kind'] not in {'assistant','tool_call','tool_result','error'}:
            continue
        pending.append(event)
        if event['kind'] == 'assistant':
            yield dict(response_id=event['event_id'], timestamp=event['timestamp'], events=pending)
            pending = []


def render(record, text):
    return (f'<!-- live-mirror-v1 agent={record["agent"]} session={record["session_id"]} turn={record["turn_id"]} -->\n'
        '# Latest visible response\n\n'+
        '\n'.join(f'- {name}: {record.get(name)}' for name in
            ('agent','session_id','turn_id','timestamp','status','github_commit_sha','github_remote_verified','secret_scan','source_transcript_path'))+
        '\n\n'+text+'\n')


def prepare(root, session, transcript):
    root = Path(root)
    agent, sid = session['agent'], session['session_id']
    if agent not in {'codex','claude'} or not h.ID.fullmatch(sid):
        raise ValueError('Invalid mirror identity')
    index = load_index(root)
    key = agent+':'+sid
    old = index.get('sessions', {}).get(key)
    responses = list(units(session))
    if not responses:
        return None
    start = len(responses)-1  # Explicit baseline: no fabricated historical deployment coverage.
    if old:
        matches = [i for i,r in enumerate(responses) if r['response_id']==old['response_id']]
        if not matches:
            raise ValueError('Mirror source lost its previously published response')
        start = matches[0]
    records, names = [], []
    for ordinal,response in enumerate(responses[start:],start+1):
        fingerprint = h.sha(response['events'])
        if old and old.get('status')=='SYNC_COMPLETE' and old['response_id']==response['response_id'] and old['response_sha256']==fingerprint:
            continue
        turn_id = 'visible-'+h.sha(response['response_id'])[:24]
        folder = Path('collaboration/live-turns')/agent/sid
        turn_path = (folder/(turn_id+'.md')).as_posix()
        record = dict(agent=agent,session_id=sid,turn_id=turn_id,response_id=response['response_id'],
            response_ordinal=ordinal,session_started_at=session['started_at'],
            timestamp=response['timestamp'],response_sha256=fingerprint,turn_path=turn_path,
            source_transcript_path=Path(transcript).relative_to(root).as_posix(),
            status='LOCAL_ONLY',github_commit_sha=None,github_remote_verified=False,secret_scan='PASS')
        # Preserve all sanitized content in bounded per-response parts; latest stays small.
        parts = []
        summary = []
        for event in response['events']:
            text = visible_text(event['text'])
            parts.append('## '+event['kind']+' / '+str(event['timestamp'])+'\n'+h.base.fenced(text))
            if event['kind']=='assistant':
                summary.insert(0, '## Visible assistant response\n'+h.base.fenced(brief(text,12000)))
            elif event['kind'] in {'tool_call','tool_result','error'}:
                summary.append('### '+event['kind']+' / '+str(event['timestamp'])+'\n'+h.base.fenced(brief(text,800)))
        full = '\n'.join(parts)
        record['content_sha256'] = h.sha(full)
        record['part_count'] = (len(full)+PART_LIMIT-1)//PART_LIMIT
        links = []
        for ordinal,offset in enumerate(range(0,len(full),PART_LIMIT),1):
            part = (folder/turn_id/f'part-{ordinal:04d}.md').as_posix()
            h.atomic(root/part, '# Visible response content part\n\n'+full[offset:offset+PART_LIMIT]+'\n')
            names.append(part)
            links.append(f'- [Content part {ordinal}](/{part})')
        content = ('\n'.join(summary[:9])+'\n\n## Full sanitized response and visible tools\n'+
                   '\n'.join(links)+'\n\nSource: /'+record['source_transcript_path']+
                   f'\nVisible records: {len(response["events"])}; content parts: {record["part_count"]}. '
                   'Parts are numbered consecutively from part-0001.md in the turn directory.\n'
                   'Latest includes the assistant response and up to eight tool/error excerpts; all content remains in parts.\n'
                   'This is a completed visible record/quiescent snapshot, not process-exit proof.\n')
        # No silent loss: full parts remain authoritative; excerpt counts are explicit.
        content = brief(content,LIMIT)+'\n\nFull turn index: /'+turn_path+'\n'
        h.atomic(root/turn_path,render(record,content))
        names.append(turn_path)
        records.append((record,content))
    if not records:
        return None
    newest = records[-1][0]
    current = index.get('agents',{}).get(agent)
    def rank(record):
        return (datetime.fromisoformat(record['timestamp'].replace('Z','+00:00')),
            datetime.fromisoformat(record.get('session_started_at',record['timestamp']).replace('Z','+00:00')),
            record.get('response_ordinal',0))
    promote = (current is None or
        (current.get('session_id')==sid and newest['response_ordinal']>current.get('response_ordinal',0)) or
        (current.get('session_id')!=sid and rank(newest)>rank(current)) or
        (current.get('session_id')==sid and newest['response_id']==current.get('response_id')))
    bundle = dict(root=root,index=index,key=key,records=records,promote=promote,names=names)
    update(bundle,None,False)
    return bundle


def update(bundle, commit, verified, failure=None):
    root, index = bundle['root'], bundle['index']
    names = list(bundle['names'])
    for record,content in bundle['records']:
        record.update(github_commit_sha=commit,github_remote_verified=verified,
                      status='SYNC_COMPLETE' if verified else ('FAILED' if failure else 'LOCAL_ONLY'))
        if failure:
            record['incomplete_reason'] = failure
            if failure == 'ArtifactScanError':
                record['secret_scan'] = 'FAILED'
        h.atomic(root/record['turn_path'],render(record,content))
    record,content = bundle['records'][-1]
    index.setdefault('sessions',{})[bundle['key']] = dict(record)
    # Latest is a small connector index, not a second unbounded archive.
    if len(index['sessions'])>32:
        newest=sorted(index['sessions'],key=lambda key:index['sessions'][key]['timestamp'],reverse=True)[:32]
        index['sessions']={key:index['sessions'][key] for key in newest}
    if bundle['promote']:
        index.setdefault('agents',{})[record['agent']] = dict(record)
        latest = 'collaboration/live-latest/'+record['agent']+'.md'
        h.atomic(root/latest,render(record,content))
        names.append(latest)
    index_path = 'collaboration/live-latest/index.json'
    h.write_json(root/index_path,index)
    names.append(index_path)
    bundle['paths'] = list(dict.fromkeys(names))
    return bundle['paths']
