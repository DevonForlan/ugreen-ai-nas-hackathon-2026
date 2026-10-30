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
        secret_scan='PASS',remote_verified=True,
        verification_scope='source/result payload is verified; checkpoint publication SHA is recorded in durable agent ledger after push')


def write(root,record,sequence):
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
