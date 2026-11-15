"""Convert the page transcriptions of a Temple Classics volume edited by Oelsner into
section files: ocr/en-oelsner/NNN.txt (the Inferno, 1903) into texts/en-oelsner/,
ocr/en-purgatorio/NNN.txt (the Purgatorio, 1904) into texts/en-purgatorio/, or
ocr/en-paradiso/NNN.txt (the Paradiso, 1910) into texts/en-paradiso/.

The volumes share their layout; what differs (verses per canto, the pages of each canto,
the plates and figures, the front and end matter, the decisions by hand) is in the
settings of each volume below. See texts/PLAN.md for the layout. Run from the repository
root:

    uv run texts/scripts/convert_en_oelsner.py [inferno|purgatorio|paradiso]
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ================================================================ the Inferno (1903)

INFERNO = {}
INFERNO["src"] = ROOT / "ocr" / "en-oelsner"
INFERNO["dst"] = ROOT / "texts" / "en-oelsner"
INFERNO["vocab"] = [INFERNO["src"], ROOT / "ocr" / "en"]
# The printed page = leaf - 12; the epigraph on 013 is p. [1].
INFERNO["PAGE_OFFSET"] = 12
INFERNO["EPIGRAPH"] = 13

# Verses per canto in the Inferno.
INFERNO["VERSES"] = [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136, 136,
          136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139, 157, 139]

# Canto n (1-based): first page (Argument), last page (notes or plate).
INFERNO["CANTO_PAGES"] = [(14, 25), (26, 37), (38, 47), (48, 59), (60, 71), (72, 81), (82, 91), (92, 101),
               (102, 111), (112, 123), (124, 133), (134, 145), (146, 157), (158, 169),
               (170, 179), (180, 191), (192, 201), (202, 213), (214, 225), (226, 237),
               (238, 249), (250, 261), (262, 273), (274, 285), (286, 297), (298, 309),
               (310, 321), (322, 333), (334, 345), (346, 357), (358, 369), (370, 381),
               (382, 393), (394, 404)]

# Full-page maps, plates and tables printed after a canto's notes.
INFERNO["PLATES"] = {25, 37, 133, 191, 249, 321, 345}


# The figures cut from the scans by crop_en_oelsner_images.py (texts/en-oelsner/images),
# shown where they are printed: at the top of their page, or after the note that
# introduces them (IMAGE_AFTER_NOTE, the end of that note). Their names and captions
# stay as text.
INFERNO["IMAGES"] = {
    25: "Map: Dante's geographical description",
    37: "Section of the Earth: Hell, Purgatory and the passage of the poets",
    133: "The hours at which the signs of the Zodiac rise",
    191: "Map: the rivers of Romagna and the mouth of the Po",
    284: "Diagram for Canto XXIV 34-40 (after Scartazzini)",
    411: "Fig. I: plan of concentric spheres",
    412: "Fig. II: section of the eight revolving heavens",
}
INFERNO["IMAGE_AFTER_NOTE"] = {284: "will make these verses clear:"}
# Figures printed below the notes of a page, from the line given to the page's end:
# their labels and caption (none in the Inferno).
INFERNO["FIGURE_FROM"] = {}
# A figure between two notes, its labels from the first line given to the last (none in
# the Inferno).
INFERNO["FIGURE_BETWEEN"] = {}
# Pages whose signature mark stands on its own line above the page number.
INFERNO["SIGNATURE_ABOVE"] = set()
# Italic spans closed at a line end and opened again on the next line joined into one
# (`*com-*` / `*pare*`); not in the Inferno, whose texts were made before.
INFERNO["ITALIC_JOIN"] = False

INFERNO["FRONT"] = ("title-page", [7, 8, 10, 11, 13])
INFERNO["BACK"] = [
    ("note-on-dantes-hell", [405, 406, 407]),
    ("the-chronology-of-the-inferno", [408, 409, 410]),
    ("plan-of-concentric-spheres", [411]),
    ("section-of-the-universe", [412]),
    ("editorial-note", [413]),
    ("index-to-maps-plates-and-tables", [414]),
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
    if n == EPIGRAPH:
        return "[1]"  # the epigraph
    if n < EPIGRAPH:
        return None
    return str(n - PAGE_OFFSET)


def marker(n, band=""):
    label = page_no(n)
    where = f"p. {label} ({n:03d})" if label else f"({n:03d})"
    return f"<!-- {where}{', ' + band if band else ''} -->"


# ---------------------------------------------------------------- reading

HEAD = re.compile(r"[\dIlO ]*(INFERNO|PURGATORIO|PARADISO|CANTO [IVXL1 ]+|([IVX]+\. )?NOTES"
                  r"|DANTE['’]S (HELL|PURGATORY|PARADISE)|\d+ EDITORIAL NOTE|EDITORIAL NOTE \d+"
                  r"|CHRONOLOGY OF [\"“](INFERNO|PURGATORIO)[\"”])?[\dIlO ]*")


def is_head(line):
    s = line.replace("*", "").strip()
    return bool(s) and HEAD.fullmatch(s) is not None


# A misprint marked in ocr/en-oelsner, `{{printed|fixed}}`, or a correction from a
# corrigenda list, `{{printed|LIST|fixed}}` (ocr/PLAN.md, "Decisions"): the fixed side.
MISPRINT = re.compile(r"\{\{([^{}|]*)\|(?:([0-9]+(?:&[0-9]+)*)\|)?([^{}|]*)\}\}")


def fixed(t):
    return MISPRINT.sub(r"\3", t)


FIGURE_LINES = {}  # page -> the lines of the figure below its notes (FIGURE_FROM)
FIGURE_LINES_BETWEEN = {}  # page -> the labels of the figure between notes (FIGURE_BETWEEN)


def read_page(n):
    """Lines of a page without running head, page number, and handwritten notes."""
    text = fixed((SRC / f"{n:03d}.txt").read_text(encoding="utf-8"))
    text = re.sub(r" *\(handwritten:[^)]*\)", "", text)
    lines = [l.rstrip() for l in text.strip().split("\n")]
    if n in FIGURE_FROM:
        # a figure below the notes, to the page's end: kept apart, not read as notes
        k = min(i for i, l in enumerate(lines) if l.strip() == FIGURE_FROM[n])
        FIGURE_LINES[n] = lines[k:]
        lines = lines[:k]
        while lines and not lines[-1].strip():
            lines.pop()
    if n in FIGURE_BETWEEN:
        # a figure between two notes: its labels kept apart, shown after its image
        first, last = FIGURE_BETWEEN[n]
        k = lines.index(first)
        m = lines.index(last, k)
        FIGURE_LINES_BETWEEN[n] = lines[k:m + 1]
        lines = lines[:k] + lines[m + 1:]
    # running head (and page number), recognized by position: the first lines
    for _ in range(2):
        if lines and is_head(lines[0]):
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)
    # page number or printer's signature mark (`B`, `2 C`) at the foot of the page
    if n not in FIGURE_LINES and lines \
            and re.fullmatch(r"[\dIlO]+|(\d+ ?)?[A-Z]( \d+)?", lines[-1].strip()):
        lines.pop()
        # a signature mark on the line above the page number (`Q` / `241`)
        if n in SIGNATURE_ABOVE and re.fullmatch(r"(\d+ ?)?[A-Z]", lines[-1].strip()):
            lines.pop()
    # tercet numbers transcribed as a column of their own (`016`, `046`)
    if n not in PLATES and CANTO_PAGES[0][0] <= n <= CANTO_PAGES[-1][1]:
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

VOCAB_LOWER = set()
UNDECIDED = []


def build_vocab(dirs):
    """The words of the transcriptions, unbroken: the joins of line-end hyphens."""
    vocab = set()
    for d in dirs:
        for f in d.glob("*.txt"):
            text = fixed(f.read_text(encoding="utf-8"))
            # the fragments of words hyphenated at a line end are not words
            text = re.sub(r"[A-Za-zÀ-ÿ’']+-\n\s*(\*\*[^*]*\*\* )?\*?[A-Za-zÀ-ÿ’']+", " ", text)
            vocab.update(re.findall(r"[A-Za-zÀ-ÿ’']+(?:-[A-Za-zÀ-ÿ’']+)*", text))
    return {w.lower() for w in vocab}


# Line-end hyphens decided by hand: the word as it is to be written.
INFERNO["HYPHEN_FIXED"] = {
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


def range_split(head, tail):
    """A number range divided at a line end (`76-` / `108`): joined with no space."""
    return bool(re.search(r"\d-$", head)) and tail[:1].isdigit()


def join_lines(lines, where):
    """Join the printed lines of a paragraph into one line."""
    text = lines[0]
    for l in lines[1:]:
        if ITALIC_JOIN and re.search(r"[^*]\*$", text) and re.match(r"\*[^*]", l):
            # an italic span closed at the line end and opened again on the next line:
            # one span, across a line-end hyphen too (`*com-*` / `*pare*`)
            text, l = text[:-1], l[1:]
            if re.search(r"[A-Za-zÀ-ÿ’']-$", text):
                text = join_hyphen(text, l, where)
            else:
                text += " " + l
        elif re.search(r"[A-Za-zÀ-ÿ’']-$", text):
            text = join_hyphen(text, l, where)
        elif text.endswith("]-") and l[:1].islower():
            # a word hyphenated after an editor's bracket (`[down]-` / `wards`)
            text = text[:-1] + l
        elif text.endswith("—") or l.startswith("—") or range_split(text, l):
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
            if n in IMAGES:
                parts.append(image(n))
            parts.append(render_plate(read_page(n)))
            n += 1
            continue
        it_lines = read_page(n)
        en_n = n + 1
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
            canto_notes(canto, n, paragraphs(it_rest), band="notes")
            canto_notes(canto, en_n, en_rest, band="notes")
        n += 2 if en_lines is not None else 1
    if canto.verse != canto.total:
        errors.append(f"canto {c}: {canto.verse} verses, expected {canto.total}")
    errors.extend(canto.errors)
    return parts


def canto_notes(canto, n, paras, band=""):
    if not paras:
        if n in FIGURE_LINES:
            canto.parts.append(marker(n, band))
            canto.parts.extend(figure(n))
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
                if ITALIC_JOIN and re.search(r"[^*]\*$", prev_text) \
                        and re.match(r"\*[^*]", text):
                    joined = join_lines([prev_text, text], f"{where} (note)")
                elif re.search(r"[A-Za-z]-$", prev_text):
                    joined = join_hyphen(prev_text, text, f"{where} (note)")
                elif prev_text.endswith("—") or range_split(prev_text, text):
                    joined = prev_text + text
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
        if n in IMAGE_AFTER_NOTE and text.endswith(IMAGE_AFTER_NOTE[n]):
            parts.append(image(n))
            if n in FIGURE_LINES_BETWEEN:
                parts.append(render_plate(FIGURE_LINES_BETWEEN[n]))
    if n in FIGURE_LINES:
        parts.extend(figure(n))


def figure(n):
    """A figure below the notes: its image, its labels line by line, its caption (the
    last paragraph, italic lines joined into one span)."""
    paras = paragraphs(FIGURE_LINES[n])
    caption = paras.pop() if paras[-1][0].startswith("*") else None
    out = [image(n)]
    if paras:
        out.append(render_plate([l for p in paras for l in p]))
    if caption:
        out.append(esc(join_lines(caption, f"{n:03d}")))
    return out


# The first note paragraph of a page after a finished sentence, checked against the
# images: continued from the previous page (flush left) or a new paragraph (indented).
INFERNO["NOTE_CONTINUED"] = {189, 356}
INFERNO["NOTE_NEW"] = {69}

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
INFERNO["DROP_LINES"] = {13: ["774552"], 413: ["2 C"]}
# Pages printed as tables or plates: kept line by line.
INFERNO["TABLES"] = {407}
# Pages of the end matter kept line by line from the paragraph that begins with the line
# given (a scheme below the text), and indexes printed without space between entries.
INFERNO["LINES_FROM"] = {}
INFERNO["INDEX_ENTRIES"] = set()
# Footnotes without a printed number: page -> (marker in the text, note text start).
INFERNO["FOOTNOTES"] = {405: ("translation.¹", "Essays on Dante,")}


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


# Pages 411-412 are taken from the Fifth Edition (1904), which rewrote them: the
# explanation of Fig. I under its figure on 411, then that of Fig. II from the foot of 411
# onto 412, above its figure. Each figure is a section of its own: Fig. I with 411 up to
# the label of Fig. II, Fig. II with the rest of 411 and with 412.
INFERNO["FIGURES"] = (411, 412, "**Fig. II.")


def convert_figures(n):
    first, second, start = FIGURES
    paras = paragraphs_raw(page_lines(first))
    k = next(i for i, p in enumerate(paras) if p[0].startswith(start))
    text = lambda p: esc(join_lines([l.strip() for l in p], f"{n:03d}"))
    if n == first:
        return [marker(first), image(first)] + [text(p) for p in paras[:k]]
    rest, after = paras[k:], paragraphs_raw(page_lines(second))
    # the last paragraph of 411 runs on into the first of 412, in one italic span
    tail, head = rest[-1], after[0]
    if tail[-1].endswith("*") and head[0].startswith("*"):
        tail, head = tail[:-1] + [tail[-1][:-1]], [head[0][1:]] + head[1:]
    rest[-1] = tail + head
    return [marker(first)] + [text(p) for p in rest[:-1]] + [text(rest[-1]), marker(second)] \
        + [text(p) for p in after[1:]] + [image(second)]


def convert_plain(pages, title_page=False):
    parts = []
    for i, n in enumerate(pages):
        parts.append(marker(n))
        if n in IMAGES:
            parts.append(image(n))
        lines = page_lines(n)
        note = None
        if n in FOOTNOTES:
            ref, start = FOOTNOTES[n]
            k = next(k for k, l in enumerate(lines) if start in l[:len(start) + 3])
            note = join_lines([l.strip() for l in lines[k:] if l.strip()], f"{n:03d}")
            note = re.sub(r"^¹\s*", "", note)  # the mark, when the base writes it
            lines = lines[:k]
        paras = paragraphs_raw(lines)
        if n in INDEX_ENTRIES:
            paras = index_entries(paras)
        from_k = None
        if n in LINES_FROM:
            from_k = next(k for k, p in enumerate(paras) if p[0].strip() == LINES_FROM[n])
        for j, p in enumerate(paras):
            if title_page or n in TABLES or (from_k is not None and j >= from_k):
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


def index_entries(paras):
    """An index printed without space between its entries: each entry, ended by the line
    with its page number, a paragraph of its own."""
    out = []
    for p in paras:
        cur = []
        for l in p:
            cur.append(l)
            if re.search(r"\d+(-\d+)?$", l.strip()):
                out.append(cur)
                cur = []
        if cur:
            out.append(cur)
    return out


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


# ================================================================ the Purgatorio (1904)

PURGATORIO = {}
PURGATORIO["src"] = ROOT / "ocr" / "en-purgatorio"
PURGATORIO["dst"] = ROOT / "texts" / "en-purgatorio"
PURGATORIO["vocab"] = [PURGATORIO["src"], INFERNO["src"], ROOT / "ocr" / "en"]
PURGATORIO["PAGE_OFFSET"] = 12
PURGATORIO["EPIGRAPH"] = 13

PURGATORIO["VERSES"] = [136, 133, 145, 139, 136, 151, 136, 139, 145, 139, 142, 136, 154, 151,
                        145, 145, 139, 145, 145, 151, 136, 154, 133, 154, 139, 148, 142, 148,
                        154, 145, 145, 160, 145]

_FIRST = [14, 26, 36, 48, 60, 72, 86, 104, 116, 128, 138, 150, 162, 176, 190, 202, 214, 226,
          240, 254, 270, 282, 296, 308, 322, 334, 346, 360, 374, 390, 404, 416, 430]
PURGATORIO["CANTO_PAGES"] = [(f, l - 1) for f, l in zip(_FIRST, _FIRST[1:] + [444])]

# The plate of the Zodiac (p. 59), the family tables (pp. 86-91, 241), the map (pp. 376-377).
PURGATORIO["PLATES"] = {71, 98, 99, 100, 101, 102, 103, 253, 388, 389}
PURGATORIO["IMAGES"] = {
    24: "The course of the Poets round and up the northern half of the Mount of Purgatory",
    25: "The mountain under light and shade at 6 a.m.",
    46: "Clock marking simultaneous hours at different regions of the earth",
    47: "The longitudes of Purgatory, Spain, Italy, Jerusalem and India",
    59: "The mountain under light and shade at noonday",
    71: "The hours at which the signs of the Zodiac begin to rise at the spring equinox",
    115: "The mountain under light and shade at 6 p.m.",
    388: "Map of Upper and Central Italy in Dante's time (west)",
    389: "Map of Upper and Central Italy in Dante's time (east)",
}
PURGATORIO["IMAGE_AFTER_NOTE"] = {}
PURGATORIO["FIGURE_FROM"] = {24: "N", 25: "N", 46: "NOON", 47: "Purgatory.", 59: "N",
                             115: "N"}
PURGATORIO["FIGURE_BETWEEN"] = {}
PURGATORIO["SIGNATURE_ABOVE"] = {253}
PURGATORIO["ITALIC_JOIN"] = True

PURGATORIO["FRONT"] = ("title-page", [7, 8, 10, 11, 13])
PURGATORIO["BACK"] = [
    ("note-on-dantes-purgatory", [444, 445, 446]),
    ("the-chronology-of-the-purgatorio", [447, 448, 449]),
    ("general-editorial-note", [451]),
    ("translators-note", [452]),
    ("editorial-note", [453]),
    ("index-to-plates-tables-etc", [454, 455]),
]
# Line-end hyphens decided by hand (as INFERNO's): the word as it is to be written.
PURGATORIO["HYPHEN_FIXED"] = {
    "distin-guishing": "distinguishing",  # divided across pages (149)
    "father-in": "father-in-law",  # father- / in-law
    "mid-quadrant": "mid-quadrant", "foster-mothers": "foster-mothers",
    "supernatural-rationalistic": "supernatural-rationalistic",
    "over-heard": "overheard", "over-taking": "overtaking", "o’er-shadows": "o’ershadows",
    "other-where": "otherwhere", "fossa-nuova": "Fossanuova",
}
# The first note paragraph of a page after a finished sentence, checked in the images
# (as NOTE_CONTINUED above).
PURGATORIO["NOTE_CONTINUED"] = {45, 69, 113, 252, 343, 415, 428}
PURGATORIO["NOTE_NEW"] = {267}
PURGATORIO["DROP_LINES"] = {}
PURGATORIO["TABLES"] = set()
PURGATORIO["LINES_FROM"] = {}
PURGATORIO["INDEX_ENTRIES"] = set()
PURGATORIO["FOOTNOTES"] = {}
PURGATORIO["FIGURES"] = ()

# ================================================================ the Paradiso (1910)
# The structure from ocr/en-paradiso/INDEX.md; the decisions by hand (FIGURE_FROM,
# SIGNATURE_ABOVE, HYPHEN_FIXED, NOTE_CONTINUED, NOTE_NEW, ...) are filled in by the
# mechanical checks once the base is there (ocr/en-paradiso/PLAN.md, step 2).

PARADISO = {}
PARADISO["src"] = ROOT / "ocr" / "en-paradiso"
PARADISO["dst"] = ROOT / "texts" / "en-paradiso"
PARADISO["vocab"] = [PARADISO["src"], PURGATORIO["src"], INFERNO["src"], ROOT / "ocr" / "en"]
# The printed page = leaf - 10; the epigraph on 011 is p. [1] (ocr/en-paradiso/README.md).
PARADISO["PAGE_OFFSET"] = 10
PARADISO["EPIGRAPH"] = 11

PARADISO["VERSES"] = [142, 148, 130, 142, 139, 142, 148, 148, 142, 148, 139, 145, 142, 139,
                      148, 154, 142, 136, 148, 148, 142, 154, 139, 154, 139, 142, 148, 139,
                      145, 148, 142, 151, 145]

_FIRST = [12, 24, 36, 46, 58, 70, 86, 100, 112, 126, 140, 152, 166, 178, 190, 202, 218, 228,
          238, 254, 266, 278, 290, 300, 312, 324, 336, 348, 360, 372, 384, 396, 408]
PARADISO["CANTO_PAGES"] = [(f, l - 1) for f, l in zip(_FIRST, _FIRST[1:] + [420])]

# The maps with pages of their own (pp. 115, 191, 207), the Tables of Kings (pp. 240-243)
# and the table of Dante's descent (p. 373), each at the end of a canto's notes.
PARADISO["PLATES"] = {125, 201, 217, 250, 251, 252, 253, 383}
PARADISO["IMAGES"] = {
    22: "Diagram of the four circles and three crosses",
    69: "Diagram of the three mirrors",
    98: "Map illustrating the boundaries of Provence",
    99: "Map of Naples and Sicily",
    110: "Map of Hungary, Rascia, etc.",
    111: "Map of the Mediterranean, shewing the position of Marseilles",
    125: "Map of the district about Romano",
    151: "Map shewing the position of Assisi",
    201: "Map of the district about Florence",
    217: "Map of Cacciaguida's Florence",
    406: "Map of the World west of Jerusalem",
    407: "Map of the World east of Jerusalem",
}
# The diagram on 022 stands between two notes: after the note that ends so, its labels
# (FIGURE_BETWEEN: the first and the last) after the image.
PARADISO["IMAGE_AFTER_NOTE"] = {22: "it at the same spot."}
PARADISO["FIGURE_BETWEEN"] = {22: ("S.P.", "N.P.")}
# The figures below the notes, from their first line to the page's end.
PARADISO["FIGURE_FROM"] = {69: "*Canto II*", 98: "R.Rhone", 99: "R.Tronto", 110: "BOHEMIA",
                           111: "MARSEILLES", 151: "S. UBALDO", 406: "II", 407: "I"}
PARADISO["SIGNATURE_ABOVE"] = set()
PARADISO["ITALIC_JOIN"] = True

PARADISO["FRONT"] = ("title-page", [5, 6, 8, 9, 11])
PARADISO["BACK"] = [
    ("note-on-dantes-paradise", [420, 421, 422, 423]),
    ("epigraph", [424]),
    ("general-editorial-note", [425]),
    ("editorial-note", [426, 427, 428]),
    ("index-to-maps-diagrams-and-tables", [429, 430]),
]
PARADISO["HYPHEN_FIXED"] = {
    "establish-ment": "establishment", "signa-ture": "signature", "endow-ment": "endowment",
    "inter-change": "interchange",
    "new-create": "new-create", "diverse-natured": "diverse-natured", "things-to": "things-to",
    "a-moving": "a-moving", "three-stringed": "three-stringed", "tooth-grips": "tooth-grips",
}
PARADISO["NOTE_CONTINUED"] = {35}
PARADISO["NOTE_NEW"] = {57}
PARADISO["DROP_LINES"] = {}
PARADISO["TABLES"] = set()
# The scheme of the heavens below the text of 423; the index on 429.
PARADISO["LINES_FROM"] = {423: "Empyrean"}
PARADISO["INDEX_ENTRIES"] = {429}
PARADISO["FOOTNOTES"] = {420: ("*Essays on Dante*¹", "*Essays on Dante.*")}
PARADISO["FIGURES"] = ()

VOLUMES = {"inferno": INFERNO, "purgatorio": PURGATORIO, "paradiso": PARADISO}


def configure(name):
    """Make the settings of a volume the module's globals, read by the functions above."""
    global SRC, DST, VOCAB_LOWER
    vol = VOLUMES[name]
    SRC, DST = vol["src"], vol["dst"]
    globals().update({k: v for k, v in vol.items() if k.isupper()})
    VOCAB_LOWER = build_vocab(vol["vocab"])


def image(n):
    return f"![{IMAGES[n]}](images/{n:03d}.jpg)"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("volume", nargs="?", default="inferno", choices=VOLUMES)
    configure(ap.parse_args().volume)
    DST.mkdir(parents=True, exist_ok=True)
    errors = []
    write(1, FRONT[0], convert_plain(FRONT[1], title_page=True))
    num = 1
    for c, (first, last) in enumerate(CANTO_PAGES, 1):
        num += 1
        write(num, f"canto-{c:02d}", convert_canto(c, first, last, errors))
    for slug, pages in BACK:
        num += 1
        if pages[0] in FIGURES:
            write(num, slug, convert_figures(pages[0]))
        else:
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
