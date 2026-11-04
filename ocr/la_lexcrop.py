"""Check 2 of ocr/la/PLAN.md: crops of the candidates' words, and a reader's readings of them.

    la_lexcrop.py LIST FIRST LAST [-g G] --crops DIR [--labels]
    la_lexcrop.py LIST FIRST LAST [-g G] --readings READ [-o OUT]

LIST is the output of la_lexcheck.py; its candidates of group G (default 2) on pages
FIRST..LAST are taken, in its order.

--crops writes, for each candidate, a crop of the page image around its word, 8 to an
image (DIR/c001.png, ...; each with a yellow label, its number, and a red box on the
word), and DIR/context.tsv (`n  line`): the line as in ocr/la, the word replaced by
`____` (a word broken at the line end: `____- / ____`), cut to about 60 letters on each
side. The word is found among Tesseract's words by its neighbours (a window of five
tokens), within the located line, or within the whole page for an essay paragraph or a
line not located; a word Tesseract split in two is joined. A word broken at the line end
gets a second strip, the first word of the next line. The box may be off the word (no
Tesseract box, an essay's hyphen halves): the masked line lets the reader find it.
--labels adds `PAGE:LINE form` to the labels (for one's own use; not for a blind reader).

--readings compares a reader's READ (`n  reading`, a TSV with a header) with the forms:
lists the candidates whose reading differs (hyphens and case aside; a reading that
contains the form as a word agrees), `n PAGE:LINE form | reading | Tesseract`, and the
count."""

import argparse
import csv
import difflib
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import la_lemmacheck as L
import la_lexcheck as X

LET = r"[^\W\d_]"
ROW = re.compile(r"(\d) (\d{4}):(\d+) ")


def rows(path, first, last, group):
    out = []
    for line in open(path, encoding="utf-8"):
        m = ROW.match(line)
        if m and int(m[1]) == group and first <= int(m[2]) <= last:
            out.append(line.split())
    return out


def letters(t):
    return re.sub(r"[^\w]", "", t.lower())


def sim(a, b):
    return difflib.SequenceMatcher(None, letters(a), letters(b)).ratio()


def raw_line(n, line):
    return re.sub(r"[\[\]]", "", L.text_line(n, line)).replace("’", "'").strip()


def find_box(n, line, ti=None, form=None):
    """Tesseract's box of the word: token ti of the line, or the token holding form; and
    whether the word is broken at the line end."""
    raw = raw_line(n, line)
    toks = raw.split()
    hyph = False
    if ti is None:
        ti = next((k for k, t in enumerate(toks) if form in t), None)
        if ti is None:
            ti = next((k for k, t in enumerate(toks) if form.lower() in t.lower()), None)
        if ti is None:  # joined across the line end
            ti, hyph = len(toks) - 1, raw.endswith("-")
    page = [w for ws in L.tess_lines(n) for w in ws]
    run, value = (None, 0) if len(raw) > 200 else X.locate_run(n, line)
    pool = run if run and value >= 0.7 else page
    k0, k1 = ti - max(0, ti - 2), min(len(toks), ti + 3) - ti
    win = " ".join(toks[ti - k0:ti + k1])
    tok = toks[ti]

    def score(j):
        return (0.6 * sim(win, " ".join(w[4] for w in pool[max(0, j - k0):j + k1]))
                + 0.4 * sim(tok, pool[j][4]))

    j = max(range(len(pool)), key=score)
    x0, y0, x1, y1, t = pool[j]
    changed = True
    while changed:  # a word Tesseract split in two
        changed = False
        for a in page:
            if a[0] >= x0 and a[2] <= x1:
                continue
            same = min(a[3], y1) - max(a[1], y0) > 0.5 * (y1 - y0)
            near = (a[2] <= x0 + 2 and -2 <= x0 - a[2] < 0.3 * (y1 - y0)) or \
                   (a[0] >= x1 - 2 and -2 <= a[0] - x1 < 0.3 * (y1 - y0))
            if same and near:
                x0, y0, x1, y1 = min(x0, a[0]), min(y0, a[1]), max(x1, a[2]), max(y1, a[3])
                changed = True
    return (x0, y0, x1, y1, t), hyph


