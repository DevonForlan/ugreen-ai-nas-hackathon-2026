"""Sanitized, append-preserving visible history. No native writes or model calls."""
from datetime import datetime, timezone
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent


def module(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


base = module('history_sanitizer', 'export-codex-session.py')
scan = module('history_scanner', 'scan-codex-secrets.py')
ID = re.compile(r'[A-Za-z0-9_-]{8,100}')
PRIVATE_CALL = re.compile(r'(?i)inspect-transcript-shapes\.py|\.claude[\\/]sessions|Get-ChildItem\s+Env:|(?:^|[;\n])\s*(?:printenv|env|set)\s*(?:$|[;\n])|(?:\.codex|\.claude)[\\/][^\n]*?(?:auth|credentials)|\bauth\.json\b')
ENV_DUMP = re.compile(r'(?m)^[A-Z_][A-Z0-9_]{2,}\s*=')


class ArtifactScanError(ValueError):
    def __init__(self,path,findings):
        self.artifact=path.name if path.name in {'session.md','visible.json','manifest.json'} else 'turn.md'
        self.findings=findings
        super().__init__('Derived content failed secret scan; values are not printed')


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def sha(value):
    return hashlib.sha256((value if isinstance(value, str) else packed(value)).encode('utf-8')).hexdigest()


def clean(value):
    text = base.printable(value)
    normalized = text.replace('\\n','\n').replace('\\"','"')
    if len(ENV_DUMP.findall(normalized)) >= 8:
        return '[ENVIRONMENT DUMP OMITTED]'
    # Do not leak global inventory into the transcript of the project doing the inspection.
    if all(key in normalized for key in ('event_types','sessions','cwd')):
        return '[CROSS-PROJECT INVENTORY OMITTED]'
    if re.search(r'"type"\s*:\s*"(?:response_item|session_meta|api-request-blob)"',text):
        return '[RAW RUNTIME DUMP OMITTED]'
    text = base.sanitize(text)
    text = re.sub(r'(?im)(\b'+base.SENSITIVE+r'\s*[:=])\s*$',r'\1 [REDACTED]',text)
    if scan.scan_text(text) or scan.scan_text(json.dumps(text,ensure_ascii=False)):
        return '[UNSANITIZABLE CONTENT OMITTED]'
    return text


def regular(path):
    path = Path(path)
    if any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()) for p in (path, *path.parents)):
        raise ValueError('Symlink/junction history paths are not supported')
    return path


