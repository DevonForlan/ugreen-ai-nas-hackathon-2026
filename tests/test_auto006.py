"""AUTO-006 regressions; no model invocations or credential content reads."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import agent_workflow as w
import agent_security as s
import agent_live_mirror as m
import agent_live_sync as live
import agent_transcripts as h
from agent_evidence import compact
from test_agent_workflow import Hub,Tools


class RemediationTests(unittest.TestCase):
    def test_project_companion_discovers_newer_session_without_pinning_old(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'.git').mkdir();sources=[];seen=[]
            class Stub:
                def __init__(self,source,agent,root,sid,*args):self.sid=sid
                def step(self,clock):seen.append(self.sid);return None
            def source(sid):
                path=root/(sid+'.jsonl');path.write_text(json.dumps({'type':'session_meta','payload':{'id':sid,'cwd':str(root)}})+'\n');sources.append(path)
            source('older-source-123')
            with patch.object(h,'discover',side_effect=lambda agent:list(sources)),patch.object(live,'Watcher',Stub):
                watcher=live.ProjectWatcher('codex',root);watcher.step(0)
                source('newer-source-456');watcher.step(6)
            self.assertIn('older-source-123',seen);self.assertIn('newer-source-456',seen)

    def test_large_failing_output_keeps_stop_ledger_and_comment_small(self):
        output='PUBLIC failure evidence\n'*5000
        with tempfile.TemporaryDirectory() as folder:
            tools=w.LiveTools();native=type('Native',(),{'native_codex':lambda self:'native.exe'})()
            with patch.object(w,'ROOT',Path(folder)),patch.object(w,'load_module',return_value=native),patch.object(w,'command',side_effect=w.CommandFailure(7,output,'')):
                with self.assertRaises(w.Gate):tools.tests([['python','-m','unittest']])
            record=tools.last_test_evidence[0]
            self.assertGreater(record['output_bytes'],65536);self.assertNotIn('output',record)
            self.assertEqual((Path(folder)/record['artifact_path']).read_text(),output)
            hub=Hub();state={'state':'CODEX_RUNNING','body_sha256':w.digest(hub.item['body']),'codex_attempts':1,'cc_rounds':0,'history':[],
                'test_evidence':[dict(record,output=output)],'handoff':{'tests':[dict(record,output=output)]}}
            policy={'agent_timeout_seconds':30,'max_review_bytes':4096,'plans':{}}
            w.Engine(hub,Tools(),policy).gate(hub.issue(1),state,None,'Required tests failed')
            self.assertEqual(hub.state['state'],'USER_DECISION_REQUIRED');self.assertTrue(hub.comments)
            self.assertLess(len(json.dumps(hub.state)),10000)

    def test_unsanitizable_oversize_decision_uses_fixed_emergency_payload(self):
        hub=Hub();policy={'agent_timeout_seconds':30,'max_review_bytes':4096,'plans':{}}
        state={'state':'CODEX_RUNNING','body_sha256':w.digest(hub.item['body']),'codex_attempts':2,'cc_rounds':3,'history':[], 'huge':'x'*100000}
        w.Engine(hub,Tools(),policy).gate(hub.issue(1),state,None,'x'*100000)
        self.assertTrue(hub.state['emergency_payload_fallback']);self.assertEqual(hub.state['cc_rounds'],3)
        self.assertEqual(hub.state['codex_attempts'],2);self.assertTrue(hub.comments)

    def test_cwd_and_project_path_shims_never_resolve_or_execute(self):
        original=Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);marker=root/'executed'
            for name in ('claude.exe','claude.cmd','node.exe','codex.exe','codex.cmd'):
                (root/name).write_text('echo executed > '+str(marker))
            try:
                os.chdir(root)
                with patch.dict(os.environ,{'PATH':str(root)+os.pathsep+'.'}):
                    for name in ('claude','node','codex'):self.assertIsNone(s.resolve_agent_executable(name,root))
                    spec=importlib.util.spec_from_file_location('safe_usage',Path(w.__file__).with_name('codex-usage.py'))
                    usage=importlib.util.module_from_spec(spec);spec.loader.exec_module(usage)
                    self.assertIsNone(usage.native_codex())
                    with self.assertRaises(w.Gate):w.claude_launcher()
            finally:os.chdir(original)
            self.assertFalse(marker.exists())

    def test_literal_path_environment_is_pinned(self):
        self.assertEqual(s.git_environment()['GIT_LITERAL_PATHSPECS'],'1')

    def test_api_stop_checkpoint_both_states_never_call_git(self):
        class API(w.GitHub):
            def __init__(self):super().__init__('owner/repo');self.head_sha='a'*40;self.entries=[];self.calls=[]
            def api(self,path,method='GET',payload=None,missing=False):
                self.calls.append((path,method))
                if '/git/ref/heads/' in path:return {'object':{'sha':self.head_sha}}
                if '/git/commits/' in path:return {'tree':{'sha':'b'*40}}
                if path.endswith('/git/trees'):self.entries=payload['tree'];return {'sha':'d'*40}
                if path.endswith('/git/commits'):return {'sha':'c'*40}
                if method=='PATCH':self.head_sha=payload['sha'];return {}
                raise AssertionError('Unexpected API call')
        for phase in ('USER_DECISION_REQUIRED','FAILED'):
            api=API();state={'state':phase,'codex_attempts':1,'cc_rounds':0}
            with patch.object(w,'git',side_effect=AssertionError('No local Git')):
                self.assertEqual(api.stop_checkpoint(9,'AUTO-006',state),'c'*40)
            record=json.loads(api.entries[0]['content'])
            self.assertTrue(record['needs_user']);self.assertEqual(record['state'],phase)
            self.assertEqual(record['publication_transport'],'GitHub API state branch')
            self.assertEqual(len(api.entries),3)

    def test_unverified_boundary_blocks_even_if_code_review_passes(self):
        tools=w.LiveTools();tools.active_policy={'require_verified_read_boundary':True,'sandbox_boundary':{'external_sentinels_denied':False}}
        with patch.object(w,'git',side_effect=AssertionError('No local Git before boundary gate')):
            with self.assertRaises(w.Gate):tools.preflight('owner/repo')

    def test_long_lived_old_session_and_new_session_latest_moves_forward(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);transcript=root/'collaboration/codex-sessions/public.md';transcript.parent.mkdir(parents=True)
            old=h.empty('codex','old-session-123',str(root),'2026-10-24T00:00:00Z')
            h.add(old,'assistant','OLD','2026-10-30T01:00:00Z','old-response');h.finish(old)
            m.update(m.prepare(root,old,transcript),'a'*40,True)
            new=h.empty('codex','new-session-456',str(root),'2026-10-30T02:00:00Z')
            h.add(new,'assistant','NEW','2026-10-30T03:00:00Z','new-response');h.finish(new)
            m.update(m.prepare(root,new,transcript),'b'*40,True)
            self.assertIn('NEW',(root/'collaboration/live-latest/codex.md').read_text())
            h.add(old,'assistant','OLD SESSION NEW RESPONSE','2026-10-30T04:00:00Z','old-new');h.finish(old)
            m.update(m.prepare(root,old,transcript),'c'*40,True)
            self.assertIn('OLD SESSION NEW RESPONSE',(root/'collaboration/live-latest/codex.md').read_text())
            self.assertEqual(m.load_index(root)['agents']['codex']['response_id'],'old-new')


if __name__=='__main__':unittest.main()
