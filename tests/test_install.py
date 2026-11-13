import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_dsh_skills", ROOT / "scripts/install_dsh_skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cyber-install-test-")
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "project"
        self.destination = self.base / "plugin/skills/_ext"
        self.skills = []
        for name in ("alpha", "beta"):
            directory = self.source / "skills" / name
            directory.mkdir(parents=True)
            (directory / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Test\n---\n")
            self.skills.append({"name": name, "path": "skills/" + name, "kind": "local"})

    def tearDown(self):
        self.assertTrue(self.base.name.startswith("cyber-install-test-"))
        self.temporary.cleanup()

    def test_preview_is_read_only(self):
        plan = installer.install(self.source, self.destination, self.skills, False)
        self.assertEqual(len(plan), 2)
        self.assertFalse(self.destination.exists())

    def test_repeat_install_preserves_edits_and_manifest(self):
        installer.install(self.source, self.destination, self.skills, True)
        entry = self.destination / "alpha/SKILL.md"
        entry.write_text(entry.read_text() + "local edit\n")
        manifest = (self.destination / "_MANIFEST.json").read_bytes()
        installer.install(self.source, self.destination, self.skills, True)
        self.assertIn("local edit", entry.read_text())
        self.assertEqual((self.destination / "_MANIFEST.json").read_bytes(), manifest)

    def test_unknown_entry_is_not_removed(self):
        extra = self.destination / "extra"
        extra.mkdir(parents=True)
        (extra / "SKILL.md").write_text("---\nname: extra\ndescription: Test\n---\n")
        with self.assertRaises(ValueError):
            installer.install(self.source, self.destination, self.skills, True)
        self.assertTrue((extra / "SKILL.md").is_file())

    def test_missing_source_fails_before_any_copy(self):
        self.skills[1]["path"] = "skills/missing"
        with self.assertRaises(ValueError):
            installer.install(self.source, self.destination, self.skills, True)
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
