from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate import validate_skill, validate_tree


REQUIRED_BODY = """## Scope

Test scope.

## Required Inputs

Test inputs.

## Success Criteria

Test success.

## Failure Modes

Test failures.

## Workflow

Test workflow.

## Output Contract

Test output.
"""


def make_skill(root: Path, directory: str, declared: str, body: str = REQUIRED_BODY) -> Path:
    skill = root / directory
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {declared}\ndescription: Use when testing validation behavior.\n---\n\n"
        f"# Test\n\n{body}\n",
        encoding="utf-8",
    )
    (skill / "references" / "evaluation-scenarios.md").write_text(
        "# Evaluation Scenarios\n\n- Minimal scenario.\n",
        encoding="utf-8",
    )
    return skill


class ValidatorTests(unittest.TestCase):
    def test_rejects_directory_frontmatter_name_mismatch(self) -> None:
        with TemporaryDirectory() as tmp:
            skill = make_skill(Path(tmp), "actual", "declared")
            self.assertIn("directory name", "\n".join(validate_skill(skill)))

    def test_rejects_missing_local_markdown_reference(self) -> None:
        with TemporaryDirectory() as tmp:
            skill = make_skill(
                Path(tmp),
                "sample",
                "sample",
                REQUIRED_BODY + "\n[Missing](references/missing.md)\n",
            )
            self.assertIn("missing local reference", "\n".join(validate_skill(skill)))

    def test_rejects_missing_evaluation_scenarios_or_tests(self) -> None:
        with TemporaryDirectory() as tmp:
            skill = make_skill(Path(tmp), "sample", "sample")
            (skill / "references" / "evaluation-scenarios.md").unlink()
            self.assertIn("evaluation-scenarios.md", "\n".join(validate_skill(skill)))

    def test_rejects_duplicate_declared_names(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_skill(root, "first", "duplicate")
            make_skill(root, "second", "duplicate")
            findings = validate_tree(root)
            self.assertIn("duplicate skill name", "\n".join(sum(findings.values(), [])))

    def test_accepts_repository_skill_corpus(self) -> None:
        root = Path(__file__).parents[1] / "skills"
        self.assertEqual({}, validate_tree(root))


if __name__ == "__main__":
    unittest.main()
