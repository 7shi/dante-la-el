"""Views for deciding marks and checks in the images (one stacked PNG per call).

    la_view.py review WORK PAGE:K[,PAGE:K...] -o OUT.png    review.tsv crops, labelled
    la_view.py context WORK [CLASS] [-o OUT]                review.tsv marks in their text
    la_view.py next WORK [N] -o OUT.png                     the next N marks not in mine.tsv
    la_view.py word TESS PAGE:REGEX[:N] ... [-z 2] -o OUT.png   around the Nth Tesseract word
    la_view.py strip PAGE:Y ... -o OUT.png                   full page width around height Y

`review` takes the keys of review.tsv (`page:k`); `context` prints each mark of review.tsv
(or of one class: comma, letters, punct, onesided) with the text around it, from
WORK/post/; `next` shows the crops and contexts of the next N marks (default 16) of
review.tsv that WORK/mine.tsv does not decide yet (decisions go in with la_mine.py); `word` finds a word in Tesseract's PAGE.tsv (TESS) and crops the lines around
it, enlarged by -z; `strip` is for the rule positions that la_lines.py and la_check.py -v
give."""

import argparse
import csv
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent / "la"
MARK = re.compile(r"\{\{(.*?)\|(.*?)\}\}", re.S)


def stack(parts, out):
    """parts: [(label, image)] stacked with a yellow label bar each."""
    if not parts: sys.exit("nothing to show")
    W = max(c.width for _, c in parts)
    im = Image.new("RGB", (W, sum(c.height + 22 for _, c in parts)), "white"); d = ImageDraw.Draw(im); y = 0
    for n, c in parts:
        d.rectangle((0, y, W, y + 20), fill="yellow"); d.text((3, y + 4), n, fill="black")
        im.paste(c.convert("RGB"), (0, y + 22)); y += c.height + 22
    im.save(out)


def review_rows(work):
    rows = list(csv.reader(open(Path(work, "review.tsv"), encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def crops(work, ds):
    parts = []
    for d in ds:
        if not d["crop"]: print(f"{d['page']}:{d['k']}", "no crop (not located): use `word`"); continue
        parts.append((f"{d['page']}:{d['line']} k{d['k']}  L={d['left']!r} R={d['right']!r}",
                      Image.open(Path(work, "crops", d["crop"]))))
    return parts


def cmd_review(a):
    rows = {f"{d['page']}:{d['k']}": d for d in review_rows(a.work)}; ds = []
    for k in a.keys.split(","):
        if k in rows: ds.append(rows[k])
        else: print(k, "not in review.tsv")
    stack(crops(a.work, ds), a.output)


def context(work, d, cache):
    """One mark of review.tsv with the text around it (cache: page -> text and marks)."""
    unm = lambda s: MARK.sub(r"\1", s)
    p, line = d["page"], int(d["line"])
    if p not in cache:
        t = Path(work, "post", f"{p}.txt").read_text(encoding="utf-8")
        cache[p] = (t, list(MARK.finditer(t)))
    t, ms = cache[p]
    left, right = d["left"].replace("⏎", "\n"), d["right"].replace("⏎", "\n")
    # the line of review.tsv is counted on the ocr/la sides (la_markup.mark_line)
    m = [m for m in ms if unm(t[:m.start()]).count("\n") + 1 == line and m.group(1) == left and m.group(2) == right]
    if not m: return f"{p}:{d['k']}\t{d['reason']}\t{d['model']}\t?? L={d['left']!r} R={d['right']!r}"
    m = m[0]
    s = unm(t[max(0, m.start() - 70):m.start()]) + "«" + m.group(1) + "|" + m.group(2) + "»" + unm(t[m.end():m.end() + 40])
    return f"{p}:{d['k']}\t{d['reason']}\t{d['model']}\t{d['tess']}\t" + s.replace("\n", "⏎")


def cmd_context(a):
    cache = {}
    out = [context(a.work, d, cache) for d in review_rows(a.work) if not a.cls or d["class"] == a.cls]
    text = "\n".join(out) + "\n"
    if a.output: Path(a.output).write_text(text, encoding="utf-8")
    else: sys.stdout.write(text)


def cmd_next(a):
    mine = Path(a.work, "mine.tsv"); done = set()
    if mine.exists():
        done = {(r[0], r[2]) for r in csv.reader(open(mine, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}
    ds = [d for d in review_rows(a.work) if (d["page"], d["k"]) not in done][:a.n]
    if not ds: print("every mark of review.tsv is in mine.tsv"); return
    cache = {}
    for d in ds: print(context(a.work, d, cache))
    parts = crops(a.work, ds)
    if parts: stack(parts, a.output)


def cmd_word(a):
    parts = []
    for it in a.items:
        p, rx, *n = it.split(":"); n = int(n[0]) if n else 1
        rows = [r for r in csv.DictReader(open(Path(a.tess, f"{p}.tsv"), encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)
                if re.search(rx, r["text"] or "")]
        if len(rows) < n: print(it, f"{len(rows)} hits"); continue
        r = rows[n - 1]; x, y, w, h = (int(r[k]) for k in ("left", "top", "width", "height"))
        im = Image.open(ROOT / f"{p}.png")
        c = im.crop((max(0, x - a.width), max(0, y - 70), min(im.width, x + w + a.width), min(im.height, y + h + 70)))
        if a.zoom != 1: c = c.resize((int(c.width * a.zoom), int(c.height * a.zoom)), Image.LANCZOS)
        print(it, f"{len(rows)} hits, shown: {r['text']}")
        parts.append((it, c))
    stack(parts, a.output)


def cmd_strip(a):
    parts = []
    for it in a.items:
        p, y = it.split(":"); y = int(y); im = Image.open(ROOT / f"{p}.png").convert("L")
        top = max(0, y - 110); c = im.crop((0, top, im.width, min(im.height, y + 70)))
        c = c.resize((int(c.width * a.scale), int(c.height * a.scale)))
        yy = int((y - top) * a.scale); ImageDraw.Draw(c).line((0, yy, 12, yy), fill=0, width=3)
        parts.append((it, c))
    stack(parts, a.output)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("review"); s.add_argument("work"); s.add_argument("keys"); s.add_argument("-o", "--output", required=True)
    s = sub.add_parser("context"); s.add_argument("work"); s.add_argument("cls", nargs="?"); s.add_argument("-o", "--output")
    s = sub.add_parser("next"); s.add_argument("work"); s.add_argument("n", nargs="?", type=int, default=16)
    s.add_argument("-o", "--output", required=True)
    s = sub.add_parser("word"); s.add_argument("tess"); s.add_argument("items", nargs="+")
    s.add_argument("-w", "--width", type=int, default=480, help="pixels left and right of the word")
    s.add_argument("-z", "--zoom", type=float, default=1.0); s.add_argument("-o", "--output", required=True)
    s = sub.add_parser("strip"); s.add_argument("items", nargs="+"); s.add_argument("-s", "--scale", type=float, default=0.55)
    s.add_argument("-o", "--output", required=True)
    a = ap.parse_args()
    {"review": cmd_review, "context": cmd_context, "next": cmd_next, "word": cmd_word, "strip": cmd_strip}[a.cmd](a)


if __name__ == "__main__":
    main()
