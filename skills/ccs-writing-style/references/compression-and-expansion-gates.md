# Compression and Expansion Gates — CCS

Numeric gates for the security-venue prose this skill covers, with the corpus anchor, sample size, and measurement basis of every number. The skill triggers for **ACM CCS, IEEE S&P, and NDSS**; the USENIX Security form lives in the `usenixsec-writing-style` skill and the cryptography-venue (CRYPTO/LNCS) form in the `crypto-venue-paper-writing` skill, and this file restates neither. The gates below are shared across the four security venues because the corpora measure no significant difference between them in the quantities they gate; the venue-specific rows are marked as such, and the page budget and ethics obligations are read per venue from that venue's own official call.

**Which corpus supplies which number.** The security four-venue corpus (IEEE S&P 4 / ACM CCS 5 / USENIX Security 18 / NDSS 8, 35 papers) supplies the abstract, contribution, overview, threat-model, and scheme-section distributions, because those are shapes the security venues share. The cryptography three-venue corpus (62 tier-A papers, 135 full LaTeX sources) supplies the cross-section mass floor and the subsection-share distribution, because it is the only corpus that measured them with a declared basis. Where a rule could be misread as a CCS-specific constant, the adjacent sentence says so.

## Counting method — reproduce these numbers yourself

Every gate below is a count. The counts are only comparable if the basis is declared, so state it in the report.

- **words** — whitespace-separated alphanumeric tokens of the plain-text rendering; the security corpus counts `[A-Za-z][A-Za-z'\-]*` over PDF-extracted text, the cryptography corpus counts whitespace-separated tokens of the plain-text rendering of the LaTeX source. A word count is always reported with which of the two it is.
- **sentences** — split on `.`/`!`/`?` followed by whitespace or end of text, after protecting common abbreviations and reference numbers from splitting.
- **section words** — a section's words include its subsections unless the report says `direct`; `direct` means the section's own text without its subsections.
- **body words** — all sections before the first appendix section or appendix marker.
- **pages** — measured on the compiled PDF under the venue template of the cycle in hand. The security corpus's page-interval numbers carry a plus/minus one page error because a section boundary was taken at the heading page; treat page-level conclusions as plus/minus one page.
- **an IACR ePrint author version is a different layout from the ACM or IEEE proceedings version.** Nine CCS and S&P corpus papers were read from the author's ePrint version, and the corpus records this at the top of its basis section (`skills-work/corpus/security/statistics.md:21`). Its page numbers must never be compared against an ACM, IEEE, USENIX, or NDSS page limit. Only a compiled PDF under the cycle's own template may be checked against a limit.
- **word-bag Jaccard** — over two texts A and B: |set(words(A)) ∩ set(words(B))| / |set(words(A)) ∪ set(words(B))|, case-folded, punctuation stripped, deduplicated.
- **trigram Jaccard** — the same index over the sets of adjacent word trigrams, which is more sensitive to reused phrasing than the word bag.
- **numeric-literal class** — measured quantities: multi-digit exact decimals, exact success or failure probabilities, bit counts, byte counts, and timings. Small structural integers (a number of parties, a number of protocol rounds, a party index) are not in the class.

`scripts/count_prose_gates.py` in this repository prints these counts for a manuscript or for one extracted span. Run it before rewriting and after; a gate report without before-and-after numbers is incomplete.

### Checking that a pointer still points at something

Pointer resolvability is enforced by **two instruments that must agree**, because they have different reach:

- **In the repository:** the shared checker, `python3 skills-work/tools/rule-trace-check.py --fail-on-gap` (its C15 check). Expected `RESULT: PASS [no FAIL]`, exit 0.
- **Wherever this skill is installed:** `python3 scripts/check_pointer_resolution.py`, which ships with the skill and therefore travels to `~/.dsh/skills`, where `skills-work/tools/` does not exist (R-20a). Expected `RESULT: PASS (n/n gate names resolve)`, exit 0; it prints one `OK`/`FAIL` line per pointer/owner pair, then a `skip` line for every name it excluded.

Both use the same contextual criterion: a gate name that is backticked, or introduced by *invoke / call / apply / run / use / check / grep*, is a **use** and must resolve in the owning file; a name the text warns about is a **mention** and is left alone. That distinction is what lets a pointer file warn "a reader may expect a gate named after the design section; no such gate exists — the owner declares `Gate-Expand-Scheme`" without failing: the warning is excluded as a mention, and the canonical gate the sentence sends the reader to is still checked. Run either instrument after a gate is renamed, after a pointer file changes the name it uses, and before a submission. `scripts/check_pointer_resolution.py --self-test` proves both directions at once (13 cases) if you want to see the guard rather than trust it.

