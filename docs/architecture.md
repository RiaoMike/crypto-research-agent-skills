# Architecture

## Portable Core

Every skill is self-contained under `skills/<name>/`. The required `SKILL.md` carries trigger metadata and the core workflow. Detailed protocols live in `references/`; deterministic validation lives in `scripts/`; examples and tests remain local to the skill.

This structure implements progressive disclosure: harnesses catalog names and descriptions, load the full skill only when it matches, and load supporting resources only when routed. The design follows the [Agent Skills specification](https://agentskills.io/specification).

## Research Layers

```text
idea and constraints
        ↓
literature → paper reading → related-work synthesis → bounded novelty
        ↓
theorem/reduction review ↔ ZKP security review ↔ lattice parameter audit
        ↓
experiments and artifacts → evidence ledger
        ↓
paper writing → adversarial review → human submission review
```

`crypto-research-pipeline` maintains the project state across layers. A blocker discovered downstream propagates to every dependent claim and reopens the earliest responsible stage. Text quality never upgrades evidence quality.

## Evidence Types

The suite keeps these states distinct:

- reported by a source;
- derived in the current work;
- estimated by a named model/tool;
- measured in a documented environment;
- independently reproduced;
- conjectured or planned;
- unavailable or blocked.

Claims link to citations, proof objects, parameters, commands, outputs, figures/tables, policy snapshots, limitations, and decisions. The pipeline preserves superseded states rather than rewriting research history.

## Harness Boundary

The portable skills do not name browser, filesystem, shell, proof-assistant, citation-database, or subagent APIs. The harness supplies those capabilities and permissions. Missing capabilities produce explicit limitations. Runtime-specific extensions belong in adapters or wrapper skills so the canonical core remains reusable.

## Human Boundary

Agents may organize evidence, propose experiments, audit arguments, draft text, and simulate internal review. Accountable humans retain ethics and dual-use decisions, vulnerability disclosure, authorship, conflicts, funding statements, final scientific claims, and external submission authority.

