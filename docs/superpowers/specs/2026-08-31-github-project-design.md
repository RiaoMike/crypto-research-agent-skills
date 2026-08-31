# Crypto Research Agent Skills GitHub Project Design

Date: 2026-08-31
Status: Approved for implementation
Repository name: `crypto-research-agent-skills`
Visibility: Public
License: MIT
Initial version: `v0.1.0`

## Purpose

Publish the existing `crypto-research-skill-creator` meta-skill and twelve cryptography research skills as one portable, maintainable open-source project. The project must explain how to use the same skill core with Codex, Claude Code, DeepSeek-based harnesses, and generic Agent Skills-compatible runtimes.

The repository targets top-venue research rigor through explicit evidence gates. It does not guarantee global novelty, proof correctness, protocol security, artifact reproducibility on untested systems, paper acceptance, authorship decisions, or autonomous submission.

## Users and Primary Workflows

The primary users are cryptography, ZKP, and lattice researchers using coding/research agents.

Supported workflows:

1. Install the full suite or selected skills into a compatible harness.
2. Give an idea to `crypto-research-pipeline` and receive a gated research program rather than invented results.
3. Search literature, verify citations, read papers, synthesize related work, and perform bounded novelty checks.
4. Audit theorems, reductions, ZKP security properties, lattice parameters, experiments, and artifacts.
5. Draft a manuscript from a verified claim/evidence ledger and run adversarial internal review.
6. Use `crypto-research-skill-creator` to create, audit, or refactor additional domain skills with the same conventions.

## Repository Architecture

```text
crypto-research-agent-skills/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── skills/
│   ├── crypto-research-skill-creator/
│   ├── crypto-research-pipeline/
│   └── eleven additional research skills/
├── docs/
│   ├── getting-started.md
│   ├── codex.md
│   ├── claude-code.md
│   ├── deepseek-harness.md
│   ├── generic-agent-skills.md
│   ├── capabilities.md
│   ├── architecture.md
│   └── superpowers/specs/this document
├── scripts/
│   ├── install.py
│   └── validate.py
└── .github/workflows/
    └── validate.yml
```

The `skills/` directory is the canonical source. Each skill retains its `SKILL.md` and supporting `references/`, `scripts/`, `examples/`, or assets. Runtime-specific instructions belong in `docs/`, not inside the shared skill core unless behavior genuinely differs.

## Included Skills

The project contains thirteen skill packages:

- Meta-skill: `crypto-research-skill-creator`.
- Orchestrator: `crypto-research-pipeline`.
- Discovery and synthesis: `crypto-idea-evaluator`, `crypto-literature-search`, `crypto-paper-reader`, `crypto-related-work-synthesis`, `crypto-novelty-check`.
- Formal and domain review: `crypto-theorem-review`, `zkp-security-review`, `lattice-parameter-audit`.
- Evidence and publication: `crypto-experiment-reproducibility`, `crypto-paper-writing`, `crypto-paper-review`.

## Cross-Harness Installation

The installer accepts one or more skill names and an explicit destination. It also supports documented presets:

- Codex personal skills directory.
- Claude Code personal skills directory.
- Cross-runtime `.agents/skills` directory.
- A user-supplied project or harness directory for DeepSeek-based systems.

The installer must:

- run without third-party Python packages;
- refuse overwrites unless `--force` is explicitly provided;
- support `--dry-run`;
- copy exact skill directories without rewriting their contents;
- print installed skills and destination paths;
- return nonzero on invalid source, unknown skill, or failed copy.

DeepSeek is a model family rather than a single standardized harness. The documentation therefore defines a generic system-prompt/skill-loader contract and gives adapter examples instead of claiming one universal DeepSeek path.

## Validation

The repository validator uses only the Python standard library and checks:

- every direct child of `skills/` has `SKILL.md`;
- frontmatter contains valid `name` and `description` fields;
- directory name matches frontmatter `name`;
- descriptions begin with `Use when` and stay trigger-focused;
- referenced local Markdown files exist;
- required research sections exist where applicable;
- evaluation-scenario files are present;
- forbidden placeholders and author-machine absolute paths are absent;
- duplicate skill names are rejected.

GitHub Actions runs the validator and installer dry-run on Windows and Ubuntu with supported Python versions. Local verification runs the same commands before push.

Structural validation does not substitute for blinded behavioral trials. The project documents this limitation and keeps each skill's evaluation scenarios as executable test specifications for future cross-harness trials.

## Documentation

`README.md` is the English landing page and `README.zh-CN.md` is the Chinese equivalent. Both contain:

- project purpose and scope;
- skill inventory;
- quick installation;
- a minimal idea-to-paper-readiness example;
- safety and scientific-integrity boundaries;
- links to runtime-specific guides.

Runtime guides describe discovery/trigger behavior, installation directories, manual loading fallback, and example prompts. Commands must be copyable and must not assume the author's machine paths or credentials.

## GitHub Publication

The local project will be initialized as a Git repository with default branch `main`. After validation:

1. create the public repository `crypto-research-agent-skills` under the authenticated GitHub account;
2. push the validated `main` branch;
3. set a concise description and relevant topics;
4. create annotated tag `v0.1.0` and push it;
5. verify the remote default branch, public visibility, README rendering, file tree, and tag.

No repository is deleted or overwritten. If a repository with the target name already exists, publication stops for explicit user direction.

## Error Handling

- Missing or invalid GitHub authentication: stop after preserving the complete local repository and request account authorization.
- Existing remote repository name: do not reuse or overwrite it without explicit approval.
- Validation failure: do not create a release tag or push a claimed-ready version.
- Push or API failure: report the exact failed step; retain the local commit for retry.
- Runtime documentation uncertainty: state the adapter contract and avoid inventing a canonical path.

## Acceptance Criteria

- All thirteen skills are present and byte-equivalent to the validated source versions except for explicitly reviewed portability fixes.
- English and Chinese entry documentation is complete and internally consistent.
- Codex, Claude Code, generic Agent Skills, and DeepSeek-harness usage paths are documented.
- Installer dry-run and isolated install tests pass on the local system.
- The full validator reports zero failures and GitHub Actions is configured to run equivalent checks.
- No placeholder, local absolute path, secret, token, generated cache, or ZIP binary is committed.
- The public GitHub repository, `main` branch, and `v0.1.0` tag are remotely visible after push.
