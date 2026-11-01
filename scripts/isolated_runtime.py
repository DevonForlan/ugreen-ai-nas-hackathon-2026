"""AUTO-007: task-owned Docker Sandbox microVM, never a host credential bridge.

This experimental backend does not enable the autonomous controller. Authentication
is deliberately a separate User Gate; it never consumes host provider credentials.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
NAME = 'auto007-probe-1'
WORKSPACE = ROOT / 'tmp/AUTO-007/runtime/workspace'
GUEST_WORKSPACE = '/'+WORKSPACE.as_posix().replace(':', '', 1).lstrip('/').replace('C/', 'c/', 1)
HOME = '/home/agent/auto007'
BACKEND = 'docker-sandbox-microvm-v0.12'
CLASSES = ('USERPROFILE', 'APPDATA', 'LOCALAPPDATA', 'CODEX_HOME',
           'Claude-config', 'gh-config', 'SSH', 'Documents-Desktop')
ALLOWED_HOSTS = ('registry.npmjs.org', 'nodejs.org')
ENV = {'HOME': HOME, 'USERPROFILE': HOME, 'APPDATA': HOME+'/config',
       'LOCALAPPDATA': HOME+'/local', 'CODEX_HOME': HOME+'/codex',
       'CLAUDE_CONFIG_DIR': HOME+'/claude', 'XDG_CONFIG_HOME': HOME+'/config',
       'GIT_CONFIG_GLOBAL': HOME+'/gitconfig', 'GIT_CONFIG_NOSYSTEM': '1',
       'GIT_TERMINAL_PROMPT': '0', 'TMPDIR': HOME+'/tmp',
       'PATH': HOME+'/tools/node_modules/.bin:/usr/local/bin:/usr/bin:/bin'}


class RuntimeFailure(RuntimeError):
    pass


def stamp():
    return datetime.now(timezone.utc).isoformat()


def host_env():
    # Allowlist: neither provider/Git tokens nor SSH agents reach Docker clients.
    names = ('SystemRoot', 'WINDIR', 'PATH', 'PATHEXT', 'TEMP', 'TMP',
             'USERPROFILE', 'LOCALAPPDATA', 'APPDATA', 'PROGRAMFILES',
             'PROGRAMDATA', 'HOMEDRIVE', 'HOMEPATH')
    return {k: v for k, v in os.environ.items() if k.upper() in
            {n.upper() for n in names}}


def command(argv, timeout=90):
    child = subprocess.Popen(argv, stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=host_env(), cwd=ROOT)
    try:
        out, err = child.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Kill descendants before parent, avoiding orphaned Docker plugin clients.
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                           capture_output=True, timeout=15)
        child.kill(); child.communicate()
        raise RuntimeFailure('Runtime command timed out; inspect named sandbox state')
    if child.returncode:
        # Guest/npm/proxy output is untrusted and may contain authentication data.
        raise RuntimeFailure('Runtime command failed (exit '+str(child.returncode)+'); no raw output exported')
    return out.decode('utf-8', errors='strict').strip()


def validate_name(name):
    if not re.fullmatch(r'auto007-[a-z0-9-]{1,40}', name):
        raise ValueError('Only task-owned auto007 sandbox names are allowed')
    return name


def guest(name, script, timeout=90):
    validate_name(name)
    return command(['docker','sandbox','exec',name,'python3','-c',guest_wrapper(script)], timeout)


def guest_wrapper(script):
    # Clean environment inside VM, not merely in host launcher. No host auth/socket.
    # Retain only the VM's built-in policy proxy and CA paths. Neither provider
    # tokens nor SSH sockets from the template environment are inherited.
    wrapper = ('import os,subprocess,urllib.parse\nenv='+repr(ENV)+'\n'
        'for k in ("HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy"):\n'
        ' v=os.environ.get(k)\n'
        ' if v and urllib.parse.urlsplit(v).hostname=="host.docker.internal": env[k]=v\n'
        'for k in ("NODE_EXTRA_CA_CERTS","SSL_CERT_FILE","REQUESTS_CA_BUNDLE"):\n'
        ' v=os.environ.get(k)\n'
        ' if v and v.startswith("/"): env[k]=v\n'
        'raise SystemExit(subprocess.run(["python3","-c",'+repr(script)+'],env=env).returncode)')
    return wrapper


def configure(name):
    validate_name(name)
    args = ['docker', 'sandbox', 'network', 'proxy', name, '--policy', 'deny']
    for host in ALLOWED_HOSTS:
        args += ['--allow-host', host]
    command(args)
    guest(name, 'from pathlib import Path\n'+
          '\n'.join('Path('+repr(HOME+'/'+p)+').mkdir(parents=True,exist_ok=True)'
                    for p in ('config', 'local', 'codex', 'claude', 'tmp', 'tools'))+
          '\nPath('+repr(HOME+'/gitconfig')+').write_text("[user]\\n name = AUTO-007 Runtime\\n email = runtime@example.invalid\\n")')


def create(name):
    validate_name(name)
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    # No root repository mount; only this disposable, initially empty directory.
    command(['docker', 'sandbox', 'create', '--name', name, 'shell', str(WORKSPACE)], 900)
    configure(name)


def snapshot(paths):
    """Explicit tracked regular files only; reject reparse ancestors and secrets."""
    spec = importlib.util.spec_from_file_location('runtime_scan', ROOT/'scripts/scan-codex-secrets.py')
    scanner = importlib.util.module_from_spec(spec); spec.loader.exec_module(scanner)
    resolved = []
    for value in paths:
        pure = PurePosixPath(value)
        if pure.is_absolute() or '..' in pure.parts or '\\' in value or ':' in value or not pure.parts:
            raise ValueError('Unsafe snapshot path')
        if pure.parts[0] in ('.git', 'tmp', 'automation') or scanner.forbidden(value):
            raise ValueError('Forbidden snapshot path')
        source = ROOT.joinpath(*pure.parts)
        for parent in (source, *source.parents):
            if parent == ROOT.parent: break
            if parent.is_symlink() or (hasattr(parent, 'is_junction') and parent.is_junction()):
                raise ValueError('Snapshot reparse point rejected')
        command(['git', '--literal-pathspecs', 'ls-files', '--error-unmatch', '--', value])
        if source.stat().st_size > 1024*1024:
            raise ValueError('Snapshot size bound exceeded')
        data = source.read_bytes()
        if len(data) > 1024*1024 or scanner.scan_blob(value, data):
            raise ValueError('Snapshot size/content scan rejected')
        target = WORKSPACE/'repo'/pure
        # A guest may mutate the shared tree: do not follow its symlinks on host.
        for parent in (target, *target.parents):
            if parent == WORKSPACE.parent: break
            if parent.is_symlink() or (hasattr(parent, 'is_junction') and parent.is_junction()):
                raise ValueError('Snapshot destination reparse point rejected')
        resolved.append((target, data))
    for target, data in resolved:
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
    return len(resolved)


def bootstrap(name):
    configure(name)
    guest(name, 'import subprocess\nsubprocess.run('+repr([
        'npm', 'install', '--prefix', HOME+'/tools', '--no-audit', '--no-fund',
        '@openai/codex', '@anthropic-ai/claude-code'])+',check=True)', 600)
    return functional(name)


def functional(name):
    script = '''import subprocess,json,os
from pathlib import Path
result={}
for name in ('codex','claude','git','node'):
 try:
  p=subprocess.run([name,'--version'],capture_output=True,text=True,timeout=30)
  result[name]={'launched':p.returncode==0,'version':p.stdout.strip()[:120]}
 except (OSError,subprocess.TimeoutExpired):result[name]={'launched':False,'version':'UNKNOWN'}
result['ssh_agent_exposed']='SSH_AUTH_SOCK' in os.environ
print(json.dumps(result))'''
    return json.loads(guest(name, script, 150))


def boundary(name):
    # Synthetic directory tree only. Never locate/open existing credential files.
    external = Path(tempfile.mkdtemp(prefix='AUTO007-synthetic-'))
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    sentinels = {}
    try:
        for kind in CLASSES:
            path = external/kind/'sentinel.txt'; path.parent.mkdir()
            path.write_text('PUBLIC SYNTHETIC SENTINEL', encoding='utf-8')
            posix = path.as_posix()
            drive = posix[0].lower(); tail = posix[2:]
            sentinels[kind] = [str(path), posix, '/'+drive+tail, '/mnt/'+drive+tail,
                               '/host_mnt/'+drive+tail, '/run/desktop/mnt/host/'+drive+tail]
        public = WORKSPACE/'workspace-sentinel.txt'
        public.write_text('PUBLIC SYNTHETIC SENTINEL', encoding='utf-8')
        script = 'from pathlib import Path\nimport json\nchecks='+repr(sentinels)+'''
def readable(path):
 try:
  with Path(path).open('rb') as stream: stream.read(1)
  return True
 except OSError: return False
rows=[{'path_class':kind,'readable':any(readable(p) for p in paths)} for kind,paths in checks.items()]
base=Path('/home/agent/auto007')
for kind,path in [('runtime-config',base/'config/synthetic.txt'),('runtime-temp',base/'tmp/synthetic.txt')]:
 path.write_text('PUBLIC SYNTHETIC SENTINEL'); rows.append({'path_class':kind,'readable':readable(path)});path.unlink()
rows.append({'path_class':'workspace','readable':readable('''+repr(GUEST_WORKSPACE+'/workspace-sentinel.txt')+''')})
print(json.dumps(rows))'''
        rows = json.loads(guest(name, script))
        now = stamp()
        return [dict(row, runtime_backend=BACKEND, test_timestamp=now) for row in rows]
    finally:
        for kind in CLASSES:
            (external/kind/'sentinel.txt').unlink(missing_ok=True)
            (external/kind).rmdir()
        external.rmdir()


def require_boundary(rows):
    expected={kind:False for kind in CLASSES}
    expected.update({'workspace':True,'runtime-config':True,'runtime-temp':True})
    if len(rows)!=len(expected) or {r.get('path_class') for r in rows}!=set(expected):
        raise RuntimeFailure('Incomplete synthetic boundary evidence')
    if any(type(r.get('readable')) is not bool or r['readable']!=expected[r['path_class']] for r in rows):
        raise RuntimeFailure('Synthetic credential boundary or positive control failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['create', 'configure', 'bootstrap', 'probe', 'check', 'snapshot'])
    parser.add_argument('--name', default=NAME)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--file', action='append', default=[])
    args = parser.parse_args(); validate_name(args.name)
    if args.action == 'create': create(args.name); value={'created':args.name}
    elif args.action == 'configure': configure(args.name); value={'configured':args.name}
    elif args.action == 'bootstrap': value=bootstrap(args.name)
    elif args.action == 'probe': value=boundary(args.name); require_boundary(value)
    elif args.action == 'check': value=functional(args.name)
    else: value={'snapshot_files':snapshot(args.file)}
    text=json.dumps(value,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8',newline='\n')
    print(text,end='')


if __name__ == '__main__':
    try: main()
    except (RuntimeFailure, ValueError) as error:
        print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(1)
