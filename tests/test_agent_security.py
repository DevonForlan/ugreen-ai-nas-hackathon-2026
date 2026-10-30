import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import agent_security as s
import agent_checkpoints as c
import agent_workflow as w
from test_agent_workflow import Hub,Tools,task_body,review


class SecurityTests(unittest.TestCase):
    def test_snapshot_includes_ignored_hooks_and_bytecode(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve()
            subprocess.run(['git','init',str(root)],capture_output=True,check=True)
            (root/'.gitignore').write_text('.vscode/\n__pycache__/\n')
            before=s.scope_snapshot(root)
            for name in ('.vscode/tasks.json','__pycache__/danger.pyc','.git/hooks/pre-commit'):
                path=root/name;path.parent.mkdir(exist_ok=True);path.write_text('changed executable data')
            after=s.scope_snapshot(root)
            for name in ('.vscode/tasks.json','__pycache__/danger.pyc','.git/hooks/pre-commit'):
                self.assertNotEqual(before.get(name),after[name])

    def test_nested_instructions_and_controller_artifacts_protected(self):
        for name in ('src/AGENTS.md','src/agents.md','src/lib/CLAUDE.md','src/.CODEX/config.toml','src/.claude/hooks.json',
                     'collaboration/cc-reports/forged.md','collaboration/checkpoints/t/latest.json'):
            with self.assertRaises(w.Gate):w.allowed_changes([name],{'allowed_write_paths':['src/','collaboration/']},'AUTO-T1')

    def test_native_sandbox_argv_has_no_host_fallback(self):
        args=s.sandbox_command('native-codex.exe',['python','-m','unittest'],Path.cwd())
        self.assertEqual(args[0],'native-codex.exe')
        self.assertIn('sandbox',args);self.assertIn('-B',args)
        self.assertIn(':workspace',args)
        self.assertIn('--sandbox-state-disable-network',args)
        with self.assertRaises(ValueError):s.sandbox_command('native',['unknown-relative-runner'],Path.cwd())

    def test_git_hooks_fsmonitor_never_executed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'.git').mkdir()
            self.assertIn('core.fsmonitor=false',s.git_prefix(root))
            (root/'.git/agent-empty-hooks/anything').write_text('bad')
            with self.assertRaises(RuntimeError):s.git_prefix(root)

    def test_specific_user_gate_options(self):
        for reason in ('Secret detected','Required tests failed','Scope expansion','Maximum iterations'):
            question,options=s.gate_details(reason)
            self.assertNotEqual(question,'How should this task proceed?')
            self.assertEqual(len(options),2)

    def test_checkpoint_schema_fields_and_sequence_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            state={'state':'CODEX_RUNNING','codex_attempts':1,'cc_rounds':0}
            data=c.value('AUTO-T1','STARTED',state,'a'*40,None,'Implement scoped requirement')
            paths=c.write(Path(folder),data,1)
            self.assertEqual(len(paths),3)
            self.assertTrue((Path(folder)/'collaboration/checkpoints/AUTO-T1/latest.json').exists())
            data['progress_summary']='different transition'
            with self.assertRaises(ValueError):c.write(Path(folder),data,1)

    def test_test_evidence_preserves_head_and_tail(self):
        output='HEAD EVIDENCE\n'+'case passed\n'*1000+'TAIL EVIDENCE\n'
        fake=type('Native',(),{'native_codex':lambda self:'native.exe'})()
        with patch.object(w,'load_module',return_value=fake),patch.object(w,'command',return_value=output) as run:
            tests=w.LiveTools().tests([['python','-m','unittest']])
        self.assertNotIn('output',tests[0])
        self.assertEqual((w.ROOT/tests[0]['artifact_path']).read_text(encoding='utf-8'),output)
        (w.ROOT/tests[0]['artifact_path']).unlink()
        self.assertIn('sandbox',run.call_args.args[0])
        self.assertNotIn('finalize-codex-task.py',str(run.call_args))

    def test_control_hash_changes_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'scripts').mkdir();(root/'scripts/a.py').write_text('pass')
            report=root/'review.md';report.write_text('independent review PASS')
            import hashlib
            policy={'approval':{'trust_root':'B','test_boundary':'A','review_result':'PASS','review_report':'review.md','review_report_sha256':hashlib.sha256(report.read_bytes()).hexdigest()},'control_plane_sha256':s.control_files(root)}
            s.verify_control(root,policy)
            (root/'scripts/new.py').write_text('unexpected')
            with self.assertRaises(ValueError):s.verify_control(root,policy)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.hub=Hub();self.tools=Tools()
        self.policy={'repository':'owner/repo','trusted_authors':[],'allowed_task_prefixes':['AUTO-'],
            'agent_timeout_seconds':60,'max_review_bytes':98304,'max_steps':6,'max_codex_attempts':3,'max_cc_review_rounds':3,
            'plans':{'AUTO-T1':{'issue_number':1,'body_sha256':w.digest(self.hub.item['body']),'codex_enabled':True,'cc_enabled':True,'sandbox_acknowledged':True,'allowed_write_paths':['src/'],'required_tests':[['python','-m','unittest']],'followups':{}}}}

    def test_verified_handoff_recovery_does_not_call_model(self):
        self.hub.item['labels']=['CODEX_RUNNING']
        self.hub.state={'state':'CODEX_RUNNING','body_sha256':w.digest(self.hub.item['body']),'codex_attempts':1,'cc_rounds':0,'history':[],
            'handoff':{'attempt_number':1,'head':self.tools.head,'report':self.tools.report,'tests':[{'exit_code':0}]}}
        self.hub.version='1'
        state=w.Engine(self.hub,self.tools,self.policy).recover(self.hub.issue(1))
        self.assertEqual(state,'READY_FOR_CC_REVIEW');self.assertEqual(self.tools.codex_calls,0)
        self.assertEqual(self.hub.state['codex_attempts'],1)

    def test_uncertain_running_state_never_replays(self):
        self.hub.item['labels']=['CODEX_RUNNING']
        self.hub.state={'state':'CODEX_RUNNING','body_sha256':w.digest(self.hub.item['body']),'codex_attempts':1,'cc_rounds':0,'history':[]}
        with self.assertRaises(w.Gate):w.Engine(self.hub,self.tools,self.policy).recover(self.hub.issue(1))
        self.assertEqual(self.tools.codex_calls,0)

    def test_verified_cc_recovery_keeps_independent_authority(self):
        self.hub.item['labels']=['CC_REVIEWING']
        self.hub.state={'state':'CC_REVIEWING','body_sha256':w.digest(self.hub.item['body']),'codex_attempts':1,'cc_rounds':1,'history':[],
            'review':review(),'review_report':'collaboration/cc-reports/check.md','review_commit_sha':'a'*40,
            'review_round_proof':1,'reviewed_head':'a'*40,'handoff':{'head':'a'*40}}
        self.hub.artifact=lambda path,sha: '# CC Review\n\n'+json.dumps({'issue':1,'reviewed_commit':'a'*40,'review':review()})
        self.hub.version='1'
        self.assertEqual(w.Engine(self.hub,self.tools,self.policy).recover(self.hub.issue(1)),'DONE')
        self.assertEqual(self.tools.cc_calls,0)

    def test_all_phase_checkpoints_and_no_duplicate_done_work(self):
        phases=[]
        self.tools.checkpoint=lambda fields,state,phase,summary='':phases.append(phase)
        with patch.object(w.scanner,'scan_repo',return_value=(1,[])):
            engine=w.Engine(self.hub,self.tools,self.policy)
            self.assertEqual(engine.step(self.hub.issue(1)),'READY_FOR_CC_REVIEW')
            self.assertEqual(engine.step(self.hub.issue(1)),'DONE')
            self.tools.head='9'*40  # unrelated push alone cannot re-authorize a DONE task
            self.assertEqual(w.Engine(self.hub,self.tools,self.policy).step(self.hub.issue(1)),'DONE')
        self.assertEqual(self.tools.codex_calls,1);self.assertEqual(self.tools.cc_calls,1)
        self.assertEqual(phases,['STARTED','IMPLEMENTATION_COMPLETE','TEST_COMPLETE','READY_FOR_CC_REVIEW','CC_REVIEWING','CC_PASS','DONE'])

    def test_recovery_rejects_old_review_round(self):
        self.hub.item['labels']=['CC_REVIEWING']
        self.hub.state={'state':'CC_REVIEWING','body_sha256':w.digest(self.hub.item['body']),'codex_attempts':2,'cc_rounds':2,'history':[],
            'review':review(),'review_report':'old.md','review_commit_sha':'a'*40,
            'review_round_proof':1,'reviewed_head':'a'*40,'handoff':{'head':'b'*40}}
        with self.assertRaises(w.Gate):w.Engine(self.hub,self.tools,self.policy).recover(self.hub.issue(1))
        self.assertEqual(self.tools.cc_calls,0)


