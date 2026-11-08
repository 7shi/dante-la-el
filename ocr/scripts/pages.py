"""Writes the pages FIRST–LAST of a converted text, cut at its page markers.

The files of TEXTDIR (`texts/la`, …; README.md left out) are read in order, and the text
from the marker of scan FIRST (`<!-- p. 26 (0080) -->`) up to the marker after scan LAST
is written, markers included. FIRST and LAST are scan numbers, the number in parentheses.
It is the text given to a reader of the read-through (ocr/PLAN.md, "Read-through").

    uv run ocr/scripts/pages.py texts/la 79 98 -o tmp/read/0079-0098.md
"""
import argparse
import re
import sys
from pathlib import Path

MARK = re.compile(r"^<!-- p\. .*\((\d+)\) -->$")

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
ap.add_argument("textdir", type=Path, help="directory of the converted text (e.g. texts/la)")
ap.add_argument("first", type=int, help="first scan number")
ap.add_argument("last", type=int, help="last scan number")
ap.add_argument("-o", "--output", type=Path, help="output file (default: stdout)")
a = ap.parse_args()

out, keep, seen = [], False, []
for f in sorted(a.textdir.glob("*.md")):
    if f.name == "README.md":
        continue
    for line in f.read_text(encoding="utf-8").split("\n"):
        m = MARK.match(line)
        if m:
            keep = a.first <= int(m[1]) <= a.last
            if keep:
                seen.append(m[1])
        if keep:
            out.append(line)

if not seen:
    sys.exit(f"no page markers for {a.first}–{a.last} in {a.textdir}")
text = "\n".join(out).rstrip("\n") + "\n"
if a.output:
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(text, encoding="utf-8")
    print(f"{len(seen)} pages ({seen[0]}–{seen[-1]}), {len(text.split())} words: {a.output}",
          file=sys.stderr)
else:
    sys.stdout.write(text)
