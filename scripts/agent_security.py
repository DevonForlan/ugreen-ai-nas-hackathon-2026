"""Trusted controller checks. Inspect bytes without executing agent-written files."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import platform


def scope_snapshot(root):
    root=Path(root).resolve()
    result={}
    for directory,folders,files in os.walk(root,followlinks=False):
        base=Path(directory)
        relative=base.relative_to(root).as_posix()
        # Git objects are immutable data, not executable policy. Include all other
        # ignored/control files; never hide .vscode, bytecode, hooks or nested rules.
        if relative=='.git':
            folders[:]=[p for p in folders if p!='objects']
        for name in list(folders):
            path=base/name
            if path.is_symlink() or (hasattr(path,'is_junction') and path.is_junction()):
                result[path.relative_to(root).as_posix()]='LINK:'+os.readlink(path)
                folders.remove(name)
        for name in files:
            path=base/name;key=path.relative_to(root).as_posix()
            if path.is_symlink():
                result[key]='LINK:'+os.readlink(path)
            else:
                if path.stat().st_size>64*1024*1024:
                    raise ValueError('Scope file exceeds inspection bound')
                result[key]=hashlib.sha256(path.read_bytes()).hexdigest()
            if len(result)>100000:
                raise ValueError('Scope inventory exceeds inspection bound')
    # External core.hooksPath is never executed (controller forces an empty path),
    # but track the configured value too, rather than trusting a local config edit.
    p=subprocess.run(['git','-C',str(root),'-c','core.fsmonitor=false','config','--get','core.hooksPath'],capture_output=True,timeout=30)
    result['__agent_control__/configured-hooks-path']=hashlib.sha256(p.stdout).hexdigest()
    return result


def protected(name):
    name=name.casefold()
    parts=Path(name).as_posix().split('/')
    return (any(x in {'.git','.codex','.claude','.github','.vscode','__pycache__'} for x in parts)
            or any(x in {'agents.md','claude.md','.gitattributes','.gitmodules'} for x in parts)
            or name.startswith(('scripts/','automation/','__agent_control__/','collaboration/cc-reports/',
                'collaboration/checkpoints/','collaboration/live-latest/','collaboration/live-turns/',
                'collaboration/run-ledger/','collaboration/codex-sessions/','collaboration/cc-sessions/'))
            or name in {'.gitignore','docs/06_decision_log.md'})


def sandbox_command(native,argv,root):
    if not argv or not all(isinstance(x,str) for x in argv):
        raise ValueError('Pinned test argv required')
    # Resolve the host interpreter before entering the sandbox; do not find an
    # agent-written executable through cwd/PATH. Never run a host fallback.
    if Path(argv[0]).stem.lower() in {'python','python3','python313'}:
        argv=[sys.executable,'-B',*argv[1:]]
    elif not Path(argv[0]).is_absolute():
        raise ValueError('Non-Python test executables must be pinned absolute paths')
    return [native,'--no-daemon','-a','never','sandbox',
            '--permission-profile',':workspace','--sandbox-state-disable-network',
            '--',*argv]  # 0.165 sandbox has its own profile; legacy -s is insufficient here


def gate_details(reason):
    text=reason.lower()
    if any(x in text for x in ('secret','credential','authentication','login')):
        return ('Will you remediate through native login/revocation, or cancel this task?',
                ['Remediate privately using native credential UI; then issue a new approved plan','Cancel the task without publishing sensitive data'])
    if any(x in text for x in ('test','sandbox')):
        return ('Should the pinned tests/sandbox be repaired, or should this task be stopped?',
                ['Repair the sandbox or approve corrected pinned tests','Stop; do not execute agent-written tests on the host'])
    if any(x in text for x in ('scope','control-plane','instruction','policy')):
        return ('Should this change be removed, or separately approved as a bounded scope change?',
                ['Remove out-of-scope changes and open a fresh bounded task','Review and explicitly approve a new scoped plan'])
    if any(x in text for x in ('maximum','budget','iteration')):
        return ('Should this task stop, or be replaced by a newly scoped task after reviewing the failures?',
                ['Stop and inspect the accumulated evidence','Create a new scoped task; never reset exhausted counters'])
    return ('How should the owner resolve this specific stop: '+reason[:160]+'?',
            ['Review the pinned evidence and correct this specific blocker','Cancel or replace this task with a smaller approved requirement'])


def git_prefix(root):
    directory=Path(root)/'.git/agent-empty-hooks'
    directory.mkdir(parents=True,exist_ok=True)
    if directory.is_symlink() or any(directory.iterdir()):
        raise RuntimeError('Trusted empty Git hook directory changed; stop')
    return ['git','-C',str(root),'-c','core.hooksPath='+str(directory),'-c','core.fsmonitor=false']


def host_id():
    return hashlib.sha256(platform.node().encode()).hexdigest()


def process_birth(pid):
    if os.name!='nt':
        try:return str(os.stat('/proc/'+str(pid)).st_ctime_ns)
        except FileNotFoundError:return None
    import ctypes as c
    from ctypes import wintypes as t
    api=c.WinDLL('kernel32',use_last_error=True)
    api.OpenProcess.argtypes=[t.DWORD,t.BOOL,t.DWORD];api.OpenProcess.restype=t.HANDLE
    api.GetProcessTimes.argtypes=[t.HANDLE,c.POINTER(t.FILETIME),c.POINTER(t.FILETIME),c.POINTER(t.FILETIME),c.POINTER(t.FILETIME)]
    api.GetExitCodeProcess.argtypes=[t.HANDLE,c.POINTER(t.DWORD)]
    api.CloseHandle.argtypes=[t.HANDLE]
    handle=api.OpenProcess(0x1000,False,pid)
    if not handle:
        if c.get_last_error() in {87,1168}:return None
        raise ValueError('Cannot prove process identity; no lock recovery')
    try:
        status=t.DWORD();api.GetExitCodeProcess(handle,c.byref(status))
        if status.value!=259:return None
        start,exit,kernel,user=t.FILETIME(),t.FILETIME(),t.FILETIME(),t.FILETIME()
        if not api.GetProcessTimes(handle,c.byref(start),c.byref(exit),c.byref(kernel),c.byref(user)):
            raise ValueError('Cannot verify process birth identity')
        return str((start.dwHighDateTime<<32)|start.dwLowDateTime)
    finally:api.CloseHandle(handle)


def control_files(root):
    root=Path(root)
    names=[]
    for folder in ('scripts','automation','.github'):
        names += [p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc')]
    names += [root/n for n in ('AGENTS.md','CLAUDE.md','.gitignore') if (root/n).is_file()]
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in names if p.relative_to(root).as_posix()!='automation/policy.json'}


def verify_control(root,policy):
    approval=policy.get('approval',{})
    if approval.get('trust_root')!='B' or approval.get('test_boundary')!='A' or approval.get('review_result')!='PASS':
        raise ValueError('Conditional B/A approval and independent PASS are required')
    if not policy.get('control_plane_sha256') or control_files(root)!=policy['control_plane_sha256']:
        raise ValueError('Control-plane hash differs from the independently reviewed trust root')
    report=Path(root)/approval.get('review_report','MISSING_REVIEW')
    if (not report.is_file() or report.is_symlink() or
            hashlib.sha256(report.read_bytes()).hexdigest()!=approval.get('review_report_sha256')):
        raise ValueError('Independent review report does not match its pinned digest')
