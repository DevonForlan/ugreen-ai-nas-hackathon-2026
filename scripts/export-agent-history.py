#!/usr/bin/env python3
"""Refresh sanitized global histories; optionally publish an explicit captured snapshot."""
import argparse
import json
from pathlib import Path
from agent_transcripts import archive, discover, ledger, project, read_native, refresh, save_run


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',choices=['codex','claude','all'],default='all')
    p.add_argument('--archive-root',type=Path)
    p.add_argument('--project',type=Path,default=Path.cwd())
    p.add_argument('--global-only',action='store_true')
    p.add_argument('--task-id')
    p.add_argument('--session-id')
    p.add_argument('--round',type=int,default=1)
    p.add_argument('--publish',action='store_true')
    args=p.parse_args()
    agents=('codex','claude') if args.agent=='all' else (args.agent,)
    root=Path(project(args.project))
    project_path=None if args.global_only or not (root/'.git').exists() else root
    if args.publish and not (args.task_id and args.session_id and len(agents)==1 and project_path):
        p.error('--publish requires Git project, one agent, task-id and session-id')
    if args.task_id or args.session_id:
        if not (args.task_id and args.session_id and len(agents)==1 and project_path):
            p.error('Snapshot ledger requires task-id, session-id, one agent and Git project')
        session=None
        for path in discover(agents[0]):
            if args.session_id in path.name:
                candidate=read_native(path,agents[0])
                if candidate and candidate['session_id']==args.session_id:
                    session=candidate;break
        if not session:
            p.error('Explicit native session not found')
        item,path,value=save_run(session,None,project_path,args.task_id,args.round,args.archive_root)
        if args.publish:
            from agent_history_sync import publish
            result=publish(item,path,value,project_path)
            print(json.dumps(result))
        else:
            print(json.dumps({'ledger':path.relative_to(project_path).as_posix(),'status':value['status'],
                              'final_response_captured':value['final_response_captured']}))
    else:
        result=refresh(agents,args.archive_root,project_path)
        print(json.dumps(result,sort_keys=True))
        return 1 if result['failures'] else 0
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,RuntimeError) as exc:
        print('LOCAL_ONLY: history synchronization stopped ('+type(exc).__name__+'). No content/credentials printed.')
        raise SystemExit(1)
