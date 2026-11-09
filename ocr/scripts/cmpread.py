"""Compares the page files of a source with a retype and with Tesseract, word by word.

For each page of RETYPE (`RETYPE/PAGE.txt`), the words and marks of `DIR/PAGE.txt` (the
base; the printed side of a misprint mark), of the retype and of Tesseract's word boxes
(`TESS/PAGE.tsv`) are aligned. Normalized first: the quotes and apostrophes straight, any
dash or run of dashes one `-`, the superscript note markers dropped, the spacing ignored
(`ch’ io` = `ch’io`, `lontana :` = `lontana:`), a word hyphenated at a line end joined. For
the Greek: Unicode NFC (the accent `ά` with tonos or oxia alike), the elision marks, the
numeral signs and `„` as the quotes, the upper dot `·` however written; the accents and
breathings themselves are compared. Every place where the base differs from the
retype is listed with Tesseract's words for the same place, in a class:

- A: Tesseract agrees with the retype against the base (case ignored);
- B: the retype alone differs;
- C: base and retype differ in length by at least --run tokens (default 6): a run one of
  them lacks (lost text, a line doubled).

Output, a TSV sorted by page and line: page, line (of the base), class, base, retype,
tesseract, and the text of the base line.

    uv run ocr/scripts/cmpread.py ocr/en tmp/en-retype01 -t ocr/en/tesseract -o cmp.tsv
"""
import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
ap.add_argument("dir", type=Path, help="directory of the page files (e.g. ocr/en)")
ap.add_argument("retype", type=Path, help="directory of the retyped pages (PAGE.txt)")
ap.add_argument("-t", "--tess", type=Path, help="Tesseract's TSVs (default: DIR/tesseract)")
ap.add_argument("-o", "--output", type=Path, help="output TSV (default: stdout)")
ap.add_argument("--run", type=int, default=6, help="least length of a lost run, class C (6)")
ap.add_argument("pages", nargs="*", help="pages to compare (default: all of RETYPE)")
a = ap.parse_args()
tess_dir = a.tess or a.dir / "tesseract"

MARK = re.compile(r"\{\{([^{}|]*)\|[^{}|]*\}\}")
SUPER = re.compile(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+")
TOKEN = re.compile(r"\w+|-|[^\w\s]")
QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "´": "'", "`": "'",
                        "„": '"', "«": '"', "»": '"', "\u1fbf": "'", "\u1fbd": "'",
                        "\u02bc": "'", "\u02b9": "'", "\u0384": "'",
                        "˙": "·", "•": "·", "\u0387": "·"})
HYPHEN_END = re.compile(r"(\w)-[ \t]*$")


def norm(text):
    text = unicodedata.normalize("NFC", text)
    text = SUPER.sub("", MARK.sub(r"\1", text)).translate(QUOTES)
    return re.sub(r"[-‐‑‒–—―]+", "-", text)


def tokens(lines):
    """(token, line) over the lines; a word hyphenated at a line end is joined and given
    the first line."""
    out, join = [], False
    for n, line in enumerate(lines, 1):
        toks = TOKEN.findall(norm(line))
        if join and toks and re.match(r"\w", toks[0]):
            out[-1] = (out[-1][0] + toks[0], out[-1][1])
            toks = toks[1:]
        out += [(t, n) for t in toks]
        join = bool(HYPHEN_END.search(line)) and len(out) >= 2 and out[-1][0] == "-"
        if join:
            out.pop()
    return out


def tess_tokens(page):
    f = tess_dir / f"{page}.tsv"
    if not f.exists():
        return []
    rows = f.read_text(encoding="utf-8").split("\n")[1:]
    cells = [r.split("\t") for r in rows if r.count("\t") >= 7]
    words = []
    for k, c in enumerate(cells):
        # a word hyphenated at a line end joined with the first word of the next line
        if words and words[-1][1] and words[-1][0].endswith("-"):
            words[-1] = (words[-1][0][:-1] + c[7], False)
            continue
        last = k + 1 == len(cells) or cells[k + 1][:3] != c[:3]
        words.append((c[7], last and len(c[7]) > 1))
    return [t for w, _ in words for t in TOKEN.findall(norm(w))]


def align(x, y):
    return difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes()


def compare(page):
    base_lines = (a.dir / f"{page}.txt").read_text(encoding="utf-8").split("\n")
    base = tokens(base_lines)
    ret = [t for t, _ in tokens((a.retype / f"{page}.txt").read_text(encoding="utf-8").split("\n"))]
    tess = tess_tokens(page)
    bk = [t for t, _ in base]
    # each base token's place in Tesseract (equal runs only), to find Tesseract's words
    # for a span of the base
    pos = {}
    for op, i1, i2, j1, j2 in align([t.lower() for t in bk], [t.lower() for t in tess]):
        if op == "equal":
            for k in range(i2 - i1):
                pos[i1 + k] = j1 + k

    def tess_span(i1, i2):
        left = max((pos[k] + 1 for k in range(i1 - 1, -1, -1) if k in pos), default=None)
        right = min((pos[k] for k in range(i2, len(bk)) if k in pos), default=None)
        if left is None or right is None or right < left or right - left > 3 * (i2 - i1) + 10:
            return None
        return tess[left:right]

    out = []
    for op, i1, i2, j1, j2 in align(bk, ret):
        if op == "equal":
            continue
        b, r = bk[i1:i2], ret[j1:j2]
        line = base[i1][1] if i1 < len(base) else base[-1][1]
        t = tess_span(i1, i2)
        if abs(len(b) - len(r)) >= a.run:
            cls = "C"
        elif t is not None and [x.lower() for x in t] == [x.lower() for x in r]:
            cls = "A"
        else:
            cls = "B"
        out.append((page, line, cls, " ".join(b), " ".join(r),
                    "?" if t is None else " ".join(t), base_lines[line - 1]))
    return out


pages = a.pages or sorted(f.stem for f in a.retype.glob("*.txt") if f.stem.isdigit())
rows = []
for p in pages:
    if not (a.retype / f"{p}.txt").exists():
        print(f"{p}: no retype", file=sys.stderr)
        continue
    rows += compare(p)
text = "\n".join(["page\tline\tclass\tbase\tretype\ttesseract\ttext"]
                 + ["\t".join(map(str, r)) for r in rows]) + "\n"
if a.output:
    a.output.write_text(text, encoding="utf-8")
    counts = {c: sum(r[2] == c for r in rows) for c in "ABC"}
    print(f"{len(pages)} pages, {len(rows)} places: "
          + ", ".join(f"{c} {n}" for c, n in counts.items()) + f": {a.output}")
else:
    sys.stdout.write(text)
