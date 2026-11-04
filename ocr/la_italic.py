"""Italics of ocr/la/DONE.md: the italic words of the commentary, found by their slant.

    la_italic.py FIRST LAST -t TESS [-o OUT] [-v] [--boxes DIR] [--min-slant X] [--max-upright X]

For each line of the commentary (the blocks after the verse and its gloss line, as
la_lemmacheck.py finds them; on a page with no verse, every block but the page head), the
Tesseract words of the line are located (la_lemmacheck.locate) and each word of ocr/la takes
the Tesseract word that most of its letters align with (a word left without one, as in a
paragraph-per-line essay, is aligned in the stream of the whole commentary). The word's
box, over the height of its Tesseract line, widened four times and binarized, is sheared
over a range of slants; the slant whose column profile is sharpest (the largest sum of
squares) is the slant of its vertical strokes. Measured from the page's median (the scan's
skew), a word is italic from --min-slant (default 0.16), roman up to --max-upright (0.09),
unknown between or without a box (italic measures about 0.27, roman 0). A word of one
letter is unknown, as its accent slants (`è`).

Output per page: the runs of italic words (consecutive words of the commentary, across
lines; an unknown word inside a run is kept in it, and one next to a run is taken in unless
a stop stands between: `corporea. Ad im-`), each with its lines, its words (`?` after an
unknown one), and the lemma of check 1 (la_lemmacheck.py) it overlaps, or `none`; then the
lemmas that no run overlaps (`not italic`). -v lists every commentary line with the slant
of each word; --boxes writes each page with its words boxed (red italic, blue roman, green
unknown). The errors are in lines where Tesseract's boxes are wrong (a misread line, boxes
shifted by a word). A page with no Tesseract words (0001, 0004) is skipped."""

import argparse
import difflib
import re
import statistics
import sys
from pathlib import Path

from PIL import Image

import la_lemmacheck as L

SLANTS = [round(-0.20 + 0.02 * i, 2) for i in range(36)]  # -0.20 .. 0.50


