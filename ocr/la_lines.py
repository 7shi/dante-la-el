"""Checks of ocr/la pages after the markup method: rules, line breaks, dots.

    la_lines.py FIRST LAST -t TESS [-o OUT]

Each hit is a place to look at in the image, not a correction.

- rules: each short rule found in a column of ocr/la/PAGE.png (la_check.py's detection) is
  matched to the ocr/la line above it by the last three words of the Tesseract line above
  the rule. `NO BLANK` is a matched line not followed by a blank line; `?` is a rule whose
  line could not be matched (often a page-end rule, which is not written, or a rule at a
  column top). The detection misses faint rules.
- breaks: a line break of ocr/la where Tesseract reads the last two words of the line and
  the first word of the next inside one printed line (a printed line broken in two). Lines
  ending with a hyphen are skipped.
- dots: a dot followed by a lowercase word (in the line or at the start of the next), the
  commas convention's candidates. Abbreviations (`etc.`, `al.`, `cap.`, `i.`, small-capital
  references such as `GEN.`) are still listed: skip them by eye."""

import argparse
import collections
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import la_check as C  # noqa: E402

ROOT = C.ROOT
SKIP = {"etc", "al", "cap"}


def norm(w):
    return re.sub(r"[^a-z]", "", w.lower())


def tess_lines(tess, page):
    """Tesseract's words per line: [(text, left, top, width, height)]."""
    f = Path(tess, f"{page}.tsv")
    lines = collections.OrderedDict()
    if not f.exists(): return lines
    for r in f.read_text(encoding="utf-8").splitlines()[1:]:
        c = r.split("\t")
        if len(c) == 8 and c[7].strip():
            lines.setdefault((c[0], c[1], c[2]), []).append((c[7], int(c[3]), int(c[4]), int(c[5]), int(c[6])))
    return lines


def check_rules(page, L, lines):
    out = []
    im = Image.open(ROOT / f"{page}.png").convert("L")
    keys = [[norm(w) for w in l.split() if norm(w)][-3:] for l in L]
    for x0, x1 in C.columns(im):
        for y in C.rules(im, x0, x1):
            above = [ws for ws in lines.values()
                     if x0 - 40 <= ws[0][1] and ws[-1][1] <= x1 and max(w[2] + w[4] for w in ws) < y]
            if not above: continue
            ws = max(above, key=lambda ws: ws[0][2])
            k = [norm(w[0]) for w in ws if norm(w[0])][-3:]
            hit = [i for i, kk in enumerate(keys) if kk == k and k]
            if len(hit) != 1:
                out.append(f"{page} y{y} ?  {' '.join(w[0] for w in ws)[-40:]}"); continue
            i = hit[0]; nxt = L[i + 1] if i + 1 < len(L) else "(end)"
            if nxt != "": out.append(f"{page}:{i + 1} y{y} NO BLANK  {L[i][-40:]:>40} | {nxt[:40]}")
    return out


def check_breaks(page, L, lines):
    out = []
    inside = collections.Counter()
    for ws in lines.values():  # split a Tesseract line where it jumps a column gap
        seg, last = [], None
        for t, x, _, w, _ in ws:
            if last is not None and x - last > 60:
                inside.update(zip(seg, seg[1:], seg[2:])); seg = []
            if norm(t): seg.append(norm(t))
            last = x + w
        inside.update(zip(seg, seg[1:], seg[2:]))
    own = collections.Counter()
    for l in L:
        w = [norm(x) for x in l.split() if norm(x)]
        own.update(zip(w, w[1:], w[2:]))
    for i in range(len(L) - 1):
        if L[i].endswith("-"): continue
        x = [norm(w) for w in L[i].split() if norm(w)]
        y = [norm(w) for w in L[i + 1].split() if norm(w)]
        if len(x) < 2 or not y: continue
        t = (x[-2], x[-1], y[0])
        if inside[t] > own[t]: out.append(f"{page}:{i + 1}\t{L[i][-40:]:>40} | {L[i + 1][:40]}")
    return out


def check_dots(page, t):
    out = []
    for m in re.finditer(r"(\w+)\.([ \n])([a-z]\w*)", t):
        if m.group(1).lower() in SKIP: continue
        ln = t.count("\n", 0, m.start()) + 1
        s = t[max(0, m.start() - 40):m.end() + 20].replace("\n", "⏎")
        out.append(f"{page}:{ln}\t{s}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-t", "--tessdir", required=True, help="Tesseract's PAGE.tsv files")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    a = ap.parse_args()
    rules, breaks, dots = [], [], []
    for p in range(a.first, a.last + 1):
        page = f"{p:04}"
        if not (ROOT / f"{page}.txt").exists(): continue
        t = (ROOT / f"{page}.txt").read_text(encoding="utf-8"); L = t.split("\n")
        lines = tess_lines(a.tessdir, page)
        if lines and (ROOT / f"{page}.png").exists():
            rules += check_rules(page, L, lines); breaks += check_breaks(page, L, lines)
        dots += check_dots(page, t)
    out = ["# rules"] + rules + ["", "# breaks"] + breaks + ["", "# dots"] + dots
    text = "\n".join(out) + "\n"
    if a.output: Path(a.output).write_text(text, encoding="utf-8")
    else: sys.stdout.write(text)


if __name__ == "__main__":
    main()
