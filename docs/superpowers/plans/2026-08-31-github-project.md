# Crypto Research Agent Skills GitHub Project Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the meta-skill and twelve validated cryptography research skills as a documented, testable, public, cross-harness GitHub project.

**Architecture:** Keep every portable skill unchanged under `skills/`, place runtime-specific installation and loading guidance under `docs/`, and provide dependency-free Python tools for validation and installation. Use standard-library unit tests and a GitHub Actions matrix to make local and remote verification equivalent.

**Tech Stack:** Markdown, Python 3.10+ standard library, `unittest`, Git, GitHub CLI, GitHub Actions YAML.

## Global Constraints

- Repository name is exactly `crypto-research-agent-skills`.
- Visibility is public, license is MIT, default branch is `main`, and initial tag is `v0.1.0`.
- Include `crypto-research-skill-creator` and all twelve research skills.
- Do not commit ZIP binaries, secrets, tokens, caches, local absolute paths, or unresolved placeholders.
- Do not require third-party Python packages.
- Do not claim a universal DeepSeek skill directory; require an explicit custom destination when the harness lacks a documented convention.
- Do not overwrite an installed skill unless `--force` is explicit.
- “Top-venue rigor” is a target, never an acceptance, novelty, correctness, or security guarantee.

---

### Task 1: Import the Canonical Skill Corpus

**Files:**
- Create: `skills/crypto-research-skill-creator/**`
- Create: `skills/crypto-research-pipeline/**`
- Create: `skills/crypto-idea-evaluator/**`, `skills/crypto-literature-search/**`, `skills/crypto-paper-reader/**`, `skills/crypto-related-work-synthesis/**`, `skills/crypto-novelty-check/**`, `skills/crypto-theorem-review/**`, `skills/zkp-security-review/**`, `skills/lattice-parameter-audit/**`, `skills/crypto-experiment-reproducibility/**`, `skills/crypto-paper-writing/**`, and `skills/crypto-paper-review/**`
- Create: `tests/test_corpus.py`

**Interfaces:**
- Consumes: validated source directories in the parent workspace outputs.
- Produces: `skills/` as the canonical repository corpus and `EXPECTED_SKILLS` in `tests/test_corpus.py`.

- [ ] **Step 1: Write the failing corpus test**

```python
from pathlib import Path
import unittest

EXPECTED_SKILLS = {
    "crypto-research-skill-creator", "crypto-research-pipeline",
    "crypto-idea-evaluator", "crypto-literature-search", "crypto-paper-reader",
    "crypto-related-work-synthesis", "crypto-novelty-check",
    "crypto-theorem-review", "zkp-security-review", "lattice-parameter-audit",
    "crypto-experiment-reproducibility", "crypto-paper-writing", "crypto-paper-review",
}

class CorpusTests(unittest.TestCase):
    def test_exact_skill_set_and_entrypoints(self):
        root = Path(__file__).parents[1] / "skills"
        actual = {path.name for path in root.iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, actual)
        for name in actual:
            self.assertTrue((root / name / "SKILL.md").is_file())
```

- [ ] **Step 2: Run the test and observe the missing corpus failure**

Run: `python -m unittest tests.test_corpus -v`
Expected: failure because `skills/` or the thirteen skill directories do not exist.

- [ ] **Step 3: Copy the exact validated skill directories**

Copy the meta-skill from `outputs/crypto-research-skill-creator` and the twelve research skills from `outputs/crypto-research-skills-complete`. Exclude suite-level ZIP files and duplicate root documentation.

- [ ] **Step 4: Verify the corpus test passes and compare source hashes**

Run: `python -m unittest tests.test_corpus -v`
Expected: one passing test.

Run a SHA-256 relative-path comparison between each source skill and its imported destination.
Expected: zero missing, extra, or mismatched files.

- [ ] **Step 5: Commit the corpus**

```bash
git add skills tests/test_corpus.py
git commit -m "feat: add portable crypto research skill suite"
```

### Task 2: Build the Dependency-Free Validator

**Files:**
- Create: `scripts/validate.py`
- Create: `tests/test_validate.py`

**Interfaces:**
- Consumes: `Path` to a directory whose direct children are skill directories.
- Produces: `validate_skill(path: Path) -> list[str]`, `validate_tree(root: Path) -> dict[str, list[str]]`, and a CLI returning `0` on no findings and `1` otherwise.

