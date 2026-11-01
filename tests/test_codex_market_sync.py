"""Full visible-history fidelity, identity, redaction and partition checks."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import codex_market_sync as m


class MarketHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        (self.root / '.git').mkdir()
        self.source = Path(self.temp.name) / 'native.jsonl'
        self.sid = 'market-test-session-123'
        self.rows = [dict(type='session_meta', payload=dict(id=self.sid, cwd=str(self.root), timestamp='2026-11-01T00:00:00Z'))]

    def add(self, role, text, channel=None):
        self.rows.append(dict(type='response_item', timestamp='2026-11-01T00:00:01Z', payload=dict(
            type='message', role=role, channel=channel, content=[dict(type='text', text=text)])))

    def save(self):
        self.source.write_text(''.join(json.dumps(r) + '\n' for r in self.rows), encoding='utf-8')

    def export(self):
        self.save()
        return m.export(self.source, self.sid, self.root)

    def test_long_prompts_responses_tools_and_hidden_exclusion(self):
        prompt = '\u4fdd\u7559' * 20000
        response = 'complete response ' * 5000
        self.add('user', prompt)
        self.add('assistant', 'MUST_NOT_EXPORT', 'analysis')
        self.add('developer', 'PRIVATE_DEVELOPER')
        self.rows.append(dict(type='response_item', payload=dict(type='reasoning', text='PRIVATE_REASONING')))
        self.rows.append(dict(type='response_item', payload=dict(type='function_call', name='example', arguments='COMPLETE_ARGS' * 2000)))
        self.rows.append(dict(type='response_item', payload=dict(type='function_call_output', output='COMPLETE_RESULT' * 2000)))
        self.add('assistant', response, 'final')
        manifest, _ = self.export()
        text = (self.root / manifest['transcript']['path']).read_text(encoding='utf-8')
        self.assertIn(prompt, text)
        self.assertIn(response, text)
        self.assertIn('COMPLETE_ARGS' * 2000, text)
        self.assertIn('COMPLETE_RESULT' * 2000, text)
        self.assertNotIn('MUST_NOT_EXPORT', text)
        self.assertNotIn('PRIVATE_DEVELOPER', text)
        self.assertNotIn('PRIVATE_REASONING', text)
        latest = (self.root / 'collaboration/live-latest/codex-market.md').read_text(encoding='utf-8')
        self.assertIn(response, latest)
        self.assertEqual(manifest['visible_event_count'], 4)
        self.assertEqual(manifest['final_response_captured'], 'unknown')

    def test_value_redaction_preserves_context_and_is_scannable(self):
        samples = ['pass' + 'word' + ': ' + 'sensitive-value', 'device code' + ': ' + 'ABCD-1234',
                   'OTP' + ': ' + '123456', 'api_' + 'key' + '=' + 'sk-' + 'a' * 30,
                   'Author' + 'ization' + ': ' + 'Bear' + 'er ' + 'b' * 30]
        for text in samples:
            cleaned = m.sanitize('before\n' + text + '\nafter')
            self.assertIn(m.REDACTED, cleaned)
            self.assertIn('before', cleaned)
            self.assertIn('after', cleaned)
            self.assertEqual(m.h.scan.scan_text(cleaned), [])

    def test_parts_reconstruct_exact_utf8(self):
        text = ('\u4fdd\u7559\U0001f600' * 2000) + '\nlast'
        files = {}
        info = m.put_document(self.root, 'doc.md', text, lambda i: f'parts/part-{i:04d}.md', files, size=777)
        rebuilt = ''.join((self.root / n).read_text(encoding='utf-8') for n in info['parts'])
        self.assertEqual(rebuilt, text)
        self.assertEqual(m.digest(rebuilt), info['sha256'])
        for name in info['parts']:
            self.assertIn(name, (self.root / 'doc.md').read_text(encoding='utf-8'))

    def test_append_identity_and_no_legacy_writes(self):
        legacy = self.root / 'collaboration/live-latest/codex.md'
        legacy.parent.mkdir(parents=True)
        legacy.write_text('OLD CODEX UNCHANGED', encoding='utf-8')
        self.add('user', 'first')
        self.add('assistant', 'first reply')
        manifest, _ = self.export()
        old_hashes = manifest['event_hashes']
        self.add('user', 'next')
        self.add('assistant', 'next reply')
        manifest, _ = self.export()
        self.assertEqual(manifest['event_hashes'][:len(old_hashes)], old_hashes)
        self.assertEqual(manifest['turn_count'], 2)
        self.assertEqual(legacy.read_text(encoding='utf-8'), 'OLD CODEX UNCHANGED')
        self.rows[1]['payload']['content'][0]['text'] = 'tampered'
        with self.assertRaises(ValueError):
            self.export()

    def test_mixed_owner_and_partial_tail(self):
        self.add('user', 'prompt')
        self.save()
        with self.source.open('ab') as f:
            f.write(b'{"partial":')
        data = m.native(self.source, self.sid, self.root)
        self.assertFalse(data['source_complete'])
        self.assertEqual(len(data['events']), 1)
        self.rows[0]['payload']['id'] = 'different-session-123'
        self.save()
        with self.assertRaises(ValueError):
            m.native(self.source, self.sid, self.root)

    def test_manifest_identity_cannot_be_reassigned(self):
        self.add('user', 'prompt')
        manifest, _ = self.export()
        path = self.root / f'collaboration/codex-market-sessions/{self.sid}/manifest.json'
        manifest['project_sha256'] = 'different-project'
        path.write_text(json.dumps(manifest), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.export()


if __name__ == '__main__':
    unittest.main()
