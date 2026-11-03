"""
Check that the quotation marks of each translation (<canticle>/<NN>.txt)
follow those of the original, line by line.

The original nests its quotes as «» > “” > ‘’, while the Modern Greek
translation writes every level as «» (or now and then “”), so the kind of
mark is not compared. Instead, the nesting depth - opening marks minus
closing marks, counted from the start of the canto - is compared at the end
of every line. In the translation ’ is the apostrophe of elision (γι’, απ’),
so only «» and “” count there; in the original ’ always closes a ‘.

The translation must follow the original line by line, so each run of
consecutive lines whose depths differ is reported as a mismatch: a mark is
missing or extra, or a quote boundary has moved to a neighbouring line.

The model is not called.
"""

import argparse
import sys
from pathlib import Path

from dante_corpus import ref
from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos

CANTICLES = ["inferno", "purgatorio", "paradiso"]

ORIG_OPEN, ORIG_CLOSE = "«“‘", "»”’"
TRANS_OPEN, TRANS_CLOSE = "«“", "»”"


def count(text: str, marks: str) -> int:
    return sum(text.count(c) for c in marks)


def runs(canticle: str, canto: int, translations: list[str]) -> list[tuple[int, int]]:
    """[first, last] line numbers of each run whose depths differ."""
    lines = ref(f"{canticle} {canto}")
    depth_orig = depth_trans = 0
    result: list[list[int]] = []
    for line, trans in zip(lines, translations):
        depth_orig += count(line.text, ORIG_OPEN) - count(line.text, ORIG_CLOSE)
        depth_trans += count(trans, TRANS_OPEN) - count(trans, TRANS_CLOSE)
        if depth_orig != depth_trans:
            if result and result[-1][1] == line.no - 1:
                result[-1][1] = line.no
            else:
                result.append([line.no, line.no])
    return [(first, last) for first, last in result]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("canticles", nargs="*", metavar="canticle", choices=CANTICLES,
                        help="Canticles to check (default: all)")
    parser.add_argument("-d", "--dir", type=Path, required=True,
                        help="Directory holding <canticle>/<NN>.txt (e.g. el)")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    args = parser.parse_args()
    canticles = args.canticles or CANTICLES
    if err := check_canto_spec(canticles, args.canto):
        parser.error(err)

    mismatches = 0
    for canticle in canticles:
        for canto in select_cantos(canticle, args.canto):
            path = args.dir / canticle / f"{canto:02d}.txt"
            if not path.exists():
                continue
            translations = path.read_text().splitlines()
            for first, last in runs(canticle, canto, translations):
                span = f"{first}" if first == last else f"{first}-{last}"
                print(f"{path}: {span}")
                mismatches += 1
    print(f"\n{mismatches} mismatch(es)")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
