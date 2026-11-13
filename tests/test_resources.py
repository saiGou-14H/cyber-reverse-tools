import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fetch_resources", ROOT / "scripts/fetch_resources.py")
fetch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cyber-resources-test-")
        self.base = Path(self.temporary.name).resolve()
        self.upstream = self.base / "upstream"
        self.upstream.mkdir()
        self.project = self.base / "project"
        self.project.mkdir()
        fetch.git(self.upstream, "init", "--initial-branch=main")
        skill = self.upstream / "chosen"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: chosen\ndescription: Test\n---\nBody\n")
        (skill / "references/input.txt").write_text("original\n")
        (skill / "nested").mkdir()
        (skill / "nested/SKILL.md").write_text("---\nname: unrelated\n---\n")
        (self.upstream / "LICENSE").write_text("Synthetic test license\n")
        fetch.git(self.upstream, "add", ".")
        fetch.git(self.upstream, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                  "-c", "commit.gpgsign=false", "commit", "-m", "fixture")
        self.commit = fetch.git(self.upstream, "rev-parse", "HEAD")
        self.source = {"id": "fixture", "repository": self.upstream.as_uri(), "commit": self.commit,
                       "license_files": ["LICENSE"]}
        self.skill = {"name": "chosen", "source_path": "chosen", "path": "downloaded-skills/chosen"}

    def tearDown(self):
        # The resolved temporary root was created by this test; no user checkout is removed.
        self.assertTrue(self.base.name.startswith("cyber-resources-test-"))
        self.temporary.cleanup()

    def test_pinned_checkout_and_export(self):
        (self.upstream / "chosen/references/input.txt").write_text("later upstream change\n")
        fetch.git(self.upstream, "add", ".")
        fetch.git(self.upstream, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                  "-c", "commit.gpgsign=false", "commit", "-m", "later")
        checkout = fetch.source_checkout(self.project, self.source)
        self.assertEqual(fetch.git(checkout, "rev-parse", "HEAD"), self.commit)
        destination = fetch.materialize_skill(self.project, self.skill, self.source, checkout)
        self.assertEqual((destination / "references/input.txt").read_text(), "original\n")
        self.assertFalse((destination / "nested").exists())
        self.assertTrue((destination / "UPSTREAM-LICENSE").is_file())
        self.assertEqual(fetch.materialize_skill(self.project, self.skill, self.source, checkout), destination)

    def test_preserves_changed_export(self):
        checkout = fetch.source_checkout(self.project, self.source)
        destination = fetch.materialize_skill(self.project, self.skill, self.source, checkout)
        file = destination / "references/input.txt"
        file.write_text("local edit\n")
        with self.assertRaises(RuntimeError):
            fetch.materialize_skill(self.project, self.skill, self.source, checkout)
        self.assertEqual(file.read_text(), "local edit\n")

    def test_rejects_source_traversal(self):
        checkout = fetch.source_checkout(self.project, self.source)
        skill = dict(self.skill, source_path="../outside")
        with self.assertRaises(ValueError):
            fetch.materialize_skill(self.project, skill, self.source, checkout)

    def test_catalog_references_and_local_entries(self):
        sources, skills, tools = fetch.load_catalog(ROOT)
        self.assertEqual(len(skills), 22)
        self.assertEqual(len(tools), 21)
        self.assertEqual(len(sources), 27)
        for skill in skills:
            if skill["kind"] == "local":
                self.assertTrue((ROOT / skill["path"] / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