- [ ] **Step 1: Write failing validator tests**

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.validate import validate_skill, validate_tree

def make_skill(root: Path, directory: str, declared: str, body: str) -> Path:
    skill = root / directory
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {declared}\ndescription: Use when testing validation behavior.\n---\n\n"
        f"# Test\n\n{body}\n",
        encoding="utf-8",
    )
    (skill / "references" / "evaluation-scenarios.md").write_text("# Evaluation Scenarios\n", encoding="utf-8")
    return skill

class ValidatorTests(unittest.TestCase):
    def test_rejects_directory_frontmatter_name_mismatch(self):
        with TemporaryDirectory() as tmp:
            skill = make_skill(Path(tmp), "actual", "declared", "## Scope\n")
            self.assertIn("directory name", "\n".join(validate_skill(skill)))

    def test_rejects_missing_local_markdown_reference(self):
        with TemporaryDirectory() as tmp:
            skill = make_skill(Path(tmp), "sample", "sample", "[Missing](references/missing.md)")
            self.assertIn("missing local reference", "\n".join(validate_skill(skill)))

    def test_rejects_missing_evaluation_scenarios(self):
        with TemporaryDirectory() as tmp:
            skill = make_skill(Path(tmp), "sample", "sample", "## Scope\n")
            (skill / "references" / "evaluation-scenarios.md").unlink()
            self.assertIn("evaluation-scenarios.md", "\n".join(validate_skill(skill)))

    def test_accepts_repository_skill_corpus(self):
        root = Path(__file__).parents[1] / "skills"
        self.assertEqual({}, validate_tree(root))
```

Each fixture uses `tempfile.TemporaryDirectory`, creates a minimal skill, and asserts the exact finding substring.

- [ ] **Step 2: Run the validator tests and observe import failure**

Run: `python -m unittest tests.test_validate -v`
Expected: failure because `scripts.validate` is absent.

- [ ] **Step 3: Implement frontmatter, structure, reference, and portability checks**

Implement standard-library parsing for the initial YAML mapping bounded by `---`. Validate `name`, `description`, directory alignment, `Use when` prefix, local Markdown links, evaluation scenarios, duplicate names, required headings, forbidden placeholder markers, and Windows/Unix author-home paths.

- [ ] **Step 4: Run unit tests and validate the complete corpus**

Run: `python -m unittest tests.test_validate -v`
Expected: all tests pass.

Run: `python scripts/validate.py skills`
Expected: `PASS: 13 skills validated` and exit `0`.

- [ ] **Step 5: Commit the validator**

```bash
git add scripts/validate.py tests/test_validate.py
git commit -m "feat: add portable skill validation"
```

### Task 3: Build the Cross-Harness Installer

**Files:**
- Create: `scripts/install.py`
- Create: `tests/test_install.py`

**Interfaces:**
- Consumes: `resolve_destination(target: str, destination: str | None, home: Path) -> Path` and `install_skills(source: Path, destination: Path, names: list[str], force: bool, dry_run: bool) -> list[Path]`.
- Produces: CLI flags `--target {codex,claude,agents,custom}`, `--dest PATH`, repeatable `--skill NAME`, `--force`, and `--dry-run`.

- [ ] **Step 1: Write failing installer tests**

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from scripts.install import install_skills, resolve_destination

class InstallerTests(unittest.TestCase):
    def test_presets_resolve_under_supplied_home(self):
        home = Path("/test-home")
        self.assertEqual(home / ".codex" / "skills", resolve_destination("codex", None, home))
        self.assertEqual(home / ".claude" / "skills", resolve_destination("claude", None, home))
        self.assertEqual(home / ".agents" / "skills", resolve_destination("agents", None, home))

    def test_custom_requires_destination(self):
        with self.assertRaises(ValueError):
            resolve_destination("custom", None, Path("/test-home"))

    def test_refuses_existing_skill_without_force(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            (source / "sample").mkdir(parents=True)
            (source / "sample" / "SKILL.md").write_text("sample", encoding="utf-8")
            (destination / "sample").mkdir(parents=True)
            with self.assertRaises(FileExistsError):
                install_skills(source, destination, ["sample"], False, False)

    def test_dry_run_writes_nothing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            (source / "sample").mkdir(parents=True)
            (source / "sample" / "SKILL.md").write_text("sample", encoding="utf-8")
            planned = install_skills(source, destination, ["sample"], False, True)
            self.assertEqual([destination / "sample"], planned)
            self.assertFalse(destination.exists())

    def test_selected_skill_copy_is_byte_identical(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            (source / "sample").mkdir(parents=True)
            payload = b"portable-skill\n"
            (source / "sample" / "SKILL.md").write_bytes(payload)
            install_skills(source, destination, ["sample"], False, False)
            self.assertEqual(payload, (destination / "sample" / "SKILL.md").read_bytes())
```

