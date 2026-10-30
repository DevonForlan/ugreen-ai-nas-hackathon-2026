#!/usr/bin/env python3
"""Outer owner: interactive live companion plus post-exit capture; no agent work loop."""
import argparse
from datetime import datetime, timezone
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
import time
from agent_transcripts import (archive, claude_result, codex_result, discover, events, module,
                               now, project, read_native, refresh, save_run)
from agent_history_sync import publish


def headless(agent,prompt,cwd,timeout=1800,root=None):
    # Reuse verified native launcher and credential-environment filtering, not the loop.
    cli=module('history_cli','agent_workflow.py')
    started=now()
    if agent=='codex':
        native=cli.load_module('history_native','codex-usage.py').native_codex()
        if not native:
            raise RuntimeError('Native Codex unavailable')
        with tempfile.TemporaryDirectory(prefix='agent-final-') as folder:
            out=Path(folder)/'last-message.txt'
            argv=[native,'--no-daemon','-a','never','-c','sandbox_workspace_write.network_access=false',
                  'exec','--ignore-user-config','--sandbox','workspace-write','--json',
                  '--output-last-message',str(out),'-']
            if not (Path(project(cwd))/'.git').exists():
                argv.insert(-1,'--skip-git-repo-check')
            raw=cli.command(argv,cwd=cwd,input_text=prompt,timeout=timeout,isolate_env=True)
            ended=now()  # command returns only after process exit
            final=out.read_text(encoding='utf-8')
        session,proof=codex_result(raw,prompt,final,cwd,started,ended)
    else:
        schema=(Path(__file__).parent.parent/'automation/cc-review.schema.json').read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='claude-visible-review-') as folder:
            argv=cli.claude_launcher()+['--safe-mode','--restricted','--tools','',
                '--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--no-session-persistence',
                '-p','--output-format','json','--json-schema',schema]
            raw=cli.command(argv,cwd=Path(folder),input_text=prompt,timeout=timeout,isolate_env=True)
            ended=now()
        envelope=json.loads(raw)
        # The supplied review result must be valid; do not certify malformed reviewer JSON.
        cli.review_json(envelope.get('structured_output',envelope.get('result')))
        session,proof=claude_result(envelope,prompt,cwd,started,ended)
    item=archive(session,root,proof=proof)
    return session,proof,item


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent',required=True,choices=['codex','claude'])
    parser.add_argument('--interactive',action='store_true')
    parser.add_argument('--prompt-file',type=Path)
    parser.add_argument('--project',type=Path,default=Path.cwd())
    parser.add_argument('--task-id',default='INTERACTIVE')
    parser.add_argument('--round',type=int,default=1)
    parser.add_argument('--timeout',type=int,default=1800)
    parser.add_argument('--archive-root',type=Path)
    parser.add_argument('--publish',action='store_true')
    parser.add_argument('--live-sync',action='store_true',help='Owned interactive transcript companion')
    parser.add_argument('cli_args',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    cwd=args.project.resolve()
    gitroot=Path(project(cwd))
    gitroot=gitroot if (gitroot/'.git').exists() else None
    if args.interactive:
        cli=module('history_interactive','agent_workflow.py')
        argv=([cli.load_module('history_native_interactive','codex-usage.py').native_codex()]
              if args.agent=='codex' else cli.claude_launcher())
        if not argv[0]:
            raise RuntimeError('Native agent not available')
        before={str(p):(p.stat().st_size,p.stat().st_mtime_ns) for p in discover(args.agent)}
        extra=args.cli_args[1:] if args.cli_args[:1]==['--'] else args.cli_args
        if (extra[:1]==['exec'] or any(x in extra for x in ('-p','--print','--ephemeral','--no-session-persistence',
                '--background','--bg','--cloud','--teleport'))):
            parser.error('Use the headless history runner for non-interactive/ephemeral execution; TUI wrapper requires native persistence')
        result=1
        companion=None
        process=None
        try:
            process=subprocess.Popen(argv+extra,cwd=cwd)  # real TUI, no keyboard simulation
            warned=False
            while process.poll() is None:
                if args.live_sync and args.publish and gitroot and companion is None:
                    candidates=[]
                    for path in discover(args.agent):
                        if before.get(str(path)) == (path.stat().st_size,path.stat().st_mtime_ns):
                            continue
                        session=read_native(path,args.agent)
                        if session and session['projects']==[project(gitroot)]:
                            candidates.append((path,session['session_id']))
                    if len(candidates)==1:
                        path,sid=candidates[0]
                        command=[sys.executable,'-X','utf8',str(Path(__file__).with_name('agent_live_sync.py')),
                            '--agent',args.agent,'--source',str(path),'--session-id',sid,
                            '--project',str(gitroot),'--owner-pid',str(process.pid),'--follow-project']
                        companion=subprocess.Popen(command,cwd=cwd,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform=='win32' else 0)
                        print('Live sanitized transcript sync attached: '+sid,flush=True)
                    elif len(candidates)>1 and not warned:
                        print('WARNING: live sync needs an exact session; multiple changed sessions. Use attach mode.',flush=True)
                        warned=True
                if companion is not None and companion.poll() is not None and not warned:
                    print('WARNING: live sync stopped; agent continues. LOCAL ONLY — inspect live-sync-status.json.',flush=True)
                    warned=True
                time.sleep(1)
            result=process.returncode
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                process.wait(timeout=15)
            if companion is not None:
                # Owner exit ends the bounded companion. No detached/orphan watcher.
                try:
                    companion.wait(timeout=180)
                except subprocess.TimeoutExpired:
                    companion.terminate()
                    companion.wait(timeout=15)
                    print('WARNING: live companion forcibly stopped after owner exit; inspect lock before reuse.',flush=True)
            stats=refresh(root=args.archive_root,project_path=gitroot)
            print(json.dumps({'archive_refresh':stats,'interactive_final_capture':'unknown'}))
        candidates=[]
        for path in discover(args.agent):
            if before.get(str(path)) == (path.stat().st_size,path.stat().st_mtime_ns):
                continue
            s=read_native(path,args.agent)
            if s and gitroot and s['projects']==[project(gitroot)]:
                candidates.append(s)
        if gitroot and len(candidates)==1:
            # Exit of the TUI does not prove which connected client's last turn ended.
            item,path,value=save_run(candidates[0],None,gitroot,args.task_id,args.round,args.archive_root,failed=result!=0)
            if args.publish:
                print(json.dumps(publish(item,path,value,gitroot)))
            print('Interactive snapshot retained. Final capture is UNKNOWN; no SYNC_COMPLETE claim.')
        else:
            print('LOCAL_ONLY: no unique owned project session; global retention refreshed without guessing identity.')
        return result
    if not args.prompt_file or args.cli_args:
        parser.error('Headless mode requires --prompt-file; extra CLI flags are not accepted')
    started=now()
    try:
        session,proof,item=headless(args.agent,args.prompt_file.read_text(encoding='utf-8'),cwd,args.timeout,args.archive_root)
    except BaseException as exc:
        if gitroot and re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.task_id):
            from agent_transcripts import write_json
            failure=dict(task_id=args.task_id,agent=args.agent,session_id=None,round=args.round,
                started_at=started,ended_at=now(),last_visible_response_at=None,final_response_captured=False,
                local_archive_updated=False,project_transcript_updated=False,secret_scan='NOT_RUN',commit_sha=None,
                github_synced=False,status='FAILED',error_type=type(exc).__name__)
            write_json(gitroot/'collaboration/run-ledger'/f'{args.task_id}_{args.agent}_round-{args.round}_{uuid.uuid4().hex}.json',failure)
        raise
    if not gitroot:
        print(json.dumps({'status':'LOCAL_ONLY','final_response_captured':bool(proof),'archive_updated':True}))
        return 0
    item,path,value=save_run(session,proof,gitroot,args.task_id,args.round,args.archive_root)
    if args.agent=='claude':
        review_path=gitroot/'collaboration/cc-reports'/f'{datetime.now():%Y-%m-%d_%H%M}_{args.task_id}_{value["run_id"]}.md'
        from agent_transcripts import atomic
        atomic(review_path,'# CC Review\n\nTask: '+args.task_id+'\n\n'+events(session)[-1]['text']+'\n')
        extra_paths=[review_path]
    else:
        extra_paths=[]
    if args.publish:
        print(json.dumps(publish(item,path,value,gitroot,extra_paths)))
    else:
        print(json.dumps({'status':value['status'],'ledger':path.relative_to(gitroot).as_posix()}))
    if not proof:
        print('LOCAL_ONLY: final response could not be proven; never SYNC_COMPLETE.')
        return 2
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:
        print('LOCAL_ONLY / FAILED: '+type(exc).__name__+'; inspect local state. No raw output or credentials printed.')
        raise SystemExit(1)
