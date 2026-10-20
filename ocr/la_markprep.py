"""Prepare the marked pages of la_markup.py for the image decisions, without any LLM call.

    la_markprep.py WORK PAGE... -t TESSDIR

WORK/markup/PAGE.txt are the pages marked by `la_markup.py -o WORK/markup` ({{ocr|glm}}).
TESSDIR/PAGE.tsv is Tesseract's word list of ocr/la/PAGE.png (`ocr/la/tesseract/`, made
by its Makefile: block_num, par_num, line_num, left, top, width, height, text).

1. Trivial marks are resolved to their left side (the ocr/la reading), without the image:
   - head:      A only, a whole line on lines 1-3: page number, running head;
   - number:    tercet numbers at the start of a verse line, A only or against the same
                number with a dot (`1` / `1.`), on a page whose numbers are in order;
   - signature: A only, the digits of the last line, when the page 8 before or after ends
                with the number before or after it;
   - google:    B only `Digitized by Google`;
   - spacing:   equal but for spaces next to an apostrophe, spaces after punctuation, and
                a line-end hyphen of the left (against a hyphen, a space or nothing); a space
                between two words (`quanto lor` / `quantolor`) is not ignored;
   - quote:     as spacing, with `’` read as `'`;
   - note:      as quote, with `(¹)` read as `(1)`;
   - moved:     an A-only and a B-only mark of the page with the same text.
   Written to WORK/post/PAGE.txt; WORK/post.log lists them.

2. The other marks are located in the image by Tesseract's word boxes: the words of the
   ocr/la text around a mark vote for its place (near words weigh more, the mark's own words
   little), the context widened (6, 15, 30 words) while the place is not clear; an ambiguous
   place is settled by the order of the located marks around it, or by the only Tesseract
   word like the mark's word. The crop is the printed line(s) with their neighbours, at the
   scan's own resolution (WORK/crops/PAGE-LINE-K.png; WORK/locate.tsv).

3. WORK/ask.txt lists the marks for la_markdecide.py: located, two-sided, and not decided by
   rule later (`:`/`;` and `.`/`,` differences are not asked)."""

import argparse
import collections
import difflib
import re
import statistics
import sys
import unicodedata
from pathlib import Path

from PIL import Image

import la_markup as M

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
HEAD = re.compile(r"[A-Z ]+|\d+")
APOS, PUNCT = "'’", ",.;:!?"
NUM = re.compile(r"^([0-9]+\.?|[⁰¹²³⁴⁵⁶⁷⁸⁹]+) +(?=\S)")
CTXS = (6, 15, 30)  # context words on each side, widened while not located
GAP = 50  # pixels: a wider gap between words of a row is a column gap


# ---- classes of marks (also used by la_markresolve.py) ----

