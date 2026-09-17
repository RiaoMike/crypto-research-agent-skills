---
name: ccs-writing-style
description: Use when revising an ACM CCS paper for a precise threat model, calibrated attack/defense claims, the CCS page budget, double-blind wording, adaptive-evaluation honesty, abstract and contribution-list condensation, technical-overview and scheme-section expansion, and the security house style expected by an adversarial SIGSAC program committee; also covers IEEE S&P and NDSS submissions, which share the same security-venue register and corpus-calibrated rules and have no dedicated skill of their own.
---

# CCS Writing Style

A CCS paper must let an adversarial reviewer locate every claim against a named adversary and checked evidence. Adapted from the CCS writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Evidence base for the numeric gates

Every number in the condensation gates and the expansion gates below is measured, not chosen. Two corpora back them:

- Security four-venue corpus: 35 papers (IEEE S&P 4 / ACM CCS 5 / USENIX Security 18 / NDSS 8), full texts on disk, 25 read in full. Quantified tables Q1–Q9 with sample sizes, extraction basis, and re-computation commands: `skills-work/corpus/security/statistics.md`.
- Cryptography three-venue corpus: 62 tier-A papers plus 135 full LaTeX sources. `skills-work/corpus/crypto/statistics.md`, whose `§Bases` section defines every unit used here.

**Provenance of the citations in this skill.** Every `file:line` citation below is a provenance annotation rather than a link: it points at the corpus snapshot inside the authoring workspace (`skills-work/`), and it is not expected to resolve beside an installed copy. The snapshots are the security four-venue corpus (35 papers, 25 read in full) and the cryptography tier-A corpus (62 papers); each threshold this skill states is self-contained, carrying its own sample size and measurement basis inline so it can be checked without following any path.

Rule this skill follows: a threshold is quoted with its source file, its line, its sample size `n`, and its basis. Where the two corpora disagree, the corpus governs and the manuscript in front of you is not a constant. Where neither corpus measures the quantity, the rule is written qualitatively with no number — an invented number is a defect, not a default.

Measured facts that justify each gate, with anchors:

