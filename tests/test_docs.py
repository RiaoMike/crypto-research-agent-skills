from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
REQUIRED = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "docs/getting-started.md",
    "docs/codex.md",
    "docs/claude-code.md",
    "docs/deepseek-harness.md",
    "docs/generic-agent-skills.md",
    "docs/capabilities.md",
    "docs/architecture.md",
}


class DocumentationTests(unittest.TestCase):
    def test_required_public_files_exist(self) -> None:
        missing = {name for name in REQUIRED if not (ROOT / name).is_file()}
        self.assertEqual(set(), missing)

    def test_bilingual_readmes_link_to_each_other(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("README.zh-CN.md", english)
        self.assertIn("README.md", chinese)

    def test_each_skill_is_named_in_capabilities(self) -> None:
        capabilities = (ROOT / "docs" / "capabilities.md").read_text(encoding="utf-8")
        for skill in (ROOT / "skills").iterdir():
            if skill.is_dir():
                self.assertIn(skill.name, capabilities)

    def test_documented_installer_commands_match_cli(self) -> None:
        markdown = [ROOT / path for path in REQUIRED if path.endswith(".md")]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in markdown)
        self.assertIn("python scripts/install.py --target codex", combined)
        self.assertIn("python scripts/install.py --target claude", combined)
        self.assertIn("python scripts/install.py --target agents", combined)
        self.assertIn("python scripts/install.py --target custom --dest", combined)

    def test_no_author_paths_secrets_or_unresolved_markers(self) -> None:
        forbidden = (
            "C:\\" + "Users\\epicr",
            "/Users/" + "epicr",
            "BEGIN " + "PRIVATE KEY",
            "gho" + "_************************************",
            "TODO" + "_MARKER",
            "TBD" + "_MARKER",
        )
        for path in ROOT.rglob("*"):
            if (
                not path.is_file()
                or ".git" in path.parts
                or "__pycache__" in path.parts
                or "superpowers" in path.parts
            ):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in forbidden:
                self.assertNotIn(marker, text, f"{marker} found in {path}")


if __name__ == "__main__":
    unittest.main()
