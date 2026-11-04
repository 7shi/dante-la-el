"""Italics of ocr/la/DONE.md: mark the italic words of the commentary from their slant, and
list the lines to look at in the image.

    la_italicmark.py SLANT -d OUTDIR [-o FLAGS] [-t TESS] [--likeness X] [--pages SPEC] [--join]

SLANT is the -v output of la_italic.py. The words of each commentary line it lists are
marked in ocr/la's text (its `*` removed) from their slant: italic from 0.16, roman up to
0.09 (relative to the page, as la_italic.py prints them). The words are taken as one
stream per paragraph (consecutive lines), so that the rules see across a line end:

- a word unknown or of one letter takes its nearest measured neighbours (italic if both
  are, or the one there is);
- the two halves of a word broken at a line end take the larger slant;
- a capital word measured roman just before an italic word, no stop between, is taken in
  (a lemma's head measures about -0.20 on its capital: `Non`, `Nos`);
- an elided word of one letter takes the side of the word after it (`*s'abbica*`);
- the pieces of a word joined by a bracket take the larger slant, or the first piece's
  side if none is measured (`*A[l]latro*`, `*O[r] quando*`);
- `etc.` is not marked (it stays outside the pair by the convention).

Marks: each line closes its own pairs; runs split at : . ; ? ! ( ); commas stay inside,
the stop after a run outside; a line-end hyphen and a bracket next to a word go inside.
Each page is written to OUTDIR/PAGE.txt; the essays (a page whose first line is in
capitals, to the next CAPITUL... page) are left out, unless --pages names the pages to
mark (`114,382-385`: only those, essays or not). With --join (the essays and the front
matter), two runs with only a period between them (and commas, spaces) are one run: a
source abridged is one pair, `*IV Sent., dist. XLV, cap. III. De*`. The flagged lines are then decided
in the image and corrected in OUTDIR before its pages go into ocr/la.

FLAGS lists the lines to decide in the image, with the reasons:
  box     Tesseract's words in the line are unlike it (likeness < --likeness): a misread
          line or shifted boxes, where the slant was measured on other words;
  letter  a word unknown or of one letter where italic and roman meet (`ab A, quod`);
  half    the halves of a broken word measured unlike;
  lone    a word measured unlike both its neighbours with no stop between (`primus` roman
          inside an italic run);
  alone   a word italic whose nearest measured words are roman, with a stop on one side
          at most, or measured under 0.20 (`ego`, `Zeno`, `ex` measured wrong;
          `*follem*, idest` right);
  head    a paragraph's first word roman just before a colon, italics after it in the
          line (`*Ego*: scilicet Dantes: *bene vidi …*`, the capital measured upright);
  caps    a word in capitals marked italic, not a Roman numeral (small capitals measured
          as italic: `DROUILHET DE *SIGALAS*`);
  edge    a word of one letter that begins or ends a run, or roman beside one with no stop
          between (`*e Della vera …*`, the `e` roman);
  join    runs joined across a period by --join (a source abridged, or two quotations)."""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import la_lemmacheck as L

STOP = re.compile(r"[:.;?!()]")
JOIN = re.compile(r"[\s.,]*\.[\s.,]*")
ROMAN = re.compile(r"[IVXLCDM]+")


def read_slants(path):
    """{(page, line): [slant or None per word]} from la_italic.py -v."""
    out, page = {}, None
    for l in open(path, encoding="utf-8"):
        m = re.match(r"## (\d{4})", l)
        if m:
            page = int(m.group(1)); continue
        m = re.match(r"  +(\d+) (.*)", l.rstrip("\n"))
        if m and page is not None:
            out[(page, int(m.group(1)))] = [None if w.endswith("/?") else float(w.rsplit("/", 1)[1])
                                            for w in m.group(2).split()]
    return out


def essays(last):
    """The essay pages up to last: from a page whose first line is in capitals (not a
    CAPITUL... or INCIPIT heading) to the next CAPITUL... page; blank pages are left out."""
    out, essay = set(), False
    for n in range(79, last + 1):
        f = L.ROOT / f"{n:04d}.txt"
        if not f.exists():
            continue
        first = f.read_text(encoding="utf-8").split("\n", 1)[0].strip()
        if first.startswith("[Blank page]"):
            continue
        if first.startswith("CAPITUL") or first.startswith("INCIPIT"):
            essay = False
        elif re.search(r"[^\W\d_]", first) and first == first.upper():
            essay = True
        if essay:
            out.add(n)
    return out


