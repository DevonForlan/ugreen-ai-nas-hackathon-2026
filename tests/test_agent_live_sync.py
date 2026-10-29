"""Read-only incremental detection and bounded publication without model usage."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import agent_live_sync as live
import agent_transcripts as h


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name).resolve()
        self.repo = self.folder/'repo'
        self.repo.mkdir()
        (self.repo/'.git').mkdir()
        self.source = self.folder/'native.jsonl'
        self.sid = 'live-test-session-123'
        self.stamp = '2026-10-29T01:00:00Z'
        self.append(dict(type='session_meta', timestamp='2026-10-25T01:00:00Z',
            payload=dict(id=self.sid, cwd=str(self.repo), timestamp='2026-10-25T01:00:00Z')))
        self.w = live.Watcher(self.source, 'codex', self.repo, self.sid, self.folder/'archive', debounce=3)

    def append(self, row):
        with self.source.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row)+'\n')

    def message(self, role='assistant', text='Harmless visible checkpoint'):
        self.append(dict(type='response_item', timestamp=self.stamp,
                         payload=dict(type='message', role=role, channel='final', content=text)))

    def publish(self):
        with patch.object(live, 'publish', return_value='a'*40) as publish:
            result = self.w.step(10)
            if result:
                self.assertTrue(all(name.endswith('.md') for name in publish.call_args_list[0].args[1]))
                self.assertEqual(publish.call_args_list[1].args[1], ['collaboration/live-sync-status.json'])
            return result, publish.call_count

    def test_appended_assistant_and_multiday_active_attach(self):
        self.message()
        self.w.step(0)
        result, calls = self.publish()
        self.assertEqual(calls, 2)
        self.assertEqual(result['status'], 'SYNC_COMPLETE')
        status = json.loads(self.w.status_path.read_text(encoding='utf-8'))
        self.assertTrue(status['github_remote_verified'])
        self.assertEqual(status['last_visible_event_at'], self.stamp)
        self.assertEqual(status['final_response_captured'], 'unknown')
        self.assertIn('Harmless visible checkpoint', next((self.repo/'collaboration/codex-sessions').glob('*.md')).read_text(encoding='utf-8'))

    def test_appended_user(self):
        self.message('user', 'Visible requirement')
        self.w.step(0)
        self.assertEqual(self.publish()[0]['status'], 'SYNC_COMPLETE')

    def test_stream_coalescence_and_partial_line(self):
        self.message(text='chunk one')
        self.w.step(0)
        self.message(text='chunk two')
        self.assertIsNone(self.w.step(2))
        self.assertIsNone(self.w.step(4))
        result, calls = self.publish()
        self.assertEqual(calls, 2)
        self.assertIsNotNone(result)
        cursor = live.Cursor(self.source, 'codex')
        cursor.poll()
        with self.source.open('a', encoding='utf-8') as f:
            f.write('{"type":')
        self.assertFalse(cursor.poll())
        self.assertEqual(cursor.malformed, 0)

    def test_internal_only_no_commit(self):
        self.append(dict(type='response_item', payload=dict(type='message', role='assistant', channel='analysis', content='PRIVATE THINKING')))
        self.append(dict(type='response_item', payload=dict(type='reasoning', text='PRIVATE THINKING')))
        self.message(text='')
        with patch.object(live, 'publish') as pub:
            self.w.step(0)
            self.w.step(10)
            pub.assert_not_called()

    def test_hidden_excluded_from_export(self):
        self.append(dict(type='response_item', payload=dict(type='message', role='assistant', channel='analysis', content='PRIVATE THINKING')))
        self.message()
        self.w.step(0)
        self.publish()
        text = next((self.repo/'collaboration/codex-sessions').glob('*.md')).read_text(encoding='utf-8')
        self.assertNotIn('PRIVATE THINKING', text)

    def test_restart_idempotence(self):
        self.message()
        self.w.step(0)
        self.publish()
        new = live.Watcher(self.source, 'codex', self.repo, self.sid, self.folder/'archive')
        with patch.object(live, 'publish') as pub:
            new.step(0)
            new.step(10)
            pub.assert_not_called()

    def test_rotation_reopen(self):
        cursor = live.Cursor(self.source, 'codex')
        self.message()
        self.assertTrue(cursor.poll())
        old = self.source.read_bytes()
        self.source.unlink()
        self.source.write_bytes(old)
        # Replacement replays safely; sanitized visible hash suppresses duplicate publication.
        cursor.identity = None
        self.assertTrue(cursor.poll())

    def test_malformed_event_count_no_raw_leak(self):
        with self.source.open('a', encoding='utf-8') as f:
            f.write('not json PRIVATE RAW\n')
        self.message()
        self.w.step(0)
        self.publish()
        self.assertEqual(self.w.cursor.malformed, 1)
        self.assertNotIn('PRIVATE RAW', self.w.status_path.read_text(encoding='utf-8'))

    def test_network_failure_local_only(self):
        self.message()
        self.w.step(0)
        with patch.object(live, 'publish', side_effect=live.SyncError('fixture unavailable')):
            with self.assertRaises(live.SyncError):
                self.w.step(10)
        saved = json.loads(self.w.status_path.read_text(encoding='utf-8'))
        self.assertEqual(saved['github_sync_status'], 'LOCAL_ONLY')
        self.assertFalse(saved['github_remote_verified'])
        self.assertTrue(saved['local_archive_updated'])

    def test_secret_blocking(self):
        path = self.repo/'collaboration/codex-sessions/test.md'
        path.parent.mkdir(parents=True)
        path.write_text('example = '+('gh'+'p_')+'a'*36, encoding='utf-8')
        with self.assertRaises(h.ArtifactScanError):
            live.selected_scan(self.repo, ['collaboration/codex-sessions/test.md'])

    def test_claude_format(self):
        path = self.folder/'claude.jsonl'
        rows = [dict(type='user', sessionId=self.sid, uuid='user-001', cwd=str(self.repo), timestamp=self.stamp,
                     message=dict(role='user', content='requirement')),
                dict(type='assistant', sessionId=self.sid, uuid='reply-001', cwd=str(self.repo), timestamp=self.stamp,
                     message=dict(role='assistant', content=[dict(type='thinking', thinking='PRIVATE'), dict(type='text', text='visible review')]))]
        path.write_text(''.join(json.dumps(row)+'\n' for row in rows), encoding='utf-8')
        w = live.Watcher(path, 'claude', self.repo, self.sid, self.folder/'archive')
        with patch.object(live, 'publish', return_value='b'*40):
            w.step(0)
            self.assertEqual(w.step(10)['status'], 'SYNC_COMPLETE')
        text = next((self.repo/'collaboration/cc-sessions').glob('*.md')).read_text(encoding='utf-8')
        self.assertIn('visible review', text)
        self.assertNotIn('PRIVATE', text)
        rows[-1]['message']['content'][-1]['text'] = 'visible review extended stream'
        with path.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(rows[-1])+'\n')
        with patch.object(live, 'publish', return_value='c'*40):
            w.step(20)
            self.assertEqual(w.step(30)['status'], 'SYNC_COMPLETE')

    def test_cache_retains_only_hashes_and_sanitized_values(self):
        cache = live.SanitizedCache(lambda v: '[REDACTED]', max_bytes=32)
        self.assertEqual(cache('PRIVATE INPUT'), '[REDACTED]')
        self.assertNotIn('PRIVATE INPUT', str(cache.values))
        cache('another value')
        self.assertLessEqual(cache.size, 32)

    def test_tool_result_and_error_detection(self):
        for kind in ('function_call_output','custom_tool_call_output'):
            self.assertTrue(live.visible(dict(type='response_item',payload=dict(type=kind,output='test passed')), 'codex'))
        self.assertTrue(live.visible(dict(type='event_msg',payload=dict(type='error',message='failed')), 'codex'))
        self.assertFalse(live.visible(dict(type='assistant',message=dict(role='assistant',content=None)), 'claude'))

    def test_git_mutation_lock_defers_without_stealing(self):
        self.message()
        self.w.step(0)
        lock = self.repo/'.git/agent-transcript-publish.lock'
        lock.write_text('other explicit owner')
        with patch.object(live, 'publish') as pub:
            self.assertIsNone(self.w.step(10))
            pub.assert_not_called()
        self.assertEqual(lock.read_text(), 'other explicit owner')

    def test_archive_failure_updates_local_failure_receipt(self):
        self.message()
        self.w.step(0)
        with patch.object(h, 'archive', side_effect=ValueError('prefix changed')):
            with self.assertRaises(ValueError):
                self.w.step(10)
        status = json.loads(self.w.status_path.read_text(encoding='utf-8'))
        self.assertEqual(status['github_sync_status'], 'LOCAL_ONLY')
        self.assertFalse(status['github_remote_verified'])

    def test_burst_is_bounded(self):
        self.message()
        self.w.step(0)
        for tick in (2,4,6,8):
            self.message(text='visible burst '+str(tick))
            self.assertIsNone(self.w.step(tick))
        self.message(text='last visible burst')
        with patch.object(live, 'publish', return_value='d'*40) as pub:
            self.assertEqual(self.w.step(10)['status'], 'SYNC_COMPLETE')
            self.assertEqual(pub.call_count, 2)

    def test_secret_failure_blocks_publisher_and_marks_failed(self):
        self.message()
        self.w.step(0)
        with patch.object(live, 'selected_scan', side_effect=h.ArtifactScanError(Path('session.md'), [])), \
                patch.object(live, 'publish') as pub:
            with self.assertRaises(h.ArtifactScanError):
                self.w.step(10)
        pub.assert_not_called()
        saved = json.loads(self.w.status_path.read_text(encoding='utf-8'))
        self.assertEqual(saved['github_sync_status'], 'FAILED')
        self.assertEqual(saved['secret_scan'], 'FAILED')

    def test_owner_exit_no_orphan(self):
        argv = ['live', '--agent', 'codex', '--session-id', self.sid, '--source', str(self.source),
                '--project', str(self.repo), '--owner-pid', '1234']
        with patch.object(sys, 'argv', argv), patch.object(live, 'git', return_value=str(self.repo/'.git')), \
                patch.object(live, 'alive', return_value=False), patch.object(live.Watcher, 'step') as step:
            live.main()
        self.assertEqual(step.call_count, 2)
        self.assertFalse((self.repo/'.git/agent-live-sync.lock').exists())


if __name__ == '__main__':
    unittest.main()
