"""Cut the maps, diagrams and plates of a Temple Classics volume edited by Oelsner from
the scans: ocr/en-oelsner into texts/en-oelsner/images/NNN.jpg (NNN the scan),
ocr/en-purgatorio into texts/en-purgatorio/images/NNN.jpg, or ocr/en-paradiso into
texts/en-paradiso/images/NNN.jpg.

The Inferno's figures are taken from the Fifth
Edition (1904), which prints them without show-through: 411 and 412 are its pages in
ocr/en-oelsner itself, the others its pages in ocr/en-oelsner/fifth/. The captions and names stay as text
in the Markdown; the images show the figures only. The grey paper is made white: the
levels are stretched from the darkest ink to a little below the paper (the 75th
percentile: the paper is most of a figure, the fill of 284 too much for the median), so
that the show-through from the other side fades too. The Purgatorio's are cut from its own
scan (the Fourth Edition, 1904), in the same way.

    uv run texts/scripts/crop_en_oelsner_images.py [inferno|purgatorio|paradiso] [-o OUTDIR]
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

# The Paradiso: the maps and diagrams, cut from its own scan (the reprint of November
# 1910), with their labels, without the captions and the map numbers (I, II) printed
# with them; the boxes from the ink of each page, specks left out (ocr/en-paradiso, step 6).
PARADISO = {
    22: (205, 462, 1200, 1290),   # the four circles and three crosses (between two notes)
    69: (425, 830, 765, 1455),    # the three mirrors
    98: (380, 1042, 1005, 1662),  # Provence
    99: (240, 1027, 900, 1648),   # Naples and Sicily
    110: (235, 785, 1157, 2006),  # Hungary, Rascia, etc.
    111: (30, 1446, 1110, 2023),  # the Mediterranean (Marseilles)
    125: (52, 217, 1062, 1908),   # the district about Romano, with an inset (full page)
    151: (88, 694, 1025, 1808),   # Assisi
    201: (0, 98, 1226, 1886),     # the district about Florence (full page; to the edge)
    217: (62, 112, 1132, 1874),   # Cacciaguida's Florence (full page)
    406: (318, 1048, 1135, 1862), # the world west of Jerusalem (II)
    407: (125, 1035, 938, 1852),  # the world east of Jerusalem (I)
}

VOLUMES = {"inferno": (INFERNO, "en-oelsner"), "purgatorio": (PURGATORIO, "en-purgatorio"),
           "paradiso": (PARADISO, "en-paradiso")}


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
