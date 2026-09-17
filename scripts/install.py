#!/usr/bin/env python3
"""Install one or more skills into a supported agent harness directory."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
from uuid import uuid4


TARGETS = ("codex", "claude", "agents", "custom")


def resolve_destination(target: str, destination: str | None, home: Path) -> Path:
    """Resolve a harness preset or require an explicit custom destination."""
    if target == "custom":
        if not destination:
            raise ValueError("--dest is required when --target custom is used")
        return Path(destination).expanduser()
    if destination:
        raise ValueError("--dest may only be used with --target custom")
    presets = {
        "codex": home / ".codex" / "skills",
        "claude": home / ".claude" / "skills",
        "agents": home / ".agents" / "skills",
    }
    try:
        return presets[target]
    except KeyError as error:
        raise ValueError(f"unknown target: {target}") from error


def _available_skills(source: Path) -> dict[str, Path]:
    if not source.is_dir():
        raise ValueError(f"skills source does not exist: {source}")
    available = {
        path.name: path
        for path in source.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if not available:
        raise ValueError(f"no skills found in source: {source}")
    return available


def install_skills(
    source: Path,
    destination: Path,
    names: list[str],
    force: bool,
    dry_run: bool,
) -> list[Path]:
    """Validate an install set, then copy each skill through a staging path."""
    source = Path(source)
    destination = Path(destination)
    available = _available_skills(source)
    requested = list(dict.fromkeys(names)) if names else sorted(available)
    unknown = [name for name in requested if name not in available]
    if unknown:
        raise ValueError(f"unknown skill(s): {', '.join(unknown)}")

    targets = [destination / name for name in requested]
    collisions = [path.name for path in targets if path.exists()]
    if collisions and not force:
        raise FileExistsError(
            "refusing to overwrite existing skill(s): "
            + ", ".join(collisions)
            + "; pass --force to replace them"
        )
    if dry_run:
        return targets

    destination.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for name, target in zip(requested, targets, strict=True):
        staging = destination / f".{name}.staging-{uuid4().hex}"
        backup = destination / f".{name}.backup-{uuid4().hex}"
        try:
            # Skip build artifacts. `.gitignore` keeps them out of commits but
            # `copytree` does not read it, so without this filter a stale
            # `__pycache__/*.pyc` would be installed beside a freshly edited script.
            shutil.copytree(
                available[name],
                staging,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            if target.exists():
                target.rename(backup)
            staging.rename(target)
            if backup.exists():
                shutil.rmtree(backup)
            installed.append(target)
        except Exception:
            if staging.exists():
                shutil.rmtree(staging)
            if backup.exists() and not target.exists():
                backup.rename(target)
            raise
    return installed


def build_parser() -> argparse.ArgumentParser:
    default_source = Path(__file__).resolve().parents[1] / "skills"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=default_source, help="Directory containing skill folders")
    parser.add_argument("--target", choices=TARGETS, default="agents", help="Harness destination preset")
    parser.add_argument("--dest", help="Destination path, required only for the custom target")
    parser.add_argument("--skill", action="append", default=[], help="Skill name to install; repeat to select multiple")
    parser.add_argument("--force", action="store_true", help="Replace existing selected skills")
    parser.add_argument("--dry-run", action="store_true", help="Print planned copies without writing")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        destination = resolve_destination(args.target, args.dest, Path.home())
        paths = install_skills(args.source, destination, args.skill, args.force, args.dry_run)
    except (ValueError, FileExistsError, OSError) as error:
        parser.error(str(error))
    verb = "WOULD INSTALL" if args.dry_run else "INSTALLED"
    for path in paths:
        print(f"{verb}: {path}")
    print(f"SUMMARY: {len(paths)} skill(s), target={args.target}, dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
