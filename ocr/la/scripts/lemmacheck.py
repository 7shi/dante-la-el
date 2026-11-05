"""Check 1 of ocr/la/PLAN.md: the lemmas of the commentary against the verse they quote.

    lemmacheck.py FIRST LAST [-o OUT] [-v] [--min-run N] [--min-exact N]
    lemmacheck.py FIRST LAST --crops DIR [--seed N] [--min-likeness X]
    lemmacheck.py FIRST LAST --readings DIR [-o OUT]

For each page of a canto (the scans of CANTOS in texts/scripts/convert_la.py, the essay aside), the
words of the commentary (the blocks after the verse and its gloss line) are aligned to the
Latin and the Italian verse of the whole canto, read as one stream of words. A lemma is a
run of commentary words that follow verse words in order, each equal to its verse word or
one or two letters from it (case, punctuation, `u`/`v`, `i`/`j` and the edition's spelling
variants `y`/`i`, `h`, doubled letters ignored), with at least --min-run words (default 3)
of which at least --min-exact are equal (default 2) and more than half. In a lemma, each
word that is not equal is a candidate, unless it differs only in its last two letters (an
inflection), is of 3 letters or fewer, or is its verse neighbour's word (two words
swapped): listed with the page and line of both sides and both lines.

Left out: the candidates decided in ocr/la/lemmacheck.tsv (`page line form decision note`;
matched by page and form). -v lists every lemma found too (`=` before each), for the trial.

--crops writes an image of each line of the candidates (both sides) to DIR, in a shuffled
order, for a reader who transcribes them from the image alone without seeing a lemma beside
its verse (DIR/lines.tsv maps the images back; see write_crops()). --readings compares the
reader's DIR/readings.tsv (`L0001<TAB>line as printed`) with ocr/la: each candidate with the
reader's words on both sides (`DIFFERS` where they are not ocr/la's), and every word of
those lines read otherwise."""

import argparse
import csv
import difflib
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESS = ROOT / "tesseract"  # italic.py -t sets it


def unmark(t):
    """The text without the italic marks `*…*` (ocr/la/PLAN.md, "Italics"); a `*` after a
    digit is printed (1283 `154*`) and stays."""
    return re.sub(r"(?<!\d)\*", "", t)
sys.path.insert(0, str(ROOT.parent.parent / "texts" / "scripts"))
from convert_la import CANTOS  # noqa: E402

WORD = re.compile(r"[^\W\d_]+")
NUMBER = re.compile(r"\[?\d+ ")
GLOSS = re.compile(r"\(\d{1,2}\)")


def norm(w):
    return w.lower().replace("v", "u").replace("j", "i")


def dist(a, b, limit=2):
    """Levenshtein distance of a and b, or limit + 1 if it is greater than limit."""
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > limit:
            return limit + 1
        prev = cur
    return prev[-1]


def loose(w):
    """The spelling variants of the edition ignored: `y` for `i`, `h`, doubled letters."""
    return re.sub(r"(.)\1", r"\1", w.replace("y", "i").replace("h", ""))


def near(a, b):
    """0 if equal, 1 or 2 if within reach, None if not. A pair within reach is a candidate
    (see candidate()) or only lets the lemma run on."""
    if a == b or loose(a) == loose(b):
        return 0
    d = dist(a, b)
    if d == 1 or (d == 2 and min(len(a), len(b)) > 3):
        return d
    return None


def candidate(a, b):
    """A pair within reach is listed unless it differs only in the last two letters (an
    inflection, an elision) or is a short word (3 letters or fewer)."""
    if min(len(a), len(b)) <= 3:
        return False
    if len(a) == len(b) and dist(a, b) == 1:
        return a[-1] == b[-1]  # one letter for another, not the last (0133 `nora`)
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return k < max(len(a), len(b)) - 2


def page_parts(n):
    """(italian, latin, commentary): lists of (line number, text) of page n."""
    lines = unmark((ROOT / f"{n:04d}.txt").read_text(encoding="utf-8")).replace("’", "'").split("\n")
    bs, cur = [], []
    for i, l in enumerate(lines, 1):
        if l.strip():
            cur.append((i, l.strip()))
        elif cur:
            bs.append(cur); cur = []
    if cur:
        bs.append(cur)
    verse, comm = [], []
    for b in bs:
        if all(re.fullmatch(r"[\dA-ZÀ-Ý' .,]+", t) for _, t in b):
            continue  # page number, heading, signature mark
        if NUMBER.match(b[0][1]) and not comm:
            while GLOSS.match(b[-1][1]):  # the gloss lines at the block's end; a verse
                b = b[:-1]                # line may start with a gloss mark (0402:16)
            verse.append(b)
        elif GLOSS.match(b[0][1]) and not comm:
            continue
        else:
            comm.extend(b)
    it = verse[0] if len(verse) >= 1 else []
    la = verse[1] if len(verse) >= 2 else []
    return it, la, comm


