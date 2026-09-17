---
name: usenixsec-writing-style
description: Use when drafting or revising prose for a USENIX Security Symposium paper — threat-model-first structure, calibrated security claims, disclosure narrative woven into the text, the current USENIX page budget and its ethics and open-science sections, abstract and contribution-list condensation, technical-overview and design-section expansion, and the plain systems-security register this program committee rewards.
---

# USENIX Security Writing Style

A USENIX Security paper argues like an engineer under oath: state what the adversary can do, show what you built or broke, measure it honestly, and say plainly what does not follow. Adapted from the USENIX writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Evidence base, and where the shared gates live

### Provenance of the citations in this skill

Every `file:line` citation in this skill is a **provenance annotation, not a link**: the paths point at the corpus snapshot inside the authoring workspace (`skills-work/`), and they are not expected to resolve beside an installed copy of this skill. The snapshot behind them is the security four-venue corpus — 35 papers, 25 of them read in full — plus, where a cross-family comparison is made, the 62 tier-A cryptography papers. Every threshold this skill states is self-contained: it carries its sample size `n` and its measurement basis inline, so a reader can check or recompute it without following any path.

### USENIX-specific measurements

These are the numbers that decide this skill's four own rules. Each is measured, and carries its basis and sample inline. All are drawn from the security four-venue corpus (`skills-work/corpus/security/statistics.md`).

| Quantity | Value (basis, sample) | Anchor |
|---|---|---|
| Standalone overview section | **USENIX 56%** (10 of 18 papers, section audit) — the embedded form is permitted here | `corpus/security/statistics.md:84`, `:216` |
| Standalone threat-model section | **USENIX 28%** (5 of 18 papers, section audit) — second-lowest of the four venues | `corpus/security/statistics.md:153`, `:217` |
| Threat-model section size, when standalone | median **843** words (q1 769, q3 1041, n=16, words) | `corpus/security/statistics.md:157` |
| Body page limit | **13** pages plus one for the two mandated sections; 14-page ceiling for a major revision (policy, per cycle) | `corpus/security/statistics.md:175` |
| Ethics and open-science obligation | **two titled sections required**, immediately before the References (policy, not corpus-derived: 2 of 35 papers mention ethics) | `corpus/security/statistics.md:182` |
| Adaptive-attack posture in the literature | **3 of 35** papers discuss it — the absence is what reviewers notice | `corpus/security/statistics.md:185` |

### The shared gates are owned elsewhere

The family-wide security-venue gates — the abstract and contribution counts, the two overlap indices, the deletion lists, the threat-model precision requirement, the overview and design constituent checklists, the design-versus-analysis mass ratio and the value-placement rule — are owned by **`ccs-writing-style`**, in that skill's `references/compression-and-expansion-gates.md`, and are invoked from there by name. They are not restated here, and this skill holds no second copy of them. The rewrite tables live in the same skill's `references/sentence-rewrites.md`; the counting instrument and its printed basis are documented with the gates.

This is the doctrine both skills publish: a rule is stated once and pointed at. The measurements above and the shared gates' evidence tables may quote the same corpus lines — facts are shared, rule sentences are not.


## Scope

In scope: adversary-first structure and wording; quantified calibration of every strong claim; the two policy-mandated sections and their placement; page-budget planning against the current call; the permitted embedded overview form; the disclosure thread woven into the methodology and the vulnerability discussion; plain systems-English register; caption discipline; self-anonymization at submission time; and the revision passes that check adversary consistency and calibration.

Out of scope: inventing systems, attacks, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization. The family-wide security-venue gates belong to `ccs-writing-style` and are invoked from there, not restated here. The cryptography and LNCS family belongs to `crypto-venue-paper-writing`.

## Required Inputs

- the current USENIX Security official call for papers and template (page budget, appendices, ethics, AI-disclosure, artifact policy);
- manuscript draft or section under revision;
- the stated adversary or the raw security claims to be given one;
- measurement data or attack demonstrations that claims must be calibrated against.

## Success Criteria

- Every claim sits relative to a named adversary, and the evaluation never assumes a stronger or weaker attacker than the stated model grants.
- The abstract, contribution list, overview and design sections pass the family gates invoked from `ccs-writing-style`, with the counts reported rather than judged.
- The body carries a section titled "Ethics considerations" and a section titled "Open science", each immediately preceding the References, and neither was carried over from a previous cycle's wording.
- The body fits the current USENIX limit — 13 pages plus the extra page for those two sections — under the unaltered official template, with no spacing or margin tricks.
- The overview function is present in one of the two permitted forms and carries the full constituent checklist.
- The disclosure thread states rate limits and opt-out handling in the methodology, and when and how each flaw was reported at the point it is introduced.
- Strong verbs carry their measurement, non-goals are named as concretely as goals, and figures read on their own.
- No AI-flavor prose remains (the de-AI checklist is owned by `crypto-venue-paper-writing`).

