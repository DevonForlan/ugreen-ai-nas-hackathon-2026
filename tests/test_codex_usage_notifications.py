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

    def parse(self, **windows):
        return usage.quota_percentages({'rateLimits': windows})

    def test_five_and_six_hour_windows_are_dynamic(self):
        for minutes,label in ((300,'5H'),(360,'6H'),(330,'5H30M'),(45,'45M'),(90,'1H30M')):
            row=self.parse(primary=self.window(minutes))[0]
            self.assertEqual(row['name'],label)
            self.assertEqual(row['remainingPercent'],82)
            self.assertIn('100 - native usedPercent',row['percentageSource'])

    def test_unknown_duration_does_not_hide_actual_percentage(self):
        row=self.parse(primary={'usedPercent':21})[0]
        self.assertEqual(row['name'],'Window UNKNOWN')
        self.assertEqual(row['remainingPercent'],79)
        self.assertIsNone(row['resetAtLocal'])

    def test_timezone_and_weekly_reset(self):
        stamp=usage.local_timestamp('2026-10-28T06:00:00Z')
        self.assertEqual(stamp,'2026-10-28 14:00:00 +08:00')
        self.assertEqual(usage.local_timestamp(1793167200),stamp)
        rows=self.parse(primary=dict(usedPercent=21,windowDurationMins=10080,resetsAt='2026-11-02T00:00:00Z'))
        self.assertEqual(rows[0]['name'],'Weekly (168H)')
        self.assertEqual(rows[0]['resetAtLocal'],'2026-11-02 08:00:00 +08:00')
        self.assertIsNone(usage.local_timestamp('2026-10-28T06:00:00'))

    def test_remaining_and_used_semantics(self):
        direct=self.parse(primary={'remainingPercent':30})[0]
        self.assertEqual(direct['remainingPercent'],30)
        self.assertEqual(direct['percentageSource'],'native remainingPercent')
        conflict=self.parse(primary={'remainingPercent':30,'usedPercent':20})[0]
        self.assertIsNone(conflict['remainingPercent'])
        for used in (True,-1,101,float('nan'),'18'):
            self.assertIsNone(self.parse(primary=self.window(360,used))[0]['remainingPercent'])

    def test_missing_reset_does_not_invalidate_percentage(self):
        row=self.parse(primary={'windowDurationMins':360,'usedPercent':21})[0]
        self.assertEqual(row['remainingPercent'],79)
        self.assertIn('Reset: UNKNOWN',usage.footer([row],10))

    def test_multiple_buckets_do_not_guess_entitlement(self):
        self.assertEqual(usage.quota_percentages({'rateLimitsByLimitId':{'other':{'primary':self.window(300)}}}),[])

    def test_native_unavailable_and_footer_updated_time(self):
        text=usage.footer(usage.quota_percentages(None),999)
        self.assertIn('Window UNKNOWN',text)
        self.assertNotIn('5H',text)
        self.assertIn('Updated: UNKNOWN',text)
        row=self.parse(primary=self.window(360))[0]
        self.assertIn('Updated: 2026-10-28 14:00:00 +08:00',usage.footer([row],999,'2026-10-28 14:00:00 +08:00'))
        self.assertIn('Session 999 tokens',text)

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
