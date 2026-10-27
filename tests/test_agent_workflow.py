"""No model calls or network. Exercise the complete bounded handoff state machine."""
import copy
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import agent_workflow as w
spec = importlib.util.spec_from_file_location('orchestrator', ROOT / 'scripts/agent-orchestrator.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


def task_body(task='AUTO-T1'):
    values = {key: 'Bounded evidence; no scope expansion.' for key in w.FIELDS}
    values.update({'Task ID': task, 'Maximum Iterations': 'Codex attempts: 3\nCC review rounds: 3'})
    return '\n\n'.join('### ' + k + '\n' + values[k] for k in w.FIELDS)


def review(result='PASS'):
    return {'result': result, 'summary': 'Checked supplied criteria and evidence.',
            'required_changes': ['Fix the failing assertion.'] if result == 'CHANGES_REQUESTED' else [],
            'recommended_next_task': '', 'user_question': 'Which bounded option should be approved?' if result == 'USER_DECISION_REQUIRED' else ''}


class Hub:
    def __init__(self):
        self.item = {'number': 1, 'title': 'AUTO-T1', 'body': task_body(), 'labels': ['READY_FOR_CODEX'],
                     'author': 'owner', 'editor': None, 'open': True}
        self.state, self.version = None, None
        self.comments, self.created = [], []
        self.fail_once = False

    def issue(self, number): return copy.deepcopy(self.item)
    def ledger(self, number): return copy.deepcopy(self.state), self.version

    def save(self, number, state, expected):
        if self.fail_once:
            self.fail_once = False
            raise w.RemoteError('GitHub unavailable')
        if expected != self.version:
            raise w.RemoteError('CAS conflict')
        self.version = str(int(self.version or 0) + 1)
        self.state = copy.deepcopy(state)
        return self.version

    def labels(self, issue, state): self.item['labels'] = [state]
    def comment(self, number, body): self.comments.append(body)
    def artifact(self, path, sha): return '# Codex report\nPublished evidence.'
    def create_issue(self, title, body):
        self.created.append((title, body))
        return {'number': 2}


class Tools:
    def __init__(self):
        self.head = 'a' * 40
        self.tree = {'src/example.py': 'base', 'docs/00_PROJECT_STATUS.md': 'base'}
        self.codex_calls, self.cc_calls = 0, 0
        self.review = review()
        self.codex_error = None
        self.notifications = []
        self.notify_error = False
        self.report = 'collaboration/codex-reports/2026-10-27_0100_AUTO-T1.md'

    def preflight(self, repository): return self.head
    def snapshot(self): return dict(self.tree)
    def notify(self, *args):
        if self.notify_error:
            raise RuntimeError('UI unavailable')
        self.notifications.append(args)

    def codex(self, prompt, timeout):
        self.codex_calls += 1
        if self.codex_error:
            raise self.codex_error
        self.tree.update({'src/example.py': str(self.codex_calls), 'docs/00_PROJECT_STATUS.md': str(self.codex_calls), self.report: str(self.codex_calls)})
        return {'result': 'HANDOFF', 'summary': 'Implemented.', 'report_path': self.report,
                'gate_reason': '', 'user_question': ''}, {'input_tokens': 10, 'output_tokens': 5}

    def tests(self, argv): return [{'command': argv[0], 'exit_code': 0, 'output': 'Tests PASS (mock)'}]
    def finalize(self, task):
        self.head = str(self.codex_calls) * 40
        return {'commit': self.head, 'taskCommit': self.head, 'synced': True}
    def diff(self, base, head): return 'diff --git a/src/example.py b/src/example.py\n+ bounded change'
    def cc(self, prompt, timeout):
        self.cc_calls += 1
        self.last_packet = prompt
        return copy.deepcopy(self.review), 'UNKNOWN'
    def review_report(self, issue, fields, state, value):
        self.head = 'e' * 40
        return 'collaboration/cc-reports/review.md'


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.hub, self.tools = Hub(), Tools()
        self.policy = {'repository': 'owner/repo', 'trusted_authors': [], 'allowed_task_prefixes': ['AUTO-'],
                       'agent_timeout_seconds': 60, 'max_review_bytes': 98304, 'max_steps': 6,
                       'max_codex_attempts': 3, 'max_cc_review_rounds': 3,
                       'plans': {'AUTO-T1': {'issue_number': 1, 'body_sha256': w.digest(self.hub.item['body']),
                                             'codex_enabled': True, 'cc_enabled': True, 'sandbox_acknowledged': True,
                                             'allowed_write_paths': ['src/'], 'required_tests': [['python', '-m', 'unittest']],
                                             'followups': {}}}}
        self.engine = w.Engine(self.hub, self.tools, self.policy)
        scan = patch.object(w.scanner, 'scan_repo', return_value=(1, []))
        scan.start()
        self.addCleanup(scan.stop)

    def step(self): return self.engine.step(self.hub.issue(1))

    def test_every_legal_transition_and_codex_cannot_done(self):
        for edge, actor in w.EDGES.items():
            self.assertEqual(w.transition(*edge, actor), edge[1])
        with self.assertRaises(w.Gate): w.transition('CC_REVIEWING', 'DONE', 'codex')
        with self.assertRaises(w.Gate): w.transition('READY_FOR_CODEX', 'DONE', 'codex')

    def test_illegal_transitions(self):
        for old in w.STATES:
            for new in w.STATES:
                if (old, new) not in w.EDGES:
                    with self.assertRaises(w.Gate): w.transition(old, new, 'codex')

    def test_mandatory_gate_overrides_ordinary_edges(self):
        self.assertEqual(w.transition('CODEX_RUNNING', 'USER_DECISION_REQUIRED', 'controller', True), 'USER_DECISION_REQUIRED')

    def test_codex_handoff_then_independent_cc_pass(self):
        self.assertEqual(self.step(), 'READY_FOR_CC_REVIEW')
        self.assertEqual(self.tools.cc_calls, 0)
        self.assertEqual(self.hub.state['codex_attempts'], 1)
        self.assertIn('head', self.hub.state['handoff'])
        self.assertEqual(self.step(), 'DONE')
        self.assertEqual(self.tools.cc_calls, 1)
        self.assertIn('codex_report', self.tools.last_packet)
        self.assertEqual(self.hub.state['history'][-1]['usage'], 'UNKNOWN')

    def test_changes_requested_reenters_codex_with_fixed_scope(self):
        self.step()
        self.tools.review = review('CHANGES_REQUESTED')
        self.assertEqual(self.step(), 'CHANGES_REQUESTED')
        self.assertEqual(self.hub.state['cc_rounds'], 1)
        self.assertEqual(self.step(), 'READY_FOR_CC_REVIEW')
        self.assertEqual(self.hub.state['codex_attempts'], 2)

    def test_max_attempts_survive_new_engine(self):
        self.step()
        self.hub.state.update(state='CHANGES_REQUESTED', codex_attempts=3)
        self.hub.item['labels'] = ['CHANGES_REQUESTED']
        self.engine = w.Engine(self.hub, self.tools, self.policy)
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertEqual(self.tools.codex_calls, 1)

    def test_third_unsuccessful_review_requires_user(self):
        self.step()
        self.hub.state.update(codex_attempts=3, cc_rounds=2)
        self.tools.review = review('CHANGES_REQUESTED')
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertEqual(self.hub.state['cc_rounds'], 3)

    def test_cc_user_question_is_preserved(self):
        self.step()
        self.tools.review = review('USER_DECISION_REQUIRED')
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertIn('Which bounded option', self.hub.state['decision']['question'])
        self.assertTrue(self.hub.state['decision']['options'])

    def test_fatal_error_failed_no_false_handoff(self):
        self.tools.codex_error = RuntimeError('fatal mock')
        with self.assertRaises(RuntimeError): self.step()
        self.assertEqual(self.hub.state['state'], 'FAILED')
        self.assertNotIn('handoff', self.hub.state)

    def test_github_failure_stops_before_agent(self):
        self.hub.fail_once = True
        with self.assertRaises(w.RemoteError): self.step()
        self.assertEqual(self.tools.codex_calls, 0)
        self.assertEqual(self.hub.state['state'], 'FAILED')

    def test_malformed_reviewer_json_is_user_gate(self):
        self.step()
        self.tools.review = '{not valid JSON'
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')

    def test_contradictory_pass_rejected(self):
        v = review()
        v['required_changes'] = ['Unresolved blocker']
        with self.assertRaises(w.Gate): w.review_json(v)
        v = review()
        v['user_question'] = 'Unresolved scope decision'
        with self.assertRaises(w.Gate): w.review_json(v)

    def test_notification_fallback_does_not_change_result(self):
        self.tools.notify_error = True
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.step(), 'READY_FOR_CC_REVIEW')
        self.assertIn('Notification fallback', output.getvalue())

    def test_unauthorized_author_and_editor_rejected(self):
        for field in ('author', 'editor'):
            self.hub.item[field] = 'external-contributor'
            with self.assertRaises(w.Gate): self.step()
            self.hub.item[field] = 'owner'
        self.assertEqual(self.tools.codex_calls, 0)
        self.assertFalse(self.hub.comments)

    def test_requirement_mutation_and_dual_labels_rejected(self):
        self.step()
        self.hub.item['body'] += '\nUnapproved scope expansion.'
        with self.assertRaises(w.Gate): self.step()
        self.hub.item['body'] = task_body()
        self.hub.item['labels'] = ['READY_FOR_CC_REVIEW', 'DONE']
        with self.assertRaises(w.Gate): self.step()

    def test_missing_owner_plan_gates_without_model(self):
        self.policy['plans'] = {}
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertEqual(self.tools.codex_calls, 0)

    def test_unapproved_followup_cannot_expand_scope(self):
        self.step()
        self.tools.review['recommended_next_task'] = 'Build a new product'
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertFalse(self.hub.created)

    def test_only_preapproved_followup_is_created_and_not_executed(self):
        self.policy['plans']['AUTO-T1']['followups']['AUTO-T2'] = {'title': 'Approved next check', 'body': task_body('AUTO-T2')}
        self.step()
        self.tools.review['recommended_next_task'] = 'AUTO-T2'
        self.assertEqual(self.step(), 'DONE')
        self.assertEqual(len(self.hub.created), 1)
        self.assertEqual(self.tools.codex_calls, 1)

    def test_controlplane_and_out_of_scope_changes_gate(self):
        for path in ('scripts/agent_workflow.py', 'outside.txt', '../outside'):
            with self.assertRaises(w.Gate): w.allowed_changes({path}, self.policy['plans']['AUTO-T1'], 'AUTO-T1')

    def test_dry_run_never_calls_agent_or_mutates(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rows = cli.preview(self.hub, self.policy, [self.hub.issue(1)])
        self.assertEqual(rows[0]['next_state'], 'CODEX_RUNNING')
        self.assertTrue(json.loads(output.getvalue())['dry_run'])
        self.assertIsNone(self.hub.state)
        self.assertEqual(self.tools.codex_calls + self.tools.cc_calls, 0)

    def test_scope_prefix_blocks_competition_tasks(self):
        self.hub.item['body'] = task_body('R01')
        with self.assertRaises(w.Gate): self.step()

    def test_user_stop_during_codex_cannot_be_overwritten_by_handoff(self):
        original = self.tools.codex
        def stopped(prompt, timeout):
            result = original(prompt, timeout)
            self.hub.item['labels'] = ['USER_DECISION_REQUIRED']
            return result
        self.tools.codex = stopped
        self.assertEqual(self.step(), 'USER_DECISION_REQUIRED')
        self.assertNotIn('handoff', self.hub.state)

    def test_dry_run_respects_other_issue_global_stop(self):
        stopped = dict(self.hub.issue(1), number=2, labels=['USER_DECISION_REQUIRED'])
        with contextlib.redirect_stdout(io.StringIO()):
            rows = cli.preview(self.hub, self.policy, [self.hub.issue(1)], inventory=[self.hub.issue(1), stopped])
        self.assertEqual(rows[0]['intended_action'], 'GLOBAL_STOP')

    def test_codex_uses_exec_schema_sandbox_and_does_not_export_raw_events(self):
        def fake_command(argv, **kwargs):
            Path(argv[argv.index('--output-last-message') + 1]).write_text(json.dumps({'result': 'HANDOFF'}), encoding='utf-8')
            return '{"type":"private_runtime","value":"opaque_fixture"}\n{"type":"turn.completed","usage":{"input_tokens":5}}\n'
        native = type('Native', (), {'native_codex': staticmethod(lambda: 'codex.exe')})
        tools = w.LiveTools()
        with patch.object(w, 'load_module', return_value=native), patch.object(w, 'command', side_effect=fake_command) as run:
            value, usage = tools.codex('bounded fixture', 30)
        argv = run.call_args.args[0]
        self.assertIn('exec', argv)
        self.assertIn('--no-daemon', argv)
        self.assertEqual(argv[argv.index('--sandbox') + 1], 'workspace-write')
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox', argv)
        self.assertTrue(run.call_args.kwargs['isolate_env'])
        self.assertEqual(usage, {'input_tokens': 5})
        self.assertNotIn('opaque_fixture', json.dumps(value))

    def test_cc_uses_toolless_isolated_json_print_mode(self):
        tools = w.LiveTools()
        with patch.object(w.shutil, 'which', return_value='claude.exe'), patch.object(w, 'command', return_value=json.dumps({'structured_output': review()})) as run:
            value, _ = tools.cc('bounded fixture', 30)
        argv = run.call_args.args[0]
        self.assertIn('-p', argv)
        self.assertIn('--safe-mode', argv)
        self.assertIn('--restricted', argv)
        self.assertEqual(argv[argv.index('--tools') + 1], '')
        self.assertIn('--strict-mcp-config', argv)
        self.assertIn('--no-session-persistence', argv)
        self.assertNotEqual(run.call_args.kwargs['cwd'], w.ROOT)
        self.assertTrue(run.call_args.kwargs['isolate_env'])
        self.assertEqual(value['result'], 'PASS')

    def test_model_subprocess_does_not_inherit_gh_credential_environment(self):
        key = 'GH_' + 'TOKEN'
        process = type('P', (), {'returncode': 0, 'communicate': lambda self, *a, **k: ('safe', '')})()
        with patch.dict(w.os.environ, {key: 'fixture-value'}), patch.object(w.subprocess, 'Popen', return_value=process) as launch:
            self.assertEqual(w.command(['fixture'], isolate_env=True), 'safe')
        self.assertNotIn(key, launch.call_args.kwargs['env'])
        self.assertEqual(launch.call_args.kwargs['env']['CODEX_AGENT_WORKFLOW'], '1')

    def test_npm_native_claude_entry_is_resolved_from_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / 'node_modules/@anthropic-ai/claude-code'
            (package / 'bin').mkdir(parents=True)
            (package / 'bin/claude.exe').write_text('not executed', encoding='utf-8')
            (package / 'package.json').write_text(json.dumps({'bin': {'claude': 'bin/claude.exe'}}), encoding='utf-8')
            with patch.object(w.shutil, 'which', return_value=str(root / 'claude.cmd')):
                self.assertEqual(w.claude_launcher(), [str(package / 'bin/claude.exe')])

    def test_review_packet_is_bounded_without_truncating_evidence(self):
        with self.assertRaises(w.Gate):
            w.review_prompt({}, 'report', 'x' * 2000, [], 1024)


class LockTests(unittest.TestCase):
    def test_local_lock_is_exclusive_without_time_guessing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'lock'
            with w.local_lock(path):
                with self.assertRaises(w.Locked):
                    with w.local_lock(path): pass
            self.assertFalse(path.exists())

    def test_remote_ref_lock_second_acquisition_cannot_steal(self):
        class Hub(w.GitHub):
            def __init__(self):
                super().__init__('owner/repo')
                self.refs, self.count = {}, 0
            def head(self): return 'a' * 40
            def api(self, path, method='GET', payload=None, missing=False):
                if '/git/commits/' in path: return {'tree': {'sha': 'b' * 40}}
                if path.endswith('/git/commits'):
                    self.count += 1
                    return {'sha': str(self.count) * 40}
                if path.endswith('/git/refs') and method == 'POST':
                    ref = payload['ref'][5:]
                    if ref in self.refs: raise w.RemoteError('exists')
                    self.refs[ref] = payload['sha']
                elif method == 'DELETE': del self.refs[path.split('/git/refs/')[1]]
                else: return {'object': {'sha': self.refs[path.split('/git/ref/')[1]]}}
        hub = Hub()
        with hub.lock(1):
            with self.assertRaises(w.Locked):
                with hub.lock(1): pass
            self.assertEqual(len(hub.refs), 2)
        self.assertFalse(hub.refs)


if __name__ == '__main__':
    unittest.main()