### The instrument's contract — three rules a measuring device must obey

An instrument that reports a clean zero where it matched nothing is worse than no instrument, so the script is bound by three rules and states them in its own output.

1. **The tokenizer is pinned and printed.** The script prints the exact pattern it used in a `tokenizer` field, and the printed `basis` describes that same pattern rather than a basis it never applied. Counts from this script are comparable only to counts from the same pattern on the same text form; a different tokenizer shifts word counts by a few percent, so re-run rather than rescale. Expected agreement between two honest tokenizations is about 4% on a 250-word span.
2. **An unmatched pattern is reported as unmatched.** The contribution list may be written as bullet lines, as bold run-in labels (the form this manuscript uses), or as plain paragraphs. `--items any` finds all three; the report names the mode and, when nothing matched, returns `match_status: "unmatched"` with every per-item field set to null and a `degenerate` note. A null per-item gate is never a pass — the script exits non-zero so a caller cannot read a clean result out of a failed match.
3. **A missing structural input is refused, not defaulted.** `section-mass` with no `--section`, or with a pattern that matches no heading, prints `status: "degenerate"`, leaves `sections` and `ratios` null, names the remedy, and exits non-zero. An empty report is not evidence that a section is well proportioned.

## Thresholds, with anchors

The last column says which corpus the anchor resolves in. **Security** means `skills-work/corpus/security/statistics.md` (35 papers, PDF-extracted text); **Crypto** means `skills-work/corpus/crypto/statistics.md` (62 tier-A papers, LaTeX plain-text rendering). The two corpora count different textual bases, so a number is only comparable to another number from the same corpus; the earlier CCS reference cited `corpus/...` shorthand, and the full paths are used here so every anchor resolves from the workspace root.

| Gate quantity | Threshold | n | Basis | Anchor | Corpus |
|---|---|---|---|---|---|
| Abstract words | at most **220** (corpus median; q1 173, q3 241, max 362) | 35 | words, PDF-extracted text | `skills-work/corpus/security/statistics.md:31` | Security |
| Abstract sentences | at most **9** (q1 8, q3 11) | 35 | sentences | `skills-work/corpus/security/statistics.md:32` | Security |
| Mean words per abstract sentence | at most **24.1** (the corpus median; 1.25× would be 30, offered as a tolerance band rather than a gate) | 35 | words/sentence | `skills-work/corpus/security/statistics.md:33` | Security |
| Longest abstract sentence | at most **40** (crypto-corpus median; q3 49) | 59 | words | `skills-work/corpus/crypto/statistics.md:124` | Crypto |
| Contribution items | at most **5**, absolute **10** (q1 3, q3 6, max 10) | 22 | items | `skills-work/corpus/security/statistics.md:58` | Security |
| Words per contribution item | at most **72** (q1 22, q3 150, max 574) | 22 | words | `skills-work/corpus/security/statistics.md:59` | Security |
| Contribution items carrying a number | median **66.7%** — a target, not a floor | 22 | share | `skills-work/corpus/security/statistics.md:60` | Security |
| Contributions vs abstract, word-bag Jaccard | at most **0.20** (median 0.201, max 0.309) | 22 | word sets | `skills-work/corpus/security/statistics.md:61` | Security |
| Contributions vs abstract, trigram Jaccard | at most **0.019** (the corpus median; max 0.038) | 22 | trigram sets | `skills-work/corpus/security/statistics.md:62` | Security |
| Abstract process narration | **0** instances tolerated | 35 | manual + lexical scan | `skills-work/corpus/security/statistics.md:48` | Security |
| Contributions vs threat model, word-bag Jaccard | at most **0.20** | 22 | word sets | `skills-work/corpus/security/statistics.md:61` | Security |
| Technical overview, minimum size | at least **596** words (the corpus minimum; q1 854, median 1535.5) | 20 | words | `skills-work/corpus/security/statistics.md:92` | Security |
| Technical overview, expected size | median **1535.5** words; CCS-only median **1058** | 20 / 5 | words | `skills-work/corpus/security/statistics.md:92`, `:219` | Security |
| Technical overview, presence | **5 of 5** CCS papers present an overview function | 5 | manual section audit | `skills-work/corpus/security/statistics.md:82` | Security |
| Overview components | **5** required components | 25 | manual deep read | `skills-work/corpus/security/statistics.md:104` | Security |
| Scheme section, expected size | median **3481** words (corpus and CCS-only coincide) | 35 / 5 | words | `skills-work/corpus/security/statistics.md:119`, `:127` | Security |
| Scheme section, required constituents | **5** constituents at 10–20 of 25 papers each | 25 | regex count over deep reads | `skills-work/corpus/security/statistics.md:131` | Security |
| Scheme/analysis word ratio | at least **0.44** (q1; median 0.89, only 40% above 1) | 10 | words, direct | `skills-work/corpus/crypto/statistics.md:285` | Crypto |
| Abstract length, four-venue medians | S&P 214 / CCS 205 / USENIX 212 / NDSS 227.5; ranges fully overlapping — the null finding that forbids per-venue caps | 35 | words | `skills-work/corpus/security/statistics.md:213` | Security |
| Standalone overview section share | S&P 100% / CCS 100% / NDSS 100% / **USENIX 56%** | 35 | section audit | `skills-work/corpus/security/statistics.md:216` | Security |
| Standalone threat-model section share | S&P 25% / CCS 60% / USENIX 28% / NDSS 88% | 35 | section audit | `skills-work/corpus/security/statistics.md:217` | Security |
| Body page limits, official CFP | S&P 13 (+5) / CCS 12 excluding refs / USENIX 13 (+1) / NDSS 15 all-inclusive | — | official calls | `skills-work/corpus/security/statistics.md:220` | Security |
| Scheme/design section words | at least **2663** words (corpus q1 of the design-section word count; the implied share of a 13800-word body is 0.19) | 35 | words | `skills-work/corpus/security/statistics.md:119` | Security |
| Threat-model section size | median **843** words (q1 769, q3 1041) | 16 | words | `skills-work/corpus/security/statistics.md:157` | Security |
| Largest child subsection share | flag above the corpus q3 **0.607** (median 0.491, p90 0.774) | 561 | words | `skills-work/corpus/crypto/statistics.md:330` | Crypto |
| CCS body page limit | **12** pages, excluding bibliography, marked appendices, supplementary material — policy, verify at execution time | — | official call | `skills-work/corpus/security/statistics.md:177` | Security |

