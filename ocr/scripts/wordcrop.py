"""Crops bands of a page image around words, for deciding a flagged place in the image.

Each SPEC is `PAGE:TEXT[:N]`: the Nth word (default 1) of Tesseract's word list
`TESS/PAGE.tsv` whose text contains TEXT (without case). A band of `DIR/PAGE.png` around
the word, with the lines just above and below it, is written under a yellow label giving
the spec and how many words matched; a spec that matches no word gets the label only. The
bands are stacked into one PNG.

    uv run ocr/scripts/wordcrop.py ocr/la out.png 0301:morderet 0316:altos:2
"""
import argparse
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# A font with Greek for the labels, if one is installed; PIL's default font has none.
try:
    FONT = ImageFont.truetype("NotoSans-Regular.ttf", 13)
except OSError:
    FONT = ImageFont.load_default()

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
ap.add_argument("dir", type=Path, help="directory of the page images (e.g. ocr/la)")
ap.add_argument("output", type=Path, help="output PNG")
ap.add_argument("specs", nargs="+", metavar="SPEC", help="PAGE:TEXT[:N]")
ap.add_argument("-t", "--tess", type=Path,
                help="directory of Tesseract's word lists (default: DIR/tesseract)")
ap.add_argument("--side", type=int, default=650, help="pixels left and right of the word (650)")
ap.add_argument("--above", type=int, default=40, help="pixels above the word (40)")
ap.add_argument("--below", type=int, default=75, help="pixels below the word (75)")
a = ap.parse_args()
tess = a.tess or a.dir / "tesseract"

parts = []
for spec in a.specs:
    f = spec.split(":")
    if len(f) not in (2, 3) or not f[1]:
        ap.error(f"bad spec: {spec} (PAGE:TEXT[:N])")
    page, text, n = f[0], f[1].lower(), int(f[2]) if len(f) == 3 else 1
    with open(tess / f"{page}.tsv", newline="") as fp:
        rows = csv.DictReader(fp, delimiter="\t", quoting=csv.QUOTE_NONE)
        hits = [r for r in rows if text in (r["text"] or "").lower()]
    label = Image.new("RGB", (1500, 22), "yellow")
    ImageDraw.Draw(label).text((4, 3), f"{spec} ({len(hits)} hits)", fill="black", font=FONT)
    parts.append(label)
    if len(hits) >= n:
        r = hits[n - 1]
        x, y, w, h = (int(r[k]) for k in ("left", "top", "width", "height"))
        im = Image.open(a.dir / f"{page}.png")
        parts.append(im.crop((max(0, x - a.side), max(0, y - a.above),
                              x + w + a.side, y + h + a.below)).convert("RGB"))

out = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts)), "white")
y = 0
for p in parts:
    out.paste(p, (0, y))
    y += p.height
out.save(a.output)
