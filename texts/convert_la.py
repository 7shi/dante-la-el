"""Convert ocr/la/NNNN.txt (Serravalle's translation and commentary, 1891) into texts/la/NNN-title.md.

Only Inferno I–XIII (scans 0079–0232) are converted so far: the rest of ocr/la is not yet
completed (see ocr/la/PLAN.md). See PLAN.md for the layout. Run from the repository root:

    uv run texts/convert_la.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ocr" / "la"
DST = ROOT / "texts" / "la"

# Verses per canto in the Inferno.
VERSES = [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136, 136,
          136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139, 157, 139]

# Cantos converted: (first scan, the scan of the essay, last scan), from INDEX.md.
CANTOS = [(79, 92, 92), (93, 102, 102), (103, 114, 114), (115, 127, 128), (129, 139, 140),
          (141, 150, 150), (151, 161, 162), (163, 171, 172), (173, 183, 184), (185, 196, 196),
          (197, 206, 206), (207, 220, 220), (221, 232, 232)]
FIRST_FILE = 8  # 008-inferno-canto-01.md (001–007 are the front matter, not converted yet)
OFFSET = 54  # printed page = scan - 54

ORDINALS = ["PRIMUM", "SECUNDUM", "TERTIUM", "QUARTUM", "QUINTUM", "SEXTUM", "SEPTIMUM",
            "OCTAVUM", "NONUM", "DECIMUM", "UNDECIMUM", "DUODECIMUM", "TERTIUMDECIMUM"]
GENITIVES = ["PRIMI", "SECUNDI", "TERTII", "QUARTI", "QUINTI", "SEXTI", "SEPTIMI", "OCTAVI",
             "NONI", "DECIMI", "UNDECIMI", "DUODECIMI", "TERTIIDECIMI"]

# The essays' titles as printed, in the case of INDEX.md (where it reads `angeli`, the print
# has `ANGIOLI`).
ESSAYS = {
    "LA DIVINA COMMEDIA": "La divina commedia",
    "ROMA NEL CONCETTO DI DANTE": "Roma nel concetto di Dante",
    "L'INFERNO E L'AMOR DIVINO": "L'inferno e l'amor divino",
    "LA FEDE DI DANTE": "La fede di Dante",
    "MINOSSE E LA REA COSCIENZA NELL' ETERNITÀ": "Minosse e la rea coscienza nell'eternità",
    "LA RISURREZIONE DEI CORPI": "La risurrezione dei corpi",
    "IL PECCATO DEGLI ANGIOLI": "Il peccato degli angioli",
    "IL SIMBOLISMO NELLE VISIONI": "Il simbolismo nelle visioni",
    "GLI ANGIOLI BUONI E CATTIVI": "Gli angioli buoni e cattivi",
    "LA SELVA IN CUI SI SMARRÌ L'ALIGHIERI": "La selva in cui si smarrì l'Alighieri",
    "L'ARTE DIVINA E L'ARTE UMANA": "L'arte divina e l'arte umana",
    "I PRODIGI NELLA MORTE DI CRISTO": "I prodigi nella morte di Cristo",
    "FEDERICO II.": "Federico II",
}

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
TO_SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
NUMBER = re.compile(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+|\d+) ")  # a tercet number at the start of a verse line
GLOSS = re.compile(r"\((?:[¹²³⁴⁵⁶⁷⁸⁹]|\d)\)")  # `(¹) costui. — (²) sarà.`


def text_of(n):
    return (SRC / f"{n:04d}.txt").read_text(encoding="utf-8").replace("’", "'")


def marker(n, printed=True):
    p = n - OFFSET
    return f"<!-- p. {p if printed else f'[{p}]'} ({n:04d}) -->"


def blocks(lines):
    """The blank-separated blocks of lines."""
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def esc(line):
    """Keep a line from being read as Markdown list or heading syntax."""
    line = re.sub(r"^(\d+)\. ", r"\1\\. ", line)
    return re.sub(r"^([-+*#>]) ", r"\\\1 ", line)


# ---------------------------------------------------------------- hyphenation

WORD = r"[^\W\d_]+"
VOCAB = set()
for f in SRC.glob("[0-9][0-9][0-9][0-9].txt"):
    t = f.read_text(encoding="utf-8").replace("’", "'")
    # the fragments of words hyphenated at a line end are not words
    t = re.sub(WORD + r"-\n\s*" + WORD, " ", t)
    VOCAB.update(w.lower() for w in re.findall(WORD + r"(?:-" + WORD + r")*", t))
UNDECIDED = []

# Line-end hyphens decided by hand: the word as it is to be written.
HYPHEN_FIXED = {}


def join_hyphen(head, tail, where):
    m1 = re.search(r"(" + WORD + r")-$", head)
    m2 = re.match(r"\W*?(" + WORD + r")", tail)
    if not m1 or not m2:
        return head + tail
    a, b = m1.group(1), m2.group(1)
    key = f"{a}-{b}".lower()
    if key in HYPHEN_FIXED:
        sep = "-" if "-" in HYPHEN_FIXED[key] else ""
    elif (a + b).lower() in VOCAB:
        sep = ""  # the unbroken form wins: hyphens inside a line of unchecked pages are breaks
    elif key in VOCAB:
        sep = "-"
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}-{b}")
    else:
        sep = ""
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}{b}")
    return head[:-1] + sep + tail


def join_lines(lines, where):
    """Join printed lines into one line."""
    text = lines[0]
    for l in lines[1:]:
        if re.search(WORD + "-$", text):
            text = join_hyphen(text, l, where)
        else:
            text += " " + l
    return text


# ---------------------------------------------------------------- pages

def read_page(n, errors):
    """(head, lines): the running head or heading removed, the signature mark at the foot
    removed. head is (printed page number or None, the heading/running head or None)."""
    lines = text_of(n).rstrip("\n").split("\n")
    number = None
    if re.fullmatch(r"\d+", lines[0]):
        number = int(lines[0])
        if number != n - OFFSET:
            errors.append(f"{n:04d}: page number {number}")
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    title = None
    if lines and re.fullmatch(r"[A-ZÀ-Ý' .]+", lines[0].strip()) and len(lines[0]) > 4:
        title = lines.pop(0).strip()
    # signature mark: a number alone at the foot, after a blank line
    if len(lines) > 2 and re.fullmatch(r"\d+", lines[-1].strip()) and not lines[-2].strip():
        lines = lines[:-2]
    return number, title, lines


def split_verse(n, bs, errors):
    """The verse at the top of a page: (italian, latin, glosses, rest)."""
    it, la, gl = [], [], []
    k = 0
    for part in ("it", "la"):
        if k < len(bs) and NUMBER.match(bs[k][0]):
            b = bs[k]  # a gloss line may follow the verse without a blank line
            e = len(b)
            while e > 1 and GLOSS.match(b[e - 1]):
                e -= 1
            (it if part == "it" else la).extend(b[:e])
            gl.extend(b[e:])
            k += 1
        while k < len(bs) and GLOSS.match(bs[k][0]):
            gl.extend(bs[k])
            k += 1
    if bool(it) != bool(la):
        errors.append(f"{n:04d}: one verse column only")
    return it, la, gl, bs[k:]


def tercets(lines, n, where):
    """Group verse lines into tercets: [(printed number or None, [lines])]. A line opened by
    `[` is the end of the line above, set on a line of its own (`[togle.`)."""
    out = []
    for l in lines:
        if l.startswith("[") and len(l.split()) <= 2 and not l.endswith("]") and out:
            out[-1][1][-1] = join_lines([out[-1][1][-1], l[1:]], f"{n:04d}")
            RUNOVER.append(f"{n:04d} {where}: {out[-1][1][-1][-40:]}")
            continue
        m = NUMBER.match(l)
        if m:
            out.append((int(m.group(1).translate(SUP)), [l[m.end():]]))
        elif out and len(out[-1][1]) < 3:
            out[-1][1].append(l)
        else:
            out.append((None, [l]))  # an unnumbered tercet (the print omits the number)
    return out


RUNOVER = []


def column_width(lines):
    """The length of a full line: the 90th percentile, not swayed by a long gloss line."""
    ls = sorted(len(l) for l in lines)
    return ls[int(len(ls) * 0.9)] if ls else 60


def paragraphs(lines, width):
    """Split a block of commentary lines into printed paragraphs: a line that ends a
    sentence and falls short of the column width ends its paragraph."""
    out, cur = [], []
    for l in lines:
        cur.append(l)
        if re.search(r"[.?!:]$", l) and len(l) < width - 8:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def convert_canto(c, errors):
    first, essay, last = CANTOS[c - 1]
    parts = []
    verse = {"it": [], "la": []}  # (page, printed number, lines)
    carry = None  # the commentary paragraph open at the end of the previous page
    for n in range(first, last + 1):
        text = text_of(n)
        if text.strip() == "[Blank page]":
            continue
        number, title, lines = read_page(n, errors)
        parts.append(marker(n, number is not None))
        if title:
            if n == first:
                want = f"CAPITULI {GENITIVES[c - 1]} SUMMARIUM"
            elif n >= essay:
                want = title if title in ESSAYS or number else None
            elif number is None:
                want = f"CAPITULUM {ORDINALS[c - 1]}"
            else:
                want = title  # the running head (also on an essay's second page)
            if want != title:
                errors.append(f"{n:04d}: heading {title!r}")
            if n >= essay and title != "INFERNI":
                parts.append(f"# {ESSAYS.get(title, title)}")
            elif number is None:
                parts.append("# " + " ".join(w.capitalize() for w in title.split()))
            elif title not in ("INFERNI", f"CAPITULUM {ORDINALS[c - 1]}"):
                errors.append(f"{n:04d}: running head {title!r}")
        bs = blocks(lines)
        if n >= essay:
            width = column_width([l for b in bs for l in b])
            for b in bs:
                if width > 120 and any(len(l) > 80 for l in b):
                    # paragraphs on one line each; a paragraph broken at a column change
                    # (no sentence end) is joined
                    cur = []
                    for l in b:
                        cur.append(l)
                        if re.search(r"[.?!:;»)]$", l):
                            parts.append(esc(join_lines(cur, f"{n:04d}")))
                            cur = []
                    if cur:
                        parts.append(esc(join_lines(cur, f"{n:04d}")))
                elif len(b) > 1 and all(len(l) < width * 0.75 and not l.endswith("-") for l in b):
                    parts.append("\\\n".join(esc(l) for l in b))  # verse quoted in the essay
                else:  # printed lines
                    parts.extend(esc(join_lines(p, f"{n:04d}")) for p in paragraphs(b, width))
            continue
        it, la, gl, rest = split_verse(n, bs, errors)
        if it:
            ti, tl = tercets(it, n, "it"), tercets(la, n, "la")
            if [len(t[1]) for t in ti] != [len(t[1]) for t in tl]:
                errors.append(f"{n:04d}: the columns differ: {[len(t[1]) for t in ti]}"
                              f" / {[len(t[1]) for t in tl]}")
            for (ni, li), (nl, ll) in zip(ti, tl):
                if ni is None and len(li) == 1 and len(ll) == 1 and verse["it"]:
                    # the canto's last line, set alone after the last tercet
                    if parts[-1].startswith("<!--"):
                        errors.append(f"{n:04d}: the last line on a page of its own")
                    verse["it"][-1][2].extend(li)
                    verse["la"][-1][2].extend(ll)
                    parts[-2] += "\\\n&emsp;" + esc(li[0])
                    parts[-1] += "\\\n&emsp;" + esc(ll[0])
                    continue
                k = len(verse["it"]) + 1
                verse["it"].append((n, ni, li))
                verse["la"].append((n, nl, ll))
                for lines_ in (li, ll):
                    parts.append(f"{str(k).translate(TO_SUP)} " + "\\\n&emsp;".join(esc(l) for l in lines_))
            if gl:
                parts.append(esc(join_lines(gl, f"{n:04d}")))
        body = [l for b in rest for l in b]
        width = column_width(body)
        for bi, b in enumerate(rest):
            ps = paragraphs(b, width)
            for pi, p in enumerate(ps):
                if carry is not None and bi == 0 and pi == 0:
                    # a word hyphenated across the page break is joined on the earlier page
                    head = parts[carry]
                    if re.search(WORD + "-$", head):
                        m = re.match(r"(\S+)\s*(.*)", p[0])
                        parts[carry] = join_hyphen(head, m.group(1), f"{n:04d}")
                        p = [m.group(2)] + p[1:] if m.group(2) else p[1:]
                        if not p:
                            continue
                parts.append(esc(join_lines(p, f"{n:04d}")))
        last_line = body[-1] if body else ""
        carry = len(parts) - 1 if body and re.search(WORD + "-$", last_line) else None
    # tercet numbers: computed by counting, checked against the printed ones
    for lang in ("it", "la"):
        lines = sum(len(t[2]) for t in verse[lang])
        if lines != VERSES[c - 1]:
            errors.append(f"canto {c} {lang}: {lines} lines, expected {VERSES[c - 1]}")
        for k, (n, num, _) in enumerate(verse[lang], 1):
            if num is not None and num != k:
                errors.append(f"{n:04d} {lang}: printed number {num} at tercet {k}")
            if num is None:
                MISSING_NUMBER.append(f"{n:04d} {lang}: tercet {k}")
    return parts


MISSING_NUMBER = []


def main():
    DST.mkdir(parents=True, exist_ok=True)
    errors = []
    for c in range(1, len(CANTOS) + 1):
        parts = convert_canto(c, errors)
        path = DST / f"{FIRST_FILE + c - 1:03d}-inferno-canto-{c:02d}.md"
        path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    for e in errors:
        print("ERROR", e)
    for x in MISSING_NUMBER:
        print("NO NUMBER", x)
    for x in RUNOVER:
        print("RUNOVER", x)
    for u in dict.fromkeys(UNDECIDED):
        print("HYPHEN", u)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
