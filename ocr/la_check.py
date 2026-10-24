"""Structure checks of ocr/la pages: tercet numbers, and section rules against blank lines.

    la_check.py FIRST LAST [-d DIR]... [-v] [-o OUT]

-d reads the page files from DIR (repeatable, the first that has the page; default ocr/la),
such as a work directory's out/ before it is written; the images stay in ocr/la.

- tercets: in the Italian (first) and Latin (second) verse block of each page, a number
  must start every third verse line (runover lines `[…` do not count), the numbers must rise
  by one and continue from the previous page (reset at a page with `CAPITUL…`).
- rules: the short centred rules printed in the commentary (both columns, found in
  ocr/la/PAGE.png) are counted against the blank lines after the verse block; a page where
  the counts differ is listed. The image count often misses rules of the right column and
  rules at a page end, so a listed page is to be looked at, not corrected blindly.
  -v lists every page with the y positions of the rules."""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent / "la"
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
TERCET = re.compile(r"^([0-9]+\.?|[⁰¹²³⁴⁵⁶⁷⁸⁹]+) +(?=\S)")
RULE_NUM = re.compile(r"^(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\d{1,2})\s")
DIRS = [ROOT]


def txt(page):
    """The page file from the first of DIRS that has it, or None."""
    return next((Path(d, f"{page}.txt") for d in DIRS if Path(d, f"{page}.txt").exists()), None)


# ---- tercet numbers ----

def check_tercets(first, last):
    out, prev = [], {}
    for p in range(first, last + 1):
        f = txt(f"{p:04}")
        if f is None: continue
        text = f.read_text(encoding="utf-8")
        if re.search(r"^CAPITUL", text, re.M) and re.search(r"^(¹|1\.?) ", text, re.M): prev = {}
        paras = [b.split("\n") for b in re.split(r"\n\s*\n", text)]
        verse = [b for b in paras if sum(1 for l in b if TERCET.match(l)) >= 1 and len(b) >= 2
                 and sum(len(l) for l in b) / len(b) < 75 and not b[0].startswith("(")]
        for k, b in enumerate(verse[:2]):
            lang = "both" if "\t" in "".join(b) else "it" if k == 0 else "la"
            lines = [l for l in b if not (l.startswith("[") and "]" not in l)]
            nums = [(i, int(TERCET.match(l)[1].translate(SUP).rstrip("."))) for i, l in enumerate(lines) if TERCET.match(l)]
            if not nums: continue
            off = nums[0][0] % 3
            for i, n in nums:
                if i % 3 != off: out.append(f"{p:04} {lang}: number {n} at verse line {i + 1} (expected every 3rd)")
            for (i, a), (j, b2) in zip(nums, nums[1:]):
                if b2 != a + 1: out.append(f"{p:04} {lang}: {a} then {b2}")
                if j - i != 3: out.append(f"{p:04} {lang}: {j - i} lines between {a} and {b2}")
            if lang in prev and nums[0][0] == 0 and nums[0][1] != prev[lang] + 1:
                out.append(f"{p:04} {lang}: starts at {nums[0][1]}, previous page ended at {prev[lang]}")
            if nums[0][0] > 0 and lang in prev and nums[0][1] not in (prev[lang] + 1, prev[lang] + 2):
                out.append(f"{p:04} {lang}: starts at {nums[0][1]} after {nums[0][0]} lines, previous {prev[lang]}")
            prev[lang] = nums[-1][1]
    return out


# ---- section rules against blank lines ----