## Condensation gates

### Compression is an action list, not a length knob

The measured lengths are ceilings to check, not the instrument that produces the cut. A draft is compressed by doing these three things and re-measuring, in this order:

1. **Delete research-process narration.** The corpus contains 0 of 35 papers narrating process in the abstract, the contributions, or the overview (`skills-work/corpus/security/statistics.md:48`), so every stage name, round label, attempt count, and abandoned-design inventory is a deletion candidate rather than a judgement call.
2. **Delete abstract-versus-contributions duplication.** Measure the two overlap indices (gate above) and give each shared span a disposition — delete, merge into one statement, or move into the body with a forward reference. This is the mechanical half of the condensation, and it is where over-length abstracts actually lose their words.
3. **Replace adjectives with numbers, or delete them.** A claim that cannot carry a number carries a scope instead ("on this platform, at this version"); one that can carry neither is deleted.

Length caps do not enter this list because the corpus does not support a per-venue one: the four security venues' abstract medians are 205 to 227.5 words with fully overlapping ranges (`skills-work/corpus/security/statistics.md:213`), and the crypto venues sit at a median of 210 (`skills-work/corpus/crypto/statistics.md:121`). Setting a different hard cap per venue would encode a difference the corpora do not contain.


### Gate-Condense-Abstract

**Input** the abstract. **Output** words, sentences, longest sentence, per-paragraph move labels (context / gap / build / result), and the share of words in each move.

**Pass:** words ≤ 220 unless a recorded reason names why the venue's own distribution supports more; sentences ≤ 9; mean sentence length ≤ 30 words; longest sentence ≤ 40 words; at least one paragraph performs the build move by naming the artifact, protocol, or mechanism the paper contributes; zero process-narration spans; no sentence shared verbatim with the contributions list.

**Fail:** every number inside the caps but no paragraph naming what is built; a 220-word abstract whose analysis paragraphs hold over half the words and whose build paragraph is a single clause. The reported defect has exactly this shape — a 247-word abstract in four paragraphs, three of which report analysis outcomes — and it passes a bare length cap, so a length cap alone never closes this gate.

**Near-miss to catch:** an abstract at 219 words achieved by deleting the construction sentence.

### Gate-Condense-Contributions

