"""Versioned phase checkpoints and publication without executing host tests/hooks."""
from datetime import datetime,timezone
import json
from pathlib import Path
import re


PHASES={'STARTED','IMPLEMENTATION_COMPLETE','TEST_COMPLETE','READY_FOR_CC_REVIEW',
        'CC_CHANGES_REQUESTED','FIX_COMPLETE','CC_PASS','DONE','USER_DECISION_REQUIRED','FAILED','CC_REVIEWING'}


def value(task,phase,state,source,result,summary='',tests=None):
    if phase not in PHASES or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',task):
        raise ValueError('Invalid checkpoint task or phase')
    stamp=datetime.now(timezone.utc).isoformat()
    return dict(schema_version=1,task_id=task,phase=phase,state=state['state'],
        actor='cc' if phase.startswith('CC_') or phase=='DONE' else 'codex' if phase in {'STARTED','IMPLEMENTATION_COMPLETE','TEST_COMPLETE','FIX_COMPLETE','READY_FOR_CC_REVIEW'} else 'controller',
        started_at=state.setdefault('started_at',stamp),updated_at=stamp,
        source_commit_sha=source,result_commit_sha=result,tests_summary=tests or [],
        files_changed_summary=state.get('files_changed',[]),progress_summary=summary,
        blocker=state.get('decision'),next_action='Independent CC review' if phase=='READY_FOR_CC_REVIEW' else 'Follow the pinned legal state transition',
        needs_user=phase in {'USER_DECISION_REQUIRED','FAILED'},
        attempt_number=state['codex_attempts'],review_round=state['cc_rounds'],
        live_response_pointer='collaboration/live-latest/'+('claude.md' if phase.startswith('CC_') or phase=='DONE' else 'codex.md'),
        secret_scan='PASS',remote_verified=False,verified_payload_commit=None,
        verification_scope='After push, verified_payload_commit identifies the remotely verified payload; receipt publication SHA is stored in the GitHub agent ledger')


def validate(record):
    schema=json.loads((Path(__file__).resolve().parents[1]/'automation/checkpoint.schema.json').read_text(encoding='utf-8'))
    def check(data,spec):
        kinds={'string':str,'integer':int,'boolean':bool,'array':list,'object':dict,'null':type(None)}
        types=spec.get('type');types=[types] if isinstance(types,str) else types
        if types and not any(type(data) is kinds[k] for k in types):raise ValueError('Checkpoint field type mismatch')
        if 'enum' in spec and data not in spec['enum']:raise ValueError('Unknown checkpoint enum')
        if 'const' in spec and data!=spec['const']:raise ValueError('Checkpoint constant mismatch')
        if isinstance(data,str) and 'pattern' in spec and not re.fullmatch(spec['pattern'],data):raise ValueError('Malformed checkpoint identifier')
        if type(data) is int and (data<spec.get('minimum',data) or data>spec.get('maximum',data)):raise ValueError('Checkpoint counter out of bounds')
        if isinstance(data,list):
            for item in data:check(item,spec.get('items',{}))
        if isinstance(data,dict):
            if set(spec.get('required',[]))-set(data):raise ValueError('Missing checkpoint fields')
            props=spec.get('properties',{})
            if spec.get('additionalProperties') is False and set(data)-set(props):raise ValueError('Unknown checkpoint fields')
            for name,item in data.items():
                if name in props:check(item,props[name])
    check(record,schema)
    if record['secret_scan']!='PASS':raise ValueError('Unsafe checkpoint cannot publish')
    if record['remote_verified'] and not record.get('verified_payload_commit'):raise ValueError('Missing verified checkpoint payload')


def write(root,record,sequence):
    validate(dict(record,sequence=sequence))
    folder=Path(root)/'collaboration/checkpoints'/record['task_id']
    folder.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(dict(record,sequence=sequence),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    latest=folder/'latest.json';entry=folder/f'{sequence:06d}.json'
    if entry.exists() and entry.read_text(encoding='utf-8')!=raw:
        raise ValueError('Checkpoint sequence already belongs to another transition')
    entry.write_text(raw,encoding='utf-8',newline='\n');latest.write_text(raw,encoding='utf-8',newline='\n')
    md=folder/'latest.md'
    md.write_text('# '+record['task_id']+' / '+record['phase']+'\n\n'+
        '\n'.join('- '+key+': '+str(record[key]) for key in ('state','actor','updated_at','source_commit_sha','result_commit_sha','attempt_number','review_round','needs_user','progress_summary','live_response_pointer'))+'\n',encoding='utf-8',newline='\n')
    return [p.relative_to(root).as_posix() for p in (entry,latest,md)]


def attest(root,record,sequence,payload_sha):
    folder=Path(root)/'collaboration/checkpoints'/record['task_id']
    entry=folder/f'{sequence:06d}.json'
    old=json.loads(entry.read_text(encoding='utf-8'))
    if old!=dict(record,sequence=sequence) or old['remote_verified']:
        raise ValueError('Only the exact just-published checkpoint may be attested')
    updated=dict(old,remote_verified=True,verified_payload_commit=payload_sha)
    validate(updated)
    raw=json.dumps(updated,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    for path in (entry,folder/'latest.json'):path.write_text(raw,encoding='utf-8',newline='\n')
    return [entry.relative_to(root).as_posix(),(folder/'latest.json').relative_to(root).as_posix()]
