"""Crop the verse column missing from an ocr/la page, for its transcription from the image.

    la_versecrop.py PAGE... -t TESS -o OUTDIR

A canto page prints the verse at the top in two columns, the Italian on the left and the
Latin on the right. For a page whose file has only one of them (la_survey.py: Italian or
Latin missing), the verse block of the file is found (la_survey.verse_block), its lines are
looked up in Tesseract's word boxes (TESS/PAGE.tsv) to give the height of the printed verse,
and the other column at that height, up to the blank band between the columns (with a
margin of 15 pixels, and for the Italian on up to the end of its longest words, since the
columns can overlap), is cropped at the scan's own resolution: OUTDIR/PAGE.png. The edge of
the other column can come in (tercet numbers, first letters). The lines of the file are matched word by word, not copied anywhere.

OUTDIR/crops.tsv lists for each page: the missing column (it, la), the box (x0 y0 x1 y1), the
verse lines of the file, how many of them were found in Tesseract's words, the printed lines
Tesseract has in the box, and a status: ok, or what to look at (few lines found, line
counts differ, no verse block)."""

import argparse
import collections
import re
import statistics
import sys
from pathlib import Path

from PIL import Image
from rapidfuzz import fuzz

import la_survey as S

ROOT = S.ROOT


def tess_words(path):
    """Tesseract's words: normalized text, box, and the id of its printed line."""
    out = []
    for row in path.read_text(encoding="utf-8").splitlines()[1:]:
        f = row.split("\t")
        if len(f) < 12 or f[0] != "5" or not f[11].strip(): continue
        x, y, w, h = map(int, f[6:10])
        out.append(dict(n=S.norm(f[11]), box=(x, y, x + w, y + h), line=tuple(map(int, f[1:5]))))
    return out


def verse_lines(p):
    """The verse lines of the file's block: no gloss lines, runover words or heads."""
    lines = (ROOT / f"{p}.txt").read_text(encoding="utf-8").splitlines()
    return [lines[i] for i in S.verse_block(lines) if S.keep(lines[i])]