- [ ] **Step 2: Run tests and observe import failure**

Run: `python -m unittest tests.test_install -v`
Expected: failure because `scripts.install` is absent.

- [ ] **Step 3: Implement destination resolution and safe copying**

Map `codex` to `~/.codex/skills`, `claude` to `~/.claude/skills`, and `agents` to `~/.agents/skills`. Require `--dest` for `custom`. Validate all requested skill names before any copy, refuse collisions unless forced, and use temporary staging plus rename for each destination.

- [ ] **Step 4: Run tests and isolated end-to-end installs**

Run: `python -m unittest tests.test_install -v`
Expected: all tests pass.

Run: `python scripts/install.py --target custom --dest .install-smoke --dry-run`
Expected: thirteen planned installations and no new destination files.

Run a real install into a new temporary directory and compare all source/destination hashes.
Expected: zero differences.

- [ ] **Step 5: Commit the installer**

```bash
git add scripts/install.py tests/test_install.py
git commit -m "feat: add cross-harness installer"
```

### Task 4: Add Public Documentation and Project Metadata

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Create: `CONTRIBUTING.md`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `docs/getting-started.md`
- Create: `docs/codex.md`
- Create: `docs/claude-code.md`
- Create: `docs/deepseek-harness.md`
- Create: `docs/generic-agent-skills.md`
- Create: `docs/capabilities.md`
- Create: `docs/architecture.md`
- Create: `tests/test_docs.py`

**Interfaces:**
- Consumes: installer CLI and the thirteen canonical skill names.
- Produces: bilingual entry points and runtime-specific copy/paste instructions whose commands match the actual CLI.

- [ ] **Step 1: Write failing documentation integrity tests**

```python
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
REQUIRED = {
    "README.md", "README.zh-CN.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
    "docs/getting-started.md", "docs/codex.md", "docs/claude-code.md",
    "docs/deepseek-harness.md", "docs/generic-agent-skills.md",
    "docs/capabilities.md", "docs/architecture.md",
}

class DocumentationTests(unittest.TestCase):
    def test_required_public_files_exist(self):
        missing = {name for name in REQUIRED if not (ROOT / name).is_file()}
        self.assertEqual(set(), missing)

    def test_bilingual_readmes_link_to_each_other(self):
        self.assertIn("README.zh-CN.md", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("README.md", (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"))

    def test_each_skill_is_named_in_capabilities(self):
        capabilities = (ROOT / "docs" / "capabilities.md").read_text(encoding="utf-8")
        for skill in (ROOT / "skills").iterdir():
            if skill.is_dir():
                self.assertIn(skill.name, capabilities)

    def test_documented_installer_commands_match_cli(self):
        combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in REQUIRED if path.endswith(".md"))
        self.assertIn("python scripts/install.py --target codex", combined)
        self.assertIn("python scripts/install.py --target claude", combined)
        self.assertIn("python scripts/install.py --target agents", combined)
        self.assertIn("python scripts/install.py --target custom --dest", combined)

    def test_no_local_paths_secrets_or_unresolved_markers(self):
        forbidden = ("C:\\Users\\", "/Users/", "BEGIN PRIVATE KEY", "gho_", "TODO_MARKER", "TBD_MARKER")
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for marker in forbidden:
                    self.assertNotIn(marker, text, f"{marker} found in {path}")
```

- [ ] **Step 2: Run tests and observe missing-document failures**

Run: `python -m unittest tests.test_docs -v`
Expected: failures naming the absent public files.

- [ ] **Step 3: Write metadata and bilingual landing pages**

