"""Fast checks for physical export-folder contents, including ignored files."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('finalizer', Path(__file__).resolve().parents[1] / 'scripts/finalize-codex-task.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ExportFolderTests(unittest.TestCase):
    def test_owned_markdown_and_reject_foreign_or_raw(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'collaboration/codex-sessions'
            folder.mkdir(parents=True)
            owner = hashlib.sha256(module.exporter.canonical(root).encode()).hexdigest()
            entry = folder / 'session.md'
            entry.write_text(f'<!-- codex-export-v1 project={owner} session=test -->\n', encoding='utf-8')
            with patch.object(module, 'ROOT', root):
                module.validate_exports()
                entry.write_text('Foreign or unfiltered Markdown', encoding='utf-8')
                with self.assertRaises(RuntimeError):
                    module.validate_exports()
                entry.unlink()
                (folder / 'raw.jsonl').write_text('{}\n', encoding='utf-8')
                with self.assertRaises(RuntimeError):
                    module.validate_exports()


if __name__ == '__main__':
    unittest.main()