def tokens(lines, page, verse=False):
    """[(norm, form, page, line)]; a word broken by a line-end hyphen is joined."""
    out = []
    pending = None
    for i, t in lines:
        if verse:
            t = NUMBER.sub("", t, count=1)
        t = GLOSS.sub(" ", t)
        ws = [(m.group(), m.end()) for m in WORD.finditer(t)]
        for k, (w, end) in enumerate(ws):
            if pending is not None and k == 0:
                w = pending[0] + w
                line = pending[1]
                pending = None
            else:
                line = i
            if k == len(ws) - 1 and t[end:end + 1] == "-" and end + 1 == len(t):
                pending = (w, line)
                continue
            out.append((norm(w), w, page, line))
    if pending:
        out.append((norm(pending[0]), pending[0], page, pending[1]))
    return out


def lemmas(comm, verse, min_run, min_exact):
    """[(i, j, k, kinds)]: commentary comm[i:i+k] against verse[j:j+k]; kinds 0/1/2 per word."""
    index = {}
    for j, v in enumerate(verse):
        index.setdefault(v[0], []).append(j)
    found, i = [], 0
    while i < len(comm):
        best = None
        # a lemma may open with a near word: try the starts at i through exact anchors at i..i+1
        starts = set()
        for a in range(i, min(i + 2, len(comm))):
            for j in index.get(comm[a][0], ()):
                if j - (a - i) >= 0:
                    starts.add(j - (a - i))
        for j in starts:
            kinds = []
            while i + len(kinds) < len(comm) and j + len(kinds) < len(verse):
                k = near(comm[i + len(kinds)][0], verse[j + len(kinds)][0])
                if k is None:
                    break
                kinds.append(k)
            while kinds and kinds[-1]:
                kinds.pop()  # a lemma ends on an equal word
            exact = kinds.count(0)
            if len(kinds) >= min_run and exact >= min_exact and exact * 2 > len(kinds):
                if best is None or len(kinds) > len(best[2]):
                    best = (i, j, kinds)
        if best:
            found.append((best[0], best[1], len(best[2]), best[2]))
            i += len(best[2])
        else:
            i += 1
    return found


def text_line(page, line):
    return unmark((ROOT / f"{page:04d}.txt").read_text(encoding="utf-8")).split("\n")[line - 1]


def find(first, last, min_run, min_exact, decided, verbose=None):
    """The candidates of pages first..last: [(page, line, lang, form, verse page, verse line,
    verse form)]. verbose: a list that gets the lemmas found as text."""
    found = []
    for cantos in CANTOS.values():
        for start, essay, _ in cantos:
            pages = range(start, essay)
            if pages.stop <= first or pages.start > last:
                continue
            parts = {n: page_parts(n) for n in pages}
            verse = {"la": [], "it": []}
            for n in pages:
                verse["it"] += tokens(parts[n][0], n, True)
                verse["la"] += tokens(parts[n][1], n, True)
            for n in pages:
                if not first <= n <= last:
                    continue
                comm = tokens(parts[n][2], n)
                for lang in ("la", "it"):
                    v = verse[lang]
                    for i, j, k, kinds in lemmas(comm, v, min_run, min_exact):
                        if verbose is not None:
                            verbose.append(f"= {n:04d}:{comm[i][3]} {lang} "
                                           + " ".join(w[1] for w in comm[i:i + k])
                                           + f"  | {v[j][2]:04d}:{v[j][3]} "
                                           + " ".join(w[1] for w in v[j:j + k]))
                        for x, kind in enumerate(kinds):
                            c, w = comm[i + x], v[j + x]
                            if not kind or not candidate(c[0], w[0]):
                                continue
                            if any(0 <= y < len(v) and loose(v[y][0]) == loose(c[0])
                                   for y in (j + x - 1, j + x + 1)):
                                continue  # two words swapped (0133 `niger aier`)
                            if (f"{n:04d}", c[1]) in decided:
                                continue
                            found.append((n, c[3], lang, c[1], w[2], w[3], w[1]))
    return found


