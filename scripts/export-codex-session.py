#!/usr/bin/env python3
"""Read-only Codex JSONL -> sanitized project Markdown; Python stdlib only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

REDACTED = '[REDACTED]'
SENSITIVE = r'(?:[A-Za-z0-9_.-]*(?:api[_-]?key|access[_-]?key|secret|password|passwd|pwd|token|credential|authorization|cookie|private[_-]?key)[A-Za-z0-9_.-]*|AccountKey|SharedAccessSignature|User\s+ID|UID)'
ASSIGN = re.compile(r'(?i)([\"\']?\b' + SENSITIVE + r'[\"\']?\s*[:=]\s*)(?:\[REDACTED\]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[^\s,;\r\n}\]]+)')
PATTERNS = [
    (re.compile(r'-----BEGIN (?:[A-Z0-9 ]*PRIVATE KEY)-----[\s\S]*?(?:-----END [A-Z0-9 ]*PRIVATE KEY-----|\Z)'), REDACTED),
    (re.compile(r'(?im)\b(?:Authorization|Proxy-Authorization|Cookie|Set-Cookie)\s*:[^\r\n]*'), REDACTED),
    (re.compile(r'(?i)\b(?:Bearer|Basic)\s+[A-Za-z0-9_./+~=-]+'), REDACTED),
    (re.compile(r'\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{12,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b'), REDACTED),
    (re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'), REDACTED),
    (re.compile(r'(?i)([a-z][a-z0-9+.-]*://)[^\s/@]+:[^\s/@]+@'), r'\1[REDACTED]@'),
    (ASSIGN, r'\1[REDACTED]'),
]


def sanitize(text):
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return re.sub(r'<(system|developer|analysis|reasoning|internal_metadata)(?:\s[^>]*)?>[\s\S]*?(?:</\1>|\Z)', '[INTERNAL CONTENT OMITTED]', text, flags=re.I)


def safe_value(value):
    if isinstance(value, dict):
        return {k: (REDACTED if re.fullmatch(SENSITIVE, k, re.I) else safe_value(v))
                for k, v in value.items()
                if k.lower() not in {'reasoning', 'analysis', 'encrypted_content', 'system', 'developer',
                                      'system_prompt', 'base_instructions', 'developer_instructions', 'instructions', 'metadata',
                                      'internal_chat_message_metadata_passthrough'}}
    if isinstance(value, list):
        return [safe_value(v) for v in value]
    if isinstance(value, str):
        return sanitize(value)
    return value


def printable(value):
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except ValueError:
            return sanitize(value)
        if isinstance(parsed, (dict, list)):
            return sanitize(json.dumps(safe_value(parsed), ensure_ascii=False, indent=2))
        return sanitize(value)
    return sanitize(json.dumps(safe_value(value), ensure_ascii=False, indent=2))


def canonical(path):
    return os.path.normcase(str(Path(path).resolve()))


def project_for(cwd):
    p = Path(cwd).resolve()
    for parent in (p, *p.parents):
        if (parent / '.git').exists():
            return canonical(parent)
    return canonical(p)


def records(path, stats, limit=None):
    with path.open('rb') as stream:
        while limit is None or stream.tell() < limit:
            line = stream.readline(-1 if limit is None else limit - stream.tell())
            if not line:
                break
            try:
                item = json.loads(line.decode('utf-8-sig'))
                if isinstance(item, dict):
                    yield item
            except (ValueError, UnicodeError):
                stats['malformed_lines'] += 1


def text_content(content):
    if isinstance(content, str):
        return content
    return '\n'.join(x.get('text', '') for x in content or []
                     if isinstance(x, dict) and x.get('type') in {'input_text', 'output_text', 'text'})


def fenced(text):
    fence = '`' * (max([len(x) for x in re.findall(r'`+', text)] + [2]) + 1)
    return f'{fence}text\n{text}\n{fence}\n'


def export_one(source, project, output, stats):
    meta = None
    last = None
    ended = None
    # Both passes use the same byte boundary while an active rollout is appended.
    limit = source.stat().st_size
    # Validate ownership before extracting visible content. Mixed-project sessions fail closed.
    for e in records(source, stats, limit):
        p = e.get('payload', {})
        if not isinstance(p, dict):
            continue
        if e.get('type') == 'session_meta':
            if meta is not None:
                raise ValueError('Multiple session metadata records')
            meta = {k: p.get(k) for k in ('id', 'cwd', 'timestamp')}
        if e.get('timestamp'):
            last = e['timestamp']
        if e.get('type') == 'event_msg' and p.get('type') == 'session_end':
            ended = e.get('timestamp')
        if e.get('type') in {'session_meta', 'turn_context'} and p.get('cwd'):
            if project_for(p['cwd']) != canonical(project):
                stats['other_or_mixed_project'] += 1
                return
    if not meta or not meta.get('cwd') or project_for(meta['cwd']) != canonical(project):
        stats['unidentified'] += 1
        return
    sid = meta.get('id', '')
    start = str(meta.get('timestamp') or '')
    if not re.fullmatch(r'[A-Za-z0-9-]{8,80}', sid) or not re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', start):
        raise ValueError('Unsupported session ID or timestamp')
    owner = hashlib.sha256(canonical(project).encode()).hexdigest()
    marker = f'<!-- codex-export-v1 project={owner} session={sid} -->'
    target = output / f'{start[:10]}_{start[11:13]}{start[14:16]}_{sid}.md'
    if target.is_symlink() or (target.exists() and target.read_text(encoding='utf-8').splitlines()[0] != marker):
        raise ValueError('Destination ownership mismatch')
    parts = [marker, '# Codex Session', f'- Session ID: {sid}', f'- Start time: {start}',
             f'- End time: {ended or "Not recorded (last event is not an end time)"}',
             f'- Last recorded event: {last}', f'- Working directory: {sanitize(meta["cwd"])}',
             '- Timestamp timezone: preserved from source (usually UTC).',
             '- Export: visible text and tools only; sanitized; unknown/internal events omitted.', '']
    # Response items are canonical; duplicate event_msg transcript copies are omitted.
    for e in records(source, {'malformed_lines': 0}, limit):
        p = e.get('payload', {})
        if not isinstance(p, dict):
            continue
        kind, t = e.get('type'), p.get('type')
        label = value = None
        if kind == 'response_item':
            if t == 'message' and p.get('role') in {'user', 'assistant'} and p.get('channel') not in {'analysis', 'reasoning'}:
                label = 'User prompt' if p['role'] == 'user' else 'Codex response'
                value = text_content(p.get('content'))
            elif t in {'function_call', 'custom_tool_call'}:
                label = 'Tool / command call'
                value = {k: p[k] for k in ('name', 'call_id') if k in p}
                value['input'] = printable(p.get('arguments', p.get('input', '')))
            elif t in {'function_call_output', 'custom_tool_call_output'}:
                label = 'Tool / command result (including errors and test output)'
                value = {k: p[k] for k in ('call_id', 'output') if k in p}
        elif kind == 'event_msg' and t in {'error', 'warning', 'turn_aborted'}:
            label = 'Error / warning / interruption'
            value = {k: p[k] for k in ('message', 'error', 'reason') if k in p}
        if label and value:
            parts += [f'## {label} — {sanitize(str(e.get("timestamp", "")))}', fenced(printable(value))]
    rendered = sanitize('\n'.join(parts))
    if target.exists() and target.read_text(encoding='utf-8') == rendered:
        stats['unchanged'] += 1
        return
    # Temporary files contain only already-sanitized text.
    fd, tmp = tempfile.mkstemp(prefix='.codex-export-', suffix='.tmp', dir=output)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(rendered)
        os.replace(tmp, target)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    stats['written'] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path.cwd(), help='Git root, defaults to cwd')
    parser.add_argument('--source', type=Path, help='Default: CODEX_HOME/sessions or ~/.codex/sessions')
    args = parser.parse_args()
    project = args.project.resolve()
    if not (project / '.git').exists():
        parser.error('--project must be a Git repository root')
    source = (args.source or Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex') / 'sessions').resolve()
    if not source.is_dir():
        parser.error('Session source directory does not exist')
    output = project / 'collaboration' / 'codex-sessions'
    output.mkdir(parents=True, exist_ok=True)
    if output.resolve() != output.absolute():
        parser.error('Output must not traverse a symlink/junction')
    stats = dict(scanned=0, written=0, unchanged=0, other_or_mixed_project=0, unidentified=0, malformed_lines=0, failures=0)
    for path in sorted(source.rglob('*.jsonl')):
        if path.is_symlink():
            continue
        stats['scanned'] += 1
        try:
            export_one(path, project, output, stats)
        except (OSError, ValueError, TypeError, IndexError) as exc:
            stats['failures'] += 1
            print(f'Export skipped: {type(exc).__name__}')
    print(json.dumps(stats, sort_keys=True))
    return 1 if stats['failures'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
