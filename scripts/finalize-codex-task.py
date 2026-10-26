#!/usr/bin/env python3
"""Implementation for the PowerShell finalize entrypoint. Never force-push."""
import argparse
import hashlib
import importlib.util
import json
from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('secret_scan', ROOT / 'scripts/scan-codex-secrets.py')
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)
export_spec = importlib.util.spec_from_file_location('codex_export', ROOT / 'scripts/export-codex-session.py')
exporter = importlib.util.module_from_spec(export_spec)
export_spec.loader.exec_module(exporter)
HEADINGS = ['Task', 'Objective', 'Request', 'Work Completed', 'Findings', 'Files Changed', 'Commands Executed', 'Tests', 'Git Diff Summary', 'Known Issues', 'Security Notes', 'Open Questions', 'Pending User Decisions', 'Recommended Reviewer Scope', 'Recommended Next Step', 'Git Commit']
STATUS = ['Current Phase', 'Current Objective', 'Completed', 'In Progress', 'Blockers', 'Pending User Decisions', 'Next Planned Step']


class SecurityScanError(RuntimeError):
    pass


def failure_status(phase, task_committed, error):
    return 'WARNING' if phase == 'PUSH' and task_committed and not isinstance(error, SecurityScanError) else 'FAILED'


def run(args, capture=False):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never', PYTHONIOENCODING='utf-8')
    env.setdefault('GIT_SSH_COMMAND', 'ssh -o BatchMode=yes')
    limit = 1800 if args[1:3] == ['-m', 'unittest'] else 600
    p = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, stdin=subprocess.DEVNULL, timeout=limit)
    if p.returncode:
        if len(args) > 1 and args[1] == 'scripts/scan-codex-secrets.py':
            print(p.stdout.decode('utf-8', errors='replace'), flush=True)
        if args[1:3] == ['-m', 'unittest']:
            print('Tests failed; commit and push stopped.', flush=True)
            print(exporter.sanitize((p.stdout + p.stderr).decode('utf-8', errors='replace'))[:16000], flush=True)
        raise RuntimeError(f'Command failed (exit {p.returncode}): {args[0]} {args[1] if len(args) > 1 else ""}; inspect locally without sharing credentials')
    output = p.stdout.decode('utf-8', errors='replace')
    if args[1:3] == ['-m', 'unittest']:
        output += p.stderr.decode('utf-8', errors='replace')
    if not capture and output:
        display = exporter.sanitize(output)
        print(display[:24000], end='' if display.endswith('\n') else '\n', flush=True)
        if len(output) > 24000:
            print('[display truncated; scans always inspect full content]')
    return output.strip() if capture else output


def git(*args, capture=True):
    return run(['git', *args], capture=capture)


def scan(staged=False, revision=None, reset=False):
    count, findings = scanner.scan_repo(ROOT, staged, revision)
    scanner.show(count, findings)
    if findings:
        if reset:
            git('reset', capture=True)
        raise SecurityScanError('Secret/path scan blocked finalization; no secret values printed')


def validate_exports():
    directory = ROOT / 'collaboration/codex-sessions'
    owner = hashlib.sha256(exporter.canonical(ROOT).encode()).hexdigest()
    prefix = f'<!-- codex-export-v1 project={owner} session='
    for path in directory.iterdir():
        if path.is_symlink() or not path.is_file() or path.suffix.lower() != '.md':
            print(f'collaboration/codex-sessions/{path.name}:1: non-markdown-or-nonregular-export')
            raise RuntimeError('Session output directory must contain only sanitized Markdown')
        with path.open(encoding='utf-8') as stream:
            if not stream.readline().startswith(prefix):
                print(f'collaboration/codex-sessions/{path.name}:1: export-owner-mismatch')
                raise RuntimeError('Session Markdown has no matching exporter ownership marker')


def report_for(task):
    matches = sorted((ROOT / 'collaboration/codex-reports').glob(f'????-??-??_????_{task}.md'))
    if not matches:
        raise RuntimeError('Missing task report: YYYY-MM-DD_HHMM_<TaskId>.md')
    report = matches[-1]
    if not git('status', '--porcelain', '--', report.relative_to(ROOT).as_posix()):
        raise RuntimeError('Update the task report before finalizing')
    text = report.read_text(encoding='utf-8')
    for heading in HEADINGS:
        if heading == 'Git Commit' and '# Commit SHA' in text:
            continue  # Existing reports remain readable; new template uses Git Commit.
        if not re.search(r'^# ' + re.escape(heading) + r'\s*$', text, re.M):
            raise RuntimeError(f'Missing report section: {heading}')
    status = (ROOT / 'docs/00_PROJECT_STATUS.md').read_text(encoding='utf-8')
    for heading in STATUS:
        if f'## {heading}' not in status:
            raise RuntimeError(f'Missing project status section: {heading}')
    if 'Last Updated:' not in status:
        raise RuntimeError('Missing Last Updated in project status')
    changed = set(git('diff', '--name-only', 'HEAD').splitlines())
    if 'docs/00_PROJECT_STATUS.md' not in changed:
        raise RuntimeError('Update docs/00_PROJECT_STATUS.md for this task before finalizing')
    return report


