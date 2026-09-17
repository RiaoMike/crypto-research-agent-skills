#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""count_venue_gates.py — the measurable gates of the crypto-venue writing skill.

This is the instrument behind `skills/crypto-venue-paper-writing/SKILL.md`.  It exists
because the guard added for the construction-to-analysis ratio is a requirement that
nothing could violate while the skill shipped no process: a rule that says "do not print
a band verdict here" is unenforceable unless something can print one.

It implements the numeric gates the skill states, on a named twin, with an explicit
status for every gate:

    measured   a number was produced
    degenerate the `direct` basis collapsed onto heading lines for a contributing
               section, so the ratio must not receive a band verdict
    unmatched  a named region or section could not be located in the twin

A gate never fails silently.  The exit codes distinguish the two ways this program can
refuse, so that neither a broken measurement nor a failed verdict is invisible to a
pipeline that keys on exit status:

    0   every gate was `measured`.  NOTE: a *breach* of a stated threshold is a finding,
        not an error, so 0 means "measured cleanly", never "compliant".
    1   VERDICT failure — the `--dename` pass condition was FAIL (unresolvable
        identifiers remain).  This is the one mode that renders a verdict.
    2   MEASUREMENT failure — some gate was `degenerate` or `unmatched`, so a band
        verdict must not be printed for it.  Also returned for a missing input file.

Every gate prints its own status on its own axis (`measured` / `degenerate` /
`unmatched`), and a gate with nothing to measure is never reported as satisfied.

Two gates are deliberately TWO-SIDED rather than caps, because a cap cannot see a section
that was never written and cannot refuse a structure that makes its own criterion
unmeasurable:
    related-work-floor   a floor (392 words, the median of n=3) as well as the
                         section-budget ceilings;
                         `unmatched` when no region is supplied and no heading matches, so
                         absence is reported rather than passed
    abstract-paragraphs  a floor of 2 paragraphs; with fewer, `abstract-build-share` is
                         `unmatched` instead of printing a share that can only be 0.0 or 1.0
    contributions-block / contributions-items print the SAME six-clause contract verdict,
                         so the block gate cannot print `ok` while an item clause fails
                         (R-VENUE-05's two-sided pass condition)

Every threshold and every basis in this file is quoted from the skill's own reference
files, which remain the authority:
    references/compression-rules.md   abstract and contribution caps, duplication metric
    references/expansion-rules.md     overview floors, ratio bands, the degeneracy guard
    references/section-budget.md      largest-child ceiling, the Related Work floor,
                                      and its exemption
    references/numeric-placement.md   (not a numeric gate; not implemented here)

Usage:
    python3 count_venue_gates.py --manuscript research-work/paper/final-paper.md
    python3 count_venue_gates.py --manuscript <twin> --items bold     # or any|paragraph|bullet|none
    python3 count_venue_gates.py --manuscript <twin> --related 69-75   # related-work span
    python3 count_venue_gates.py --manuscript research-work/paper/latex/main.tex --twin tex
    python3 count_venue_gates.py --manuscript ... --json
    python3 count_venue_gates.py --self-test
    python3 count_venue_gates.py --self-scan
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Thresholds — each quoted from the skill's reference files.  Do not invent: a
# threshold that cannot be traced to skills-work/corpus/*/statistics.md is a fabricated
# threshold (captain ruling R-3).
# ---------------------------------------------------------------------------
ABSTRACT_WORDS_CAP = 210          # compression-rules.md: crypto/statistics.md:121, n=59
ABSTRACT_BUILD_SHARE_FLOOR = 0.56  # crypto/statistics.md:165, n=15 (hand-coded)
ABSTRACT_LONGEST_SENTENCE_CAP = 40  # crypto/statistics.md:124, n=59
# The abstract's PARAGRAPH floor, not a count-to-report.  The corpus's abstract-paragraph
# row has min 1, q1 2, median 2 (crypto/statistics.md:123, n=59) and 0.78 of tier-A
# abstracts carry more than one paragraph (crypto/statistics.md:128, n=59), so a
# single-paragraph abstract is in the corpus's bottom decile of structure AND makes the
# skill's own four-move annotation and build share unmeasurable: with one paragraph there
# is one move, so the share can only be 0.0 or 1.0 by construction.  Both halves of the
# corpus evidence are inlined here because a threshold with no sample size is fabricated
# (R-3) and because this file must stay self-contained (R-13).
ABSTRACT_PARAGRAPH_FLOOR = 2      # crypto/statistics.md:123 and :128, n=59
BULLETS_RANGE = (2, 5)            # crypto/statistics.md:196, n=50
BLOCK_WORDS_CAP = 146             # crypto/statistics.md:197, n=50
BULLET_WORDS_CAP = 29.5           # PER-ITEM cap, crypto/statistics.md:198, n=214
PER_BULLET_CAP = BULLET_WORDS_CAP  # alias kept for continuity
LONGEST_BULLET_CAP = 57.5         # crypto/statistics.md:199, n=50
BLOCK_ABSTRACT_RATIO_CAP = 0.81   # crypto/statistics.md:200, n=50
SHARED_NGRAM_N = 6                # crypto/statistics.md:206-207
SHARED_NGRAM_CAP = 0              # crypto/statistics.md:211 (median 0; max 6)
OVERVIEW_WORDS_FLOOR = 379        # expansion-rules.md: crypto/statistics.md:239, n=18
OVERVIEW_LINES_FLOOR = 99         # crypto/statistics.md:240, n=18
OVERVIEW_SHARE_FLOOR = 0.25       # crypto/statistics.md:241, n=18
# Related Work floor — section-budget.md §The Related Work floor.  The crypto corpus has
# NO related-work size distribution (crypto/statistics.md:413 records `related` with a
# zero count, and its per-paper table has no related-work column), so this floor cannot be
# quoted from statistics.md the way every other threshold in this file is.  It is quoted
# from the only measurement that exists: the three comparators of the t36 structural
# comparison that expose a related-work section at all, at 228 / 392 / 1067 words on the
# whitespace-token basis, n=3.  The value is the sample's MEDIAN, 392, per the captain's
# ruling on t37; the observed minimum and maximum travel with it as context rather than as
# a second threshold.  Raw values: skills-work/eval/metrics.json ->
# percentiles["M5.related_work_words"] (stable, machine-generated) and
# comparators[14,15,19].M5.related_work_words; the measurement is reported in
# skills-work/eval/structural-comparison.md, whose M5 table states the n=3.
# n=3 is small and is stated wherever the number is printed: the gate never prints the
# floor without it.
RELATED_WORK_WORDS_FLOOR = 392    # median of n=3 (228 min / 1067 max), ws basis
RELATED_WORK_N = 3                # the sample size, printed with every use
RELATED_WORK_RANGE = (228, 1067)  # observed spread in the same n=3, context only
# The same heading test the sibling measuring instrument uses
# (skills-work/eval/measure-structure.py, the `RELATED_RE` pattern
# `related work|prior work|related literature`, case-insensitive, matched anywhere in the
# heading — cited by name, not by line, per R-23) so that the two instruments cannot
# disagree about which section they are measuring.  R-24.1: a gate implemented in two
# instruments is not re-invented in the second one.
RELATED_WORK_RE = re.compile(r"related work|prior work|related literature", re.I)
RATIO_FAIL_BELOW = 0.44           # crypto/statistics.md:285, n=10 (words, direct)
RATIO_PASS_AT = 0.89              # crypto/statistics.md:285 (median)
CEILING_MAJORITY = 0.50           # section-budget.md: crypto/statistics.md:330
CEILING_OUTLIER = 0.65            # crypto/statistics.md:334
DEGENERATE_DIRECT_WORDS = 20      # expansion-rules.md §Degenerate: "smaller than 20 words"

# A section's `direct` span is the section's own text with its immediate children's spans
# removed (crypto/statistics.md:18-19).  When prose lives in the subsections, that
# subtraction leaves heading lines, and the number stops measuring text.
WS = re.compile(r"\S+")
ALNUM = re.compile(r"[A-Za-z0-9]+")
SENTENCE = re.compile(r"[.!?](?=\s|$)")
MD_HEAD = re.compile(r"^(#{2,3})\s+(.*)$")
TEX_HEAD = re.compile(r"\\(sub)?section\*?\{(.*)\}")


def count_words(text: str, basis: str) -> int:
    """`ws` = whitespace tokens; `alnum` = the corpus basis (statistics.md:12)."""
    return len(WS.findall(text)) if basis == "ws" else len(ALNUM.findall(text))


def headings(lines: list[str], twin: str) -> list[dict]:
    """Every heading with its line number and level, in file order."""
    out = []
    rx = MD_HEAD if twin == "md" else TEX_HEAD
    for i, line in enumerate(lines, 1):
        m = rx.search(line)
        if not m:
            continue
        if twin == "md":
            level = 2 if len(m.group(1)) == 2 else 3
            title = m.group(2).strip()
        else:
            level = 3 if m.group(1) else 2
            # the greedy title capture swallows the label's closing brace, so strip a
            # TRAILING label rather than a brace-balanced one
            raw_title = re.sub(r"\\label\{[^}]*\}?\s*$", "", m.group(2))
            title = re.sub(r"\\[a-zA-Z]+\s*", "", raw_title).replace("{", "").replace("}", "").strip()
        out.append({"line": i, "level": level, "title": title})
    return out


def spans(heads: list[dict], total: int) -> list[dict]:
    """Each heading paired with the last line before the next heading at <= its level."""
    out = []
    for i, h in enumerate(heads):
        end = total
        for nxt in heads[i + 1:]:
            if nxt["level"] <= h["level"]:
                end = nxt["line"] - 1
                break
        out.append({**h, "end": end})
    return out


def find_section(heads: list[dict], pattern: str) -> dict | None:
    """First section whose title matches `pattern` (case-insensitive)."""
    rx = re.compile(pattern, re.I)
    for h in heads:
        if rx.search(h["title"]):
            return h
    return None


def direct_words(lines: list[str], sec: dict, all_spans: list[dict], basis: str) -> tuple[int, int]:
    """Return (direct words, number of heading-only lines) for a section.

    Direct = the section's span minus the spans of its immediate children.
    """
    children = [c for c in all_spans if c is not sec and sec["line"] < c["line"] <= sec["end"]]
    covered = set()
    for c in children:
        covered.update(range(c["line"], c["end"] + 1))
    own = [lines[n - 1] for n in range(sec["line"], sec["end"] + 1) if n not in covered]
    words = count_words("\n".join(own), basis)
    heading_only = sum(1 for l in own if l.strip().startswith(("#", "\\section", "\\subsection"))
                       or not l.strip())
    return words, len(own) - heading_only


def is_degenerate(direct_w: int, prose_lines: int, sec: dict, lines: list[str], basis: str) -> bool:
    """expansion-rules.md §Degenerate: smaller than its own heading, or under 20 words,
    or its direct span holds no running prose."""
    heading = count_words(lines[sec["line"] - 1], basis)
    return direct_w < heading or direct_w < DEGENERATE_DIRECT_WORDS or prose_lines <= 0


def ngrams(text: str, n: int) -> Counter:
    toks = [t.lower() for t in ALNUM.findall(text)]
    return Counter(tuple(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1)))


