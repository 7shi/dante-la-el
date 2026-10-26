"""Format checks of ocr/la pages: the verse blocks' tercet numbers and leftover marks.

    la_seqcheck.py FIRST LAST [-d DIR ...] [-v] [-o OUT]

For each page file (the first DIR that has PAGE.txt; default ocr/la), the verse blocks are
the blank-line separated blocks containing a tercet number (`1 `, `27 `). Listed:

- `seq`: a block whose numbers do not run one by one (a number missing or wrong);
- `it/la`: a page with two verse blocks (the Italian and the Latin) whose numbers differ;
- `sup`: a tercet number or gloss mark in superscript digits (`²⁷`, `(¹)`);
- `leftover`: `<sup>`, `[For ` (a delegate's note), a line of only `—` (a rule written as
  a dash), or a double space;
- `indent`: a line starting with a space.

la_check.py checks the tercet numbers across pages (every third line, continuity) and the
rules; this one checks what it does not. One line per page with hits (all pages with -v):
the page, the first number of each verse block, the hits."""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "la"


def check(text):
    blocks = [b for b in text.split("\n\n") if re.search(r"(?m)^\d+ \D", b)]
    seqs = [[int(m) for m in re.findall(r"(?m)^(\d+) ", b)] for b in blocks]
    hits = []
    bad = [s for s in seqs if s != list(range(s[0], s[0] + len(s)))]
    if bad: hits.append(f"seq {bad}")
    if len(seqs) == 2 and seqs[0] != seqs[1]: hits.append(f"it/la {seqs}")
    if re.search(r"(?m)^[⁰¹²³⁴⁵⁶⁷⁸⁹]+ |\([⁰¹²³⁴⁵⁶⁷⁸⁹]+[).,]", text): hits.append("sup")
    if re.search(r"<sup>|\[For |^—$|  ", text, re.M): hits.append("leftover")
    if re.search(r"(?m)^ ", text): hits.append("indent")
    return [s[0] for s in seqs], hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-d", "--dir", action="append",
                    help="page files; repeatable, the first that has the page is read (default ocr/la)")
    ap.add_argument("-v", "--verbose", action="store_true", help="list the pages without hits too")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    a = ap.parse_args()
    dirs = a.dir or [str(ROOT)]
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    for n in range(a.first, a.last + 1):
        page = f"{n:04d}"
        f = next((Path(d, f"{page}.txt") for d in dirs if Path(d, f"{page}.txt").exists()), None)
        if f is None: continue
        firsts, hits = check(f.read_text(encoding="utf-8"))
        if hits or a.verbose:
            print(page, firsts, "; ".join(hits), file=out)
    if a.output: out.close()


if __name__ == "__main__":
    main()
