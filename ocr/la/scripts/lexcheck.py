"""Check 2 of ocr/la/PLAN.md: rare forms one or two letters from common ones.

    lexcheck.py FIRST LAST [-o OUT] [-t TESS] [-d DIR] [--min N] [--ratio X] [-g G]

The words of all pages (0001-1296; the italic marks removed, a word hyphenated at a line
end joined) are counted case-insensitively. Each form of count 1-2 on pages FIRST..LAST
that has a neighbour, a form at edit distance 1 (2 for forms of 8 letters or more) with a
count of at least --min (default 5) and at least --ratio (default 5) times its own, is a
candidate: listed with its page and line, the counts, the neighbours, the line, and
Tesseract's word at that place (TESS/PAGE.tsv, default ocr/la/tesseract; `t:`).

Ranked in three groups by Tesseract's word: 1, a neighbour (accents aside: Tesseract often
drops them), or a form whose neighbour differs from it only in accents (on which Tesseract
has no vote); 2, another word; 3, the form itself (accents aside). In the trial on the first
transcription (commit 89ac4a3) 78% of group 1 were misreadings, 24% of group 2, 0.8% of
group 3. -g G lists the groups up to G only (default 3). A pair of letters that the OCRs
confuse (PAIRS) is shown (`[c/e]`). Left out: the forms decided at
that page (matched by page and form, as line numbers shift) in ocr/la/lexcheck.tsv,
lemmacheck.tsv, versecheck.tsv and the "Suspected misprints" of ocr/la/PLAN.md.

-d reads the page files from DIR instead of ocr/la (the recall trial on an earlier
transcription); the decided forms and Tesseract stay those of ocr/la."""

import argparse
import csv
import difflib
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import lemmacheck as L

ROOT = Path(__file__).resolve().parent.parent
WORD = re.compile(r"[^\W\d_⁰¹²³⁴⁵⁶⁷⁸⁹]+")  # superscripts are \w
PAIRS = [("c", "e"), ("n", "u"), ("r", "t"), ("rn", "m"), ("li", "h"), ("f", "s"), ("cl", "d")]
TABLES = ("lexcheck.tsv", "lemmacheck.tsv", "versecheck.tsv", "misprints.tsv")


def page_words(text):
    """[(form, line)] of a page: the italic marks removed, a word broken by a hyphen at a
    line end joined to the first word of the next line (as texts/scripts/convert_la.py)."""
    # the brackets of a restored letter are not word breaks (`desist[eb]amus`)
    lines = re.sub(r"[\[\]]", "", L.unmark(text)).replace("’", "'").split("\n")
    out, pending = [], None
    for i, t in enumerate(lines, 1):
        t = t.strip()
        ws = list(WORD.finditer(t))
        for k, m in enumerate(ws):
            w, line = m.group(), i
            if pending and k == 0:
                w, line = pending[0] + w, pending[1]
            pending = None
            if k == len(ws) - 1 and t[m.end():] == "-":
                pending = (w, line)
                continue
            out.append((w, line))
        if not ws and t:
            pending = None
    if pending:
        out.append(pending)  # broken at the page end: its tail is on the next page
    return out


def deletes(w, d):
    """w and every form of w with up to d letters deleted."""
    out, cur = {w}, {w}
    for _ in range(d):
        cur = {x[:i] + x[i + 1:] for x in cur for i in range(len(x))}
        out |= cur
    return out


def limit(w):
    return 2 if len(w) >= 8 else 1


def neighbours(counts, rare, min_count, ratio):
    """form -> [neighbours] for the forms in rare (symmetric deletion, then the distance)."""
    common = [w for w, c in counts.items() if c >= min_count]
    index = defaultdict(set)
    for w in common:
        for x in deletes(w, 2 if len(w) >= 7 else 1):
            index[x].add(w)
    out = {}
    for w in rare:
        d = limit(w)
        near = set()
        for x in deletes(w, d):
            near |= index.get(x, set())
        found = sorted((n for n in near if n != w and counts[n] >= ratio * counts[w]
                        and L.dist(w, n, d) <= d), key=lambda n: -counts[n])
        if found:
            out[w] = found
    return out


def pair_of(a, b):
    """The pair of PAIRS that turns a into b (one replacement), or None."""
    for x, y in PAIRS:
        for p, q in ((x, y), (y, x)):
            i = a.find(p)
            while i >= 0:
                if a[:i] + q + a[i + len(p):] == b:
                    return f"{p}/{q}"
                i = a.find(p, i + 1)
    return None


