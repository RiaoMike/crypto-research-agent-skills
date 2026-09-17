---
name: crypto-venue-paper-writing
description: Use when drafting, restructuring, or polishing a cryptography paper for a named top venue (CRYPTO, EUROCRYPT, ASIACRYPT, IEEE S&P, ACM CCS, USENIX Security, NDSS) or for CRYPTO/LNCS-style submission, including corpus-calibrated compression of the abstract and contribution list, mandatory elaboration of the technical overview and construction sections, section-mass budgeting, numeric placement, de-naming and de-AI rewriting, double-blind compliance, and format checks.
---

# Crypto Venue Paper Writing

Two defects drive this skill, and they are opposites. Places that must be **condensed** (the abstract, the contribution list) come out wordy; places that must be **detailed** (the technical overview, the concrete construction) come out thin. This skill decides both by number rather than by taste.

Every threshold below is a median or a quartile of a frozen corpus of accepted top-venue papers, cited as `file:line` with its sample size `n` and its measurement basis. Write for the venue, not in the abstract: structural and stylistic decisions are made against one named conference's current official call, template, page limit, and reviewing culture.

## Scope

**Venue ownership — the binding boundary.** This skill owns the crypto/LNCS venue family, plus the corpus-calibrated rule set that both venue families reuse:

- the **crypto/LNCS family**: CRYPTO, EUROCRYPT, ASIACRYPT, and CRYPTO/LNCS-style submission;
- the **corpus-calibrated compression, expansion, and budget rules** that both venue families reuse.

**Delegated, and not restated here.** All **security-venue** register and rules belong to the two security skills — **ACM CCS**, **IEEE S&P** and **NDSS** to `ccs-writing-style`, **USENIX Security** to `usenixsec-writing-style`: their page budgets, the USENIX-mandated `Ethics considerations` and `Open science` sections together with their placement, the CCS IRB and responsible-disclosure obligations, and the per-venue overview and threat-model forms. This skill must not state a security-venue-specific rule. A draft aimed at CCS, IEEE S&P, NDSS, or USENIX Security must be written with the corresponding security skill, which owns the venue register; this skill supplies only the shared corpus-calibrated rules. A rule that genuinely applies to both families is written here **once** and cited by the sibling skills — it is never duplicated into them.

`description` lists every venue name because the frontmatter is a trigger list, not a claim of ownership; the ownership boundary is the one above.

In scope: repairing a draft that is wordy where it must be tight and thin where it must be deep; choosing a structure and section budget for the crypto/LNCS family; compressing an abstract and a contribution list to corpus-calibrated caps; enforcing a minimum technical-overview and construction substance and a named constituent checklist; measuring cross-section mass and relocating rather than deleting over-thick material; placing concrete numbers by section; naming and de-naming rules; applying an executable de-AI checklist; verifying double-blind anonymity; checking LNCS template formatting for the crypto family; and running a diagnosis-first pre-submission pass.

Out of scope: inventing results, proofs, citations, or experiments; upgrading claim tiers; deciding novelty or authorship; guaranteeing acceptance; submitting without human authorization; and the delegated security-venue register and rules named above (ACM CCS, IEEE S&P and NDSS in `ccs-writing-style`; USENIX Security in `usenixsec-writing-style`), which this skill points to but does not own.

Threshold provenance: every number in this skill is derived from the frozen writing-craft corpora under `skills-work/corpus/` — the crypto/LNCS corpus (62 tier-A venue papers, 135 full LaTeX sources) and the security four-venue corpus (35 papers, 25 read in full) — together with the EVH-MLPC revision record. Those `skills-work/…:file:line` citations are **provenance annotations into the authoring workspace's corpus snapshot, not links**, and they are not expected to resolve beside an installed copy. Every threshold is self-contained in this skill: it carries its sample size `n` and its measurement basis inline. No rule here is invented, and no numeric threshold is chosen by taste.

## Required Inputs

- the target venue and its **current** official call for papers (page limit, template, anonymity, ethics, artifact policy), fetched at execution time;
- the manuscript draft, or verified claims/evidence to write from, in LaTeX **and** its markdown twin when both exist (the rules measure either, but never mix them in one comparison);
- a named region map: which `file:line` span is the abstract, the contribution list, the technical overview, the construction, the security analysis, and each appendix;
- the comparison corpus for the related-work and comparison-table positioning;
- the venue template or bibliography style, when a format pass is requested.

## Success Criteria

Every criterion is a number with a basis and a sample size. A threshold stated as an adjective does not satisfy it.

