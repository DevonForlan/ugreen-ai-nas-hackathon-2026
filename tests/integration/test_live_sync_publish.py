"""Real disposable Git pushes; URL policy only is substituted for the local bare remote."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'scripts'))
import agent_live_sync as live


class LiveGitTests(unittest.TestCase):
    def test_real_companion_exits_after_owner_process(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            subprocess.run(['git','init',str(root)],capture_output=True,check=True)
            source = root.parent/(root.name+'-source.jsonl')
            try:
                source.write_text(json.dumps(dict(type='session_meta',payload=dict(
                    id='owner-exit-test-123',cwd=str(root),timestamp='2026-10-29T00:00:00Z')))+'\n',encoding='utf-8')
                owner = subprocess.Popen([sys.executable,'-c','import time; time.sleep(1)'])
                child = subprocess.Popen([sys.executable,str(Path(live.__file__).resolve()),
                    '--agent','codex','--session-id','owner-exit-test-123','--source',str(source),
                    '--project',str(root),'--owner-pid',str(owner.pid),'--max-runtime','10'],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                owner.wait(timeout=5)
                stdout, stderr = child.communicate(timeout=10)
                self.assertEqual(child.returncode,0,stderr.decode(errors='replace'))
                self.assertFalse(list((root/'.git').glob('agent-live-sync-*.lock')))
            finally:
                source.unlink(missing_ok=True)

    def test_real_push_verify_isolation_divergence_and_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            repo = base/'repo'
            repo.mkdir()
            remote = base/'remote.git'
            def git(*args):
                return subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True).stdout.decode().strip()
            git('init', '-b', 'main')
            git('config', 'user.name', 'Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            (repo/'code.txt').write_text('baseline')
            git('add', '.')
            git('commit', '-m', 'baseline')
            subprocess.run(['git', 'init', '--bare', str(remote)], capture_output=True, check=True)
            git('remote', 'add', 'origin', str(remote))
            git('push', '-u', 'origin', 'main')
            (repo/'code.txt').write_text('Unrelated developer edit')
            path = repo/'collaboration/codex-sessions/fixture.md'
            path.parent.mkdir(parents=True)
            path.write_text('Visible sanitized reply\n', encoding='utf-8')
            name = path.relative_to(repo).as_posix()
            original = live.git
            def local(root, *args):
                if args[:2] == ('remote', 'get-url'):
                    return 'https://github.com/fixture/repo.git'
                return original(root, *args)
            with patch.object(live, 'git', side_effect=local):
                commit = live.publish(repo, [name], 'logs: fixture snapshot')
                self.assertEqual(commit, git('ls-remote', 'origin', 'refs/heads/main').split()[0])
                self.assertEqual(git('show', commit+':code.txt'), 'baseline')
                self.assertEqual((repo/'code.txt').read_text(), 'Unrelated developer edit')
                self.assertEqual(git('diff', '--cached', '--name-only'), '')
                # Existing user staging is never overwritten.
                git('add', 'code.txt')
                with self.assertRaises(live.SyncError):
                    live.publish(repo, [name], 'must stop')
                git('reset', '-q', 'HEAD', '--', 'code.txt')
                # Local-only/unpublished commit: refuse to carry it into an automatic push.
                git('add', 'code.txt')
                git('commit', '-m', 'unpublished developer commit')
                with self.assertRaises(live.SyncError):
                    live.publish(repo, [name], 'must not push unrelated history')
                self.assertEqual(commit, git('ls-remote', 'origin', 'refs/heads/main').split()[0])
                # Divergent remote also stops; never force.
                git('push', 'origin', 'main')
                git('update-ref', 'refs/heads/main', commit)
                with self.assertRaises(live.SyncError):
                    live.publish(repo, [name], 'divergence')


if __name__ == '__main__':
    unittest.main()
