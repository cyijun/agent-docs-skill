"""Detect drift and broken source links in a self-hosted documentation project."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project_check', ROOT / 'scripts/check_project.py')
check_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_module)

class SelfManagement(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            '.git', '.local', '__pycache__', 'forward-tests', 'validation-report.json', 'build_materials.py'))

    def tearDown(self):
        self.temp.cleanup()

    def test_project_is_consistent(self):
        self.assertEqual(check_module.check_project(self.root), [])

    def test_edited_consumer_copy_is_detected(self):
        target = self.root / '.agents/skills/prose-standard/SKILL.md'
        target.write_text(target.read_text() + '\nUnreviewed local policy.\n')
        self.assertTrue(any('differs from' in error for error in check_module.check_project(self.root)))

    def test_broken_distribution_reference_is_detected(self):
        target = self.root / 'agent-docs/SKILL.md'
        target.write_text(target.read_text() + '\n[Missing](references/no-such-file.md)\n')
        self.assertTrue(any('no-such-file.md' in error for error in check_module.check_project(self.root)))

if __name__ == '__main__':
    unittest.main()