# --------------------------------------------------------------------------
# Contribution-item matching: PORTED from the style-side instrument
# (ccs-writing-style/scripts/count_prose_gates.py) rather than re-implemented,
# per captain ruling R-24.1 — a failure mode fixed in one instrument must be
# propagated to every sibling instrument implementing the same gate.
#
# F8 (silent zero on the manuscript's own item form) is the failure mode this
# port fixes: this skill's manuscript writes its contributions as BOLD RUN-IN
# items (`**(1) A scheme definition.** …`), which a bullet-only matcher does not
# see. A per-item gate that matches nothing cannot fail, so it must never report
# a clean count: `match_status: unmatched` is turned into an `unmatched` gate and
# a non-zero exit.
# --------------------------------------------------------------------------
# One tokenizer per run: the DECLARED basis.  The per-item word counts are reported on
# the same basis as every other number in this instrument, and the pattern is printed
# with them, so no figure has to be re-interpreted against an outside instrument.
BASIS_PATTERN = {"ws": r"\S+", "alnum": r"[A-Za-z0-9]+"}
BASIS_LABEL = {"ws": "whitespace tokens", "alnum": "alphanumeric tokens"}
STYLE_PER_ITEM_CAP = 72   # cross-instrument comparison figure only; NOT a venue
                          # threshold (the venue per-item cap is BULLET_WORDS_CAP)
BULLET_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BOLD_ITEM = re.compile(r"^\s*(?:[-*+]\s+)?\*\*(?P<label>[^*]{1,160})\*\*")
ITEM_MODES = ("bullet", "bold", "paragraph", "any", "none")


def item_prose(text: str) -> str:
    """Markup and dash normalisation, ported: the two instruments must agree."""
    cleaned = re.sub(r"\\[a-zA-Z]+\*?(?:\{[^{}]*\})?", " ", text)
    cleaned = cleaned.replace("--", " ").replace("---", " ")
    cleaned = cleaned.replace("\u2014", " ").replace("\u2013", " ")
    return re.sub(r"[\\$*_`{}]", " ", cleaned)


def item_body(text: str) -> str:
    """Drop a leading heading line, as the style instrument's clean_span does, so the
    two instruments' words_total are comparable on the same basis."""
    lines = text.split("\n")
    if lines and re.match(r"^\s*#{1,6}\s", lines[0]):
        lines = lines[1:]
    return "\n".join(lines)


def item_words(item: str, basis: str = "ws") -> int:
    """Per-item word count on the DECLARED basis.

    Deliberately NOT a separate tokenizer: the per-item numbers must be counted by the
    same tokenizer as every other number this run prints, or the gate becomes
    incomparable with the report it sits in.  On the whitespace basis this gives the
    calibration manuscript's per-item lengths [218, 55, 101, 276, 85, 145].
    """
    return count_words(item, basis)


def contribution_items(text: str, mode: str) -> tuple[list[str], str]:
    """Return (items, match_status). Ported verbatim in behaviour from the style side.

    match_status is "matched" when the requested pattern found at least one item and
    "unmatched" when it found none. An unmatched result is never a clean count.
    """
    if mode == "none":
        return [], "unmatched"
    if mode == "bullet":
        lines = [l for l in text.split("\n") if BULLET_ITEM.match(l)]
        return lines, ("matched" if lines else "unmatched")
    if mode == "bold":
        lines = [l.strip() for l in text.split("\n") if BOLD_ITEM.match(l)]
        return lines, ("matched" if lines else "unmatched")
    if mode == "paragraph":
        blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
        return blocks, ("matched" if blocks else "unmatched")
    if mode == "any":
        bullets_ = [l for l in text.split("\n") if BULLET_ITEM.match(l)]
        if bullets_:
            return bullets_, "matched"
        bolds = [l.strip() for l in text.split("\n") if BOLD_ITEM.match(l)]
        if bolds:
            return bolds, "matched"
        blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
        return blocks, ("matched" if blocks else "unmatched")
    return [], "unmatched"


def bullets(text: str) -> list[str]:
    """Kept as a thin wrapper over the ported matcher; the earlier self-test uses it."""
    return contribution_items(text, "bullet")[0]


CONTRACT_CLAUSES = 6


def contributions_verdict(bw: int, aw: int, ratio: float, items: list[str],
                          item_status: str, basis: str, shared_n: int | None
                          ) -> tuple[list[str], list[str], dict]:
    """Evaluate the contribution-list contract ONCE, as a conjunction.

    Returns `(breaches, unmeasured, evidence)`.  The contract is deliberately evaluated in
    one place and printed by both contribution gates, because the two gates used to print
    two different verdicts: `contributions-block` reported `ok` on the strength of the word
    count and the block/abstract ratio alone, so a block that broke the item count, the
    longest item and the per-item cap on every item still carried the word `ok` — which is
    how the 139-word single-item shape t36 measured reads as passing.  `R-VENUE-05` states
    the two-sided form in the rule text ("不通过=只给上限不给下限" / a bullet range written as
    an interval, `2 to 5`); this function is that rule made executable.

    A clause that cannot be evaluated is returned in `unmeasured`, never omitted: a gate
    that silently drops a clause it cannot check is the F8/F9 failure family again.
    """
    ev: dict = {}
    bre: list[str] = []
    unm: list[str] = []

    # 1. item count — two-sided, and the lower bound is the one that was missing
    if item_status != "matched":
        unm.append(f"item count in {BULLETS_RANGE} (no item matched, mode found none)")
    else:
        n = len(items)
        ev["items"] = n
        if not (BULLETS_RANGE[0] <= n <= BULLETS_RANGE[1]):
            bre.append(f"items {n} outside {BULLETS_RANGE}")

        # 2. longest item
        iwords = [item_words(i, basis) for i in items]
        imax = max(iwords, default=0)
        ev["per_item"] = iwords
        ev["longest"] = imax
        if imax > LONGEST_BULLET_CAP:
            bre.append(f"longest item {imax} > {LONGEST_BULLET_CAP} (venue cap)")

        # 3. per-item cap — independent of the item count (R-24a.1)
        over_cap = sum(1 for w in iwords if w > BULLET_WORDS_CAP)
        ev["over_cap"] = over_cap
        if over_cap:
            bre.append(f"{over_cap} item(s) over {PER_BULLET_CAP} (venue per-item cap); "
                       f"per-item words: {iwords}")

    # 4. whole block
    ev["block_words"] = bw
    if bw > BLOCK_WORDS_CAP:
        bre.append(f"{bw} words > {BLOCK_WORDS_CAP}")

    # 5. block / abstract ratio
    if aw:
        ev["ratio"] = ratio
        if ratio > BLOCK_ABSTRACT_RATIO_CAP:
            bre.append(f"block/abstract {ratio:.4f} > {BLOCK_ABSTRACT_RATIO_CAP}")
    else:
        unm.append(f"block/abstract ratio (no abstract region, cap {BLOCK_ABSTRACT_RATIO_CAP})")

    # 6. duplication with the abstract
    if shared_n is None:
        unm.append(f"shared {SHARED_NGRAM_N}-grams (no abstract region, cap {SHARED_NGRAM_CAP})")
    else:
        ev["shared_ngrams"] = shared_n
        if shared_n > SHARED_NGRAM_CAP:
            bre.append(f"{shared_n} shared {SHARED_NGRAM_N}-grams > {SHARED_NGRAM_CAP}")
    return bre, unm, ev