Use MIT license text, version `0.1.0`, concise contribution guidance, and Python cache/editor exclusions. Explain the suite's scientific-integrity boundaries prominently.

- [ ] **Step 4: Write runtime and capability guides**

Document Codex, Claude Code, `.agents/skills`, and custom DeepSeek-harness installation. Include trigger examples, manual-loading fallback, the idea-to-submission-readiness workflow, and the distinction between automation and accountable human decisions. Verify current runtime facts against official primary documentation.

- [ ] **Step 5: Run documentation and full test suites**

Run: `python -m unittest discover -s tests -v`
Expected: all tests pass.

- [ ] **Step 6: Commit public documentation**

```bash
git add README.md README.zh-CN.md LICENSE CHANGELOG.md CONTRIBUTING.md .gitignore pyproject.toml docs tests/test_docs.py
git commit -m "docs: add cross-agent usage and contribution guides"
```

### Task 5: Add Continuous Integration and Run Release Verification

**Files:**
- Create: `.github/workflows/validate.yml`
- Create: `docs/validation.md`

**Interfaces:**
- Consumes: `scripts/validate.py`, `scripts/install.py`, and all unit tests.
- Produces: Ubuntu/Windows and Python 3.10/3.12 CI jobs plus a human-readable release verification record.

- [ ] **Step 1: Add the CI workflow**

Configure `push` and `pull_request` triggers. Matrix over `ubuntu-latest` and `windows-latest`, Python `3.10` and `3.12`. Run:

```text
python -m unittest discover -s tests -v
python scripts/validate.py skills
python scripts/install.py --target custom --dest .install-smoke --dry-run
```

- [ ] **Step 2: Run CI-equivalent commands locally**

Run the full unittest suite, validator, dry-run installer, and real isolated installer. Scan tracked candidates for secrets, tokens, local absolute paths, ZIP files, caches, and unresolved markers.

Expected: zero test failures, zero validator findings, zero copy mismatches, and zero forbidden tracked files.

- [ ] **Step 3: Record exact results**

Write `docs/validation.md` with the date, Python/Git versions, test counts, skill counts, limitations, and commands run. Do not claim cross-harness behavioral trials that were not performed.

- [ ] **Step 4: Commit CI and validation evidence**

```bash
git add .github/workflows/validate.yml docs/validation.md
git commit -m "ci: validate skills across supported platforms"
```

### Task 6: Publish and Verify GitHub v0.1.0

**Files:**
- Modify: Git metadata only; no source file changes expected.

**Interfaces:**
- Consumes: clean validated `main`, authenticated GitHub account `RiaoMike`, repository name `crypto-research-agent-skills`.
- Produces: public GitHub repository, pushed `main`, and tag `v0.1.0`.

- [ ] **Step 1: Verify the target repository does not already exist**

Run: `gh repo view RiaoMike/crypto-research-agent-skills --json nameWithOwner,visibility`
Expected: not found. If found, stop without modifying it.

- [ ] **Step 2: Verify local release state**

Run: `git status --short`
Expected: no output.

Run: `git log --oneline --decorate -5`
Expected: the design, corpus, validator, installer, docs, and CI work represented in committed history.

- [ ] **Step 3: Create and push the public repository**

Run:

```text
gh repo create RiaoMike/crypto-research-agent-skills --public --source . --remote origin --description "Portable research-grade agent skills for cryptography, ZKP, and lattice research" --push
```

- [ ] **Step 4: Set topics and create the initial tag**

Set topics: `agent-skills`, `cryptography`, `zero-knowledge-proofs`, `lattice-cryptography`, `research-tools`, `codex`, `claude-code`, `deepseek`.

Create annotated tag `v0.1.0` with message `Initial public release` and push it.

- [ ] **Step 5: Verify remote state from GitHub**

Query repository visibility, default branch, description, topics, latest commit SHA, tag reference, and README URL through GitHub CLI/API. Verify the remote commit equals local `HEAD` and the tag resolves to the release commit.

- [ ] **Step 6: Report usage and exact limitations**

Return the GitHub URL, installation commands for Codex/Claude/generic/custom harnesses, the idea-to-research example, validation evidence, and the boundary that publication does not guarantee scientific correctness or venue acceptance.
