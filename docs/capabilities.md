# Capability Map

## Meta-Skill

### `crypto-research-skill-creator`

Creates, audits, and refactors reusable cryptography/ZKP/lattice skills. It enforces trigger specificity, scope, inputs, success criteria, failure modes, citation verification, claim distinctions, domain checks, output contracts, and evaluation scenarios.

## Orchestration

### `crypto-research-pipeline`

Turns an idea or partial project into a versioned, evidence-gated workflow through literature, novelty, theory, security, parameters, experiments, writing, and pre-review. It propagates blockers, rolls back unsupported claims, records decisions, and stops for human sign-off.

## Discovery and Synthesis

### `crypto-idea-evaluator`

Produces a bounded research question, contribution/claim map, assumptions, feasibility analysis, risk register, discriminating tests, kill criteria, and go/pivot/stop recommendation.

### `crypto-literature-search`

Builds reproducible search queries and screened corpora, verifies identifiers and supporting passages, follows citation chains, maps closest work, and records the search boundary.

### `crypto-paper-reader`

Extracts definitions, claims, assumptions, theorem/proof structure, reductions, security models, parameters, costs, evidence, limitations, and follow-up questions from one paper.

### `crypto-related-work-synthesis`

Builds taxonomies, historical development, claim matrices, tradeoff maps, closest-work comparisons, research gaps, and an evidence base for related-work writing.

### `crypto-novelty-check`

Adversarially tests decomposed contribution claims against verified prior art and priority evidence. It reports only novelty conclusions bounded by the documented search.

## Formal, Security, and Parameter Review

### `crypto-theorem-review`

Audits definitions, quantifiers, lemmas, theorems, game hops, reductions, runtime/loss, oracle access, aborts, probability accounting, edge cases, and dependency failures.

### `zkp-security-review`

Audits completeness, soundness, knowledge extraction, zero knowledge, simulation soundness, setup, Fiat–Shamir assumptions, transcript binding, composition, aggregation, recursion, folding, and implementation concerns.

### `lattice-parameter-audit`

Traces LWE/RLWE/MLWE/SIS-family assumptions and reductions into concrete parameters. Checks correctness/failure probabilities, attacks, estimator inputs and versions, cost models, memory, sensitivity, and implementation compatibility.

## Evidence and Publication

### `crypto-experiment-reproducibility`

Designs and audits benchmarks, estimators, proof checkers, code artifacts, datasets, environments, seeds, repetitions, negative results, and claim-to-command-to-output provenance.

### `crypto-paper-writing`

Builds contribution-led outlines and manuscript sections from verified claims and evidence. It maintains calibrated wording across proven, estimated, measured, reproduced, conjectured, planned, and unavailable results.

### `crypto-venue-paper-writing`

Rewrites a cryptography paper in the two places where it goes wrong: it compresses the abstract and the contribution list to corpus-calibrated caps (abstract words, build share, longest sentence, bullet count and length, block/abstract ratio, and shared 6-grams against the abstract) and expands the technical overview and the construction to corpus floors with mandatory constituents. It also budgets section mass and relocates rather than deletes, keeps concrete measured values out of construction and proof sections, de-names research-process vocabulary by adjudication rather than by hit count, runs an executable de-AI checklist, checks double-blind anonymity and the LNCS template, and reports a diagnosis with the measured number, the threshold, and a verdict for every region. It owns the cryptography/LNCS family and the shared corpus-calibrated rules the security skills invoke; it states no security-venue-specific rule.

### `ccs-writing-style`

Revises an ACM CCS, IEEE S&P, or NDSS paper for threat-model-first structure, calibrated attack/defense claims, the current page budget, double-blind wording, and adaptive-evaluation honesty. It owns the family-wide security-venue gates — abstract and contribution condensation, the two abstract-to-contribution overlap indices, the overview and design constituent checklists, the design-versus-analysis mass ratio, and concrete-value placement — and reports counts instead of judgements. The USENIX skill and the cryptography skill invoke these gates by name rather than restating them.

### `usenixsec-writing-style`

Drafts or revises USENIX Security prose with a load-bearing adversary statement, quantified claim calibration, the two policy-mandated sections (`Ethics considerations` and `Open science`) immediately before the References, the 13-page budget plus that extra page, the disclosure thread woven into the methodology, and a plain systems-security register. It adds the USENIX-only checks and measurement table and invokes the shared family gates from `ccs-writing-style`, holding no second copy of them.

### `crypto-paper-review`

Runs adversarial pre-review across fit, significance, novelty, correctness, security, parameters, evaluation, artifacts, ethics, clarity, and compliance. Findings are severity-ranked and routed to exact repair obligations.

## What the Full Suite Can Deliver

The three writing skills ship two dependency-free counting instruments alongside their rules, so the gates can be measured rather than asserted: `skills/crypto-venue-paper-writing/scripts/count_venue_gates.py` and `skills/ccs-writing-style/scripts/count_prose_gates.py`. Each reports a status (`measured` / `degenerate` / `unmatched`) per gate instead of a silent pass, and exits non-zero when a gate cannot be measured — `2` for a measurement failure, `1` for a failed verdict-path pass condition.

Every threshold in the three writing skills is cited to a frozen corpus with its sample size and basis inline, so a threshold can be checked without access to that corpus. The corpus paths quoted in the skills are provenance annotations into the authoring workspace, not links, and are not expected to resolve beside an installed copy.

Given an idea and access to appropriate sources/tools, the suite can produce:

- a research-state and claim/evidence ledger;
- a verified literature corpus and paper-reading records;
- a bounded novelty assessment and closest-work matrix;
- theorem, reduction, ZKP-security, and lattice-parameter audit reports;
- an experiment plan and reproducibility/artifact package;
- an evidence-supported paper draft;
- an adversarial internal review and revision routing;
- a submission-readiness package for accountable human review.

It cannot autonomously certify truth, global novelty, real-world security, ethics, authorship, reproducibility everywhere, venue acceptance, or permission to submit.
