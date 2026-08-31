# Using the Skills with a DeepSeek-Based Harness

DeepSeek models can run inside many different agent harnesses. The model name does not define a universal skill directory, file-reading tool, activation protocol, or permission system. Use the custom installer target and adapt the harness explicitly.

## Install to the Harness Directory

```bash
python scripts/install.py --target custom --dest /path/to/your/harness/skills --dry-run
python scripts/install.py --target custom --dest /path/to/your/harness/skills
```

Replace the destination with a directory the selected harness can read. If the harness already supports the open Agent Skills format, point its skill configuration at that directory.

## Minimal Loader Contract

A compatible loader should:

1. enumerate direct child directories containing `SKILL.md`;
2. parse the YAML frontmatter and retain at least `name`, `description`, and file location;
3. expose the compact name/description catalog to the model;
4. instruct the model to load the matching `SKILL.md` before acting;
5. resolve relative `references/`, `scripts/`, and `examples/` paths against the skill directory;
6. expose missing network, file, compute, proof-checker, or citation capabilities honestly;
7. enforce human authorization for external writes, communication, disclosure, authorship, and submission.

This follows the open [Agent Skills client implementation guidance](https://agentskills.io/client-implementation/adding-skills-support), including progressive disclosure: catalog first, full instructions on activation, supporting resources only when required.

## System-Prompt Adapter

For a harness with filesystem reading but no native skill tool, add a compact instruction like:

```text
Available skills are listed as name, description, and SKILL.md path. When a
request matches a skill description, read that SKILL.md completely before
acting. Resolve relative paths from the directory containing SKILL.md. Load
referenced resources only when the skill routes you to them. If a required tool
or source is unavailable, report the missing verification and do not simulate it.
```

For a harness without filesystem access, implement an `activate_skill(name)` tool that returns the selected `SKILL.md`, plus a resource-reading tool rooted inside that skill directory.

## Recommended Entry Prompt

```text
Activate crypto-research-pipeline for this project. Maintain a versioned claim
and evidence ledger. Use the specialist skills when their triggers match. Do not
invent citations, novelty, proof steps, security implications, estimator runs,
benchmarks, or artifact results. Stop at accountable human submission review.
```

Model capability varies. Run the supplied evaluation scenarios with the exact model, system prompt, tool permissions, and context limits you intend to deploy.