def kind(s, w, lo, hi):
    if s is None or len(w) == 1:
        return None
    return True if s >= hi else False if s <= lo else None


def mark_page(lines, slants, lo=0.09, hi=0.16, join=False):
    """Mark the commentary lines of a page (lines: the text, no `*`; slants: {line: [...]}).
    Returns {line: (new text, set of flags)}."""
    W = []  # (line, start, end, form, slant)
    bad = set()
    for i in sorted(slants):
        u = lines[i - 1]
        t = L.GLOSS.sub(lambda m: " " * len(m.group()), u)
        ws = [(i, m.start(), m.end(), m.group()) for m in L.WORD.finditer(t)]
        if len(ws) != len(slants[i]):
            bad.add(i); continue
        W += [w + (s,) for w, s in zip(ws, slants[i])]
    n = len(W)
    flags = {i: set() for i in slants}
    for i in bad:
        flags[i].add("count")

    def gap(x):
        """A stop or a paragraph break between word x and x + 1."""
        a, b = W[x], W[x + 1]
        if a[0] == b[0]:
            return STOP.search(lines[a[0] - 1][a[2]:b[1]]) is not None
        if b[0] != a[0] + 1:
            return True
        return STOP.search(lines[a[0] - 1][a[2]:] + " " + lines[b[0] - 1][:b[1]]) is not None

    def broken(x):
        """Word x ends its line with a hyphen and word x + 1 begins the next."""
        a = W[x]
        return x + 1 < n and W[x + 1][0] == a[0] + 1 and lines[a[0] - 1][a[2]:] == "-"

    G = [gap(x) for x in range(n - 1)] + [True]
    k = [kind(w[4], w[3], lo, hi) for w in W]
    for x in range(n - 1):  # the halves of a broken word
        if broken(x):
            ss = [s for s in (W[x][4], W[x + 1][4]) if s is not None]
            a, b = k[x], k[x + 1]
            if a is not None and b is not None and a != b:
                flags[W[x][0]].add("half"); flags[W[x + 1][0]].add("half")
            if ss:
                k[x] = k[x + 1] = kind(max(ss), "xx", lo, hi)
    flag = []
    for x, v in enumerate(k):
        if v is not None:
            flag.append(v); continue
        left = next((k[y] for y in range(x - 1, -1, -1) if k[y] is not None and not G[y]), None) \
            if x > 0 and not G[x - 1] else None
        right = next((k[y] for y in range(x + 1, n) if k[y] is not None), None) if not G[x] else None
        sides = [s for s in (left, right) if s is not None]
        flag.append(bool(sides) and all(sides))
        if left is not None and right is not None and left != right:
            flags[W[x][0]].add("letter")
    for x in range(n):  # `etc.` stays outside the pair (the convention)
        if W[x][3] == "etc":
            flag[x] = False
    for x in range(n - 2, -1, -1):  # an elided one-letter word goes with the next (`s'abbica`)
        a, b = W[x], W[x + 1]
        if len(a[3]) == 1 and a[0] == b[0] and lines[a[0] - 1][a[2]:b[1]] in ("'", "’"):
            flag[x] = flag[x + 1]
    x = 0  # the pieces of a word joined by brackets go together (`*A[l]latro*`, `*O[r]*`)
    while x < n - 1:
        y = x
        while y + 1 < n and W[y][0] == W[y + 1][0] and \
                re.fullmatch(r"[\[\]]+", lines[W[y][0] - 1][W[y][2]:W[y + 1][1]]):
            y += 1
        if y > x:
            ss = [W[z][4] for z in range(x, y + 1) if k[z] is not None]
            v = kind(max(ss), "xx", lo, hi) if ss else None
            for z in range(x, y + 1):
                flag[z] = flag[x] if v is None else v
        x = y + 1
    for x in range(n - 1):  # a capital before an italic word
        if flag[x] is False and W[x][3][0].isupper() and flag[x + 1] and not G[x]:
            flag[x] = True
    for x in range(1, n - 1):
        if k[x] is None or k[x - 1] is None or k[x + 1] is None:
            continue
        if k[x - 1] == k[x + 1] != k[x] and not G[x - 1] and not G[x]:
            flags[W[x][0]].add("lone")
    for x in range(n):
        if not k[x]:
            continue
        # the nearest measured words on each side, and whether a stop stands between
        L_ = next((y for y in range(x - 1, -1, -1) if k[y] is not None), None)
        R_ = next((y for y in range(x + 1, n) if k[y] is not None), None)
        lstop = L_ is None or any(G[y] for y in range(L_, x))
        rstop = R_ is None or any(G[y] for y in range(x, R_))
        lrom = L_ is None or k[L_] is False
        rrom = R_ is None or k[R_] is False
        if lrom and rrom and (L_ is not None or R_ is not None):
            if not (lstop and rstop) or (W[x][4] is not None and W[x][4] < 0.20):
                flags[W[x][0]].add("alone")
    for x in range(n):  # a paragraph's first word roman before a colon, italics after it
        if x > 0 and W[x - 1][0] == W[x][0]:
            continue
        if x > 0 and W[x - 1][0] == W[x][0] - 1 and lines[W[x][0] - 2].strip():
            continue
        if flag[x] is not False or not W[x][3][0].isupper():
            continue
        after = lines[W[x][0] - 1][W[x][2]:]
        if after.lstrip().startswith(":") and any(flag[y] for y in range(x + 1, n) if W[y][0] == W[x][0]):
            flags[W[x][0]].add("head")
    for x in range(n):
        w = W[x][3]
        if flag[x] and len(w) > 1 and w == w.upper() and w != w.lower() and not ROMAN.fullmatch(w):
            flags[W[x][0]].add("caps")
        if len(w) == 1 and w.isalpha() and lines[W[x][0] - 1][W[x][2]:W[x][2] + 1] not in ("'", "’"):
            for y in (x - 1, x + 1):  # beside a run (roman), or at a run's end (italic)
                out_ = not 0 <= y < n or G[min(x, y)] or not flag[y]
                if flag[x] and out_ or not flag[x] and not out_:
                    flags[W[x][0]].add("edge")
    out = {}
    for i in slants:
        u = lines[i - 1]
        if i in bad:
            out[i] = (u, flags[i]); continue
        xs = [x for x in range(n) if W[x][0] == i]
        runs, cur = [], None
        for x in xs:
            j = join and cur is not None and JOIN.fullmatch(u[W[x - 1][2]:W[x][1]])
            if flag[x] and cur is not None and (not G[x - 1] or j):
                if j and G[x - 1]:
                    flags[i].add("join")
                cur.append(x)
            else:
                if cur:
                    runs.append(cur)
                cur = [x] if flag[x] else None
        if cur:
            runs.append(cur)
        parts, pos = [], 0
        for r in runs:
            a, b = W[r[0]][1], W[r[-1]][2]
            if a > 0 and u[a - 1] == "[":
                a -= 1
            if b < len(u) and u[b] == "]":
                b += 1
            if u[b:] == "-":
                b += 1
            parts += [u[pos:a], "*", u[a:b], "*"]; pos = b
        parts.append(u[pos:])
        new = "".join(parts)
        assert new.replace("*", "") == u
        out[i] = (new, flags[i])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slant", help="la_italic.py -v output")
    ap.add_argument("-d", "--outdir", required=True, help="write the marked pages here")
    ap.add_argument("-o", "--output", help="write the flags to this file instead of stdout")
    ap.add_argument("-t", "--tess", default=str(L.ROOT / "tesseract"), help="Tesseract's TSV directory")
    ap.add_argument("--likeness", type=float, default=0.8, help="flag a line below this likeness")
    ap.add_argument("--pages", help="mark only these pages, essays included (`114,382-385`)")
    ap.add_argument("--join", action="store_true", help="join runs across a period (the essays)")
    a = ap.parse_args()
    L.TESS = Path(a.tess)
    slants = read_slants(a.slant)
    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    n_flag = 0
    pages = sorted({p for p, _ in slants})
    if a.pages:
        want = set()
        for r in a.pages.split(","):
            x, _, y = r.partition("-")
            want.update(range(int(x), int(y or x) + 1))
        pages, skip = [p for p in pages if p in want], set()
    else:
        skip = essays(pages[-1])
    for page in pages:
        if page in skip:
            continue
        lines = L.unmark((L.ROOT / f"{page:04d}.txt").read_text(encoding="utf-8")).split("\n")
        marked = mark_page(lines, {i: s for (p, i), s in slants.items() if p == page}, join=a.join)
        for i, (new, flags) in sorted(marked.items()):
            _, like = L.locate(page, i)
            if like < a.likeness:
                flags.add("box")
            lines[i - 1] = new
            if flags:
                n_flag += 1
                print(f"{page:04d}:{i}\t{','.join(sorted(flags))}\t{new}", file=out)
        (outdir / f"{page:04d}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"{n_flag} lines flagged", file=sys.stderr)
    if a.output:
        out.close()


if __name__ == "__main__":
    main()
