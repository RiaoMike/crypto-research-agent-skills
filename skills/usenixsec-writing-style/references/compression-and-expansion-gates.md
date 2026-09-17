# USENIX-Specific Slots — Pointers to the Family Gates

This skill does **not** restate the numeric condensation and expansion gates. The family-wide security-venue gates — abstract and contribution counts, the two overlap indices, the deletion lists, the threat-model precision rule, the overview and design constituent checklists, the design-versus-analysis ratio, and the value-placement rule — live in exactly one place and are owned there:

**`ccs-writing-style` → `references/compression-and-expansion-gates.md`** (the family copy, covering ACM CCS, IEEE S&P and NDSS), and **`ccs-writing-style` → `references/sentence-rewrites.md`** for the rewrite tables.

When a USENIX draft is revised, invoke that file's gates by name and record their counts. The names to invoke are the owning file's own headings: `Gate-Condense-Abstract`, `Gate-Condense-Contributions`, `Gate-Condense-Contributions-vs-Threat-Model`, `Gate-Condense-Deletion-List`, `Gate-Expand-Overview`, `Gate-Expand-Scheme` and `Gate-Expand-Value-Placement`, with the counting basis taken from the same file's method section. Two naming notes, so a reader who greps the owner finds what this file sends them to:

- **`Gate-Expand-Scheme` is this skill's design gate, and that name is not negotiable.** USENIX prose calls the section the "design" or "attack technique" section rather than the construction, so a reader may expect the gate to be named after the design section. It is not: the owning file declares `Gate-Expand-Scheme` as its heading, and this skill invokes that canonical name even where its own prose says "design section". Inventing a second name for one gate is how a pointer stops resolving.
- **There is no separate balance gate.** The owning file folds the mass reading into `Gate-Expand-Scheme` as a labelled diagnosis, so the ratio and the word-count floor are reported as part of that one gate rather than as a gate of their own.

**Round note, kept here because this file is the one in scope.** This pointer file used to name two gates the owner does not declare: a design gate named after the design section, and a separate balance gate. Both are gone — the design gate is written with its canonical name and the balance reading is part of it — and the names it uses are checked by the shared instrument, `python3 skills-work/tools/rule-trace-check.py --fail-on-gap` (C15), which distinguishes a gate this file *invokes* from one it merely *mentions* in a warning. Run it after a gate is renamed or after this file changes the name it uses; expected output `RESULT: PASS [no FAIL]`, exit 0. A skill-local resolver was written for this during t22 and removed under R-20: one instrument, so the two cannot drift.

Every name this file sends a reader to must be a heading or a bold lead-in in the owning file, not a nickname invented here: a pointer is a usable instruction only if its name resolves at the other end. The check is one command per name — `grep -n '^### Gate-' ccs-writing-style/references/compression-and-expansion-gates.md` (or `grep -n '\*\*Gate-' ccs-writing-style/SKILL.md`) must return a hit — and the names above were checked that way. A pointer file may use a name its own prose prefers only when it also names the canonical gate, which is why the note above writes `Gate-Expand-Scheme` even though this skill's prose says "design section": a second, undeclared name for the same gate is exactly the defect this paragraph exists to prevent.

Keeping a single copy is the doctrine both skills publish: a doctrine that says *state it once and point there* cannot itself exist as two copies of the same paragraphs. It also removes a maintenance hazard — one copy edited while the other keeps the old threshold would give two different answers to the same check, and no reader of either file would notice.

**Shared corpus facts are not repeats.** The four-venue medians, the standalone-section shares, the page-limit table and the constituent hit counts are measurements, and both skills may report the same measurement. What must not be duplicated is a rule sentence, and this file carries none of the family's rule sentences.

---

## The checks to run, and who owns each

Invoke these by name. The seven gate rows below are the family gates owned by `ccs-writing-style` → `references/compression-and-expansion-gates.md`; the counts they produce are recorded in the run report.

