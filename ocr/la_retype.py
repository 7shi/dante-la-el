"""Append a fixes.tsv row that replaces a page, or a part of it, by a retyped text
(procedure step 6).

    la_retype.py WORK PAGE FILE NOTE [--old OLDFILE]

For a page too broken for its marks: decide every mark of PAGE (la_mine.py, usually
`left`), rerun la_markresolve.py so that WORK/out/PAGE.txt holds the resolved text, then
run this with FILE, the page retyped from the scan. The row replaces the whole text of
WORK/out/PAGE.txt by FILE's text; with --old, only the text of OLDFILE (a part of the
page, e.g. one column, copied from WORK/out/PAGE.txt), which must occur there exactly
once. Line breaks are written as `⏎`; leading and trailing blank lines are dropped.
Rerun la_markresolve.py afterwards and compare WORK/out/PAGE.txt with FILE."""

import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("work"); ap.add_argument("page"); ap.add_argument("file"); ap.add_argument("note")
    ap.add_argument("--old", metavar="OLDFILE", help="replace only this part of the page")
    a = ap.parse_args()
    out = Path(a.work, "out", f"{a.page}.txt")
    if not out.exists(): sys.exit(f"{out} missing: decide the page's marks and rerun la_markresolve.py")
    text = out.read_text(encoding="utf-8")
    old = (Path(a.old).read_text(encoding="utf-8") if a.old else text).strip("\n")
    new = Path(a.file).read_text(encoding="utf-8").strip("\n")
    if text.count(old) != 1: sys.exit(f"the old text occurs {text.count(old)} times in {out}")
    if "\t" in old + new + a.note: sys.exit("a tab in the text or the note")
    with open(Path(a.work, "fixes.tsv"), "a", encoding="utf-8") as f:
        f.write(f"{a.page}\t{old.replace(chr(10), '⏎')}\t{new.replace(chr(10), '⏎')}\t{a.note}\n")
    print("added", len(old), "->", len(new), "characters")


if __name__ == "__main__":
    main()
