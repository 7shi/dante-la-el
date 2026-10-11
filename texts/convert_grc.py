"""Convert ocr/grc/NNN.txt (Musurus's Greek translation, 1882) into texts/grc/NNN-title.md.

See PLAN.md for the layout. Run from the repository root:

    uv run texts/convert_grc.py
"""

import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "ocr" / "grc"
DST = ROOT / "texts" / "grc"

# Verses per canto in the Inferno.
VERSES = [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136, 136,
          136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139, 157, 139]

# First scan of each canto (the page with its heading); the last canto ends on 285.
CANTO_START = [21, 29, 37, 45, 53, 61, 68, 75, 82, 89, 97, 104, 112, 120, 128, 135, 143, 151,
               159, 166, 173, 181, 189, 197, 205, 213, 221, 229, 237, 245, 253, 261, 269, 278]
CANTO_END = 285
HALF_TITLE = 19
NOTES = [287] + list(range(289, 352))

NUMERALS = ["Α", "Β", "Γ", "Δ", "Ε", "ΣΤ", "Ζ", "Η", "Θ", "Ι", "ΙΑ", "ΙΒ", "ΙΓ", "ΙΔ", "ΙΕ",
            "ΙΣΤ", "ΙΖ", "ΙΗ", "ΙΘ", "Κ", "ΚΑ", "ΚΒ", "ΚΓ", "ΚΔ", "ΚΕ", "ΚΣΤ", "ΚΖ", "ΚΗ",
            "ΚΘ", "Λ", "ΛΑ", "ΛΒ", "ΛΓ", "ΛΔ"]
KERAIA = "΄"  # the numeral sign as written in the headings: Α΄

FRONT = [
    ("title-page", [1, 2, 3]),
    ("prologos", [5, 6, 7]),
    ("table-of-contents", [9, 10, 11, 12, 13]),
    ("corrigenda", [14]),
    ("corrigenda-extended", [15, 16, 17, 18]),
]

# Printed page numbers of the front matter (Greek numerals; bracketed if not printed).
FRONT_PAGES = {5: "ε΄", 6: "στ΄", 7: "ζ΄", 9: "[θ΄]", 10: "ι΄", 11: "ια΄", 12: "ιβ΄",
               13: "ιγ΄", 14: "[ιδ΄]", 15: "[1]", 16: "2", 17: "3", 18: "4"}

HEADINGS = {
    "ΠΡΟΛΟΓΟΣ.": "Πρόλογος",
    "ΠΙΝΑΞ ΤΩΝ ΕΝ ΕΚΑΣΤΗι ΩΔΗι ΠΕΡΙΕΧΟΜΕΝΩΝ.": "Πίναξ τῶν ἐν ἑκάστῃ ᾠδῇ περιεχομένων",
    "ΠΑΡΟΡΑΜΑΤΩΝ ΔΙΟΡΘΩΣΙΣ.": "Παροραμάτων διόρθωσις",
    "ΣΗΜΕΙΩΣΕΙΣ.": "Σημειώσεις",
}

# Library stamps transcribed on pages with printed text.
STAMPS = {1: ["ΠΑΝΕΠΙΣΤΗΜΙΟ ΚΡΗΤΗΣ"], 351: ["ΒΙΒΛΙΟΘΗΚΗ", "ΙΩΑΝΝΟΥ", "ΚΑΛΙΤΣΟΥΝΑΚΗ"]}


def page_no(n):
    if n in FRONT_PAGES:
        return FRONT_PAGES[n]
    if n < 21:
        return None
    p = n - 20
    return f"[{p}]" if n in CANTO_START or n in (287, 289) else str(p)


def marker(n):
    label = page_no(n)
    return f"<!-- p. {label} ({n:03d}) -->" if label else f"<!-- ({n:03d}) -->"


