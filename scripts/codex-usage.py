#!/usr/bin/env python3
"""One-shot usage footer: native Codex quota RPC + local ccusage statistics."""
import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('session_export', ROOT / 'scripts/export-codex-session.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def native_codex():
    direct = shutil.which('codex.exe')
    if direct:
        return direct
    shim = shutil.which('codex.cmd') or shutil.which('codex')
    if shim:
        # Read-only discovery of the existing npm package's native executable.
        candidates = list(Path(shim).parent.glob('node_modules/@openai/codex/node_modules/@openai/codex-win32-*/vendor/*/bin/codex.exe'))
        if len(candidates) == 1:
            return str(candidates[0])
    return None


def quota_snapshot(timeout=20):
    """Only initialize + read rate limits. No thread, login, reset, token extraction."""
    executable = native_codex()
    if not executable:
        return None
    process = None
    reader = None
    messages = queue.Queue(maxsize=64)
    try:
        process = subprocess.Popen([executable, '--no-daemon', 'app-server', '--listen', 'stdio://'],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   text=True, encoding='utf-8', creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        def read_lines():
            try:
                while True:
                    line = process.stdout.readline(1024 * 1024 + 1)
                    if not line or len(line) > 1024 * 1024:
                        break
                    try:
                        messages.put_nowait(json.loads(line))
                    except (ValueError, queue.Full):
                        continue
            except (OSError, ValueError):
                pass
        reader = threading.Thread(target=read_lines, daemon=True)
        reader.start()
        deadline = time.monotonic() + timeout
        def send(value):
            process.stdin.write(json.dumps(value) + '\n')
            process.stdin.flush()
        def response(identifier):
            while time.monotonic() < deadline:
                item = messages.get(timeout=max(0.01, deadline - time.monotonic()))
                if isinstance(item, dict) and item.get('id') == identifier:
                    return item.get('result') if 'error' not in item else None
            return None
        send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'codex_project_usage', 'version': '1.0'}}})
        if response(1) is None:
            return None
        send({'method': 'initialized'})
        send({'id': 2, 'method': 'account/rateLimits/read'})
        return response(2)
    except (OSError, ValueError, queue.Empty, BrokenPipeError):
        return None
    finally:
        if process is not None:
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
            for stream in (process.stdin, process.stdout):
                if stream:
                    stream.close()
        if reader is not None:
            reader.join(timeout=1)


def quota_percentages(snapshot):
    result = {'5H': None, 'Weekly': None}
    if not isinstance(snapshot, dict):
        return result
    buckets = snapshot.get('rateLimitsByLimitId')
    bucket = buckets.get('codex') if isinstance(buckets, dict) else snapshot.get('rateLimits')
    if not isinstance(bucket, dict) or bucket.get('limitId') not in {None, 'codex'}:
        return result
    for label, minutes in (('5H', 300), ('Weekly', 10080)):
        windows = [w for w in (bucket.get('primary'), bucket.get('secondary'))
                   if isinstance(w, dict) and w.get('windowDurationMins') == minutes]
        if len(windows) != 1:
            continue
        used = windows[0].get('usedPercent')
        reset = windows[0].get('resetsAt')
        if (type(used) in (int, float) and math.isfinite(used) and 0 <= used <= 100 and
                type(reset) in (int, float) and math.isfinite(reset) and reset > time.time()):
            result[label] = round(100 - used, 1)  # remaining %, never derived from tokens
    return result


def project_sessions():
    source = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex') / 'sessions'
    found = []
    for path in source.rglob('*.jsonl'):
        if path.is_symlink():
            continue
        try:
            with path.open(encoding='utf-8-sig') as stream:
                header = json.loads(stream.readline())
            meta = header.get('payload', {})
            if header.get('type') == 'session_meta' and exporter.project_for(meta['cwd']) == exporter.canonical(ROOT):
                sid = meta.get('id', '')
                if re.fullmatch(r'[A-Za-z0-9-]{8,80}', sid):
                    found.append((path.stat().st_mtime_ns, sid))
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return sorted(found, reverse=True)


def session_tokens(report, sid):
    if not isinstance(report, dict):
        return None
    matches = [s for s in report.get('sessions', []) if isinstance(s, dict) and
               any(str(s.get(k, '')).endswith(sid) for k in ('sessionId', 'sessionFile'))]
    if len(matches) != 1:
        return None
    value = matches[0].get('totalTokens')
    return value if type(value) is int and value >= 0 else None


def local_usage(sid=None):
    sessions = project_sessions()
    eligible = {s for _, s in sessions}
    selected = sid or os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_SESSION_ID')
    if selected and selected not in eligible:
        return None, None
    if not selected:
        selected = sessions[0][1] if sessions else None
    if not selected:
        return None, None
    shim = shutil.which('ccusage.cmd') or shutil.which('ccusage')
    if not shim:
        return selected, None
    try:
        # npm Windows .cmd is invoked through cmd.exe using only fixed arguments.
        command = [shim, 'codex', 'session', '--offline', '--json', '--no-cost']
        if Path(shim).suffix.lower() == '.cmd':
            command = ['cmd.exe', '/d', '/s', '/c', subprocess.list2cmdline(command)]
        p = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
        return selected, session_tokens(json.loads(p.stdout.decode('utf-8-sig')), selected) if p.returncode == 0 else None
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return selected, None


def footer(quotas, tokens):
    def percent(value):
        return 'UNKNOWN' if value is None else f'{value:g}%'
    count = 'UNKNOWN' if tokens is None else f'{tokens:,}'
    return f'5H {percent(quotas["5H"])} | Weekly {percent(quotas["Weekly"])} | Session {count} tokens'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session-id')
    parser.add_argument('--offline-quota', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    snapshot = None if args.offline_quota else quota_snapshot()
    quotas = quota_percentages(snapshot)
    sid, tokens = local_usage(args.session_id)
    line = footer(quotas, tokens)
    if args.json:
        print(json.dumps({'fiveHourRemainingPercent': quotas['5H'], 'weeklyRemainingPercent': quotas['Weekly'],
                          'sessionId': sid, 'sessionTokens': tokens, 'footer': line,
                          'quotaSource': 'codex-account-rateLimits' if snapshot else 'UNKNOWN'}))
    else:
        print(line)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
