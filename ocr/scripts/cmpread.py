"""Compares the page files of a source with a retype and with Tesseract, word by word.

For each page of RETYPE (`RETYPE/PAGE.txt`), the words and marks of `DIR/PAGE.txt` (the
base; the printed side of a misprint mark), of the retype and of Tesseract's word boxes
(`TESS/PAGE.tsv`) are aligned. Normalized first: the quotes and apostrophes straight, any
dash or run of dashes one `-`, the superscript note markers dropped, the spacing ignored
(`ch’ io` = `ch’io`, `lontana :` = `lontana:`), a word hyphenated at a line end joined. For
the Greek: Unicode NFC (the accent `ά` with tonos or oxia alike), the elision marks, the
numeral signs and `„` as the quotes, the upper dot `·` however written; the accents and
breathings themselves are compared. The marks of bold and italics (`**`, `*`, `_` at a
word's edge) are dropped: only the words are compared. With --verse-numbers, a number of
one to three digits at a line end, alone or in parentheses (`(7)`), and a line of such a
number alone, are dropped in all three readings (the tercet numbers of `ocr/en-oelsner`,
transcribed inconsistently). With -g, a fourth reading (GLM-OCR's pages, `GLM/PAGE.txt`,
normalized as the retype) is aligned too; a page it lacks, or one whose length is not
within --glm-ratio of the base's (a run-away page, a loop), is compared without it, and
said so on stderr. Every
place where the base differs from the retype is listed with Tesseract's (and GLM-OCR's)
words for the same place, in a class:

- A: Tesseract or GLM-OCR agrees with the retype against the base (case ignored);
- B: the retype alone differs;
- C: base and retype differ in length by at least --run tokens (default 6): a run one of
  them lacks (lost text, a line doubled);
- D (with -g): base and retype agree, and Tesseract and GLM-OCR both read the same other
  form (case and the ligatures `æ` `œ` ignored): an error the base and the retype may share. Words both lack are
  not listed (a margin label or a head they set elsewhere); marks both lack are.

Output, a TSV sorted by page and line: page, line (of the base), class, base, retype,
tesseract, (glm,) and the text of the base line; in class D the retype column has the
base's form, the other two their reading.

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
ap.add_argument("-g", "--glm", type=Path, help="directory of GLM-OCR's pages, a fourth reading")
ap.add_argument("--glm-ratio", type=float, default=1.3,
                help="GLM-OCR page used if its tokens are within 1/R..R of the base's (1.3)")
ap.add_argument("-o", "--output", type=Path, help="output TSV (default: stdout)")
ap.add_argument("--run", type=int, default=6, help="least length of a lost run, class C (6)")
ap.add_argument("--verse-numbers", action="store_true",
                help="drop a number of 1-3 digits at a line end (tercet numbers)")
ap.add_argument("pages", nargs="*", help="pages to compare (default: all of RETYPE)")
a = ap.parse_args()
tess_dir = a.tess or a.dir / "tesseract"

# a misprint mark `{{printed|fixed}}` or a correction `{{printed|LIST|fixed}}` (ocr/PLAN.md,
# "Decisions"): the printed side; a mark may span lines
MARK = re.compile(r"\{\{([^{}|]*)\|(?:[0-9]+(?:&[0-9]+)*\|)?[^{}|]*\}\}")
SUPER = re.compile(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+")
TOKEN = re.compile(r"\w+|-|[^\w\s]")
QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "´": "'", "`": "'",
                        "„": '"', "«": '"', "»": '"', "\u1fbf": "'", "\u1fbd": "'",
                        "\u02bc": "'", "\u02b9": "'", "\u0384": "'",
                        "˙": "·", "•": "·", "\u0387": "·"})
HYPHEN_END = re.compile(r"(\w)-[ \t]*$")
EMPHASIS = re.compile(r"\*+|(?<!\w)_+|_+(?!\w)")
LINE_NUMBER = re.compile(r"(^|\s)\(?\d{1,3}\)?\s*$")


def norm(text):
    text = unicodedata.normalize("NFC", text)
    text = SUPER.sub("", MARK.sub(r"\1", text)).translate(QUOTES)
    text = EMPHASIS.sub("", text)
    return re.sub(r"[-‐‑‒–—―]+", "-", text)


def tokens(lines):
    """(token, line) over the lines; a word hyphenated at a line end is joined and given
    the first line."""
    out, join = [], False
    for n, line in enumerate(lines, 1):
        if a.verse_numbers:
            line = LINE_NUMBER.sub("", line)
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
        if a.verse_numbers and last and re.fullmatch(r"\(?\d{1,3}\)?", c[7]):
            continue
        words.append((c[7], last and len(c[7]) > 1))
    return [t for w, _ in words for t in TOKEN.findall(norm(w))]


def align(x, y):
    return difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes()


def compare(page):
    base_text = (a.dir / f"{page}.txt").read_text(encoding="utf-8")
    base_lines = base_text.split("\n")
    base = tokens(MARK.sub(r"\1", base_text).split("\n"))
    ret = [t for t, _ in tokens((a.retype / f"{page}.txt").read_text(encoding="utf-8").split("\n"))]
    tess = tess_tokens(page)
    gf = a.glm / f"{page}.txt" if a.glm else None
    glm = ([t for t, _ in tokens(gf.read_text(encoding="utf-8").split("\n"))]
           if gf and gf.exists() else None)
    bk = [t for t, _ in base]
    if glm is not None and bk and not 1 / a.glm_ratio <= len(glm) / len(bk) <= a.glm_ratio:
        print(f"{page}: GLM-OCR not used ({len(glm)} tokens, the base {len(bk)})", file=sys.stderr)
        glm = None
    low = lambda ts: [t.lower() for t in ts]

    def spanner(other):
        """A function giving the words of another reading for a span of the base: each base
        token's place in it (equal runs only), the words between the nearest anchors."""
        pos = {}
        for op, i1, i2, j1, j2 in align(low(bk), low(other)):
            if op == "equal":
                for k in range(i2 - i1):
                    pos[i1 + k] = j1 + k

        def span(i1, i2):
            left = max((pos[k] + 1 for k in range(i1 - 1, -1, -1) if k in pos), default=None)
            right = min((pos[k] for k in range(i2, len(bk)) if k in pos), default=None)
            if left is None or right is None or right < left or right - left > 3 * (i2 - i1) + 10:
                return None
            return other[left:right]
        return span

    tess_span = spanner(tess)
    glm_span = spanner(glm) if glm is not None else None
    show = lambda ws: "?" if ws is None else " ".join(ws)

    def row(line, cls, b, r, t, g):
        cols = [page, line, cls, b, r, show(t)]
        if a.glm:
            cols.append("-" if glm is None else show(g))
        return tuple(cols + [base_lines[line - 1]])

    out, differ = [], set()
    for op, i1, i2, j1, j2 in align(bk, ret):
        if op == "equal":
            continue
        differ.update(range(i1 - 1, i2 + 1))
        b, r = bk[i1:i2], ret[j1:j2]
        line = base[i1][1] if i1 < len(base) else base[-1][1]
        t = tess_span(i1, i2)
        g = glm_span(i1, i2) if glm_span else None
        if abs(len(b) - len(r)) >= a.run:
            cls = "C"
        elif any(x is not None and low(x) == low(r) for x in (t, g)):
            cls = "A"
        else:
            cls = "B"
        out.append(row(line, cls, " ".join(b), " ".join(r), t, g))
    if glm is not None:
        # class D: where base and retype agree, Tesseract and GLM-OCR read the same other
        # form; the ligatures folded (both OCRs write `Æ` as `AE` or `Ae`)
        fold = lambda ts: [t.lower().replace("æ", "ae").replace("œ", "oe") for t in ts]
        for op, i1, i2, j1, j2 in align(fold(bk), fold(glm)):
            if op == "equal" or any(k in differ for k in range(i1, i2 + 1)):
                continue
            g, t = glm[j1:j2], tess_span(i1, i2)
            if t is None or fold(t) != fold(g) or abs((i2 - i1) - (j2 - j1)) >= a.run:
                continue
            # words both lack: a label or a running head they set elsewhere, not listed
            if not g and any(re.match(r"\w", x) for x in bk[i1:i2]):
                continue
            line = base[i1][1] if i1 < len(base) else base[-1][1]
            out.append(row(line, "D", " ".join(bk[i1:i2]), " ".join(bk[i1:i2]), t, g))
        out.sort(key=lambda r: r[1])
    return out


pages = a.pages or sorted(f.stem for f in a.retype.glob("*.txt") if f.stem.isdigit())
rows = []
for p in pages:
    if not (a.retype / f"{p}.txt").exists():
        print(f"{p}: no retype", file=sys.stderr)
        continue
    rows += compare(p)
head = "page\tline\tclass\tbase\tretype\ttesseract\t" + ("glm\t" if a.glm else "") + "text"
text = "\n".join([head]
                 + ["\t".join(map(str, r)) for r in rows]) + "\n"
if a.output:
    a.output.write_text(text, encoding="utf-8")
    counts = {c: sum(r[2] == c for r in rows) for c in ("ABCD" if a.glm else "ABC")}
    print(f"{len(pages)} pages, {len(rows)} places: "
          + ", ".join(f"{c} {n}" for c, n in counts.items()) + f": {a.output}")
else:
    sys.stdout.write(text)
