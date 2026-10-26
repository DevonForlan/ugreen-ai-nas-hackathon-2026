#!/usr/bin/env python3
"""Fail-closed heuristic scanning of working files, index blobs and commits."""
import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess

RULES = {
    'provider-token': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b'),
    'jwt': re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'),
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----'),
    'url-credentials': re.compile(r'\b[a-zA-Z][a-zA-Z0-9+.-]*://[^\s/@]+:[^\s/@]+@'),
    'auth-header': re.compile(r'(?im)\b(?:authorization|proxy-authorization|cookie|set-cookie)\s*:\s*(?!\[REDACTED\])(?:Bearer\s+|Basic\s+)?[A-Za-z0-9_/+=.-]+'),
    'bearer-token': re.compile(r'(?i)\bBearer\s+(?!\[REDACTED\])[A-Za-z0-9_./+=-]{12,}'),
}
ASSIGN = re.compile(r'''(?ix)
    ["']?\b(?:[\w.-]*(?:api[_-]?key|access[_-]?key(?:[_-]?id)?|secret(?:[_-]?access[_-]?key)?|password|passwd|pwd|token|credential)|AccountKey|User\s+ID|UID)["']?
    \s*[:=]\s*(?:"([^"\r\n]*)"|'([^'\r\n]*)'|([^\s,;\r\n}\]]+))
''')
PLACEHOLDERS = {'', '[REDACTED]', '[REDACTED', 'PENDING', 'None', 'null', 'true', 'false', 'REDACTED', '...', 'changeme', 'example', 'YOUR_TOKEN', 'YOUR_API_KEY', 'ghp_', 'sk-'}
MAX_BYTES = 10 * 1024 * 1024
CACHE = {}


def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if p.returncode:
        raise RuntimeError('Git scan input failed; inspect Git configuration locally')
    return p.stdout


def forbidden(path):
    p = PurePosixPath(path.replace('\\', '/').lower())
    parts, name = p.parts, p.name
    if any(x in {'.codex', '.aws', '.ssh'} for x in parts):
        return 'forbidden-runtime-or-auth-path'
    if '.claude' in parts and ('conversation-logs' in parts or name == 'settings.local.json'):
        return 'unfiltered-claude-runtime'
    if (name == '.env' or (name.startswith('.env.') and name != '.env.example') or
            name == 'auth.json' or name.startswith(('credentials', 'secrets', 'id_rsa', 'id_ed25519')) or
            name.endswith(('.pem', '.key', '.p12', '.pfx', '.credentials.json', '.jsonl', '.jsonl.zst')) or
            name in {'cookies.txt', 'cookies.json', 'environment-dump.txt', 'env-dump.txt'}):
        return 'forbidden-credential-or-raw-file'
    if path.replace('\\', '/').startswith(('collaboration/codex-sessions/', 'collaboration/codex-reports/')) and p.suffix != '.md':
        return 'non-markdown-collaboration-file'
    return None


def scan_text(text):
    findings = []
    for rule, pattern in RULES.items():
        for m in pattern.finditer(text):
            findings.append((text.count('\n', 0, m.start()) + 1, rule))
    for m in ASSIGN.finditer(text):
        value = next((v for v in m.groups() if v is not None), '')
        if (value in PLACEHOLDERS or value.startswith(('[REDACTED]', '${', '$env:', 'os.environ', 'process.env', 're.', 'r\'', 'r"')) or
                re.fullmatch(r'[A-Za-z_][\w.]*\([^\r\n]*', value) or value in {'{', '[', 'r', 'f'}):
            continue
        if value:
            findings.append((text.count('\n', 0, m.start()) + 1, 'credential-assignment'))
    return sorted(set(findings))


def scan_blob(path, data, mode='100644'):
    rule = forbidden(path)
    if rule:
        return [(path, 1, rule)]
    if mode not in {'100644', '100755'}:
        return [(path, 1, 'unsupported-symlink-or-submodule')]
    if len(data) > MAX_BYTES or b'\x00' in data:
        return [(path, 1, 'unscannable-binary-or-oversize')]
    try:
        text = data.decode('utf-8-sig')
    except UnicodeError:
        return [(path, 1, 'non-utf8-content')]
    return [(path, line, rule) for line, rule in scan_text(text)]


def scan_repo(root, staged=False, revision=None):
    findings, count = [], 0
    if staged or revision:
        raw = git(root, 'ls-files', '--stage', '-z') if staged else git(root, 'ls-tree', '-r', '-z', revision)
        entries = []
        for entry in raw.split(b'\x00'):
            if not entry:
                continue
            meta, path = entry.split(b'\t', 1)
            fields = meta.decode().split()
            mode, oid = fields[:2] if staged else (fields[0], fields[2])
            name = path.decode('utf-8')
            entries.append((name, oid, mode))
        pending = sorted({oid for name, oid, mode in entries if (name, oid, mode) not in CACHE and mode in {'100644', '100755', '120000'}})
        blobs = {}
        if pending:
            result = subprocess.run(['git', '-C', str(root), 'cat-file', '--batch'], input=('\n'.join(pending) + '\n').encode(), capture_output=True)
            if result.returncode:
                raise RuntimeError('Cannot read index/commit objects')
            offset = 0
            for oid in pending:
                end = result.stdout.index(b'\n', offset)
                header = result.stdout[offset:end].split()
                if len(header) != 3 or header[1] != b'blob':
                    raise RuntimeError('Unsupported Git object')
                size = int(header[2])
                blobs[oid] = result.stdout[end + 1:end + 1 + size]
                offset = end + size + 2
        for name, oid, mode in entries:
            key = (name, oid, mode)
            if key not in CACHE:
                CACHE[key] = scan_blob(name, blobs.get(oid, b''), mode)
            findings.extend(CACHE[key])
            count += 1
    else:
        names = git(root, 'ls-files', '--cached', '--others', '--exclude-standard', '-z')
        for name in sorted(set(x.decode('utf-8') for x in names.split(b'\x00') if x)):
            path = root / name
            if not path.exists() and not path.is_symlink():
                continue
            mode = '120000' if path.is_symlink() else '100644'
            if forbidden(name) or mode == '120000':
                data = b''
            elif path.is_file():
                with path.open('rb') as stream:
                    data = stream.read(MAX_BYTES + 1)
            else:
                data = b''
            findings.extend(scan_blob(name, data, mode))
            count += 1
    return count, findings


def show(count, findings):
    for path, line, rule in findings:
        print(f'{path}:{line}: {rule}')
    print(f'Secret scan: files={count} findings={len(findings)} (heuristic)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*')
    parser.add_argument('--worktree', action='store_true')
    parser.add_argument('--staged', action='store_true')
    parser.add_argument('--revision')
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.worktree or args.staged or args.revision:
            count, findings = scan_repo(root, args.staged, args.revision)
        else:
            files = [Path(x) for x in args.files] if args.files else [*root.glob('collaboration/codex-sessions/*.md'), *root.glob('collaboration/codex-reports/*.md')]
            findings = [f for p in files for f in scan_blob(str(p), p.read_bytes())]
            count = len(files)
        show(count, findings)
        return 1 if findings else 0
    except (OSError, RuntimeError, UnicodeError, ValueError):
        print('Secret scan failed closed: unable to read or decode input; no secret values printed.')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