def tess_lines(page):
    """Tesseract's lines of a page: [[(left, top, right, bottom, text)]], the words of each
    sorted from the left, cut where two words are far apart (Tesseract sometimes reads the
    two columns as one line); a lone `|` (the column rule) is dropped."""
    words = {}
    for r in csv.DictReader(open(TESS / f"{page:04d}.tsv", encoding="utf-8"),
                            delimiter="\t", quoting=csv.QUOTE_NONE):
        t = (r["text"] or "").strip()
        if not t or t in ("|", "||"):
            continue
        x, y, w, h = (int(r[k]) for k in ("left", "top", "width", "height"))
        words.setdefault((r["block_num"], r["par_num"], r["line_num"]), []).append((x, y, x + w, y + h, t))
    out = []
    for ws in words.values():
        ws.sort()
        seg = [ws[0]]
        for w in ws[1:]:
            if w[0] - seg[-1][2] > 35:  # cut at a wide gap: the gutter (0165:26)
                out.append(seg)
                seg = []
            seg.append(w)
        out.append(seg)
    return out


def letters(t):
    return "".join(WORD.findall(t.lower()))


def likeness(text):
    """A function giving how like a run of Tesseract words is to text (0-1)."""
    t = letters(text)
    return lambda ws: difflib.SequenceMatcher(None, t, letters(" ".join(w[4] for w in ws))).ratio()


def page_layout(page, cache={}):
    """(Tesseract lines, the line numbers of the verse, the height where the verse ends or
    None). The verse ends at the lower of the last Italian and Latin lines."""
    if page not in cache:
        lines = tess_lines(page)
        it, la, _ = page_parts(page)
        ends = [max(lines, key=likeness(b[-1][1])) for b in (it, la) if b]
        end = max(max(w[3] for w in seed) for seed in ends) if ends else None
        cache[page] = (lines, {i for i, _ in it + la}, end)
    return cache[page]


def locate(page, line):
    """The box of a line of ocr/la in the page image, and the likeness (0-1) of the
    Tesseract words in it. The Tesseract line most like it gives the height, searched above
    the verse's end for a verse line and below it for the commentary (whose lemmas are like
    the verse, 0179:62). Of all the words at that height (Tesseract may split a printed
    line, 0097:65, or join the two columns, 0238:52) the run most like the line is taken."""
    lines, verse, end = page_layout(page)
    if end is not None:
        if line in verse:
            lines = [ws for ws in lines if max(w[3] for w in ws) <= end + 5]
        else:
            lines = [ws for ws in lines if min(w[1] for w in ws) >= end - 5]
    score = likeness(text_line(page, line))
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
    # a tercet number has no letters: take it in if it stands just left of the line
    k = pool.index(best[0]) if best[0] in pool else -1
    while k > 0 and not letters(pool[k - 1][4]) and best[0][0] - pool[k - 1][2] < 50:
        k -= 1
        best = [pool[k]] + list(best)
    box = (min(w[0] for w in best), min(w[1] for w in best),
           max(w[2] for w in best), max(w[3] for w in best))
    return box, value


def line_keys(found):
    """The lines to read for the candidates: both sides, and the next line of a word broken
    at the line end."""
    keys = set()
    for n, line, _, form, vp, vl, vform in found:
        for p, l, f in ((n, line, form), (vp, vl, vform)):
            keys.add((p, l))
            if text_line(p, l).endswith("-") and f not in text_line(p, l):
                keys.add((p, l + 1))
    return sorted(keys)


def write_crops(found, d, seed, min_likeness):
    """One PNG per line (L0001.png …) in a shuffled order, so that a reader sees no lemma
    beside its verse; DIR/lines.tsv maps them back (id, page, line, likeness). A line found
    with a likeness below min_likeness (a runover word, a line Tesseract misread) gets no
    image: it is listed in DIR/unlocated.tsv, to be read in the page image."""
    from PIL import Image
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    keys = line_keys(found)
    random.Random(seed).shuffle(keys)
    rows, left_out = [], []
    for p, l in keys:
        (x0, y0, x1, y1), ratio = locate(p, l)
        if ratio < min_likeness:
            left_out.append(f"{p:04d}\t{l}\t{ratio:.2f}\t{text_line(p, l)}")
            continue
        im = Image.open(ROOT / f"{p:04d}.png")
        # Tesseract often misses a tercet number: leave room for it
        left = 70 if re.match(r"\[?\d", text_line(p, l)) else 30
        c = im.crop((max(0, x0 - left), max(0, y0 - 12), min(im.width, x1 + 30), min(im.height, y1 + 12)))
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        name = f"L{len(rows) + 1:04d}"
        c.save(d / f"{name}.png")
        rows.append(f"{name}\t{p:04d}\t{l}\t{ratio:.2f}")
    (d / "lines.tsv").write_text("id\tpage\tline\tlikeness\n" + "\n".join(rows) + "\n", encoding="utf-8")
    (d / "unlocated.tsv").write_text("page\tline\tlikeness\ttext\n" + "".join(r + "\n" for r in sorted(left_out)),
                                     encoding="utf-8")
    return len(rows), len(left_out)


