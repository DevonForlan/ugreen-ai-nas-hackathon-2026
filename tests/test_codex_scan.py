"""Fast scanner regressions; values are synthetic, constructed at runtime."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('scanner', Path(__file__).resolve().parents[1] / 'scripts/scan-codex-secrets.py')
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class ScannerTests(unittest.TestCase):
    def test_short_credentials_are_not_exempt(self):
        for name in ('password', 'api_key', 'oauth_token', 'AWS_SECRET_ACCESS_KEY'):
            self.assertTrue(scanner.scan_text(name + '=' + 'x'))
        for name in ('Cookie', 'Authorization'):
            self.assertTrue(scanner.scan_text(name + ': ' + 'a=b'))

    def test_redacted_markers_and_code_references(self):
        for name in ('password', 'api_key', 'oauth_token'):
            self.assertFalse(scanner.scan_text(name + '=' + '[REDACTED]'))
        self.assertFalse(scanner.scan_text('password' + '=' + 'os.environ.get("EXAMPLE")'))

    def test_paths_and_nonregular_content_fail_closed(self):
        self.assertTrue(scanner.scan_blob('.codex/auth.json', b''))
        self.assertTrue(scanner.scan_blob('link.txt', b'', '120000'))
        self.assertTrue(scanner.scan_blob('binary.dat', b'\x00'))


if __name__ == '__main__':
    unittest.main()
