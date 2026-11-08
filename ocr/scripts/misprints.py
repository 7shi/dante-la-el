"""Checks the misprint marks of the pages of DIR against DIR/misprints.tsv (ocr/PLAN.md,
"Decisions"; ocr/la/PLAN.md, "Misprint marks").

Every mark `{{printed|fixed}}` in a page must be one row of the TSV with `applied` `yes`
(page, line, printed, fixed), and every such row one mark. With --fix-lines, a row whose
mark is found on another line of its page (once) gets that line written into the TSV.
The page names are the digits of the page files of DIR (`0001` in ocr/la, `001` in ocr/en).

    uv run ocr/scripts/misprints.py ocr/la [--fix-lines]
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

MARK = re.compile(r"\{\{([^{}|]*)\|([^{}|]*)\}\}")
HEAD = ["page", "line", "printed", "fixed", "applied", "source", "note"]
SOURCES = {"page", "edition", "dante", "other"}


def pages(root):
    """The page files of root: the .txt files named by digits only."""
    return sorted(f for f in root.glob("*.txt") if f.stem.isdigit())


def marks(files):
    """Counter of (page, line, printed, fixed) over the marks of the pages."""
    out = Counter()
    for f in files:
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            if "{{" in line and not MARK.search(line):
                print(f"{f.stem}:{n}: a broken mark: {line}")
            for m in MARK.finditer(line):
                out[(f.stem, n, m.group(1), m.group(2))] += 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dir", type=Path, help="the directory of the pages and misprints.tsv (ocr/la)")
    ap.add_argument("--fix-lines", action="store_true", help="write the lines of moved marks into the TSV")
    a = ap.parse_args()
    files = pages(a.dir)
    width = len(files[0].stem)
    assert all(len(f.stem) == width for f in files), "page names of different lengths"
    tsv = a.dir / "misprints.tsv"
    lines = tsv.read_text(encoding="utf-8").rstrip("\n").split("\n")
    assert lines[0].split("\t") == HEAD, "unexpected header"
    rows = [l.split("\t") for l in lines[1:]]
    bad = 0
    for i, r in enumerate(rows, 2):
        if len(r) != len(HEAD) or not re.fullmatch(rf"\d{{{width}}}", r[0]) or not r[1].isdigit() \
                or r[4] not in ("yes", "no") or r[5] not in SOURCES or r[2] == r[3]:
            print(f"{tsv}:{i}: a malformed row: {r}")
            bad += 1
    found = marks(files)
    want = Counter((r[0], int(r[1]), r[2], r[3]) for r in rows if r[4] == "yes")
    missing, extra = want - found, found - want
    if a.fix_lines and missing:
        for r in rows:
            k = (r[0], int(r[1]), r[2], r[3])
            if r[4] != "yes" or k not in missing:
                continue
            moved = [e for e in extra if (e[0], e[2], e[3]) == (r[0], r[2], r[3])]
            if len(moved) == 1:
                print(f"{r[0]}: {r[2]!r} moved from line {r[1]} to {moved[0][1]}")
                r[1] = str(moved[0][1])
                extra -= Counter([moved[0]])
                missing -= Counter([k])
        tsv.write_text("\n".join(["\t".join(HEAD)] + ["\t".join(r) for r in rows]) + "\n", encoding="utf-8")
    for k in sorted(missing):
        print(f"{k[0]}:{k[1]}: no mark for the row {k[2]!r} -> {k[3]!r}")
    for k in sorted(extra):
        print(f"{k[0]}:{k[1]}: a mark with no row: {{{{{k[2]}|{k[3]}}}}}")
    n = sum(found.values())
    print(f"{len(rows)} rows, {sum(want.values())} applied; {n} marks; "
          f"{bad + sum(missing.values()) + sum(extra.values())} problems")
    sys.exit(1 if bad or missing or extra else 0)


if __name__ == "__main__":
    main()
