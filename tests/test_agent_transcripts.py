"""Visible-only retention and post-exit evidence; no model/API calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
import agent_transcripts as h
import agent_history_sync as sync


def event(kind,payload,day=25):
    return {'timestamp':f'2026-10-{day}T13:37:20Z','type':kind,'payload':payload}


def fixture(cwd,sid='session-12345678'):
    return [event('session_meta',{'id':sid,'cwd':str(cwd),'timestamp':'2026-10-25T13:37:20Z'}),
            event('response_item',{'type':'message','role':'user','content':[{'type':'input_text','text':'REG-001 visible task'}]}),
            event('response_item',{'type':'message','role':'assistant','phase':'final_answer','content':[{'type':'output_text','text':'visible final'}]},27)]


class TranscriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.repo=self.root/'repo';self.repo.mkdir();(self.repo/'.git').mkdir()
        self.local=self.root/'visible'
        self.source=self.root/'native.jsonl'
        self.rows=fixture(self.repo)

    def read(self,agent='codex'):
        self.source.write_text(''.join(json.dumps(x)+'\n' for x in self.rows),encoding='utf-8')
        return h.read_native(self.source,agent)

    def item(self,proof=False):
        s=self.read()
        p=h.prove_exit(s,'visible final',0,'2026-10-27T14:00:00Z') if proof else None
        return h.archive(s,self.local,self.repo,p)

    def test_multi_day_one_session_retains_timestamps_and_turns(self):
        s=self.read();item=h.archive(s,self.local,self.repo)
        self.assertEqual(s['session_id'],'session-12345678')
        self.assertIn('2026-10-25',item['transcript'].name)
        text=item['transcript'].read_text(encoding='utf-8')
        self.assertIn('2026-10-27',text)
        self.assertIn('Latest visible response timestamp',text)
        self.assertIn('final_response_captured: unknown',text)
        self.assertEqual(len(list((item['directory']/'turns').glob('*.md'))),1)

    def test_incremental_append_preserves_earlier_turn_and_idempotent_mtime(self):
        item=self.item();before=item['transcript'].stat().st_mtime_ns
        unchanged=self.item()
        self.assertFalse(unchanged['changed'])
        self.assertEqual(before,item['transcript'].stat().st_mtime_ns)
        self.rows.append(event('response_item',{'type':'message','role':'user','content':'next visible question'},27))
        updated=self.item()
        self.assertEqual(len(updated['session']['turns']),2)
        self.assertIn('visible final',updated['transcript'].read_text(encoding='utf-8'))
        self.assertGreater(updated['session']['source_event_count'],item['session']['source_event_count'])

    def test_multiple_sessions_projects_and_outside_git(self):
        self.item()
        other=self.root/'other';other.mkdir();(other/'.git').mkdir()
        self.rows=fixture(other,'session-OTHER123')
        s=self.read();item=h.archive(s,self.local,self.repo)
        self.assertIsNone(item['transcript'])
        self.assertEqual(len(list((self.repo/'collaboration/codex-sessions').glob('*.md'))),1)
        outside=self.root/'outside';outside.mkdir()
        self.rows=fixture(outside,'session-NONGIT12')
        item=h.archive(self.read(),self.local)
        self.assertTrue((item['directory']/'session.md').exists())
        self.assertIsNone(item['transcript'])
        self.assertEqual(len(list((self.local/'codex').iterdir())),3)

    def test_mixed_project_session_never_publishes(self):
        other=self.root/'different';other.mkdir()
        self.rows.append(event('turn_context',{'cwd':str(other)},27))
        item=h.archive(self.read(),self.local,self.repo)
        self.assertIsNone(item['transcript'])

    def test_native_rewrite_or_truncation_preserves_archive(self):
        item=self.item();before=item['transcript'].read_text(encoding='utf-8')
        self.rows.pop()
        with self.assertRaises(ValueError):self.item()
        self.assertEqual(item['transcript'].read_text(encoding='utf-8'),before)

    def test_only_outer_matching_post_exit_proof_can_certify(self):
        s=self.read()
        self.assertIsNone(h.prove_exit(s,'not the final',0,h.now()))
        self.assertIsNone(h.prove_exit(s,'visible final',1,h.now()))
        item=self.item(proof=True)
        self.assertIs(item['manifest']['final_response_captured'],True)
        self.rows.append(event('response_item',{'type':'message','role':'user','content':'new request'},27))
        item=self.item()
        self.assertIs(item['manifest']['final_response_captured'],False)

    def test_malformed_partial_event_never_certifies_complete(self):
        self.read()
        with self.source.open('a',encoding='utf-8') as f:f.write('{bad')
        s=h.read_native(self.source,'codex')
        self.assertEqual(s['malformed_events'],1)
        self.assertIsNone(h.prove_exit(s,'visible final',0,h.now()))

    def test_hidden_internal_secret_and_environment_exclusion(self):
        self.rows.extend([
            event('response_item',{'type':'reasoning','encrypted_content':'HIDDEN_ENCRYPTED'}),
            event('response_item',{'type':'message','role':'developer','content':'HIDDEN_DEVELOPER'}),
            event('response_item',{'type':'message','role':'assistant','channel':'analysis','content':'HIDDEN_ANALYSIS'}),
            event('response_item',{'type':'function_call','call_id':'private1','name':'exec','arguments':'Get-ChildItem Env:'}),
            event('response_item',{'type':'function_call_output','call_id':'private1','output':'HIDDEN_ENV_VALUE'}),
            event('response_item',{'type':'function_call_output','call_id':'safe1','output':'sk-'+'x'*32})])
        item=self.item()
        text=item['transcript'].read_text(encoding='utf-8')
        for forbidden in ('HIDDEN_ENCRYPTED','HIDDEN_DEVELOPER','HIDDEN_ANALYSIS','HIDDEN_ENV_VALUE','x'*32):
            self.assertNotIn(forbidden,text)
        self.assertIn('REDACTED',text)
        nested=json.dumps({'output':json.dumps({'role':'system','content':'HIDDEN_NESTED'})})
        self.assertNotIn('HIDDEN_NESTED',h.clean(nested))

    def test_cross_project_inventory_and_raw_runtime_dump_omitted(self):
        value={'output':json.dumps({'event_types':{},'sessions':[{'cwd':'UNRELATED_PROJECT','text':'PRIVATE_OTHER_TURN'}]})}
        self.assertNotIn('UNRELATED_PROJECT',h.clean(value))
        self.assertNotIn('PRIVATE_OTHER_TURN',h.clean(value))
        self.assertIn('OMITTED',h.clean(json.dumps(event('response_item',{'type':'reasoning','text':'NEVER_SEE'}))))

    def test_unsafe_ids_symlinks_and_archive_inside_git_rejected(self):
        self.rows[0]['payload']['id']='../../escape'
        with self.assertRaises(ValueError):self.read()
        with self.assertRaises(ValueError):h.archive_root(self.repo/'history')

    def test_claude_native_filters_thinking_system_api_blobs_and_meta(self):
        def row(kind,blocks,**extra):
            return dict(type=kind,sessionId='claude-12345678',cwd=str(self.repo),timestamp='2026-10-27T12:00:00Z',
                        message={'role':kind,'content':blocks},**extra)
        self.rows=[row('user','visible question'),row('assistant',[{'type':'thinking','thinking':'HIDDEN_THINKING'},
                      {'type':'text','text':'visible CC answer'}]),row('system','HIDDEN_SYSTEM'),
                   row('api-request-blob',[{'type':'text','text':'HIDDEN_REQUEST'}]),
                   row('user','HIDDEN_META',isMeta=True)]
        item=h.archive(self.read('claude'),self.local,self.repo)
        text=item['transcript'].read_text(encoding='utf-8')
        self.assertIn('visible CC answer',text)
        for secret in ('HIDDEN_THINKING','HIDDEN_SYSTEM','HIDDEN_REQUEST','HIDDEN_META'):self.assertNotIn(secret,text)
        self.assertIn('cc-sessions',str(item['transcript']))

    def test_codex_public_final_capture_ignores_reasoning_and_requires_terminal(self):
        rows=[{'type':'thread.started','thread_id':'exec-session123'},
              {'type':'item.completed','item':{'id':'hidden','type':'reasoning','text':'HIDDEN_WIRE'}},
              {'type':'item.completed','item':{'id':'final','type':'agent_message','text':'final captured'}},
              {'type':'turn.completed'}]
        raw='\n'.join(map(json.dumps,rows))
        s,p=h.codex_result(raw,'question', 'final captured',self.repo,h.now(),h.now(),native_roots=[])
        self.assertTrue(p)
        self.assertNotIn('HIDDEN_WIRE',h.packed(h.events(s)))
        s,p=h.codex_result('\n'.join(map(json.dumps,rows[:-1])),'question','final captured',self.repo,h.now(),h.now(),native_roots=[])
        self.assertIsNone(p)

    def test_real_child_exits_before_final_file_is_certified(self):
        output=self.root/'final.txt'
        code="import pathlib,json,sys;pathlib.Path(sys.argv[1]).write_text('exited final');print(json.dumps({'type':'thread.started','thread_id':'child-session123'}));print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'exited final'}}));print(json.dumps({'type':'turn.completed'}))"
        process=subprocess.Popen([sys.executable,'-c',code,str(output)],stdout=subprocess.PIPE,text=True)
        raw,_=process.communicate(timeout=30)
        self.assertIsNotNone(process.returncode)
        s,p=h.codex_result(raw,'fixture prompt',output.read_text(),self.repo,h.now(),h.now(),process.returncode,native_roots=[])
        self.assertTrue(h.captured(s,p))

    def test_claude_result_retained_without_native_persistence(self):
        result=dict(result='PASS',summary='verified fixture',required_changes=[],recommended_next_task='',user_question='')
        s,p=h.claude_result({'session_id':'claude-headless123','structured_output':result},'review fixture',self.repo,h.now(),h.now())
        self.assertTrue(p)
        item,path,value=h.save_run(s,p,self.repo,'AUTO-002',root=self.local)
        self.assertTrue(path.exists());self.assertTrue(item['transcript'].exists())
        self.assertFalse(h.complete(value))
        self.assertEqual(value['status'],'LOCAL_ONLY')
        _,bad=h.claude_result({'session_id':'claude-headless123','result':'failed','is_error':True},'q',self.repo,h.now(),h.now())
        self.assertIsNone(bad)

    def test_claude_timestamp_can_first_appear_after_session_metadata(self):
        self.rows=[{'type':'mode','sessionId':'claude-no-time123','cwd':str(self.repo)},
                   {'type':'user','sessionId':'claude-no-time123','cwd':str(self.repo),
                    'timestamp':'2026-10-27T12:00:00Z','message':{'role':'user','content':'visible question'}},
                   {'type':'assistant','sessionId':'claude-no-time123','timestamp':'2026-10-27T12:01:00Z',
                    'message':{'role':'assistant','content':[{'type':'text','text':'visible answer'}]}}]
        session=self.read('claude')
        self.assertEqual(session['started_at'],'2026-10-27T12:00:00Z')
        self.assertTrue(h.archive(session,self.local,self.repo)['transcript'].exists())

    def test_sync_complete_requires_every_proof_and_publication_field(self):
        item=self.item(proof=True);value=h.ledger(item,'AUTO-002')
        value.update(secret_scan='PASS',commit_sha='a'*40,github_synced=True)
        self.assertTrue(h.complete(value))
        for key in ('final_response_captured','local_archive_updated','project_transcript_updated','github_synced','ended_at','commit_sha'):
            altered=dict(value);altered[key]=False
            self.assertFalse(h.complete(altered),key)
        value['malformed_events']=1;self.assertFalse(h.complete(value))

    def test_raw_jsonl_and_nonmarkdown_cc_exports_forbidden(self):
        for path in ['collaboration/codex-sessions/raw.jsonl','collaboration/cc-sessions/raw.jsonl',
                     'collaboration/cc-sessions/runtime.json','auth.json']:
            self.assertIsNotNone(h.scan.forbidden(path))

    def test_transient_windows_replace_lock_retries_without_deleting_original(self):
        path=self.root/'retry.md';path.write_text('old',encoding='utf-8')
        real=h.os.replace;calls=[]
        def locked(src,dst):
            calls.append(1)
            if len(calls)<3:raise PermissionError('fixture sharing violation')
            return real(src,dst)
        with patch.object(h.os,'replace',side_effect=locked),patch.object(h.time,'sleep'):
            h.atomic(path,'new')
        self.assertEqual(path.read_text(encoding='utf-8'),'new')
        self.assertEqual(len(calls),3)

    def test_archive_writer_lock_is_exclusive_and_released(self):
        path=self.root/'lock'
        with h.lease(path):
            with self.assertRaises(RuntimeError):
                with h.lease(path):pass
        self.assertFalse(path.exists())


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir();(self.repo/'.git').mkdir()
        source=self.root/'source.jsonl'
        source.write_text(''.join(json.dumps(x)+'\n' for x in fixture(self.repo)),encoding='utf-8')
        s=h.read_native(source,'codex');p=h.prove_exit(s,'visible final',0,h.now())
        self.item,self.path,self.value=h.save_run(s,p,self.repo,'AUTO-002',root=self.root/'archive')
        self.staged=[];self.calls=[]

    def fake_git(self,root,*args):
        self.calls.append(args)
        if args==('branch','--show-current'):return 'main'
        if args[:2]==('remote','get-url'):return 'https://github.com/owner/repo.git'
        if args==('diff','--cached','--name-only'):return '\n'.join(self.staged)
        if args==('diff','--name-only','HEAD'):
            return '\n'.join([self.item['transcript'].relative_to(root).as_posix(),self.path.relative_to(root).as_posix()])
        if args[0]=='add':self.staged=list(args[2:])
        if args[0]=='commit':self.staged=[]
        return ''

    def test_two_phase_payload_then_verified_receipt_no_self_sha_loop(self):
        with patch.object(sync,'git',side_effect=self.fake_git),patch.object(sync,'checked'),patch.object(sync,'verify_push',side_effect=['a'*40,'b'*40]) as push:
            result=sync.publish(self.item,self.path,self.value,self.repo)
        self.assertEqual(result['status'],'SYNC_COMPLETE')
        self.assertEqual(self.value['commit_sha'],'a'*40)
        self.assertEqual(push.call_count,2)
        self.assertEqual(len([c for c in self.calls if c[0]=='commit']),2)
        self.assertTrue(h.complete(json.loads(self.path.read_text(encoding='utf-8'))))
        self.assertFalse(any('--force' in c or '--hard' in c for c in self.calls))

    def test_push_failure_never_claims_sync_complete(self):
        with patch.object(sync,'git',side_effect=self.fake_git),patch.object(sync,'checked'),patch.object(sync,'verify_push',side_effect=sync.SyncError('network')):
            with self.assertRaises(sync.SyncError):sync.publish(self.item,self.path,self.value,self.repo)
        saved=json.loads(self.path.read_text(encoding='utf-8'))
        self.assertEqual(saved['status'],'LOCAL_ONLY');self.assertFalse(saved['github_synced'])

    def test_second_receipt_push_failure_also_reverts_local_claim(self):
        with patch.object(sync,'git',side_effect=self.fake_git),patch.object(sync,'checked'),patch.object(sync,'verify_push',side_effect=['a'*40,sync.SyncError('network')]):
            with self.assertRaises(sync.SyncError):sync.publish(self.item,self.path,self.value,self.repo)
        self.assertEqual(self.value['status'],'LOCAL_ONLY')
        self.assertIn('github_synced: false',self.item['transcript'].read_text(encoding='utf-8'))

    def test_secret_scan_stops_before_staging(self):
        with patch.object(sync,'git',side_effect=self.fake_git),patch.object(sync,'checked',side_effect=sync.SecurityError('blocked')):
            with self.assertRaises(sync.SecurityError):sync.publish(self.item,self.path,self.value,self.repo)
        self.assertFalse(any(c[0]=='add' for c in self.calls))
        self.assertEqual(self.value['status'],'FAILED')


if __name__=='__main__':unittest.main()