def plain(s):
    """Letters only, without accents and case, for comparisons."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c)[0] == "L")
    return s.lower().replace("ς", "σ")


def numeral(s):
    """`Α΄`, `Αʹ`, `Α'`, … -> `Α` (None if not a canto numeral)."""
    s = re.sub(r"[^Α-Ω]+$", "", s.strip())
    return s if s in NUMERALS else None


# ---------------------------------------------------------------- reading

MARK = "[\u0384\u00b4\u0374\u02b9\u1ffd\u1fbd'’]"  # the numeral sign as transcribed
HEAD_WORD = re.compile(r"\d+|ΩΔΗ|Εἰς|[ᾨᾠὨ]δὴν|ΠΕΡΙΕΧΟΜΕΝΑ\.?|ΠΡΟΛΟΓΟΣ\.?|Σελ\."
                       r"|[Α-Ω]+" + MARK + r"?\.?|[α-ω]+" + MARK + r"?\.?")
SIGNATURE = re.compile(r"[A-ZΑ-Ω0]" + MARK + r"?\.?( 2)?")
ORNAMENT = re.compile(r"[\s—–―⸻_*☉oO-]+")


LABEL_WORD = re.compile(r"ΩΔΗ|Εἰς|ΠΕΡΙΕΧΟΜΕΝΑ\.?|ΠΡΟΛΟΓΟΣ\.?")
NUMBER_WORD = re.compile(r"\d+|[α-ω]+" + MARK + r"?\.?")


def head_words(s):
    """The words of a running-head line, or None if it is not one."""
    words = re.sub(r"(\d+)", r" \1 ", s).split()
    ok = words and len(words) <= 4 and all(HEAD_WORD.fullmatch(w) for w in words)
    return words if ok else None


# Letters missing from the print (the type did not print), supplied here: page -> (as printed, supplied)
MISSING_TYPE = {265: ("ἶπον τῷ πικρῶς", "Εἶπον τῷ πικρῶς")}  # ΛΒ΄ 86


def read_page(n, head=True):
    """Lines of a page without running head, page number, signature marks and stamps.

    With head=False, only the page number is removed from the head: on the pages of
    notes, the label is either the running head or the heading of a canto's notes."""
    text = (SRC / f"{n:03d}.txt").read_text(encoding="utf-8")
    lines = [l.rstrip() for l in text.strip().split("\n")]
    lines = [l for l in lines if l.strip() not in STAMPS.get(n, [])]
    if n in MISSING_TYPE:
        a, b = MISSING_TYPE[n]
        lines = [l.replace(a, b) for l in lines]
    if not head:
        k = next((k for k, l in enumerate(lines[:3]) if re.search(r"\d", l)), None)
        if k is not None and head_words(lines[k]):
            lines[k] = re.sub(r"\s*\d+\s*", " ", lines[k]).strip()
    elif page_no(n) and not page_no(n).startswith("[") and n not in (5, 15):
        # running head, recognized by position: a page number and a label on the
        # first lines (`2 ΩΔΗ Α΄`, `ΩΔΗ Α΄.` / `3`), and the TOC column head `Σελ.`
        label = number = False
        while lines and not (label and number) and (words := head_words(lines[0])):
            label = label or any(LABEL_WORD.fullmatch(w) for w in words)
            number = number or any(NUMBER_WORD.fullmatch(w) for w in words)
            lines.pop(0)
            while lines and not lines[0].strip():
                lines.pop(0)
        if lines and lines[0].strip() == "Σελ.":
            lines.pop(0)
    # page number or printer's signature mark (`Β΄ 2`, `C. 2`, `G`) at the foot
    while lines and (re.fullmatch(r"\d+", lines[-1].strip()) and n >= 21
                     or SIGNATURE.fullmatch(lines[-1].strip()) and n >= 21):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
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

WORD = r"[^\W\d_]+"
VOCAB = set()
for f in SRC.glob("*.txt"):
    text = f.read_text(encoding="utf-8")
    # the fragments of words hyphenated at a line end are not words
    text = re.sub(WORD + r"-\n\s*" + WORD, " ", text)
    VOCAB.update(w.lower() for w in re.findall(WORD + r"(?:-" + WORD + r")*", text))
UNDECIDED = []
GREEK = r"[\u0370-\u03ff\u1f00-\u1fff]+"

# Line-end hyphens outside Greek, decided by hand: the word as it is to be written.
HYPHEN_FIXED = {
    "veuil-je": "veuil-je", "ci-dessus": "ci-dessus",  # as ferois-je, fait-elle
    "porce-que": "porceque",  # as porque in the same sentence
    "leg-giero": "leggiero", "cor-nubia": "Cornubia", "fum-mo": "fummo",
    "lu-cifero": "Lucifero", "gad-sand": "Gadsand", "com-muns": "communs",
    "gio-vanni": "Giovanni", "bal-wearie": "Balwearie", "vul-gar": "Vulgar",
    "mala-coda": "Malacoda", "ade-lasia": "Adelasia", "gau-dentes": "Gaudentes",
    "mar-cello": "Marcello", "dic-tionnaire": "Dictionnaire", "pro-fond\u00e9ment": "profond\u00e9ment",
    "impar-faitement": "imparfaitement", "\u00e9gale-ment": "\u00e9galement", "ron-cevaux": "Roncevaux",
    "masche-roni": "Mascheroni", "vallom-brosa": "Vallombrosa", "julia-no": "Juliano",
}


