"""Applies transcription fixes to the page files of a source.

FIXES is a TSV, one fix per row: `PAGE:LINE<TAB>old<TAB>new` (line counted from 1).
`old` must occur exactly once in that line; otherwise nothing is written and the row is
reported. Each fixed line is printed. Rows starting with `#` and blank rows are skipped.

    uv run ocr/scripts/txtfix.py ocr/la fixes.tsv
    uv run ocr/scripts/txtfix.py ocr/la fixes.tsv -n     # check only
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
ap.add_argument("dir", type=Path, help="directory of the page files (e.g. ocr/la)")
ap.add_argument("fixes", type=Path, help="TSV: PAGE:LINE, old, new")
ap.add_argument("-n", "--dry-run", action="store_true", help="check the rows, write nothing")
a = ap.parse_args()

pages, rows, bad = {}, [], 0
for n, row in enumerate(a.fixes.read_text(encoding="utf-8").split("\n"), 1):
    if not row.strip() or row.startswith("#"):
        continue
    try:
        key, old, new = row.split("\t")
        page, line = key.split(":")
        line = int(line)
    except ValueError:
        print(f"row {n}: not PAGE:LINE<TAB>old<TAB>new: {row!r}", file=sys.stderr)
        bad += 1
        continue
    f = a.dir / f"{page}.txt"
    if f not in pages:
        if not f.exists():
            print(f"row {n}: no file {f}", file=sys.stderr)
            bad += 1
            continue
        pages[f] = f.read_text(encoding="utf-8").split("\n")
    ls = pages[f]
    if not 1 <= line <= len(ls):
        print(f"row {n}: {key}: no such line", file=sys.stderr)
        bad += 1
        continue
    c = ls[line - 1].count(old)
    if c != 1:
        print(f"row {n}: {key}: {old!r} occurs {c} times in {ls[line - 1]!r}", file=sys.stderr)
        bad += 1
        continue
    ls[line - 1] = ls[line - 1].replace(old, new)
    rows.append((key, ls[line - 1]))

if bad:
    sys.exit(f"{bad} bad rows: nothing written")
for key, text in rows:
    print(f"{key}\t{text}")
if not a.dry_run:
    for f, ls in pages.items():
        f.write_text("\n".join(ls), encoding="utf-8")