**Condensation — the abstract** (`references/compression-rules.md`):

1. Abstract body is **at most 210 words** (corpus median, `skills-work/corpus/crypto/statistics.md:121`, n=59 tier-A). The corpus third quartile is 253 and its maximum is 483, so a longer abstract is not automatically wrong — but quote the corpus line that licenses the length, and a 250-word cap alone does **not** satisfy this rule.
2. **At least 0.56 (56%)** of abstract words describe what is built, pooled over the hand-coded four-move sample (build share 0.56, `skills-work/corpus/crypto/statistics.md:165`, n=15). This is the criterion that catches an abstract which spends two thirds of itself on proved bounds and gives its own construction one sentence: such a draft can pass any length cap.
3. Longest abstract sentence is **at most 40 words** (median of the per-abstract longest sentence, `skills-work/corpus/crypto/statistics.md:124`, n=59; third quartile 49).
4. `## Workflow` prints the abstract's total word count, its per-paragraph move labelling, its build share, and its longest sentence, before and after the rewrite.

**Condensation — the contribution list** (`references/compression-rules.md`):

5. **2 to 5 bullets**, median 4 (`skills-work/corpus/crypto/statistics.md:196`, n=50 tier-A).
6. **At most 29.5 words per bullet**, median 29.5 over 214 bullets (`skills-work/corpus/crypto/statistics.md:198`); the longest single bullet is **at most 57.5 words**, median 57.5 (`skills-work/corpus/crypto/statistics.md:199`, n=50). Both caps are the corpus median used unrounded, so each cap is exactly the number its cited line carries.
7. Whole block is **at most 146 words**, median 146 (`skills-work/corpus/crypto/statistics.md:197`, n=50), and **at most 0.81x** the abstract's length (block/abstract ratio, median 0.81, `skills-work/corpus/crypto/statistics.md:200`, n=50). A list longer than the abstract it summarises is the mechanical signature of an expanded abstract rather than a compressed list.
8. **Zero shared 6-grams** between the abstract and the contribution block, on the corpus metric: 6-grams over case-folded `[a-z0-9]+` tokens, counted as an absolute number and as a ratio over the abstract's 6-grams (`skills-work/corpus/crypto/statistics.md:206-212`, n=50; median 0, maximum 6, and only 0.1 of papers share any). Where a shared 6-gram is a named object introduced in both places, record the disposition instead of deleting the name.
9. Every span that leaves the abstract or the list **has a destination** — a named section, a footnote, or an appendix — and the destination is written down. Nothing is deleted outright.

**Elaboration — the technical overview** (`references/expansion-rules.md`):

10. A separately titled overview section is **not** mandatory: only 29% of tier-A papers have one (`skills-work/corpus/crypto/statistics.md:229`, n=62), and a title-keyed requirement misses the majority. The overview's **content and mass** are mandatory instead.
11. The overview is **at least 379 words**, the corpus minimum (`skills-work/corpus/crypto/statistics.md:239`, n=18); **at least 1930 words** (first quartile) is the practical target for a construction-centred paper, against a corpus median of 3423.
12. The overview is **at least 99 source lines** (`skills-work/corpus/crypto/statistics.md:240`, n=18) and **at least 0.25 of the introduction's words** (`skills-work/corpus/crypto/statistics.md:241`, n=18; first quartile 0.96, median 1.48). 
    Where the overview lives as a named block inside the introduction instead, the figure is **at least 295 words** (`skills-work/corpus/crypto/statistics.md:252`, n=5).
13. The overview carries the five mandatory constituents listed in `references/expansion-rules.md`, each anchored to a corpus line, and **at least 4 named sub-blocks** (first quartile; median 5, `skills-work/corpus/crypto/statistics.md:243`).

**Elaboration — the construction** (`references/expansion-rules.md`):