def join_hyphen(head, tail, where):
    m1 = re.search(r"(" + WORD + r")-$", head)
    m2 = re.match(r"\W*?(" + WORD + r")", tail)
    if not m1 or not m2:
        return head + tail
    a, b = m1.group(1), m2.group(1)
    greek = re.fullmatch(GREEK, a + b)
    if f"{a}-{b}".lower() in HYPHEN_FIXED:
        sep = "-" if "-" in HYPHEN_FIXED[f"{a}-{b}".lower()] else ""
    elif f"{a}-{b}".lower() in VOCAB or b[0].isupper():
        sep = "-"
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}-{b}")
    else:
        sep = ""
        if not greek and (a + b).lower() not in VOCAB:
            # Greek is hyphenated by syllables; other languages (`sur-le-champ`) are listed
            UNDECIDED.append(f"{where}: {a}-{b} -> {a}{b}")
    return head[:-1] + sep + tail


def join_lines(lines, where):
    """Join the printed lines of a paragraph into one line."""
    text = lines[0]
    for l in lines[1:]:
        if re.search(WORD + "-$", text):
            text = join_hyphen(text, l, where)
        elif text.endswith("—") or l.startswith("—"):
            text += l
        else:
            text += " " + l
    return text


def esc(line):
    """Keep a line from being read as Markdown list or heading syntax."""
    line = re.sub(r"^(\d+)\. ", r"\1\\. ", line)
    return re.sub(r"^([-+*#>]) ", r"\\\1 ", line)


# ---------------------------------------------------------------- table of contents

def read_toc():
    """The printed arguments: {canto: (text, page)}."""
    lines = []
    for n in range(9, 14):
        lines += [l for l in read_page(n) if l.strip() and l.strip() not in
                  ("ΠΙΝΑΞ ΤΩΝ ΕΝ ΕΚΑΣΤΗι ΩΔΗι", "ΠΕΡΙΕΧΟΜΕΝΩΝ.")]
    entries = []
    for l in lines:
        if l.startswith("ΩΔΗ"):
            entries.append([])
        if entries:
            entries[-1].append(l.strip())
    toc = {}
    for e in entries:
        text = join_lines(e, "toc")
        m = re.fullmatch(r"ΩΔΗ ([Α-Ω]+)[^\s—]*\s*—\s*(.*?)[\s.]*?(\d+)", text)
        if not m:
            sys.exit(f"TOC entry: {text}")
        c = NUMERALS.index(numeral(m.group(1))) + 1
        toc[c] = (m.group(2).rstrip(". "), int(m.group(3)), text)
    return toc


TOC = read_toc()


# ---------------------------------------------------------------- canto pages

def convert_canto(c, first, last, errors):
    total = VERSES[c - 1]
    parts = []
    if first == CANTO_START[0]:
        parts.append(marker(HALF_TITLE))
        parts.extend(join_lines(p, "019") for p in paragraphs(read_page(HALF_TITLE)))
    verse = 0
    printed = []  # (page, printed number, position of its line)
    for n in range(first, last + 1):
        lines = [l for l in read_page(n) if l.strip()]
        parts.append(marker(n))
        if n == first:
            head = lines.pop(0)
            m = re.fullmatch(r"ΩΔΗ (\S+)", head.strip())
            if not m or numeral(m.group(1)) != NUMERALS[c - 1]:
                errors.append(f"{n:03d}: heading {head!r}")
            parts.append(f"# ᾨδὴ {NUMERALS[c - 1]}{KERAIA}")
            arg, lines = split_argument(c, n, lines, errors)
            parts.append(arg)
        out = []
        tail = []
        for k, l in enumerate(lines):
            s = l.strip()
            letter = re.search(r"[^\W\d_]", s)
            if out and letter and letter.group().islower() and len(s) < 20:
                # a turnover line: the end of a long verse, set on the next line (`069`)
                TURNOVER.append(f"{n:03d}: {out[-1][1][-30:]} | {s}")
                out[-1] = (out[-1][0], join_lines([out[-1][1], s], f"{n:03d}"))
                continue
            if verse >= total:
                tail = lines[k:]
                break
            if ORNAMENT.fullmatch(s):
                errors.append(f"{n:03d}: ornament in the verse: {s}")
                continue
            m = re.match(r"(\d+)\s*(.*)", s)
            num = None
            if m:
                num, s = int(m.group(1)), m.group(2)
                if not s:
                    printed.append((n, num, verse + 0.5))  # a number on a line of its own
                    continue
            verse += 1
            if num is not None:
                printed.append((n, num, verse))
            out.append((verse, s))
        if out:
            parts.append("\\\n".join(f"{s} {i}" if i % 5 == 0 else s for i, s in out))
        for p in paragraphs(tail):
            parts.append(join_lines(p, f"{n:03d}"))
            if not (n == CANTO_END and p == ["ΤΕΛΟΣ."]):
                errors.append(f"{n:03d}: text after the last verse: {p[0][:40]}")
    if verse != total:
        errors.append(f"canto {c}: {verse} verses, expected {total}")
    PRINTED.extend((c, n, num, pos) for n, num, pos in printed)
    return parts


