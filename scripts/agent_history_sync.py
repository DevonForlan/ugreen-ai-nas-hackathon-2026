"""Bounded two-phase publication of sanitized transcript artifacts and receipts."""
import json
import os
from pathlib import Path
import re
import subprocess
from agent_security import git_prefix
from agent_transcripts import (archive, atomic, base, clean, complete, events, now, packed,
                               regular, render, scan, sha, write_json, lease)


class SyncError(RuntimeError):
    pass


class SecurityError(SyncError):
    pass


def git(root,*args):
    env = dict(os.environ,GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='Never')
    p = subprocess.run(git_prefix(root)+list(args),cwd=root,env=env,capture_output=True,timeout=600)
    if p.returncode:
        raise SyncError('Git operation failed: '+args[0]+'; credentials/output not logged')
    return p.stdout.decode('utf-8').strip()


def checked(root,staged=False,revision=None):
    count,findings = scan.scan_repo(root,staged,revision)
    if findings:
        scan.show(count,findings)
        raise SecurityError('Security scan failed; no secret values printed')


def verify_push(root,branch):
    remote = git(root,'ls-remote','origin','refs/heads/'+branch)
    if remote:
        base_sha = remote.split()[0]
        git(root,'fetch','--no-tags','origin',base_sha)
        git(root,'merge-base','--is-ancestor',base_sha,'HEAD')
        for commit in git(root,'rev-list',base_sha+'..HEAD').splitlines():
            checked(root,revision=commit)
    else:
        for commit in git(root,'rev-list','HEAD').splitlines():
            checked(root,revision=commit)
    git(root,'push','--set-upstream','origin','HEAD:refs/heads/'+branch)
    head = git(root,'rev-parse','HEAD')
    if git(root,'ls-remote','origin','refs/heads/'+branch).split()[0] != head:
        raise SyncError('Remote SHA did not verify')
    return head


def publish(item,ledger_path,value,project_path,extra_paths=()):
    with lease(item['directory']/'.archive.lock'):
        return _publish(item,ledger_path,value,project_path,extra_paths)


def _publish(item,ledger_path,value,project_path,extra_paths=()):
    """No model call and no whole-repo staging. Failure preserves work and stops.

    commit_sha pins the payload commit, never the ledger's own metadata commit.
    Only the verified payload can be certified in a subsequent bounded receipt commit.
    """
    root = Path(project_path).resolve()
    ledger_path = Path(ledger_path)
    transcript = item['transcript']
    names = [transcript.relative_to(root).as_posix(),ledger_path.relative_to(root).as_posix()]
    names += [Path(p).relative_to(root).as_posix() for p in extra_paths]
    if any(scan.forbidden(p) for p in names):
        raise SyncError('Unsafe publication path')
    if any(not p.startswith(('collaboration/codex-sessions/','collaboration/cc-sessions/','collaboration/cc-reports/','collaboration/run-ledger/')) for p in names):
        raise SyncError('Only transcript/review/ledger artifacts may be published here')
    try:
        if git(root,'diff','--cached','--name-only'):
            raise SyncError('Existing staging must be finalized separately; no reset performed')
        branch = git(root,'branch','--show-current')
        if not branch:
            raise SyncError('Detached branch cannot publish')
        remote = git(root,'remote','get-url','origin')
        if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?',remote):
            raise SyncError('Only credential-free GitHub HTTPS origin is supported')
        if git(root,'remote','get-url','--push','origin') != remote:
            raise SyncError('Fetch and push origins differ')
        # Restrict dirty tracked/untracked paths; preserve unrelated owner work.
        changed = set(git(root,'diff','--name-only','HEAD').splitlines())
        changed.update(git(root,'ls-files','--others','--exclude-standard').splitlines())
        if changed - set(names):
            raise SyncError('Unrelated local work must be finalized first')
        checked(root)
        value['secret_scan'] = 'PASS'
        value['transcript_sha256'] = sha(transcript.read_text(encoding='utf-8'))
        write_json(ledger_path,value)
        git(root,'status','--short')
        git(root,'diff','--',*names)
        git(root,'add','--',*names)
        checked(root,staged=True)
        git(root,'diff','--cached','--',*names)
        if git(root,'diff','--cached','--name-only'):
            git(root,'commit','-m',f'logs: capture {value["task_id"]} {value["agent"]} run')
        payload_sha = verify_push(root,branch)
        final_ready=(value['final_response_captured'] is True and bool(value['ended_at']) and value.get('malformed_events',0)==0)
        value.update(commit_sha=payload_sha,github_synced=final_ready,snapshot_uploaded=True,verified_at=now())
        value['status'] = 'SYNC_COMPLETE' if complete(value) else 'LOCAL_ONLY'
        # These flags certify the immutable payload, not this active Python process.
        atomic(transcript,render(item['session'],item['manifest'],root,synced=value['github_synced']))
        write_json(ledger_path,value)
        checked(root)
        git(root,'diff','--',*names)
        git(root,'add','--',*names)
        checked(root,staged=True)
        git(root,'diff','--cached','--',*names)
        if git(root,'diff','--cached','--name-only'):
            git(root,'commit','-m',f'logs: verify {value["task_id"]} transcript payload')
        receipt_sha = verify_push(root,branch)
        manifest = json.loads((item['directory']/'manifest.json').read_text(encoding='utf-8'))
        manifest['github_sync'][sha(base.canonical(root))] = dict(marker=item['session']['marker'],complete=value['github_synced'],
            commit_sha=payload_sha,receipt_commit_sha=receipt_sha,verified_at=value['verified_at'],
            turns={t['turn_id']:sha(t['events']) for t in item['session']['turns']})
        write_json(item['directory']/'manifest.json',manifest)
        return dict(commit=receipt_sha,payload_commit=payload_sha,status=value['status'])
    except Exception as exc:
        value.update(github_synced=False,status='FAILED' if isinstance(exc,SecurityError) else 'LOCAL_ONLY')
        if isinstance(exc,SecurityError):
            value['secret_scan']='FAILED'
        write_json(ledger_path,value)
        atomic(transcript,render(item['session'],item['manifest'],root,synced=False))
        raise
