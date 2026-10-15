"""Insert a transcribed Italian verse column into ocr/la pages that lack it.

    la_verseinsert.py PAGE... -d DIR [-n]

DIR/PAGE.txt is the Italian verse of the page, checked (tercet numbers as superscripts,
runover lines `[…`). It is inserted before the first line of the page's Latin verse block
(la_survey.verse_block), followed by a blank line, with a blank line before it where the
running head stands right above the verse. In the Latin block, the tercet numbers become
superscripts (`27`, `^27` → `²⁷`), and each counted line (no runover, gloss or head line)
gets the number of the Italian line at the same place: a number added or changed is
listed, to be checked in the image (the Latin numbers of these pages are unchecked OCR).
A page whose Latin block has another number of lines than the Italian is listed and left
as it is. -n lists without writing."""

import argparse
import re
import sys
from pathlib import Path

import la_survey as S

ROOT = S.ROOT
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
UNSUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
ITNUM = re.compile(r"^([⁰¹²³⁴⁵⁶⁷⁸⁹]+) ")
LANUM = re.compile(r"^\^?([⁰¹²³⁴⁵⁶⁷⁸⁹]{1,3}|\d{1,3})\.? +(?=\S)")


def counted(l):
    t = l.strip()
    runover = re.match(r"\[[a-zà-ù]", t)  # 0447 `[Et veniet …]`: a whole line supplied
    return (S.keep(l) and not S.is_head(l) and not runover and t.upper() != t
            and not re.fullmatch(r"\(\W*\)", t))  # 0309 `(...)`


def insert(p, src):
    lines = (ROOT / f"{p}.txt").read_text(encoding="utf-8").splitlines()
    it = src.read_text(encoding="utf-8").splitlines()
    block = S.verse_block(lines)
    la = [i for i in block if counted(lines[i])]
    nums = [m[1].translate(UNSUP) if (m := ITNUM.match(l)) else None
            for l in it if not l.startswith("[")]
    if not la: return None, [f"{p}: no Latin verse block"]
    if len(la) != len(nums):
        return None, [f"{p}: Latin {len(la)} lines, Italian {len(nums)}: left as it is"]
    notes = []
    for i, n in zip(la, nums):
        l = lines[i]
        m = LANUM.match(l)
        old = m[1].translate(UNSUP) if m else None
        body = l[m.end():] if m else l
        lines[i] = f"{n.translate(SUP)} {body}" if n else body
        if old != n: notes.append(f"{p}: Latin number {old or '-'} -> {n or '-'}: {body[:50]}")
    first = la[0]
    pre = [""] if first > 0 and lines[first - 1].strip() else []
    lines[first:first] = pre + it + [""]
    return lines, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pages", nargs="+", help="page numbers, e.g. 0237 0238")
    ap.add_argument("-d", "--dir", type=Path, required=True, help="the checked PAGE.txt files")
    ap.add_argument("-n", "--dry-run", action="store_true", help="list, do not write")
    a = ap.parse_args()
    for p in a.pages:
        p = f"{int(p):04d}"
        lines, notes = insert(p, a.dir / f"{p}.txt")
        for n in notes: print(n)
        if lines is not None and not a.dry_run:
            (ROOT / f"{p}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