14. Construction-to-analysis mass ratio, measured on **words, `direct` basis** (a section's own text with its immediate children's spans subtracted): **below 0.44 fails** (corpus first quartile, `skills-work/corpus/crypto/statistics.md:285`, n=10); **0.44 to 0.89 needs expansion**; **at 0.89 or above passes** (corpus median).
    **Degeneracy guard — mandatory, and registered in the R-VENUE-13 row rather than only here.** Before printing any of those three band verdicts, test the basis: a section's `direct` measurement is **degenerate** when its `direct` word count is smaller than the word count of its own heading, or smaller than 20 words, or its `direct` span holds no running prose (only heading lines and fragments). **When the guard fires the rule must not print `pass`, `needs expansion`, or `fail`, and must not cite the 0.44 or 0.89 bands:** it reports only the hierarchical numbers, names the twin (`tex` or `md`) and the unit (raw lines, content lines, or words), and names the sections that tripped the guard. The guard decides real verdicts, not edge cases: on the calibration manuscript §3/§4/§5 carry no direct prose, so their `direct` spans collapse onto heading lines and measure 8/4/4 (md) and 9/5/5 (tex), ratios 3.00 and 2.80 — and the unguarded rule prints `pass` for a §3 that the constituent checklist in the next criterion calls thin. An independently written counter agrees: `direct_words` design = 10 against analysis = 3.
66. The construction section carries the constituent checklist in `references/expansion-rules.md`, with **at least 5 items**, each anchored to a corpus line. This checklist, not the ratio, is the discriminating instrument, and it is also the fallback whenever the mass-ratio guard above fires.
    Its discriminating power comes from the corpus's own quartile table: `correctness_claim` appears in 0.0 of the thinnest quartile against 0.857 of the thickest, and `labelled_parameter_list` in 0.143 against 0.857 (`skills-work/corpus/crypto/statistics.md:351-370`).
    A calibration caution that must travel with any verdict from this checklist: the calibration manuscript's §3 *is* thin, but not for the reason an earlier draft of the rules gave — §3.4 (`research-work/paper/final-paper.md:131-151`) is an ordered round-by-round message flow, so §3 fails on its **parameter list** and **roadmap**, not on message ordering; and its §4 **passes the required checklist 5 of 5**, the row-band layout table being at `research-work/paper/final-paper.md:174-181` and the worked instance at `:266`. Verdicts and reasons are both in `references/expansion-rules.md`.

Two qualifications on that ratio rule, which any pass reproduces. The `direct` basis itself is defined in the corpus's basis section (`skills-work/corpus/crypto/statistics.md:18-19`). And a rule of the form "the construction exceeds the analysis" is not supported: only 40% of corpus pairs exceed 1 (`skills-work/corpus/crypto/statistics.md:288`), and a second, differently-based measurement exists — median 1.1, first quartile 0.39, with appendices included, n=17 (`skills-work/corpus/crypto/statistics.md:290`) — so a rule has to name which basis it uses and may not mix them.
16. Section role is decided by **what a section presents**, never by its title: 69% of tier-A papers have no section whose title contains "Construction" (`skills-work/corpus/crypto/statistics.md:112`), so `Description ...` and `Parameters.` blocks count as construction material.

**Budget and placement** (`references/section-budget.md`, `references/numeric-placement.md`):

17. No single subsection holds a **majority** of its parent section's words: above 0.50 a relocation pass is required, and above 0.65 the parent is an outlier (only 0.205 of corpus pairs are above 0.65, `skills-work/corpus/crypto/statistics.md:334`, and `skills-work/corpus/crypto/statistics.md:333` gives the 0.48 share above 0.50).
    The corpus median largest-child share is 0.491, its third quartile 0.607 and its 90th percentile 0.774, over 561 parent-child pairs (`skills-work/corpus/crypto/statistics.md:330`).
