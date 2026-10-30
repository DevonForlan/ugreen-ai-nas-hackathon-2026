"""Bounded controller metadata; full output belongs in separately scanned artifacts."""
import copy
import hashlib
import json


def summary(item):
    raw=item.get('output','')
    raw=raw if isinstance(raw,str) else ''
    command=item.get('command',[])
    return dict(command=[str(x)[:512] for x in command[:32]] if isinstance(command,list) else [],
        exit_code=item.get('exit_code'),output_sha256=item.get('output_sha256') or hashlib.sha256(raw.encode()).hexdigest(),
        output_bytes=item.get('output_bytes',len(raw.encode())),tail=str(item.get('tail',raw[-1024:]))[-1024:],
        **({'artifact_path':item['artifact_path']} if 'artifact_path' in item else {}))


def compact(state):
    value=copy.deepcopy(state)
    for key in ('test_evidence',):
        if isinstance(value.get(key),list):value[key]=[summary(x) for x in value[key][:16] if isinstance(x,dict)]
    if isinstance(value.get('handoff'),dict) and isinstance(value['handoff'].get('tests'),list):
        value['handoff']['tests']=[summary(x) for x in value['handoff']['tests'][:16] if isinstance(x,dict)]
    return value


def minimal_stop(state):
    def counter(key):
        n=state.get(key)
        return n if type(n) is int and 0<=n<=3 else 3
    return dict(state=state['state'],body_sha256=state.get('body_sha256','UNKNOWN'),
        codex_attempts=counter('codex_attempts'),cc_rounds=counter('cc_rounds'),history=[],
        decision={'reason':'Emergency stop; inspect pinned evidence. Details omitted safely.',
            'question':'Options: reconcile evidence or cancel. Recommendation: keep stopped.',
            'options':['Reconcile pinned evidence','Cancel without retry'],
            'recommendation':'Keep stopped; never reset exhausted counters.'},emergency_payload_fallback=True)