TURNOVER = []
PRINTED = []  # (canto, page, printed number, position of its line)
ARG_CHECK = []
# Arguments printed differently in the TOC, checked against the images:
# αἱρετικοί— / αἱρετικοί.— (10), μετὰ / κατὰ (22), ἔννατον / ἕνατον (31)
ARG_CHECKED = {10, 22, 31}


def split_argument(c, n, lines, errors):
    """The argument at the top of a canto's first page, found by its length in the TOC."""
    toc_text = TOC[c][0]
    want = len(plain(toc_text))
    arg = []
    k = 0
    while k < len(lines) and ORNAMENT.fullmatch(lines[k].strip()):
        k += 1
    while k < len(lines) and len(plain(" ".join(arg))) < want - 3:
        arg.append(lines[k].strip())
        k += 1
    while k < len(lines) and ORNAMENT.fullmatch(lines[k].strip()):
        k += 1
    text = join_lines(arg, f"{n:03d}")
    ratio = SequenceMatcher(None, plain(text), plain(toc_text)).ratio()
    if ratio < 1 and c not in ARG_CHECKED:
        ARG_CHECK.append(f"{n:03d} canto {c} ({ratio:.3f}):\n    page: {text}\n    toc:  {toc_text}")
    if ratio < 0.9:
        errors.append(f"{n:03d}: argument differs from the TOC ({ratio:.2f})")
    if TOC[c][1] != n - 20:
        errors.append(f"canto {c}: TOC page {TOC[c][1]}, scan {n:03d}")
    return text, lines[k:]


# ---------------------------------------------------------------- notes

NOTE_START = re.compile(r"(\d+(?:\s?[-–,]\s?\d+)*)\.\s")
NOTE_HEAD = re.compile(r"Εἰς [ᾨᾠὨ]δὴν (\S+)")
HEAD_CHECK = []
HEAD_MISPRINTED = {298, 299}  # the running head says Ε΄ over the notes to canto 6
CONTINUED_CHECK = []  # a paragraph continued from the previous page after a blank line
NUMBER_IN_NOTE = []  # lines starting with a number that cannot start a note
NUMBER_CHECKED = {"318"}  # a year at the start of a line inside a note (`1300. Ὁ Γ. Βιλλάνης`)
UNNUMBERED = []  # note paragraphs after a blank line without a line number
NOTE_ERRORS = []


# Quotations in verse, set off inside a note (by their first words): the number of
# printed lines, with a citation set on a line of its own; they keep their lines.
NOTE_VERSE = {
    "“The sun to me": 4, "“ Ὁ δ᾽ εὐτυχήσας": 2, "“Non secus": 2, "“Ὄλβιος ὃς": 2,
    "“ Σκιρτᾷ δ᾽": 2, "“ Quales mugitus": 3, "“Io credo": 1, ". . . tremuere": 3,
    "“ Πολλῶν δ᾽": 1, "“ Qui mores": 1, "“Tolle moras": 1,
}
# Note paragraphs without a number, checked against the images (by their first words).
NOTE_UNNUMBERED = ["Ἀσδέντης,", "“Οἱ δὲ Γίγαντες", "Πέτρα Ἀπουάνα", "Τύποις CLAYTON"]
VERSE = "\0"  # marks a line of verse among the lines of a note