18. Relocation is **move-not-delete**: every claim, status label, number, and provenance travels with the moved text. Verification records, review narrative, superseded metrics, measurement tables, and tool output are relocatable; claims and their status wording are not.
19. Concrete measured values appear in evaluation, parameters, and implementation material, and **never** in construction or proof sections — the corpus audit finds exactly zero high-precision literals in those roles (`skills-work/corpus/crypto/statistics.md:405-415`). A concrete value may sit in a theory section only when it carries a filed reason of the class *analytic or design-point arithmetic, not a measurement*; measurement records belong in a heading-marked evidence record.
20. Process-register naming never appears as an example or a prescription, and the de-naming pass follows the **adjudication contract owned by `references/de-ai-and-style.md`** — that file is the authority for the classes, the definition test, and the permitted-literal blocks, and this criterion must not restate it. The pass is satisfied when **every class-1/3/6 candidate has been adjudicated**, each with either its **definition anchor** or `no definition found`, and there are **zero unresolvable identifiers**. Raw per-class hit counts are **diagnostics only and must never be presented as the verdict**. A literal may appear only inside the five blocks that must name one in order to be usable — the anti-pattern table, §Stage 2's definition-test row, the class-6 discussion, the worked adjudication, and the reproducible command — and each anti-pattern entry must carry its forbidding sentence.
21. **Status contract for the two mass rules — this is what makes the guard falsifiable.** The section-mass pass is executed by the **shipped instrument**, `scripts/count_venue_gates.py`, which measures each named region on a named twin and reports, for every section it evaluates, exactly one status: `measured` (a number was produced), `degenerate` (the `direct` guard of criterion 14 fired for that section), or `unmatched` (a named section could not be located in the twin). **`degenerate` and `unmatched` are the required statuses when the guard fires or a section is not found — never a silent pass and never an omitted row.** A pass that prints a band verdict in either case, or that omits the section from the report, has failed. The same statuses apply to the ceiling of criterion 17, with one structural exception recorded in `references/section-budget.md`: the ceiling compares a child against its parent on **hierarchical** counts and never subtracts direct spans, so it cannot be `degenerate` — only `measured` or `unmatched`.
    The instrument returns a **non-zero exit code** — **2** whenever any gate is `degenerate` or `unmatched`, so "the guard fired but nothing printed a band" is a detectable state rather than a silent one, and **1** when a *verdict-path* pass condition fails (e.g. the de-naming scan reporting unresolvable identifiers). A *breach* of a stated threshold is a finding, not an error: the exit code reports measurement integrity and pass-condition outcomes, not compliance. Run it as

    ```bash
    cd skills-work/crypto-research-agent-skills
    python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py --self-test          # counts itself: "self-test: 64/64 as expected", exit 0
    python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py --manuscript <your.md> --build-share <hand-coded 0..1>
    python3 skills/crypto-venue-paper-writing/scripts/count_venue_gates.py --dename <twin.md> <twin.tex>
    ```

    The construction/analysis mapping is an **input** (`--construction 3,4 --analysis 5`), never a title-based detection, because a title-keyed rule misfires — on this manuscript one heading carries both vocabularies and the detector paired it with itself.

## Failure Modes

- **Words where it must be tight.** An abstract over 210 words, a contribution list over 146 words or over 5 bullets, a bullet over 29.5 words, or a shared 6-gram between abstract and list: run the abstract compression pass in `references/compression-rules.md` and return the four counts plus the destination of every removed span. A near-miss — a 240-word abstract whose build share is 0.30 — still fails: report it as an allocation defect, not a length defect.
- **Thin where it must be deep.** An overview under 379 words, under 0.25 of the introduction, or missing a mandatory constituent: run the expansion pass and name every absent constituent. A 288-word overview that "reads complete" is the reported defect, not a judgement call.
- **Length-only compliance.** A draft that satisfies the caps but inverts the allocation, or expands everywhere rather than relocating, has not passed. Report the allocation and the ratio bands, not just the totals.
- **Unnamed basis.** Any printed ratio, page count, or word budget that does not state which twin (`tex` or `md`), which unit (raw lines, content lines, or words), and which basis (`direct` or hierarchical) is unusable; remeasure before reporting.
- **Title-keyed structure.** A section classified as "construction" or "analysis" from its heading alone will mis-file the majority of papers. Classify by content and list the sections you classified.
- **Numbers parked in a theory section.** A measured value appearing in a construction or proof section without a filed reason of the analytic/design-point class is the re-induced form of the reported defect: relocate it with its digits and provenance intact.
- **Fabrication.** No result, citation, parameter, measurement, or review outcome may be invented. A threshold that cannot be traced to a corpus `file:line` is not a threshold; write the rule without a number instead of choosing one.
- **AI-flavor prose that survives a first pass.** Run the grep-level checklist in `references/de-ai-and-style.md` and rewrite; do not merely flag.
- **Venue rules may have changed.** Never assert a remembered page limit or style file: fetch the current official call and record a dated snapshot.
- **De-identification gap** (author names, institution, identifying repository links) must be fixed before any format pass.

## Workflow

Diagnose before rewriting. Steps 1-2 produce the diagnosis; a rewrite that starts before them cannot say which section is thin and which is redundant.