def contract_tail(breaches: list[str], unmeasured: list[str]) -> str:
    """The single verdict string both contribution gates end with."""
    done = CONTRACT_CLAUSES - len(unmeasured)
    parts = list(breaches) + [f"{u} NOT EVALUATED" for u in unmeasured]
    body = "; ".join(parts) if parts else "ok"
    return f"contributions contract: {done}/{CONTRACT_CLAUSES} clauses evaluated -> {body}"


def gate(name: str, region: str, basis: str, status: str, detail: str) -> dict:
    return {"gate": name, "region": region, "basis": basis, "status": status, "detail": detail}


def run_gates(lines: list[str], twin: str, regions: dict, basis: str,
              item_mode: str = "any") -> list[dict]:
    heads = spans(headings(lines, twin), len(lines))
    top = [h for h in heads if h["level"] == 2]
    out: list[dict] = []

    def span(a: int, b: int) -> str:
        return "\n".join(lines[a - 1:b])

    # G1–G3 abstract -------------------------------------------------------
    ar = regions.get("abstract")
    if not ar:
        out.append(gate("abstract", "n/a", basis, "unmatched", "no abstract region given"))
        abstract_text = ""
    else:
        abstract_text = span(*ar)
        w = count_words(abstract_text, basis)
        out.append(gate("abstract-words", f"{twin}:{ar[0]}-{ar[1]}", basis,
                        "measured", f"{w} words vs cap {ABSTRACT_WORDS_CAP} -> "
                                    f"{'BREACH' if w > ABSTRACT_WORDS_CAP else 'ok'}"))
        paras = [p for p in re.split(r"\n\s*\n", abstract_text) if p.strip()]
        lens = [count_words(p, basis) for p in paras]
        sent = [s for s in SENTENCE.split(abstract_text) if s.strip()]
        longest = max((count_words(s, basis) for s in sent), default=0)
        out.append(gate("abstract-longest-sentence", f"{twin}:{ar[0]}-{ar[1]}", basis, "measured",
                        f"{longest} words vs cap {ABSTRACT_LONGEST_SENTENCE_CAP} -> "
                        f"{'BREACH' if longest > ABSTRACT_LONGEST_SENTENCE_CAP else 'ok'}"))
        # The four-move annotation and the build share are PER-PARAGRAPH measurements.  A
        # one-paragraph abstract has one paragraph and therefore one move, so its "build
        # share" can only be 0.0 or 1.0 and the criterion above it is not falsifiable on the
        # artefact.  The paragraph count is therefore a floor, not a number to report.
        nparas = len(paras)
        estruct = ("no paragraph structure: the region has no non-blank block, so the "
                   "paragraph count is not a measurement — report unmatched, never 0"
                   if not nparas else
                   f"{nparas} paragraph(s) vs floor {ABSTRACT_PARAGRAPH_FLOOR} -> "
                   + ("ok" if nparas >= ABSTRACT_PARAGRAPH_FLOOR else
                      f"BREACH — a single-paragraph abstract is below the corpus floor "
                      f"(crypto/statistics.md:123 has min 1, q1 2, median 2, n=59; "
                      f"crypto/statistics.md:128 records 0.78 of tier-A abstracts with more "
                      f"than one paragraph), and with one paragraph the four-move allocation "
                      f"and the build share are not measurable at all"))
        out.append(gate("abstract-paragraphs", f"{twin}:{ar[0]}-{ar[1]}", basis,
                        "measured" if nparas else "unmatched", estruct))
        share = None
        unbuildable = nparas < ABSTRACT_PARAGRAPH_FLOOR
        if unbuildable:
            # Criterion 4 is a per-paragraph annotation.  With fewer than 2 paragraphs the
            # share is not a four-move allocation, so the gate must refuse rather than
            # print a number that cannot mean what the criterion says it means.
            given = regions.get("build_share")
            share = f"withheld; {given} was supplied but is not a four-move allocation" \
                if given is not None else "not reported"
            out.append(gate("abstract-build-share", f"{twin}:{ar[0]}-{ar[1]}", basis, "unmatched",
                            f"unmatched — {max(nparas, 0)} paragraph(s) < floor "
                            f"{ABSTRACT_PARAGRAPH_FLOOR}, so there is no paragraph structure to "
                            f"label context/gap/build/result and no build share "
                            f"({share}). Split the abstract into at least two paragraphs "
                            f"(crypto/statistics.md:128: 0.78 of tier-A abstracts have more "
                            f"than one) and re-run; NO verdict is implied."))
        elif "build_share" in regions:               # hand-coded, supplied by the caller
            share = regions["build_share"]
            how = "hand-coded (supplied)"
            out.append(gate("abstract-build-share", f"{twin}:{ar[0]}-{ar[1]}", basis, "measured",
                            f"{share:.4f} ({how}) vs floor {ABSTRACT_BUILD_SHARE_FLOOR} -> "
                            f"{'BREACH' if share < ABSTRACT_BUILD_SHARE_FLOOR else 'ok'}"))
        else:
            moves = classify_moves(paras)
            build = sum(n for n, mv in zip(lens, moves) if mv == "build")
            share = (build / w) if w else 0.0
            how = (f"keyword classifier {moves} — DIAGNOSTIC ONLY: the corpus records 0.14 "
                   f"from a keyword pass against 0.56 hand-coded (statistics.md:177-179), so "
                   f"pass --build-share to supply the hand-coded value")
            out.append(gate("abstract-build-share", f"{twin}:{ar[0]}-{ar[1]}", basis, "measured",
                            f"{share:.4f} ({how}) vs floor {ABSTRACT_BUILD_SHARE_FLOOR} -> "
                            f"{'BREACH' if share < ABSTRACT_BUILD_SHARE_FLOOR else 'ok'}"))

    # G4–G5 contributions --------------------------------------------------
    cr = regions.get("contributions")
    if not cr:
        out.append(gate("contributions", "n/a", basis, "unmatched", "no contributions region given"))
        contrib_text = ""
    else:
        contrib_text = span(*cr)
        bw = count_words(contrib_text, basis)
        aw = count_words(abstract_text, basis) if abstract_text else 0
        ratio = (bw / aw) if aw else 0.0

        # The contract is evaluated ONCE here and printed by BOTH contribution gates, so
        # they cannot report two different verdicts about the same block (R-VENUE-05's
        # two-sided pass condition; see contributions_verdict).
        items, item_status = contribution_items(contrib_text, item_mode)
        shared_n = None
        if aw:
            shared = ngrams(abstract_text, SHARED_NGRAM_N) & ngrams(contrib_text, SHARED_NGRAM_N)
            shared_n = sum(shared.values())
        bre, unm, ev = contributions_verdict(bw, aw, ratio, items, item_status, basis, shared_n)

        # block-level gate: the whole contract, not only the word count and the ratio
        out.append(gate("contributions-block", f"{twin}:{cr[0]}-{cr[1]}", basis, "measured",
                        f"{bw} words (whole span), block/abstract {ratio:.4f}; "
                        + contract_tail(bre, unm)))

        # per-item gate: the PORTED matcher and its pinned tokenizer, with an
        # explicit match_status. This is the gate F8 killed silently.
        iregion = f"{twin}:{cr[0]}-{cr[1]} (items={item_mode})"
        if item_status != "matched":
            out.append(gate("contributions-items", iregion,
                            f"{BASIS_LABEL[basis]} ({BASIS_PATTERN[basis]}), same tokenizer as the rest of the run", "unmatched",
                            f"match_status: unmatched — item mode {item_mode!r} found no item in "
                            f"the contributions span, so the per-item caps cannot be evaluated "
                            f"and NO verdict is implied. Re-run with --items bold, "
                            f"--items paragraph or --items any. "
                            + contract_tail(bre, unm)))
        else:
            iwords = ev["per_item"]
            imax = ev["longest"]
            over_cap = ev["over_cap"]
            over_style = sum(1 for w in iwords if w > STYLE_PER_ITEM_CAP)
            out.append(gate("contributions-items", iregion,
                            f"{BASIS_LABEL[basis]} ({BASIS_PATTERN[basis]}), same tokenizer as the rest of the run",
                            "measured",
                            f"tokenizer = {BASIS_PATTERN[basis]} ({BASIS_LABEL[basis]}, the "
                            f"declared basis of this run); match_status = matched; "
                            f"items = {len(items)}; longest item = {imax}; "
                            f"per-item = {iwords}; "
                            f"items > BULLET_WORDS_CAP ({BULLET_WORDS_CAP}) = {over_cap}; "
                            f"words_total = {item_words(item_body(contrib_text), basis)} (span body, "
                            f"heading line dropped); "
                            f"items > {STYLE_PER_ITEM_CAP} (the style instrument's cap, quoted only "
                            f"as a cross-instrument comparison) = {over_style}; "
                            + contract_tail(bre, unm)))
        if aw:
            out.append(gate("abstract-contributions-duplication",
                            f"{twin}:{ar[0]}-{ar[1]} vs {cr[0]}-{cr[1]}", basis, "measured",
                            f"{shared_n} shared {SHARED_NGRAM_N}-grams "
                            f"(ratio {shared_n / max(1, sum(ngrams(abstract_text, SHARED_NGRAM_N).values())):.4f}) "
                            f"vs cap {SHARED_NGRAM_CAP} -> "
                            f"{'BREACH' if shared_n > SHARED_NGRAM_CAP else 'ok'}"))

    # G6 overview ----------------------------------------------------------
    ov, intro = regions.get("overview"), regions.get("introduction")
    if not ov:
        out.append(gate("overview", "n/a", basis, "unmatched", "no overview region given"))
    else:
        ow = count_words(span(*ov), basis)
        ol = ov[1] - ov[0] + 1
        if not intro:
            status, share_s = "unmatched", "no introduction region given"
        else:
            iw = count_words(span(*intro), basis)
            share = ow / iw if iw else 0.0
            share_s = (f"{share:.4f} of {twin}:{intro[0]}-{intro[1]} ({ow}/{iw}) "
                       f"vs floor {OVERVIEW_SHARE_FLOOR} -> "
                       f"{'BREACH' if share < OVERVIEW_SHARE_FLOOR else 'ok'}")
            status = "measured"
        bre = []
        if ow < OVERVIEW_WORDS_FLOOR:
            bre.append(f"{ow} words < floor {OVERVIEW_WORDS_FLOOR}")
        if ol < OVERVIEW_LINES_FLOOR:
            bre.append(f"{ol} lines < floor {OVERVIEW_LINES_FLOOR}")
        out.append(gate("overview", f"{twin}:{ov[0]}-{ov[1]}", basis, status,
                        f"{ow} words / {ol} lines, share {share_s}; "
                        + ("; ".join(bre) if bre else "floors ok")))

    # G7 construction/analysis ratio, WITH the degeneracy guard ------------
    # The sections are an INPUT, never a detection: the corpus records that 69% of
    # tier-A papers have no section whose title contains "Construction"
    # (statistics.md:112-113), so a title-keyed mapping misfires.  On this manuscript a
    # title-keyed match pairs "2.2 Security notions for evaluation protocols" with
    # itself, because that one title carries both vocabularies.
    nums = regions.get("sections", {})
    cnums, anums = nums.get("construction"), nums.get("analysis")
    if not cnums or not anums:
        suggestion = [h["title"][:40] for h in heads
                      if h["level"] == 2 and re.search(
                          regions.get("construction_pattern",
                                      r"construction|our scheme|description|parameters|protocol"),
                          h["title"], re.I)]
        out.append(gate("construction-analysis-ratio", "n/a", f"words, direct ({basis})",
                        "unmatched",
                        "the construction/analysis mapping is an INPUT and none was supplied; "
                        f"--construction/--analysis are required. A title-keyed guess would have "
                        f"selected {suggestion or 'nothing'} — and the corpus warns that a "
                        f"title-keyed rule misses the majority (statistics.md:113)."))
    else:
        def pick(n):
            r"""Resolve section number N.

            A markdown heading carries its own number ("## 3. The host protocol"), so the
            title is matched.  A LaTeX \section does not, so fall back to ordinal position
            among top-level sections, which agrees with the printed numbering when the file
            has no unnumbered leading section.
            """
            for h in heads:
                if h["level"] == 2 and re.match(r"^{}\.".format(n), h["title"].strip()):
                    return h
            tops = [h for h in heads if h["level"] == 2]
            return tops[n - 1] if 1 <= n <= len(tops) else None
        csecs = [s for s in (pick(n) for n in cnums) if s]
        asec = pick(anums[0])
        if not csecs or not asec or len(csecs) != len(cnums):
            missing = [n for n in cnums if not pick(n)] + ([] if asec else list(anums))
            out.append(gate("construction-analysis-ratio", "n/a", f"words, direct ({basis})",
                            "unmatched", f"named section(s) {missing} not found in the {twin} twin"))
        else:
            cw = cp = 0
            cdeg = []
            for s in csecs:
                w, prose = direct_words(lines, s, heads, basis)
                cw += w
                cp += prose
                if is_degenerate(w, prose, s, lines, basis):
                    cdeg.append(f"§{s['title'][:22]} direct={w}")
            aw2, ap = direct_words(lines, asec, heads, basis)
            adeg = (f"§{asec['title'][:22]} direct={aw2}"
                    if is_degenerate(aw2, ap, asec, lines, basis) else None)
            region = (f"construction {twin}:" +
                      ",".join(f"{s['line']}-{s['end']}" for s in csecs) +
                      f" vs analysis {twin}:{asec['line']}-{asec['end']}  "
                      f"(mapping supplied: construction={cnums}, analysis={anums})")
            if cdeg or adeg:
                who = ", ".join(cdeg + ([adeg] if adeg else []))
                out.append(gate("construction-analysis-ratio", region, f"words, direct ({basis})",
                                "degenerate",
                                f"guard fired for {who}; the ratio is NOT evaluated on the `direct` "
                                f"basis — no band verdict may be printed. Report hierarchical "
                                f"counts with the twin and unit named. (Raw ratio {cw}/{aw2} = "
                                f"{(cw / aw2) if aw2 else float('nan'):.2f} is meaningless.)"))
            else:
                ratio = cw / aw2 if aw2 else 0.0
                band = ("fail (below q1)" if ratio < RATIO_FAIL_BELOW
                        else "needs expansion" if ratio < RATIO_PASS_AT
                        else "pass (at or above median)")
                out.append(gate("construction-analysis-ratio", region, f"words, direct ({basis})",
                                "measured",
                                f"{cw}/{aw2} = {ratio:.4f} on the direct basis -> {band}"))

    # G8 ceiling, with its structural exemption from the direct guard ------
    parents = [h for h in heads if h["level"] == 2]
    rows = []
    for p in parents:
        kids = [h for h in heads if h["level"] == 3 and p["line"] < h["line"] <= p["end"]]
        if not kids:
            continue
        pw = count_words(span(p["line"], p["end"]), basis)
        if not pw:
            rows.append(f"§'{p['title'][:28]}' unmatched (parent empty)")
            continue
        big = max(kids, key=lambda k: count_words(span(k["line"], k["end"]), basis))
        bw2 = count_words(span(big["line"], big["end"]), basis)
        share = bw2 / pw
        band = ("within budget" if share <= CEILING_MAJORITY
                else "relocation pass required" if share <= CEILING_OUTLIER else "outlier")
        rows.append(f"§'{p['title'][:26]}' -> §'{big['title'][:22]}' {share:.4f} [{band}]")
    out.append(gate("largest-child-ceiling", f"{twin} top-level sections", "hierarchical words",
                    "measured" if rows else "unmatched",
                    "; ".join(rows) if rows else "no parent/child pair found"))

    # G9 the Related Work floor, the mirror of the ceiling -------------------
    # Every other gate in this file states a cap; a cap cannot see a section that was
    # never written.  t36 measured the sample's Related Work at 102 words against a
    # corpus median of 392 and found that it "passed every gate unreviewed" because no
    # floor existed (the M5 item of skills-work/eval/structural-comparison.md).  See the
    # constants above for the n=3 provenance, which is printed with every use.
    rel = regions.get("related")
    how = "region supplied by the caller"
    if not rel:
        hit = next((h for h in heads if h["level"] == 2 and RELATED_WORK_RE.search(h["title"])), None) \
            or next((h for h in heads if h["level"] == 3 and RELATED_WORK_RE.search(h["title"])), None)
        if hit:
            # body only: the sibling instrument that produced the corpus figures selects the
            # section by heading and measures its BODY — it takes the (heading, body) pair —
            # so the heading line is dropped to stay comparable.  Cited by name, not by line
            # (R-23).
            rel = (hit["line"] + 1, hit["end"])
            how = (f"located by heading match {RELATED_WORK_RE.pattern!r} on "
                   f"{twin}:{hit['line']} \"{hit['title'][:40]}\", heading line excluded so "
                   f"the count is comparable with the corpus figure")
    if not rel:
        out.append(gate("related-work-floor", "n/a", f"words ({basis}), heading excluded",
                        "unmatched",
                        "no related-work region was supplied and no heading matches "
                        f"{RELATED_WORK_RE.pattern!r}. This is reported, never passed: no "
                        "floor verdict is implied either way. The corpus exposes a "
                        "related-work section in only 3 of 20 comparators (the M5 table of "
                        "skills-work/eval/structural-comparison.md), so a paper that "
                        "folds the material into the introduction is not in breach — but the "
                        "floor then applies to the named introduction block and the caller "
                        "must name it with --related A-B."))
    else:
        rw = count_words(span(*rel), basis)
        band = ("ok — at or above the floor, within corpus practice"
                if rw >= RELATED_WORK_WORDS_FLOOR else
                f"BREACH — {RELATED_WORK_WORDS_FLOOR - rw} words below the floor")
        out.append(gate("related-work-floor", f"{twin}:{rel[0]}-{rel[1]}",
                        f"words ({basis}), heading excluded", "measured",
                        f"{rw} words vs floor {RELATED_WORK_WORDS_FLOOR} "
                        f"(n={RELATED_WORK_N}, the sample median) -> {band}; {how}. "
                        f"Provenance: the crypto corpus has no related-work size "
                        f"distribution, so the floor is quoted from the three t36 "
                        f"comparators that expose such a section at all "
                        f"(228 / 392 / 1067 words, i.e. min / median / max of the same "
                        f"n={RELATED_WORK_N}; raw values in skills-work/eval/metrics.json "
                        f"-> percentiles[\"M5.related_work_words\"]) — a small sample, "
                        f"stated rather than smoothed over (R-3)."))
    return out


