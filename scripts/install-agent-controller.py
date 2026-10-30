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

from agent_security import control_files,verify_control,git_prefix


def install(root,target_base=None):
    root=Path(root).resolve()
    policy=json.loads((root/'automation/policy.json').read_text(encoding='utf-8'))
    verify_control(root,policy)
    head=policy['approval']['reviewed_head']
    if len(head)!=40 or any(x not in '0123456789abcdef' for x in head):
        raise ValueError('Invalid reviewed commit')
    # The exact reviewed implementation must already exist on GitHub history.
    prefix=git_prefix(root)
    remote=subprocess.check_output(prefix+['ls-remote','origin','refs/heads/main'],cwd=root).decode().split()[0]
    subprocess.run(prefix+['fetch','--no-tags','origin',remote],cwd=root,check=True,capture_output=True)
    subprocess.run(prefix+['merge-base','--is-ancestor',head,remote],cwd=root,check=True,capture_output=True)
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
    args=parser.parse_args()
    print(install(args.workspace))