| Quantity | Value (basis, sample) | Anchor |
|---|---|---|
| Abstract words, security four venues | median **220**, q1 173, q3 241, min 116, max 362 (n=35) | `corpus/security/statistics.md:31` |
| Abstract sentences | median **9**, q1 8, q3 11 (n=35) | `corpus/security/statistics.md:32` |
| Mean words per abstract sentence | **24.1** (n=35) | `corpus/security/statistics.md:33` |
| Venue split of abstract length | S&P 214 / CCS 205 / USENIX 212 / NDSS 227.5 — **no significant difference** | `corpus/security/statistics.md:50` |
| Contribution items | median **5**, q1 3, q3 6, min 1, max 10 (n=22) | `corpus/security/statistics.md:58` |
| Words per contribution item | median **72**, q1 22, q3 150, min 7, max 574 (n=22) | `corpus/security/statistics.md:59` |
| Items carrying a number | median **66.7%** (n=22) | `corpus/security/statistics.md:60` |
| Contributions ↔ abstract, word-bag Jaccard | median **0.201**, max 0.309 (n=22) | `corpus/security/statistics.md:61` |
| Contributions ↔ abstract, trigram Jaccard | median **0.019**, max 0.038 (n=22) | `corpus/security/statistics.md:62` |
| Why two overlap indices | word-bag catches a rewritten abstract; trigrams catch reused sentences (both at their corpus medians) | `corpus/security/statistics.md:67` |
| Abstract length, four-venue medians | S&P 214 / CCS 205 / USENIX 212 / NDSS 227.5 (n=35, words), ranges fully overlapping — a null finding, so no per-venue cap | `corpus/security/statistics.md:213` |
| Standalone overview section | S&P 100% / CCS 100% / NDSS 100% / **USENIX 56%** (n=35, section audit) | `corpus/security/statistics.md:216` |
| Standalone threat-model section | S&P 25% / **CCS 60%** / USENIX 28% / NDSS 88% (n=35, section audit) | `corpus/security/statistics.md:217` |
| Body page limits, official CFP | S&P 13 (+5) / **CCS 12** excluding refs / USENIX 13 (+1) / NDSS 15 all-inclusive (policy, per-cycle) | `corpus/security/statistics.md:220` |
| Abstract process narration | **0 of 35** papers narrate research process in the abstract | `corpus/security/statistics.md:48` |
| Technical overview present | **27 of 35 (77%)**; CCS **5 of 5** | `corpus/security/statistics.md:85` |
| Technical overview size | median **1535.5** words, min 596, q1 854 (n=20) | `corpus/security/statistics.md:92` |
| Overview size, CCS only | median **1058** words (n=5) | `corpus/security/statistics.md:219` |
| Overview internal components | 5 named components, each with a corpus instance | `corpus/security/statistics.md:104` |
| Scheme/construction section | median **3481** words (n=35); CCS median 3481 (n=5) | `corpus/security/statistics.md:119` |
| Scheme section components | 4 regular-expression-counted classes at 10–19 of 25 papers | `corpus/security/statistics.md:131` |
| Threat/security-model section | median **843** words, q1 769, q3 1041 (n=16) | `corpus/security/statistics.md:157` |
| Threat-model section, CCS only | standalone section in **3 of 5** papers | `corpus/security/statistics.md:152` |
| Security-analysis membership of a thin design | floor **0.44** = q1 of construction/analysis words, direct basis (n=10) | `corpus/crypto/statistics.md:285` |
| Design word share of body | **2663/13800 ≈ 0.19**; evaluation 1291 words (n=32) | `corpus/security/statistics.md:121` |
| Overview size, crypto venues | median **3423** words (n=18) — the crypto-venue comparison, not a CCS target | `corpus/crypto/statistics.md:239` |
| Large section held by its largest child | median share **0.491** (n=561) | `corpus/crypto/statistics.md:330` |

## Scope

In scope: threat-model-first structure and wording; first-page security contribution framing; claim-to-evidence pairing (proof, measurement, exploit, or cost); abstract and contribution-list condensation to the measured bounds above; technical-overview and scheme-section expansion against the constituent checklists; page-budget compression for the current limit of the venue in hand (CCS, IEEE S&P, or NDSS); double-blind anonymization of self-citations, tool names, acknowledgments, and artifacts; adaptive-evaluation honesty for defenses; sentence-level rewrites that remove overclaiming, marketing adjectives, and research-process narration; concrete-value placement; and an output diagnosis format for revision.

Out of scope: inventing attacks, defenses, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization. Writing-style rules for the cryptography venues (CRYPTO, EUROCRYPT, ASIACRYPT, LNCS) are owned by the `crypto-venue-paper-writing` skill; this skill owns the security-venue (CCS, USENIX Security, NDSS, IEEE S&P) form of them. Where the two would state the same rule, this skill states it once and points there.

### Venue mapping — what is shared across the four security venues, and what is CCS-only

This skill triggers for **ACM CCS, IEEE S&P, and NDSS**. The `usenixsec-writing-style` skill owns the USENIX Security form, including the two sections that venue mandates. IEEE S&P and NDSS have no dedicated skill, so this one carries their shared form — and that makes the split below load-bearing rather than cosmetic: a triggered S&P or NDSS run must not silently inherit a rule that was calibrated for CCS.

