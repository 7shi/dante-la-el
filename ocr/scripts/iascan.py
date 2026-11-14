"""Checks the scans of a book on Internet Archive before choosing one (ocr/GUIDE.md, "Choosing the scan").

The OCR that Internet Archive provides for each scan is enough: `_djvu.xml` has the text
of each leaf, `_djvu.txt` the running text.

    uv run ocr/scripts/iascan.py fetch -d tmp/ia ID...           # the OCR files into tmp/ia/ID/
    uv run ocr/scripts/iascan.py image -d tmp/ia ID LEAF...      # leaf images, ID-nLEAF.jpg
    uv run ocr/scripts/iascan.py leaves tmp/ia/ID/ID_djvu.xml    # page offsets, repeated leaves
    uv run ocr/scripts/iascan.py heads tmp/ia/ID/ID_djvu.xml 396 424
    uv run ocr/scripts/iascan.py diff A_djvu.txt B_djvu.txt      # revisions between printings
    uv run ocr/scripts/iascan.py pages ID_djvu.xml -d ocr/X/ia-ocr [--first 1 --last 400 --shift 0]

`leaves`: the printed page number of each leaf, from the first or last word of its first
or last line, minus the leaf number (1-based); the runs of a constant offset, and the
leaves off the commonest offset (a change that lasts marks a missing, repeated or inserted
leaf; a single one is mostly a misread number), and the leaves whose text repeats another's.
`heads`: the first and last line of leaves FIRST–LAST, to look at a place `leaves` marked.
`diff`: a word diff of two OCR texts, only the blocks where at least MIN words differ,
which leaves the rewritten passages above the OCR noise.
`pages`: the OCR of the chosen scan as page files, `DIR/PAGE.txt` (leaf + SHIFT, three
digits), one printed line per line, for `cmpread.py -i` (a reference column).
"""
import argparse
import difflib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

BASE = "https://archive.org/download"
FILES = ["_djvu.txt", "_djvu.xml", "_page_numbers.json"]


def download(url, path):
    try:
        with urllib.request.urlopen(url) as r:
            path.write_bytes(r.read())
        print(path)
    except Exception as e:
        print(f"{url}: {e}", file=sys.stderr)


def cmd_fetch(a):
    for ident in a.ids:
        d = a.dir / ident
        d.mkdir(parents=True, exist_ok=True)
        for s in FILES:
            download(f"{BASE}/{ident}/{ident}{s}", d / f"{ident}{s}")


def cmd_image(a):
    a.dir.mkdir(parents=True, exist_ok=True)
    for leaf in a.leaves:
        # the leaf images are numbered from 0 (n0) and the leaves of _djvu.xml from 1
        download(f"{BASE}/{a.id}/page/n{leaf - 1}.jpg", a.dir / f"{a.id}-n{leaf}.jpg")


def read_leaves(path):
    leaves = []
    for _, el in ET.iterparse(path):
        if el.tag == "OBJECT":
            leaves.append([" ".join(w.text or "" for w in l.iter("WORD")) for l in el.iter("LINE")])
            el.clear()
    return leaves


def page_number(lines):
    for l in lines[:1] + lines[-1:]:
        toks = l.split()
        for t in toks[:1] + toks[-1:]:
            if re.fullmatch(r"\d{1,3}", t) and int(t) > 0:
                return int(t)
    return None


def cmd_leaves(a):
    leaves = read_leaves(a.xml)
    nums = [(i, n) for i, n in ((i, page_number(l)) for i, l in enumerate(leaves, 1)) if n]
    out = [f"{a.xml.name}: {len(leaves)} leaves, {len(nums)} with a page number"]
    runs = []
    for i, n in nums:
        if runs and runs[-1][2] == i - n:
            runs[-1][1] = (i, n)
            runs[-1][3] += 1
        else:
            runs.append([(i, n), (i, n), i - n, 1])
    out.append(f"runs of a constant offset (printed page = leaf - offset), {a.min_run} pages or more:")
    for (i1, n1), (i2, n2), off, c in runs:
        if c >= a.min_run:
            out.append(f"  leaves {i1}-{i2}  pp. {n1}-{n2}  offset {off}  ({c} pages)")
    common = Counter(i - n for i, n in nums).most_common(1)[0][0]
    odd = [f"{i} (p. {n}, {i - n})" for i, n in nums if i - n != common and abs(i - n - common) < 20]
    out.append(f"off the commonest offset {common}: " + (", ".join(odd) or "none"))
    where = {}
    for i, lines in enumerate(leaves, 1):
        k = re.sub(r"\W", "", " ".join(lines[1:4]))[:80]
        if len(k) > 40:
            where.setdefault(k, []).append(i)
    reps = [v for v in where.values() if len(v) > 1]
    out.append("repeated leaves: " + (", ".join("-".join(map(str, v)) for v in reps) or "none"))
    print("\n".join(out))


