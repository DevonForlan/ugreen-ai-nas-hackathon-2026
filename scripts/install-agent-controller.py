#!/usr/bin/env python3
"""Operator-only: install the reviewed control plane outside agent-writable worktrees.

Run from a reviewed clean checkout before enabling any model. Future restarts use
this installed command, never a launcher that an interrupted model could edit.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import hashlib

from agent_security import control_files,verify_control,git_prefix,git_environment


def install(root,target_base=None,expect_policy_sha256=None):
    root=Path(root).resolve()
    policy=json.loads((root/'automation/policy.json').read_text(encoding='utf-8'))
    actual=hashlib.sha256((root/'automation/policy.json').read_bytes()).hexdigest()
    if not expect_policy_sha256 or expect_policy_sha256!=actual:
        raise ValueError('Operator must pin --expect-policy-sha256 from the reviewed published policy')
    verify_control(root,policy)
    head=policy['approval']['reviewed_head']
    if len(head)!=40 or any(x not in '0123456789abcdef' for x in head):
        raise ValueError('Invalid reviewed commit')
    # The exact reviewed implementation must already exist on GitHub history.
    prefix=git_prefix(root)
    env=dict(os.environ,**git_environment())
    remote=subprocess.check_output(prefix+['ls-remote','origin','refs/heads/main'],cwd=root,env=env).decode().split()[0]
    subprocess.run(prefix+['fetch','--no-tags','origin',remote],cwd=root,env=env,check=True,capture_output=True)
    subprocess.run(prefix+['merge-base','--is-ancestor',head,remote],cwd=root,env=env,check=True,capture_output=True)
    # The approval commit contains the independent report and the reviewed source.
    # Compare canonical Git text blobs, not just a self-consistent mutable manifest.
    for name in [*policy['control_plane_sha256'],policy['approval']['review_report']]:
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts or (root/relative).is_symlink():
            raise ValueError('Unsafe reviewed source path')
        committed=subprocess.check_output(prefix+['cat-file','blob',head+':'+relative.as_posix()],cwd=root,env=env)
        if (root/relative).read_bytes().replace(b'\r\n',b'\n')!=committed.replace(b'\r\n',b'\n'):
            raise ValueError('Installed source/review differs from the approved Git commit: '+name)
    print(json.dumps({'policy_sha256':actual,'reviewed_head':head,'plans':policy['plans'],
                      'allowed_task_prefixes':policy['allowed_task_prefixes']},sort_keys=True))
    base=Path(target_base or Path(os.environ['LOCALAPPDATA'])/'CodexAgentController')
    revision=head+'-'+hashlib.sha256((root/'automation/policy.json').read_bytes()).hexdigest()[:16]
    destination=(base/revision).resolve()
    if destination==root or destination.is_relative_to(root):
        raise ValueError('Trusted controller must be outside the worktree')
    if destination.exists():
        if control_files(destination)!=policy['control_plane_sha256'] or (destination/'automation/policy.json').read_bytes()!=(root/'automation/policy.json').read_bytes():
            raise ValueError('Do not overwrite an existing reviewed installation; install a new approved version')
        return destination
    destination.mkdir(parents=True)
    for name in [*policy['control_plane_sha256'],'automation/policy.json']:
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts or (root/relative).is_symlink():
            raise ValueError('Unsafe reviewed source path')
        target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(root/relative,target)
    if control_files(destination)!=policy['control_plane_sha256']:
        raise ValueError('Installed controller hash mismatch')
    return destination


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--expect-policy-sha256',required=True)
    args=parser.parse_args()
    print(install(args.workspace,expect_policy_sha256=args.expect_policy_sha256))