1. **Freeze the venue and the region map.** Fetch the current official call and template; record the date. Produce the `file:line` map from `## Required Inputs` for both twins when both exist. Do not proceed to any budget claim without it.
2. **Run the diagnosis pass.** For each region, print: abstract words, sentences, per-paragraph move labelling and build share; contribution block words, bullet count, longest bullet, and abstract-to-list shared 6-grams; each section's raw lines, content lines, and words, with the largest-child share per parent; the construction-to-analysis ratio with its basis; and the overview's words, lines, and share of the introduction. Output a ranked list that names the under-detailed section and the redundant section with their numbers. Generic advice is not an acceptable output of this step.
3. **Run the abstract compression pass** (`references/compression-rules.md`). Cut in this order: process narration, meta-narration, abstract-to-list duplication, adjectives standing where a number belongs. Move, never delete: write each removed span's destination. Re-report the four counts.
4. **Run the expansion pass** (`references/expansion-rules.md`). Bring each region up to its floor and its mandatory constituents. Every added sentence must restate material already in the manuscript, in the design record, or in an artifact — never a new claim.
5. **Run the section-mass and relocation pass** (`references/section-budget.md`). Relocate over-thick ledger material to a heading-marked evidence record, carrying every claim, status label, and number with it.
6. **Run the numeric-placement pass** (`references/numeric-placement.md`). Scan the construction and proof regions for the concrete-literal class; relocate each hit with its digits and provenance, or file the analytic/design-point reason that licenses it.
7. **Run the de-identification and de-naming pass** (`references/de-ai-and-style.md`, which owns the classes, the definition test, and the permitted-literal blocks). Collect the class-1/3/6 candidates, then **adjudicate every one of them against the manuscript and write the verdict**: `violation` with `no definition found`, or `legitimate(a)`/`(b)`/`(c)` with its definition anchor, or `not-a-token` for a match that is not a token at all. The pass is **not** "zero hits" — it is **no unadjudicated hits and zero unresolvable identifiers**, and the raw per-class counts are diagnostics that must never be presented as the verdict.
8. **Run the pre-submission pass.** Number-and-body consistency, claim tiers, citation integrity, double-blind scan, page budget against the fetched call, template compile. Report every unresolved item as a question for the human author rather than resolving it silently.

## Output Contract

Return, in this order, and keep the diagnosis visible even when the rewrite is complete:

1. **Target-venue policy snapshot** with the fetch date and the source URL.
2. **Diagnosis table** — one row per region, with the measured numbers, the threshold it was compared against, and a verdict of `redundant`, `thin`, `over-thick`, or `within budget`. A row with no number is not a diagnosis.
3. **Rewrite or diffs**, with every removed span's destination recorded.
4. **The four abstract numbers** before and after: total words, build share, longest sentence, paragraph move labelling.
5. **The five contribution-list numbers** before and after: bullets, block words, longest bullet, block/abstract ratio, shared 6-grams.
6. **Expansion report** — overview words/lines/share with the absent constituents named; construction ratio with its named basis and the constituent checklist with its present/absent marks.
7. **Budget report** — per-section and per-subsection shares with the largest-child verdict, and the relocation ledger.
8. **Numeric-placement report** and the **de-naming and de-AI checklist results**.
9. **Venue compliance report** — double-blind, page limit, template, bibliography style, against the fetched call.
10. **Unresolved items** requiring the human author, each with the reason it could not be decided here.

## Reference Files

| File | Contents |
|------|----------|
| [compression-rules.md](references/compression-rules.md) | Abstract caps, build-share floor, sentence cap, contribution-list caps, the duplication metric, and the delete-or-migrate list with destinations |
| [expansion-rules.md](references/expansion-rules.md) | Technical-overview floors and constituent checklist; construction constituent checklist; construction-to-analysis ratio bands with their basis |
| [section-budget.md](references/section-budget.md) | Per-section and per-subsection share ceilings; the move-not-delete relocation rule and the relocatable classes |
| [numeric-placement.md](references/numeric-placement.md) | Which sections carry concrete values and which carry symbolic expressions; relocation that preserves value and provenance |
| [venue-structure.md](references/venue-structure.md) | Venue-specific structure, four-move abstract formula, page and template anchors, venue policy table |
| [de-ai-and-style.md](references/de-ai-and-style.md) | De-AI vocabulary/structure/content red flags, the process-register anti-pattern list, sentence-level register, executable grep checklist |
| [evaluation-scenarios.md](references/evaluation-scenarios.md) | Test specifications for independent evaluation |
| [count_venue_gates.py](scripts/count_venue_gates.py) | **The instrument** — every numeric gate in this skill (abstract cap and four-move build share, contribution caps and the duplication metric, overview floors, the construction-to-analysis ratio **with the degeneracy guard**, and the largest-child ceiling), plus `--dename` for the de-naming adjudication and `--self-scan` for this skill's own files. Non-zero exit when a gate is `degenerate` or `unmatched`. `--self-test` runs its assertion suite and prints its own count — currently `self-test: 64/64 as expected`, exit 0. |
