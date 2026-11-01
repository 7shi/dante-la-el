"""Verse check of ocr/la/PLAN.md: the Latin verse read again from the image.

    la_versecheck.py FIRST LAST --crops DIR [--italian] [--seed N] [--min-likeness X]
    la_versecheck.py FIRST LAST --readings DIR [--italian] [-o OUT]

The Latin verse of a canto page (the second verse block, as la_lemmacheck.py finds it;
gloss lines left out) has had one reading only. --crops writes an image of each of its
lines to DIR, in a shuffled order, for a reader who transcribes them from the image alone
(DIR/lines.tsv maps them back; a line that Tesseract cannot locate, such as a runover word,
goes to DIR/unlocated.tsv, to be read in the page image). This is check 1's procedure
(la_lemmacheck.py --crops), over every line of the Latin verse.

--readings compares the reader's DIR/readings.tsv (`L0001<TAB>line as printed`) with
ocr/la, line by line: every line whose words differ (letters, accents and the tercet
number; not the punctuation) is listed with both forms and the differing words; lines with
no reading are counted.

--italian does the same for the Italian verse (the first verse block) instead."""

import argparse
import random
import re
import sys
from pathlib import Path

import la_lemmacheck as L

NUMBER = re.compile(r"^\[?(\d+) ")


def verse_lines(first, last, italian=False):
    """[(page, line)] of the Latin (or Italian) verse of the canto pages in FIRST..LAST."""
    pages = sorted(p for cantos in L.CANTOS.values() for start, essay, _ in cantos
                   for p in range(start, essay) if first <= p <= last)
    out = []
    for p in pages:
        if not (L.ROOT / f"{p:04d}.txt").exists():
            continue
        it, la, _ = L.page_parts(p)
        out.extend((p, i) for i, _ in (it if italian else la))
    return out


def write_crops(keys, d, seed, min_likeness):
    """As la_lemmacheck.write_crops, for the given lines."""
    from PIL import Image
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    keys = list(keys)
    random.Random(seed).shuffle(keys)
    rows, left_out = [], []
    for p, l in keys:
        (x0, y0, x1, y1), ratio = L.locate(p, l)
        if ratio < min_likeness:
            left_out.append(f"{p:04d}\t{l}\t{ratio:.2f}\t{L.text_line(p, l)}")
            continue
        im = Image.open(L.ROOT / f"{p:04d}.png")
        left = 70 if NUMBER.match(L.text_line(p, l)) else 30
        c = im.crop((max(0, x0 - left), max(0, y0 - 12), min(im.width, x1 + 30), min(im.height, y1 + 12)))
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        name = f"L{len(rows) + 1:04d}"
        c.save(d / f"{name}.png")
        rows.append(f"{name}\t{p:04d}\t{l}\t{ratio:.2f}")
    (d / "lines.tsv").write_text("id\tpage\tline\tlikeness\n" + "\n".join(rows) + "\n", encoding="utf-8")
    (d / "unlocated.tsv").write_text("page\tline\tlikeness\ttext\n" + "".join(r + "\n" for r in sorted(left_out)),
                                     encoding="utf-8")
    return len(rows), len(left_out)


def number(t):
    m = NUMBER.match(t)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("--crops", metavar="DIR", help="write the line images to read")
    ap.add_argument("--readings", metavar="DIR", help="compare a reader's DIR/readings.tsv")
    ap.add_argument("--italian", action="store_true", help="the Italian verse, not the Latin")
    ap.add_argument("--seed", type=int, default=1, help="the shuffle of --crops")
    ap.add_argument("--min-likeness", type=float, default=0.8, help="of a line image (--crops)")
    a = ap.parse_args()
    keys = verse_lines(a.first, a.last, a.italian)
    if a.crops:
        n, left_out = write_crops(keys, a.crops, a.seed, a.min_likeness)
        print(f"{len(keys)} verse lines: {n} images, {left_out} unlocated", file=sys.stderr)
    if not a.readings:
        return
    readings = L.read_readings(a.readings)
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    unread = differ = 0
    for p, l in keys:
        theirs = readings.get((p, l))
        if theirs is None:
            unread += 1
            continue
        ours = L.text_line(p, l)
        d = L.word_diff(ours, theirs)
        if number(ours) != number(theirs):
            d.insert(0, f"#{number(ours)}>#{number(theirs)}")
        if d:
            differ += 1
            print(f"{p:04d}:{l}\t{'; '.join(d)}\n  o> {ours}\n  r> {theirs}", file=out)
    print(f"{len(keys)} verse lines, {len(keys) - unread} read, {differ} differ, {unread} not read",
          file=sys.stderr)


if __name__ == "__main__":
    main()
