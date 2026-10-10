"""Convert ocr/en/NNN.txt (Carlyle's edition, 1889) into texts/en/NNN-title.md.

See PLAN.md for the layout. Run from the repository root:

    uv run texts/convert_en.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ocr" / "en"
DST = ROOT / "texts" / "en"

# Verses per canto in the Inferno, used to check the verse classification.
VERSES = [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136, 136,
          136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139, 157, 139]

# Canto n (1-based): Argument page, last page (blank versos are skipped).
CANTO_PAGES = [(55, 66), (67, 78), (79, 88), (89, 100), (101, 112), (113, 122), (123, 134),
               (135, 146), (147, 158), (159, 172), (173, 184), (185, 196), (197, 210),
               (211, 222), (223, 234), (235, 246), (247, 258), (259, 270), (271, 284),
               (285, 298), (299, 312), (313, 324), (325, 336), (337, 348), (349, 360),
               (361, 372), (373, 384), (385, 398), (399, 412), (413, 426), (427, 438),
               (439, 450), (451, 464), (465, 476)]

FRONT = [
    ("title-page", [5, 6, 9, 10]),
    ("preface-first-edition", range(11, 19)),
    ("preface-second-and-third-editions", [19]),
    ("manuscripts-and-editions", range(21, 32)),
    ("comments-and-translations", range(32, 47)),
    ("the-inferno-of-dante", range(47, 55)),
]
INDEX = ("index-of-proper-names", [477] + list(range(479, 487)))

# Headings printed in the middle of a page.
MID_HEADINGS = {"PREFACE TO THE THIRD EDITION."}

# Note markers missing in the print, added so that the note is referenced: page -> (old, new).
ADDED_MARKERS = {
    132: ("malignant shores.", "malignant shores.²"),
    233: ("Accorso; also", "Accorso;¹ also"),
    429: ("its way, directed", "its way,¹ directed"),
}

# Pages printed without a page number (besides the Argument pages).
UNNUMBERED = {11, 19, 21, 32, 47, 477, 479} | {first for first, _ in CANTO_PAGES}

EN_WORDS = set("the and of to he my his him with that which was is it as thou thee "
               "thy they them their from this not but be had have for on at by so who what "
               "said there all were when".split())
IT_WORDS = set("che il la di e mi non per lo le del della ch’ io un una si se con al "
               "ma quel quella più già sì ed è era sen va nel nella ne da tu ei egli quei così come "
               "poi".split())

ROMAN = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"),
         (50, "l"), (40, "xl"), (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def roman(n):
    s = ""
    for v, r in ROMAN:
        while n >= v:
            s += r
            n -= v
    return s


def page_label(n):
    if n <= 10:
        return None
    p = roman(n - 6) if n <= 54 else str(n - 54)
    return f"[{p}]" if n in UNNUMBERED else p


def marker(n):
    label = page_label(n)
    return f"<!-- p. {label} ({n:03d}) -->" if label else f"<!-- ({n:03d}) -->"


def read_page(n):
    text = (SRC / f"{n:03d}.txt").read_text(encoding="utf-8").strip()
    if n in ADDED_MARKERS:
        old, new = ADDED_MARKERS[n]
        assert text.count(old) == 1, n
        text = text.replace(old, new)
    return text


def blocks(text):
    return [b.split("\n") for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]


def is_italian(lines):
    """Tell a short block of Italian verse from English prose."""
    if any(len(l) > 55 for l in lines):
        return False
    words = re.findall(r"[\w’]+", " ".join(lines).lower())
    en = sum(w in EN_WORDS for w in words)
    it = sum(w in IT_WORDS or w.endswith("’") for w in words)
    return it >= en


# ---------------------------------------------------------------- hyphenation

VOCAB = set()
for f in SRC.glob("*.txt"):
    VOCAB.update(re.findall(r"[A-Za-zÀ-ÿ’]+(?:-[A-Za-zÀ-ÿ’]+)*", f.read_text(encoding="utf-8")))
VOCAB_LOWER = {w.lower() for w in VOCAB}
UNDECIDED = []


def join_hyphen(head, tail, where):
    """Join `head` ending in '-' with `tail`; return the joined text."""
    m1 = re.search(r"([A-Za-zÀ-ÿ’]+)-$", head)
    m2 = re.match(r"([A-Za-zÀ-ÿ’]+)", tail)
    a, b = m1.group(1), m2.group(1)
    if (a + b).lower() in VOCAB_LOWER:
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


def ends_hyphen(text):
    return bool(re.search(r"[A-Za-zÀ-ÿ’]-$", text))


# ---------------------------------------------------------------- page model

class Page:
    def __init__(self, n):
        self.n = n
        self.headings = []  # (level, text) before the content
        self.prose = []  # list of blocks (list of lines)
        self.verse = []  # list of lines
        self.vnotes = []  # list of lines
        self.notes = []  # list of [number, paragraphs]; paragraph = list of lines
        self.cont = []  # paragraphs continuing the previous page's last note
        self.tail = []  # blocks after the notes (closing lines)
        self.refs = []  # note numbers referenced in the text


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
            out.append(w[0].upper() + w[1:])
    return " ".join(out)


def is_heading(lines):
    s = " ".join(lines)
    return len(lines) == 1 and s == s.upper() and re.search(r"[A-Z]{3}", s) and len(s) < 60


def parse_body(n):
    """A canto text page: prose, verse, verse notes, footnotes."""
    p = Page(n)
    phase = "prose"
    split = []
    for b in blocks(read_page(n)):
        # a footnote sometimes follows verse or another note without a blank line
        start = 0
        for i in range(1, len(b)):
            if re.match(r"\d{1,2} ", b[i]):
                split.append(b[start:i])
                start = i
        split.append(b[start:])
    for b in split:
        first = b[0]
        if re.fullmatch(r"CANTO [IVXL]+\.", first):
            continue
        if first == "END OF THE INFERNO.":
            p.tail.append(b)
            continue
        if phase in ("prose", "verse"):
            if re.match(r"\d+\. ", first) and phase == "verse":
                phase = "vnotes"
            elif re.match(r"\d+ ", first):
                phase = "notes"
            elif phase == "prose":
                # verse may follow a prose line without a blank line
                j = next((j for j, l in enumerate(b) if is_italian([l])), None)
                if j is not None:
                    if j:
                        p.prose.append(b[:j])
                        b = b[j:]
                    phase = "verse"
            elif phase == "verse" and not is_italian(b):
                phase = "notes"  # unnumbered: continued note
        if phase == "prose":
            p.prose.append(b)
        elif phase == "verse":
            p.verse.extend(b)
        elif phase == "vnotes":
            if re.match(r"\d+\. ", first):
                p.vnotes.extend(b)
                continue
            phase = "notes"
        if phase == "notes":
            m = re.match(r"(\d+) (.*)", first)
            if m and (not p.notes or int(m.group(1)) == p.notes[-1][0] + 1):
                p.notes.append([int(m.group(1)), [[m.group(2)] + b[1:]]])
            elif p.notes:
                p.notes[-1][1].append(b)
            else:
                p.cont.append(b)
    return p


def parse_plain(n, first_page):
    """Front matter, Argument, and index pages: headings, prose, footnotes."""
    p = Page(n)
    in_notes = False
    for b in blocks(read_page(n)):
        if n > 10 and not p.prose and not in_notes and is_heading(b):
            level = 2 if b[0].startswith("ARGUMENT") or not first_page else 1
            p.headings.append((level, title_case(b[0])))
            continue
        m = re.match(r"(\d+) (.*)", b[0])
        if m and 10 < n < 477 and (in_notes or int(m.group(1)) == 1):
            in_notes = True
            p.notes.append([int(m.group(1)), [[m.group(2)] + b[1:]]])
        elif in_notes:
            p.notes[-1][1].append(b)
        elif b[0] in MID_HEADINGS:
            p.prose.append(("heading", title_case(b[0])))
        else:
            p.prose.append(b)
    return p


# ---------------------------------------------------------------- cross-page joins

def link_pages(pages):
    """Resolve hyphens and continued notes between consecutive pages."""
    last_note = pages[0].notes[-1] if pages and pages[0].notes else None
    for prev, cur in zip(pages, pages[1:]):
        where = f"{prev.n:03d}->{cur.n:03d}"
        # prose: a word split across the page is joined on the earlier page
        if prev.prose and cur.prose and isinstance(prev.prose[-1], list) \
                and isinstance(cur.prose[0], list) and ends_hyphen(prev.prose[-1][-1]):
            word, _, rest = cur.prose[0][0].partition(" ")
            word = note_refs(cur, word)  # a marker on the moved word keeps its page
            prev.prose[-1][-1] = join_hyphen(prev.prose[-1][-1], word, where)
            if rest:
                cur.prose[0][0] = rest
            else:
                cur.prose[0] = cur.prose[0][1:]
                if not cur.prose[0]:
                    cur.prose.pop(0)
        # continued notes are appended to the last note started before this page
        if cur.cont:
            if not last_note:
                sys.exit(f"{where}: continued note without a note to continue")
            paras = last_note[1]
            # the first block continues the note's last paragraph
            if ends_hyphen(paras[-1][-1]):
                paras[-1][-1] = join_hyphen(paras[-1][-1], cur.cont[0][0], where)
            else:
                paras[-1][-1] += " " + cur.cont[0][0]
            paras[-1].extend(cur.cont[0][1:])
            paras.extend(cur.cont[1:])
            cur.cont = []
        if cur.notes:
            last_note = cur.notes[-1]


# ---------------------------------------------------------------- rendering

def esc(line):
    """Keep a line from being read as Markdown list or heading syntax."""
    line = re.sub(r"^(\d+)\. ", r"\1\\. ", line)
    return re.sub(r"^([-+*#>]) ", r"\\\1 ", line)


def hard(lines, indent=""):
    return ("\\\n" + indent).join(esc(l) for l in lines)


def render_notes(page):
    out = []
    for num, paras in page.notes:
        label = page_label(page.n).strip("[]")
        body = f"[^{label}-{num}]: " + hard(paras[0], "    ")
        for para in paras[1:]:
            body += "\n\n    " + hard(para, "    ")
        out.append(body)
    return out


SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def note_refs(page, text):
    """Turn superscript note markers (¹, ²…) into footnote references."""
    label = (page_label(page.n) or "").strip("[]")

    def ref(m):
        n = int(m.group().translate(SUP))
        page.refs.append(n)
        return f"[^{label}-{n}]"
    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+", ref, text)


def render_page(page, verse_no=None):
    out = render_content(page, verse_no)
    return [out[0]] + [x if x.startswith("[^") else note_refs(page, x) for x in out[1:]]


def render_content(page, verse_no):
    out = [marker(page.n)]
    for level, text in page.headings:
        out.append("#" * level + " " + text)
    for b in page.prose:
        if isinstance(b, tuple):
            out.append("# " + b[1])
        else:
            out.append(hard(b))
    if page.verse:
        lines = []
        for line in page.verse:
            i = verse_no[0]
            verse_no[0] += 1
            text = line if i % 3 == 0 else "&emsp;" + line
            if (i + 1) % 5 == 0:
                text += f" {i + 1}"
            lines.append(text)
        out.append("\\\n".join(lines))
    out.extend(esc(l) for l in page.vnotes)
    out.extend(render_notes(page))
    out.extend(hard(b) for b in page.tail)
    return out


def check_refs(pages, errors, missing):
    for p in pages:
        nums = [x[0] for x in p.notes]
        if sorted(p.refs) != sorted(set(p.refs)) or not set(p.refs) <= set(nums):
            errors.append(f"{p.n:03d}: note markers {p.refs}, notes {nums}")
        elif nums and not p.refs:
            missing.append(f"{p.n:03d}")
        elif set(p.refs) != set(nums):
            errors.append(f"{p.n:03d}: note markers {p.refs}, notes {nums}")


def write(num, slug, parts):
    path = DST / f"{num:03d}-{slug}.md"
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def is_blank(n):
    return read_page(n) in ("[Blank page]", "[Cover]")


def main():
    DST.mkdir(parents=True, exist_ok=True)
    num = 0
    errors = []
    missing = []  # pages whose note markers are not restored yet
    for slug, rng in FRONT:
        num += 1
        pages = [parse_plain(n, i == 0) for i, n in enumerate(rng)]
        link_pages(pages)
        write(num, slug, [x for p in pages for x in render_page(p)])
        check_refs(pages, errors, missing)

    for c, (first, last) in enumerate(CANTO_PAGES, 1):
        num += 1
        arg = parse_plain(first, True)
        body = [parse_body(n) for n in range(first + 1, last + 1) if not is_blank(n)]
        link_pages(body)
        verse_no = [0]
        parts = [f"# Canto {roman(c).upper()}"]
        parts += render_page(arg)
        for p in body:
            parts += render_page(p, verse_no)
        check_refs([arg] + body, errors, missing)
        if verse_no[0] != VERSES[c - 1]:
            errors.append(f"canto {c}: {verse_no[0]} verses, expected {VERSES[c - 1]}")
        for p in body:
            nums = [x[0] for x in p.notes]
            if nums and nums != list(range(1, len(nums) + 1)):
                errors.append(f"{p.n:03d}: note numbers {nums}")
        write(num, f"canto-{c:02d}", parts)

    num += 1
    slug, rng = INDEX
    pages = [parse_plain(n, i == 0) for i, n in enumerate(rng)]
    write(num, slug, [x for p in pages for x in render_page(p)])

    for e in errors:
        print("ERROR", e)
    for u in UNDECIDED:
        print("HYPHEN", u)
    if missing:
        print("NO MARKERS", len(missing), "pages:", " ".join(missing))


if __name__ == "__main__":
    main()
