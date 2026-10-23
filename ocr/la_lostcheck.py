"""Text of the two OCRs that an ocr/la page lacks (lost lines and passages).

    la_lostcheck.py FIRST LAST -t TESS [-g GLM] [-d DIR ...] [-n N] [-v] [-o OUT]

For each page, the words of Tesseract (TESS/PAGE.tsv) and of GLM-OCR (GLM/PAGE.txt, default
ocr/la/glm-ocr) are looked up in the page file (the first DIR that has PAGE.txt; default
ocr/la), loosely and in any order: each run of three words (normalized: lowercase, letters
only, u/v and i/j alike, words broken at a line end joined) counts as found when the file
has a run of three words at a similarity of 75 or more (rapidfuzz ratio). A word is covered
when a found run includes it. A hit is a run of N words or more (default 4) not covered:

- `both`: a run of Tesseract's words that GLM-OCR has too: text lost from the file (two
  OCRs agree), to look at in the image;
- `tess` / `glm`: a run only one OCR has: mostly that OCR's noise (specks, ornaments,
  `Digitized by Google`), sometimes text the other OCR lost too (GLM-OCR has no verse).

The order of the text is not checked (a moved line is found in any order), nor text that
the file and both OCRs lack. One line per page (`PAGE both N tess N glm N`, pages without
hits left out unless -v), then the hits."""

import argparse
import csv
import re
import sys
from pathlib import Path

from rapidfuzz import fuzz, process

ROOT = Path(__file__).resolve().parent / "la"


def norm(w):
    w = w.lower().replace("v", "u").replace("j", "i").replace("æ", "e").replace("œ", "e")
    return re.sub(r"[^a-zàèéìòóùäëïöü]", "", w)


def words(lines):
    """The normalized words of the lines, a word hyphenated at a line end joined."""
    out, carry = [], None
    for line in lines:
        ws = line.split()
        for k, w in enumerate(ws):
            if carry is not None:
                w, carry = carry + w.lstrip("["), None
            if k == len(ws) - 1 and re.search(r"\w-$", w):
                carry = w[:-1]
                continue
            if norm(w): out.append(norm(w))
    if carry and norm(carry): out.append(norm(carry))
    return out


def tess_lines(tess, page):
    """Tesseract's lines (block, paragraph, line), each as the text of its words."""
    lines = {}
    with open(Path(tess, f"{page}.tsv"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            t = (r["text"] or "").strip()
            if t: lines.setdefault((r["block_num"], r["par_num"], r["line_num"]), []).append(t)
    return [" ".join(v) for v in lines.values()]


def grams(ws):
    return [" ".join(ws[i:i + 3]) for i in range(max(0, len(ws) - 2))]


def covered(ws, target):
    """Indices of the words of ws inside a run of three found (loosely) in target."""
    cov = set()
    if not target: return cov
    for i, g in enumerate(grams(ws)):
        if process.extractOne(g, target, scorer=fuzz.ratio, score_cutoff=75):
            cov.update((i, i + 1, i + 2))
    return cov


def runs(n, cov, minlen):
    out, s = [], None
    for i in range(n + 1):
        if i < n and i not in cov:
            if s is None: s = i
        elif s is not None:
            if i - s >= minlen: out.append((s, i))
            s = None
    return out


def check(page, dirs, tess, glm, minlen):
    f = next((Path(d, f"{page}.txt") for d in dirs if Path(d, f"{page}.txt").exists()), None)
    if f is None: return None
    fg = grams(words(f.read_text(encoding="utf-8").split("\n")))
    tf, gf = Path(tess, f"{page}.tsv"), Path(glm, f"{page}.txt")
    T = words(tess_lines(tess, page)) if tf.exists() else []
    G = words(gf.read_text(encoding="utf-8").split("\n")) if gf.exists() else []
    hits = []
    tg, gg = grams(T), grams(G)
    for s, e in runs(len(T), covered(T, fg), minlen):
        both = len(covered(T[s:e], gg)) >= 0.6 * (e - s)
        hits.append(("both" if both else "tess", " ".join(T[s:e])))
    for s, e in runs(len(G), covered(G, fg), minlen):
        if len(covered(G[s:e], tg)) < 0.6 * (e - s):  # else listed as `both` above
            hits.append(("glm", " ".join(G[s:e])))
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-t", "--tessdir", required=True, help="Tesseract's PAGE.tsv files")
    ap.add_argument("-g", "--glmdir", default=str(ROOT / "glm-ocr"), help="GLM-OCR's PAGE.txt files")
    ap.add_argument("-d", "--dir", action="append",
                    help="page files; repeatable, the first that has the page is read (default ocr/la)")
    ap.add_argument("-n", type=int, default=4, help="the shortest run reported (words)")
    ap.add_argument("-v", "--verbose", action="store_true", help="list the pages without hits too")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    a = ap.parse_args()
    dirs = a.dir or [str(ROOT)]
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    for n in range(a.first, a.last + 1):
        page = f"{n:04d}"
        hits = check(page, dirs, a.tessdir, a.glmdir, a.n)
        if hits is None or not hits and not a.verbose: continue
        c = {k: sum(h[0] == k for h in hits) for k in ("both", "tess", "glm")}
        print(page, " ".join(f"{k} {v}" for k, v in c.items()), file=out)
        for k, t in hits:
            print(f"  {k}: {t}", file=out)
    if a.output: out.close()


if __name__ == "__main__":
    main()