| Applies to every security venue this skill covers | CCS-only |
|---|---|
| The counted condensation gates (abstract, contribution list, contributions-versus-threat-model duplication, deletion list) | The 12-page body limit excluding bibliography, appendices, and supplementary material |
| The counted expansion gates (overview components, design constituents, design-versus-analysis ratio, value placement) | The IRB / responsible-disclosure compliance statement obligation |
| Threat-model precision: explicit and locatable, capability list in prose, one statement of the adversary (the four-venue standalone shares are S&P 25% / CCS 60% / USENIX 28% / NDSS 88%, `corpus/security/statistics.md:217`) | The standalone-section default, which follows CCS's 60% — the S&P and NDSS shares are 25% and 88%, so for those venues the placement is the author's call under the same precision requirement |
| Adaptive-attack honesty, caption discipline, de-identification, the deletion lists, and the register | The CCS page-budget snapshot procedure; S&P and NDSS have their own limits, so read their own current call |

The page budget and the ethics/disclosure obligation for each venue are read from that venue's own official call — archived per venue under `skills-work/corpus/security/raw/` (CCS 12 pages excluding references, S&P 13 pages plus 5 for references and appendices, NDSS 15 pages all-inclusive, USENIX 13 plus one ethics and open-science page; digest at `corpus/security/statistics.md:220`). Never carry one venue's number to another, and never measure an ePrint author version against any of them (`corpus/security/statistics.md:21`).

## Required Inputs

- current official call for papers and template of the venue in hand — CCS, IEEE S&P, or NDSS here; page limit, anonymity, ethics, AI-disclosure, artifact policy;
- manuscript draft or section under revision;
- stated threat model, or the raw security claims to be given one;
- evaluation data or attack demonstrations that claims must be calibrated against.

## Success Criteria