def masked(n, line, form, width=60):
    """The line with the form replaced by ____ (both parts of a word broken at the line
    end), cut to about width letters on each side."""
    raw = raw_line(n, line)
    m = re.search(rf"(?<!{LET}){re.escape(form)}(?!{LET})", raw) or re.search(re.escape(form), raw, re.I)
    if m:
        t = raw[:m.start()] + "____" + raw[m.end():]
    else:  # joined across the line end
        m = re.search(rf"({LET}+)-$", raw)
        nxt = raw_line(n, line + 1)
        m2 = re.match(rf"{LET}+", nxt)
        t = raw[:m.start(1) if m else len(raw)] + "____- / ____" + (nxt[m2.end():] if m2 else nxt)
    i, e = t.find("____"), t.rfind("____") + 4
    lo, hi = max(0, i - width), min(len(t), e + width)
    return ("…" if lo else "") + t[lo:hi] + ("…" if hi < len(t) else "")


def crop(n, w):
    im = Image.open(L.ROOT / f"{n:04d}.png").convert("RGB")
    x0, y0, x1, y1 = w[:4]
    a = max(0, x0 - 420)
    c = im.crop((a, max(0, y0 - 14), min(im.width, x1 + 420), min(im.height, y1 + 14)))
    c = c.resize((c.width * 3 // 2, c.height * 3 // 2))
    ImageDraw.Draw(c).rectangle(((x0 - a) * 3 // 2 - 2, 2, (x1 - a) * 3 // 2 + 2, c.height - 2),
                                outline="red")
    return c


def write_crops(rs, out, labels):
    out.mkdir(parents=True, exist_ok=True)
    crops, ctx = [], []
    for r in rs:
        n, line = (int(x) for x in r[1].split(":"))
        form = r[2]
        w, hyph = find_box(n, line, form=form)
        cs = [crop(n, w)]
        if hyph:
            cs.append(crop(n, find_box(n, line + 1, ti=0)[0]))
        c = Image.new("RGB", (max(x.width for x in cs), sum(x.height for x in cs)), "white")
        y = 0
        for x in cs:
            c.paste(x, (0, y))
            y += x.height
        k = len(crops) + 1
        crops.append((f"{k} {r[1]} {form}" if labels else f"{k}", c))
        ctx.append(f"{k}\t{masked(n, line, form)}")
    for k in range(0, len(crops), 8):
        part = crops[k:k + 8]
        W = max(c.width for _, c in part)
        H = sum(c.height + 18 for _, c in part)
        b = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(b)
        y = 0
        for lab, c in part:
            d.rectangle((0, y, W, y + 17), fill="yellow")
            d.text((4, y + 3), lab, fill="black")
            y += 18
            b.paste(c, (0, y))
            y += c.height
        b.save(out / f"c{k // 8 + 1:03d}.png")
    (out / "context.tsv").write_text("n\tline\n" + "\n".join(ctx) + "\n", encoding="utf-8")
    print(f"{len(crops)} crops, {(len(crops) + 7) // 8} images", file=sys.stderr)


def compare(rs, path):
    with open(path, encoding="utf-8") as f:
        rd = {r[0]: r[1] if len(r) > 1 else ""
              for r in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)}
    out, dis = [], 0
    for i, r in enumerate(rs, 1):
        t = rd.get(str(i), "").replace("’", "'")
        j = t.replace("-", "").lower()
        if j != r[2].lower() and r[2].lower() not in re.findall(rf"{LET}+", j):
            dis += 1
            out.append(f"{i} {r[1]} {r[2]} | {t} | {r[-1]}")
    out.append(f"{dis} differ of {len(rs)}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("list", help="the output of la_lexcheck.py")
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int)
    ap.add_argument("-g", "--group", type=int, default=2, help="the group to take (default 2)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--crops", help="write the crops and context.tsv to this directory")
    g.add_argument("--readings", help="compare this reader's TSV with the forms")
    ap.add_argument("--labels", action="store_true", help="PAGE:LINE form in the labels")
    ap.add_argument("-o", "--output", help="write the comparison to this file instead of stdout")
    a = ap.parse_args()
    rs = rows(a.list, a.first, a.last, a.group)
    if a.crops:
        write_crops(rs, Path(a.crops), a.labels)
    else:
        text = compare(rs, a.readings)
        if a.output:
            Path(a.output).write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)


if __name__ == "__main__":
    main()
