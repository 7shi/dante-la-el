"""Convert ocr/en-oelsner/NNN.txt (Temple Classics edition, 1903) into texts/en-oelsner/NNN-title.md.

See PLAN.md for the layout. Run from the repository root:

    uv run texts/convert_en_oelsner.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ocr" / "en-oelsner"
DST = ROOT / "texts" / "en-oelsner"

# Verses per canto in the Inferno.
VERSES = [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136, 136,
          136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139, 157, 139]

# Canto n (1-based): first page (Argument), last page (notes or plate).
CANTO_PAGES = [(14, 25), (26, 37), (38, 47), (48, 59), (60, 71), (72, 81), (82, 91), (92, 101),
               (102, 111), (112, 123), (124, 133), (134, 145), (146, 157), (158, 169),
               (170, 179), (180, 191), (192, 201), (202, 213), (214, 225), (226, 237),
               (238, 249), (250, 261), (262, 273), (274, 285), (286, 297), (298, 309),
               (310, 321), (322, 333), (334, 345), (346, 357), (358, 369), (370, 381),
               (382, 393), (394, 402)]

# Full-page maps, plates and tables printed after a canto's notes.
PLATES = {25, 37, 133, 191, 249, 321, 345}

# The leaf with pp. 385-386 is missing between these scans: p. 385 (English of
# vv. 19-51 of Canto XXXIV) and p. 386 (Italian of vv. 52-84).
MISSING_AFTER = 396
MISSING_VERSES = range(52, 85)

FRONT = ("title-page", [7, 8, 10, 11, 13])
BACK = [
    ("note-on-dantes-hell", [403, 404, 405]),
    ("the-chronology-of-the-inferno", [406, 407, 408]),
    ("plan-of-concentric-spheres", [409]),
    ("section-of-the-universe", [410]),
    ("editorial-note", [411]),
    ("index-to-maps-plates-and-tables", [412]),
]

ROMAN = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
         (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]

# A note starts with the verse numbers it explains: `1.`, `2-3.`, `69, 70.`, `107, 8.`
NOTE_START = re.compile(r"(\d+(?:[-–,] ?\d+)*\.|\* ?\* ?\*) ")
LABEL = re.compile(r"\*\*([^*]+)\*\* ?")


def roman(n):
    s = ""
    for v, r in ROMAN:
        while n >= v:
            s += r
            n -= v
    return s


def page_no(n):
    if n == 13:
        return "[1]"  # the epigraph
    if n < 13:
        return None
    return str(n - 12 if n <= MISSING_AFTER else n - 10)


def marker(n, band=""):
    label = page_no(n)
    where = f"p. {label} ({n:03d})" if label else f"({n:03d})"
    return f"<!-- {where}{', ' + band if band else ''} -->"


# ---------------------------------------------------------------- reading

HEAD = re.compile(r"[\dIlO ]*(INFERNO|CANTO [IVXL1 ]+|([IVX]+\. )?NOTES|DANTE['’]S HELL"
                  r"|CHRONOLOGY OF [\"“]INFERNO[\"”])?[\dIlO ]*")


def is_head(line):
    s = line.replace("*", "").strip()
    return bool(s) and HEAD.fullmatch(s) is not None


def read_page(n):
    """Lines of a page without running head, page number, and handwritten notes."""
    text = (SRC / f"{n:03d}.txt").read_text(encoding="utf-8")
    text = re.sub(r" *\(handwritten:[^)]*\)", "", text)
    lines = [l.rstrip() for l in text.strip().split("\n")]
    # running head (and page number), recognized by position: the first lines
    for _ in range(2):
        if lines and is_head(lines[0]):
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)
    # page number or printer's signature mark (`B`, `2 C`) at the foot of the page
    if lines and re.fullmatch(r"[\dIlO]+|(\d+ ?)?[A-Z]( \d+)?", lines[-1].strip()):
        lines.pop()
    # tercet numbers transcribed as a column of their own (`016`, `046`)
    if n not in PLATES and 14 <= n <= 402:
        lines = [l for l in lines if not re.fullmatch(r"\s*\d+\s*", l)]
    return lines


def paragraphs(lines):
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


# ---------------------------------------------------------------- hyphenation

VOCAB = set()
for d in (SRC, ROOT / "ocr" / "en"):
    for f in d.glob("*.txt"):
        text = f.read_text(encoding="utf-8")
        # the fragments of words hyphenated at a line end are not words
        text = re.sub(r"[A-Za-zÀ-ÿ’']+-\n\s*(\*\*[^*]*\*\* )?\*?[A-Za-zÀ-ÿ’']+", " ", text)
        VOCAB.update(re.findall(r"[A-Za-zÀ-ÿ’']+(?:-[A-Za-zÀ-ÿ’']+)*", text))
VOCAB_LOWER = {w.lower() for w in VOCAB}
UNDECIDED = []


# Line-end hyphens decided by hand: the word as it is to be written.
HYPHEN_FIXED = {
    "re-erected": "re-erected", "in-law": "in-law",  # father-in- / law
    "half-horses": "half-horses", "vicar-general": "Vicar-General",
    "evil-doing": "evil-doing", "heart-felt": "heart-felt",  # as in ocr/en
    "praise-worthy": "praiseworthy", "over-threw": "overthrew", "re-building": "rebuilding",
    "any-where": "anywhere", "mis-belief": "misbelief", "dis-honoured": "dishonoured",
    "de-formed": "deformed", "de-signate": "designate", "de-veloped": "developed",
    "dis-cussed": "discussed", "waver-ing": "wavering", "dismount-ing": "dismounting",
    "favour-ing": "favouring", "presum-ably": "presumably", "con-siderations": "considerations",
    "incom-patible": "incompatible", "sacra-ments": "sacraments", "repre-hensible": "reprehensible",
    "specifi-cally": "specifically", "miti-gation": "mitigation",
    "tele-machus": "Telemachus", "sini-baldo": "Sinibaldo", "bian-cucci": "Biancucci",
}


def join_hyphen(head, tail, where):
    m1 = re.search(r"([A-Za-zÀ-ÿ’']+)-$", head)
    m2 = re.match(r"\*?([A-Za-zÀ-ÿ’']+)", tail)
    if not m1 or not m2:
        return head + tail
    a, b = m1.group(1), m2.group(1)
    if f"{a}-{b}".lower() in HYPHEN_FIXED:
        sep = "-" if "-" in HYPHEN_FIXED[f"{a}-{b}".lower()] else ""
    elif (a + b).lower() in VOCAB_LOWER:
        sep = ""
    elif min(len(a), len(b)) >= 4 and a.lower() in VOCAB_LOWER and b.lower() in VOCAB_LOWER:
        sep = "-"
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}-{b}")
    elif f"{a}-{b}".lower() in VOCAB_LOWER or b[0].isupper():
        sep = "-"
    else:
        sep = ""
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}{b}")
    return head[:-1] + sep + tail


def join_lines(lines, where):
    """Join the printed lines of a paragraph into one line."""
    text = lines[0]
    for l in lines[1:]:
        if re.search(r"[A-Za-zÀ-ÿ’']-$", text):
            text = join_hyphen(text, l, where)
        elif text.endswith("—") or l.startswith("—"):
            text += l
        else:
            text += " " + l
    return text


def join_prose(lines, where):
    """An English paragraph: marginal labels are moved to its start."""
    labels = []
    body = []
    for l in lines:
        m = LABEL.match(l)
        if m:
            labels.append(m.group(1).strip())
            l = l[m.end():]
        if l:
            body.append(l)
    text = join_lines(body, where) if body else ""
    return text + label_comments(labels)


def label_comments(labels):
    """Marginal labels, kept out of the text as machine-readable comments."""
    return "".join(f" <!-- label: {l} -->" for l in labels)


# ---------------------------------------------------------------- canto pages

def verse_text(line):
    """An Italian verse line without its printed tercet number."""
    line = re.sub(r"\s*\(\d+\)$", "", line)
    line = re.sub(r"\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+$", "", line)
    line = re.sub(r"\s+\^?\d+$", "", line)
    return line.strip()


def tercets(first, last):
    """Number of tercet beginnings among verses first..last."""
    return sum(1 for i in range(first, last + 1) if i % 3 == 1)


class Canto:
    def __init__(self, c, first, last):
        self.c = c
        self.total = VERSES[c - 1]
        self.verse = 0  # verses read so far
        self.parts = [f"# Canto {roman(c).upper()}"]
        self.notes = []  # [(page, [paragraph lines]), ...] in reading order
        self.errors = []
        self.first, self.last = first, last

    # Italian page: verse until the canto ends, then notes
    def italian(self, n, lines, verse_lines):
        start = self.verse + 1
        rest = []
        for k, l in enumerate(lines):
            if not l.strip() or re.fullmatch(r"\s*\d+\s*", l):
                continue
            if self.verse >= self.total or NOTE_START.match(l.strip()):
                rest = lines[k:]
                break
            self.verse += 1
            if self.c == 34 and self.verse in MISSING_VERSES:
                self.errors.append(f"{n:03d}: verse {self.verse} expected on the missing leaf")
            verse_lines.append((self.verse, verse_text(l)))
        return start, self.verse, rest

    def render_verse(self, verse_lines):
        out = []
        for i, text in verse_lines:
            labels = []
            m = LABEL.match(text)
            if m:
                labels.append(m.group(1).strip())
                text = text[m.end():]
            line = text if i % 3 == 1 else "&emsp;" + text
            if i % 3 == 1 and i > 1:
                line += f" {i}"
            line += label_comments(labels)
            out.append(line)
        return "\\\n".join(out)

    def add_notes(self, n, paras):
        for p in paras:
            self.notes.append((n, p))


def split_english(lines, count):
    paras = paragraphs(lines)
    return paras[:count], paras[count:]


def convert_canto(c, first, last, errors):
    canto = Canto(c, first, last)
    parts = canto.parts
    notes_started = False
    n = first
    while n <= last:
        if n in PLATES:
            parts.append(marker(n))
            parts.append(render_plate(read_page(n)))
            n += 1
            continue
        it_lines = read_page(n)
        en_n = n + 1 if n != MISSING_AFTER else None
        en_lines = read_page(en_n) if en_n and en_n <= last and en_n not in PLATES else None
        arg = None
        if n == first:
            it_paras = paragraphs(it_lines)
            en_paras = paragraphs(en_lines)
            arg = (it_paras[0], en_paras[0])
            it_lines = [l for p in it_paras[1:] for l in p + [""]]
            en_lines = [l for p in en_paras[1:] for l in p + [""]]
        if canto.verse >= canto.total:
            # pages of notes only
            canto_notes(canto, n, paragraphs(it_lines))
            n += 1
            continue
        verse_lines = []
        if n == MISSING_AFTER + 1:
            # an English page whose Italian page is missing
            v1, v2 = MISSING_VERSES[0], MISSING_VERSES[-1]
            canto.verse = v2
            eng, rest = split_english(it_lines, tercets(v1, v2))
            parts.append(f"<!-- pp. 385–386 missing from the scan -->")
            parts.append(marker(n))
            parts.extend(join_prose(p, f"{n:03d}") for p in eng)
            if rest:
                errors.append(f"{n:03d}: text after the English tercets")
            n += 1
            continue
        v1, v2, it_rest = canto.italian(n, it_lines, verse_lines)
        if arg:
            parts.append(marker(n))
            parts.append("## Argument")
            arg_it = join_lines(arg[0], f"{n:03d}")
            arg_en = join_lines(arg[1], f"{en_n:03d}")
            if re.search(r"[A-Za-z]-$", arg_it):
                word, _, arg_en = arg_en.partition(" ")
                arg_it = join_hyphen(arg_it, word, f"{n:03d}->{en_n:03d}")
            parts.append(arg_it)
            parts.append(marker(en_n))
            parts.append(arg_en)
            parts.append(marker(n, "text"))
        else:
            parts.append(marker(n))
        parts.append(canto.render_verse(verse_lines))
        if en_lines is not None:
            count = tercets(v1, v2)
            if v2 == canto.total and canto.total % 3 == 1:
                count -= 1  # the last line is translated with the last tercet
            eng, en_rest = split_english(en_lines, count)
            parts.append(marker(en_n, "text") if arg else marker(en_n))
            parts.extend(join_prose(p, f"{en_n:03d}") for p in eng)
            for p in eng:
                if NOTE_START.match(p[0]):
                    errors.append(f"{en_n:03d}: note in the English tercets: {p[0][:40]}")
        else:
            en_rest = []
            if n != MISSING_AFTER:
                errors.append(f"{n:03d}: no facing English page")
        if en_rest and not NOTE_START.match(en_rest[0][0]):
            NOTE_START_CHECK.append(f"{en_n:03d}: {en_rest[0][0][:50]}")
        it_notes = paragraphs(it_rest)
        if it_notes and en_lines is not None and not en_rest \
                and not re.search(r"[.!?”\"’):*\]]$", it_notes[-1][-1]):
            # the note runs over to the English page, but no notes were found there:
            # a missing paragraph break has pulled them into the English tercets
            errors.append(f"{en_n:03d}: the note continued from {n:03d} is missing")
        if paragraphs(it_rest) or en_rest:
            if n == MISSING_AFTER:
                errors.append(f"{n:03d}: notes before the missing leaf")
            canto_notes(canto, n, paragraphs(it_rest), band="notes")
            if en_n:
                canto_notes(canto, en_n, en_rest, band="notes")
        n += 2 if en_lines is not None else 1
    if canto.verse != canto.total:
        errors.append(f"canto {c}: {canto.verse} verses, expected {canto.total}")
    errors.extend(canto.errors)
    return parts


def canto_notes(canto, n, paras, band=""):
    if not paras:
        return
    parts = canto.parts
    if not getattr(canto, "notes_heading", False):
        parts.append("## Notes")
        canto.notes_heading = True
    parts.append(marker(n, band))
    where = f"{n:03d}"
    for k, p in enumerate(paras):
        text = join_lines(p, where)
        prev = canto.last_note if getattr(canto, "last_note", None) else None
        if k == 0 and prev is not None and not NOTE_START.match(text) and n not in NOTE_NEW:
            # a paragraph continued from the previous page
            i, prev_text = prev
            if not re.search(r"[.!?”\"):]$", prev_text) or text[:1].islower() \
                    or n in NOTE_CONTINUED:
                if re.search(r"[A-Za-z]-$", prev_text):
                    joined = join_hyphen(prev_text, text, f"{where} (note)")
                else:
                    joined = prev_text + " " + text
                parts[i] = esc(joined)
                canto.last_note = (i, joined)
                continue
            CONTINUED_CHECK.append(f"{where}: {text[:50]}")
        if prev is not None and parts[-1] != marker(n, band) \
                and not re.search(r"[.!?”\"’):*\]]$", prev[1]):
            BREAK_CHECK.append(f"{where}: …{prev[1][-30:]} | {text[:30]}")
        parts.append(esc(text))
        canto.last_note = (len(parts) - 1, text)


# The first note paragraph of a page after a finished sentence, checked against the
# images: continued from the previous page (flush left) or a new paragraph (indented).
NOTE_CONTINUED = {189, 356}
NOTE_NEW = {69, 211, 225, 237, 332}

CONTINUED_CHECK = []
NOTE_START_CHECK = []
BREAK_CHECK = []  # a note paragraph after one that does not end a sentence


def esc(line):
    """Keep a line from being read as Markdown list or heading syntax."""
    line = re.sub(r"^(\d+)\. ", r"\1\\. ", line)
    return re.sub(r"^([-+*#>]) ", r"\\\1 ", line)


def render_plate(lines):
    return "\\\n".join(esc(l.strip()) for l in lines if l.strip())


# ---------------------------------------------------------------- other pages

def title_case(s):
    small = {"of", "the", "to", "and", "a", "in", "on", "for"}
    words = s.rstrip(".").lower().split()
    out = []
    for i, w in enumerate(words):
        if re.fullmatch(r"[ivxlc]+", w):
            out.append(w.upper())
        elif i and w in small:
            out.append(w)
        else:
            k = 1 if w[0] in "“\"‘" else 0
            out.append(w[:k] + w[k].upper() + w[k + 1:])
    return " ".join(out)


# Physical-copy and printer's marks transcribed on pages with printed text.
DROP_LINES = {13: ["774552"], 411: ["2 C"]}
# Pages printed as tables or plates: kept line by line.
TABLES = {405}
# Footnotes without a printed number: page -> (marker in the text, note text start).
FOOTNOTES = {403: ("translation.¹", "Essays on Dante,")}


def page_lines(n):
    lines = read_page(n)
    drop = DROP_LINES.get(n, [])
    return [l for l in lines if l.strip() not in drop]


def is_title(p):
    s = " ".join(p).replace("*", "")
    return s == s.upper() and re.search(r"[A-Z]{3}", s) and len(s) < 60


def render_lines(p):
    """A block kept line by line; leading spaces become indentation."""
    out = []
    for l in p:
        indent = (len(l) - len(l.lstrip())) // 2
        out.append("&emsp;" * indent + esc(l.strip()))
    return "\\\n".join(out)


def convert_plain(pages, title_page=False):
    parts = []
    for i, n in enumerate(pages):
        parts.append(marker(n))
        lines = page_lines(n)
        note = None
        if n in FOOTNOTES:
            ref, start = FOOTNOTES[n]
            k = next(k for k, l in enumerate(lines) if start in l[:len(start) + 3])
            note = join_lines([l.strip() for l in lines[k:] if l.strip()], f"{n:03d}")
            lines = lines[:k]
        for j, p in enumerate(paragraphs_raw(lines)):
            if title_page or n in TABLES:
                parts.append(render_lines(p))
            elif i == 0 and j == 0 and is_title(p):
                parts.append("# " + title_case(" ".join(p).replace("*", "")))
            elif all(l.startswith(" ") for l in p):
                parts.append(render_lines(p))
            else:
                parts.append(esc(join_lines([l.strip() for l in p], f"{n:03d}")))
        if note:
            label = f"[^{page_no(n)}-1]"
            ref, _ = FOOTNOTES[n]
            parts = [x.replace(ref, ref.rstrip("¹") + label) for x in parts]
            parts.append(f"{label}: {note}")
    return parts


def paragraphs_raw(lines):
    """Blocks separated by blank lines, keeping leading spaces."""
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.rstrip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def write(num, slug, parts):
    path = DST / f"{num:03d}-{slug}.md"
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main():
    DST.mkdir(parents=True, exist_ok=True)
    errors = []
    write(1, FRONT[0], convert_plain(FRONT[1], title_page=True))
    num = 1
    for c, (first, last) in enumerate(CANTO_PAGES, 1):
        num += 1
        write(num, f"canto-{c:02d}", convert_canto(c, first, last, errors))
    for slug, pages in BACK:
        num += 1
        write(num, slug, convert_plain(pages))
    for e in errors:
        print("ERROR", e)
    for u in UNDECIDED:
        print("HYPHEN", u)
    for x in BREAK_CHECK:
        print("NOTE BREAK AFTER UNFINISHED SENTENCE", x)
    for x in NOTE_START_CHECK:
        print("ENGLISH NOTES NOT STARTING WITH A NUMBER", x)
    for x in CONTINUED_CHECK:
        print("NEW PARAGRAPH AT PAGE TOP", x)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