def find_line(line, words, used):
    """The Tesseract words of one file line: its long words matched one by one, kept where
    they lie on one printed line (the most common line id among the matches)."""
    want = [S.norm(w) for w in S.NUM.sub("", line).split()]
    want = [w for w in want if len(w) >= 4]
    hits = []
    for w in want:
        # the verse stands above the commentary, whose lemmas repeat its words: the
        # highest good match
        good = [k for k, t in enumerate(words)
                if k not in used and len(t["n"]) >= 3 and fuzz.ratio(w, t["n"]) >= 70]
        if good: hits.append(min(good, key=lambda k: words[k]["box"][1]))
    if not hits: return []
    ids = collections.Counter(words[k]["line"] for k in hits)
    lid, n = ids.most_common(1)[0]
    return [k for k in hits if words[k]["line"] == lid] if n >= max(1, len(want) // 3) else []


def gutter(im, left, right, y0, y1):
    """The x of the blank band between the two verse columns, in the middle of the text
    width: the least ink over the verse height, summed over 15 pixel columns (the band is
    narrow, about 30 pixels, and holds specks and the tercet numbers' edges)."""
    g = im.convert("L").crop((left, y0, right, y1))
    w, h = g.size
    px = g.load()
    ink = [sum(px[x, y] < 128 for y in range(0, h, 2)) for x in range(w)]
    win = [sum(ink[x - 7:x + 8]) for x in range(int(0.3 * w), int(0.75 * w))]
    k = min(range(len(win)), key=win.__getitem__)
    return left + int(0.3 * w) + k


def crop_page(p, tessdir, outdir):
    verse = verse_lines(p)
    if not verse: return [p, "", "", len(verse), 0, 0, "no verse block"]
    missing = "it" if statistics.mean(S.latin_score(l) for l in verse) > 0 else "la"
    words = tess_words(tessdir / f"{p}.tsv")
    if not words: return [p, missing, "", len(verse), 0, 0, "no Tesseract words"]
    im = Image.open(ROOT / f"{p}.png")
    W, H = im.size
    xs0 = sorted(t["box"][0] for t in words); xs1 = sorted(t["box"][2] for t in words)
    left, right = xs0[len(xs0) // 50], xs1[-len(xs1) // 50 - 1]  # text area, outliers off
    lh = statistics.median(t["box"][3] - t["box"][1] for t in words)
    used, found = set(), []
    for l in verse:
        ks = find_line(l, words, used)
        used.update(ks)
        if ks: found.append([words[k]["box"] for k in ks])
    # the verse stands at the top: keep the run of found lines from the highest one down,
    # cut at the first wide gap (the lemmas of the commentary repeat verse words)
    found.sort(key=lambda bs: min(b[1] for b in bs))
    tops = [min(b[1] for b in bs) for bs in found]
    pitch = statistics.median([b - a for a, b in zip(tops, tops[1:]) if b > a + lh] or [2 * lh])
    run = found[:1]
    for bs in found[1:]:  # a line or two not found leave a gap of two or three lines
        if min(b[1] for b in bs) - min(b[1] for b in run[-1]) > 3.5 * pitch: break
        run.append(bs)
    if len(run) < max(2, len(verse) // 2):
        return [p, missing, "", len(verse), len(run), 0, "few lines found"]
    y0 = max(0, int(min(b[1] for bs in run for b in bs) - 1.5 * lh))
    y1 = min(H, int(max(b[3] for bs in run for b in bs) + 2.5 * lh))  # a runover word below
    g = gutter(im, left, right, min(b[1] for bs in run for b in bs),
               max(b[3] for bs in run for b in bs))  # not the head above nor the glosses below
    # a margin: a long line or a gloss mark can reach into the band
    x0, x1 = (max(0, left - 60), g + 15) if missing == "it" else (g - 15, min(W, right + 60))
    if missing == "it":
        # the columns overlap: a long Italian line can reach past the band, beside the
        # tercet number of another Latin line (0625): take in the words that start left of
        # the band (not those Tesseract joins across it)
        ends = [t["box"][2] for t in words if y0 <= t["box"][1] <= y1
                and t["box"][0] < g - 10 and t["box"][2] < g + 80]
        x1 = min(W, max([x1] + [e + 5 for e in ends]))
    crop = im.crop((x0, y0, x1, y1))
    crop.save(outdir / f"{p}.png")
    inside = {t["line"] for t in words
              if x0 <= (t["box"][0] + t["box"][2]) / 2 <= x1 and y0 + lh / 2 <= t["box"][1] <= y1 - lh
              and len(t["n"]) >= 3}
    status = "ok" if abs(len(inside) - len(verse)) <= 1 else "line counts differ"
    if len(run) < len(verse) - 2: status = "few lines found" if status == "ok" else status
    return [p, missing, f"{x0} {y0} {x1} {y1}", len(verse), len(run), len(inside), status]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pages", nargs="+", help="page numbers, e.g. 0237 0238")
    ap.add_argument("-t", "--tessdir", type=Path, required=True, help="Tesseract's PAGE.tsv files")
    ap.add_argument("-o", "--outdir", type=Path, required=True, help="crops and crops.tsv")
    a = ap.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    rows = [["page", "missing", "box", "verse", "found", "tess", "status"]]
    for p in a.pages:
        rows.append(crop_page(p, a.tessdir, a.outdir))
        print("\t".join(map(str, rows[-1])), file=sys.stderr)
    (a.outdir / "crops.tsv").write_text("\n".join("\t".join(map(str, r)) for r in rows) + "\n",
                                       encoding="utf-8")
    print(collections.Counter(r[-1] for r in rows[1:]), file=sys.stderr)


if __name__ == "__main__":
    main()
