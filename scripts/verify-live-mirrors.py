#!/usr/bin/env python3
"""Bounded real AUTO-004 probe: one harmless Claude reply, verified while CLI lives.

No tools/MCP, no raw stdout files, no auth extraction. Codex remains the active
interactive process; send its harmless marker visibly after this probe announces READY.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import uuid

from agent_workflow import claude_launcher
from agent_transcripts import discover, now, write_json


def github_file(repo,path):
    result=subprocess.run(['gh','api','repos/'+repo+'/contents/'+path],capture_output=True,timeout=30)
    if result.returncode:
        raise RuntimeError('GitHub file unavailable; raw output withheld')
    value=json.loads(result.stdout)
    if not value.get('content'):
        raise ValueError('Small mirror connector content missing')
    return base64.b64decode(value['content']).decode('utf-8')


def assistant_contains(text,marker):
    if '## Visible assistant response\n' not in text:
        return False
    body=text.split('## Visible assistant response\n',1)[1]
    body=body.split('\n### ',1)[0].split('\n## Full ',1)[0]
    return marker in body


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',default='DevonForlan/ugreen-ai-nas-hackathon-2026')
    parser.add_argument('--timeout',type=int,default=300)
    parser.add_argument('--codex-marker',default='AUTO004-CODEX-LIVE-CHECK')
    args=parser.parse_args()
    if not 30<=args.timeout<=600:
        parser.error('Timeout must be 30..600 seconds')
    root=Path(__file__).resolve().parents[1]
    sid=str(uuid.uuid4())
    marker='AUTO004-CLAUDE-LIVE-'+sid[:8]
    allowed={'SYSTEMROOT','WINDIR','PATH','PATHEXT','USERPROFILE','HOMEDRIVE','HOMEPATH','HOME','APPDATA','LOCALAPPDATA','TEMP','TMP','COMSPEC','LANG','TERM'}
    env={k:v for k,v in os.environ.items() if k.upper() in allowed}
    env['CLAUDE_CODE_DISABLE_BACKGROUND_TASKS']='1'
    child=None
    watcher=None
    incoming=queue.Queue(maxsize=1000)
    def drain(stream,parse):
        for line in stream:
            if len(line)>1024*1024:
                continue
            if parse:
                try:
                    value=json.loads(line)
                    if value.get('type')=='assistant':
                        texts=[b.get('text','') for b in value.get('message',{}).get('content',[]) if b.get('type')=='text']
                        if marker in '\n'.join(texts):
                            incoming.put_nowait(True)
                except (ValueError,TypeError,queue.Full):
                    pass
            # All other native/internal stdout/stderr is discarded, not saved/printed.
    try:
        child=subprocess.Popen(claude_launcher()+['--safe-mode','--restricted','--tools','',
            '--strict-mcp-config','--mcp-config','{"mcpServers":{}}','-p',
            '--input-format','stream-json','--output-format','stream-json','--verbose','--session-id',sid],
            cwd=root,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            text=True,encoding='utf-8',errors='replace')
        threading.Thread(target=drain,args=(child.stdout,True),daemon=True).start()
        threading.Thread(target=drain,args=(child.stderr,False),daemon=True).start()
        child.stdin.write(json.dumps({'type':'user','session_id':sid,'message':{'role':'user','content':'Reply exactly with '+marker+'. Do not use tools or read files.'},'parent_tool_use_id':None})+'\n')
        child.stdin.flush()
        print(json.dumps({'READY':True,'claude_pid':child.pid,'claude_session_id':sid,'claude_marker':marker,'codex_marker':args.codex_marker}),flush=True)
        deadline=time.monotonic()+args.timeout
        found=False
        while time.monotonic()<deadline:
            if child.poll() is not None:
                raise RuntimeError('Claude exited before live acceptance; not PASS')
            if watcher is None:
                sources=[p for p in discover('claude') if p.name==sid+'.jsonl']
                if len(sources)==1:
                    watcher=subprocess.Popen([sys.executable,'-X','utf8',str(root/'scripts/agent_live_sync.py'),
                        '--agent','claude','--session-id',sid,'--source',str(sources[0]),
                        '--project',str(root),'--owner-pid',str(child.pid),'--max-runtime',str(args.timeout)],
                        cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            try:
                found=incoming.get_nowait() or found
            except queue.Empty:
                pass
            if found:
                try:
                    index=json.loads(github_file(args.repository,'collaboration/live-latest/index.json'))
                    cc=index['agents']['claude'];codex=index['agents']['codex']
                    cc_text=github_file(args.repository,'collaboration/live-latest/claude.md')
                    codex_text=github_file(args.repository,'collaboration/live-latest/codex.md')
                    if (cc['session_id']==sid and assistant_contains(cc_text,marker) and assistant_contains(codex_text,args.codex_marker)
                            and all(x['status']=='SYNC_COMPLETE' and x['github_remote_verified'] for x in (cc,codex))):
                        evidence=dict(task='AUTO-004',status='PASS',observed_at=now(),claude_process_alive=child.poll() is None,
                            claude_session_id=sid,claude_marker=marker,codex_marker=args.codex_marker,
                            claude_receipt=cc,codex_receipt=codex,
                            latest_files_read_directly_from_github=True)
                        write_json(root/'collaboration/run-ledger/AUTO-004_live-acceptance.json',evidence)
                        print(json.dumps({'status':'PASS','claude_alive':True,'claude_commit':cc['github_commit_sha'],'codex_commit':codex['github_commit_sha']}),flush=True)
                        return 0
                except (RuntimeError,ValueError,KeyError):
                    pass
            if watcher is not None and watcher.poll() is not None:
                raise RuntimeError('Live mirror watcher stopped before acceptance')
            time.sleep(3)
        raise RuntimeError('Live mirror acceptance timed out; not PASS')
    finally:
        if child is not None:
            if child.stdin and not child.stdin.closed:
                child.stdin.close()
            try:
                child.wait(timeout=15)
            except subprocess.TimeoutExpired:
                child.terminate();child.wait(timeout=15)
        if watcher is not None:
            try:
                watcher.wait(timeout=120)
            except subprocess.TimeoutExpired:
                watcher.terminate();watcher.wait(timeout=15)


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print('AUTO-004 NOT PASS: '+type(exc).__name__+'; no native output or auth data logged.',flush=True)
        raise SystemExit(1)