def render_note(lines, where):
    """Join the lines of a note; the lines of verse keep their breaks."""
    out, prose = [], []
    for l in lines + [None]:
        if l is None or l.startswith(VERSE):
            if prose:
                out.append(esc(join_lines(prose, where)))
                prose = []
            if l is not None:
                out.append(esc(l[1:]))
        else:
            prose.append(l)
    return "\\\n".join(out)


def convert_notes(errors):
    parts = []
    canto = 0
    last_num = 0  # the last line number with a note in the canto
    cur = None  # [index in parts, printed lines, first page] of the paragraph being read
    footnotes = []

    def flush():
        if cur:
            parts[cur[0]] = render_note(cur[1], cur[2])

    for n in NOTES:
        where = f"{n:03d}"
        lines = read_page(n, head=False)
        # the label at the top is the running head unless it opens the next canto
        top = next((k for k, l in enumerate(lines[:3]) if NOTE_HEAD.fullmatch(l.strip())), None)
        if top is not None:
            c = numeral(NOTE_HEAD.fullmatch(lines[top].strip()).group(1))
            if canto == 34 or c != NUMERALS[canto]:
                if c != NUMERALS[canto - 1] and n not in HEAD_MISPRINTED:
                    HEAD_CHECK.append(f"{where}: running head {lines[top].strip()}"
                                      f" in the notes to canto {canto}")
                del lines[top]
        parts.append(marker(n))
        if n == 287:
            parts.extend(join_lines(p, where) for p in paragraphs(lines))
            continue
        # a footnote at the foot of the page: from a line starting with `*` to the end;
        # its marker (`Ἱερεμίου,*`, `Νεμβρώδ,*)`) becomes a reference
        foot = next((k for k, l in enumerate(lines) if re.match(r"\*\)? ", l)), None)
        if foot is not None:
            label = f"[^{n - 20}-1]"
            text = join_lines([l.strip() for l in lines[foot:] if l.strip()], where)
            footnotes.append(f"{label}: " + re.sub(r"^\*\)? ", "", text))
            lines = lines[:foot]
            k = next(k for k, l in enumerate(lines) if re.search(r"\S\*\)?", l))
            lines[k] = re.sub(r"(?<=\S)\*\)?", label, lines[k], count=1)
        blank = False
        first = True  # the first text of the page
        verse = 0  # lines of verse still to come
        for l in lines:
            s = l.strip()
            if not s:
                blank = not first  # not the space left by the running head
                continue
            v = next((k for k in NOTE_VERSE if s.startswith(k)), None)
            if v or verse:
                # verse belongs to the note it is quoted in, across a blank line
                verse = NOTE_VERSE[v] if v else verse
                verse -= 1
                cur[1].append(VERSE + s)
                blank = first = False
                continue
            m = NOTE_HEAD.fullmatch(s)
            start = NOTE_START.match(s)
            if start:
                nums = [int(x) for x in re.findall(r"\d+", start.group(1))]
                fits = canto and last_num < nums[0] and nums[-1] <= VERSES[canto - 1]
                if not fits and not blank and not first:
                    if where not in NUMBER_CHECKED:
                        NUMBER_IN_NOTE.append(f"{where}: {s[:50]}")
                    start = None
            if s in HEADINGS:
                flush()
                parts.append(f"# {HEADINGS[s]}")
                cur = None
            elif m:
                flush()
                c = NUMERALS.index(numeral(m.group(1))) + 1 if numeral(m.group(1)) else None
                if c != canto + 1:
                    NOTE_ERRORS.append(f"{where}: heading {s} after canto {canto}")
                canto = c or canto + 1
                last_num = 0
                parts.append(f"## Εἰς ᾨδὴν {NUMERALS[canto - 1]}{KERAIA}")
                cur = None
            elif start or blank or cur is None or s == "ΤΕΛΟΣ ΤΩΝ ΣΗΜΕΙΩΣΕΩΝ.":
                if start:
                    if not fits:
                        NOTE_ERRORS.append(f"{where}: note {start.group(1)} in canto {canto}"
                                           f" after {last_num} (verses {VERSES[canto - 1]})")
                    last_num = max(last_num, nums[-1])
                elif first and cur is not None:
                    # a paragraph continued from the previous page
                    if blank:
                        CONTINUED_CHECK.append(f"{where}: {s[:50]}")
                    cur[1].append(s)
                    blank = first = False
                    continue
                elif s != "ΤΕΛΟΣ ΤΩΝ ΣΗΜΕΙΩΣΕΩΝ." and not any(s.startswith(k) for k in NOTE_UNNUMBERED):
                    UNNUMBERED.append(f"{where}: {s[:50]}")
                flush()
                parts.append(None)
                cur = [len(parts) - 1, [s], where]
            else:
                cur[1].append(s)
            blank = first = False
        flush()
        parts.extend(footnotes)
        footnotes = []
    if canto != 34:
        NOTE_ERRORS.append(f"notes end in canto {canto}")
    errors.extend(NOTE_ERRORS)
    return parts


