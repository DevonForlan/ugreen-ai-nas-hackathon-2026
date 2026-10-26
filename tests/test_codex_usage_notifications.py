"""Fast deterministic checks: quota provenance, UNKNOWN fallback, safe notifications."""
import importlib.util
import io
import json
from pathlib import Path
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


usage = load('usage', 'codex-usage.py')
notification = load('notification', 'codex-notification.py')
finalizer = load('finalizer', 'finalize-codex-task.py')


class UsageTests(unittest.TestCase):
    def window(self, minutes, used=18):
        return {'usedPercent': used, 'windowDurationMins': minutes, 'resetsAt': int(time.time()) + 3600}

    def test_quota_uses_actual_window_not_primary_position(self):
        v = {'rateLimits': {'limitId': 'codex', 'primary': self.window(10080, 9), 'secondary': self.window(300)}}
        self.assertEqual(usage.quota_percentages(v), {'5H': 82, 'Weekly': 91})
        v['rateLimits']['secondary'] = None
        self.assertEqual(usage.quota_percentages(v), {'5H': None, 'Weekly': 91})

    def test_unknown_and_invalid_quota_never_inferred(self):
        self.assertEqual(usage.quota_percentages(None), {'5H': None, 'Weekly': None})
        for used in (True, -1, 101, float('nan'), '18'):
            v = {'rateLimits': {'primary': self.window(300, used)}}
            self.assertIsNone(usage.quota_percentages(v)['5H'])
        v = {'rateLimits': {'primary': self.window(60)}}
        self.assertIsNone(usage.quota_percentages(v)['5H'])
        self.assertIn('5H UNKNOWN | Weekly UNKNOWN', usage.footer(usage.quota_percentages(None), 99999999))

    def test_multiple_buckets_do_not_guess_entitlement(self):
        v = {'rateLimitsByLimitId': {'other': {'primary': self.window(300)}}}
        self.assertIsNone(usage.quota_percentages(v)['5H'])

    def test_session_is_not_global_totals(self):
        sid = 'session-12345678'
        v = {'totals': {'totalTokens': 999999}, 'sessions': [{'sessionId': 'path/' + sid, 'totalTokens': 1234}]}
        self.assertEqual(usage.session_tokens(v, sid), 1234)
        self.assertIsNone(usage.session_tokens(v, 'other-session'))
        v['sessions'].append(dict(v['sessions'][0]))
        self.assertIsNone(usage.session_tokens(v, sid))

    def test_rpc_is_bounded_and_child_is_closed(self):
        class SavedIO(io.StringIO):
            def close(self):
                self.saved = self.getvalue()
                super().close()
        class Process:
            def __init__(self, output):
                self.stdin = SavedIO()
                self.stdout = io.StringIO(output)
                self.terminated = False
            def poll(self): return 0 if self.terminated else None
            def terminate(self): self.terminated = True
            def wait(self, timeout): return 0
        p = Process('{"id":1,"result":{}}\n{"id":2,"result":{"rateLimits":{}}}\n')
        with patch.object(usage, 'native_codex', return_value='native-codex'), patch.object(usage.subprocess, 'Popen', return_value=p) as launch:
            self.assertEqual(usage.quota_snapshot(.1), {'rateLimits': {}})
        methods = [json.loads(line)['method'] for line in p.stdin.saved.splitlines()]
        self.assertEqual(methods, ['initialize', 'initialized', 'account/rateLimits/read'])
        self.assertIn('--no-daemon', launch.call_args.args[0])
        self.assertTrue(p.terminated)
        p = Process('')
        with patch.object(usage, 'native_codex', return_value='native-codex'), patch.object(usage.subprocess, 'Popen', return_value=p):
            self.assertIsNone(usage.quota_snapshot(.01))
        self.assertTrue(p.terminated)


class NotificationTests(unittest.TestCase):
    def test_status_sound_mapping(self):
        for status, sound in {'SUCCESS': 'Asterisk', 'WARNING': 'Exclamation', 'FAILED': 'Hand'}.items():
            self.assertEqual(notification.prepare(status, 'Title', 'Message')['sound'], sound)
        with self.assertRaises(ValueError):
            notification.prepare('INVALID', 'Title', 'Message')

    def test_payload_is_sanitized_bounded_and_xml_escaped(self):
        value = 'ghp_' + 'X' * 36
        payload = notification.prepare('SUCCESS', 'A < B', 'token' + '=' + value + ' ' + 'x' * 300)
        self.assertNotIn(value, json.dumps(payload))
        self.assertIn('&lt;', payload['xml'])
        self.assertLessEqual(len(payload['message']), 240)
        self.assertIn('silent="true"', payload['xml'])

    def test_sync_failure_is_warning_security_failure_is_failed(self):
        self.assertEqual(finalizer.failure_status('PUSH', True, RuntimeError()), 'WARNING')
        self.assertEqual(finalizer.failure_status('PUSH', True, finalizer.SecurityScanError()), 'FAILED')
        self.assertEqual(finalizer.failure_status('VALIDATE', False, RuntimeError()), 'FAILED')
