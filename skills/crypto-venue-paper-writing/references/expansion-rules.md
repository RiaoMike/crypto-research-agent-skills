# Expansion Rules — The Technical Overview and the Construction

Executable rules for the two places that must be **detailed**. Every floor and every checklist item carries its corpus `file:line`, sample size `n`, and basis.

Basis vocabulary, quoted from `skills-work/corpus/crypto/statistics.md:10-21`: `words` are whitespace-separated alphanumeric tokens of the plain-text rendering; `lines` are physical source lines of the file the unit lives in, comments removed; a section's `words` include its subsections' words unless the number says `direct`, and `direct` means the section's own text with its immediate children's spans subtracted. **Pages are not measurable in a LaTeX source** — the corpus records no page number, so a rule stated in pages is unusable.

## Why a floor is needed at all

Thinness is invisible without a distribution. The corpus's smallest technical overview is 379 words and its first quartile is already 1930 (`skills-work/corpus/crypto/statistics.md:239`, n=18), while its median is 3423. An overview of a few hundred words reads as complete to its own author and is below the corpus floor; the calibration manuscript's overview is 288 words, under the corpus minimum. A skill that never states the floor cannot flag it.

The same holds for the construction. But a **mass** rule alone does not catch the reported defect, and this file says so explicitly rather than pretending otherwise. The reported pre-revision construction-to-analysis ratio was 0.576 measured on tex lines and 0.667 on words, both on the **hierarchical** basis (a section's span including its subsections); the corpus bands in §The construction-to-analysis mass ratio below are stated on the **words, `direct`** basis, and **that basis degenerates on this manuscript**. Sections 3, 4 and 5 carry no direct prose — nearly all their text sits in subsections — so their `direct` spans collapse onto heading lines and measure 8 / 4 / 4 words on the markdown twin and 9 / 5 / 5 on the tex twin, giving ratios of 3.00 and 2.80. Those are meaningless numbers, and they make the rule print **`pass` at 0.89 or above** for the very §3 that the constituent checklist below calls thin. An independently written counter agrees: t5's instrument computes `direct_words` design = 10 against analysis = 3, a ratio of 3.33. So the mass rule is not the detector for this defect, and it must not be used as one on any manuscript whose `direct` basis degenerates: **the guard in §Degenerate `direct` measurement — the mandatory guard is required**, and the instrument that actually discriminates thin from thick is the constituent checklist in §The construction below, where the thinnest quartile and the thickest quartile separate sharply. Treat the ratio as a guardrail only where its basis is sound, and the checklist as the detector.

## The technical overview

### Placement: content and mass are mandatory, a title is not

**Do not require a separately titled overview section.** Only 29% of tier-A papers have one (18 of 62, `skills-work/corpus/crypto/statistics.md:229`), and a rule keyed on the title misses the other 71%. The corpus's placement variants, with counts (`skills-work/corpus/crypto/statistics.md:230-232`):

- a separate top-level section — 16 papers;
- a named subsection inside the introduction — 4 to 5 papers;
- a named paragraph block inside the introduction — 2 or more papers, a lower bound because authors rename the heading macro.

What is mandatory is that the overview **function** be locatable and that it clear the floors below. Record which form was used and the `file:line` span.

### Floors

| quantity | floor | practical target | corpus value | anchor | n |
|---|---|---|---|---|---|
| overview words | **379** (corpus minimum) | **1930** (q1) | median 3423 · q3 4420 · max 6360 | `skills-work/corpus/crypto/statistics.md:239` | 18 |
| overview lines | **99** (corpus minimum) | **200** (q1) | median 271.5 | `skills-work/corpus/crypto/statistics.md:240` | 18 |
| overview words / introduction words | **0.25** (corpus minimum) | **0.96** (q1) | median 1.48 | `skills-work/corpus/crypto/statistics.md:241` | 18 |
| named sub-blocks inside the overview | **4** (q1) | 5 (median) | q3 11 · max 23 | `skills-work/corpus/crypto/statistics.md:243` | 19 |
| named block inside the introduction, instead of a section | **295** words (corpus minimum) | 401 (q1) | median 558 | `skills-work/corpus/crypto/statistics.md:252` | 5 |

The corpus states the reading plainly: the minimum "is the number a draft has to clear before it is comparable to the thinnest overview in this sample; the first quartile is the practical target" (`skills-work/corpus/crypto/statistics.md:245-246`).

A cross-check from the security corpus, usable when the target venue is a security venue: the overview function is present in 27 of 35 papers (77%) and, when present,
it runs a median 2 pages and 1535.5 words (`skills-work/corpus/security/statistics.md:85`, `skills-work/corpus/security/statistics.md:89-92`). The two corpora agree that a paragraph is not an overview.

### Mandatory constituents

All five are required. Each is anchored to a corpus line carrying a real instance, and each is a *reader-necessity*, not a stylistic preference: the corpus's smallest overviews carry them and the thin-draft failure mode is their absence.

1. **The obstacle, stated as a failed first attempt.** Give the natural design and why it does not work, then the fix. Corpus instance: a block literally named `First Attempt.` whose next block is the optimization (`skills-work/corpus/crypto/statistics.md:270`). This is a first-class move, not filler.
2. **The idea, one named sub-block per mechanism.** At least four named sub-blocks, one per mechanism, each with the same shape. Corpus: median 5 named blocks (`skills-work/corpus/crypto/statistics.md:269`), and each block typically states the obstacle, the idea, why it works, and then points forward (`skills-work/corpus/crypto/craft-notes.md:222-249`).
3. **Why it works — a mechanism sentence, not a restatement.** State the property that makes the idea succeed. Corpus: informal statement environments placed next to the formal ones (`skills-work/corpus/crypto/statistics.md:272`); the security corpus records the stable structure as 「难点 → 我们的想法 → 为何可行」 and finds both an intuition sentence and a mechanism sentence in 24 of its 25 deep-read papers (`skills-work/corpus/security/statistics.md:96-102`).
4. **An explicit pointer to the formal statement or proof.** Name the section, theorem, or lemma label that delivers what the overview promised. Corpus: `skills-work/corpus/crypto/statistics.md:274`, instance `T:2608.06724/overview.tex:48`. The security corpus records the same device — for example "See Sec. VI for details." (`skills-work/corpus/security/statistics.md:107`).
5. **A labelled step list in the shape of the final object.** The overview should carry the object's steps in order, in prose or a description list, before the formal construction exists. Corpus: `skills-work/corpus/crypto/statistics.md:273`, instance `T:2608.06724/overview.tex:29`.

Two further devices are supported but optional: a roadmap of the overview's own subsections (`skills-work/corpus/crypto/statistics.md:275`) and an enumeration of challenges, each later answered by name (`skills-work/corpus/crypto/statistics.md:271`). The security corpus adds a sixth useful item — name a recurring condition as a **named object** so later sections can cite it (`skills-work/corpus/security/statistics.md:110`).

### What the overview must not become

- **A second contribution list.** The overview is not interchangeable with the contributions: it is the reader's route into the mechanisms, and the corpus's overviews are larger than the contribution blocks they make concrete (`skills-work/corpus/crypto/craft-notes.md:202-221`).
- **A formula dump.** Prose in the construction and overview carries the *reason* for each formal step, not the notation again (`skills-work/corpus/crypto/craft-notes.md:309-323`).
- **A place for concrete measured values.** See `references/numeric-placement.md`.

## The construction

### How to find the construction section

**Never key on the title.** 69% of tier-A papers have no section whose title contains "Construction" — 43 of 62 (`skills-work/corpus/crypto/statistics.md:112`). Classify by what a section *presents*, and count `Description ...`, `Parameters.`, `Our scheme`, and similar blocks as construction material. The corpus names the papers a title-keyed rule misses (`skills-work/corpus/crypto/statistics.md:293-296`).

### The constituent checklist — the discriminating instrument

Each item below shows its presence share in the **thinnest** and **thickest** quartiles of construction sections (n=7 each), from `skills-work/corpus/crypto/statistics.md:351-370`. Items with a wide thin-to-thick gap are the ones a thin section is actually missing; all five marked **required** below must be present.

| # | constituent | thin quartile | thick quartile | anchor | required |
|---|---|---|---|---|---|
| 1 | `correctness_claim` — a correctness or "why it works" statement | 0.0 | 0.857 | `skills-work/corpus/crypto/statistics.md:356` | **yes** |
| 2 | `labelled_parameter_list` — parameters, algorithms, or parties as a labelled list | 0.143 | 0.857 | `skills-work/corpus/crypto/statistics.md:361` | **yes** |
| 3 | `reader_roadmap` — a statement of how the section is organised | 0.0 | 0.571 | `skills-work/corpus/crypto/statistics.md:364` | **yes** |
| 4 | `step_ordering` — the steps of the object in order | 0.429 | 1.0 | `skills-work/corpus/crypto/statistics.md:367` | **yes** |
| 5 | `intuition_sentence` — an intuitive explanation beside the formalism | 0.0 | 0.429 | `skills-work/corpus/crypto/statistics.md:360` | **yes** |
| 6 | `security_notion_needed` — the construction names the notion the analysis will prove | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:366` | recommended |
| 7 | `why_necessary` — why each ingredient is needed | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:369` | recommended |
| 8 | `citation_to_prior_building_block` — build-up from named prior constructions | 0.0 | 0.286 | `skills-work/corpus/crypto/statistics.md:354` | recommended |

Baseline shares over the whole construction sample (n=29), so a section can be compared against the corpus rather than against the thin quartile only: `step_ordering` 0.69, `labelled_parameter_list` 0.586, `formal_object_box` 0.552, `correctness_claim` 0.414, `protocol_diagram` 0.379, `complexity_statement` 0.241 (`skills-work/corpus/crypto/statistics.md:316`, `skills-work/corpus/crypto/statistics.md:310`, `skills-work/corpus/crypto/statistics.md:307`, `skills-work/corpus/crypto/statistics.md:305`, `skills-work/corpus/crypto/statistics.md:312`, `skills-work/corpus/crypto/statistics.md:304`).

Two corpus warnings about the table. First, the automated counts are a **lower bound**: authors rename heading macros, so a named block may exist undetected. Second, two constituents are genuinely rare in the corpus (`parameter_choice_reason` 0.0, `worked_example` 0.0, `skills-work/corpus/crypto/statistics.md:311`, `skills-work/corpus/crypto/statistics.md:319`), so their absence is **not** a defect — do not add them just to tick the list.

The security corpus supplies an independent, compatible checklist for a concrete scheme section, usable as a cross-check: a named object or relation (19 of 25), a protocol or algorithm box (10 of 25), a parameter-choice justification (15 of 25), and a complexity or communication expression (17 of 25) (`skills-work/corpus/security/statistics.md:131-138`). It also records the cap: a named-object definition is what makes a recurring condition citable, and the mechanism explanation belongs in prose rather than in a regular expression (`skills-work/corpus/security/statistics.md:140-143`).

### The construction-to-analysis mass ratio

**Basis: words, `direct` measurement** — the section's own text with its immediate children's spans subtracted (`skills-work/corpus/crypto/statistics.md:18-19`). State the basis with every number you print.

| band | ratio | corpus meaning | anchor |
|---|---|---|---|
| **fail** | below **0.44** | thinner than the corpus first quartile (n=10) | `skills-work/corpus/crypto/statistics.md:285` |
| **needs expansion** | 0.44 to below **0.89** | above the first quartile, below the median | `skills-work/corpus/crypto/statistics.md:285` |
| **pass** | **0.89** and above | at or above the corpus median | `skills-work/corpus/crypto/statistics.md:285` |

Corpus distribution on that basis: min 0.11 · q1 0.44 · median 0.89 · q3 1.41 · max 2.88, n=10. Only 40% of pairs exceed 1 and 70% exceed 0.5 (`skills-work/corpus/crypto/statistics.md:288`), so **"the construction must exceed the analysis" is not supported by the corpus and must not be written as a rule.**

A second figure exists on a different basis and must not be mixed with the first: on **words with appendix sections of the same role added**, n rises to 17 and the median ratio is 1.1, q1 0.39, q3 1.64 (`skills-work/corpus/crypto/statistics.md:290`). A third, on **lines with hierarchical spans**, has median 1.21 and q1 0.36 (`skills-work/corpus/crypto/statistics.md:286`). Choose one, name it, and keep the comparison inside it.

The basis-dependence is not academic. The same manuscript measures 0.576 on tex lines and 0.667 on words before revision, and 0.9524 on tex lines against 1.3120 on md lines after — different bases, different verdicts at the same moment in the paper's history. Any printed ratio without its named basis is unusable, and md and tex measurements may not be mixed in one comparison.

Cross-venue check available for a security-venue paper: the security corpus reports a construction-to-proof page ratio with a median of 5 to 1 (construction median 5 pages, proof median 1 page, `skills-work/corpus/security/statistics.md:124`), on a page basis. Because the crypto corpus cannot measure pages at all, **do not transfer that figure into a LaTeX-source measurement** — use it only when the unit really is pages.

### Degenerate `direct` measurement — the mandatory guard

**This guard is mandatory, and it is carried by the registry row for R-VENUE-13 as well as by this file, because downstream execution follows the registry row rather than this prose.**

**What degeneracy is.** A section's `direct` count is the section's own text with its immediate children's spans subtracted (`skills-work/corpus/crypto/statistics.md:18-19`). When a section's prose lives almost entirely in its subsections, that subtraction leaves only the section heading and stray connective lines, and the `direct` number stops measuring text and starts measuring headings.

**Detection.** Treat the `direct` basis as **degenerate** for a section when either holds:

- the section's `direct` word count is **smaller than the word count of its own heading** plus a small allowance, or more plainly smaller than 20 words; **or**
- the section's `direct` span contains **no running prose** — every counted line is a heading, a label, or a fragment.

Report the detection as a named observation per section, with the `direct` count, the heading count, and the twin.

**Scope of the guard — which sections it covers, and on which side.** The guard is evaluated for **every section whose `direct` count enters the printed figure, numerator and denominator alike**. For the construction-to-analysis ratio that is:

- **the numerator** — each section classified as construction by content (see §How to find the construction section), summed;
- **the denominator** — the section classified as analysis, whose `direct` count forms the whole denominator.

A degenerate reading on *either* side makes the ratio meaningless, so both sides are tested. The ratio is printed **only when every contributing section returns `measured`**. If any contributing section returns `degenerate`, the ratio is reported as **not evaluated on the `direct` basis**, with the hierarchical numbers, the named twin and unit, and the offending section named — never as a band verdict. If a contributing section cannot be located at all, its status is `unmatched`, which has the same consequence.

The guard does **not** cover the overview floors of §Floors, which are absolute word and line counts on a named span rather than a `direct` ratio; those are reported against their floors with the twin and unit named, and a span that cannot be located is `unmatched`.

**Required behaviour when it fires.** The rule **must not** output a corpus band conclusion for that section:
- it **must not** print `pass`, `needs expansion`, or `fail`, and must not quote the 0.44 or 0.89 bands, because the input to those bands is meaningless;
- it reports **only the hierarchical numbers** — the section spans with subsections included — together with the **named twin** (`tex` or `md`) and the **named unit** (`raw lines`, `content lines`, or `words`);
- it states which sections tripped the guard, and reports the ratio as **not evaluated on the `direct` basis**;
- for the thin/thick judgement it falls back to the constituent checklist in §The constituent checklist, which is the discriminating instrument anyway.

**Why this is not optional — the measured failure.** On the calibration manuscript the guard is the difference between a correct verdict and a false negative. Sections 3, 4 and 5 carry no direct prose, so:

| twin | §3 direct | §4 direct | §5 direct | printed ratio | verdict the unguarded rule printed |
|---|---|---|---|---|---|
| markdown | 8 words | 4 words | 4 words | 3.00 | `pass` at 0.89 or above |
| tex | 9 words | 5 words | 5 words | 2.80 | `pass` at 0.89 or above |

Those `direct` counts are heading lines, not content. The rule as written *without* the guard therefore prints **`pass` for §3**, a section the constituent checklist simultaneously calls thin. Two independently written counters produce the same degenerate reading — this file's tokenizer gives 8 / 4 / 4 and 9 / 5 / 5, and t5's instrument computes `direct_words` design = 10 against analysis = 3, a ratio of 3.33. A false-negative instrument is worse than a missing rule, which is why the guard is a hard requirement rather than advice.

### Deferral discipline

The construction is allowed to defer detail, but the deferral must be **named** and nothing may be lost. The corpus defers proofs and says where (`skills-work/corpus/crypto/craft-notes.md:324-337`), and the deferral count is small: forward references inside a construction section have a median of 0 and a maximum of 3 (`skills-work/corpus/crypto/statistics.md:387`, n=29). When material moves out of the construction, record it in the relocation ledger required by `references/section-budget.md` and keep its claim and status wording.

## Pass output

The expansion pass returns, and `## Output Contract` requires:

- **Overview:** the `file:line` span, its placement form, words, lines, and share of the introduction, each against floor and target; the present/absent mark for each of the five mandatory constituents; the named sub-block count.
- **Construction:** the sections classified as construction and the rule used to classify them (content, not title); words and the named basis; the ratio and its band; the present/absent mark for each checklist item; the list of constituents absent relative to the thick quartile.
- **Additions ledger:** one row per added sentence, with the source it restates — the manuscript, the design record, or an artifact. An addition with no source is a new claim and is not permitted here.
- **Residual shortfalls:** any region still below its floor, with the reason, and the explicit statement of whether a corpus line licenses the exception.

## Worked calibration

The pass must reproduce these verdicts on the frozen calibration manuscript; they are the contract's measurements, not new ones.

| region | measured | floor / target | verdict |
|---|---|---|---|
| §1.3 technical overview `research-work/paper/final-paper.md:60-67` | 288 words / 8 lines | floor 379 words · 99 lines | **breach** — below the corpus minimum |
| overview share of the introduction | **0.1567** = overview 288 words ÷ region **1838** words, region `research-work/paper/final-paper.md:29-75`, basis **whitespace tokens (`\S+`)** | floor 0.25 | **breach on allocation** — the overview is also smaller than the 902-word contribution list it exists to make concrete. The region is named because the figure moves with it: the region is the introduction's budgeted subsection block, from §1.1 at `:29` to the last line before §2 at `:75`. Widening it to `:23-75` — the §1 heading plus its two framing paragraphs, which are not budgeted subsections — gives 288 ÷ 2102 = **0.1370**, a different number, so the two are never mixed and neither is quoted without its region. |
| §3 host protocol `research-work/paper/final-paper.md:106-157` | 1089 words | 5-item checklist | **thin** — but read the corrected reason below: §3 has more than the earlier text claimed |
| §4 construction `research-work/paper/final-paper.md:158-269` | 2646 words | 5-item checklist | **passes the checklist 5 of 5** — the earlier text called it thin and was wrong on its stated grounds |
| §3/§4/§5 `direct` basis (the rule's mandated basis) | 8 / 4 / 4 words (md), 9 / 5 / 5 (tex) | ratios 3.00 (md) and 2.80 (tex) against the 0.44–0.89 bands | **guard fires** — the basis is degenerate, so **no band verdict is printed**; only the hierarchical numbers are reported, with the twin and unit named |
| construction/analysis ratio, tex lines, hierarchical basis | 0.9524 | instrument reproduction, not a corpus-band comparison | **within band** — recorded with its basis |
| construction/analysis ratio, md lines, hierarchical basis | 1.3120 | same | **within band** |
| construction/analysis ratio, md words, hierarchical basis | 1.1243 | same | **within band** |
| same ratio before revision, tex lines, hierarchical basis | 0.576 | below the corpus q1 of 0.44 in spirit, but a different basis — see the note below | **needs expansion** — the band that the mass rule alone would have left alone |

Two notes that a pass must reproduce, because they are where a careless report goes wrong.

First, the corpus bands (fail below 0.44, pass at 0.89 and above) are on **words, `direct`**; the manuscript figures above are on **hierarchical** spans. They may be **reported side by side but never substituted for one another**. The ratio's job on the manuscript is to reproduce the instrument's frozen reading, and its job against the corpus is a separate, explicitly cross-basis indication. On this manuscript the `direct` basis trips the degeneracy guard, so no band verdict is printed at all.

Second, the last-but-one row is the honesty check on this file: a rule that measured mass alone would have called the pre-revision §3/§4 acceptable, because 0.576 sits above the first quartile, and would now print `pass` for a thin §3 through a degenerate basis. **The five-item checklist is what names §3 as thin**, and a pass that reports only the ratio has not run.

### The corrected §3 and §4 verdicts (non-normative calibration record), and why the earlier text was wrong

The earlier version of this table stated that §3 had "no ordered message flow and no drawn instance" and that §4 had "no worked table layout and no per-round algorithm box". **Both reasons were false against the manuscript, and a calibration table whose stated reason does not match the text gets copied into reviews, so the corrections are recorded here rather than quietly edited.** A verdict is recorded with the text that produced it, not only with its conclusion.

| region | the superseded claim (withdrawn — nothing in this column is asserted by this file) | what the manuscript actually contains | corrected verdict |
|---|---|---|---|
| §3 host protocol | "no ordered message flow and no drawn instance" | an ordered round-by-round message flow at `research-work/paper/final-paper.md:131-151`, opening "One round of the host proceeds as follows. The prover commits …" and then answering in turn and ordering the two sumchecks over the same committed table | **`thin` stands; the stated reason was wrong.** §3 *has* the step-ordering constituent and fails instead on its **labelled parameter list** and its **reader roadmap** |
| §4 construction | "no worked table layout and no per-round algorithm box" | the row-band layout table at `research-work/paper/final-paper.md:174-181` (content / randomness / flood / padding bands, each with its row-index range) and a worked instance at `research-work/paper/final-paper.md:266` — one masking row at `u = mu + n + 1 = 2^13 + 1`, `R' = 2^14`, `M = 2^10 - 1 = 1023` | **`thin` is withdrawn.** §4 **passes the required checklist 5 of 5**; only the *recommended* per-round algorithm box is absent, which does not make a section thin |

So the verdicts this file now expects from a pass are: the §1.3 overview **thin** (under the 379-word corpus minimum), §3 **thin** on the parameter-list and roadmap constituents, §4 **passing** the required checklist, and the §5 subsection share **over the 0.50 majority ceiling** — see `references/section-budget.md`. A pass that copies "§4 is thin" into a review, or that justifies §3's thinness by message ordering, contradicts the manuscript and has not run.
