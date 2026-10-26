"""Security and isolation regression tests. All credentials are synthetic."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('exporter', Path(__file__).resolve().parents[1] / 'scripts/export-codex-session.py')
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)


class ExportTests(unittest.TestCase):
    def test_secret_classes(self):
        values = [
            'OPENAI_API_KEY' + '=' + '"synthetic value with spaces"',
            'GITHUB_TOKEN' + '=' + 'synthetic_github', 'AWS_SECRET_ACCESS_KEY' + '=' + 'synthetic_aws',
            'AWS_SESSION_TOKEN' + '=' + 'synthetic_session', 'password' + ': ' + 'synthetic_password',
            'Authorization' + ': ' + 'Bearer' + ' synthetic_auth', 'Cookie' + ': ' + 'session=synthetic_cookie',
            'oauth_token' + '=' + 'synthetic_oauth', 'Bearer' + ' synthetic_bearer',
            'postgres://' + 'synthetic_user' + ':' + 'synthetic_pass@localhost/db',
            'Server=local;User ID' + '=' + 'synthetic_sql_user;Password' + '=' + 'synthetic_sql_pass;',
            '-' * 5 + 'BEGIN ' + 'PRIVATE KEY' + '-' * 5 + '\nsynthetic_private\n' + '-' * 5 + 'END PRIVATE KEY' + '-' * 5,
            'sk-' + 'x' * 32, 'ghp_' + 'y' * 36, 'AKIA' + 'Z' * 16,
        ]
        for value in values:
            with self.subTest(value=value):
                clean = ex.sanitize(value)
                self.assertNotIn('synthetic_', clean)
                self.assertNotIn('synthetic value', clean)
                self.assertIn(ex.REDACTED, clean)
                self.assertEqual(ex.sanitize(clean), clean)

    def test_nested_json(self):
        value = json.dumps(dict(zip(['password', 'reasoning', 'cmd'], ['synthetic nested secret', 'PRIVATE_REASONING', 'echo okay'])))
        clean = ex.printable(value)
        self.assertNotIn('synthetic nested secret', clean)
        self.assertNotIn('PRIVATE_REASONING', clean)
        self.assertIn('echo okay', clean)

    def test_export_isolation_idempotence_and_ownership(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            project = root / 'repo'
            project.mkdir()
            (project / '.git').mkdir()
            other = root / 'other'
            other.mkdir()
            (other / '.git').mkdir()
            output = project / 'collaboration/codex-sessions'
            output.mkdir(parents=True)
            source = root / 'session.jsonl'
            def event(kind, payload):
                return {'timestamp': '2026-10-25T13:37:20Z', 'type': kind, 'payload': payload}
            events = [event('session_meta', {'id': 'test-session-1234', 'cwd': str(project), 'timestamp': '2026-10-25T13:37:20Z', 'base_instructions': 'PRIVATE_SYSTEM'}),
                      event('response_item', {'type': 'message', 'role': 'system', 'content': [{'type': 'input_text', 'text': 'PRIVATE_SYSTEM'}]}),
                      event('response_item', {'type': 'reasoning', 'summary': 'PRIVATE_REASONING'}),
                      event('response_item', {'type': 'message', 'role': 'assistant', 'channel': 'analysis', 'content': [{'type': 'output_text', 'text': 'PRIVATE_ANALYSIS'}]}),
                      event('response_item', {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'Visible task'}]}),
                      event('response_item', {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'Visible answer'}]}),
                      event('response_item', {'type': 'function_call', 'name': 'exec', 'arguments': '{"cmd":"python -m unittest"}'}),
                      event('response_item', {'type': 'function_call_output', 'output': 'Tests passed\npassword' + '=' + 'synthetic_password\n```'}),
                      event('event_msg', {'type': 'error', 'message': 'Visible failure'})]
            def write():
                source.write_text('\n'.join(json.dumps(e) for e in events) + '\n', encoding='utf-8')
            def stats():
                return dict(malformed_lines=0, written=0, unchanged=0, unidentified=0, other_or_mixed_project=0)
            write()
            s = stats()
            ex.export_one(source, project, output, s)
            self.assertEqual(s['written'], 1)
            target = next(output.glob('*.md'))
            content = target.read_text(encoding='utf-8')
            for text in ('PRIVATE_SYSTEM', 'PRIVATE_REASONING', 'PRIVATE_ANALYSIS', 'synthetic_password'):
                self.assertNotIn(text, content)
            for text in ('Visible task', 'Visible answer', 'Tests passed', 'Visible failure', 'python -m unittest'):
                self.assertIn(text, content)
            for heading in ('User Messages', 'Codex Visible Responses', 'Tool / Command Calls', 'Tool / Command Results', 'Errors', 'Tests'):
                self.assertIn('## ' + heading + '\n', content)
            before = target.stat().st_mtime_ns
            ex.export_one(source, project, output, s)
            self.assertEqual(s['unchanged'], 1)
            self.assertEqual(before, target.stat().st_mtime_ns)
            events.append(event('turn_context', {'cwd': str(other)}))
            write()
            ex.export_one(source, project, output, s)
            self.assertEqual(s['other_or_mixed_project'], 1)
            self.assertEqual(target.read_text(encoding='utf-8'), content)
            events.pop()
            write()
            target.write_text('Other project record', encoding='utf-8')
            with self.assertRaises(ValueError):
                ex.export_one(source, project, output, s)
            self.assertEqual(target.read_text(encoding='utf-8'), 'Other project record')


if __name__ == '__main__':
    unittest.main()