class LeaseRecoveryTests(unittest.TestCase):
    def test_trusted_outside_record_blocks_pid_forgery_and_releases_only_dead_owner(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder).resolve();root=base/'repo';control=base/'controller'
            (root/'.git').mkdir(parents=True);control.mkdir()
            issue=Hub().issue(1)
            marker='a'*40
            class Remote(w.GitHub):
                def __init__(self):
                    super().__init__('owner/repo');self.refs={'heads/agent-locks/executor':marker,'heads/agent-locks/issue-1':marker}
                def head(self):return 'b'*40
                def ledger(self,number):return None,None
                def api(self,path,method='GET',payload=None,missing=False):
                    if '/git/commits/' in path:return {'tree':{'sha':'d'*40}}
                    if path.endswith('/git/commits'):return {'sha':'c'*40}
                    if path.endswith('/git/refs') and method=='POST':
                        key=payload['ref'][5:]
                        if key in self.refs:raise w.RemoteError('exists')
                        self.refs[key]=payload['sha'];return None
                    if method=='DELETE':self.refs.pop(path.split('/git/refs/')[1]);return None
                    key=path.split('/git/ref/')[1]
                    return {'object':{'sha':self.refs[key]}} if key in self.refs else None
            hub=Remote();policy={'repository':'owner/repo','trusted_authors':[],'plans':{'AUTO-T1':{'issue_number':1,'body_sha256':w.digest(issue['body'])}}}
            record={'owner':'owned-nonce','pid':9999,'process_birth':'old-birth','host_id':'local-host','repository':'owner/repo','issue_number':1,'body_sha256':w.digest(issue['body']),'remote_marker':marker,'status':'CLAIMED'}
            lock=root/'.git/agent-workflow.lock'
            with patch.object(w,'ROOT',root),patch.object(w,'CONTROL_ROOT',control),patch.object(w,'verify_control'),patch.object(w,'host_id',return_value='local-host'):
                w.trusted_lease_path().write_text(json.dumps(record))
                lock.write_text(json.dumps(dict(record,pid=1234)))  # worktree-side forgery must not authorize recovery
                with patch.object(w,'process_birth',return_value='old-birth'):
                    with self.assertRaises(w.Locked):w.recover_locks(hub,policy,issue,lock)
                self.assertEqual(len(hub.refs),2)
                with patch.object(w,'process_birth',return_value=None):
                    w.recover_locks(hub,policy,issue,lock)
                self.assertFalse(lock.exists());self.assertFalse(hub.refs)
                self.assertEqual(json.loads(w.trusted_lease_path().read_text())['status'],'RECOVERED_NO_STATE_OR_COUNTER_RESET')


if __name__=='__main__':unittest.main()