def cmd_heads(a):
    for i, lines in enumerate(read_leaves(a.xml), 1):
        if a.first <= i <= a.last:
            first, last = (lines[0], lines[-1]) if lines else ("", "")
            print(f"{i} | {first[:60]} | {last[:40]}")


def words(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"-\s*\n\s*", "", t)
    return [w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{3,}", t)]


def cmd_diff(a):
    x, y = words(a.a), words(a.b)
    sm = difflib.SequenceMatcher(None, x, y, autojunk=False)
    n = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal" and max(i2 - i1, j2 - j1) >= a.min:
            n += 1
            print(f"[word {i1}]\n  - {' '.join(x[i1:i2])[:200]}\n  + {' '.join(y[j1:j2])[:200]}")
    print(f"{n} blocks of {a.min} words or more, in {len(x)} and {len(y)} words")


def cmd_pages(a):
    a.dir.mkdir(parents=True, exist_ok=True)
    i = 0
    for _, el in ET.iterparse(a.xml):
        if el.tag == "OBJECT":
            i += 1
            if a.first <= i <= (a.last or i):
                lines = [" ".join(w.text or "" for w in l.iter("WORD")) for l in el.iter("LINE")]
                (a.dir / f"{i + a.shift:0{a.width}d}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
            el.clear()
    print(f"{a.dir}: leaves {a.first}-{a.last or i} as {a.first + a.shift}-{(a.last or i) + a.shift}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fetch", help="download the OCR files of the scans")
    p.add_argument("ids", nargs="+", help="Internet Archive identifiers")
    p.add_argument("-d", "--dir", type=Path, required=True, help="directory for ID/ID_djvu.*")
    p.set_defaults(func=cmd_fetch)
    p = sub.add_parser("image", help="download leaf images, to compare the scans")
    p.add_argument("id", help="Internet Archive identifier")
    p.add_argument("leaves", nargs="+", type=int, help="leaf numbers (1-based, as in `leaves`)")
    p.add_argument("-d", "--dir", type=Path, required=True, help="output directory")
    p.set_defaults(func=cmd_image)
    p = sub.add_parser("leaves", help="page offsets and repeated leaves")
    p.add_argument("xml", type=Path, help="ID_djvu.xml")
    p.add_argument("--min-run", type=int, default=3, help="least run shown (3)")
    p.set_defaults(func=cmd_leaves)
    p = sub.add_parser("heads", help="first and last lines of some leaves")
    p.add_argument("xml", type=Path, help="ID_djvu.xml")
    p.add_argument("first", type=int)
    p.add_argument("last", type=int)
    p.set_defaults(func=cmd_heads)
    p = sub.add_parser("diff", help="revisions between two printings")
    p.add_argument("a", type=Path, help="ID_djvu.txt of the earlier printing")
    p.add_argument("b", type=Path, help="ID_djvu.txt of the later printing")
    p.add_argument("--min", type=int, default=5, help="least words in a block (5)")
    p.set_defaults(func=cmd_diff)
    p = sub.add_parser("pages", help="the OCR as page files, for cmpread.py -i")
    p.add_argument("xml", type=Path, help="ID_djvu.xml")
    p.add_argument("-d", "--dir", type=Path, required=True, help="output directory")
    p.add_argument("--first", type=int, default=1, help="first leaf (1)")
    p.add_argument("--last", type=int, default=0, help="last leaf (default: all)")
    p.add_argument("--shift", type=int, default=0, help="page file = leaf + SHIFT (0)")
    p.add_argument("--width", type=int, default=3, help="digits of the page file (3)")
    p.set_defaults(func=cmd_pages)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