def slant(im, box, zoom=4):
    """The slant of the vertical strokes in box (x0, y0, x1, y1) of the grey image im: the
    horizontal shift per pixel of height, positive leaning right. The box is widened zoom
    times before it is binarized, so that a shear moves its rows by fractions of a pixel
    (at full pixels, a small word cannot tell 0 from 0.1)."""
    x0, y0, x1, y1 = box
    c = im.crop((x0, y0, x1, y1))
    w, h = c.size
    c = c.resize((w * zoom, h), Image.BILINEAR).point(lambda v: 255 if v < 128 else 0)
    pad = int(0.5 * h * zoom) + 2
    best = None
    for s in SLANTS:
        t = c.transform((w * zoom + 2 * pad, h), Image.AFFINE,
                        (1, -s * zoom, -pad + s * zoom * h / 2, 0, 1, 0), Image.NEAREST)
        v = sum(x * x for x in t.resize((t.width // zoom, 1), Image.BOX).get_flattened_data())
        if best is None or v > best[0]:
            best = (v, s)
    return best[1]


def line_words(text):
    """The words of a line as la_lemmacheck.tokens sees them (gloss marks removed)."""
    t = L.GLOSS.sub(" ", text)
    return [(m.group(), m.end()) for m in L.WORD.finditer(t)], t


def align(words, tess):
    """For each word (a string), the index of the Tesseract word (tess: [(..., text)]) that
    most of its letters align with, or None."""
    a, owner_a = "", []
    for k, w in enumerate(words):
        a += w.lower(); owner_a += [k] * len(w)
    b, owner_b = "", []
    for k, w in enumerate(tess):
        t = L.letters(w[4])
        b += t; owner_b += [k] * len(t)
    votes = [dict() for _ in words]
    for i, j, n in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for x in range(n):
            v = votes[owner_a[i + x]]
            v[owner_b[j + x]] = v.get(owner_b[j + x], 0) + 1
    return [max(v, key=v.get) if v else None for v in votes]


def page_words(page, im):
    """The words of the commentary of a page: [(line, form, slant or None, box or None)], in
    the order of the file."""
    _, _, comm = L.page_parts(page)
    lines, _, _ = L.page_layout(page)
    allw = [w for ws in lines for w in ws]
    full = {}  # each word's box over the height of its line (a short word's box is small)
    for ws in lines:
        top = statistics.median(v[1] for v in ws)
        bottom = statistics.median(v[3] for v in ws)
        for w in ws:
            full[w] = (w[0], int(min(w[1], top)), w[2], int(max(w[3], bottom)))
    out = []
    for i, text in comm:
        ws, _ = line_words(text)
        if not ws:
            continue
        (x0, y0, x1, y1), _ = L.locate(page, i)
        tess = sorted(w for w in allw if x0 <= (w[0] + w[2]) / 2 <= x1 and y0 <= (w[1] + w[3]) / 2 <= y1)
        idx = align([w for w, _ in ws], tess)
        cache = {}
        for (w, _), k in zip(ws, idx):
            if k is None:
                out.append((i, w, None, None))
                continue
            if k not in cache:
                cache[k] = slant(im, full[tess[k]])
            out.append((i, w, cache[k], full[tess[k]]))
    # a word left unknown (a paragraph-per-line essay, whose line spans many printed lines;
    # a line Tesseract split) is aligned in the stream of the whole commentary instead
    _, _, end = L.page_layout(page)
    stream = [w for w in allw if end is None or w[1] >= end - 5]
    idx = align([w for _, w, _, _ in out], stream)
    for x, (i, w, s, box) in enumerate(out):
        if s is None and idx[x] is not None:
            out[x] = (i, w, slant(im, full[stream[idx[x]]]), full[stream[idx[x]]])
    return out


def tokens(words):
    """The words joined at a line-end hyphen, as la_lemmacheck.tokens joins them:
    [(norm, form, line, [indices into words])]."""
    out, k = [], 0
    while k < len(words):
        parts = [k]
        while words[parts[-1]][3] and parts[-1] + 1 < len(words):
            parts.append(parts[-1] + 1)
        form = "".join(words[p][1] for p in parts)
        out.append((L.norm(form), form, words[k][0], parts))
        k = parts[-1] + 1
    return out


def page_lemmas(first, last):
    """{page: [(lang, set of (line, form)), text]}: the lemmas of check 1, from
    la_lemmacheck.find's verbose list."""
    verbose = []
    L.find(first, last, 3, 2, set(), verbose)
    out = {}
    for v in verbose:
        head, verse = v[2:].split("  | ", 1)
        loc, lang, *ws = head.split(" ")
        out.setdefault(int(loc.split(":")[0]), []).append((lang, int(loc.split(":")[1]), ws, verse))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-t", "--tess", required=True, help="Tesseract's TSV directory")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("-v", "--verbose", action="store_true", help="list the slant of every word")
    ap.add_argument("--min-slant", type=float, default=0.16, help="italic from this slant")
    ap.add_argument("--max-upright", type=float, default=0.09, help="roman up to this slant")
    ap.add_argument("--boxes", metavar="DIR", help="write each page with its words boxed: "
                    "red italic, blue roman (DIR/PAGE.png)")
    a = ap.parse_args()
    L.TESS = Path(a.tess)
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    lemmas = page_lemmas(a.first, a.last)
    total = {"runs": 0, "lemma": 0, "none": 0, "not italic": 0}
    for n in range(a.first, a.last + 1):
        if not (L.TESS / f"{n:04d}.tsv").exists() or "[Blank page]" in L.text_line(n, 1):
            continue
        if not L.page_layout(n)[0]:  # no Tesseract words: a cover, a library mark (0001, 0004)
            print(f"{n:04d}: no Tesseract words, skipped", file=sys.stderr)
            continue
        im = Image.open(L.ROOT / f"{n:04d}.png").convert("L")
        raw = page_words(n, im)
        if not raw:
            continue
        known = [s for _, _, s, _ in raw if s is not None]
        base = statistics.median(known) if known else 0
        # (line, form, slant, ends with a hyphen at the line end, box, the text after it)
        words, k = [], 0
        while k < len(raw):
            i = raw[k][0]
            ws, t = line_words(L.text_line(n, i).replace("’", "'").strip())
            for x, (w, end) in enumerate(ws):
                after = t[end:ws[x + 1][1] - len(ws[x + 1][0])] if x + 1 < len(ws) else t[end:]
                hyphen = x + 1 == len(ws) and after == "-"
                words.append((i, w, raw[k + x][2], hyphen, raw[k + x][3], after))
            k += len(ws)
        toks = tokens(words)

        def kind(s):
            """True italic, False roman, None between."""
            if s is None:
                return None
            return True if s - base >= a.min_slant else False if s - base <= a.max_upright else None

        def italic(tok):
            ss = [words[p][2] for p in tok[3] if words[p][2] is not None]
            if not ss or len(tok[1]) == 1:  # a lone letter: its accent slants (`è`)
                return None
            return kind(max(ss))

        def apart(x):
            """A stop between token x and the next."""
            return bool(re.search(r"[.,:;!?()\[\]]", words[toks[x][3][-1]][5]))

        flags = [italic(t) for t in toks]
        if a.boxes:
            from PIL import ImageDraw
            Path(a.boxes).mkdir(parents=True, exist_ok=True)
            b = im.convert("RGB"); d = ImageDraw.Draw(b)
            for w in words:
                if w[4] is not None:
                    d.rectangle(w[4], outline={True: "red", False: "blue", None: "green"}[kind(w[2])], width=2)
            b.save(Path(a.boxes) / f"{n:04d}.png")
        # a run: italic words and the unknown words between them; an unknown word next to
        # a run is taken in unless a stop stands between (0095:94 `corporea. Ad im-`)
        runs, k = [], 0
        while k < len(toks):
            if flags[k]:
                j = k
                while j + 1 < len(toks) and flags[j + 1] is not False:
                    j += 1
                while flags[j] is None and apart(j - 1):
                    j -= 1
                while k > 0 and flags[k - 1] is None and not apart(k - 1) \
                        and not (runs and runs[-1][1] >= k - 1):
                    k -= 1
                runs.append((k, j)); k = j + 1
            else:
                k += 1
        print(f"## {n:04d}  (upright {base:+.2f})", file=out)
        if a.verbose:
            cur = None
            for i, w, s, *_ in words:
                if i != cur:
                    if cur is not None:
                        print(file=out)
                    print(f"  {i:3d}", end="", file=out); cur = i
                mark = "?" if s is None else f"{s - base:+.2f}"
                print(f" {w}/{mark}", end="", file=out)
            print(file=out)
        lem = lemmas.get(n, [])
        used = set()
        for k, j in runs:
            span = toks[k:j + 1]
            lines = sorted({words[p][0] for t in span for p in t[3]})
            text = " ".join(t[1] if flags[k + x] else f"{t[1]}?" for x, t in enumerate(span))
            match = []
            for x, (lang, line, ws, verse) in enumerate(lem):
                # the lemma's tokens are the commentary's: match by the first line and the words
                for y in range(len(toks)):
                    if toks[y][2] == line and [t[1] for t in toks[y:y + len(ws)]] == ws:
                        if y <= j and y + len(ws) - 1 >= k:
                            match.append(f"{lang} {' '.join(ws)} | {verse}"); used.add(x)
                        break
            total["runs"] += 1
            total["lemma" if match else "none"] += 1
            where = f"{lines[0]}" if len(lines) == 1 else f"{lines[0]}-{lines[-1]}"
            print(f"{n:04d}:{where} {text}", file=out)
            for m in match or ["none"]:
                print(f"    = {m}", file=out)
        for x, (lang, line, ws, verse) in enumerate(lem):
            if x not in used:
                total["not italic"] += 1
                print(f"{n:04d}:{line} not italic: {lang} {' '.join(ws)} | {verse}", file=out)
    print(f"{total['runs']} runs ({total['lemma']} with a lemma, {total['none']} none), "
          f"{total['not italic']} lemmas not italic", file=out)
    if a.output:
        out.close()


if __name__ == "__main__":
    main()