| Check | Owner | What USENIX adds |
|---|---|---|
| `Gate-Condense-Abstract` | `ccs-writing-style` | nothing — the four-venue null finding forbids a per-venue cap |
| `Gate-Condense-Contributions` | `ccs-writing-style` | nothing, for the same reason |
| `Gate-Condense-Contributions-vs-Threat-Model` | `ccs-writing-style` | the adversary statement may be embedded, so the map is from promised goals to the embedded statement |
| `Gate-Condense-Deletion-List` | `ccs-writing-style` | this venue's plain-register fix: a number and a population rather than a softer adjective |
| `Gate-Expand-Overview` | `ccs-writing-style` | the embedded form is permitted here (56%); the constituent checklist still binds |
| `Gate-Expand-Scheme` (this skill's design gate, canonical in the owner) | `ccs-writing-style` | the embedded-overview permission does not extend to the design constituents: this skill applies the owning checklist unchanged |
| The mass reading inside `Gate-Expand-Scheme` | `ccs-writing-style` | report the ratio with its declared basis; a ratio without a basis is not a result |
| `Gate-Expand-Value-Placement` | `ccs-writing-style` | nothing |
| Counting method and printed basis | `ccs-writing-style` (script) | record the basis the instrument prints, not a remembered one |
| Adversary precision (slot 4) | this skill | 28% standalone rate; precision, not a heading |
| Two mandated sections (slot 2) | this skill | "Ethics considerations" and "Open science" immediately before the References |
| Budget (slot 1) | this skill | 13 pages plus one; the current call governs |
| Overview form (slot 3) | this skill | both forms accepted; the 56% figure is why |

## The four things that are genuinely USENIX's own

Everything below is USENIX-specific: it either does not exist at the sibling venues or takes a different value there. Each item cites the corpus line that measured it, or the policy clause that mandates it.

### 1. Page budget — 13 pages plus one

The body limit is 13 pages plus an additional page for the two mandated sections below, with a 14-page body ceiling for a major revision (`skills-work/corpus/security/statistics.md:175`). The sibling limits for contrast: ACM CCS 12 pages excluding bibliography and appendices, IEEE S&P 13 pages of text plus 5 for references and appendices, NDSS 15 pages all-inclusive (`:220`). Never carry one venue's figure to another, and never measure an author's ePrint copy against any of them (`:21`).

### 2. Two sections the policy mandates, by title and position

A section titled **Ethics considerations** and a section titled **Open science**, each immediately preceding the References section, required in the main body or in the extra page the policy provides (`skills-work/corpus/security/statistics.md:175`; the official clause text is archived at `skills-work/corpus/security/raw/usenix25-submission-policies.html`). No sibling venue mandates this pair — ACM CCS asks for an IRB and responsible-disclosure statement instead, IEEE S&P runs a Research Ethics Committee, and NDSS asks for an ethics-review disclosure plus a disclosure plan (`:176` through `:178`).

This obligation is policy rather than a corpus statistic, and the corpus shows why it must be treated that way: only 2 of 35 security papers contain the word "ethic" and none carries a disclosure narrative (`:182` to `:183`). Do not size these two sections from the literature, and do not carry a previous cycle's wording forward — re-read the call and date the snapshot.

### 3. The overview function may be embedded here

An overview function appears in 27 of 35 corpus papers, but the independent-section form is venue-dependent: IEEE S&P 100%, ACM CCS 100%, NDSS 100%, **USENIX Security 56%** (`skills-work/corpus/security/statistics.md:216`; per-venue presence is 10 of 18 USENIX papers at `:84`).

This skill therefore accepts **both** an independent top-level overview section and an overview subsection or named paragraph inside the introduction, and it must not be read as requiring the section form. What it does not excuse is the overview function's absence: the constituent checklist owned by `ccs-writing-style` is mandatory wherever the overview lives, and the word floor applies when the overview is a standalone section or a named subsection — when it is a named paragraph, report the floor as a ratio to the introduction instead.

### 4. The thin standalone-threat-model habit

A standalone threat or security model section appears in IEEE S&P 25%, ACM CCS 60%, **USENIX 28%** and NDSS 88% of corpus papers (`skills-work/corpus/security/statistics.md:217`; the USENIX row is `:153`). USENIX thus sits second-lowest of the four venues, which is why the placement requirement here is precision rather than a heading: the adversary is stated once, in one place, in prose — parties and trust assumptions, then capabilities, then what is not guaranteed — wherever that statement sits. The size target of 843 words applies only when the section exists on its own (`:157`).

---

## Division of labour, for the reader who lands here

| Skill | Owns | Triggered by |
|---|---|---|
| `ccs-writing-style` | The family-wide security-venue gates and rewrite tables, plus the CCS-specific page budget and IRB/responsible-disclosure statement | ACM CCS, IEEE S&P, NDSS |
| `usenixsec-writing-style` (this skill) | The four slots above: the 13+1 page budget, the two mandated sections and their placement, the permitted embedded overview form, and the thin-standalone-threat-model habit quoted at 28% | USENIX Security |
| `crypto-venue-paper-writing` | The cryptography and LNCS family: CRYPTO, EUROCRYPT, ASIACRYPT, and the corpus-calibrated rules both families share | Cryptography venues and LNCS-style submission |

Run the family gates from `ccs-writing-style` for the counted checks, then apply the four USENIX slots above on top. Where the two would conflict, the venue clause wins: the USENIX page budget and its two mandated sections outrank the family defaults, and nothing in this file overrides a gate that `ccs-writing-style` owns.
