"""Exercise real Git/index/push behavior using disposable repos and a bare remote."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('finalizer', BASE / 'scripts/finalize-codex-task.py')
finalizer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finalizer)
scanner = finalizer.scanner


class FinalizeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.remote = Path(self.tmp.name) / 'remote.git'
        self.home = Path(self.tmp.name) / 'codex-home'
        (self.home / 'sessions').mkdir(parents=True)
        self.env = dict(os.environ, CODEX_HOME=str(self.home), PYTHONIOENCODING='utf-8', GIT_TERMINAL_PROMPT='0', CODEX_USAGE_DISABLED='1', CODEX_NOTIFY_DISABLED='1', CODEX_SOUND_DISABLED='1')
        self.status = self.root / 'docs/00_PROJECT_STATUS.md'
        if hasattr(type(self), 'template'):
            shutil.copytree(type(self).template / 'repo', self.root, dirs_exist_ok=True)
            shutil.copytree(type(self).template / 'remote.git', self.remote)
            self.git('remote', 'set-url', 'origin', str(self.remote))
            return
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Workflow Test')
        self.git('config', 'user.email', 'workflow@example.invalid')
        self.git('config', 'commit.gpgSign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / '.git/empty-test-hooks'))
        (self.root / 'scripts').mkdir()
        for name in ('finalize-codex-task.py', 'finalize-codex-task.ps1', 'finalize.ps1', 'scan-codex-secrets.py', 'export-codex-session.py', 'notify-codex.ps1', 'codex-notification.py'):
            shutil.copy(BASE / 'scripts' / name, self.root / 'scripts' / name)
        (self.root / '.gitignore').write_text('__pycache__/\n*.pyc\n.env\n.codex/\n', encoding='utf-8')
        (self.root / 'docs').mkdir()
        self.status = self.root / 'docs/00_PROJECT_STATUS.md'
        self.status.write_text('Last Updated: baseline\n' + '\n'.join('## ' + h + '\nBaseline\n' for h in finalizer.STATUS), encoding='utf-8')
        (self.root / 'note.txt').write_text('safe baseline\n', encoding='utf-8')
        self.git('add', '-A')
        self.git('commit', '-m', 'chore: baseline')
        subprocess.run(['git', 'init', '--bare', str(self.remote)], check=True, capture_output=True)
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-u', 'origin', 'main')
        cached = tempfile.TemporaryDirectory()
        type(self).addClassCleanup(cached.cleanup)
        type(self).template = Path(cached.name)
        shutil.copytree(self.root, type(self).template / 'repo')
        shutil.copytree(self.remote, type(self).template / 'remote.git')

    def git(self, *args):
        p = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, env=self.env)
        if p.returncode:
            raise AssertionError('Test Git operation failed: ' + args[0])
        return p.stdout.decode('utf-8').strip()

    def prepare(self):
        self.status.write_text(self.status.read_text(encoding='utf-8').replace('baseline', 'updated task'), encoding='utf-8')
        folder = self.root / 'collaboration/codex-reports'
        folder.mkdir(parents=True, exist_ok=True)
        self.report = folder / '2026-10-26_1500_TEST.md'
        self.report.write_text('\n'.join('# ' + h + '\n\n' + ('PENDING' if h == 'Git Commit' else 'Task evidence') + '\n' for h in finalizer.HEADINGS), encoding='utf-8')
        (self.root / 'note.txt').write_text('safe task change\n', encoding='utf-8')

    def cli(self, *args, ps=False):
        command = (['powershell', '-NoProfile', '-File', str(self.root / 'scripts/finalize.ps1'), 'TEST'] if ps else
                   [sys.executable, str(self.root / 'scripts/finalize-codex-task.py'), '--task-id', 'TEST'])
        return subprocess.run(command + list(args), cwd=self.root, env=self.env, capture_output=True, encoding='utf-8', errors='replace', timeout=600)

    def remote_sha(self):
        return self.git('ls-remote', '--heads', 'origin', 'refs/heads/main').split()[0]

    def test_modified_commit_push_metadata_and_no_change(self):
        self.prepare()
        p = self.cli('-Message', 'chore: test actual finalize', ps=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn('SYNCED', p.stdout)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.remote_sha())
        self.assertIn(self.git('rev-parse', 'HEAD~1'), self.report.read_text(encoding='utf-8'))
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '3')
        self.assertEqual(self.git('status', '--porcelain'), '')
        p = self.cli()
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('Nothing to commit', p.stdout)
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '3')

    def test_dry_run_preserves_index_head_remote(self):
        self.prepare()
        head = self.git('rev-parse', 'HEAD')
        p = self.cli('--dry-run')
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn('DRY RUN', p.stdout)
        self.assertEqual(head, self.git('rev-parse', 'HEAD'))
        self.assertEqual(head, self.remote_sha())
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')

    def test_worktree_secret_stops_before_add(self):
        self.prepare()
        secret = 'ghp_' + 'Q' * 36
        (self.root / 'note.txt').write_text(secret, encoding='utf-8')
        p = self.cli()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('File: note.txt | Rule: provider-token | Line: 1', p.stdout)
        self.assertNotIn(secret, p.stdout + p.stderr)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '1')

    def test_index_secret_is_detected_when_worktree_is_clean(self):
        self.prepare()
        secret = 'sk-' + 'Q' * 40
        (self.root / 'note.txt').write_text(secret, encoding='utf-8')
        self.git('add', 'note.txt')
        (self.root / 'note.txt').write_text('safe baseline\n', encoding='utf-8')
        self.assertFalse(scanner.scan_repo(self.root)[1])
        self.assertTrue(scanner.scan_repo(self.root, staged=True)[1])
        p = self.cli()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('File: note.txt | Rule: provider-token | Line: 1', p.stdout)
        self.assertNotIn(secret, p.stdout + p.stderr)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')

    def test_secret_inserted_after_add_resets_index(self):
        self.prepare()
        original_git = finalizer.git
        def intercept(*args, **kwargs):
            result = original_git(*args, **kwargs)
            if args == ('add', '-A'):
                path = self.root / 'note.txt'
                path.write_text('ghp_' + 'Z' * 36, encoding='utf-8')
                original_git('add', 'note.txt')
                path.write_text('safe task change\n', encoding='utf-8')
            return result
        output = io.StringIO()
        with patch.object(finalizer, 'ROOT', self.root), patch.object(finalizer, 'git', side_effect=intercept), patch.dict(os.environ, self.env), patch.object(sys, 'argv', ['finalize', '--task-id', 'TEST']), contextlib.redirect_stdout(output):
            code = finalizer.main()
        self.assertEqual(code, 1)
        self.assertIn('provider-token', output.getvalue())
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '1')

    def test_failed_tests_stop_before_commit(self):
        self.prepare()
        folder = self.root / 'tests'
        folder.mkdir()
        (folder / 'test_failure.py').write_text('import unittest\nclass Failure(unittest.TestCase):\n def test_failure(self): self.fail("expected")\n', encoding='utf-8')
        p = self.cli()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('LOCAL ONLY', p.stdout)
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '1')

    def test_push_failure_and_retry(self):
        self.prepare()
        self.git('remote', 'set-url', 'origin', str(self.remote) + '-missing')
        name = 'codex-finalize-' + 'a' * 32 + '.json'
        p = self.cli('--result-name', name)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('LOCAL ONLY', p.stdout)
        state = json.loads((self.root / '.git' / name).read_text(encoding='utf-8'))
        self.assertEqual(state['status'], 'WARNING')
        self.assertFalse(state['synced'])
        self.assertEqual(self.git('rev-list', '--count', 'HEAD'), '3')
        self.git('remote', 'set-url', 'origin', str(self.remote))
        p = self.cli('--push-only')
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.remote_sha())

    def test_outgoing_ancestor_secret_cannot_be_hidden_by_deletion(self):
        (self.root / 'note.txt').write_text('ghp_' + 'W' * 36, encoding='utf-8')
        self.git('add', '-A')
        self.git('commit', '-m', 'test: synthetic historical fixture')
        (self.root / 'note.txt').write_text('safe again\n', encoding='utf-8')
        self.git('add', '-A')
        self.git('commit', '-m', 'test: delete synthetic fixture')
        before = self.remote_sha()
        p = self.cli('--push-only')
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('provider-token', p.stdout)
        self.assertEqual(before, self.remote_sha())

    def test_forbidden_paths_and_credential_rules(self):
        for path in ('.env', '.env.local', '.codex/auth.json', 'raw.jsonl', 'cookies.txt', 'id_rsa', 'private.pem'):
            self.assertTrue(scanner.scan_blob(path, b'fixture'))
        for key in ('API_KEY', 'AWS_SECRET_ACCESS_KEY', 'PASSWORD', 'OAUTH_TOKEN'):
            self.assertTrue(scanner.scan_text(key + '=' + 'synthetic_fixture'))
        self.assertFalse(scanner.scan_text('password' + '=' + '[REDACTED]'))
        self.assertTrue(scanner.scan_blob('binary.dat', b'\x00fixture'))


if __name__ == '__main__':
    unittest.main()
