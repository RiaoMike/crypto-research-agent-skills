# Changelog

All notable changes are documented here.

## Unreleased — 2026-11-24

Fixes found by a controlled end-to-end evaluation on a held-out security-venue paper
(read -> outline -> write -> blind review), plus two structural gaps the review surfaced.

- **Instrument contract.** `ccs-writing-style/scripts/count_prose_gates.py` now prints the
  measurement failure on stderr and exits **2** for "no heading matched" and for a malformed
  `--section` spec, matching its documented exit-code contract (previously
  `raise SystemExit(str)` returned exit 1). `--self-test` remains 47/47.
- **Repair-diff re-review.** `crypto-paper-writing/references/authoring-workflow.md` gains a
  mandatory repair-diff audit: every gate-driven repair emits a four-list diff (cite keys /
  formal statements, round counts and parameters / title-abstract claim wording / numbers),
  and a non-empty diff forces a `crypto-theorem-review` and a `crypto-paper-review` re-review
  with a required `regressions introduced` field. This closes the failure mode where a repair
  passed the gate while silently changing the theorem's round index.
- **Condensation may not strengthen a claim.** `ccs-writing-style/references/compression-and-expansion-gates.md`
  adds `Gate-Condense-Claim-Preservation` (modality, quantifiers, scope, and claim object
  preserved; delete/merge/downgrade only), and the abstract gate points to it.
  `crypto-venue-paper-writing/references/compression-rules.md` cites the same rule for the
  cryptography family. Observed defect: "commits once to the message" compressed to "never
  commits to the codeword" while the construction still commits codeword columns.
- **Section-order contract.** New `ccs-writing-style/references/section-order.md`: the
  CCS/S&P/NDSS default body order, the banned structure forms (Roadmap subsection, standalone
  numbered Open Problems, a central result named Claim, bare work-plan labels), and the
  conformance check to record before freeze. Wired into `ccs-writing-style/SKILL.md`.
- **Planning-ID scan.** `crypto-venue-paper-writing/references/de-ai-and-style.md` narrows the
  defined-label exemption: an inline `(A1)`-`(A4)` assumption list is a class-1 style finding
  even when defined, unless the label lives in a standard theorem-like environment; the grep
  checklist gains `\([A-Z][0-9]\)`.
- **De-AI freeze gate.** `authoring-workflow.md` Step 7 requires three freeze artifacts: the
  venue section-order conformance check, the de-AI grep output (hits and waivers), and named
  `assumption` environments.

Evidence: the evaluation workspace's `report/FINAL.md` section 14 and
`skill-optimization/APPLIED*.md`; raw gate transcripts in that workspace's
`submission/supplementary/instruments/`.

## 0.3.0 — 2026-09-17

Two opposite defects drove this release: the places that must be condensed (the abstract, the contribution list) were wordy, and the places that must be detailed (the technical overview, the concrete construction) were thin. Both are now decided by measured thresholds instead of by taste.

- Rewrite the compression and expansion rules of the three writing skills around a frozen writing-craft corpus: 62 tier-A cryptography papers (135 full LaTeX sources) and 35 security four-venue papers (25 read in full). Every threshold carries its corpus `file:line`, its sample size `n`, and its measurement basis inline. No threshold is chosen by taste, and where neither corpus measures a quantity the rule is stated qualitatively rather than with an invented number.
- Add `crypto-venue-paper-writing/references/compression-rules.md` and `expansion-rules.md`: abstract cap and build-share floor, contribution-list caps and the abstract-to-list 6-gram duplication metric, technical-overview floors and constituents, and the construction-to-analysis mass ratio with its band boundaries.
- Add `crypto-venue-paper-writing/references/section-budget.md` and `numeric-placement.md`: the largest-child share ceiling with move-not-delete relocation, and the rule that concrete measured values never sit in construction or proof sections.
- Add `crypto-venue-paper-writing/scripts/count_venue_gates.py`, the shipped counting instrument. It reports one status per gate (`measured` / `degenerate` / `unmatched`) rather than a silent pass, refuses to print a ratio band when a section's `direct` measurement is degenerate, and exits non-zero — `2` for measurement failure, `1` for a failed verdict-path pass condition — so "the guard fired but printed nothing" is detectable. Its `--self-test` runs 64 assertions.
- Add the shared security-venue gates to `ccs-writing-style/references/compression-and-expansion-gates.md`, together with `scripts/count_prose_gates.py` and `scripts/check_pointer_resolution.py`, which resolves gate names across owning files. `usenixsec-writing-style` invokes these by name instead of restating them, so no rule sentence exists in two places.
- Extend the family gates to IEEE S&P and NDSS, which share the CCS register and have no skill of their own; record that the four security venues do not differ significantly in abstract length, so no per-venue abstract cap is imposed.
- State the venue ownership boundary explicitly: `crypto-venue-paper-writing` owns the cryptography/LNCS family and the shared corpus-calibrated rules, the two style skills own the security-venue register.

## 0.2.0 — 2026-09-07

- Add `crypto-venue-paper-writing`: structure, abstract compression, and de-AI rewriting for top cryptography and security venues, built from revision feedback on real CRYPTO/LNCS manuscripts.
- Add `ccs-writing-style` and `usenixsec-writing-style`: venue-specific threat-model, claim-calibration, and page-budget guidance adapted from the MIT-licensed Awesome-Journal-Skills collection.
- Update the corpus test, capability map, and bilingual READMEs for the three new skills.

## 0.1.1 — 2026-08-31

- Prevent recursive skill discovery from treating the meta-skill's two structural examples as independently installed skills.
- Add a regression test that permits `SKILL.md` only at the top level of each canonical skill directory.

## 0.1.0 — 2026-08-31

- Publish `crypto-research-skill-creator` and twelve cryptography research skills.
- Add Codex, Claude Code, generic Agent Skills, and custom DeepSeek-harness installation paths.
- Add a dependency-free validator and safe cross-platform installer.
- Add static evaluation scenarios for every research skill and executable tests for the meta-skill.
- Add bilingual project documentation and top-venue research-integrity boundaries.