- The security contribution is on the first page: problem, attacker, gap, mechanism, evidence.
- The abstract passes every condensation gate: at most **220 words**, at most **9 sentences**, mean sentence length at most the corpus median **24.1 words**, one paragraph that names the built artifact or mechanism, no research-process narration, no marketing adjective from the checklist, and no contribution sentence reused verbatim.
- The contributions list passes its own gates: at most **5** items normally and never more than **10**, at most **72 words** per item, at most **250 words** total, word-bag Jaccard against the abstract at most **0.20** and trigram Jaccard at most **0.019**, and no duplicated span left with the disposition unstated.
- The contributions list and the threat model are not the same text: their word-bag Jaccard is at most 0.20, and conversely every security goal the paper promises appears in the threat model as a statement of what the adversary may do.
- The technical overview is a named subsection with at least **596 words** (the corpus minimum; q1 is 854) and carries all five required components; the scheme section carries at least **five** required components and is not thinner than **0.44** of the analysis section by word count.
- The threat model is explicit and early, names attacker capabilities, knowledge, position, and goal once in prose, and every attack/defense step stays inside those capabilities.
- Every security claim is paired with proof, measurement, exploit demonstration, or a cost number; nothing reads as marketing.
- Concrete measured values appear only in the sections allowed to carry them; theory and construction text carries symbolic or asymptotic expressions.
- Claims survive an adversarial pass: no overstated exploitability, no "practical" claims beyond the tested environment and versions, adaptive defenses state the attacker they were tested against.
- Double-blind wording holds in self-citations, tool names, acknowledgments, and artifact descriptions.
- The body fits the current page budget of the venue in hand — CCS 12 pages excluding bibliography and appendices, IEEE S&P 13 plus 5, NDSS 15 all-inclusive, each read from that venue's own call — with the core argument readable without the appendix.
- No AI-flavor prose remains (see the `crypto-venue-paper-writing` skill's de-AI checklist for the grep-level rules).

## Condensation and expansion gates

These gates are procedural, not advisory. Every threshold cites its corpus anchor, sample size, and basis. Run them as counts; a verdict adjective is not a result.

### Compression gates

**Gate-Condense-Abstract — Abstract cap and allocation.**
Text: the abstract; cap 220 words after condensation (basis: words of the extracted text, n=35, `corpus/security/statistics.md:31`; q1 is 173, so 220 is the corpus median and the corpus's own long tail reaches 362 — the cap is a target, and any abstract between the cap and 250 words needs a recorded reason).
Check: count words, sentences, and the words in the longest sentence; label each paragraph by the move it performs (context / gap / build / result); report the four numbers plus the per-paragraph allocation.
Pass: words ≤ 220, sentences ≤ 9, longest sentence ≤ 40 (crypto-corpus median), mean sentence length ≤ the corpus median of 24.1 words, and at least one paragraph performs the build move by naming the artifact, protocol, or mechanism this paper contributes.
Fail: any count over the bound with no recorded reason; an abstract whose every paragraph reports analysis outcomes while the construction this venue expects gets no naming paragraph — this is the exact shape of the reported defect (a 247-word abstract with 66% of its words in analysis paragraphs) and such an abstract passes a bare length cap, so the length cap alone never closes this gate.

**Gate-Condense-Contributions — Contributions cap and duplication metric.**
Text: the contribution block in the introduction.
Check: count items; count words per item and in total; compute two metrics against the abstract — the Jaccard index over the deduplicated word sets of the two texts, and the Jaccard index over the sets of adjacent word trigrams — and list every shared trigram with the two line numbers it appears on.
Pass: items ≤ 5 (≤ 10 absolute), words per item ≤ 72 with at most one item above 150, list ≤ 250 words; word-bag Jaccard ≤ 0.20 and trigram Jaccard ≤ 0.019 (both corpus medians, n=22, `corpus/security/statistics.md:61-62`).
Fail: an item that only restates an abstract sentence with the words rearranged; a total over the cap with no reported number; a list at 0.30 Jaccard against its own abstract (the corpus maximum) left in place. Two items over 100 words each with the rest below 10 words is also a fail — the measured distribution's quartiles are 22 and 150, so the item lengths must be deliberate, not accidental.

**Gate-Condense-Contributions-vs-Threat-Model — Contribution list versus threat model.**
Text: the contribution block and the threat/security-model section.
Check: compute the same word-bag Jaccard between the two spans; then list, for each promised security goal in the contributions, the threat-model sentence that states what the adversary may do.
Pass: Jaccard ≤ 0.20; each promised goal has a threat-model counterpart; the threat model adds at least one capability, assumption, or explicit non-goal that the contributions do not state.
Fail: a threat model that is the contributions list with a heading — the corpus instance is a threat-model paragraph that opens by re-listing the parties the contributions already listed, so the two texts do the same work in two places. Restating the adversary is not the failure; restating it *only* there, with no capability the reader did not already have, is.

**Gate-Condense-Deletion-List — Marketing adjectives and process narration.**
Text: the abstract, contributions, introduction, and every claim sentence.
Check: grep for the marketing adjectives (`highly effective`, `trivial`, `negligible`, `completely`, `significantly`, `practical`, `efficient`, `robust`, `scalable`, `guarantees`, `breakthrough`, `seamless`, `powerful`, `state-of-the-art` without a companion number) and for research-process narration (stage identifiers, round labels, letter-number identifiers such as a `C`-prefixed contribution tag, `ref`-prefixed citation keys, attempt counts, abandoned-design inventories, "we first tried … then").
Pass: every surviving adjective carries a measurement, a scope, or is deleted; zero process-narration matches outside a sentence that quotes the anti-pattern in order to forbid it (n=35, `corpus/security/statistics.md:48` — the corpus contains 0 instances of process narration in abstracts).
Fail: one adjective left with no number and no recorded waiver; one identifier from an internal planning register left as if it were a paper concept. The plan's labels are not the paper's names.

### Expansion gates

**Gate-Expand-Overview — Technical overview floor and components.**
Text: the technical-overview subsection.
Check: count its words and lines; report whether it is a standalone top-level section or a named subsection of the introduction; check the checklist below, component by component, and report each as present with its line, or absent.
Checklist (each item anchored in the corpus):
1. one or two sentences of intuition stating the goal in plain terms;
2. a mechanism sentence explaining *why* the construction or attack works, not only what it is;
3. one named sub-block per subproblem, its title naming the subproblem it solves (median 5 named components across the corpus);
4. a forward reference from each sub-block to the section that gives the formal detail;
5. an early statement of the cost, leakage, or assumption the mechanism buys its result with.

Pass: at least **596 words** (the corpus minimum for a standalone overview, n=20, `corpus/security/statistics.md:92`; the first quartile is 854), all five components present, and at least three named sub-blocks.
Fail: a component list that answers four of five; an overview that is only a table of contents ("Section 3 presents X, Section 4 proves Y") with no mechanism sentence; an 1100-word overview with one block — length without components does not pass. Note the venue contrast: CCS papers in the corpus present an overview function in 5 of 5 cases, so for CCS this gate always applies and never resolves to "this venue does not use overviews".

**Gate-Expand-Scheme — Scheme-section floor and components.**
Text: the design/construction/protocol section — the section that describes what is built, whatever its title, since 69% of tier-A papers (43 of 62) have no section whose title contains the word "Construction" (`corpus/crypto/statistics.md:112`) and only 46.8% of tier-A papers have any construction-role body section at all (`corpus/crypto/statistics.md:291`); a title-keyed rule misses the rest.
Check: count its words on a declared basis; check the constituents below; report each as present with its line or absent.
Required constituents (regular-expression-counted classes, n=25 deep reads, `corpus/security/statistics.md:131-138`, with the crypto-venue confirmation at `corpus/crypto/statistics.md:300`):
1. a step ordering that says in what order the protocol or attack proceeds (20 of 25 papers; the single highest-hit constituent);
2. a named object, relation, or function defined once and reused, instead of re-deriving the same condition inline (19 of 25);
3. a complexity, communication, or cost expression (17 of 25);
4. the reason for the parameter, size, or field choice (15 of 25);
5. a protocol or algorithm box, or a figure that carries the message flow (10 of 25 for a box; more once figures that carry flow are counted).

Pass: all five present, and at least one mechanism-explanation sentence per mechanism (the causal sentence class the corpus has in the deep reads but which a phrase-level count under-counts — do not use the phrase count as the floor).
Fail: a scheme section whose description is a single synthesis sentence plus parameters; a section with the boxes but no step ordering. Where a required constituent genuinely does not apply, the report must name the component and the reason; silence is a fail.

**Reading the numbers inside this gate — a diagnosis, not a second gate.** The pass/fail decision for the scheme section is the one above; the mass figures are reported alongside it. Count the scheme section, the security-analysis section and the evaluation section on one declared basis, then read:
Text: the scheme section, the security-analysis section, and the evaluation section.
Check: count words of each on one declared basis; compute scheme/analysis; compute the scheme section's share of the body.
Reading: a scheme/analysis ratio at or above **0.44** (q1 of the construction/analysis word ratio, direct basis, n=10, `corpus/crypto/statistics.md:285`) and a scheme section at or above **2663** words on the same basis are within the corpus distribution; below either, the section is described as thin and the missing constituents are named. The reported defect shape is 18 and 81 lines of protocol and construction against 172 lines of analysis, and this reading is the instrument that measures it — the ratio and the constituent checklist remain independent, so a ratio above the floor with three constituents missing still fails the gate above.
Fail (as a reading of the gate above, not a separate verdict): a scheme section clearly thinner than the sections about it, under either floor, with the missing scheme-section constituents named.

**Gate-Expand-Value-Placement — Concrete-value placement.**
Text: every section; specifically the design and proof regions versus the evaluation, parameters, and implementation regions.
Check: scan the design and analysis regions for numeric literals in the class of measured quantities (long decimal expansions, exact success or failure probabilities, bit counts and timings), and scan the evaluation region for symbolic-only statements that should carry the measured value.
Pass: measured values live in the evaluation, parameter, and implementation sections; the design and proof regions carry symbolic or asymptotic expressions; any measured value that belongs elsewhere is *relocated with its digits and its provenance*, never rounded away, never deleted, and the receiving section states where it came from.
Fail: a concrete success probability sitting in a construction paragraph with no location statement; a value deleted or replaced by an adjective "in the interest of style". The cheapest way to look detailed is to pour measured numbers into a construction — that recreates a known defect class, and this gate exists to stop it.

### Venue-specific gates

**Gate-Venue-Threat-Model — Threat-model placement and size.** The requirement is that the adversary statement is **explicit and locatable** — stated once, in one place, in prose — not that it owns a heading. Standalone-section share is venue-dependent: S&P 25% / **CCS 60%** / USENIX 28% / NDSS 88% (`corpus/security/statistics.md:217`; the corpus's own CCS pair rows are at `:152`). A standalone section is the CCS default, so the gate is: a standalone section unless a recorded reason says why the adversary statement lives inside the system overview, and a draft that satisfies every requirement below from inside the system overview has not failed. When standalone, its size target is the corpus median of **843 words** (n=16, q1 769, q3 1041, `corpus/security/statistics.md:157`). The internal order is fixed by the corpus: parties and trust assumptions (who may collude) → adversary capabilities (what it sees, changes, and when it decides) → security goals and explicit non-goals. Capability lists are written as assumption-plus-decidable-statement prose, not as a table (`corpus/security/statistics.md:165`). Fail: a threat model that is a bulleted capability table with no trust assumptions, or one that drifts between model and evaluation.

**Gate-Venue-Disclosure-Ethics — Disclosure and ethics statement.** ACM CCS '24 requires that authors convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed, with the body limit at 12 pages excluding bibliography, appendices, and supplementary material (`corpus/security/statistics.md:177`). Gate: the paper states IRB status and the responsible-disclosure action, or says explicitly that neither applies and why, at the point the reader needs it. This is a policy obligation, not a corpus-derived rule — only 2 of 35 corpus papers contain the word "ethic" and 0 of 35 carry a disclosure narrative (`corpus/security/statistics.md:182-183`), so the corpus cannot set its size. Fail: an ethics or disclosure statement added as a detached closing sentence with no relation to the experiment it covers.

**Gate-Venue-Page-Budget — Page budget and policy snapshot.** The CCS '24 limit is 12 pages excluding bibliography, marked appendices, and supplementary material (`corpus/security/statistics.md:177`). Gate: record a dated policy snapshot quoting the current call, check the body against it, and route overflow to appendices with forward references rather than by tightening spacing or margins. Never assert the limit from memory: this number is the CCS '24 cycle's, and the call for the submission cycle in hand governs. Fail: a budget report without a dated snapshot; a compression plan that shrinks section mass by template tricks.

**Gate-Venue-Adaptive-Attack — Adaptive-attack honesty.** Adaptive-attack discussion appears in only 3 of 35 corpus papers (`corpus/security/statistics.md:185`), the fewest of any posture the corpus measures — reviewers look for the absence. Gate: a defense evaluated against the attack it was designed to stop is reported as a standing limitation, and any adaptive evaluation names the adaptive attacker it used.

**Gate-Venue-Subsection-Share — Subsection share and move-not-delete relocation.** No child subsection should hold more than about **0.6** of its parent section (median largest-child share 0.491, q3 0.607, n=561, `corpus/crypto/statistics.md:330`; treat 0.6 as a diagnostic flag, not a hard gate — the median parent is already at half). Relocatable material is defined as verification records, review or process anecdotes, superseded metric tables, and measurement tables that no longer carry the argument. Relocation is *move, never delete*: every claim keeps its status wording and its provenance where it lands. Fail: "rebalance by deleting the extra subsection"; a relocation that drops a status label off a claim.

## Failure Modes

- No threat model or a shifting one: stop and draft the adversary statement before revising claims.
- Attack/defense claim without evidence anchor: expose it and scope the claim to what was measured or demonstrated.
- Abstract over the condensation caps, or under them while spending most of its words on analysis outcomes: run the abstract count instead of judging by feel.
- Contributions that restate the abstract, or a threat model that restates the contributions: run the contributions counts and report the two Jaccard values.
- Technical overview present but below the floor or missing components: run the overview gate and name each absent component with its line.
- Scheme section thinner than the sections around it, or missing scheme-section constituents: run both scheme gates together; a ratio inside the floor with constituents missing is still a fail.
- Measured values inside design or proof text, or symbolic-only evaluation numbers: run the value-placement gate and relocate rather than delete.
- CCS page limit may have changed since training: verify the current official call before any compression claim.
- De-identification gap: fix author names, institution, and identifying repository references before the format pass.
- Evaluation only against the designed-for attack: report it as a standing limitation, not as strength.

## Workflow

1. Verify the current official call and template of the venue in hand (CCS, IEEE S&P, or NDSS); record a dated policy snapshot before any budget statement.
2. Read the draft and produce a diagnosis: clear / under-specified threat model / overclaimed / overloaded / verbose where it must be dense / thin where it must be dense. State the target venue first, because the page budget and the ethics obligation that follow are read from that venue's call and not from CCS by default.
3. Condensation count pass — run the counts over the abstract and the contributions and report the numbers: abstract words, sentences, longest sentence, per-paragraph move allocation; contribution item count, words per item, list total; contributions-versus-abstract word-bag and trigram Jaccard; contributions-versus-threat-model Jaccard. Report the before and after numbers together.
4. Fix the threat model and the first-page framing.
5. Expansion count pass — run the gates over the overview and the scheme section and report each component as present or absent: overview words and location, scheme words, scheme/analysis ratio, scheme share of body, and every overview and scheme component with its line.
6. Rewrite claims against evidence: pair each claim with proof, measurement, exploit, or cost; strip the adjectives on the deletion list and the process narration.
7. Compress to the target venue's page budget — never to another venue's — moving transcripts, extra measurements, and full proofs to appendices with forward references.
8. Run the double-blind scan and the de-AI grep checklist; fix every hit or record a waiver.
9. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: writing diagnosis; the counted gate report set — abstract words/sentences/longest sentence/allocation, contribution items/words/Jaccard values, overview words and components, scheme words and components, scheme-versus-analysis ratio with its declared basis; first-page fix; claim-discipline table (claim mapped to proof/measurement/exploit/cost); compression cuts (move/delete/merge); anonymity edits; page-budget report; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/compression-and-expansion-gates.md` | The condensation and expansion gates with corpus anchors, sample sizes, bases, the counting method, and the CCS-versus-USENIX rule differences |
| `references/sentence-rewrites.md` | Draft-pattern to CCS-safe-rewrite table, the deletion lists, and the compression vignette |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
| `scripts/count_prose_gates.py` | The counting instrument for every gate above: the tokenizer it used is pinned and printed with its output, and a pattern that matches nothing is reported as degenerate rather than zeroed |
| `scripts/check_pointer_resolution.py` | The installable pointer resolver: ships with this skill so the check still exists after installation to `~/.dsh/skills`, where `skills-work/tools/` does not. Run `python3 scripts/check_pointer_resolution.py` after a gate is renamed or a pointer file changes the name it uses — expected `RESULT: PASS (nn/nn gate names resolve)`, exit 0, with a `skip` line naming every mention it deliberately did not judge. `--self-test` runs 13 cases that prove both directions (a warning sentence is a mention; the same name on an instruction line still fails) |
| Pointer resolvability in the repository | The shared checker `python3 skills-work/tools/rule-trace-check.py --fail-on-gap` (C15) enforces the same rule inside this workspace. Expected: `RESULT: PASS [no FAIL]`, exit 0. The two instruments must agree on the historical defect; the cross-check is recorded in `skills-work/reports/author-style-notes.md` |
