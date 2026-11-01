"""Real disposable remote; namespace isolation and fail-closed publication."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import agent_live_sync as live


class MarketPublishTests(unittest.TestCase):
    def test_namespace_push_readback_and_old_mirror_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            root, remote = base / 'repo', base / 'remote.git'
            root.mkdir()
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, capture_output=True, check=True).stdout.decode().strip()
            git('init', '-b', 'main')
            git('config', 'user.name', 'Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            old = root / 'collaboration/live-latest/codex.md'
            old.parent.mkdir(parents=True)
            old.write_text('original old mirror', encoding='utf-8')
            git('add', '.')
            git('commit', '-m', 'baseline')
            subprocess.run(['git', 'init', '--bare', str(remote)], capture_output=True, check=True)
            git('remote', 'add', 'origin', str(remote))
            git('push', '-u', 'origin', 'main')
            git('config', 'url.' + remote.as_posix() + '.insteadOf', 'https://github.com/fixture/repo.git')
            name = 'collaboration/live-latest/codex-market.md'
            (root / name).write_text('full response ' * 5000, encoding='utf-8')
            old.write_text('unrelated dirty old mirror', encoding='utf-8')
            real = live.git
            def local(repo, *args):
                return 'https://github.com/fixture/repo.git' if args[:2] == ('remote', 'get-url') else real(repo, *args)
            with patch.object(live, 'git', side_effect=local):
                with self.assertRaises(live.SyncError):
                    live.publish(root, [name], 'legacy must reject market namespace')
                with self.assertRaises(live.SyncError):
                    live.publish(root, ['collaboration/live-latest/codex.md'], 'market must reject legacy namespace', namespace='codex-market')
                sha = live.publish(root, [name], 'market payload', namespace='codex-market')
                self.assertEqual(sha, git('ls-remote', 'origin', 'refs/heads/main').split()[0])
                content = subprocess.run(['git', '--git-dir', str(remote), 'show', sha + ':' + name], capture_output=True, check=True).stdout
                self.assertEqual(content, (root / name).read_bytes())
                self.assertEqual(git('show', sha + ':collaboration/live-latest/codex.md'), 'original old mirror')
                self.assertEqual(old.read_text(encoding='utf-8'), 'unrelated dirty old mirror')
                self.assertEqual(git('diff', '--cached', '--name-only'), '')
                git('add', 'collaboration/live-latest/codex.md')
                with self.assertRaises(live.SyncError):
                    live.publish(root, [name], 'existing staging must stop', namespace='codex-market')


if __name__ == '__main__':
    unittest.main()
