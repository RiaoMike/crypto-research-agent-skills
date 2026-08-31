# Using the Skills with Codex

## Personal Installation

From the cloned repository:

```bash
python scripts/install.py --target codex --dry-run
python scripts/install.py --target codex
```

This copies each skill to `~/.codex/skills/<skill-name>/SKILL.md`. Start a fresh Codex task if the newly created top-level directory is not detected in the current task.

## Selective Installation

```bash
python scripts/install.py --target codex \
  --skill crypto-research-pipeline \
  --skill crypto-theorem-review \
  --skill zkp-security-review
```

## Invocation

Codex can select a skill from its `name` and `description` when the request matches. Naming the skill removes ambiguity:

```text
Use lattice-parameter-audit to reproduce this MLWE concrete-security estimate.
Record the estimator version, commit, command, input parameters, cost model,
memory assumptions, sensitivity analysis, and any blocked claim wording.
```

For end-to-end work, use `crypto-research-pipeline`. Keep repositories, manuscripts, private notes, and compute resources within the scope you intend Codex to access. External communication, authorship, responsible disclosure, and submission remain human-authorized actions.

## Updating

Preview first, then explicitly replace the installed copies:

```bash
git pull
python scripts/validate.py skills
python scripts/install.py --target codex --dry-run --force
python scripts/install.py --target codex --force
```

The source repository remains separate from installed copies, so local edits under `~/.codex/skills` are overwritten only when `--force` is used.

