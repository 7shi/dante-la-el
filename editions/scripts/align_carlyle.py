"""
Cut Carlyle's Inferno (texts/en) into blocks of Italian lines and the
English that renders them, for grammar.py.

The pages of Carlyle's edition print the English prose above the Italian
verse it renders, but the English is cut where the page ends, often in the
middle of a sentence, while the Italian is cut at a whole line; at a page
break the two can be a clause or a few lines apart. The blocks are cut where
the English and the Italian part together, one cut near every page break
(or none, where a block of a line or two is joined to the one before it),
and kept in editions/en-blocks.txt (read by source.carlyle_blocks):

    canto:line<TAB>English before|English after

The block ends with Italian line `line`, and its English ends at the `|`;
the words around it must occur only once in the English of the canto.

- draft: a first cut for every page break, at the clause end (`.;:!?`)
  nearest the break in each language, choosing the pair whose English and
  Italian added to or taken from the page agree best in length (about ten
  words a line); the cuts where they do not agree are marked `# ?`. Length
  is a poor guide (a fifth of the cuts it chose were wrong), so every cut of
  editions/en-blocks.txt was then checked against the text by hand:
  the draft is not to be written over it
- check: read the file (checking that every cut is found once and in
  order), and list the blocks whose English and Italian disagree in length
  (by default the file in editions/)
"""

import argparse
import re
import sys
from pathlib import Path

# The scripts shared with the commentaries
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "commentary" / "scripts"))

from source import (BLOCKS_PATH, carlyle_blocks, carlyle_english, carlyle_passages,
                    cut_positions)

CANTOS = range(1, 35)
# About this many words of Carlyle's English render a line of the Italian
WORDS_PER_LINE = 10
# A cut whose English and Italian moved from the page break differ by more
# words than this is marked for checking
TOLERANCE = 12
EN_CLAUSE_RE = re.compile(r"[.;:!?][”’)]*(?= )")
IT_CLAUSE_RE = re.compile(r"[.;:!?][”’»)]*$")


def context(text: str, cut: int) -> str:
    """Words around the cut, as many as make it unique in text."""
    before, after = text[:cut].split(), text[cut:].split()
    for n in range(3, 30):
        spec = " ".join(before[-n:]) + "|" + " ".join(after[:n])
        if len(cut_positions(text, spec)) == 1:
            return spec
    raise ValueError(f"no unique context at {cut}")


def words(text: str) -> int:
    return len(text.split())


def draft(out):
    print("# canto:line<TAB>English before|English after (see scripts/align_carlyle.py); a draft",
          file=out)
    marked = 0
    for canto in CANTOS:
        passages = carlyle_passages(canto)
        text, page_ends = carlyle_english(passages)
        lines = [line for p in passages for line in p.lines]
        ends = [line.no for line in lines if IT_CLAUSE_RE.search(line.text.rstrip())]
        en_ends = [m.end() for m in EN_CLAUSE_RE.finditer(text)]
        for passage, ec in zip(passages[:-1], page_ends):
            iend = passage.end
            en_options = [e for e in en_ends if e < ec][-1:] + [e for e in en_ends if e >= ec][:1]
            it_options = [n for n in ends if n < iend][-1:] + [n for n in ends if n >= iend][:1]
            best = min(
                ((abs((words(text[ec:e]) if e >= ec else -words(text[e:ec]))
                      - WORDS_PER_LINE * (n - iend)), e, n)
                 for e in en_options for n in it_options),
            )
            score, e, n = best
            mark = "\t# ?" if score > TOLERANCE else ""
            marked += bool(mark)
            print(f"{canto}:{n}\t{context(text, e)}{mark}", file=out)
    print(f"{marked} cuts marked for checking", file=sys.stderr)


def check(path: Path):
    count = 0
    for canto in CANTOS:
        blocks = carlyle_blocks(canto, path)
        count += len(blocks)
        for block in blocks:
            size = block.end - block.start + 1
            if abs(words(block.english) - WORDS_PER_LINE * size) > WORDS_PER_LINE * size // 2 + TOLERANCE:
                print(f"{canto}:{block.start}-{block.end}\t{size} lines, "
                      f"{words(block.english)} words")
    print(f"{count} blocks", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("draft", help="Write a first cut of every page break")
    p.add_argument("-o", "--output", type=argparse.FileType("w"), default=sys.stdout,
                   help="Output file (default: standard output)")
    p = sub.add_parser("check", help="Read the blocks and list those of odd length")
    p.add_argument("file", type=Path, nargs="?", default=BLOCKS_PATH,
                   help=f"The file of cuts (default: {BLOCKS_PATH.name} in editions/)")
    args = parser.parse_args()
    if args.mode == "draft":
        draft(args.output)
    else:
        check(args.file)


if __name__ == "__main__":
    main()
