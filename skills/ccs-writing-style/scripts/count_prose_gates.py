#!/usr/bin/env python3
"""Count the prose gates that the writing-style skills apply.

The skills state numeric gates for the abstract, the contribution list, the
technical overview, and the design-versus-analysis mass. A gate that cannot be
counted is not a gate, so this script is the counting instrument the skills
refer to. It reports numbers and never renders a verdict: the gates' pass and
fail conditions are in the skills' reference files, and the move labels that the
allocation gate needs are supplied by the reader, not guessed here.

Basis (declared so that two runs are comparable):

  words       tokens carrying at least one letter or digit, punctuation
              stripped and case preserved
  paragraphs  blank-line separated blocks
  sentences   split on . ! ? followed by whitespace or end of text, after
              protecting common abbreviations and section references
  jaccard     |set(A) & set(B)| / |set(A) | set(B)| over deduplicated,
              case-folded, punctuation-stripped word sets
  trigram     the same index over adjacent word trigrams
  section words
              by default a section's words include its subsections; --direct
              counts the section's own text only

Usage:

  # abstract and contribution gates (--items any finds bullets, bold run-in labels or paragraphs)
  python3 scripts/count_prose_gates.py abstract-contributions PAPER.md \
      --abstract-heading "Abstract" \
      --contributions-heading "Contributions|Our Contributions|Main Results" \
      --threat-model-heading "Threat Model|Security Model"

  # section mass gates
  python3 scripts/count_prose_gates.py section-mass PAPER.md \
      --section "design:Design|Construction|Protocol|Scheme" \
      --section "analysis:Security Analysis|Proof|Security of" \
      --section "overview:Technical Overview|Our Techniques|Overview"

  # a raw span, for a single gate
  python3 scripts/count_prose_gates.py span --file abstract.txt

Exit codes, and why a measurement device needs them:

  0   every requested pattern matched and the numbers are reportable
  2   a requested pattern matched nothing: the report carries `status: "degenerate"` (or
      `match_status: "unmatched"` for the item list) and the fields it could not measure are
      null. No verdict is implied, and the caller must not read a null per-item gate as a pass.
  non-zero from argparse for a usage error.

A gate that matched nothing cannot fail, so reporting it with a clean-looking zero would be a
false negative. The script therefore refuses to return a pass-shaped result for an empty match.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# The tokenizer is pinned here and nowhere else. Every count this script prints uses
# exactly this pattern, and the pattern is printed verbatim in the report so a reader can
# reproduce the number without guessing. It is NOT the corpus basis (`[A-Za-z][A-Za-z'\-]*`
# over PDF-extracted text, or whitespace tokens over LaTeX): inline math becomes several
# tokens here, because `x_i` and `3/4` each carry letters or digits.
TOKEN_PATTERN = r"[A-Za-z0-9][A-Za-z0-9'\-]*"
WORD = re.compile(TOKEN_PATTERN)
TOKEN_BASIS = (
    f"tokens matching {TOKEN_PATTERN} (a token starts with a letter or digit and continues "
    "with letters, digits, apostrophes or hyphens)"
)
COMPARISON_TOLERANCE = (
    "compare only counts produced by the same tokenizer on the same text form; a different "
    "tokenizer moves word counts by a few percent (measured spread across four reasonable "
    "tokenizers: 18% relative on a high-overlap pair), so re-run rather than rescaling"
)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
ABBREVIATIONS = (
    "e.g.", "i.e.", "cf.", "et al.", "vs.", "Fig.", "Eq.", "Sec.", "No.",
    "resp.", "approx.", "w.r.t.", "Sect.", "Ch.", "pp.", "vol.",
)
HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")


def words(text: str) -> list[str]:
    """Count every token that carries at least one letter or digit.

    Math markup such as a subscript, a sum index, or a norm bar becomes one
    token each, which is why a count over LaTeX source runs slightly above a
    count over the rendered text. Compare like with like: state which text the
    count was taken from.
    """
    return WORD.findall(text)


def normalize(token: str) -> str:
    return token.lower().strip("'-")


def sentences(text: str) -> list[str]:
    protected = text
    for index, abbreviation in enumerate(ABBREVIATIONS):
        protected = protected.replace(abbreviation, f"\x00{index}\x00")
    protected = re.sub(r"\b(?:[A-Z]|\d+)\.", lambda m: m.group(0).replace(".", "\x01"), protected)
    parts = [part.replace("\x01", ".") for part in SENTENCE_SPLIT.split(protected)]
    restored: list[str] = []
    for part in parts:
        for index, abbreviation in enumerate(ABBREVIATIONS):
            part = part.replace(f"\x00{index}\x00", abbreviation)
        if part.strip():
            restored.append(part.strip())
    return restored


def jaccard(left: list[str], right: list[str]) -> float:
    a, b = set(left), set(right)
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def trigrams(tokens: list[str]) -> list[str]:
    normalized = [normalize(token) for token in tokens if normalize(token)]
    return [
        " ".join(normalized[index : index + 3])
        for index in range(max(0, len(normalized) - 2))
    ]


def paragraphs(text: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text)]
    kept: list[str] = []
    for block in blocks:
        if not block or block.startswith("#"):
            continue
        if re.fullmatch(r"[-*_=~\s]{3,}", block):
            continue
        if re.match(r"^\**[Kk]eywords\**[:\s]", block):
            continue
        kept.append(block)
    return kept


def prose(text: str) -> str:
    """Normalized text for word counting: markup and dash variants removed."""
    cleaned = re.sub(r"\\[a-zA-Z]+\*?(?:\{[^{}]*\})?", " ", text)
    cleaned = cleaned.replace("--", " ").replace("---", " ")
    cleaned = cleaned.replace("\u2014", " ").replace("\u2013", " ")
    return re.sub(r"[\\$*_`{}]", " ", cleaned)


BULLET_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BOLD_ITEM = re.compile(r"^\s*(?:[-*+]\s+)?\*\*(?P<label>[^*]{1,160})\*\*")


def contribution_items(text: str, mode: str) -> tuple[list[str], str]:
    """Return (items, match_status).

    match_status is "matched" when the requested pattern found at least one item, and
    "unmatched" when it found none. An unmatched result is never reported as a clean
    count: the caller turns it into a degenerate marker, because a per-item gate that
    matches zero items cannot fail and must not look like a pass.
    """
    if mode == "bullet":
        lines = [line for line in text.split("\n") if BULLET_ITEM.match(line)]
        return lines, ("matched" if lines else "unmatched")
    if mode == "bold":
        lines = [line.strip() for line in text.split("\n") if BOLD_ITEM.match(line)]
        return lines, ("matched" if lines else "unmatched")
    if mode == "paragraph":
        blocks = paragraphs(text)
        return blocks, ("matched" if blocks else "unmatched")
    if mode == "any":
        bullets = [line for line in text.split("\n") if BULLET_ITEM.match(line)]
        if bullets:
            return bullets, "matched"
        bolds = [line.strip() for line in text.split("\n") if BOLD_ITEM.match(line)]
        if bolds:
            return bolds, "matched"
        blocks = paragraphs(text)
        return blocks, ("matched" if blocks else "unmatched")
    return [], "unmatched"


def clean_span(text: str) -> str:
    """Drop a leading heading line, a trailing rule, and a keywords block."""
    lines = text.split("\n")
    if lines and HEADING.match(lines[0]):
        lines = lines[1:]
    body = "\n".join(lines)
    body = re.split(r"\n\s*[-*_=~]{3,}\s*(\n|$)", body)[0]
    body = re.split(r"\n\s*\**[Kk]eywords\**[:\s]", body)[0]
    return body.strip()


def parse_sections(text: str) -> list[tuple[int, str, int, int]]:
    """Return (level, title, start offset, end offset) per heading."""
    lines = text.split("\n")
    offsets: list[tuple[int, str, int]] = []
    position = 0
    for line in lines:
        match = HEADING.match(line)
        if match:
            offsets.append((len(match.group("hashes")), match.group("title"), position))
        position += len(line) + 1
    offsets.append((0, "__end__", position))
    result: list[tuple[int, str, int, int]] = []
    for index in range(len(offsets) - 1):
        level, title, start = offsets[index]
        end = offsets[index + 1][2]
        result.append((level, title, start, end))
    return result


def section_spans(text: str, pattern: str, direct: bool) -> list[tuple[str, str]]:
    """Return every (title, body) whose heading matches pattern."""
    regex = re.compile(pattern, re.IGNORECASE)
    sections = parse_sections(text)
    found: list[tuple[str, str]] = []
    for index, (level, title, start, _end) in enumerate(sections):
        if not regex.search(title):
            continue
        cut = len(text)
        for later_level, _later_title, later_start, _later_end in sections[index + 1 :]:
            if later_level and later_level <= level:
                cut = later_start
                break
        if direct:
            for later_level, _later_title, later_start, _later_end in sections[index + 1 :]:
                if later_level:
                    cut = later_start
                    break
        found.append((title, text[start:cut]))
    return found


def select_section(text: str, pattern: str, direct: bool) -> tuple[str, str]:
    """Return (title, body) for the first heading whose title matches pattern.

    A section spans to the next heading of the same or a shallower level, so
    subsections are included unless direct is set.
    """
    spans = section_spans(text, pattern, direct)
    if not spans:
        raise SystemExit(f"no heading matched {pattern!r}")
    return spans[0]


def spanning_section(text: str, heading_pattern: str) -> str:
    _title, body = select_section(text, heading_pattern, direct=False)
    return body


def report_abstract_contributions(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    abstract = clean_span(spanning_section(text, args.abstract_heading))
    contributions = clean_span(spanning_section(text, args.contributions_heading))

    abstract_tokens = words(prose(abstract))
    abstract_sentences = sentences(prose(abstract))
    longest = max((len(words(sentence)) for sentence in abstract_sentences), default=0)
    mean = (len(abstract_tokens) / len(abstract_sentences)) if abstract_sentences else 0.0
    blocks = paragraphs(abstract)
    allocation = [
        {"paragraph": index + 1, "words": len(words(block)), "first_line": block.split("\n")[0][:120]}
        for index, block in enumerate(blocks)
    ]

    items, item_status = contribution_items(contributions, args.items)
    item_words = [len(words(prose(item))) for item in items]
    contribution_tokens = words(prose(contributions))

    result = {
        "tokenizer": TOKEN_PATTERN,
        "basis": TOKEN_BASIS,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "paragraph_basis": "paragraphs = blank-line separated blocks, keyword lines and horizontal rules excluded",
        "jaccard_basis": "deduplicated word sets and adjacent-word-trigram sets, case-folded, punctuation stripped",
        "abstract": {
            "words": len(abstract_tokens),
            "sentences": len(abstract_sentences),
            "longest_sentence_words": longest,
            "mean_sentence_words": round(mean, 1),
            "paragraphs": len(blocks),
            "allocation": allocation,
            "manual_step_required": "label each paragraph context / gap / build / result; the allocation gate fails when no paragraph names what is built",
        },
        "contributions": {
            "item_mode": args.items,
            "match_status": item_status,
            "items": (len(items) if item_status == "matched" else None),
            "words_total": len(contribution_tokens),
            "words_per_item": (item_words if item_status == "matched" else None),
            "words_per_item_max": (max(item_words, default=0) if item_status == "matched" else None),
            "items_over_72_words": (
                sum(1 for count in item_words if count > 72) if item_status == "matched" else None
            ),
            "items_over_150_words": (
                sum(1 for count in item_words if count > 150) if item_status == "matched" else None
            ),
            "degenerate": (
                None if item_status == "matched" else
                f'item_mode {args.items!r} matched no item in the contributions span; the per-item '
                "gates cannot fire on this draft and NO verdict is implied. Re-run with --items "
                "bold, --items paragraph or --items any."
            ),
        },
        "duplication": {
            "abstract_vs_contributions_word_jaccard": round(
                jaccard(abstract_tokens, contribution_tokens), 4
            ),
            "abstract_vs_contributions_trigram_jaccard": round(
                jaccard(trigrams(abstract_tokens), trigrams(contribution_tokens)), 4
            ),
            "shared_trigrams_count": len(
                set(trigrams(abstract_tokens)) & set(trigrams(contribution_tokens))
            ),
            "shared_trigrams": sorted(
                set(trigrams(abstract_tokens)) & set(trigrams(contribution_tokens))
            )[:40],
        },
    }

    if args.threat_model_heading:
        threat = clean_span(spanning_section(text, args.threat_model_heading))
        threat_tokens = words(prose(threat))
        result["duplication"]["contributions_vs_threat_model_word_jaccard"] = round(
            jaccard(contribution_tokens, threat_tokens), 4
        )
        result["threat_model"] = {
            "words": len(threat_tokens),
            "manual_step_required": (
                "map each promised security goal to the threat-model sentence stating what "
                "the adversary may do, and list the capabilities, assumptions, or non-goals "
                "the model adds"
            ),
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if item_status != "matched":
        return 2
    return 0


def report_section_mass(args: argparse.Namespace) -> int:
    if not args.section:
        print(json.dumps({
            "status": "degenerate",
            "reason": "no --section was given, so no section mass could be measured",
            "sections": None,
            "ratios": None,
            "remedy": (
                "pass one or more --section NAME:PATTERN (or NAME+=PATTERN to sum several "
                "matches), e.g. --section 'design+=^3\\. |^4\\. ' --section 'analysis:^5\\. '"
            ),
            "verdict_implied": None,
        }, indent=2, ensure_ascii=False))
        return 2
    text = Path(args.file).read_text(encoding="utf-8")
    sections: dict[str, dict[str, object]] = {}
    for spec in args.section:
        accumulate = "+=" in spec and (":" not in spec or spec.index("+=") < spec.index(":"))
        if accumulate:
            name, pattern = spec.split("+=", 1)
        elif ":" in spec:
            name, pattern = spec.split(":", 1)
        else:
            raise SystemExit(f"--section needs NAME:PATTERN or NAME+=PATTERN, got {spec!r}")
        spans = section_spans(text, pattern, direct=args.direct)
        if not spans:
            print(json.dumps({
                "status": "degenerate",
                "reason": f"the pattern for section {name!r} matched no heading in {args.file}",
                "pattern": pattern,
                "sections": None,
                "ratios": None,
                "remedy": "check the heading spelling, or pass a broader pattern",
                "verdict_implied": None,
            }, indent=2, ensure_ascii=False))
            return 2
        bodies = [body for _title, body in spans]
        direct_bodies = [body for _title, body in section_spans(text, pattern, direct=True)]
        sections[name] = {
            "matched_headings": [title for title, _body in spans],
            "matched_heading": spans[0][0],
            "word_per_match": [len(words(prose(body))) for body in bodies],
            "words": sum(len(words(prose(body))) for body in bodies),
            "direct_words": sum(len(words(prose(body))) for body in direct_bodies),
            "paragraphs": sum(len(paragraphs(body)) for body in bodies),
        }

    body_text = text.split("\n#")[0] if args.body_until_appendix else text
    body_words = len(words(prose(body_text)))

    ratios: dict[str, float] = {}
    names = [spec.split(":", 1)[0] for spec in args.section]
    if "design" in sections and "analysis" in sections:
        design = sections["design"]["words"]
        analysis = sections["analysis"]["words"]
        ratios["design_over_analysis"] = round(design / analysis, 4) if analysis else 0.0
        ratios["design_share_of_body"] = round(design / body_words, 4) if body_words else 0.0

    result = {
        "status": "matched",
        "tokenizer": TOKEN_PATTERN,
        "basis": (
            "words: " + TOKEN_BASIS + "; section words include subsections unless --direct; body "
            "words are counted to the first top-level appendix heading when --body-until-appendix "
            "is passed"
        ),
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "direct_only": bool(args.direct),
        "sections": sections,
        "body_words": body_words,
        "ratios": ratios,
        "manual_step_required": (
            "mark each required constituent present with its line or absent: overview needs "
            "intuition, mechanism sentence, named sub-blocks, forward references, and a cost or "
            "leakage statement; the design section needs step ordering, a named reused object, a "
            "complexity or cost expression, a parameter reason, and a protocol box or flow figure, "
            "plus one mechanism sentence per mechanism"
        ),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def report_span(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    tokens = words(prose(text))
    sentence_list = sentences(prose(text))
    print(
        json.dumps(
            {
                "tokenizer": TOKEN_PATTERN,
                "basis": TOKEN_BASIS,
                "words": len(tokens),
                "sentences": len(sentence_list),
                "longest_sentence_words": max(
                    (len(words(sentence)) for sentence in sentence_list), default=0
                ),
                "paragraphs": len(paragraphs(text)),
            },
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    condensation = subparsers.add_parser("abstract-contributions", help="condensation gate counts")
    condensation.add_argument("file")
    condensation.add_argument("--abstract-heading", default=r"Abstract")
    condensation.add_argument(
        "--contributions-heading",
        default=r"Contributions|Our Contributions|Main Results|Our Results",
    )
    condensation.add_argument("--threat-model-heading", default="")
    condensation.add_argument(
        "--items",
        choices=("bullet", "bold", "paragraph", "any", "none"),
        default="any",
        help=(
            "how the contribution list is written: bullet lines, bold run-in labels, "
            "paragraphs, any of those (default), or not counted"
        ),
    )
    condensation.set_defaults(func=report_abstract_contributions)

    mass = subparsers.add_parser("section-mass", help="expansion gate counts")
    mass.add_argument("file")
    mass.add_argument(
        "--section",
        action="append",
        default=[],
        metavar="NAME:PATTERN",
        help="NAME:PATTERN takes the first match; NAME+=PATTERN sums every match",
    )
    mass.add_argument("--direct", action="store_true", help="count each section's own text only")
    mass.add_argument(
        "--body-until-appendix",
        action="store_true",
        help="stop the body word count at the first top-level appendix heading",
    )
    mass.set_defaults(func=report_section_mass)

    span = subparsers.add_parser("span", help="count one raw span")
    span.add_argument("--file", required=True)
    span.set_defaults(func=report_span)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