BUILD_CUES = ("we construct", "we build", "we present", "we introduce", "we give", "we define",
              "we propose", "our scheme", "our construction", "we design", "we describe")
GAP_CUES = ("however", "remains open", "no prior", "gap", "unresolved", "limitation of",
            "does not", "fails to", "we are not aware")
RESULT_CUES = ("theorem", "lemma", "bound", "prove", "proven", "corollary", "we show",
               "conditional", "we obtain", "margin", "achieved")
CONTEXT_CUES = ("is the core", "has attracted", "in recent years", "are used", "widely used",
                "state of the art", "previous works", "prior work")


def classify_moves(paras: list[str]) -> list[str]:
    """Label each abstract paragraph context / gap / build / result.

    A keyword classifier, reported as a DIAGNOSTIC.  The corpus records that a keyword
    pass and a hand-coded pass disagree materially (0.14 vs 0.56, statistics.md:177-179),
    so the caller should supply the hand-coded share with --build-share for a verdict.
    """
    out = []
    for p in paras:
        low = p.lower()
        score = {
            "build": sum(w in low for w in BUILD_CUES),
            "gap": sum(w in low for w in GAP_CUES),
            "result": sum(w in low for w in RESULT_CUES),
            "context": sum(w in low for w in CONTEXT_CUES),
        }
        out.append(max(score, key=lambda k: score[k]) if any(score.values()) else "context")
    return out


