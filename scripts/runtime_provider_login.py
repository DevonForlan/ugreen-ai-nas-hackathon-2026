"""Native user-terminal OAuth for the existing AUTO-007 VM. No credential bridge.

Never run interactive login through captured agent tools, terminal transcription,
output redirection or CI. Provider-native prompts belong only in the user's local
terminal/browser. Only boolean status and public network policy are exported.
"""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import isolated_runtime as runtime

AUTH_CODEX = ('auth.openai.com',)
AUTH_CLAUDE = ('claude.ai','platform.claude.com','api.anthropic.com')
MODEL_HOSTS = ('chatgpt.com','api.anthropic.com')
BOOTSTRAP_HOSTS = ('registry.npmjs.org','nodejs.org')
ALL_HOSTS = tuple(dict.fromkeys((*AUTH_CODEX,*AUTH_CLAUDE,*MODEL_HOSTS,*BOOTSTRAP_HOSTS)))
PHASES = {'codex':AUTH_CODEX,'claude':(*AUTH_CODEX,*AUTH_CLAUDE),
          'runtime':(*AUTH_CODEX,*AUTH_CLAUDE,*MODEL_HOSTS)}
EVIDENCE = runtime.ROOT/'collaboration/run-ledger/AUTO-007_provider-login.json'


def save_evidence(value):
    EVIDENCE.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
    checkpoint=runtime.ROOT/'collaboration/checkpoints/AUTO-007/provider-login.json'
    checkpoint.parent.mkdir(parents=True,exist_ok=True)
    checkpoint.write_text(json.dumps({
        'task_id':'AUTO-007','checkpoint_kind':'PROVIDER_LOGIN_ONLY',
        'status':value['status'],'checked_at':value['checked_at'],
        'providers':value['providers'],'network_phase':value['network_phase'],
        'evidence_path':EVIDENCE.relative_to(runtime.ROOT).as_posix(),
        'autonomous_execution_enabled':False},indent=2)+'\n',encoding='utf-8',newline='\n')


def resume_existing():
    listing=runtime.command(['docker','sandbox','ls'])
    rows=[line.split(None,3) for line in listing.splitlines() if line.split()[:1]==[runtime.NAME]]
    if len(rows)!=1 or len(rows[0])!=4:
        raise runtime.RuntimeFailure('Existing named sandbox missing; creation is prohibited')
    _,agent,state,workspace=rows[0]
    if agent!='shell' or workspace.replace('\\','/').casefold()!=runtime.WORKSPACE.as_posix().casefold():
        raise runtime.RuntimeFailure('Existing sandbox workspace identity mismatch')
    if state=='stopped':runtime.command(['docker','sandbox','run',runtime.NAME,'--','-c','true'],180)
    elif state!='running':raise runtime.RuntimeFailure('Existing sandbox state uncertain; no recreation')


def network(phase):
    allowed=PHASES[phase]
    args=['docker','sandbox','network','proxy',runtime.NAME,'--policy','deny']
    # v0.12 uses most-specific rule precedence. A host-only block cannot
    # override a pre-existing host:443 allow (verified with the native log).
    for wildcard in ('*.anthropic.com','*.anthropic.com:443'):
        args += ['--block-host',wildcard]
    for host in ALL_HOSTS:
        args += ['--block-host',host]
        args += ['--allow-host' if host in allowed else '--block-host',host+':443']
    runtime.command(args)
    return [host+':443' for host in allowed]


def status():
    # Provider outputs stay inside guest. Never return email, account ID, tokens,
    # login URLs, one-time codes or raw error/log text to the host controller.
    code='''import json,subprocess
result={}
for agent,args in [('codex',['codex','login','status']),('claude',['claude','auth','status','--json'])]:
 try:
  p=subprocess.run(args,capture_output=True,text=True,timeout=30)
  if agent=='claude':
   raw=json.loads(p.stdout); value=raw.get('loggedIn')
   authenticated=value if type(value) is bool else None
  else:authenticated=(p.returncode==0) if p.returncode in (0,1) else None
 except (OSError,ValueError,subprocess.TimeoutExpired):authenticated=None
 result[agent]={'authenticated':authenticated}
print(json.dumps(result))'''
    return json.loads(runtime.guest(runtime.NAME,code))


def verify_network(phase):
    started=datetime.now(timezone.utc)
    hosts=tuple(dict.fromkeys((*PHASES[phase],*BOOTSTRAP_HOSTS,'example.com')))
    code='import urllib.request,urllib.error\nfor host in '+repr(hosts)+''':
 try:urllib.request.urlopen('https://'+host+'/',timeout=12).close()
 except Exception:pass
print('public-host-probes-complete')'''
    runtime.guest(runtime.NAME,code,150)
    # Official v0.12 log is an aggregate of hostname/port/rule/counter metadata;
    # no request URLs, headers, bodies or login codes are read or exported.
    log=json.loads(runtime.command(['docker','sandbox','network','log','--json','--limit','1000']))
    rows=[]
    for host in hosts:
        matches=[]
        for kind,allowed in (('allowed_hosts',True),('blocked_hosts',False)):
            for row in log.get(kind,[]):
                if row.get('vm_name')==runtime.NAME and row.get('host')==host+':443':
                    when=datetime.fromisoformat(row['last_seen'])
                    if when>=started:matches.append((when,allowed))
        observed=max(matches)[1] if matches else None
        expected=host in PHASES[phase]
        if observed is not expected:
            raise runtime.RuntimeFailure('Native proxy enforcement not verified; OAuth must not start')
        rows.append({'host':host+':443','allowed':observed})
    return rows


