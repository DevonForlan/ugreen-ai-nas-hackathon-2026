"""Actual scoped checkpoint commits/pushes against a disposable bare remote."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import agent_workflow as w
import agent_transcripts as h
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from test_agent_workflow import Hub


class CheckpointGitTests(unittest.TestCase):
    def test_literal_bracket_filename_publishes_only_exact_file(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve()/'repo';root.mkdir();remote=root.parent/'remote.git'
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            (root/'baseline').write_text('public');git('add','.');git('commit','-m','baseline')
            subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','origin','main')
            (root/'src').mkdir();(root/'src/[x].py').write_text('EXACT = True\n');(root/'src/x.py').write_text('UNRELATED = True\n')
            with patch.object(w,'ROOT',root):sha=w.LiveTools().publish_paths(['src/[x].py'],'test literal path')
            self.assertIn('src/[x].py',git('ls-tree','-r','--name-only',sha))
            self.assertNotIn('src/x.py',git('ls-tree','-r','--name-only',sha))
            self.assertIn('src/x.py',git('status','--short'));self.assertEqual(git('diff','--cached','--name-only'),'')

    def test_real_git_tamper_gate_and_fatal_path_never_execute_helper_or_push(self):
        for fatal in (False,True):
            with self.subTest(fatal=fatal),tempfile.TemporaryDirectory() as folder:
                base=Path(folder).resolve();root=base/'repo';root.mkdir();control=base/'controller';control.mkdir()
                marker=base/'HELPER_EXECUTED.txt'
                def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()
                git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
                (root/'public.txt').write_text('public');git('add','.');git('commit','-m','public baseline');head=git('rev-parse','HEAD')
                hub=Hub();events=[]
                class FakeModelTools(w.LiveTools):
                    def preflight(self,repository):return head
                    def notify(self,*args):events.append(('notify',args[0]))
                    def checkpoint(self,fields,state,phase,summary=''):
                        events.append(('checkpoint',phase))
                        if phase in {'USER_DECISION_REQUIRED','FAILED'}:
                            # If an unsafe stop path calls Git, this real local helper writes a marker.
                            subprocess.run(['git','-C',str(root),'credential','fill'],input=b'protocol=https\nhost=example.invalid\n\n',env=dict(__import__('os').environ,GIT_TERMINAL_PROMPT='0'),capture_output=True,timeout=10)
                    def flush_capture(self,**kwargs):raise AssertionError('Unsafe capture after tamper')
                    def codex(self,prompt,timeout):
                        with (root/'.git/config').open('a') as stream:
                            stream.write('\n[credential]\n\thelper = !echo EXECUTED > "'+str(marker).replace('\\','/')+'"\n')
                        if fatal:raise RuntimeError('Simulated fatal after Git tamper')
                        return {'result':'HANDOFF','summary':'public','report_path':'','gate_reason':'','user_question':''},'UNKNOWN'
                policy={'repository':'owner/repo','trusted_authors':['owner'],'allowed_task_prefixes':['AUTO-'],
                    'max_codex_attempts':3,'max_cc_review_rounds':3,'agent_timeout_seconds':30,'max_review_bytes':65536,
                    'plans':{'AUTO-T1':{'issue_number':1,'body_sha256':w.digest(hub.item['body']),'codex_enabled':True,'cc_enabled':True,
                        'sandbox_acknowledged':True,'required_tests':[['python','-m','unittest']],'allowed_write_paths':['src/']}}}
                with patch.object(w,'ROOT',root),patch.object(w,'CONTROL_ROOT',control):
                    engine=w.Engine(hub,FakeModelTools(),policy)
                    if fatal:
                        with self.assertRaises(RuntimeError):engine.step(hub.issue(1))
                    else:self.assertEqual(engine.step(hub.issue(1)),'USER_DECISION_REQUIRED')
                self.assertEqual(hub.state['state'],'FAILED' if fatal else 'USER_DECISION_REQUIRED')
                self.assertTrue(hub.comments);self.assertTrue((control/'runtime/AUTO_STOP.json').exists())
                self.assertFalse(marker.exists());self.assertEqual(git('rev-parse','HEAD'),head)
                self.assertNotIn(('checkpoint','FAILED'),events);self.assertNotIn(('checkpoint','USER_DECISION_REQUIRED'),events)

    def test_actual_fetch_and_native_capture_do_not_impersonate_model_edits(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder).resolve();root=base/'repo';root.mkdir();remote=base/'remote.git'
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            (root/'fixture.py').write_text('PUBLIC = True\n');git('add','.');git('commit','-m','baseline')
            subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','origin','main');head=git('rev-parse','HEAD')
            tools=w.LiveTools()
            with patch.object(w,'ROOT',root),patch.object(h,'archive_root',return_value=base/'global-visible'):
                self.assertEqual(tools.diff(head,head),'')
                before=tools.snapshot()  # controller fetch precedes the model boundary
                for agent in ('codex','claude'):
                    native=base/(agent+'.jsonl')
                    if agent=='codex':
                        rows=[{'timestamp':'2026-10-30T01:00:00Z','type':'session_meta','payload':{'id':'public-session-1234','cwd':str(root),'timestamp':'2026-10-30T01:00:00Z'}},
                            {'timestamp':'2026-10-30T01:00:01Z','type':'response_item','payload':{'type':'message','role':'assistant','phase':'final_answer','content':[{'type':'output_text','text':'Public final'}]}}]
                        native.write_text(''.join(json.dumps(row)+'\n' for row in rows))
                        session=h.read_native(native,'codex');proof=h.prove_exit(session,'Public final',0,'2026-10-30T01:00:02Z')
                    else:
                        session,proof=h.claude_result({'session_id':'public-claude-1234','result':'Public final','is_error':False},'Public prompt',root,'2026-10-30T01:00:00Z','2026-10-30T01:00:02Z')
                    tools._retain_capture(session,proof)
                    self.assertEqual(tools.snapshot(),before)
                    self.assertTrue((base/'global-visible'/agent/session['session_id']/'manifest.json').exists())

    def test_real_checkpoint_push_and_dirty_model_files_are_not_staged(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve()/'repo';root.mkdir()
            remote=root.parent/'remote.git'
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args]).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            (root/'fixture.py').write_text('BASELINE = True\n')
            git('add','.');git('commit','-m','baseline')
            subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','-u','origin','main')
            (root/'fixture.py').write_text('MODEL_WORK_UNCOMMITTED = True\n')
            tools=w.LiveTools()
            state={'state':'CODEX_RUNNING','codex_attempts':1,'cc_rounds':0}
            with patch.object(w,'ROOT',root):
                commit=tools.checkpoint({'Task ID':'AUTO-CKPT'},state,'STARTED','Trusted bounded task')
            self.assertEqual(commit,git('ls-remote','origin','refs/heads/main').split()[0])
            self.assertEqual(git('show','HEAD:fixture.py'),'BASELINE = True')
            data=json.loads(git('show','HEAD:collaboration/checkpoints/AUTO-CKPT/latest.json'))
            self.assertEqual(data['phase'],'STARTED');self.assertEqual(data['attempt_number'],1)
            self.assertEqual(git('diff','--cached','--name-only'),'')
            self.assertIn('fixture.py',git('status','--short'))


if __name__=='__main__':unittest.main()
