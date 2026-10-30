"""Regression evidence for independent AUTO-005 readiness findings; no model calls."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import agent_workflow as w
import agent_checkpoints as c
import agent_security as s
from test_agent_workflow import Hub,Tools,review,task_body


class ReadinessFixTests(unittest.TestCase):
    def test_followup_partial_write_recovers_existing_issue_without_duplicate(self):
        hub=Hub();tools=Tools();policy={'agent_timeout_seconds':30,'max_review_bytes':4096}
        engine=w.Engine(hub,tools,policy);plan={'followups':{'AUTO-T2':{'title':'next','body':task_body('AUTO-T2')}}}
        state={'state':'CC_REVIEWING','review':dict(review(),recommended_next_task='AUTO-T2')}
        def partial(title,body):
            hub.created.append((title,body));raise w.RemoteError('Simulated response lost after creation')
        hub.create_issue=partial;hub.find_followup=lambda body,policy:None
        with self.assertRaises(w.RemoteError):engine.followup(hub.issue(1),state,None,plan)
        self.assertEqual(hub.state['followup_intent']['status'],'CREATE_STARTED')
        fresh,version=hub.ledger(1);hub.find_followup=lambda body,policy:{'number':2}
        engine.followup(hub.issue(1),fresh,version,plan,recovery=True)
        self.assertEqual(len(hub.created),1);self.assertEqual(hub.state['next_issue'],2)

    def test_actual_command_preserves_stdout_stderr_and_failure(self):
        result=w.command([sys.executable,'-B','-c','import sys; print("public stdout"); print("public stderr",file=sys.stderr)'],include_stderr=True)
        self.assertIn('public stdout',result);self.assertIn('public stderr',result)
        with self.assertRaises(w.CommandFailure) as caught:
            w.command([sys.executable,'-B','-c','import sys; print("public failure"); sys.exit(7)'])
        self.assertEqual(caught.exception.code,7);self.assertIn('public failure',caught.exception.stdout)
        self.assertNotIn('public failure',str(caught.exception))
        isolated=w.command([sys.executable,'-B','-c','import os; print(os.environ["CODEX_NOTIFY_DISABLED"])'],isolate_env=True)
        self.assertEqual(isolated.strip(),'1')

    def test_exact_code_review_is_not_sanitizer_rewritten(self):
        code="secret_scan='PASS'\nreturn stdout + (stderr if include_stderr else '')"
        self.assertEqual(w.exact_text(code),code)
        prompt=w.review_prompt({},'',code,[],65536)
        self.assertIn("secret_scan='PASS'",prompt);self.assertIn('return stdout',prompt)

    def test_every_phase_validates_and_attests_only_verified_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            for index,phase in enumerate(sorted(c.PHASES),1):
                record=c.value('AUTO-SCHEMA',phase,{'state':'CODEX_RUNNING','codex_attempts':1,'cc_rounds':0},'a'*40,None)
                self.assertFalse(record['remote_verified']);c.write(Path(folder),record,index)
                c.attest(Path(folder),record,index,'b'*40)
                data=json.loads((Path(folder)/'collaboration/checkpoints/AUTO-SCHEMA/latest.json').read_text())
                self.assertTrue(data['remote_verified']);self.assertEqual(data['verified_payload_commit'],'b'*40)
                with self.assertRaises(ValueError):c.validate(dict(data,unexpected=True))
                with self.assertRaises(ValueError):c.validate(dict(data,source_commit_sha='HEAD'))

    def test_emergency_checkpoint_failure_cannot_suppress_comment_or_notification(self):
        hub=Hub();tools=Tools()
        policy={'agent_timeout_seconds':30,'max_review_bytes':4096,'plans':{'AUTO-T1':{'issue_number':1}}}
        state={'state':'READY_FOR_CODEX','body_sha256':w.digest(hub.item['body']),'codex_attempts':0,'cc_rounds':0,'history':[]}
        version=None
        tools.checkpoint=lambda *a:(_ for _ in ()).throw(w.Gate('Secret detected before checkpoint publication'))
        w.Engine(hub,tools,policy).gate(hub.issue(1),state,version,'Secret detected')
        self.assertEqual(hub.state['state'],'USER_DECISION_REQUIRED')
        self.assertTrue(hub.comments);self.assertTrue(tools.notifications)
        self.assertIn('checkpoint_error',hub.state)

    def test_failed_tests_retain_actual_exit_and_sanitized_output(self):
        native=type('Native',(),{'native_codex':lambda self:'native.exe'})()
        tools=w.LiveTools()
        with patch.object(w,'load_module',return_value=native),patch.object(w,'command',side_effect=w.CommandFailure(2,'HEAD\n','TAIL\n')):
            with self.assertRaises(w.Gate):tools.tests([['python','-m','unittest']])
        self.assertEqual(tools.last_test_evidence[0]['exit_code'],2)
        self.assertEqual(tools.last_test_evidence[0]['output'],'HEAD\nTAIL\n')

    def test_reviewer_user_gate_requires_options_and_recommendation(self):
        data=review('USER_DECISION_REQUIRED');data['user_question']='Which one?'
        with self.assertRaises(w.Gate):w.review_json(data)
        data['user_question']='Choose? Options: stop; revise. Recommendation: stop.'
        self.assertEqual(w.review_json(data)['result'],'USER_DECISION_REQUIRED')

    def test_installer_rejects_consistent_mutable_policy_source_and_report_forgery(self):
        spec=importlib.util.spec_from_file_location('installer',Path(w.__file__).with_name('install-agent-controller.py'))
        installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'repo';root.mkdir();(root/'scripts').mkdir();(root/'automation').mkdir()
            source=root/'scripts/core.py';source.write_text('REVIEWED = True\n')
            report=root/'review.md';report.write_text('Independent PASS\n')
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            git('add','.');git('commit','-m','reviewed fixture');head=git('rev-parse','HEAD')
            remote=Path(folder)/'remote.git';subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','origin','main')
            policy={'approval':{'trust_root':'B','test_boundary':'A','review_result':'PASS','reviewed_head':head,
                'review_report':'review.md','review_report_sha256':hashlib.sha256(report.read_bytes()).hexdigest()},
                'control_plane_sha256':s.control_files(root),'plans':{},'allowed_task_prefixes':['AUTO-']}
            path=root/'automation/policy.json'
            def save():
                path.write_text(json.dumps(policy));return hashlib.sha256(path.read_bytes()).hexdigest()
            expected=save()
            with self.assertRaises(ValueError):installer.install(root,Path(folder)/'controller')
            policy['allowed_task_prefixes']=['ARBITRARY-'];save()
            with self.assertRaises(ValueError):installer.install(root,Path(folder)/'controller',expected)
            source.write_text('UNREVIEWED = True\n');report.write_text('Forged PASS\n')
            policy['control_plane_sha256']=s.control_files(root)
            policy['approval']['review_report_sha256']=hashlib.sha256(report.read_bytes()).hexdigest()
            with self.assertRaises(ValueError):installer.install(root,Path(folder)/'controller',save())
            source.write_text('REVIEWED = True\n');report.write_text('Independent PASS\n')
            policy['allowed_task_prefixes']=['AUTO-'];policy['control_plane_sha256']=s.control_files(root)
            policy['approval']['review_report_sha256']=hashlib.sha256(report.read_bytes()).hexdigest()
            installed=installer.install(root,Path(folder)/'controller',save())
            self.assertEqual((installed/'scripts/core.py').read_text(),'REVIEWED = True\n')


if __name__=='__main__':unittest.main()