def atomic(path, text):
    """Only sanitized derived content reaches temporary files; unchanged files keep mtime."""
    path = regular(path)
    findings=scan.scan_text(text)
    if findings:
        raise ArtifactScanError(path,findings)
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    regular(path)
    fd, tmp = tempfile.mkstemp(prefix='.agent-history-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        for attempt in range(8):
            try:
                os.replace(tmp, path)
                break
            except PermissionError:
                if attempt==7:
                    raise
                time.sleep(min(0.02*(2**attempt),0.5))
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return True


def write_json(path, value):
    return atomic(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


@contextmanager
def lease(path):
    path=regular(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    identity=uuid.uuid4().hex
    try:
        with path.open('x',encoding='utf-8') as stream:
            stream.write(identity)
    except FileExistsError as exc:
        raise RuntimeError('History writer already active; never steal a lock by age') from exc
    try:
        yield
    finally:
        if path.exists() and path.read_text(encoding='utf-8')==identity:
            path.unlink()


def project(cwd):
    return base.project_for(cwd) if cwd else None


def archive_root(path=None):
    path = regular(Path(path or Path.home() / '.codex-visible-history').absolute())
    if any((p / '.git').exists() for p in (path, *path.parents)):
        raise ValueError('Global archive must stay outside every Git repository')
    path.mkdir(parents=True, exist_ok=True)
    if os.name != 'nt':
        path.chmod(0o700)
    return path


def empty(agent, sid, cwd, started):
    if agent not in {'codex', 'claude'} or not isinstance(sid, str) or not ID.fullmatch(sid):
        raise ValueError('Unsupported agent/session identity')
    return dict(agent=agent, session_id=sid, cwd=cwd, started_at=started,
                last_event_at=None, last_visible_response_at=None, projects=[], turns=[],
                source_event_count=0, source_byte_cursor=0, malformed_events=0,
                final_response_captured='unknown', ended_at=None)


def add(session, kind, text, timestamp, event_id, cwd=None, call_id=None, final=False):
    text = clean(text)
    if not text:
        return
    turns = session['turns']
    if not turns or kind == 'user':
        turns.append(dict(turn_id=f'turn-{len(turns)+1:06d}', events=[]))
    event = dict(event_id=event_id, kind=kind, text=text, timestamp=timestamp,
                 cwd=clean(cwd or session['cwd'] or 'UNKNOWN'))
    if call_id:
        event['call_id'] = str(call_id)
    if final:
        event['final_candidate'] = True
    turns[-1]['events'].append(event)
    if kind == 'assistant':
        session['last_visible_response_at'] = timestamp


def events(session):
    return [e for t in session['turns'] for e in t['events']]


def finish(session):
    session['projects'] = sorted(set(x or 'UNKNOWN' for x in session['projects']))
    session['visible_event_count'] = len(events(session))
    session['visible_sha256'] = sha(events(session))
    session['marker'] = sha([session['source_event_count'], session['source_byte_cursor'], session['visible_sha256']])
    return session


def read_native(path, agent):
    """One fixed byte boundary; all non-visible event types/blocks are dropped."""
    path = regular(path)
    if agent == 'claude' and 'subagents' in path.parts:
        return None  # internal agent prompts are not a user conversation
    limit = path.stat().st_size
    session = None
    deferred = []
    blocked = set()
    cwd = None
    projects = set()
    malformed = count = 0
    with path.open('rb') as f:
        while f.tell() < limit:
            line = f.readline(limit - f.tell())
            count += 1
            if not line.endswith(b'\n'):
                malformed += 1
                continue
            try:
                e = json.loads(line.decode('utf-8-sig'))
                if not isinstance(e, dict):
                    raise ValueError()
            except (ValueError, UnicodeError):
                malformed += 1
                continue
            stamp = e.get('timestamp') if isinstance(e.get('timestamp'), str) else None
            if agent == 'codex':
                p = e.get('payload')
                if not isinstance(p, dict):
                    p = {}
                if e.get('type') == 'session_meta':
                    if session:
                        raise ValueError('Multiple native session identities')
                    if isinstance(p.get('source'), dict) and 'subagent' in p['source']:
                        return None
                    cwd = p.get('cwd')
                    session = empty(agent, p.get('id'), cwd, p.get('timestamp') or stamp)
                if e.get('type') in {'session_meta', 'turn_context'} and isinstance(p.get('cwd'), str):
                    cwd = p['cwd']
                    projects.add(project(cwd))
                if session is None:
                    continue
                session['last_event_at'] = stamp or session['last_event_at']
                typ = p.get('type')
                if e.get('type') == 'response_item':
                    if typ == 'message' and p.get('role') in {'user', 'assistant'} and p.get('channel') not in {'analysis', 'reasoning'}:
                        value=base.text_content(p.get('content'))
                        if not value and isinstance(p.get('content'),list) and any(isinstance(b,dict) and b.get('type') in {'image','input_image','audio','input_audio','file'} for b in p['content']):
                            value='[NON-TEXT ATTACHMENT RETAINED ONLY IN NATIVE SOURCE]'
                        add(session, p['role'], value, stamp, f'native-{count}', cwd,
                            final=p.get('phase') in {'final', 'final_answer'} or p.get('channel') == 'final')
                    elif typ in {'function_call', 'custom_tool_call'}:
                        raw = {k:p[k] for k in ('name', 'arguments', 'input') if k in p}
                        cid = p.get('call_id', f'native-{count}')
                        if PRIVATE_CALL.search(packed(raw)):
                            blocked.add(cid)
                            raw = '[PRIVATE AUTH/ENVIRONMENT/INVENTORY CALL OMITTED]'
                        add(session, 'tool_call', raw, stamp, f'native-{count}', cwd, cid)
                    elif typ in {'function_call_output', 'custom_tool_call_output'}:
                        cid = p.get('call_id', '')
                        value = '[PRIVATE CALL RESULT OMITTED]' if cid in blocked else p.get('output', '')
                        add(session, 'tool_result', value, stamp, f'native-{count}', cwd, cid)
                elif e.get('type') == 'event_msg' and typ in {'error', 'warning', 'turn_aborted'}:
                    add(session, 'error', {k:p[k] for k in ('message','error','reason') if k in p}, stamp, f'native-{count}', cwd)
                elif e.get('type') == 'event_msg' and typ == 'session_end':
                    session['ended_at'] = stamp
            else:
                if isinstance(e.get('cwd'), str):
                    cwd = e['cwd']
                    projects.add(project(cwd))
                sid = e.get('sessionId')
                if session is None and sid:
                    session = empty(agent, sid, cwd, stamp)
                if not session:
                    continue
                if not session['started_at'] and stamp:
                    session['started_at']=stamp
                if sid and sid != session['session_id']:
                    raise ValueError('Mixed Claude session identities')
                session['last_event_at'] = stamp or session['last_event_at']
                # Excludes system, api-request/blob, attachments, snapshots, thinking, etc.
                if e.get('type') not in {'user','assistant'} or e.get('isMeta'):
                    continue
                msg = e.get('message')
                if not isinstance(msg, dict):
                    continue
                role = msg.get('role')
                if role != e['type']:
                    continue
                content = msg.get('content', [])
                if isinstance(content, str):
                    content = [{'type':'text','text':content}]
                for j, b in enumerate(content if isinstance(content,list) else []):
                    if not isinstance(b,dict):
                        continue
                    eid = str(e.get('uuid') or f'native-{count}') + f'-{j}'
                    typ = b.get('type')
                    if typ == 'text':
                        deferred.append((eid, role, b.get('text',''), stamp, cwd, None, False))
                    elif typ == 'tool_use' and role == 'assistant':
                        cid = b.get('id', eid)
                        value = {k:b[k] for k in ('name','input') if k in b}
                        if PRIVATE_CALL.search(packed(value)):
                            blocked.add(cid)
                            value = '[PRIVATE AUTH/ENVIRONMENT/INVENTORY CALL OMITTED]'
                        deferred.append((eid, 'tool_call', value, stamp, cwd, cid, False))
                    elif typ == 'tool_result' and role == 'user':
                        cid = b.get('tool_use_id', '')
                        value = '[PRIVATE CALL RESULT OMITTED]' if cid in blocked else b.get('content','')
                        if isinstance(value, list):
                            value = base.text_content(value)
                        deferred.append((eid, 'tool_result', value, stamp, cwd, cid, False))
                    elif typ in {'image','document','audio'}:
                        deferred.append((eid,role,'[NON-TEXT ATTACHMENT RETAINED ONLY IN NATIVE SOURCE]',stamp,cwd,None,False))
    if not session:
        return None
    # Duplicate Claude UUID/block snapshots collapse to their latest visible version.
    unique = {}
    for row in deferred:
        unique[row[0]] = row
    for eid, kind, text, stamp, at, cid, final in unique.values():
        add(session, kind, text, stamp, eid, at, cid, final)
    session.update(projects=sorted(x or 'UNKNOWN' for x in projects), source_event_count=count, source_byte_cursor=limit, malformed_events=malformed)
    return finish(session)


def source_roots(agent):
    if agent == 'codex':
        home = Path(os.environ.get('CODEX_HOME') or Path.home()/'.codex')
        return [home/'sessions', home/'archived_sessions']
    return [Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home()/'.claude')/'projects']


def discover(agent, roots=None):
    found = []
    for root in roots if roots is not None else source_roots(agent):
        if Path(root).is_dir():
            found.extend(p for p in Path(root).rglob('*.jsonl') if 'subagents' not in p.parts)
    return sorted(set(found))


def captured(session, proof):
    last = next((e for e in reversed(events(session)) if e['kind']=='assistant'), None)
    return bool(proof and proof.get('process_exited') is True and proof.get('exit_code') == 0
                and proof.get('session_id') == session['session_id'] and session['malformed_events'] == 0
                and proof.get('marker') == session['marker'] and last
                and proof.get('final_sha256') == sha(last['text'].strip())
                and events(session)[-1]['kind'] == 'assistant')


def prove_exit(session, final_text, exit_code, ended_at):
    """Only the outer process owner calls this after wait()/communicate() returns."""
    last = next((e for e in reversed(events(session)) if e['kind']=='assistant'), None)
    proof = dict(process_exited=True, exit_code=exit_code, ended_at=ended_at,
                 session_id=session['session_id'], marker=session['marker'], final_sha256=sha(clean(final_text).strip()))
    if not last or last['text'].strip() != clean(final_text).strip():
        return None
    return proof if captured(session, proof) else None


def ownership(session, project_path):
    return not project_path or session['projects'] == [project(project_path)]


def render(session, manifest, project_path=None, synced=False):
    agent, sid = session['agent'], session['session_id']
    owner = sha(base.canonical(project_path)) if project_path else 'local'
    prefix = 'codex-export-v1' if agent == 'codex' else 'claude-export-v1'
    lines = [f'<!-- {prefix} project={owner} session={sid} -->', '# '+('Codex' if agent=='codex' else 'Claude Code')+' Session',
             f'- Session ID: {sid}', f'- Start Time: {session["started_at"]}', f'- End Time: {manifest.get("ended_at") or "Not proven"}',
             f'- Working Directory: {clean(session["cwd"] or "UNKNOWN")}', f'- Last recorded event: {session["last_event_at"]}',
             f'- Latest visible response timestamp: {session["last_visible_response_at"]}', f'- Export timestamp: {manifest["exported_at"]}',
             f'- Source event count: {session["source_event_count"]}', f'- Source byte cursor: {session["source_byte_cursor"]}',
             f'- Visible event count: {session["visible_event_count"]}', f'- Snapshot marker: {session["marker"]}',
             '- final_response_captured: '+str(manifest['final_response_captured']).lower(),
             '- github_synced: '+str(synced).lower(), f'- Malformed/partial events: {session["malformed_events"]}',
             '- Sync applies only to this exact snapshot. Active-session future responses are not certified.', '']
    lines += ['## Turn Index', '', '| Turn | First event | Last visible response | Final capture | GitHub snapshot |',
              '| --- | --- | --- | --- | --- |']
    for t in session['turns']:
        replies = [e for e in t['events'] if e['kind']=='assistant']
        final = manifest['final_response_captured'] if t is session['turns'][-1] else 'unknown'
        lines.append(f'| {t["turn_id"]} | {t["events"][0]["timestamp"]} | {replies[-1]["timestamp"] if replies else "UNKNOWN"} | {str(final).lower()} | {str(synced).lower()} |')
    lines.append('')
    sections = [('User Messages', {'user'}),('Codex Visible Responses' if agent=='codex' else 'Claude Visible Responses', {'assistant'}),
                ('Tool / Command Calls', {'tool_call'}),('Tool / Command Results', {'tool_result'}),('Errors', {'error'}),('Tests',set())]
    for heading, kinds in sections:
        lines.append('## '+heading)
        count = 0
        for turn in session['turns']:
            for e in turn['events']:
                if e['kind'] not in kinds:
                    continue
                count += 1
                lines += [f'### {turn["turn_id"]} / {e["event_id"]} / {e["timestamp"]}',base.fenced(e['text'])]
        if heading == 'Tests':
            lines.append('Test commands and full visible test results remain in the tool sections; no test outcome is inferred.')
        elif not count:
            lines.append('No separately recorded entries.')
        lines.append('')
    return '\n'.join(line.rstrip() for line in base.sanitize('\n'.join(lines)).splitlines()).rstrip()+'\n'


def archive(session, root=None, project_path=None, proof=None, allow_stream_growth=False):
    root=archive_root(root)
    if session.get('agent') not in {'codex','claude'} or not ID.fullmatch(session.get('session_id') or ''):
        raise ValueError('Unsafe archive identity')
    with lease(root/session['agent']/session['session_id']/'.archive.lock'):
        return _archive(session,root,project_path,proof,allow_stream_growth)


def _archive(session, root=None, project_path=None, proof=None, allow_stream_growth=False):
    root = archive_root(root)
    directory = root/session['agent']/session['session_id']
    path = directory/'manifest.json'
    old = json.loads(regular(path).read_text(encoding='utf-8')) if path.exists() else None
    if old and (old.get('session_id') != session['session_id'] or old.get('agent') != session['agent']):
        raise ValueError('Archive ownership mismatch')
    if old and old['source_event_count'] > session['source_event_count']:
        raise ValueError('Native source shrank; earlier archive preserved')
    prior = {}
    if old:
        # Never silently erase earlier visible turns if a native source is rewritten.
        previous = json.loads((directory/'visible.json').read_text(encoding='utf-8'))
        prior = {e['event_id']:dict(e,text=clean(e['text'])) for e in previous}
        current = {e['event_id']:e for e in events(session)}
        def preserved(key, value):
            candidate = current.get(key)
            if candidate == value:
                return True
            # Claude can append a newer snapshot of the same UUID/block while
            # streaming. Explicit live mode permits text growth, never erasure.
            return (allow_stream_growth and candidate is not None and value['kind']=='assistant'
                and candidate['kind']=='assistant' and candidate['text'].startswith(value['text'])
                and {k:v for k,v in candidate.items() if k not in {'text','timestamp'}} ==
                    {k:v for k,v in value.items() if k not in {'text','timestamp'}})
        if any(not preserved(key,value) for key,value in prior.items()):
            raise ValueError('Native visible prefix changed; earlier archive preserved')
    proof = proof or (old or {}).get('exit_proof')
    valid = captured(session, proof)
    manifest = dict(schema_version=1, agent=session['agent'], session_id=session['session_id'],
                    started_at=session['started_at'], last_event_at=session['last_event_at'],
                    last_visible_response_at=session['last_visible_response_at'], marker=session['marker'],
                    source_event_count=session['source_event_count'], source_byte_cursor=session['source_byte_cursor'],
                    visible_event_count=session['visible_event_count'], malformed_events=session['malformed_events'],
                    final_response_captured=valid if proof else 'unknown', exit_proof=proof,
                    ended_at=proof['ended_at'] if valid else None, github_sync=(old or {}).get('github_sync', {}))
    comparable = dict(old or {})
    comparable.pop('exported_at',None)
    manifest['exported_at'] = old['exported_at'] if old and comparable==manifest else now()
    changed = write_json(directory/'visible.json', events(session))
    changed |= atomic(directory/'session.md', render(session,manifest))
    for turn in session['turns']:
        turn_path = directory/'turns'/(turn['turn_id']+'.md')
        if (allow_stream_growth and turn_path.exists() and
                all(prior.get(e['event_id']) == e for e in turn['events'])):
            # Historical turn content is unchanged. Its existing marker describes
            # that older exact snapshot; the manifest/session carry current freshness.
            continue
        turn_sync = any(v.get('turns',{}).get(turn['turn_id']) == sha(turn['events']) for v in manifest['github_sync'].values())
        turn_final = manifest['final_response_captured'] if turn is session['turns'][-1] else 'unknown'
        content = ('# '+turn['turn_id']+'\n\nSession ID: '+session['session_id']+
                   '\nFinal response captured: '+str(turn_final).lower()+'\nGitHub snapshot synced: '+str(turn_sync).lower()+
                   '\nSnapshot marker: '+session['marker']+'\n\n'+
                   '\n'.join(f'## {e["kind"]} / {e["timestamp"]}\n'+base.fenced(e['text']) for e in turn['events']))
        changed |= atomic(turn_path,base.sanitize(content))
    changed |= write_json(path,manifest)
    target = None
    if project_path and ownership(session,project_path):
        started = session['started_at']
        if not isinstance(started,str) or not re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}',started):
            raise ValueError('Missing usable session start timestamp')
        folder = 'codex-sessions' if session['agent']=='codex' else 'cc-sessions'
        target = Path(project_path)/'collaboration'/folder/f'{started[:10]}_{started[11:13]}{started[14:16]}_{session["session_id"]}.md'
        marker = render(session,manifest,project_path).splitlines()[0]
        if target.exists() and regular(target).read_text(encoding='utf-8').splitlines()[0] != marker:
            raise ValueError('Project export ownership mismatch')
        sync = manifest['github_sync'].get(sha(base.canonical(project_path)),{})
        changed |= atomic(target,render(session,manifest,project_path,sync.get('marker')==session['marker'] and sync.get('complete') is True))
    return dict(session=session, manifest=manifest, directory=directory, transcript=target, changed=bool(changed))


def refresh(agents=('codex','claude'), root=None, project_path=None, roots=None):
    stats = dict(discovered=0,archived=0,project_exported=0,unchanged=0,malformed_events=0,failures=0)
    for agent in agents:
        for path in discover(agent, roots.get(agent) if roots else None):
            stats['discovered'] += 1
            try:
                session = read_native(path,agent)
                if not session:
                    continue
                item = archive(session,root,project_path)
                stats['archived'] += 1
                stats['project_exported'] += bool(item['transcript'])
                stats['unchanged'] += not item['changed']
                stats['malformed_events'] += session['malformed_events']
            except (OSError,ValueError,TypeError,KeyError,RuntimeError) as exc:
                stats['failures'] += 1
                print('History skipped: unsafe/malformed source or changed prefix; no content printed.')
                if isinstance(exc,ArtifactScanError):
                    for line,rule in exc.findings[:5]:
                        print(f'File: local-visible/{exc.artifact}; Rule: {rule}; Line: {line}; Finding: REDACTED')
    return stats


def ledger(item, task_id, round_number=1, run_id=None, failed=False):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', task_id) or type(round_number) is not int or round_number < 1:
        raise ValueError('Unsafe task/round identity')
    s,m = item['session'],item['manifest']
    return dict(schema_version=1,run_id=run_id or uuid.uuid4().hex,task_id=task_id,agent=s['agent'],session_id=s['session_id'],
                round=round_number,started_at=s['started_at'],ended_at=m['ended_at'],last_visible_response_at=s['last_visible_response_at'],
                final_response_captured=m['final_response_captured'],local_archive_updated=True,
                project_transcript_updated=bool(item['transcript']),secret_scan='PENDING',commit_sha=None,github_synced=False,
                status='FAILED' if failed else 'LOCAL_ONLY',snapshot_marker=s['marker'],visible_event_count=s['visible_event_count'],
                source_event_count=s['source_event_count'],malformed_events=s['malformed_events'],
                transcript_path=None,transcript_sha256=None)


def complete(value):
    return bool(value['final_response_captured'] is True and value['local_archive_updated'] is True
                and value['project_transcript_updated'] is True and value['secret_scan']=='PASS'
                and value['github_synced'] is True and value['ended_at'] and value['last_visible_response_at']
                and re.fullmatch(r'[a-f0-9]{40,64}',value.get('commit_sha') or '')
                and value.get('malformed_events',0)==0)


def codex_result(raw, prompt, final_text, cwd, started, ended, exit_code=0, native_roots=None):
    rows = []
    bad = 0
    for line in raw.splitlines():
        try:
            e = json.loads(line)
            if not isinstance(e,dict):
                raise ValueError()
            rows.append(e)
        except ValueError:
            bad += 1
    sid = next((e.get('thread_id') for e in rows if e.get('type')=='thread.started'), None)
    s = empty('codex',sid,str(cwd),started)
    s['projects'] = [project(cwd)]
    add(s,'user',prompt,started,'input-1',str(cwd))
    for i,e in enumerate(rows):
        item = e.get('item')
        if e.get('type')=='item.completed' and isinstance(item,dict):
            typ = item.get('type')
            eid = str(item.get('id') or i)
            if typ=='agent_message':
                add(s,'assistant',item.get('text',''),ended,eid,str(cwd),final=True)
            elif typ=='command_execution':
                private = PRIVATE_CALL.search(item.get('command',''))
                add(s,'tool_call','[PRIVATE CALL OMITTED]' if private else item.get('command',''),ended,eid+'-call',str(cwd))
                add(s,'tool_result','[PRIVATE CALL RESULT OMITTED]' if private else item.get('aggregated_output',''),ended,eid+'-result',str(cwd))
            elif typ in {'mcp_tool_call','web_search','file_change'}:
                add(s,'tool_call',{k:item[k] for k in ('name','server','tool','arguments','query','changes') if k in item},ended,eid+'-call',str(cwd))
                if 'result' in item or 'error' in item:
                    add(s,'tool_result',{k:item[k] for k in ('result','error') if k in item},ended,eid+'-result',str(cwd))
        elif e.get('type') in {'error','turn.failed'}:
            add(s,'error',{k:e[k] for k in ('message','error') if k in e},ended,f'error-{i}',str(cwd))
    s.update(source_event_count=len(rows)+bad,source_byte_cursor=len(raw.encode('utf-8')),last_event_at=ended,malformed_events=bad)
    s = finish(s)
    # Prefer the richer native canonical source when the exited exec session is discoverable.
    for path in discover('codex',native_roots):
        if sid not in path.name:
            continue
        native = read_native(path,'codex')
        if native and native['session_id']==sid:
            s = native
            break
    terminal = bool(rows and rows[-1].get('type')=='turn.completed' and
                    not any(e.get('type') in {'error','turn.failed'} for e in rows))
    proof = prove_exit(s,final_text,exit_code,ended) if terminal and not bad else None
    return s,proof


def claude_result(envelope, prompt, cwd, started, ended, exit_code=0):
    if not isinstance(envelope,dict):
        raise ValueError('Malformed Claude result envelope')
    s = empty('claude',envelope.get('session_id'),str(cwd),started)
    s['projects'] = [project(cwd)]
    add(s,'user',prompt,started,'input-1',str(cwd))
    result = envelope.get('structured_output')
    if result is None:
        result = envelope.get('result')
    if not isinstance(result,(str,dict,list)) or not result:
        raise ValueError('Missing Claude visible final result')
    add(s,'assistant',result,ended,'result-1',str(cwd),final=True)
    s.update(source_event_count=2,source_byte_cursor=len(packed(result).encode('utf-8')),last_event_at=ended)
    s = finish(s)
    proof = None if envelope.get('is_error') else prove_exit(s,clean(result),exit_code,ended)
    return s,proof


def save_run(session, proof, project_path, task_id, round_number=1, root=None, run_id=None, failed=False):
    project_path = Path(project_path).resolve()
    if not ownership(session,project_path):
        raise ValueError('Refusing cross-project run publication')
    item = archive(session,root,project_path,proof)
    value = ledger(item,task_id,round_number,run_id,failed)
    if not item['transcript']:
        raise ValueError('No project transcript for run')
    value['transcript_path'] = item['transcript'].relative_to(project_path).as_posix()
    value['transcript_sha256'] = sha(item['transcript'].read_text(encoding='utf-8'))
    path = project_path/'collaboration/run-ledger'/f'{task_id}_{session["agent"]}_round-{round_number}_{value["run_id"]}.json'
    write_json(path,value)
    return item,path,value