def verify_environment():
    code='''import os,json,re
expected='''+repr(runtime.ENV)+'''
values={k:os.environ.get(k)==v for k,v in expected.items()}
blocked=('SSH_AUTH_SOCK','GH_TOKEN','GITHUB_TOKEN','OPENAI_API_KEY','ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','CLAUDE_CODE_OAUTH_TOKEN')
mounts=[]
for line in open('/proc/self/mountinfo'):
 path=line.split(' - ')[0].split()[4]
 path=re.sub(r'\\\\([0-7]{3})',lambda m:chr(int(m[1],8)),path)
 if path.startswith(('/c/','/mnt/c/','/host_mnt/','/run/desktop/mnt/host/')):mounts.append(path)
print(json.dumps({'runtime_env_correct':all(values.values()),'credential_environment_absent':all(k not in os.environ for k in blocked),'only_approved_host_mount':mounts==['''+repr(runtime.GUEST_WORKSPACE)+''']}))'''
    result=json.loads(runtime.guest(runtime.NAME,code))
    if not result or not all(v is True for v in result.values()):
        raise runtime.RuntimeFailure('Runtime environment/mount boundary verification failed')
    return result


def prepare(phase='codex'):
    resume_existing()
    env=verify_environment()
    cli=runtime.functional(runtime.NAME)
    if not all(cli[x]['launched'] for x in ('codex','claude')):
        raise runtime.RuntimeFailure('Existing provider CLI missing; no reinstall or disk reset')
    allowed=network(phase)
    verified_network=verify_network(phase)
    rows=runtime.boundary(runtime.NAME);runtime.require_boundary(rows)
    value={'task_id':'AUTO-007','checked_at':runtime.stamp(),'sandbox':runtime.NAME,
           'status':'WAITING_FOR_USER_NATIVE_LOGIN','network_phase':phase,
           'allowed_hosts':allowed,'bootstrap_access':False,'environment':env,
           'verified_network':verified_network,
           'cli':cli,'providers':status(),'credential_contents_exported':False,
           'boundary':rows,'autonomous_execution_enabled':False}
    save_evidence(value)
    return value


def interactive(provider):
    if not (sys.stdin.isatty() and sys.stdout.isatty()) or os.environ.get('CODEX_AGENT_WORKFLOW')=='1':
        raise runtime.RuntimeFailure('Login requires your own interactive terminal; captured invocation refused')
    prepare(provider)
    current=status()
    if current[provider]['authenticated'] is not True:
        argv=['codex','login','--device-auth'] if provider=='codex' else ['claude','auth','login','--claudeai']
        script=('import subprocess\n'
                'raise SystemExit(subprocess.run('+repr(argv)+',timeout=900).returncode)')
        # Intentionally inherit the user's terminal, with no PIPE/log/redirect.
        p=subprocess.run(['docker','sandbox','exec','-it',runtime.NAME,'python3','-c',
                          runtime.guest_wrapper(script)],env=runtime.host_env(),cwd=runtime.ROOT)
        if p.returncode:raise runtime.RuntimeFailure('Native login did not complete; no raw output retained')
    current=status()
    if current[provider]['authenticated'] is not True:
        raise runtime.RuntimeFailure('Native login status not authenticated; no success inferred')
    if all(current[x]['authenticated'] is True for x in ('codex','claude')):
        value=prepare('runtime');value['status']='READY_FOR_INDEPENDENT_REVIEW'
        save_evidence(value)
        print('Both providers authenticated. Boundary reverified; bootstrap blocked. Return to Codex for review/smoke; no task PASS inferred.')
    elif provider=='codex':
        prepare('claude')
        print('Codex native status: authenticated. Next: .\\scripts\\login-runtime-provider.ps1 -Provider Claude')
    else:
        prepare('codex')
        print('Claude native status: authenticated. Next: .\\scripts\\login-runtime-provider.ps1 -Provider Codex')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['prepare','status','login'])
    p.add_argument('--provider',choices=['codex','claude'],default='codex')
    a=p.parse_args()
    if a.action=='login':interactive(a.provider)
    elif a.action=='status':print(json.dumps(status()))
    else:print(json.dumps(prepare(a.provider)))


if __name__=='__main__':
    try:main()
    except (runtime.RuntimeFailure,subprocess.TimeoutExpired):
        print('Native login preparation/status failed; no credential values logged.',file=sys.stderr)
        sys.exit(1)
