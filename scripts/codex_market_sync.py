"""Full visible Codex Market history; isolated identity, paths and bounded live publisher.

Native input is read-only. No auth/config sources, raw dumps or internal records are
exported. Existing Codex exports and mirrors are never written by this module.
"""
import argparse
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

import agent_transcripts as h
import agent_live_sync as live
from agent_history_sync import git, SyncError
from agent_security import trusted_executable, process_birth

REDACTED = '[REDACTED_SECRET]'
PART_BYTES = 512000
AGENT = 'codex-market'
CODE = re.compile(r'''(?ix)(\b(?:otp|mfa|oauth[ _-]?code|device[ _-]?code|user[ _-]?code|verification[ _-]?code|one[ _-]?time[ _-]?(?:code|password))["']?\s*(?:[:=]|\bis\b)\s*)["']?[A-Za-z0-9][A-Za-z0-9_-]{3,64}["']?''')


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode('utf-8')).hexdigest()


def sanitize(value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    # Apply the proven secret patterns, but never replace a whole visible event
    # with an excerpt/summary when a value can be redacted in place.
    text = h.base.sanitize(text).replace('[REDACTED]', REDACTED)
    text = CODE.sub(lambda m: m[1] + REDACTED, text)
    if h.scan.scan_text(text):
        raise ValueError('Visible value failed secret scan; content withheld')
    return text


def native(source, sid, root):
    """Allowlisted visible records only, at a fixed complete-line byte boundary."""
    h.regular(source)
    turns, visible, meta, contexts, offset = [], [], None, set(), 0
    limit = source.stat().st_size
    prefix = hashlib.sha256()
    with source.open('rb') as stream:
        while stream.tell() < limit:
            line = stream.readline(limit - stream.tell())
            if not line.endswith(b'\n'):
                break  # An active append is not a malformed historical record.
            prefix.update(line)
            offset = stream.tell()
            row = json.loads(line.decode('utf-8-sig'))
            if not isinstance(row, dict):
                raise ValueError('Malformed native record')
            p = row.get('payload')
            p = p if isinstance(p, dict) else {}
            if row.get('type') == 'session_meta':
                if meta or p.get('id') != sid or (isinstance(p.get('source'), dict) and 'subagent' in p['source']):
                    raise ValueError('Native session identity mismatch')
                if h.project(p.get('cwd')) != h.base.canonical(root):
                    raise ValueError('Native project ownership mismatch')
                meta = dict(started_at=p.get('timestamp') or row.get('timestamp'))
            if row.get('type') in {'session_meta', 'turn_context'} and p.get('cwd'):
                contexts.add(h.project(p['cwd']))
            kind, value = None, None
            if row.get('type') == 'response_item':
                typ = p.get('type')
                if typ == 'message' and p.get('role') in {'user', 'assistant'} and p.get('channel') not in {'analysis', 'reasoning'}:
                    kind = p['role']
                    value = h.base.text_content(p.get('content'))
                    blocks = p.get('content', [])
                    if isinstance(blocks, list) and any(isinstance(b, dict) and b.get('type') in {'image', 'input_image', 'audio', 'input_audio', 'file'} for b in blocks):
                        value += '\n[NON-TEXT ATTACHMENT RETAINED ONLY IN NATIVE SOURCE]'
                elif typ in {'function_call', 'custom_tool_call'}:
                    kind, value = 'tool_call', {k: p[k] for k in ('name', 'arguments', 'input', 'call_id') if k in p}
                elif typ in {'function_call_output', 'custom_tool_call_output'}:
                    kind, value = 'tool_result', p.get('output', '')
            elif row.get('type') == 'event_msg' and p.get('type') in {'error', 'warning', 'turn_aborted'}:
                kind, value = p['type'], {k: p[k] for k in ('message', 'error', 'reason') if k in p}
            if kind is None:
                continue
            if not meta:
                raise ValueError('Visible content precedes session identity')
            text = sanitize(value)
            if kind == 'user' or not turns:
                turns.append(dict(turn_id=f'turn-{len(turns)+1:06d}', events=[]))
            event = dict(event_id=f'byte-{offset}', kind=kind, timestamp=row.get('timestamp'), text=text)
            if p.get('call_id'):
                event['call_id'] = p['call_id']
            if kind == 'assistant':
                event['channel'] = p.get('channel') or p.get('phase') or 'visible'
            turns[-1]['events'].append(event)
            visible.append(event)
    if not meta or contexts != {h.base.canonical(root)}:
        raise ValueError('Missing/mixed project ownership')
    return dict(session_id=sid, **meta, turns=turns, events=visible, source_bytes=offset,
                source_prefix_sha256=prefix.hexdigest(), source_complete=offset == limit)


def fence(text):
    return h.base.fenced(text)


def render_turn(turn):
    labels = dict(user='User', assistant='Assistant', tool_call='Tools / Call', tool_result='Tools / Result', error='Error', warning='Warning', turn_aborted='Aborted')
    out = ['# ' + turn['turn_id'], '']
    for event in turn['events']:
        out += ['### ' + labels[event['kind']], '', f"timestamp: {event['timestamp']}; event_id: {event['event_id']}", '', fence(event['text']), '']
    return '\n'.join(out)


def chunks(text, size):
    data = text.encode('utf-8')
    while data:
        cut = min(size, len(data))
        while cut < len(data) and data[cut] & 0xC0 == 0x80:
            cut -= 1
        if not cut:
            raise ValueError('Part byte budget too small')
        yield data[:cut].decode('utf-8')
        data = data[cut:]


def put(root, name, text, files):
    if '..' in Path(name).parts:
        raise ValueError('Unsafe artifact path')
    h.atomic(root / name, text)
    files[name] = digest(text)


def put_document(root, name, text, part_name, files, size=PART_BYTES):
    if len(text.encode('utf-8')) <= size:
        put(root, name, text, files)
        return dict(path=name, sha256=digest(text), parts=[])
    names = []
    for i, part in enumerate(chunks(text, size), 1):
        path = part_name(i)
        put(root, path, part, files)
        names.append(path)
    # Relative paths are valid in GitHub; ordered concatenation is byte-exact.
    index = '# Complete content parts\n\nConcatenate all parts in this order; no content omitted.\n\n'
    for path in names:
        relative = os.path.relpath(root / path, (root / name).parent).replace('\\', '/')
        index += f'- [{path}]({relative})\n'
    index += f'\ncontent_sha256: {digest(text)}\n'
    put(root, name, index, files)
    return dict(path=name, sha256=digest(text), parts=names)


def export(source, sid, root, task='Market / Ideation session visible-history synchronization', runtime=None):
    sid_ok = h.ID.fullmatch(sid)
    if not sid_ok:
        raise ValueError('Invalid session identity')
    root = h.regular(root.resolve())
    folder = f'collaboration/codex-market-sessions/{sid}'
    manifest_path = root / folder / 'manifest.json'
    old = json.loads(h.regular(manifest_path).read_text(encoding='utf-8')) if manifest_path.exists() else None
    data = native(source, sid, root)
    identity = dict(agent=AGENT, session_id=sid, project_sha256=digest(h.base.canonical(root)))
    hashes = [digest(h.packed(e)) for e in data['events']]
    if old:
        if any(old.get(k) != v for k, v in identity.items()):
            raise ValueError('Market manifest ownership mismatch')
        previous = old['event_hashes']
        if hashes[:len(previous)] != previous or len(hashes) < len(previous):
            raise ValueError('Visible history rewrite/shrink; no history overwritten')
        with source.open('rb') as stream:
            raw_prefix = stream.read(old['source_bytes'])
        if digest(raw_prefix) != old['source_prefix_sha256']:
            raise ValueError('Native prefix changed; no ownership repair attempted')
    owner = f'<!-- codex-market-export-v1 project={identity["project_sha256"]} session={sid} -->'
    target = root / folder / 'transcript.md'
    if target.exists() and not target.read_text(encoding='utf-8').startswith(owner):
        raise ValueError('Existing transcript ownership mismatch')
    files, turn_index = {}, []
    full = owner + f'\n# Session\n\nsession_id: {sid}\nagent: {AGENT}\nstarted_at: {data["started_at"]}\n\n'
    for turn in data['turns']:
        text = render_turn(turn)
        name = f'collaboration/live-turns/codex-market/{sid}/{turn["turn_id"]}.md'
        info = put_document(root, name, text, lambda i, n=name: n[:-3] + f'/part-{i:04d}.md', files)
        turn_index.append(dict(turn_id=turn['turn_id'], **info))
        full += text + '\n---\n\n'
    document = put_document(root, folder + '/transcript.md', full,
                            lambda i: folder + f'/parts/part-{i:04d}.md', files)
    # The root index also has its own immutable ownership marker.
    if document['parts']:
        index = (root / document['path']).read_text(encoding='utf-8')
        put(root, document['path'], owner + '\n' + index, files)
    latest = next((e for e in reversed(data['events']) if e['kind'] == 'assistant'), None)
    latest_turn = next((t['turn_id'] for t in reversed(data['turns']) if latest in t['events']), None) if latest else None
    latest_text = (latest or {}).get('text', '')
    latest_name = 'collaboration/live-latest/codex-market.md'
    pointer = (f'# Codex Market — full latest visible response\n\nsession_id: {sid}\nturn_id: {latest_turn}\n'
               f'timestamp: {(latest or {}).get("timestamp")}\nstatus: LOCAL_ONLY\ncurrent task: {task}\n'
               f'transcript path: {folder}/transcript.md\nlatest commit SHA: PENDING\n'
               'remote verification status: PENDING\nfinal_response_captured: unknown (active session)\n\n'
               '## Full latest visible response\n\n' + fence(latest_text))
    put(root, latest_name, pointer, files)
    manifest = dict(schema_version=1, **identity, started_at=data['started_at'], exported_at=h.now(),
                    source_bytes=data['source_bytes'], source_prefix_sha256=data['source_prefix_sha256'],
                    source_complete=data['source_complete'], event_hashes=hashes,
                    visible_event_count=len(hashes), turn_count=len(data['turns']),
                    user_prompt_count=sum(e['kind'] == 'user' for e in data['events']),
                    assistant_response_count=sum(e['kind'] == 'assistant' for e in data['events']),
                    tool_event_count=sum(e['kind'].startswith('tool_') for e in data['events']),
                    latest_turn_id=latest_turn, latest_event_id=(latest or {}).get('event_id'),
                    latest_response_sha256=digest(latest_text), transcript=document, turns=turn_index,
                    files=files, status='LOCAL_ONLY', secret_scan='PASS', backfill_complete=True,
                    final_response_captured='unknown', runtime=runtime,
                    scope='Complete sanitized visible snapshot; no internal messages or future-response claim',
                    upstream_truncation_event_ids=[e['event_id'] for e in data['events'] if e['kind']=='tool_result' and re.search(r'(?i)output truncated|truncated output|original token count', e['text'])])
    h.write_json(manifest_path, manifest)
    return manifest, list(files) + [folder + '/manifest.json']


def readback(root, commit, names):
    """Fetch exact immutable GitHub blob bytes through native gh auth; never read credentials."""
    url = git(root, 'remote', 'get-url', 'origin')
    match = re.fullmatch(r'https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?', url)
    if not match:
        raise ValueError('Unsupported GitHub origin')
    repo = match[1]
    verified = {}
    for name in names:
        expected = (root / name).read_bytes()
        oid = git(root, 'rev-parse', commit + ':' + name)
        result = subprocess.run([trusted_executable('gh'), 'api', f'repos/{repo}/git/blobs/{oid}'],
                                capture_output=True, timeout=90, stdin=subprocess.DEVNULL)
        if result.returncode:
            raise SyncError('GitHub blob readback failed; response withheld')
        value = json.loads(result.stdout)
        content = base64.b64decode(value['content'])
        if value.get('sha') != oid or content != expected:
            raise SyncError('GitHub readback bytes differ')
        verified[name] = digest(content)
    return verified


def snapshot(source, sid, root, runtime=None):
    control = Path(git(root, 'rev-parse', '--git-common-dir'))
    if not control.is_absolute():
        control = root / control
    with h.lease(control / 'agent-transcript-publish.lock'):
        manifest, names = export(source, sid, root, runtime=runtime)
        payload = live.publish(root, names, 'logs: backfill full codex-market visible history', namespace=AGENT)
        verified = readback(root, payload, names)
        folder = f'collaboration/codex-market-sessions/{sid}'
        manifest.update(status='SYNC_COMPLETE', payload_commit_sha=payload, remote_sha_verified=True,
                        github_readback_verified=True, verified_at=h.now(), readback_files=verified)
        pointer = root / 'collaboration/live-latest/codex-market.md'
        text = pointer.read_text(encoding='utf-8').replace('status: LOCAL_ONLY', 'status: SYNC_COMPLETE')
        text = text.replace('latest commit SHA: PENDING', 'latest commit SHA: ' + payload)
        text = text.replace('remote verification status: PENDING', 'remote verification status: SHA and full GitHub blob bytes verified')
        h.atomic(pointer, text)
        # Update its content digest after bounded metadata addition.
        manifest['files']['collaboration/live-latest/codex-market.md'] = digest(text)
        h.write_json(root / folder / 'manifest.json', manifest)
        receipts = [folder + '/manifest.json', 'collaboration/live-latest/codex-market.md']
        receipt = live.publish(root, receipts, 'logs: verify codex-market snapshot and readback', namespace=AGENT)
        readback(root, receipt, receipts)
        return dict(session_id=sid, turn_count=manifest['turn_count'], visible_event_count=manifest['visible_event_count'],
                    payload_commit_sha=payload, latest_commit_sha=receipt, remote_verified=True,
                    secret_scan='PASS', backfill_complete=True, latest_turn_id=manifest['latest_turn_id'])


def message_key(source, sid, root):
    data = native(source, sid, root)
    return next((e['event_id'] for e in reversed(data['events']) if e['kind'] in {'user', 'assistant'}), None)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, default=Path.cwd())
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--session-id', required=True)
    p.add_argument('--watch', action='store_true')
    p.add_argument('--owner-pid', type=int)
    p.add_argument('--owner-birth')
    p.add_argument('--max-runtime', type=int, default=28800)
    p.add_argument('--export-only', action='store_true')
    args = p.parse_args()
    root, source, sid = args.project.resolve(), args.source.resolve(), args.session_id
    if args.export_only:
        manifest, _ = export(source, sid, root)
        print(json.dumps({k: manifest[k] for k in ('session_id', 'turn_count', 'visible_event_count', 'secret_scan')}))
        return
    if not args.watch:
        print(json.dumps(snapshot(source, sid, root)))
        return
    if not args.owner_pid or not args.owner_birth or args.max_runtime <= 0 or process_birth(args.owner_pid) != args.owner_birth:
        raise ValueError('Live owner PID/birth identity is not verified')
    control = Path(git(root, 'rev-parse', '--git-common-dir'))
    if not control.is_absolute():
        control = root / control
    expiry = (datetime.now(timezone.utc) + timedelta(seconds=args.max_runtime)).isoformat()
    runtime = dict(owner_pid=args.owner_pid, owner_birth=args.owner_birth, watcher_pid=os.getpid(), expires_at=expiry)
    receipt_path = control / ('codex-market-live-' + sid + '.json')
    with h.lease(control / ('codex-market-live-' + sid + '.lock')):
        start, last_key, pending, seen = time.monotonic(), None, None, None
        # Final response is flushed after the native writer emits it, including after
        # this agent turn ends. No claim is made about an unobserved future response.
        while process_birth(args.owner_pid) == args.owner_birth and time.monotonic() - start < args.max_runtime:
            key = message_key(source, sid, root)
            if key != seen:
                seen, pending = key, time.monotonic()
            if pending is not None and time.monotonic() - pending >= 3 and key != last_key:
                try:
                    result = snapshot(source, sid, root, runtime)
                    h.write_json(receipt_path, dict(**result, runtime=runtime, updated_at=h.now(), status='SYNC_COMPLETE'))
                    last_key, pending = key, None
                except Exception as exc:
                    # Busy writer: defer without stealing its lock. Any other failure stops.
                    if str(exc) != 'History writer already active; never steal a lock by age':
                        h.write_json(receipt_path, dict(status='FAILED', error_type=type(exc).__name__, updated_at=h.now()))
                        raise
            time.sleep(1)
        h.write_json(receipt_path, dict(status='STOPPED', runtime=runtime, updated_at=h.now(), reason='Owner exited or bounded runtime elapsed'))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('LOCAL ONLY - NOT SYNCED: ' + type(exc).__name__ + '; inspect sanitized evidence, no raw output.', flush=True)
        raise SystemExit(1)
