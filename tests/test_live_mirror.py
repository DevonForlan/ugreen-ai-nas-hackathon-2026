"""Compact mirrors preserve all allowed content and never fabricate a visible turn."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import agent_live_mirror as m
import agent_transcripts as h


class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        self.transcript=self.root/'collaboration/codex-sessions/fixture.md'
        self.transcript.parent.mkdir(parents=True)
        self.session=h.empty('codex','mirror-session-123',str(self.root),'2026-10-30T00:00:00Z')

    def add(self,kind,text,eid,stamp='2026-10-30T01:00:00Z'):
        h.add(self.session,kind,text,stamp,eid)
        h.finish(self.session)

    def test_baseline_and_verified_metadata_idempotence(self):
        self.add('user','private user answer','user-001')
        self.add('tool_call','run harmless test','call-001')
        self.add('tool_result','test passed','result-001')
        self.add('assistant','new visible response','reply-001')
        bundle=m.prepare(self.root,self.session,self.transcript)
        m.update(bundle,'a'*40,True)
        text=(self.root/'collaboration/live-latest/codex.md').read_text(encoding='utf-8')
        self.assertIn('new visible response',text)
        self.assertIn('test passed',text)
        self.assertNotIn('private user answer',text)
        self.assertIn('a'*40,text)
        self.assertTrue(m.available(self.root,'codex',self.session['session_id']))
        self.assertIsNone(m.prepare(self.root,self.session,self.transcript))

    def test_no_turn_for_tool_only(self):
        self.add('tool_result','not yet a completed assistant reply','tool-001')
        self.assertIsNone(m.prepare(self.root,self.session,self.transcript))

    def test_burst_every_new_response_gets_a_turn(self):
        self.add('assistant','baseline','a')
        b=m.prepare(self.root,self.session,self.transcript);m.update(b,'a'*40,True)
        self.add('assistant','second','b')
        self.add('assistant','third','c')
        b=m.prepare(self.root,self.session,self.transcript)
        self.assertEqual(len(b['records']),2)
        self.assertIn('third',(self.root/'collaboration/live-latest/codex.md').read_text())

    def test_large_tools_bounded_latest_complete_parts(self):
        text='harmless visible log\n'*14000
        self.add('tool_result',text,'tool')
        self.add('assistant','compact conclusion','reply')
        b=m.prepare(self.root,self.session,self.transcript)
        latest=self.root/'collaboration/live-latest/codex.md'
        self.assertLess(latest.stat().st_size,32768)
        self.assertGreater(b['records'][0][0]['part_count'],1)
        chunks=[self.root/n for n in b['names'] if '/part-' in n]
        header='# Visible response content part\n\n'
        restored=''.join(p.read_text(encoding='utf-8')[len(header):-1] for p in chunks)
        self.assertEqual(restored.count('harmless visible log'),14000)

    def test_secret_otp_mfa_redaction(self):
        self.add('assistant','OTP: 123456\nMFA: "123456"\nverification code is 123456\n'+('gh'+'p_')+'x'*36,'reply')
        b=m.prepare(self.root,self.session,self.transcript)
        for name in b['paths']:
            text=(self.root/name).read_text(encoding='utf-8')
            self.assertNotIn('123456',text)
            self.assertNotIn(('gh'+'p_')+'x'*36,text)

    def test_unicode_latest_is_byte_bounded(self):
        self.add('assistant','\u53ef\u898b\u56de\u61c9'*10000,'reply')
        m.prepare(self.root,self.session,self.transcript)
        self.assertLess((self.root/'collaboration/live-latest/codex.md').stat().st_size,32768)

    def test_failed_publication_not_certified(self):
        self.add('assistant','visible','reply')
        b=m.prepare(self.root,self.session,self.transcript)
        m.update(b,None,False,'SyncError')
        self.assertFalse(m.available(self.root,'codex',self.session['session_id']))
        self.assertEqual(m.load_index(self.root)['agents']['codex']['status'],'FAILED')
        self.assertIsNotNone(m.prepare(self.root,self.session,self.transcript))

    def test_claude_separate_pointer(self):
        self.session['agent']='claude'
        self.add('assistant','independent Claude response','uuid-block-001')
        m.prepare(self.root,self.session,self.transcript)
        self.assertTrue((self.root/'collaboration/live-latest/claude.md').exists())
        self.assertFalse((self.root/'collaboration/live-latest/codex.md').exists())

    def test_older_session_cannot_replace_newer_pointer(self):
        self.add('assistant','newer','reply-new','2026-10-30T02:00:00Z')
        b=m.prepare(self.root,self.session,self.transcript);m.update(b,'a'*40,True)
        self.session=h.empty('codex','older-session-123',str(self.root),'2026-10-29T00:00:00Z')
        self.add('assistant','older','reply-old','2026-10-29T01:00:00Z')
        b=m.prepare(self.root,self.session,self.transcript);m.update(b,'b'*40,True)
        self.assertIn('newer',(self.root/'collaboration/live-latest/codex.md').read_text())


if __name__=='__main__':unittest.main()
