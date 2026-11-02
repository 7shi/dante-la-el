"""Verse check of ocr/la/PLAN.md: the Latin verse read again from the image.

    la_versecheck.py FIRST LAST --crops DIR [--italian] [--seed N] [--min-likeness X]
    la_versecheck.py FIRST LAST --readings DIR [--italian] [-o OUT]
    la_versecheck.py FIRST LAST --page-crops DIR [--italian]
    la_versecheck.py FIRST LAST --page-readings DIR [--italian] [-o OUT]

The Latin verse of a canto page (the second verse block, as la_lemmacheck.py finds it;
gloss lines left out) has had one reading only. --crops writes an image of each of its
lines to DIR, in a shuffled order, for a reader who transcribes them from the image alone
(DIR/lines.tsv maps them back; a line that Tesseract cannot locate, such as a runover word,
goes to DIR/unlocated.tsv, to be read in the page image). This is check 1's procedure
(la_lemmacheck.py --crops), over every line of the Latin verse.

--readings compares the reader's DIR/readings.tsv (`L0001<TAB>line as printed`) with
ocr/la, line by line: every line whose words differ (letters, accents and the tercet
number) is listed with both forms and the differing words; a line whose words agree but
whose punctuation differs is listed as `punctuation` (apostrophe spacing and a runover word
at the line end are not compared); lines with no reading are counted.

--page-crops writes one image per page instead: the verse block of the page (DIR/P0115.png
…), in page order, for a reader who writes its lines in order (`P0115<TAB>line`, one row per
printed line). --page-readings aligns them with the lines of ocr/la page by page and
compares them as --readings does; a reader's line with no match is listed as extra.

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


def write_page_crops(keys, d, min_likeness):
    """The verse block of each page: the box of its located lines, widened by a line
    height above and below for each unlocated line at its top or bottom."""
    from PIL import Image
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    pages = {}
    for p, l in keys:
        pages.setdefault(p, []).append(l)
    rows = []
    for p, ls in pages.items():
        found = [(l, *L.locate(p, l)) for l in ls]
        boxes = [b for _, b, r in found if r >= min_likeness]
        if not boxes:
            rows.append(f"P{p:04d}\t{len(ls)}\t0\t-")
            continue
        h = sorted(b[3] - b[1] for b in boxes)[len(boxes) // 2] * 1.6
        ok = [r >= min_likeness for _, _, r in found]
        above = ok.index(True)
        below = ok[::-1].index(True)
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        im = Image.open(L.ROOT / f"{p:04d}.png")
        c = im.crop((max(0, x0 - 30), max(0, int(y0 - 20 - above * h)),
                     min(im.width, x1 + 60), min(im.height, int(y1 + 20 + below * h))))
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        c.save(d / f"P{p:04d}.png")
        rows.append(f"P{p:04d}\t{len(ls)}\t{len(boxes)}\t{above + below}")
    (d / "pages.tsv").write_text("id\tlines\tlocated\tends unlocated\n" + "\n".join(rows) + "\n",
                                 encoding="utf-8")
    return len(pages)


def read_page_readings(d):
    """page -> the reader's lines in order, from DIR/readings.tsv (`P0115<TAB>text`)."""
    out = {}
    for l in open(Path(d, "readings.tsv"), encoding="utf-8"):
        if "\t" in l:
            k, t = l.rstrip("\n").split("\t", 1)
            k = k.strip()
            if k.startswith("P") and k[1:].isdigit():
                out.setdefault(int(k[1:]), []).append(t.strip())
    return out