def update_status_timestamp():
    path = ROOT / 'docs/00_PROJECT_STATUS.md'
    text = path.read_text(encoding='utf-8')
    stamp = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %z')
    updated = re.sub(r'(?m)^Last Updated:.*$', 'Last Updated: ' + stamp, text, count=1)
    if updated != text:
        path.write_text(updated, encoding='utf-8', newline='\n')


def push(branch):
    print('Step 8 - verify branch and remote', flush=True)
    git('branch', '--show-current', capture=False)
    if git('branch', '--show-current') != branch:
        raise RuntimeError('Branch changed during finalization; stop and inspect')
    remotes = git('remote', '-v')
    if scanner.scan_text(remotes) or re.search(r'https?://[^/@]+@', remotes):
        raise SecurityScanError('Remote contains embedded authentication; use credential manager')
    print(remotes, flush=True)
    if 'origin' not in git('remote').splitlines():
        raise RuntimeError('Missing origin remote')
    if git('remote', 'get-url', '--all', 'origin') != git('remote', 'get-url', '--push', '--all', 'origin'):
        raise RuntimeError('Origin fetch/push destinations differ; inspect configuration')
    remote_head = git('ls-remote', '--heads', 'origin', f'refs/heads/{branch}')
    if remote_head:
        git('fetch', '--no-tags', 'origin', f'refs/heads/{branch}')
        base = remote_head.split()[0]
        if git('rev-parse', 'FETCH_HEAD') != base:
            raise RuntimeError('Remote moved during verification; rerun without force')
        commits = git('rev-list', f'{base}..HEAD').splitlines()
    else:
        commits = git('rev-list', 'HEAD').splitlines()
    # Inspect every outgoing snapshot so a deleted secret in an ancestor cannot escape.
    for commit in commits:
        scan(revision=commit)
    git('push', '--set-upstream', 'origin', f'HEAD:refs/heads/{branch}')
    sha = git('rev-parse', 'HEAD')
    verified = git('ls-remote', '--heads', 'origin', f'refs/heads/{branch}')
    if not verified or verified.split()[0] != sha:
        raise RuntimeError('Remote SHA verification failed')
    print('Step 9 - verification', flush=True)
    git('status', capture=False)
    git('log', '-1', '--oneline', capture=False)
    print(f'Branch: {branch}\nCommit SHA: {sha}\nCommit message: {git("log", "-1", "--format=%s")}\nPush result: SYNCED (remote SHA verified)\nWorking tree status: {"CLEAN" if not git("status", "--porcelain") else "DIRTY"}', flush=True)
    if git('status', '--porcelain'):
        raise RuntimeError('Remote synced but working tree changed; local work remains')
    return sha


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--message')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--push-only', action='store_true')
    parser.add_argument('--result-name', help='Internal per-run result filename inside Git directory')
    args = parser.parse_args()
    outcome = {'status': 'FAILED', 'synced': False, 'taskCommitted': False}
    phase = 'VALIDATE'
    try:
        if args.result_name and not re.fullmatch(r'codex-finalize-[a-f0-9]{32}\.json', args.result_name):
            raise RuntimeError('Invalid result filename')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', args.task_id):
            raise RuntimeError('Invalid TaskId')
        if not os.path.samefile(git('rev-parse', '--show-toplevel'), ROOT):
            raise RuntimeError('Scripts must live directly under the target repository root')
        branch = git('branch', '--show-current')
        if not branch or git('diff', '--name-only', '--diff-filter=U'):
            raise RuntimeError('Detached HEAD or unresolved conflict')
        for state in ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply'):
            if (ROOT / git('rev-parse', '--git-path', state)).exists():
                raise RuntimeError('Finish the active Git operation first')
        message = args.message or f'chore: finalize Codex task {args.task_id}'
        if '\n' in message or '\r' in message or scanner.scan_text(message):
            raise RuntimeError('Unsafe commit message')
        if args.push_only:
            if git('status', '--porcelain'):
                raise RuntimeError('PushOnly requires a clean working tree')
            if args.dry_run:
                print('DRY RUN: push skipped')
                outcome['status'] = 'DRY_RUN'
            else:
                if any((ROOT / 'tests').glob('test_*.py')):
                    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'])
                phase = 'PUSH'
                outcome['taskCommitted'] = True
                outcome['commit'] = push(branch)
                outcome.update(status='SUCCESS', synced=True)
            return 0
        print('Step 1 - export sessions', flush=True)
        run([sys.executable, 'scripts/export-codex-session.py'])
        validate_exports()
        print('Step 2 - scan sanitized Markdown and all candidate working files', flush=True)
        run([sys.executable, 'scripts/scan-codex-secrets.py'])
        scan()
        print('Step 3 - git status', flush=True)
        git('status', '--short', capture=False)
        if not git('status', '--porcelain'):
            print('Nothing to commit')
            if args.dry_run:
                outcome['status'] = 'DRY_RUN'
                return 0
            upstream = subprocess.run(['git', 'rev-parse', '--abbrev-ref', '@{upstream}'], cwd=ROOT, capture_output=True)
            if upstream.returncode or git('rev-list', '@{upstream}..HEAD'):
                print('LOCAL ONLY — NOT SYNCED: use -PushOnly to verify/push existing commits')
                outcome['status'] = 'WARNING'
                return 1
            phase = 'PUSH'
            outcome['taskCommitted'] = True
            sha = git('rev-parse', 'HEAD')
            remote = git('ls-remote', '--heads', 'origin', f'refs/heads/{branch}')
            if not remote or remote.split()[0] != sha:
                raise RuntimeError('Nothing to commit, but remote SHA does not match')
            outcome.update(status='SUCCESS', synced=True, commit=sha)
            return 0
        report = report_for(args.task_id)
        if not args.dry_run:
            update_status_timestamp()
        if any((ROOT / 'tests').glob('test_*.py')):
            print('Run Python regression tests', flush=True)
            run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'])
            evidence = 'Finalize gate: Python unittest discovery PASS.'
            text = report.read_text(encoding='utf-8')
            if not args.dry_run and evidence not in text:
                report.write_text(text.replace('# Tests\n', '# Tests\n\n' + evidence + '\n', 1), encoding='utf-8', newline='\n')
        print('Step 4 - review diff and stat (untracked files were scanned too)', flush=True)
        scan(staged=True, reset=not args.dry_run)
        git('diff', capture=False)
        git('diff', '--stat', capture=False)
        git('diff', '--cached', capture=False)
        if args.dry_run:
            print('DRY RUN: export/scan/tests complete; no staging, commit, reset, or push')
            outcome['status'] = 'DRY_RUN'
            return 0
        print('Step 5 - stage all non-ignored, pre-scanned changes', flush=True)
        git('add', '-A')
        try:
            print('Step 6 - scan actual index blobs', flush=True)
            scan(staged=True)
            git('diff', '--cached', capture=False)
        except Exception:
            git('reset')
            raise
        print('Step 7 - commit', flush=True)
        git('commit', '-m', message)
        task_sha = git('rev-parse', 'HEAD')
        outcome.update(taskCommitted=True, taskCommit=task_sha)
        phase = 'METADATA'
        text = report.read_text(encoding='utf-8')
        text = re.sub(r'(?ms)(^# (?:Git Commit|Commit SHA)\s*\n).*?(?=^# |\Z)', lambda m: m[1] + '\n' + task_sha + '\n', text)
        report.write_text(text, encoding='utf-8', newline='\n')
        scan()
        git('add', '--', report.relative_to(ROOT).as_posix())
        scan(staged=True, reset=True)
        git('commit', '-m', f'chore: record {args.task_id} task commit')
        print(f'Task commit SHA: {task_sha}', flush=True)
        phase = 'PUSH'
        outcome['commit'] = push(branch)
        outcome.update(status='SUCCESS', synced=True)
        return 0
    except Exception as exc:
        outcome['status'] = failure_status(phase, outcome['taskCommitted'], exc)
        detail = str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__
        print(f'LOCAL ONLY — NOT SYNCED\n{detail}', flush=True)
        return 1
    finally:
        if args.result_name and re.fullmatch(r'codex-finalize-[a-f0-9]{32}\.json', args.result_name):
            try:
                path = ROOT / git('rev-parse', '--git-path', args.result_name)
                with path.open('x', encoding='utf-8') as stream:
                    json.dump(outcome, stream)
            except (OSError, RuntimeError):
                print('Finalize result metadata unavailable; see terminal status.')


if __name__ == '__main__':
    raise SystemExit(main())