# ---------------------------------------------------------------------------
# The self-scan — the skill must not teach the patterns it forbids.
# Accounted-for = substring artefact, one of the five literal-bearing blocks, or a
# named category (a venue name).  Anything else is a finding.
# ---------------------------------------------------------------------------
SCAN_PATTERN = r"[A-Z]-?[0-9]|[A-Z]+/[A-Z]+|[A-Z][0-9]+|ref[0-9]{2}|frag[0-9]"
PERMITTED_BLOCKS = (
    "## Process-register anti-patterns",
    "### Stage 2 — the definition test",
    "### Class 6 has two owners",
    "### Worked adjudication",
    "### Reproducible form",
)
VENUE_NAMES = {"CRYPTO/LNCS", "CRYPTO/EUROCRYPT"}


def accounted(line: str, i: int, end: int, block: str | None, token: str) -> bool:
    if block or token in VENUE_NAMES:
        return True
    if i > 0 and line[i - 1].isalnum():
        return True
    if i > 1 and line[i - 1] in "-_" and line[i - 2].isalnum():
        return True
    return end < len(line) and line[end].isdigit()


def self_scan(root: pathlib.Path) -> list[str]:
    findings = []
    for f in sorted(root.rglob("*.md")):
        block = None
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## ") or line.startswith("### "):
                block = line if any(line.startswith(b) for b in PERMITTED_BLOCKS) else None
            for m in re.finditer(SCAN_PATTERN, line):
                if accounted(line, m.start(), m.end(), block, m.group(0)):
                    continue
                findings.append(f"{f.relative_to(root)}:{n} [{m.group(0)}] {line.strip()[:70]}")
    return findings


# ---------------------------------------------------------------------------
# --dename : the de-naming scan's stage 1 + the mechanical part of stage 2.
# The owning document is references/de-ai-and-style.md; this mode implements its
# definition test so the documented command is a one-liner that cannot misfire.
# ---------------------------------------------------------------------------
DENAME_CLASSES = {1: r"[A-Z]-?[0-9]", 3: r"[A-Z]+/[A-Z]+", 6: r"[A-Z][0-9]+"}
DENAME_NAMED = {
    "A/B":         ("a", "variants A and B are defined in the section introducing the variants"),
    "ROM/XOF":     ("b", "domain-standard primitives: random-oracle model, extendable output function"),
    "P/Q":         ("b", "the cited host's public P/Q equation; inherited standard notation"),
    "CRYPTO/LNCS": ("venue", "venue name, not a construct label"),
}


def in_math(line: str, idx: int) -> bool:
    """True when idx sits inside a $...$ span — delimiter PARITY, not "between two $".

    On a math-dense line the latter wrongly reports prose that merely sits between the
    closing $ of one span and the opening $ of the next.
    """
    return line.count("$", 0, idx) % 2 == 1


def dename_row_label(line: str) -> str | None:
    s = line.strip()
    if s.startswith("|") and s.count("|") >= 3:
        return s.strip("|").split("|")[0].strip()
    if "&" in s and not s.startswith("%"):
        return s.split("&")[0].strip()
    return None


def dename_label_anchors(lines: list[str]) -> dict:
    out = {}
    for i, l in enumerate(lines, 1):
        c = dename_row_label(l)
        if not c:
            continue
        for m in re.finditer(r"[A-Z][0-9]+", c):
            out.setdefault(m.group(0), i)
    return out


def dename_scan(path: pathlib.Path) -> list[tuple]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    labels = dename_label_anchors(lines)
    rows = []
    for cls, pat in DENAME_CLASSES.items():
        for i, line in enumerate(lines, 1):
            for m in re.finditer(pat, line):
                tok = m.group(0)
                before = line[m.start() - 1] if m.start() else ""
                after = line[m.end()] if m.end() < len(line) else ""
                midword = (before.isalnum() and before.isupper()) or after.isdigit()
                if re.search(r"\\usepackage\s*\[[^\]]*" + re.escape(tok) + r"[^\]]*\]", line):
                    v, why = "legitimate(c)", "LaTeX package option"
                elif in_math(line, m.start()):
                    v, why = "legitimate(c)", "math environment"
                elif midword:
                    v, why = "not-a-token", "substring of a longer alphanumeric word"
                elif tok in labels:
                    v, why = "legitimate(a)", f"table label column at {path}:{labels[tok]}"
                elif tok in DENAME_NAMED:
                    cat, reason = DENAME_NAMED[tok]
                    v = f"legitimate({cat})" if cat in ("a", "b", "c") else "legitimate(venue)"
                    why = reason
                else:
                    v, why = "violation", "no definition found"
                style = ("  [class6-style: label cited outside its own table]"
                         if v.startswith("legitimate(a)") and labels.get(tok) != i else "")
                rows.append((f"{path}:{i}", cls, tok, v, why, style))
    return rows