def columns(im):
    w, h = im.size; px = im.load()
    ink = [sum(1 for y in range(0, h, 3) if px[x, y] < 128) for x in range(w)]
    top = max(ink); xs = [x for x in range(w) if ink[x] > top * 0.15]
    x0, x1 = max(0, xs[0] - 10), min(w, xs[-1] + 10); mid = (x0 + x1) // 2
    g = min(range(mid - (x1 - x0) // 8, mid + (x1 - x0) // 8), key=lambda x: ink[x])
    return (x0, g - 35), (g + 35, x1)


def rules(im, a, b):
    """y of short centred horizontal rules between a and b; long rules (block separators)
    reset the list."""
    w, h = im.size; px = im.load()
    # narrow the column to its text (margin specks and the facing page's bleed are outside):
    # the widest run of inked x, gaps under 30 px joined
    ink = [sum(1 for y in range(0, h, 4) if px[x, y] < 128) for x in range(a, b)]
    on = [v > 4 for v in ink]; runs, x = [], 0
    while x < len(on):
        if not on[x]: x += 1; continue
        x1 = x
        while x1 < len(on) and (on[x1] or any(on[x1:x1 + 30])): x1 += 1
        runs.append((x, x1)); x = x1
    if not runs: return []
    s0, s1 = max(runs, key=lambda r: r[1] - r[0])
    a, b = a + s0, a + s1; c = (a + b) // 2
    rows = []
    for y in range(h):
        xs = [x for x in range(a, b) if px[x, y] < 140]
        rows.append((min(xs), max(xs), len(xs)) if xs else None)
    found, y = [], 0
    while y < h:
        if rows[y] is None: y += 1; continue
        y1 = y
        while y1 < h and rows[y1] is not None: y1 += 1
        band = [rows[k] for k in range(y, y1)]
        lo = min(r[0] for r in band); hi = max(r[1] for r in band)
        solid = max(r[2] / (r[1] - r[0] + 1) for r in band)
        if y1 - y <= 8 and solid > 0.8:
            if 30 <= hi - lo <= 160 and abs((lo + hi) / 2 - c) < 80: found.append(y)
            elif hi - lo > (b - a) * 0.6 and y < h * 0.85: found = []  # verse/commentary separator
        y = y1
    return found


def blanks(page):
    """Blank lines after the verse block, less those around a quoted line (a block of one or
    two lines after a line ending in `:`), which are not rules."""
    L = txt(page).read_text(encoding="utf-8").rstrip("\n").split("\n")
    nums = [i for i, l in enumerate(L) if RULE_NUM.match(l)]
    start = 0
    if nums:
        start = nums[-1]
        while start < len(L) and L[start] != "": start += 1
    body = L[start + 1:]; n = sum(1 for l in body if l == "")
    blocks, cur = [], []
    for l in body + [""]:
        if l == "":
            if cur: blocks.append(cur)
            cur = []
        else: cur.append(l)
    for prev, b in zip(blocks, blocks[1:]):
        if len(b) <= 2 and prev[-1].rstrip().endswith(":"): n -= 2
    return n


def check_rules(first, last, verbose):
    out = []
    for p in range(first, last + 1):
        page = f"{p:04}"
        if not (ROOT / f"{page}.png").exists() or txt(page) is None: continue
        im = Image.open(ROOT / f"{page}.png").convert("L")
        (la, lb), (ra, rb) = columns(im)
        rl, rr = rules(im, la, lb), rules(im, ra, rb)
        nb = blanks(page)
        if verbose or len(rl) + len(rr) != nb:
            out.append(f"{page}: rules {len(rl)}+{len(rr)}, blank lines {nb}" + (f"  L{rl} R{rr}" if verbose else ""))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-d", "--dir", action="append",
                    help="page files; repeatable, the first that has the page is read (default ocr/la)")
    ap.add_argument("-v", "--verbose", action="store_true", help="list every page with the rule positions")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    a = ap.parse_args()
    if a.dir: DIRS[:] = a.dir
    out = ["# tercets"] + check_tercets(a.first, a.last) + ["", "# rules"] + check_rules(a.first, a.last, a.verbose)
    text = "\n".join(out) + "\n"
    if a.output: Path(a.output).write_text(text, encoding="utf-8")
    else: sys.stdout.write(text)


if __name__ == "__main__":
    main()
