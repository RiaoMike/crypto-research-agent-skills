from pathlib import Path
import unittest


EXPECTED_SKILLS = {
    "crypto-research-skill-creator",
    "crypto-research-pipeline",
    "crypto-idea-evaluator",
    "crypto-literature-search",
    "crypto-paper-reader",
    "crypto-related-work-synthesis",
    "crypto-novelty-check",
    "crypto-theorem-review",
    "zkp-security-review",
    "lattice-parameter-audit",
    "crypto-experiment-reproducibility",
    "crypto-paper-writing",
    "crypto-venue-paper-writing",
    "ccs-writing-style",
    "usenixsec-writing-style",
    "crypto-paper-review",
}


class CorpusTests(unittest.TestCase):
    def test_exact_skill_set_and_entrypoints(self) -> None:
        root = Path(__file__).parents[1] / "skills"
        actual = {path.name for path in root.iterdir() if path.is_dir()} if root.exists() else set()
        self.assertEqual(EXPECTED_SKILLS, actual)
        for name in actual:
            self.assertTrue((root / name / "SKILL.md").is_file(), name)

    def test_only_top_level_skill_directories_contain_entrypoints(self) -> None:
        root = Path(__file__).parents[1] / "skills"
        nested = sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("SKILL.md")
            if path.parent.parent != root
        )
        self.assertEqual([], nested)


if __name__ == "__main__":
    unittest.main()
