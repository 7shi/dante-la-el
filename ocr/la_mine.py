"""Append decisions of the review to WORK/mine.tsv (procedure step 6).

    la_mine.py WORK PAGE K[,K...]=DECISION[|NOTE] ...

Each argument decides the marks K of PAGE (the `k` of review.tsv) with DECISION (`left`,
`right` or `text:...`, `⏎` for a line break) and an optional NOTE after `|`. The line of
each mark is taken from WORK/review.tsv. A mark not in review.tsv, or already in mine.tsv,
stops the call before anything is written. `la_view.py next WORK` shows the marks still to
decide."""

import argparse
import csv
import sys
from pathlib import Path

HEAD = "page\tline\tk\tdecision\tnote\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("work"); ap.add_argument("page")
    ap.add_argument("items", nargs="+", metavar="K[,K...]=DECISION[|NOTE]")
    a = ap.parse_args()
    rows = list(csv.reader(open(Path(a.work, "review.tsv"), encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    line = {(r[0], r[2]): r[1] for r in rows[1:]}
    mine = Path(a.work, "mine.tsv"); have = set()
    if mine.exists():
        have = {(r[0], r[2]) for r in csv.reader(open(mine, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}
    p = a.page; out = []
    for it in a.items:
        if "=" not in it: sys.exit(f"{it}: no `=`")
        ks, d = it.split("=", 1); d, _, note = d.partition("|")
        if d not in ("left", "right") and not d.startswith("text:"): sys.exit(f"{it}: decision {d!r}")
        for k in ks.split(","):
            if (p, k) not in line: sys.exit(f"{p}:{k} not in review.tsv")
            if (p, k) in have: sys.exit(f"{p}:{k} already in mine.tsv")
            have.add((p, k)); out.append(f"{p}\t{line[p, k]}\t{k}\t{d}\t{note}\n")
    new = not mine.exists()
    with open(mine, "a", encoding="utf-8") as f: f.write((HEAD if new else "") + "".join(out))
    print(len(out), "added")


if __name__ == "__main__":
    main()