**Input** the contribution block and the abstract. **Output** item count, words per item, list total, word-bag Jaccard, trigram Jaccard, and the list of shared trigrams with the two line numbers of each.

**Pass:** items ≤ 5 (≤ 10 absolute); words per item ≤ 72 with at most one item above 150; list ≤ 250 words; word-bag Jaccard ≤ 0.20; trigram Jaccard ≤ 0.019; each duplicated span given a disposition (delete, merge, or move into the body with a forward reference).

**Fail:** an item that restates an abstract sentence with the words rearranged and no new claim; a total over 250 words with no reported number; a 0.30 Jaccard list left in place. Uneven items — two over 100 words and the rest under 10 — also fail: the measured quartiles are 22 and 150, so unequal items must be a deliberate decision, not an accident.

**Note on the metric's limit.** The corpus itself sits at a word-bag Jaccard of 0.201, so a rule that demanded near-zero overlap would fail the published literature. The threshold is the corpus median: it catches the draft whose contributions block is the abstract rewritten, and it passes the draft whose contributions recycle terminology while making distinct claims. The trigram index is the sharper instrument for the second failure — recycled sentences move it, recycled terminology barely does, which is why the corpus separates them so widely (0.201 against 0.019 at the median).

### Gate-Condense-Contributions-vs-Threat-Model

**Placement rule first.** The requirement is that the adversary statement is **explicit and locatable** — stated once, in one place, in prose — not that it occupies its own section. Standalone-section share measured across the four venues: S&P 25% / **CCS 60%** / USENIX 28% / NDSS 88% (`skills-work/corpus/security/statistics.md:217`). CCS is the venue where the standalone form is the majority habit, which is why this gate states a default rather than a universal rule: a draft that states the model in the system-overview subsection and satisfies every requirement below has not failed. A model that is scattered across the design and evaluation sections has failed regardless of where the headings are.

**Input** the contribution block and the threat or security model section. **Output** word-bag Jaccard between them, a table mapping each promised security goal in the contributions to the threat-model sentence stating what the adversary may do, and the list of capabilities, assumptions, or non-goals the threat model adds.

**Pass:** Jaccard ≤ 0.20; every promised goal has a threat-model counterpart; the threat model contributes at least one element the contributions do not state.

**Fail:** a threat-model section that opens by re-listing the parties the contributions already listed and adds nothing; a threat model consisting only of the security goals restated from the contributions, with no statement of what the adversary can do. In the corpus the capability list is written as assumption-plus-decidable-statement prose, not as a table (`skills-work/corpus/security/statistics.md:165`), and a threat-model paragraph that begins by re-enumerating the parties is the observed near-miss (`skills-work/corpus/security/statistics.md:162`).

### Gate-Condense-Deletion-List

**Input** abstract, contributions, introduction, and every claim sentence. **Output** two lists: surviving adjectives with their supporting number or scope, and surviving process-narration spans with a decision per span.

**Marketing adjectives to hunt:** highly effective, trivial, negligible, completely, significantly, practical, efficient, robust, scalable, guarantees, breakthrough, seamless, powerful, state-of-the-art (the last one only fails when no companion number or scope follows it).

**Research-process narration to hunt:** stage or phase names, round labels, attempt counts, abandoned-design inventories, letter-number identifiers from a planning register, citation-key placeholders, and "we first tried … then" narratives. The corpus contains 0 of 35 abstracts narrating process (`skills-work/corpus/security/statistics.md:48`), across all four venues.

**Pass:** every adjective carries a measurement or a scope, or is deleted; zero process-narration spans outside a sentence that quotes the pattern in order to forbid it.

**Fail:** one adjective left bare, one internal identifier left standing as though it were a paper concept. A planning register's labels are not the paper's names, and readers outside the project cannot resolve them.

## Expansion gates

### Gate-Expand-Overview

**Input** the overview span. **Output** word count, line count, whether it is standalone or nested, and each of the five components marked present with a line number or absent.

**Required components, each with its corpus anchor:**

1. an intuition statement naming the goal in plain terms;
2. a mechanism sentence explaining why the approach works, not only what it is;
3. one named sub-block per subproblem, its title naming the subproblem it solves;
4. a forward reference from each sub-block to the section that carries the formal detail;
5. an early statement of the cost, leakage, or assumption the mechanism pays for its result.

All five appear in the required shape in the corpus deep reads (`skills-work/corpus/security/statistics.md:104`), and the named sub-block pattern is confirmed in the cryptography corpus, where an overview carries 5 named blocks at the median and 11 at the third quartile (`skills-work/corpus/crypto/statistics.md:269`).