def read_readings(d):
    """(page, line) -> the reader's text, from DIR/lines.tsv and DIR/readings.tsv
    (`id<TAB>text`)."""
    ids = {}
    for r in csv.reader(open(Path(d, "lines.tsv"), encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
        if r and r[0] != "id":
            ids[r[0]] = (int(r[1]), int(r[2]))
    out = {}
    for l in open(Path(d, "readings.tsv"), encoding="utf-8"):
        if "\t" in l:
            k, t = l.rstrip("\n").split("\t", 1)
            if k.strip() in ids:
                out[ids[k.strip()]] = t.strip()
    return out


def word_diff(ours, theirs):
    """The words of a line that differ from the reader's: ['ours>theirs', …]."""
    a, b = WORD.findall(ours), WORD.findall(theirs)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(" ".join(a[i1:i2]) + ">" + " ".join(b[j1:j2]))
    return out


def reading_of(form, page, line, readings):
    """The reader's word at the place of form: the word of its reading of the line (and the
    next, for a broken word) aligned to form, or None if the line was not read."""
    ours, theirs = text_line(page, line), readings.get((page, line))
    if theirs is None:
        return None
    if ours.endswith("-") and (page, line + 1) in readings:
        ours = ours[:-1] + text_line(page, line + 1)
        theirs = theirs.rstrip("-") + readings[(page, line + 1)]
    a, b = WORD.findall(ours), WORD.findall(theirs)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        for x in range(i1, i2):
            if a[x] == form:
                if op == "equal":
                    return b[j1 + x - i1]
                return " ".join(b[j1:j2]) or "(none)"
    return "(not found)"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("first", type=int); ap.add_argument("last", type=int)
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    ap.add_argument("-v", "--verbose", action="store_true", help="list the lemmas found too")
    ap.add_argument("--min-run", type=int, default=3)
    ap.add_argument("--min-exact", type=int, default=2)
    ap.add_argument("--crops", metavar="DIR", help="write the line images to read (see crops())")
    ap.add_argument("--readings", metavar="DIR", help="compare a reader's DIR/readings.tsv")
    ap.add_argument("--seed", type=int, default=1, help="the shuffle of --crops")
    ap.add_argument("--min-likeness", type=float, default=0.8, help="of a line image (--crops)")
    a = ap.parse_args()
    decided = set()
    tsv = ROOT / "lemmacheck.tsv"
    if tsv.exists():
        for r in csv.reader(open(tsv, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
            if r and r[0] != "page":
                decided.add((r[0], r[2]))
    verbose = [] if a.verbose else None
    found = find(a.first, a.last, a.min_run, a.min_exact, decided, verbose)
    out = open(a.output, "w", encoding="utf-8") if a.output else sys.stdout
    if a.crops:
        n, left_out = write_crops(found, a.crops, a.seed, a.min_likeness)
        print(f"{n} line images, {left_out} unlocated, for {len(found)} candidates", file=out)
        return
    readings = read_readings(a.readings) if a.readings else None
    for l in verbose or []:
        print(l, file=out)
    for n, line, lang, form, vp, vl, vform in found:
        head = f"{n:04d}:{line} {lang} {form} | {vp:04d}:{vl} {vform}"
        if readings is not None:
            rc, rv = reading_of(form, n, line, readings), reading_of(vform, vp, vl, readings)
            same = rc == form and rv == vform
            head += f"  [read: {rc} | {rv}]" + ("" if same else "  DIFFERS")
        print(head, file=out)
        for tag, p, l in (("c", n, line), ("v", vp, vl)):
            print(f"    {tag}: {text_line(p, l)}", file=out)
            if readings is not None and (p, l) in readings:
                d = word_diff(text_line(p, l), readings[(p, l)])
                if d:
                    print(f"    {tag}> {readings[(p, l)]}   ({'; '.join(d)})", file=out)
    print(f"{len(found)} candidates", file=out)
    if a.output:
        out.close()


if __name__ == "__main__":
    main()
