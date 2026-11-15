"""Cut the maps, diagrams and plates of a Temple Classics volume edited by Oelsner from
the scans: ocr/en-oelsner into texts/en-oelsner/images/NNN.jpg (NNN the scan), or
ocr/en-purgatorio into texts/en-purgatorio/images/NNN.jpg.

The Inferno's figures are taken from the Fifth
Edition (1904), which prints them without show-through: 411 and 412 are its pages in
ocr/en-oelsner itself, the others its pages in ocr/en-oelsner/fifth/. The captions and names stay as text
in the Markdown; the images show the figures only. The grey paper is made white: the
levels are stretched from the darkest ink to a little below the paper (the 75th
percentile: the paper is most of a figure, the fill of 284 too much for the median), so
that the show-through from the other side fades too. The Purgatorio's are cut from its own
scan (the Fourth Edition, 1904), in the same way.

    uv run texts/scripts/crop_en_oelsner_images.py [inferno|purgatorio] [-o OUTDIR]
"""
import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

# scan: (left, top, right, bottom) in the scan's pixels, the figure without its caption
INFERNO = {
    25: (60, 240, 1192, 1757),    # Dante's geographical description (two maps)
    37: (33, 454, 1206, 1518),    # section of the Earth: Hell and Purgatory
    133: (37, 356, 1279, 1581),  # the hours at which the signs of the Zodiac rise
    191: (59, 404, 1186, 1537),   # the rivers of Romagna
    284: (278, 820, 1295, 1561),  # Scartazzini's diagram (note on XXIV 34-40)
    411: (110, 33, 1239, 965),    # plan of concentric spheres (Fig. I)
    412: (370, 293, 1232, 2261),  # section of the eight heavens (Fig. II)
}

# The Purgatorio: the diagrams with their labels, without the captions printed below.
PURGATORIO = {
    24: (190, 695, 1020, 1556),   # the course of the Poets round the mountain
    25: (30, 790, 985, 1462),     # light and shade at 6 a.m.
    46: (335, 832, 840, 1338),    # the clock of simultaneous hours
    47: (60, 960, 885, 1478),     # the longitudes
    59: (120, 578, 1020, 1556),   # light and shade at noonday
    71: (35, 383, 845, 1135),     # the hours at which the signs of the Zodiac rise
    115: (30, 716, 940, 1405),    # light and shade at 6 p.m.
    388: (40, 15, 1010, 1698),    # map of Upper and Central Italy, west
    389: (30, 15, 975, 1694),     # the same, east
}

VOLUMES = {"inferno": (INFERNO, "en-oelsner"), "purgatorio": (PURGATORIO, "en-purgatorio")}


def source(n, src):
    fifth = src / "fifth" / f"{n:03d}.png"
    return fifth if fifth.exists() else src / f"{n:03d}.png"


WHITE_MARGIN = 14  # below the paper's level, still made white
QUALITY = 85


def percentile(im, q):
    hist, total, count = im.histogram(), im.width * im.height, 0
    for v, k in enumerate(hist):
        count += k
        if count >= total * q / 100:
            return v
    return 255


def whiten(im):
    black = percentile(im, 1)
    white = percentile(im, 75) - WHITE_MARGIN
    scale = 255 / max(white - black, 1)
    return im.point(lambda v: max(0, min(255, round((v - black) * scale))))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("volume", nargs="?", default="inferno", choices=VOLUMES)
    ap.add_argument("-o", "--outdir", help="default: texts/DIR/images")
    args = ap.parse_args()
    boxes, name = VOLUMES[args.volume]
    src = ROOT / "ocr" / name
    out = Path(args.outdir or ROOT / "texts" / name / "images")
    out.mkdir(parents=True, exist_ok=True)
    for n, box in boxes.items():
        im = whiten(Image.open(source(n, src)).convert("L").crop(box))
        path = out / f"{n:03d}.jpg"
        im.save(path, quality=QUALITY, optimize=True)
        print(f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {im.width}x{im.height}")


if __name__ == "__main__":
    main()