def decided_forms():
    """{(page, form lowercased)} decided in the tables, the misprints (misprints.tsv) included."""
    out = set()
    for name in TABLES:
        tsv = ROOT / name
        if not tsv.exists():
            continue
        for r in csv.reader(open(tsv, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
            if len(r) >= 3 and r[0] != "page":
                for w in WORD.findall(r[2]):
                    out.add((r[0], w.lower()))
    return out


def tess_word(page, line, form, text):
    """Tesseract's word at the place of form (line of page), or None."""
    if not (L.TESS / f"{page:04d}.tsv").exists():
        return None
    try:
        run, _ = locate_run(page, line)
    except ValueError:
        return None
    words = [w[4] for w in run]
    if not words:
        return None
    text = re.sub(r"[\[\]]", "", text)
    head = form if form.lower() in text.lower() else None
    if head is None:  # joined across the line end: the head is the line's last word
        last = WORD.findall(text)
        head = last[-1] if last else form
    key = head.lower()
    best = max(words, key=lambda w: difflib.SequenceMatcher(None, key, w.lower()).ratio())
    t = "".join(WORD.findall(best))
    if head != form and best.endswith("-"):
        try:
            nxt, _ = locate_run(page, line + 1)
            if nxt:
                t += "".join(WORD.findall(nxt[0][4]))
        except (ValueError, IndexError):
            pass
    return t or None


def locate_run(page, line):
    """The Tesseract words of a line (as lemmacheck.locate, which gives the box)."""
    lines, verse, end = L.page_layout(page)
    if end is not None:
        if line in verse:
            lines = [ws for ws in lines if max(w[3] for w in ws) <= end + 5]
        else:
            lines = [ws for ws in lines if min(w[1] for w in ws) >= end - 5]
    score = L.likeness(L.text_line(page, line))
    seed = max(lines, key=score)
    top, bottom = min(w[1] for w in seed), max(w[3] for w in seed)
    pool = sorted(w for ws in lines for w in ws
                  if min(w[3], bottom) - max(w[1], top) > 0.5 * (w[3] - w[1]))
    best, value = seed, score(seed)
    for i in range(len(pool)):
        for j in range(i + 1, len(pool) + 1):
            v = score(pool[i:j])
            if v > value:
                best, value = pool[i:j], v
    return best, value


def count(pages_dir, min_count, ratio):
    """(places [(page, line, form)], counts, neighbours of the rare forms)."""
    L.ROOT = Path(pages_dir)
    texts = {n: (L.ROOT / f"{n:04d}.txt").read_text(encoding="utf-8") for n in range(1, 1297)
             if (L.ROOT / f"{n:04d}.txt").exists()}
    places, counts = [], Counter()
    for n, t in texts.items():
        if "[Blank page]" in t:
            continue
        for w, line in page_words(t):
            counts[w.lower()] += 1
            places.append((n, line, w))
    rare = {w for w, c in counts.items() if c <= 2}
    return places, counts, neighbours(counts, rare, min_count, ratio)


def bare(w):
    """w without its accents."""
    return "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))


def context(text, form, width=50):
    """The line, cut to about width letters on each side of form (an essay line is a
    paragraph)."""
    i = text.find(form)
    if len(text) <= 2 * width + len(form) or i < 0:
        return text
    a, b = max(0, i - width), i + len(form) + width
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


def find(first, last, pages_dir, min_count, ratio):
    """The candidates: [(group, page, line, form, count, [(neighbour, count)], pair, tess)]."""
    places, counts, near = count(pages_dir, min_count, ratio)
    decided = decided_forms()
    found = []
    for n, line, w in places:
        k = w.lower()
        if not first <= n <= last or k not in near or (f"{n:04d}", k) in decided:
            continue
        ns = near[k]
        text = L.text_line(n, line)
        tw = tess_word(n, line, w, text)
        pair = next((p for p in (pair_of(k, x) for x in ns) if p), None)
        t = bare((tw or "").lower())
        if any(bare(x) == bare(k) for x in ns):
            group = 1
        else:
            group = 3 if not t or t == bare(k) else 1 if t in {bare(x) for x in ns} else 2
        found.append((group, n, line, w, counts[k], [(x, counts[x]) for x in ns], pair, tw))
    found.sort(key=lambda f: (f[0], f[1], f[2]))
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("-t", "--tess", default=str(L.TESS), help="Tesseract's PAGE.tsv directory")
    ap.add_argument("-d", "--dir", default=str(ROOT), help="read the pages from DIR")
    ap.add_argument("--min", type=int, default=5, help="the least count of a neighbour")
    ap.add_argument("--ratio", type=float, default=5, help="a neighbour's count over the form's")
    ap.add_argument("-g", "--groups", type=int, default=3, help="list the groups up to G")
    a = ap.parse_args()
    L.TESS = Path(a.tess)
    found = find(a.first, a.last, a.dir, a.min, a.ratio)
    groups = Counter(f[0] for f in found)
    found = [f for f in found if f[0] <= a.groups]
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    for group, n, line, w, c, ns, pair, tw in found:
        nb = ", ".join(f"{x} {k}" for x, k in ns[:4])
        print(f"{group} {n:04d}:{line} {w} {c} ~ {nb}" + (f"  [{pair}]" if pair else "")
              + f"  t: {tw or '-'}", file=out)
        print(f"    {context(re.sub(r'[\[\]]', '', L.text_line(n, line)), w)}", file=out)
    print(f"{len(found)} candidates (" + ", ".join(f"group {g}: {groups[g]}" for g in (1, 2, 3)) + ")",
          file=out)
    if a.output:
        out.close()


if __name__ == "__main__":
    main()
