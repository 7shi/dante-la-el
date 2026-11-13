"""
Check that the quotation marks of each translation (<canticle>/<NN>.txt)
follow those of the original, line by line.

The original nests its quotes as «» > “” > ‘’, while a translation may write
the levels with other marks (Modern Greek writes every level as «», or now
and then “”), so the kind of mark is not compared. Instead, the nesting
depth - opening marks minus closing marks, counted from the start of the
canto - is compared at the end of every line. Which marks count in the
translation, and which are apostrophes instead, is set per language in
LANGUAGES (quotes, apostrophe); in the original ’ always closes a ‘.

The translation must follow the original line by line, so each run of
consecutive lines whose depths differ is reported as a mismatch: a mark is
missing or extra, or a quote boundary has moved to a neighbouring line.

With a source other than the Italian (-s grc), the marks are compared line
by line instead: Musurus's Greek opens a speech with “, closes it with ” or “,
opens every line inside it with „ (‚ „ inside a quote within it, which opens
with ‘“ and closes with ”’), so the depth cannot be counted from the marks
alone. The translation writes the same marks, so each line must hold the
same sequence of marks as its original: “”«» count as one kind, and ’ after
a letter is an apostrophe of elision. Each run of consecutive lines whose
sequences differ is reported.

The model is not called.
"""

import argparse
import re
import sys
from pathlib import Path

from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from generate import LANGUAGES
from source import SOURCES, source_lines

CANTICLES = ["inferno", "purgatorio", "paradiso"]

ORIG_OPEN, ORIG_CLOSE = "«“‘", "»”’"

# Quote marks compared line by line for a source other than the Italian;
# “”«» are one kind, the others are kept apart
MARK_KINDS = str.maketrans({"”": "“", "«": "“", "»": "“"})
MARKS_RE = re.compile(r"[“”«»„‚‘]|(?<!\w)’")


def count(text: str, marks: str) -> int:
    return sum(text.count(c) for c in marks)


def marks(text: str) -> str:
    """The quote marks of a line, in order, by kind."""
    return "".join(MARKS_RE.findall(text)).translate(MARK_KINDS)


def add_run(result: list[list[int]], no: int):
    if result and result[-1][1] == no - 1:
        result[-1][1] = no
    else:
        result.append([no, no])


def runs(canticle: str, canto: int, translations: list[str],
         language: dict, source: str = "it") -> list[tuple[int, int]]:
    """[first, last] line numbers of each run whose depths (or, for a source
    other than the Italian, whose marks) differ."""
    lines = source_lines(source, canticle, canto)
    result: list[list[int]] = []
    if source != "it":
        for line, trans in zip(lines, translations):
            if marks(line.text) != marks(trans):
                add_run(result, line.no)
        return [(first, last) for first, last in result]
    trans_open, trans_close = language["quotes"]
    apostrophe = re.compile(language["apostrophe"]) if language.get("apostrophe") else None
    depth_orig = depth_trans = 0
    for line, trans in zip(lines, translations):
        depth_orig += count(line.text, ORIG_OPEN) - count(line.text, ORIG_CLOSE)
        if apostrophe:
            trans = apostrophe.sub("", trans)
        depth_trans += count(trans, trans_open) - count(trans, trans_close)
        if depth_orig != depth_trans:
            add_run(result, line.no)
    return [(first, last) for first, last in result]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("canticles", nargs="*", metavar="canticle", choices=CANTICLES,
                        help="Canticles to check (default: all)")
    parser.add_argument("-l", "--lang-code", choices=list(LANGUAGES), required=True,
                        help="Language code of the target language (e.g. el)")
    parser.add_argument("-d", "--dir", type=Path, required=True,
                        help="Directory holding <canticle>/<NN>.txt (e.g. el)")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    parser.add_argument("-s", "--source", choices=list(SOURCES), default="it",
                        help="Source text the translations follow (default: it)")
    args = parser.parse_args()
    canticles = args.canticles or SOURCES[args.source]["canticles"]
    if err := check_canto_spec(canticles, args.canto):
        parser.error(err)
    if missing := set(canticles) - set(SOURCES[args.source]["canticles"]):
        parser.error(f"source {args.source} has no {', '.join(sorted(missing))}")

    mismatches = 0
    for canticle in canticles:
        for canto in select_cantos(canticle, args.canto):
            path = args.dir / canticle / f"{canto:02d}.txt"
            if not path.exists():
                continue
            translations = path.read_text().splitlines()
            for first, last in runs(canticle, canto, translations,
                                    LANGUAGES[args.lang_code], args.source):
                span = f"{first}" if first == last else f"{first}-{last}"
                print(f"{path}: {span}")
                mismatches += 1
    print(f"\n{mismatches} mismatch(es)")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
