from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.install import install_skills, resolve_destination


def create_source(root: Path, name: str = "sample", payload: bytes = b"portable-skill\n") -> Path:
    source = root / "source"
    skill = source / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_bytes(payload)
    return source


class InstallerTests(unittest.TestCase):
    def test_presets_resolve_under_supplied_home(self) -> None:
        home = Path("test-home")
        self.assertEqual(home / ".codex" / "skills", resolve_destination("codex", None, home))
        self.assertEqual(home / ".claude" / "skills", resolve_destination("claude", None, home))
        self.assertEqual(home / ".agents" / "skills", resolve_destination("agents", None, home))

    def test_custom_requires_destination(self) -> None:
        with self.assertRaises(ValueError):
            resolve_destination("custom", None, Path("test-home"))

    def test_unknown_skill_is_rejected_before_copy(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = create_source(root)
            destination = root / "destination"
            with self.assertRaises(ValueError):
                install_skills(source, destination, ["missing"], False, False)
            self.assertFalse(destination.exists())

    def test_refuses_existing_skill_without_force(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = create_source(root)
            destination = root / "destination"
            (destination / "sample").mkdir(parents=True)
            with self.assertRaises(FileExistsError):
                install_skills(source, destination, ["sample"], False, False)

    def test_dry_run_writes_nothing(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = create_source(root)
            destination = root / "destination"
            planned = install_skills(source, destination, ["sample"], False, True)
            self.assertEqual([destination / "sample"], planned)
            self.assertFalse(destination.exists())

    def test_selected_skill_copy_is_byte_identical(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = b"portable-skill\n"
            source = create_source(root, payload=payload)
            destination = root / "destination"
            installed = install_skills(source, destination, ["sample"], False, False)
            self.assertEqual([destination / "sample"], installed)
            self.assertEqual(payload, (destination / "sample" / "SKILL.md").read_bytes())

    def test_force_replaces_existing_skill(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = create_source(root, payload=b"new\n")
            destination = root / "destination"
            (destination / "sample").mkdir(parents=True)
            (destination / "sample" / "SKILL.md").write_bytes(b"old\n")
            install_skills(source, destination, ["sample"], True, False)
            self.assertEqual(b"new\n", (destination / "sample" / "SKILL.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