def align(ours, theirs, gap=0.4):
    """Pairs (i, j) of an alignment of two lists of lines by the likeness of their letters;
    i or j is None for a line left unpaired."""
    import difflib
    a = ["".join(L.WORD.findall(t)).lower() for t in ours]
    b = ["".join(L.WORD.findall(t)).lower() for t in theirs]
    n, m = len(a), len(b)
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == j == 0:
                continue
            best = []
            if i and j:
                best.append(score[i - 1][j - 1] + difflib.SequenceMatcher(None, a[i - 1], b[j - 1]).ratio())
            if i:
                best.append(score[i - 1][j] + gap)
            if j:
                best.append(score[i][j - 1] + gap)
            score[i][j] = max(best)
    pairs, i, j = [], n, m
    while i or j:
        if i and j and score[i][j] == score[i - 1][j - 1] + difflib.SequenceMatcher(None, a[i - 1], b[j - 1]).ratio():
            pairs.append((i - 1, j - 1)); i -= 1; j -= 1
        elif i and score[i][j] == score[i - 1][j] + gap:
            pairs.append((i - 1, None)); i -= 1
        else:
            pairs.append((None, j - 1)); j -= 1
    return pairs[::-1]


def bare(t):
    """A line without its tercet number, runover word and apostrophe spacing."""
    t = re.sub(r"\s*['’]\s*", "'", t)
    t = re.sub(r"^\[?\d+ ", "", t)
    t = re.sub(r"\s*\[\w+[?.,;:!]*( \(\d+\))?$", "", t)
    return re.sub(r"\s+", " ", t).strip()


def marks(t):
    """The punctuation of a line, its words replaced by `w`."""
    return L.WORD.sub("w", bare(t))


def number(t):
    m = NUMBER.match(t)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("--crops", metavar="DIR", help="write the line images to read")
    ap.add_argument("--readings", metavar="DIR", help="compare a reader's DIR/readings.tsv")
    ap.add_argument("--page-crops", metavar="DIR", help="write one verse image per page")
    ap.add_argument("--page-readings", metavar="DIR", help="compare a reader's DIR/readings.tsv of page images")
    ap.add_argument("--italian", action="store_true", help="the Italian verse, not the Latin")
    ap.add_argument("--seed", type=int, default=1, help="the shuffle of --crops")
    ap.add_argument("--min-likeness", type=float, default=0.8, help="of a line image (--crops)")
    a = ap.parse_args()
    keys = verse_lines(a.first, a.last, a.italian)
    if a.crops:
        n, left_out = write_crops(keys, a.crops, a.seed, a.min_likeness)
        print(f"{len(keys)} verse lines: {n} images, {left_out} unlocated", file=sys.stderr)
    if a.page_crops:
        n = write_page_crops(keys, a.page_crops, a.min_likeness)
        print(f"{len(keys)} verse lines: {n} page images", file=sys.stderr)
    if a.page_readings:
        readings, extra = {}, []
        by_page = read_page_readings(a.page_readings)
        for p, theirs in sorted(by_page.items()):
            ls = [l for pp, l in keys if pp == p]
            for i, j in align([L.text_line(p, l) for l in ls], theirs):
                if i is None:
                    extra.append(f"P{p:04d}\t{theirs[j]}")
                elif j is not None:
                    readings[(p, ls[i])] = theirs[j]
    elif a.readings:
        readings, extra = L.read_readings(a.readings), []
    else:
        return
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    unread = differ = punct = 0
    for p, l in keys:
        theirs = readings.get((p, l))
        if theirs is None:
            unread += 1
            continue
        ours = L.text_line(p, l)
        d = L.word_diff(ours, theirs)
        if number(ours) != number(theirs):
            d.insert(0, f"#{number(ours)}>#{number(theirs)}")
        if not d and marks(ours) != marks(theirs):
            d = ["punctuation"]
            punct += 1
        elif d:
            differ += 1
        if d:
            print(f"{p:04d}:{l}\t{'; '.join(d)}\n  o> {ours}\n  r> {theirs}", file=out)
    for e in extra:
        print(f"extra\t{e}", file=out)
    print(f"{len(keys)} verse lines, {len(keys) - unread} read, {differ} differ in words, "
          f"{punct} in punctuation only, {unread} not read, {len(extra)} extra",
          file=sys.stderr)


if __name__ == "__main__":
    main()