def run_dename(paths: list[pathlib.Path]) -> int:
    tally, viol, bad = {}, [], []
    for p in paths:
        if not p.is_file():
            print(f"unmatched: {p} not found", file=sys.stderr)
            bad.append(str(p))
            continue
        for r in dename_scan(p):
            tally[r[3]] = tally.get(r[3], 0) + 1
            if r[3] == "violation":
                viol.append(r)
            print(f"{r[0]}\tclass{r[1]}\t[{r[2]}]\t{r[3]}\t{r[4]}{r[5]}")
    print("\nVERDICT TALLY (diagnostic only, never the verdict):", dict(sorted(tally.items())))
    print(f"unresolvable identifiers: {len(viol)}")
    if bad:
        return 2
    verdict_pass = not viol
    print("pass condition: no unadjudicated hits and zero unresolvable identifiers -> "
          f"{'PASS' if verdict_pass else 'FAIL'} ({len(viol)} unresolvable)")
    # VENUE-R3-01: this is the one mode that renders a verdict, so its failure must be
    # visible to an exit-code-keyed pipeline.  Exit 1 = verdict failure, distinct from
    # exit 2 = measurement failure (a gate that could not be measured).
    return 0 if verdict_pass else 1

# ---------------------------------------------------------------------------
# --self-test
# ---------------------------------------------------------------------------
def self_test() -> int:
    fails, total = [], []

    def check(name, cond):
        total.append(name)
        print(f"  self-test {name:44} {'ok' if cond else 'FAILED'}")
        if not cond:
            fails.append(name)

    check("ws and alnum bases differ", count_words("a b;c", "ws") == 2 and count_words("a b;c", "alnum") == 3)

    # a heading-only section must be degenerate; a prose section must not
    synthetic = ["## 9. Empty", "", "### 9.1 Child", "prose " * 40, "", "## 10. Prose",
                 "real running prose here " * 40, "", "### 10.1 Child", "more prose " * 40]
    sp = spans(headings(synthetic, "md"), len(synthetic))
    empty = next(s for s in sp if s["title"].startswith("9."))
    prose = next(s for s in sp if s["title"].startswith("10."))
    ew, ep = direct_words(synthetic, empty, sp, "ws")
    pw, pp = direct_words(synthetic, prose, sp, "ws")
    check("degenerate detector fires on heading-only", is_degenerate(ew, ep, empty, synthetic, "ws"))
    check("degenerate detector clears prose section", not is_degenerate(pw, pp, prose, synthetic, "ws"))

    # the ratio gate must refuse a band when either side is degenerate
    g = run_gates(synthetic, "md", {"sections": {"construction": [9], "analysis": [10]}}, "ws")
    ratio = next(x for x in g if x["gate"] == "construction-analysis-ratio")
    check("ratio returns degenerate, not a band", ratio["status"] == "degenerate")
    check("degenerate detail forbids a band verdict", "no band verdict" in ratio["detail"])

    # an unmatched section must be reported, never passed
    g2 = run_gates(synthetic, "md", {"sections": {"construction": [99], "analysis": [10]}}, "ws")
    ratio2 = next(x for x in g2 if x["gate"] == "construction-analysis-ratio")
    check("absent section yields unmatched", ratio2["status"] == "unmatched")

    # n-gram overlap and bullet parsing
    a = "the alpha beta gamma delta epsilon zeta"
    b = "the alpha beta gamma delta epsilon zeta omega"
    # a has 7 tokens -> two 6-grams; b has 8 -> three; the first two are shared
    check("6-gram overlap counted", sum((ngrams(a, 6) & ngrams(b, 6)).values()) == 2 and
          sum(ngrams(a, 6).values()) == 2)
    check("bullets parsed", len(bullets("- one\n- two\n1) three")) == 3)

    # the scan's substring rule
    check("substring artefact accounted", accounted("D-C1 and D12", 2, 4, None, "C1")
          or accounted("D12", 0, 2, None, "D1"))

    # -- R-24.2 accrued failure-mode self-check ----------------------------
    # F8 — an item-shape mismatch must go unmatched, never a clean zero.  The
    # manuscript's own form is a BOLD RUN-IN item, which the bullet-only matcher
    # this instrument used to ship could not see.
    bold_span = "**(1) A scheme definition.** We specify the scheme.\n\n**(2) A theorem.** We prove it."
    bl, bs = contribution_items(bold_span, "bold")
    check("F8 bold run-in items are matched", len(bl) == 2 and bs == "matched")
    bullet_only = contribution_items(bold_span, "bullet")
    check("F8 bullet mode sees no bold item", bullet_only == ([], "unmatched"))
    none_mode = contribution_items(bold_span, "none")
    check("F8 --items none is unmatched, not zero", none_mode == ([], "unmatched"))

    g_f8 = run_gates(synthetic, "md", {"sections": {"construction": [9], "analysis": [10]},
                                       "contributions": (1, 4)}, "ws", item_mode="none")
    f8 = next(x for x in g_f8 if x["gate"] == "contributions-items")
    check("F8 unmatched item gate is not measured", f8["status"] == "unmatched")
    check("F8 unmatched detail says no verdict implied", "NO verdict is implied" in f8["detail"])

    # F9 — structureless input must fail loudly, never no-op silently.
    g_f9 = run_gates(["nothing here"], "md", {}, "ws")
    check("F9 structureless input yields unmatched gates",
          any(x["status"] == "unmatched" for x in g_f9))
    check("F9 structureless input claims no band",
          all(x["status"] != "measured" for x in g_f9
              if x["gate"] in ("construction-analysis-ratio", "largest-child-ceiling",
                               "contributions-items")))

    # (b) the per-item cap must exist as a named constant AND be evaluated per item.
    check("BULLET_WORDS_CAP constant exists", BULLET_WORDS_CAP == 29.5)

    # (c) t30's *inferred* case, turned into a regression fixture — in the DECLARED
    # regions.  A region slice that starts at the subsection heading pulls that heading
    # into the block, changing both the block word count and the block/abstract ratio;
    # t30's own synthetic samples died on that boundary before reaching the per-item
    # gate.  These fixtures therefore use the shipped default region map
    # (abstract 11-17, contributions 29-44) and place their bodies in the middle of it,
    # so the same slicing the calibration manuscript gets is exercised here.
    def declared_fixture(n_items: int, extra_words: int) -> list[str]:
        L = [f"preamble filler {i}" for i in range(1, 10)]          # 1-9
        L.append("## Abstract")                                     # 10
        L += [" ".join(["abstractword"] * 34) for _ in range(7)]     # 11-17
        L += ["" for _ in range(11)]                                # 18-28
        L.append("### 1.1 Our contributions")                       # 29  (slice boundary)
        for i in range(1, n_items + 1):                             # 30..
            L.append(f"**(%d) Label %d.** " % (i, i) + " ".join(["word"] * extra_words))
            L.append("")
        while len(L) < 44:
            L.append("")            # blank padding: contributes no words, so it cannot
                                    # introduce a block-level violation of its own
        return L

    # Fixture A isolates the per-item gate: 4 items of 32 words each, so EVERY item is
    # over the per-item cap while the block (132 words) stays inside its 146 cap and the
    # ratio (0.55) inside its 0.81 cap.  No block-level WORD or RATIO violation can mask it.
    #
    # t37 CHANGE, stated because this assertion's expectation had to move: it used to read
    # `blk_a["detail"].endswith("ok")`, i.e. it asserted that the BLOCK gate stayed clean
    # while the item gate fired.  With the contract unified (R-VENUE-05's two-sided pass
    # condition, see contributions_verdict) the block gate now reports the item clause too,
    # so that expectation encoded the very defect being repaired.  The block gate still must
    # not be ok here; what changed is that it is no longer silent about the item clause.
    fa = declared_fixture(4, 29)
    ga = run_gates(fa, "md", DEFAULT_REGIONS["md"], "ws", item_mode="any")
    blk_a = next(x for x in ga if x["gate"] == "contributions-block")
    itm_a = next(x for x in ga if x["gate"] == "contributions-items")
    check("(c-A) no block-level word or ratio cap fires, so nothing can mask the per-item cap",
          blk_a["detail"].rstrip().endswith("per-item words: [32, 32, 32, 32]")
          and "words > 146" not in blk_a["detail"] and "block/abstract" in blk_a["detail"]
          and "> 0.81" not in blk_a["detail"])
    check("(c-A) negative: neither gate prints ok on this shape",
          not blk_a["detail"].rstrip().endswith("ok") and not itm_a["detail"].rstrip().endswith("ok"))
    check("(c-A) positive: the gate measured, and reports 4 items",
          "items = 4" in itm_a["detail"] and "match_status = matched" in itm_a["detail"])
    check("(c-A) positive: a real longest item is reported",
          "longest item = 32" in itm_a["detail"])
    check("(c-A) positive: every offending item is named",
          "4 item(s) over 29.5 (venue per-item cap)" in itm_a["detail"])
    check("(c-A) negative: the form does not print ok",
          not itm_a["detail"].rstrip().endswith("ok"))

    # Fixture C is R-24a.3's shape: FIVE items of 30 words each.  Every item is over the
    # 29.5 per-item cap, so the block must not print ok and the per-item breach must be
    # reported.  NOTE the arithmetic: 5 x 30 = 150, so this block ALSO breaches the
    # 146-word block cap (154 with the heading).  A 5-item shape therefore cannot have all
    # items over the cap AND total <= 146 — the maximum per-item length keeping 5 items
    # inside 146 is 29.2, below the cap — so Fixture A (4 items) remains the one that
    # isolates the per-item gate.  This fixture's job is R-24a.3's: prove the shape does
    # not print ok and that the per-item violation is named among the breaches.
    fc = declared_fixture(5, 27)
    gc = run_gates(fc, "md", DEFAULT_REGIONS["md"], "ws", item_mode="any")
    itm_c = next(x for x in gc if x["gate"] == "contributions-items")
    check("(R-24a.3) positive: five 30-word items are measured, not zero",
          "items = 5" in itm_c["detail"] and "longest item = 30" in itm_c["detail"])
    check("(R-24a.3) negative: the block does not print ok",
          not itm_c["detail"].rstrip().endswith("ok"))
    check("(R-24a.3) the per-item breach is named, not merely counted",
          "5 item(s) over 29.5 (venue per-item cap)" in itm_c["detail"])
    check("(R-24a.3) documented: this shape also breaches the block cap, so it does not isolate",
          "words > 146" in next(x for x in gc if x["gate"] == "contributions-block")["detail"])

    # Fixture B is t30's SIX-item shape.  Its POSITIVE assertion is the point: a future
    # edit could satisfy the negative assertion by making everything `unmatched`, which
    # would kill the gate again (F9).  Note the arithmetic ceiling: with 6 items and the
    # block cap at 146, an item can hold at most 24 words, so this shape CANNOT fire the
    # per-item cap — fixture A is the one that isolates it.
    fb = declared_fixture(6, 20)
    gb = run_gates(fb, "md", DEFAULT_REGIONS["md"], "ws", item_mode="any")
    itm_b = next(x for x in gb if x["gate"] == "contributions-items")
    check("(c-B) positive: the six-item inline form is measured, not zero",
          "items = 6" in itm_b["detail"] and "match_status = matched" in itm_b["detail"])
    check("(c-B) positive: a real longest is reported, never the empty-list max",
          "longest item = 23" in itm_b["detail"] and "longest item = 0" not in itm_b["detail"])
    check("(c-B) positive: per-item words are printed",
          "per-item = [23, 23, 23, 23, 23, 23]" in itm_b["detail"])
    check("(c-B) documented ceiling: 6 items CANNOT fire the per-item length cap",
          "BULLET_WORDS_CAP (29.5) = 0" in itm_b["detail"])
    check("(c-B) what does fire on this shape is the item-count cap, not the length cap",
          "items 6 outside (2, 5)" in itm_b["detail"])

    # unmatched must be BOTH a status and a non-zero exit — `unmatched` with exit 0 is F9.
    g_none = run_gates(fa, "md", DEFAULT_REGIONS["md"], "ws", item_mode="none")
    itm_none = next(x for x in g_none if x["gate"] == "contributions-items")
    check("unmatched input: gate status is unmatched", itm_none["status"] == "unmatched")
    check("unmatched input: it is a non-zero-exit condition",
          any(x["status"] in ("degenerate", "unmatched") for x in g_none))
    check("unmatched input: no item number is printed as if measured",
          "items = 0" not in itm_none["detail"])

    # basis declaration — the number must carry the tokenizer it was counted with.
    g_b = run_gates(fa, "md", DEFAULT_REGIONS["md"], "ws", item_mode="bold")
    itm_b = next(x for x in g_b if x["gate"] == "contributions-items")
    check("basis: item gate prints its tokenizer", "tokenizer = " in itm_b["detail"])
    check("basis: item gate names the declared basis",
          BASIS_LABEL["ws"] in itm_b["basis"] and BASIS_PATTERN["ws"] in itm_b["basis"])
    check("basis: per-item counting uses the run's own tokenizer",
          item_words("a b;c", "ws") == count_words("a b;c", "ws")
          and item_words("a b;c", "alnum") == count_words("a b;c", "alnum"))
    check("basis: the two declared bases disagree on the same text",
          count_words("a b;c", "ws") != count_words("a b;c", "alnum"))

    # ----------------------------------------------------------------------
    # t37 — the three rule-level gaps t36 exposed.  Each gap is the same shape: the rule
    # exists in the reference file but nothing could mechanically DECIDE it, so a violating
    # manuscript reported clean.  Each fixture below therefore carries a POSITIVE assertion
    # (the gate measured a real number) beside its negative one — a negative assertion alone
    # can be satisfied by making everything `unmatched`, which is F9 again.
    # ----------------------------------------------------------------------

    # t37-(1) the contribution contract is TWO-SIDED, and its verdict is printed by both
    # gates.  This fixture is t36's one-item shape: 1 item, 139 words measured on the
    # declared basis.  The item count breaks the LOWER bound, the single item breaks the
    # per-item cap and the longest-item cap — while the block's own word count (143) and its
    # ratio to the abstract stay inside their caps.  Before the fix, `contributions-block`
    # printed `ok` on exactly this shape.
    fd = declared_fixture(1, 136)
    gd = run_gates(fd, "md", DEFAULT_REGIONS["md"], "ws", item_mode="any")
    blk_d = next(x for x in gd if x["gate"] == "contributions-block")
    itm_d = next(x for x in gd if x["gate"] == "contributions-items")
    check("(t37-1) positive: the one-item shape is measured, not zero",
          "items = 1" in itm_d["detail"] and "longest item = 139" in itm_d["detail"])
    check("(t37-1) the item-count LOWER bound is enforced, not only the ceiling",
          "items 1 outside (2, 5)" in itm_d["detail"])
    check("(t37-1) the single 139-word item is over the per-item cap",
          "1 item(s) over 29.5 (venue per-item cap)" in itm_d["detail"])
    check("(t37-1) the block gate no longer prints ok on this shape",
          not blk_d["detail"].rstrip().endswith("ok"))
    check("(t37-1) both contributions gates print the SAME contract verdict",
          blk_d["detail"].split("contributions contract:")[-1]
          == itm_d["detail"].split("contributions contract:")[-1])
    check("(t37-1) the contract is reported whole, six clauses, none dropped",
          "6/6 clauses evaluated" in blk_d["detail"])

    # control: a compliant block must still print ok in BOTH gates.  Without this, the
    # negative assertions above could be satisfied by making the contract unprintable.
    fe = declared_fixture(5, 17)
    ge = run_gates(fe, "md", DEFAULT_REGIONS["md"], "ws", item_mode="any")
    blk_e = next(x for x in ge if x["gate"] == "contributions-block")
    itm_e = next(x for x in ge if x["gate"] == "contributions-items")
    check("(t37-1) control: five 20-word items pass the whole contract in both gates",
          blk_e["detail"].rstrip().endswith("-> ok") and itm_e["detail"].rstrip().endswith("-> ok"))

    # t37-(3) the abstract's paragraph floor.  Criterion 4 asks for a per-paragraph move
    # annotation and a build share; with one paragraph there is one move, so the share can
    # only be 0.0 or 1.0 and the criterion is not falsifiable on the artefact.
    def abstract_fixture(n_paras: int, per_para: int) -> list[str]:
        L = [f"preamble filler {i}" for i in range(1, 10)]           # 1-9
        L.append("## Abstract")                                      # 10
        for i in range(n_paras):                                     # 11..
            L.append(" ".join(["abstractword"] * per_para))
            if i < n_paras - 1:
                L.append("")                                         # blank separator
        while len(L) < 17:
            L.append("")
        return L

    ar_only = {"abstract": (11, 17)}
    g1 = run_gates(abstract_fixture(1, 34), "md", ar_only, "ws")
    p1 = next(x for x in g1 if x["gate"] == "abstract-paragraphs")
    b1 = next(x for x in g1 if x["gate"] == "abstract-build-share")
    g2 = run_gates(abstract_fixture(2, 34), "md", ar_only, "ws")
    p2 = next(x for x in g2 if x["gate"] == "abstract-paragraphs")
    b2 = next(x for x in g2 if x["gate"] == "abstract-build-share")
    g3 = run_gates(abstract_fixture(1, 34), "md", {**ar_only, "build_share": 0.4}, "ws")
    b3 = next(x for x in g3 if x["gate"] == "abstract-build-share")
    g4 = run_gates(abstract_fixture(0, 0), "md", ar_only, "ws")
    p4 = next(x for x in g4 if x["gate"] == "abstract-paragraphs")

    check("(t37-3) positive: the paragraph count is measured, not skipped",
          p1["status"] == "measured" and "1 paragraph(s)" in p1["detail"])
    check("(t37-3) a single-paragraph abstract BREACHES the paragraph floor",
          "1 paragraph(s) vs floor 2 -> BREACH" in p1["detail"])
    check("(t37-3) the breach names its corpus basis and sample size",
          "crypto/statistics.md:123" in p1["detail"] and "0.78" in p1["detail"])
    check("(t37-3) with one paragraph the build share is UNMATCHED, not a number",
          b1["status"] == "unmatched" and "NO verdict is implied" in b1["detail"])
    check("(t37-3) no share figure is printed as if it had been measured",
          "not reported" in b1["detail"])
    check("(t37-3) a supplied --build-share cannot rescue a one-paragraph abstract",
          b3["status"] == "unmatched" and "withheld" in b3["detail"])
    check("(t37-3) two paragraphs clear the floor and the share is measured again",
          "2 paragraph(s) vs floor 2 -> ok" in p2["detail"] and b2["status"] == "measured")
    check("(t37-3) an empty abstract region is unmatched, never '0 paragraphs -> breach'",
          p4["status"] == "unmatched" and "no paragraph structure" in p4["detail"])

    # t37-(2) the Related Work floor: the mirror of the ceiling.  A cap cannot see a section
    # that was never written, so a 102-word Related Work passed every gate unreviewed
    # (skills-work/eval/structural-comparison.md:179).
    def related_fixture(n: int) -> list[str]:
        L = ["## 1. Introduction", "intro prose " * 10, ""]
        L.append("## 3. Related work")
        L.append(" ".join(["relatedword"] * n))
        L.append("")
        L.append("## 4. Construction")
        L.append("construction prose " * 10)
        return L

    gr = run_gates(related_fixture(102), "md", {}, "ws")
    r_short = next(x for x in gr if x["gate"] == "related-work-floor")
    gedge = run_gates(related_fixture(391), "md", {}, "ws")
    r_edge = next(x for x in gedge if x["gate"] == "related-work-floor")
    gl = run_gates(related_fixture(392), "md", {}, "ws")
    r_long = next(x for x in gl if x["gate"] == "related-work-floor")
    gt = run_gates(related_fixture(420), "md", {}, "ws")
    r_target = next(x for x in gt if x["gate"] == "related-work-floor")
    gnone = run_gates(["## 1. Introduction", "prose " * 30], "md", {}, "ws")
    r_none = next(x for x in gnone if x["gate"] == "related-work-floor")
    gsup = run_gates(related_fixture(102), "md", {"related": (4, 5)}, "ws")
    r_sup = next(x for x in gsup if x["gate"] == "related-work-floor")

    check("(t37-2) positive: a located related-work section is measured",
          r_short["status"] == "measured" and "102 words vs floor 392" in r_short["detail"])
    check("(t37-2) a short related-work section is a BREACH, not silence",
          "BREACH" in r_short["detail"])
    check("(t37-2) the floor is printed with its sample size and provenance",
          "n=3" in r_short["detail"] and "metrics.json" in r_short["detail"]
          and "sample median" in r_short["detail"])
    check("(t37-2) one word below the floor is a breach: the floor is the boundary",
          "391 words vs floor 392" in r_edge["detail"] and "BREACH" in r_edge["detail"])
    check("(t37-2) exactly at the floor is ok",
          "392 words vs floor 392" in r_long["detail"]
          and "-> ok — at or above the floor" in r_long["detail"])
    check("(t37-2) the heading line is excluded, so the count matches the corpus figure",
          r_short["region"] == "md:5-6" and "heading excluded" in r_short["basis"])
    check("(t37-2) above the floor is ok",
          "420 words vs floor 392" in r_target["detail"] and "-> ok" in r_target["detail"])
    check("(t37-2) no heading and no region is unmatched, and implies no floor verdict",
          r_none["status"] == "unmatched" and "no floor verdict is implied" in r_none["detail"])
    check("(t37-2) a supplied --related span overrides the heading lookup",
          r_sup["region"] == "md:4-5" and "region supplied by the caller" in r_sup["detail"])
    check("(t37-2) an unmatched floor gate is a non-zero-exit condition",
          any(x["status"] in ("degenerate", "unmatched") for x in gnone))

    print(f"self-test: {len(total) - len(fails)}/{len(total)} as expected")
    return 1 if fails else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manuscript", type=pathlib.Path,
                    default=pathlib.Path("research-work/paper/final-paper.md"))
    ap.add_argument("--twin", choices=("md", "tex"), default="md")
    ap.add_argument("--basis", choices=("ws", "alnum"), default="ws")
    ap.add_argument("--construction", default=None,
                    help="comma-separated top-level section numbers that form the ratio's "
                         "NUMERATOR; the mapping is an input, never a title-based detection")
    ap.add_argument("--analysis", default=None,
                    help="top-level section number that forms the ratio's DENOMINATOR")
    ap.add_argument("--related", default=None, metavar="A-B",
                    help="the related-work region as a line span, when the paper has no "
                         "heading matching 'related work|prior work|related literature' — "
                         "for example when the material is folded into the introduction. "
                         "Without it the gate looks the region up by heading, and reports "
                         "`unmatched` when it finds neither; it never passes silently.")
    ap.add_argument("--build-share", type=float, default=None,
                    help="hand-coded four-move build share; without it the classifier's "
                         "value is reported as a diagnostic only")
    ap.add_argument("--items", choices=ITEM_MODES, default="any",
                    help="how the contribution list is written: bullet lines, bold run-in "
                         "labels, paragraphs, any of those (default), or none. A mode that "
                         "matches no item yields match_status unmatched and a non-zero exit "
                         "— a per-item gate that matches nothing cannot fail (F8).")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--self-scan", action="store_true")
    ap.add_argument("--dename", nargs="*", default=None, metavar="FILE",
                    help="adjudicate every class-1/3/6 candidate in the given manuscript "
                         "twin(s); with no files, the calibration twins are used")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if args.dename is not None:
        paths = [pathlib.Path(x) for x in args.dename]
        if not paths:
            paths = [pathlib.Path("research-work/paper/final-paper.md"),
                     pathlib.Path("research-work/paper/latex/main.tex")]
        return run_dename(paths)

    if args.self_scan:
        root = pathlib.Path(__file__).resolve().parents[1]
        found = self_scan(root)
        print(f"unaccounted hits in this skill: {len(found)}")
        for f in found:
            print("  ", f)
        return 2 if found else 0

    if not args.manuscript.is_file():
        print(f"unmatched: manuscript not found at {args.manuscript}", file=sys.stderr)
        return 2

    lines = args.manuscript.read_text(encoding="utf-8", errors="replace").splitlines()
    regions = DEFAULT_REGIONS.get(args.twin, {})
    if args.construction and args.analysis:
        regions = {**regions, "sections": {
            "construction": [int(x) for x in args.construction.split(",") if x.strip()],
            "analysis": [int(args.analysis)]}}
    if args.build_share is not None:
        regions = {**regions, "build_share": args.build_share}
    if args.related:
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", args.related.strip())
        if not m:
            print(f"unmatched: --related expects A-B (a line span), got {args.related!r}",
                  file=sys.stderr)
            return 2
        regions = {**regions, "related": (int(m.group(1)), int(m.group(2)))}

    gates = run_gates(lines, args.twin, regions, args.basis, args.items)
    bad = [g for g in gates if g["status"] in ("degenerate", "unmatched")]

    if args.json:
        print(json.dumps({"manuscript": str(args.manuscript), "twin": args.twin,
                          "basis": args.basis, "gates": gates}, indent=2))
    else:
        print(f"# {args.manuscript}  twin={args.twin}  basis={args.basis}")
        for g in gates:
            print(f"\n[{g['status']:10}] {g['gate']}")
            print(f"   region : {g['region']}")
            print(f"   basis  : {g['basis']}")
            print(f"   detail : {g['detail']}")
        print(f"\n{len(gates)} gates: "
              f"{sum(1 for g in gates if g['status'] == 'measured')} measured, "
              f"{sum(1 for g in gates if g['status'] == 'degenerate')} degenerate, "
              f"{sum(1 for g in gates if g['status'] == 'unmatched')} unmatched")
        if bad:
            print("NON-ZERO EXIT: a gate could not be measured "
                  "(degenerate/unmatched). A band verdict must not be printed for it.")
    return 2 if bad else 0


# Region map for the frozen calibration manuscript, markdown twin.  These are INPUTS,
# not detections: the skill requires the region to be named, and an agent writing a new
# paper supplies its own.  The introduction region is the budgeted subsection block
# (29-75), which is the region the overview-share rule uses (expansion-rules.md).
DEFAULT_REGIONS = {
    "md": {"abstract": (11, 17), "contributions": (29, 44), "introduction": (29, 75),
           "overview": (60, 67),
           # calibration input: the manuscript's construction is §3+§4 and its analysis is §5
           "sections": {"construction": [3, 4], "analysis": [5]}},
    "tex": {},
}


if __name__ == "__main__":
    sys.exit(main())
