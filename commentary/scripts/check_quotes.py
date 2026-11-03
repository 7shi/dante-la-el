"""
Check that the quotation marks of each translation (<canticle>/<NN>.txt)
follow those of the original, line by line.

The original nests its quotes as «» > “” > ‘’, while the Modern Greek
translation writes every level as «» (or now and then “”), so the kind of
mark is not compared. Instead, the nesting depth - opening marks minus
closing marks, counted from the start of the canto - is compared at the end
of every line. In the translation ’ is the apostrophe of elision (γι’, απ’),
so only «» and “” count there; in the original ’ always closes a ‘.

Each run of consecutive lines whose depths differ is reported:

- shift: a short run that the next lines resolve; usually a quote boundary
  that the translation's word order moved to a neighbouring line, which is
  fine, but worth a look
- mismatch: a long run, or one that lasts to the end of the canto; a mark
  is missing or extra and the difference is carried along

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
    parser.add_argument("-s", "--shift", type=int, default=2, metavar="N",
                        help="Longest run reported as a shift rather than a mismatch "
                             "(default: 2)")
    args = parser.parse_args()
    canticles = args.canticles or CANTICLES
    if err := check_canto_spec(canticles, args.canto):
        parser.error(err)

    mismatches = shifts = 0
    for canticle in canticles:
        for canto in select_cantos(canticle, args.canto):
            path = args.dir / canticle / f"{canto:02d}.txt"
            if not path.exists():
                continue
            translations = path.read_text().splitlines()
            total = len(ref(f"{canticle} {canto}"))
            for first, last in runs(canticle, canto, translations):
                span = f"{first}" if first == last else f"{first}-{last}"
                if last - first + 1 <= args.shift and last < total:
                    kind = "shift"
                    shifts += 1
                else:
                    kind = "mismatch"
                    mismatches += 1
                print(f"{path}: {span}: {kind}")
    print(f"\n{mismatches} mismatch(es), {shifts} shift(s)")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