def letters(s):
    s = unicodedata.normalize("NFD", s.replace("æ", "ae").replace("œ", "oe"))
    return re.sub(r"[^a-z]+", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def klass(l, r):
    """onesided, letters, colon (`:`/`;` only), comma (`.`/`,` only) or punct."""
    if not l.strip() or not r.strip(): return "onesided"
    if letters(l) != letters(r): return "letters"
    x, y = re.sub(r"[\w\s'’]", "", l), re.sub(r"[\w\s'’]", "", r)
    if sorted(x.replace(";", ":")) == sorted(y.replace(";", ":")) and x != y: return "colon"
    if sorted(x.replace(",", ".")) == sorted(y.replace(",", ".")) and x != y: return "comma"
    return "punct"


def passage_mark(l, r):
    """A run of text found in A only over a line or more than 8 words (a dropped passage)."""
    return not r and ("\n" in l or len(l.split()) > 8)


def tess_words(path):
    """Tesseract's words: text, normalized text, box, and the id of its printed line."""
    out = []
    for row in open(path, encoding="utf-8").read().splitlines()[1:]:
        f = row.split("\t")
        if len(f) < 8 or not f[7].strip(): continue
        x, y, w, h = map(int, f[3:7])
        out.append(dict(text=f[7], n=norm(f[7]), box=(x, y, x + w, y + h),
                        line=tuple(map(int, f[0:3]))))
    return out


# ---- step 1: trivial marks ----

def quote(s): return s.replace("’", "'")
def note(s): return re.sub(r"\(([⁰-⁹¹²³]+)\)", lambda m: f"({m.group(1).translate(SUP)})", s)


def pattern(l):
    """A regex for the right sides that differ from `l` only in the allowed spacing."""
    out, i = [], 0
    while i < len(l):
        c = l[i]
        if c == "-" and l[i + 1:i + 2] == "\n" and i and l[i - 1].isalnum():
            out.append(r"-?\s*"); i += 2; continue
        if c.isspace():
            j = i
            while j < len(l) and l[j].isspace(): j += 1
            prev, nxt = l[i - 1] if i else "", l[j] if j < len(l) else ""
            free = prev in APOS + PUNCT and prev or nxt in APOS and nxt
            out.append(r"\s*" if free else r"\s+"); i = j; continue
        if out and i and (l[i - 1] in APOS + PUNCT or c in APOS) and not l[i - 1].isspace():
            out.append(r"\s*")
        out.append(re.escape(c)); i += 1
    return "".join(out)


def same(l, r): return re.fullmatch(pattern(l), r) is not None


def spacing_rule(l, r):
    if same(l, r): return "spacing"
    if same(quote(l), quote(r)): return "quote"
    if same(note(quote(l)), note(quote(r))): return "note"
    return None


def key(s): return re.sub(r"\s+", " ", note(quote(re.sub(r"(?<=\w)-\n", "", s)))).strip()


def verse_blocks(text):
    """The first two verse blocks of a page, as lists of (line number, line)."""
    lines, start, blocks = text.split("\n"), 0, []
    for i in range(len(lines) + 1):
        if i == len(lines) or not lines[i].strip():
            b = lines[start:i]
            if b and sum(1 for x in b if NUM.match(x)) >= 1 and len(b) >= 2 \
                    and sum(len(x) for x in b) / len(b) < 75 and not b[0].startswith("("):
                blocks.append(list(zip(range(start + 1, i + 1), b)))
            start = i + 1
    return blocks[:2]


def numbers_in_order(block):
    """Whether the tercet numbers of a verse block stand every third verse line (runover
    lines `[…` not counted) and rise by one."""
    lines = [x for _, x in block if not x.startswith("[")]
    nums = [(i, int(NUM.match(x)[1].translate(SUP).rstrip("."))) for i, x in enumerate(lines) if NUM.match(x)]
    if not nums: return True
    off = nums[0][0] % 3
    return all(i % 3 == off for i, _ in nums) and \
        all(b == a + 1 and j - i == 3 for (i, a), (j, b) in zip(nums, nums[1:]))


def last_number(p):
    f = Path(f"{M.ROOT}/{p:04}.txt")
    if not f.exists(): return None
    rest = [x for x in f.read_text(encoding="utf-8").split("\n") if x.strip()]
    return int(rest[-1]) if rest and rest[-1].strip().isdecimal() else None


def resolve_trivial(p, t):
    """The page with the trivial marks resolved, and (line, rule, left, right) of each."""
    plain = (M.ROOT / f"{p}.txt").read_text(encoding="utf-8")
    # la_markup.py ends a page with one newline; keep the ending of ocr/la instead
    t = t.rstrip("\n") + plain[len(plain.rstrip("\n")):]
    marks = list(M.MARK.finditer(t))
    assert M.MARK.sub(lambda m: m.group(1), t) == plain, f"{p}: the marks do not give ocr/la"
    blocks = verse_blocks(plain)
    verse = {n for b in blocks if numbers_in_order(b) for n, _ in b}
    nlines = len(plain.rstrip("\n").split("\n"))
    digits = re.compile(r"[\d⁰¹²³⁴⁵⁶⁷⁸⁹]+")
    why = {}
    for k, m in enumerate(marks):
        l, r = m.groups()
        ls = t.rfind("\n", 0, m.start()) + 1
        le = t.find("\n", m.end()); le = len(t) if le < 0 else le
        line = M.mark_line(t, m)
        whole = m.start() == ls and m.end() == le
        if not r and "\n" not in l and whole and line <= 3 and HEAD.fullmatch(l):
            why[k] = "head"
        elif m.start() == ls and digits.fullmatch(l) and line in verse and \
                (not r or r == l.translate(SUP) + "."):
            why[k] = "number"
        elif not r and whole and line == nlines and l.isdecimal() and \
                (last_number(int(p) - 8) == int(l) - 1 or last_number(int(p) + 8) == int(l) + 1):
            why[k] = "signature"
        elif not l and r.strip() == "Digitized by Google":
            why[k] = "google"
        elif l and r and (w := spacing_rule(l, r)):
            why[k] = w
    aonly = [k for k, m in enumerate(marks) if k not in why and not m.group(2)]
    for k, m in enumerate(marks):
        if k in why or m.group(1) or not m.group(2): continue
        for j in aonly:
            if j not in why and key(marks[j].group(1)) == key(m.group(2)):
                why[j] = why[k] = "moved"; break
    out, pos = "", 0
    for k, m in enumerate(marks):
        out += t[pos:m.start()] + (m.group(1) if k in why else m.group(0)); pos = m.end()
    out += t[pos:]
    log = [(M.mark_line(t, marks[k]), w, *marks[k].groups()) for k, w in sorted(why.items())]
    return out, log


# ---- step 2: locating ----

def norm(w): return re.sub(r"\W", "", w.translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹ęſ", "0123456789es")).lower())
def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0
def words(s): return [norm(w) for w in re.findall(r"\S+", s)]


def page_marks(t):
    """The ocr/la text (left sides) and the marks as (start, end, match) spans in it."""
    text, spans, pos = "", [], 0
    for m in M.MARK.finditer(t):
        text += t[pos:m.start()]; s = len(text); text += m.group(1)
        spans.append((s, len(text), m)); pos = m.end()
    return text + t[pos:], spans


def vote(before, inside, after, index):
    """Peaks of the votes for the Tesseract index of the mark start, best first, and the
    votes needed."""
    anchors = [(w, i - len(before), len(before) - i) for i, w in enumerate(before)]
    anchors += [(w, i, 0) for i, w in enumerate(inside)]
    anchors += [(w, len(inside) + i, i + 1) for i, w in enumerate(after)]
    anchors = [a for a in anchors if len(a[0]) >= 3 or a[0].isdigit()]
    # Tesseract reads the Italian and Latin verse columns row by row, so far words of a
    # verse block stand elsewhere in its order; the mark's left side may be a wrong
    # reading copied from elsewhere on the page (a gloss repeating its verse line)
    weight = {d: 1 / (1 + d / 3) if d else 0.3 for _, _, d in anchors}
    votes = collections.Counter()
    for w, o, d in anchors:
        for t in index.get(w, ()):
            for k in range(-2, 3): votes[t - o + k] += weight[d] * (3 - abs(k)) / 3
    peaks = []
    for p, v in votes.most_common():
        if all(abs(p - q) > 8 for q, _ in peaks): peaks.append((p, v))
    need = max(2, 0.35 * sum(weight[d] for _, _, d in anchors))
    return peaks, need


def refine(p, before, inside, tw):
    """The exact index near p: the word most like the mark's first word, or for an empty
    left side the gap after the word most like the word before it."""
    def score(i):
        if inside and inside[0]:
            return sim(inside[0], tw[i]["n"]) + 0.5 * sim(before[-1] if before else "",
                                                          tw[i - 1]["n"] if i else "")
        return sim(before[-1] if before else "", tw[i - 1]["n"] if i else "")
    p = min(max(p, 0), len(tw) - 1)  # a peak can fall outside the words
    cand = range(max(0, p - 3), min(len(tw), p + 4))
    return max(cand, key=lambda i: (score(i), -abs(i - p)))


def split(text, s, e):
    """The words of the text before, in and after the span [s, e). The words the span
    overlaps count as in it (`Deum{{,|.}}`, `Methaph{{y|i}}-`); an empty span inside a
    word takes that word."""
    toks = [(m.start(), m.end(), norm(m.group())) for m in re.finditer(r"\S+", text)]
    if e > s: inn = [i for i, (a, b, _) in enumerate(toks) if a < e and b > s]
    else: inn = [i for i, (a, b, _) in enumerate(toks) if a < s < b]
    if inn: i0, i1 = inn[0], inn[-1] + 1
    else: i0 = i1 = sum(1 for a, _, _ in toks if a < s)
    w = [t[2] for t in toks]
    return w[:i0], w[i0:i1], w[i1:]


def locate(text, s, e, tw, index):
    """(index, votes, status, other candidates) of the span [s, e) of the text."""
    B, I, A = split(text, s, e)
    for c in CTXS:
        before, inside, after = B[-c:], I, A[:c]
        peaks, need = vote(before, inside, after, index)
        if not peaks: continue
        (best, v), rival = peaks[0], peaks[1][1] if len(peaks) > 1 else 0
        status = "unlocated" if v < need else "ambiguous" if rival > v * 0.6 else "located"
        if status == "located": break
    if not peaks: return None, 0, "unlocated", []
    cands = [refine(p, before, inside, tw) for p, q in peaks if q > v * 0.6]
    return refine(best, before, inside, tw), round(v, 1), status, cands


def by_word(l, tw):
    """The only Tesseract index whose word is like the mark's longest word, or None."""
    w = max(words(l), key=len, default="")
    if len(w) < 4: return None
    hits = [i for i, x in enumerate(tw) if sim(w, x["n"]) >= 0.8]
    return hits[0] if len(hits) == 1 else None


def align(x, y):
    """Fuzzy longest common subsequence of two word lists: the matched (i, j) pairs."""
    n, m = len(x), len(y)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            L[i][j] = max(L[i + 1][j], L[i][j + 1],
                          L[i + 1][j + 1] + 1 if sim(x[i], y[j]) >= 0.6 else 0)
    out, i, j = [], 0, 0
    while i < n and j < m:
        if sim(x[i], y[j]) >= 0.6 and L[i][j] == L[i + 1][j + 1] + 1: out.append((i, j)); i += 1; j += 1
        elif L[i + 1][j] >= L[i][j + 1]: i += 1
        else: j += 1
    return out


def verified(i, text, s, e, tw):
    """Whether the printed line of Tesseract word i aligns with the text around the span
    across the span's place. On verse rows Tesseract joins the Italian and Latin columns and
    the check fails on right places, so it only flags (`unverified`), it moves nothing."""
    line = [k for k, w in enumerate(tw) if w["line"] == tw[i]["line"]]
    T = [tw[k]["n"] for k in line]
    B, I, A = split(text, s, e)
    K = len(T) + 3
    W = B[-K:] + I + A[:K]; a0 = len(B[-K:]); a1 = a0 + len(I)
    pairs = [(wi, ti) for wi, ti in align(W, T) if W[wi]]
    if len(pairs) < 2: return False
    ws = [wi for wi, _ in pairs]
    at = next((line[ti] for wi, ti in pairs if a0 <= wi < max(a1, a0 + 1)), None)
    if I: return at is not None or (min(ws) < a0 and max(ws) >= a1)
    return min(ws) <= a0 and max(ws) >= a0 - 1


def crop(im, tw, a, b, out):
    """Crop the printed lines of Tesseract words a..b, with the neighbouring lines."""
    a, b = max(0, min(a, b)), min(len(tw) - 1, max(a, b))
    lines = {tw[i]["line"] for i in range(a, b + 1)}
    boxes = [w["box"] for w in tw if w["line"] in lines]
    x0, y0 = min(x[0] for x in boxes), min(x[1] for x in boxes)
    x1, y1 = max(x[2] for x in boxes), max(x[3] for x in boxes)
    lh = statistics.median(x[3] - x[1] for x in boxes)
    # Tesseract may cut a printed line into pieces: widen along the row while the next
    # word is nearer than a column gap (this also keeps a tercet number at the left)
    row = sorted((w["box"] for w in tw
                  if y0 - 0.4 * lh <= (w["box"][1] + w["box"][3]) / 2 <= y1 + 0.4 * lh),
                 key=lambda b: b[0])
    for b in reversed(row):
        if b[2] <= x0 and x0 - b[2] < GAP: x0 = min(x0, b[0])
    for b in row:
        if b[0] >= x1 and b[0] - x1 < GAP: x1 = max(x1, b[2])
    # 60 pixels at the sides: a tercet number Tesseract missed stands just left of a verse
    im.crop((max(0, x0 - 60), max(0, int(y0 - 1.6 * lh)), min(im.width, x1 + 60),
             min(im.height, int(y1 + 1.6 * lh)))).save(out)
    return x0, y0, x1, y1


def locate_page(p, t, tw, cropdir):
    """The rows of locate.tsv for the marks of the page t."""
    text, spans = page_marks(t)
    index = collections.defaultdict(list)
    for i, w in enumerate(tw): index[w["n"]].append(i)
    im = Image.open(M.ROOT / f"{p}.png")
    res, allends = [], []
    for s, e, m in spans:
        l = m.group(1)
        if "\n" in l:  # first and last line of a passage
            ends = [(s, s + l.index("\n")), (e - len(l.split("\n")[-1]), e)]
        else:
            ends = [(s, e)]
        res.append([locate(text, x, y, tw, index) for x, y in ends]); allends.append(ends)
    # order: an ambiguous end takes the candidate between the located neighbours
    for k, found in enumerate(res):
        for j, f in enumerate(found):
            if f[2] != "ambiguous": continue
            lo = max((g[0] for r in res[:k] for g in r if g[2] == "located"), default=-1)
            hi = min((g[0] for r in res[k + 1:] for g in r if g[2] == "located"), default=len(tw))
            ok = [c for c in f[3] if lo <= c <= hi]
            if len(ok) == 1: found[j] = (ok[0], f[1], "order", f[3])
    rows = []
    for k, ((s, e, m), found, ends) in enumerate(zip(spans, res, allends)):
        l, r = m.groups(); line = text[:s].count("\n") + 1
        if len(found) == 1 and found[0][2] in ("ambiguous", "unlocated") and (i := by_word(l, tw)) is not None:
            found = [(i, found[0][1], "word", [])]
        order = ["unlocated", "ambiguous", "word", "order", "located"]
        status = min((f[2] for f in found), key=order.index)
        box, near, how, png = "", "", "", ""
        if status not in ("unlocated", "ambiguous"):
            how = "ok" if all(verified(f[0], text, x, y, tw) for f, (x, y) in zip(found, ends)) else "unverified"
            last = ends[-1] if "\n" in l else (s, e)
            n = len(split(text, *last)[1])
            i0, i1 = found[0][0], found[-1][0] + max(n, 1) - 1
            if not n: i0 -= 1  # a gap: show the word before it too
            png = f"{p}-{line:03}-{k}.png"
            box = crop(im, tw, i0, i1, cropdir / png)
            near = " ".join(w["text"] for w in tw[max(0, i0 - 2):i1 + 3])[:200]
        rows.append([p, str(line), status, how, "/".join(str(f[1]) for f in found),
                     ",".join(map(str, box)), l.replace("\n", "⏎")[:60], r.replace("\n", "⏎")[:60], near, png])
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("work", type=Path, help="the work directory (WORK/markup from la_markup.py)")
    ap.add_argument("pages", nargs="+", help="page numbers, e.g. 0195 0196")
    ap.add_argument("-t", "--tessdir", required=True, type=Path, help="Tesseract's PAGE.tsv files")
    a = ap.parse_args()
    for d in ("post", "crops"): (a.work / d).mkdir(parents=True, exist_ok=True)
    pages = [f"{int(p):04d}" for p in a.pages]
    log, total = [], collections.Counter()
    loc = ["page\tline\tstatus\tcheck\tvotes\tbox\tleft\tright\ttess\tcrop"]
    ask, status = [], collections.Counter()
    for p in pages:
        t = (a.work / "markup" / f"{p}.txt").read_text(encoding="utf-8")
        post, done = resolve_trivial(p, t)
        (a.work / "post" / f"{p}.txt").write_text(post, encoding="utf-8")
        for line, w, l, r in done:
            total[w] += 1
            log.append(f"{p}:{line}\t{w}\t{l.replace(chr(10), '⏎')[:50]!r}|{r[:50]!r}")
        log.append(f"{p}: {len(done)} of {len(M.MARK.findall(t))} resolved")
        rows = locate_page(p, post, tess_words(a.tessdir / f"{p}.tsv"), a.work / "crops")
        marks = list(M.MARK.finditer(post))
        for row, m in zip(rows, marks):
            loc.append("\t".join(row)); status[row[2]] += 1
            l, r = m.groups()
            if row[9] and klass(l, r) not in ("colon", "comma", "onesided") and not passage_mark(l, r):
                ask.append(row[9][:-4])
    head = [f"{w}: {n}" for w, n in total.most_common()] + [f"total: {sum(total.values())}"]
    (a.work / "post.log").write_text("\n".join(head + [""] + log) + "\n", encoding="utf-8")
    (a.work / "locate.tsv").write_text("\n".join(loc) + "\n", encoding="utf-8")
    (a.work / "ask.txt").write_text("\n".join(ask) + "\n", encoding="utf-8")
    print(f"resolved {sum(total.values())} ({', '.join(head[:-1])}); left {len(loc) - 1}: "
          + ", ".join(f"{s} {n}" for s, n in status.most_common()) + f"; to ask {len(ask)}")


if __name__ == "__main__":
    main()
