# Generic Agent Skills Integration

The repository follows the open [Agent Skills specification](https://agentskills.io/specification): each skill is a directory with a required `SKILL.md` containing YAML frontmatter and Markdown instructions, plus optional references, scripts, examples, or assets.

## Shared Installation

For clients that discover the cross-runtime directory:

```bash
python scripts/install.py --target agents --dry-run
python scripts/install.py --target agents
```

This targets `~/.agents/skills`. If your client documents another directory, use:

```bash
python scripts/install.py --target custom --dest /path/from/client/documentation
```

## Progressive Disclosure

The recommended loader behavior is:

1. At discovery, expose only each skill's `name`, `description`, and location.
2. When a task matches, load the complete `SKILL.md`.
3. Load linked references and run bundled scripts only when the workflow requires them.

Do not concatenate all skill bodies into every system prompt. That wastes context and weakens trigger isolation.

## Permission and Capability Mapping

Map abstract operations to the harness's actual tools:

- scholarly browsing and citation lookup;
- local manuscript/repository reading;
- code, estimator, or proof-checker execution;
- artifact storage and hashing;
- user approval for consequential external actions.

If one is unavailable, preserve the skill's failure-mode output instead of silently skipping the check. A citation search without source access, a proof review without the full proof, or a concrete-security claim without estimator provenance must remain limited or blocked.

## Trigger Testing

Test at least three classes for each deployment:

- positive requests that should activate the skill;
- nearby negative requests that should not activate it;
- adversarial/missing-capability requests that must degrade honestly.

The repository's `references/evaluation-scenarios.md` files provide starting cases. They are specifications, not evidence that every harness/model combination has passed.

