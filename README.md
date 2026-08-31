# Crypto Research Agent Skills

[简体中文](README.zh-CN.md) · [Getting started](docs/getting-started.md) · [Capabilities](docs/capabilities.md) · [Architecture](docs/architecture.md)

Portable, evidence-gated Agent Skills for cryptography, zero-knowledge proofs, and lattice research. The repository includes one skill-creation meta-skill and twelve research skills spanning idea triage, literature, novelty, formal review, parameters, experiments, paper writing, and adversarial pre-review.

The suite targets the working discipline expected around leading cryptography and security venues. It does **not** guarantee global novelty, proof correctness, protocol security, reproducibility on untested systems, acceptance, authorship decisions, or autonomous submission. It forbids fabricated citations, proof steps, experiments, and reviewer outcomes.

## Quick Start

Requirements: Git and Python 3.10 or later. The installer uses only the Python standard library.

```bash
git clone https://github.com/RiaoMike/crypto-research-agent-skills.git
cd crypto-research-agent-skills
python scripts/validate.py skills
```

Install all skills for your harness:

```bash
# Codex
python scripts/install.py --target codex

# Claude Code
python scripts/install.py --target claude

# Shared Agent Skills directory
python scripts/install.py --target agents

# DeepSeek or another custom harness
python scripts/install.py --target custom --dest /path/to/your/harness/skills
```

The installer refuses to overwrite an existing skill unless you explicitly pass `--force`. Use `--dry-run` to inspect the operation first, and repeat `--skill NAME` to install selected skills.

## Start a Research Project

Open a fresh agent session after installation and ask:

```text
Use crypto-research-pipeline to evaluate this ZKP/lattice idea as a gated research project.
Search and verify prior art before claiming novelty. Separate definitions, theorems,
proofs, reductions, protocol-security claims, parameters, estimates, measurements,
and reproduced results. Stop or pivot if the evidence defeats the idea. Produce a
research-state ledger, next falsifiable actions, and only evidence-supported paper text.

[Insert idea and constraints here]
```

The orchestrator routes work through the specialized skills and preserves blockers. It stops for accountable human decisions on ethics, disclosure, authorship, final claims, and external submission.

## Skill Groups

- **Meta:** `crypto-research-skill-creator`
- **Orchestration:** `crypto-research-pipeline`
- **Discovery:** `crypto-idea-evaluator`, `crypto-literature-search`, `crypto-paper-reader`, `crypto-related-work-synthesis`, `crypto-novelty-check`
- **Formal and domain review:** `crypto-theorem-review`, `zkp-security-review`, `lattice-parameter-audit`
- **Evidence and publication:** `crypto-experiment-reproducibility`, `crypto-paper-writing`, `crypto-paper-review`

See [the capability map](docs/capabilities.md) for the exact output contracts and boundaries.

## Harness Guides

- [Codex](docs/codex.md)
- [Claude Code](docs/claude-code.md)
- [DeepSeek-based harnesses](docs/deepseek-harness.md)
- [Generic Agent Skills clients](docs/generic-agent-skills.md)

The core layout follows the open [Agent Skills specification](https://agentskills.io/specification). Claude Code's documented personal and project skill locations are covered in its [official skills guide](https://code.claude.com/docs/en/skills).

## Develop and Validate

```bash
python -m unittest discover -s tests -v
python scripts/validate.py skills
python scripts/install.py --target custom --dest .install-smoke --dry-run
```

Use `crypto-research-skill-creator` when adding or refactoring a skill. Every research skill must retain explicit trigger, scope, inputs, success criteria, failure modes, workflow, output contract, integrity rules, and evaluation scenarios.

## License

MIT. See [LICENSE](LICENSE).

