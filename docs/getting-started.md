# Getting Started

## 1. Clone and Validate

```bash
git clone https://github.com/RiaoMike/crypto-research-agent-skills.git
cd crypto-research-agent-skills
python scripts/validate.py skills
```

Python 3.10 or later is required. No third-party package is needed.

## 2. Preview an Installation

```bash
python scripts/install.py --target agents --dry-run
```

Choose one target:

| Target | Destination |
|---|---|
| `codex` | `~/.codex/skills` |
| `claude` | `~/.claude/skills` |
| `agents` | `~/.agents/skills` |
| `custom` | The path supplied with `--dest` |

Examples:

```bash
python scripts/install.py --target codex
python scripts/install.py --target claude
python scripts/install.py --target agents
python scripts/install.py --target custom --dest /path/to/harness/skills
```

Install only the orchestrator and literature skill:

```bash
python scripts/install.py --target agents \
  --skill crypto-research-pipeline \
  --skill crypto-literature-search
```

The installer validates every requested name before copying and refuses existing destinations. `--force` explicitly replaces selected existing skills.

## 3. Start a Fresh Session

Some clients discover skills only at startup. Start a fresh task or session after the first installation. Then ask the agent to use a named skill or give a request that clearly matches its frontmatter description.

```text
Use crypto-idea-evaluator on this idea. Produce a claim map, feasibility risks,
kill criteria, and the next evidence-producing action. Do not claim novelty yet.
```

For the full workflow:

```text
Use crypto-research-pipeline to manage this project from idea triage through
literature, bounded novelty assessment, theory/security review, parameters,
experiments, writing, and internal review. Preserve blockers and stop for human
approval before external submission.
```

## 4. Supply Evidence, Not Just a Topic

Better inputs include the exact idea, security model, intended theorem or construction, known papers, manuscript/repository paths, parameter sets, experiment environment, resource limits, disclosure constraints, and intended venue. Missing material should remain explicitly missing; the suite instructs agents not to invent it.

## 5. Interpret the Output

The pipeline uses `pass`, `pass-with-limitations`, `fail`, and `blocked`. A polished draft does not clear a proof or novelty blocker. “Ready for human submission review” means the documented internal gates are clear; it is not an acceptance prediction or authorization to submit.