**Pass:** at least 596 words — the corpus minimum, the floor a draft must clear to be comparable to the thinnest overview in the sample (the first quartile is 854) — plus all five components and at least three named sub-blocks.

**Fail:** four of five components; a table-of-contents overview ("Section 3 presents X, Section 4 proves Y") with no mechanism sentence; a 1100-word overview with a single block — length without components does not pass. The reverse also fails: all five components in 400 words means the mechanism is asserted, not explained — 400 is below the 596-word corpus minimum, so the word floor catches that case too.

**CCS-specific note.** All five CCS corpus papers present an overview function, so this gate always applies at CCS and cannot be resolved by arguing that the venue skips overviews. Where the overview is a subsection of the introduction rather than a top-level section, the word floor still applies to that subsection; where it is a short named paragraph rather than a subsection, the component checklist still applies and the floor is reported as a ratio to the introduction instead of an absolute.

### Gate-Expand-Scheme

**Input** the scheme section — the section describing what is built, whatever its title. **Output** word count on a declared basis, the scheme/analysis ratio, the scheme share of body words, and each required constituent marked present with a line or absent.

**Why the title cannot be the key.** 69% of tier-A papers (43 of 62) have no section whose title contains the word "Construction" (`skills-work/corpus/crypto/statistics.md:112`), and only 46.8% of tier-A papers have any construction-role body section (`skills-work/corpus/crypto/statistics.md:291`). A rule keyed on the title "Construction" misses most of the literature.

**Required constituents, counted over 25 deep reads** (`skills-work/corpus/security/statistics.md:131`):

1. step ordering — in what order the protocol or attack proceeds (20 of 25);
2. a named object, relation, or function defined once and reused (19 of 25);
3. a complexity, communication, or cost expression (17 of 25);
4. the reason for a parameter, size, or field choice (15 of 25);
5. a protocol or algorithm box, or a figure carrying the message flow (10 of 25 for a box, more when flow figures are counted).

Plus the mechanism-explanation sentence class: the corpus holds it in the deep reads but the phrase-level count under-counts it (`skills-work/corpus/security/statistics.md:137`), so it is required per mechanism and is never validated by the phrase count alone.

**Pass:** all five constituents present; at least one mechanism sentence per mechanism; design/analysis word ratio ≥ 0.44; design-section words ≥ 2663 on the same basis.

**Fail:** a scheme section that is a synthesis sentence plus a parameter table; boxes with no step ordering; a ratio inside the floor while three constituents are missing — the ratio and the checklist are independent, and passing one does not excuse the other. A constituent that genuinely does not apply must be named with its reason in the report; silence fails.

**Reading the numbers — a diagnosis, not a second gate.** This gate has one pass/fail decision, and it is the one above. The mass figures are read as a diagnosis and reported alongside it: a scheme section whose ratio to the analysis section falls under 0.44, or whose word count falls under 2663 on the same basis, is described as thin, with the missing constituents named. That reading is the instrument for the reported imbalance between a thin protocol-and-construction pair and a thick analysis section, and it is deliberately expressed as a judgement about proportion rather than as a separate numerical gate — a second gate with the same thresholds would fail the same drafts twice and suggest a distinction that does not exist. Report the ratio with its basis every time; the same manuscript measures differently in lines and in words, so a ratio without its basis is not a result.

**What must not be written into this rule.** Not "the scheme must be longer than the analysis": the measured ratio has a median of 0.89 and only 40% of pairs above 1 (`skills-work/corpus/crypto/statistics.md:285`), so a floor above the median contradicts the corpus. Also not a target taken from a manuscript: a manuscript's post-fix ratio is not a constant, and the corpus distribution governs.

### Gate-Expand-Value-Placement

**Input** every section, split into a design-and-analysis region and an evaluation-and-parameters region. **Output** the numeric literals of the measured-quantity class found in each region, with line numbers, and the disposition of each relocated value.

**Pass:** measured values live in the evaluation, parameters, and implementation sections; the design and proof regions carry symbolic or asymptotic expressions; a measured value that must move is moved *with its digits and its provenance*, is never rounded away and never deleted, and the receiving section says where it came from.

**Fail:** an exact success probability or a long decimal expansion sitting in a construction paragraph with no location statement; a value replaced by an adjective in the name of style. The cheapest way to make a construction look detailed is to pour measured numbers into it, and that recreates a known defect class. Precision in the design section belongs to definitions, not to measurements.

