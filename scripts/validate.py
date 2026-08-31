#!/usr/bin/env python3
"""Validate the portable crypto research skill corpus without dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REQUIRED_HEADINGS = (
    "## Scope",
    "## Required Inputs",
    "## Success Criteria",
    "## Failure Modes",
    "## Workflow",
    "## Output Contract",
)
FORBIDDEN_PATTERNS = (
    (re.compile(r"\bTODO\b", re.IGNORECASE), "TODO marker"),
    (re.compile(r"\bTBD\b", re.IGNORECASE), "TBD marker"),
    (re.compile(r"PLACEHOLDER_VALUE", re.IGNORECASE), "placeholder value"),
    (re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"), "Windows author-home path"),
    (re.compile(r"/Users/[^/\s]+"), "macOS author-home path"),
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return the simple top-level YAML mapping and Markdown body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error

    metadata: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"\'')
    return metadata, "\n".join(lines[closing + 1 :])


def _local_reference_findings(skill: Path) -> list[str]:
    findings: list[str] = []
    for markdown in skill.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0].strip()
            if " " in target:
                target = target.split(" ", 1)[0]
            resolved = markdown.parent / unquote(target)
            if not resolved.exists():
                relative = markdown.relative_to(skill).as_posix()
                findings.append(f"missing local reference in {relative}: {raw_target}")
    return findings


def _portability_findings(skill: Path) -> list[str]:
    findings: list[str] = []
    for path in skill.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".txt", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                findings.append(f"{label} in {path.relative_to(skill).as_posix()}")
    return findings


def validate_skill(skill: Path) -> list[str]:
    """Return all structural findings for one skill directory."""
    skill = Path(skill)
    findings: list[str] = []
    entrypoint = skill / "SKILL.md"
    if not entrypoint.is_file():
        return ["SKILL.md is missing"]

    text = entrypoint.read_text(encoding="utf-8")
    try:
        metadata, body = parse_frontmatter(text)
    except ValueError as error:
        return [str(error)]

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not name:
        findings.append("frontmatter name is missing")
    elif not NAME_PATTERN.fullmatch(name):
        findings.append("frontmatter name must use lowercase letters, digits, and hyphens")
    if name and name != skill.name:
        findings.append(f"directory name '{skill.name}' does not match frontmatter name '{name}'")
    if not description:
        findings.append("frontmatter description is missing")
    elif not description.startswith("Use when"):
        findings.append("frontmatter description must begin with 'Use when'")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            findings.append(f"required heading is missing: {heading}")

    scenario = skill / "references" / "evaluation-scenarios.md"
    executable_tests = list((skill / "tests").glob("test*.py")) if (skill / "tests").is_dir() else []
    if not scenario.is_file() and not executable_tests:
        findings.append("references/evaluation-scenarios.md or executable tests are required")

    findings.extend(_local_reference_findings(skill))
    findings.extend(_portability_findings(skill))
    return findings


def validate_tree(root: Path) -> dict[str, list[str]]:
    """Return findings keyed by direct child skill directory."""
    root = Path(root)
    if not root.is_dir():
        return {str(root): ["skills root is missing or is not a directory"]}

    results: dict[str, list[str]] = {}
    declared_names: dict[str, list[str]] = {}
    for skill in sorted((path for path in root.iterdir() if path.is_dir()), key=lambda path: path.name):
        findings = validate_skill(skill)
        try:
            metadata, _ = parse_frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"))
            declared = metadata.get("name", "")
            if declared:
                declared_names.setdefault(declared, []).append(skill.name)
        except (OSError, ValueError):
            pass
        if findings:
            results[skill.name] = findings

    for declared, directories in declared_names.items():
        if len(directories) > 1:
            message = f"duplicate skill name '{declared}' declared by: {', '.join(sorted(directories))}"
            for directory in directories:
                results.setdefault(directory, []).append(message)
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default="skills", type=Path, help="Skills directory to validate")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    findings = validate_tree(args.root)
    if findings:
        for skill, messages in findings.items():
            print(f"FAIL: {skill}")
            for message in messages:
                print(f"  - {message}")
        return 1
    count = sum(1 for path in args.root.iterdir() if path.is_dir())
    print(f"PASS: {count} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