# ---------------------------------------------------------------- front matter

def render_lines(p):
    return "\\\n".join(esc(l.strip()) for l in p)


def convert_front(slug, pages):
    parts = []
    for n in pages:
        parts.append(marker(n))
        lines = read_page(n)
        if slug == "table-of-contents":
            convert_toc_page(n, lines, parts)
            continue
        for p in paragraphs(lines):
            s = " ".join(p)
            if s in HEADINGS:
                parts.append(f"# {HEADINGS[s]}")
            elif slug == "title-page":
                parts.append(render_lines(p))
            elif p[0].startswith("|"):
                parts.append("\n".join(p))
            elif n == 15 and s.startswith("Διορθώσεις"):
                parts.append("# " + join_lines(p, f"{n:03d}").rstrip("."))
            elif slug == "prologos" and n == 7 and s.startswith("Ἐν Λονδίνῳ"):
                parts.append(render_lines(p))
            else:
                parts.append(esc(join_lines(p, f"{n:03d}")))
    return parts


def convert_toc_page(n, lines, parts):
    entry = []
    out = ["Σελ."]  # the column head, printed on every page
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s in ("ΠΙΝΑΞ ΤΩΝ ΕΝ ΕΚΑΣΤΗι ΩΔΗι", "Σελ."):
            continue
        if s == "ΠΕΡΙΕΧΟΜΕΝΩΝ.":
            parts.append(f"# {HEADINGS['ΠΙΝΑΞ ΤΩΝ ΕΝ ΕΚΑΣΤΗι ΩΔΗι ΠΕΡΙΕΧΟΜΕΝΩΝ.']}")
            continue
        entry.append(s)
        if re.search(r"\d+$", s):
            text = join_lines(entry, f"{n:03d}")
            text = re.sub(r"\s*(?:\. ?)*\.?\s*(\d+)$", r" . . . \1", text)
            out.append(text)
            entry = []
    parts.extend(out)


# ---------------------------------------------------------------- main

def write(num, slug, parts):
    path = DST / f"{num:03d}-{slug}.md"
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main():
    DST.mkdir(parents=True, exist_ok=True)
    errors = []
    num = 0
    for slug, pages in FRONT:
        num += 1
        write(num, slug, convert_front(slug, pages))
    for c, first in enumerate(CANTO_START, 1):
        last = CANTO_START[c] - 1 if c < len(CANTO_START) else CANTO_END
        num += 1
        write(num, f"canto-{c:02d}", convert_canto(c, first, last, errors))
    num += 1
    write(num, "notes", convert_notes(errors))
    for e in errors:
        print("ERROR", e)
    # printed line numbers: only where the offset to the counted position changes
    offsets = {}
    for c, n, num_, pos in PRINTED:
        prev = offsets.get(c, 0)
        off = pos - num_
        if off != prev:
            print(f"LINE NUMBER canto {c} {n:03d}: printed {num_} at line {pos}"
                  f" (offset {prev:+g} -> {off:+g})")
            offsets[c] = off if abs(off) < 10 else prev  # a misread number
    for c, off in offsets.items():
        if off:
            print(f"LINE NUMBER canto {c}: offset {off:+g} at the end")
    for x in TURNOVER:
        print("TURNOVER", x)
    for x in ARG_CHECK:
        print("ARGUMENT", x)
    for u in dict.fromkeys(UNDECIDED):
        print("HYPHEN", u)
    for x in HEAD_CHECK:
        print("NOTES HEAD", x)
    for x in CONTINUED_CHECK:
        print("CONTINUED AFTER BLANK", x)
    for x in NUMBER_IN_NOTE:
        print("NUMBER INSIDE NOTE", x)
    for x in UNNUMBERED:
        print("UNNUMBERED NOTE PARAGRAPH", x)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