## Policy anchors per venue — verify at execution time

Policy numbers are cycle-specific. Record a dated policy snapshot before writing any budget claim, and quote the current call **of the venue in hand**; this skill covers three of them, and the three limits differ.

| Venue this skill covers | Body limit | Ethics / disclosure obligation | Source |
|---|---|---|---|
| ACM CCS | 12 pages, excluding bibliography, well-marked appendices, and supplementary material | Authors are expected to convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed; optional artifact evaluation | `skills-work/corpus/security/statistics.md:177`; `skills-work/corpus/security/raw/ccs2024-cfp.html` |
| IEEE S&P | up to 13 pages of text and up to 5 pages for references and appendices, 18 in total | Research Ethics Committee; ethical considerations for vulnerability disclosure; IRB disclosure for human subjects | `skills-work/corpus/security/statistics.md:176`; `skills-work/corpus/security/raw/sp2025-cfp.html` |
| NDSS | 15 pages in total, including references and appendices; double-blind | Disclose ethics review where the work has ethical or legal impact and discuss the plan for responsible disclosure of a high-impact vulnerability; artifact evaluation | `skills-work/corpus/security/statistics.md:178`; `skills-work/corpus/security/raw/ndss2025-cfp.html` |
| USENIX Security (owned by the other skill) | 13 pages plus one page for the mandated Ethics considerations and Open science sections | Two titled sections immediately preceding References | `skills-work/corpus/security/statistics.md:175`; `skills-work/corpus/security/raw/usenix25-submission-policies.html` |

An S&P or NDSS draft must not be compressed to the CCS row, and a CCS draft must not adopt the NDSS all-inclusive limit. State which venue the draft targets before any budget statement.

- **Body limit.** ACM CCS '24: no more than **12** pages excluding the bibliography, well-marked appendices, and supplementary material (`skills-work/corpus/security/statistics.md:177`).
- **Anonymity.** Anonymous review; papers not properly anonymized may be rejected without review (`skills-work/corpus/security/statistics.md:177`).
- **Ethics and disclosure.** Authors are expected to convince reviewers that proper procedures such as IRB approval or responsible disclosure have been followed (`skills-work/corpus/security/statistics.md:177`).
- **Artifact evaluation.** Optional, separate from the paper limit (`skills-work/corpus/security/statistics.md:177`).
- **Adaptive posture.** Only 3 of 35 corpus papers discuss adaptive attacks (`skills-work/corpus/security/statistics.md:185`); the corpus cannot set a size, but the absence is what reviewers notice.
- **Official originals for the numbers above.** The page limits are read from the calls archived at `skills-work/corpus/security/raw/ccs2024-cfp.html`, `sp2025-cfp.html`, `ndss2025-cfp.html`, and `usenix25-submission-policies.html` (digest also recorded at `skills-work/corpus/security/statistics.md:220`). Quote the current cycle's page, not the archived one, and date the snapshot.
- **ePrint is a different layout.** Nine CCS and S&P corpus papers were read from the author's IACR ePrint version (`skills-work/corpus/security/statistics.md:21`). Never measure an ePrint PDF against an ACM, IEEE, USENIX, or NDSS page limit.

## Division of labour with the neighbouring skills

- **`crypto-venue-paper-writing`** owns venue structure for the cryptography venues (CRYPTO, EUROCRYPT, ASIACRYPT, LNCS), its abstract formula, its section budget, and the de-AI grep checklist. This skill points there for the de-AI list rather than duplicating it, and states only what differs at CCS: 12 pages excluding bibliography and appendices, the IRB and disclosure statement, the standalone threat-model default, and the overview and scheme gates above.
- **`usenixsec-writing-style`** owns the USENIX Security form: the mandatory Ethics considerations and Open science sections, their placement, and the 13-page-plus-one budget. The shared numeric gates (abstract, contributions, overview floor, scheme constituents, ratio floor) are identical, and the corpus says why: the four security venues show no significant difference in abstract length (`skills-work/corpus/security/statistics.md:50`) or a CCS-specific contribution-item threshold (the CCS subsample is 3 papers, `skills-work/corpus/security/statistics.md:70`), so inventing a per-venue abstract cap would be a fabricated difference. What differs between CCS and USENIX is measured at `skills-work/corpus/security/statistics.md:216-221`: overview presence (100% CCS against 56% USENIX), threat-model section presence (60% against 28%), and the policy budget and ethics obligations.
- **`crypto-paper-writing`** owns drafting workflow. It is not restated here.
