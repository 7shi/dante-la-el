"""Cut the maps, diagrams and plates of ocr/en-oelsner from the scans into
texts/en-oelsner/images/NNN.jpg (NNN the scan). The captions and names stay as text
in the Markdown; the images show the figures only. The grey paper is made white: the
levels are stretched from the darkest ink to a little below the paper (the 75th
percentile: the paper is most of a figure, the fill of 284 too much for the median), so
that the show-through from the other side fades too.

    uv run texts/scripts/crop_en_oelsner_images.py [-o texts/en-oelsner/images]
"""
import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "ocr" / "en-oelsner"

# scan: (left, top, right, bottom) in the scan's pixels, the figure without its caption
BOXES = {
    25: (0, 150, 635, 998),    # Dante's geographical description (two maps)
    37: (20, 255, 690, 850),   # section of the Earth: Hell and Purgatory
    133: (5, 200, 705, 880),   # the hours at which the signs of the Zodiac rise
    191: (20, 240, 690, 890),  # the rivers of Romagna
    284: (140, 440, 745, 860), # Scartazzini's diagram (note on XXIV 34-40)
    409: (10, 335, 640, 815),  # plan of concentric spheres
    410: (155, 25, 787, 1140), # section of the Universe
}


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
    ap.add_argument("-o", "--outdir", default=str(ROOT / "texts" / "en-oelsner" / "images"))
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    for n, box in BOXES.items():
        im = whiten(Image.open(SRC / f"{n:03d}.png").convert("L").crop(box))
        path = out / f"{n:03d}.jpg"
        im.save(path, quality=QUALITY, optimize=True)
        print(f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {im.width}x{im.height}")


if __name__ == "__main__":
    main()