## USENIX-specific checks

The shared gates are invoked from `ccs-writing-style`; what follows are the checks this skill owns, each USENIX-only. Their evidence is in the table above, and their detail sections are in [compression-and-expansion-gates.md](references/compression-and-expansion-gates.md) and [section-budget.md](references/section-budget.md).

- **Adversary statement.** Stated once, in one place, in prose — parties and trust assumptions, then capabilities, then what is not guaranteed. Placement is the author's choice: 28% of corpus papers give it its own section, second-lowest of the four venues. A draft that states it inside the system overview and grants every capability the evaluation uses has not failed; a draft whose model drifts from the evaluation has, wherever the heading sits.
- **Two mandated sections.** A section titled "Ethics considerations" and a section titled "Open science", each immediately preceding the References, in the main body or in the extra page the policy provides. This is a policy obligation, verified against the current call, and it is not to be sized from the literature.
- **Budget.** 13 body pages plus one for those two sections. Read the current call and date the snapshot; never compress to a sibling venue's limit and never measure an author's ePrint copy against any limit.
- **Overview form.** Either an independent section or an overview subsection or named paragraph inside the introduction — 56% of corpus papers use the independent section, so the embedded form is permitted here and the constituent checklist still binds wherever the overview lives.
- **Disclosure narrative.** Rate limits and opt-out handling in the scan methodology paragraph; when and how a flaw was reported at the point the flaw is introduced.
- **Adaptive posture.** A defense measured only against the attack it was designed to stop is a standing limitation, and 3 of 35 corpus papers discuss adaptive attackers at all — the absence is what a reviewer notices.
- **Subsection share.** The family gate's diagnostic flag, with relocation that moves material and its claim-status wording rather than deleting it.

## Failure Modes

- Threat model missing or shifting between model and evaluation: stop and reconcile before revising prose.
- Abstract or contributions over their measured bounds, or under them while most words report analysis: run the condensation counts instead of judging by feel.
- Contributions that restate the abstract, or a threat model that restates the contributions: report the two Jaccard values and the shared spans with their lines.
- Technical overview missing its components at USENIX: the embedded form is allowed, the components are not optional — run the overview gate and name each absent component.
- Design section thinner than its analysis section, or missing required constituents: run both expansion gates; passing one does not excuse the other.
- Marketing or false modesty: rewrite with quantified hedging; a real result buried in modesty is as damaging as an overclaim.
- Live harm potential described without a responsible-conduct thread: add the disclosure narrative at the point of need.
- Ethics or open-science section missing, placed before the references incorrectly, or carried over from a previous cycle's wording: read the current call and fix the placement.
- USENIX page budget or template may have changed since training: verify the current official call before any budget claim.
- De-identification gap: anonymize names publicly attached to the group at submission time.

## Workflow

1. Verify the current USENIX call and template; record a dated policy snapshot, including the ethics and open-science section requirements and the page budget.
2. Fix the threat model and non-goals early (a standalone section, the system overview, or the background, as the draft's structure allows); state the measurement vantage and validity.
3. Condensation count pass — run the counts over the abstract and the contributions and report the numbers: abstract words, sentences, longest sentence, per-paragraph allocation; contribution items, words per item, list total; contributions-versus-abstract word-bag and trigram Jaccard; contributions-versus-threat-model Jaccard. Report before and after numbers together.
4. Expansion count pass — run the gates over the overview and the design section and report each component present with its line or absent: overview words and location, design words, design/analysis ratio with its basis, design share of the body.
5. Write or revise against a per-section page budget; move overflow to appendices with forward references, never by template tricks.
6. Calibrate every strong claim: hunt the adjective list and attach numbers or delete; strip process narration and planning-register identifiers.
7. Weave the disclosure narrative into the methodology and the vulnerability discussion.
8. Check the ethics and open-science sections exist, are titled as the policy requires, and sit immediately before the references.
9. Run the adversary-consistency pass, calibration pass, cold-reader pass, and caption pass.
10. Run the de-AI grep checklist; fix every hit or record a waiver.
11. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: threat-model precision verdict and evaluation-consistency check; the counted gate report — abstract words/sentences/longest sentence/allocation, contribution items/words/Jaccard values, overview words and components, design words and constituents, design-versus-analysis ratio with its declared basis; calibrated claim table with rewrites; disclosure-thread report (present at point of need, or gaps); ethics and open-science section placement check; per-section page usage versus budget with overflow routing; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/compression-and-expansion-gates.md` | The counting method, the threshold table with corpus anchors and sample sizes, the condensation and expansion gates, and the CCS-versus-USENIX differences |
| `references/section-budget.md` | Page budget table, calibration examples, register and revision-pass notes, the mandatory ethics and open-science sections |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
