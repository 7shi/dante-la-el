"""
The original text of a canto, line by line, from one of the sources:

- it: the Italian text of dante-corpus (all three canticles)
- grc: Musurus's Greek verse translation of the Inferno (1882), read from
  texts/grc/ of this repository; it is line for line, so Greek line n
  renders Italian line n and every canto has the line count of the Italian
- en: the Italian text printed in Carlyle's Inferno (1889), read from
  texts/en/ of this repository; its lines are those of dante-corpus (with
  the readings and the spelling of that edition), and it comes with
  Carlyle's own English prose translation, so it is only explained
  (grammar.py), never translated or checked
- en-oelsner: the Italian text printed in the Temple Classics Inferno (1903),
  read from texts/en-oelsner/ of this repository, with Oelsner's own readings,
  and with the English prose translation printed with it (Carlyle's, revised
  by Oelsner), so it is only explained (grammar.py), as en
- en-purgatorio, en-paradiso: the Italian text of the Temple Classics
  Purgatorio (1904) and Paradiso (1910), read from texts/en-purgatorio/ and
  texts/en-paradiso/, edited by Oelsner as the Inferno and printed in the
  same layout with an English prose translation (Okey's of the Purgatorio,
  Wicksteed's of the Paradiso), so they are only explained, as en-oelsner

Each line has .no (the line number) and .text, as the lines of dante-corpus.

The editions printed with an English translation are also read passage by
passage (Passage: a range of lines, their Italian, and the English that
renders them):

- carlyle_passages: texts/en, one passage per page, the verse printed on
  the page and the English prose above it; the English is cut where the
  page ends, often in mid-sentence, so at a page break it may run a clause
  or a few lines ahead of the verse or behind it
- carlyle_blocks: texts/en in blocks whose English renders exactly their
  verse, cut near every page break as editions/en-blocks.txt gives
  (checked by hand; see scripts/align_carlyle.py)
- oelsner_passages: texts/en-oelsner, texts/en-purgatorio, or
  texts/en-paradiso (the Temple Classics, with Oelsner's Italian text and
  the English facing it), one passage per spread: the English is printed
  one paragraph per tercet, facing the Italian
"""

import re
from dataclasses import dataclass
from pathlib import Path

from dante_corpus import ref

TEXTS_DIR = Path(__file__).resolve().parents[2] / "texts"
GRC_DIR = TEXTS_DIR / "grc"
CARLYLE_DIR = TEXTS_DIR / "en"
# The Temple Classics volumes, per source: the same layout in all three
OELSNER_DIRS = {source: TEXTS_DIR / source
                for source in ("en-oelsner", "en-purgatorio", "en-paradiso")}
# The cuts of Carlyle's pages into blocks (see editions/scripts/align_carlyle.py)
BLOCKS_PATH = Path(__file__).resolve().parents[2] / "editions" / "en-blocks.txt"

# Per source:
# - name: the name of the source text, as written into the prompts
# - language: the language of the source text, as written into the prompts
# - canticles: the canticles the source covers
# - prose: (optional) the English prose translation printed with the source,
#   as written into the prompts; such a source is explained against it, and
#   is not translated or checked
SOURCES = {
    "it": {
        "name": "Italian text",
        "language": "Italian",
        "canticles": ["inferno", "purgatorio", "paradiso"],
    },
    "grc": {
        "name": "Ancient Greek verse translation (by Constantine Musurus, 1882)",
        "language": "Ancient Greek",
        "canticles": ["inferno"],
    },
    "en": {
        "name": "Italian text (as printed in John A. Carlyle's edition, 1889)",
        "language": "Italian",
        "canticles": ["inferno"],
        "prose": "English prose translation by John A. Carlyle (1889)",
    },
    "en-oelsner": {
        "name": "Italian text (as edited by H. Oelsner in the Temple Classics, 1903)",
        "language": "Italian",
        "canticles": ["inferno"],
        "prose": "English prose translation by John A. Carlyle, revised by H. Oelsner "
                 "(1903; his revisions are in square brackets)",
    },
    "en-purgatorio": {
        "name": "Italian text (as edited by H. Oelsner in the Temple Classics, 1904)",
        "language": "Italian",
        "canticles": ["purgatorio"],
        "prose": "English prose translation by Thomas Okey (1904)",
    },
    "en-paradiso": {
        "name": "Italian text (as edited by H. Oelsner in the Temple Classics, 1910)",
        "language": "Italian",
        "canticles": ["paradiso"],
        "prose": "English prose translation by Philip H. Wicksteed (1910)",
    },
}
# The sources that are translated (into <lang>/ or <lang>-<source>/)
TRANSLATED_SOURCES = [name for name, source in SOURCES.items()
                      if "prose" not in source]


@dataclass
class Line:
    no: int
    text: str


@dataclass
class Passage:
    start: int
    end: int
    lines: list[Line]
    english: str


# The number printed at the end of every fifth verse line (`… στυγήρης, 5`)
NUMBER_RE = re.compile(r"\s+(\d+)$")
# The last line of the Inferno, after canto XXXIV
END_MARK = "ΤΕΛΟΣ."


def grc_lines(canto: int) -> list[Line]:
    """The verse of one canto of texts/grc: everything after the heading and
    the argument, without the page comments, the line-end backslashes, and
    the line numbers."""
    (path,) = GRC_DIR.glob(f"*-canto-{canto:02d}.md")
    lines: list[Line] = []
    heading = argument = False
    for raw in path.read_text().splitlines():
        text = raw.rstrip("\\").strip()
        if not text or text.startswith("<!--"):
            continue
        if not heading:
            heading = text.startswith("# ")
            continue
        if not argument:
            argument = True  # the first paragraph after the heading
            continue
        if text == END_MARK:
            continue
        if match := NUMBER_RE.search(text):
            number = int(match.group(1))
            if number != len(lines) + 1:
                raise ValueError(f"{path}: line {len(lines) + 1} numbered {number}")
            text = text[: match.start()]
        lines.append(Line(len(lines) + 1, text))
    return lines


# A comment such as the page marker `<!-- p. 2 (056) -->`
COMMENT_RE = re.compile(r"\s*<!--.*?-->")
# A paragraph of texts/en that is not verse: a footnote, a heading, or an
# indented quotation inside a note
NOT_VERSE = ("[^", "#", " ")
# Italian verse lines are shorter than this; English prose lines are longer
MAX_VERSE = 60


def verse_block(paragraph: str) -> list[str]:
    """The verse lines of one paragraph of texts/en, or [] if it is not verse.

    A verse block (one per page, see texts/PLAN.md) has short lines, every
    one but the last ending with the hard break `\\`; a block of one line is
    either indented (`&emsp;`) or numbered (a canto's last line, set alone).
    """
    rows = [row for row in (COMMENT_RE.sub("", row) for row in paragraph.splitlines())
            if row.strip()]
    if not rows or rows[0].startswith(NOT_VERSE):
        return []
    if any(not row.endswith("\\") for row in rows[:-1]):
        return []
    texts = [row.removesuffix("\\").removeprefix("&emsp;").strip() for row in rows]
    if any(len(text) > MAX_VERSE for text in texts):
        return []
    if len(rows) == 1 and not (rows[0].startswith("&emsp;") or NUMBER_RE.search(texts[0])):
        return []
    return texts


# A page marker: `<!-- p. 2 (056) -->`, `<!-- p. [1] (013) -->`, or in
# texts/en-oelsner with its band, `<!-- p. 2 (014), text -->`
PAGE_RE = re.compile(r"^<!-- p\. \[?(\d+)\]?[^,>]*(?:, (\w+))? -->$")
# A footnote reference of texts/en, `[^2-1]`
FOOTNOTE_REF_RE = re.compile(r"\[\^\d+-\d+\]")
# A verse note of texts/en, `40\. Bruno, brown, …`
VERSE_NOTE_RE = re.compile(r"^\d+\\\.")
# The last line of texts/en, after canto XXXIV
CARLYLE_END = "END OF THE INFERNO."


def paragraphs(text: str) -> list[tuple[int | None, str | None, str]]:
    """(page, band, paragraph) of every paragraph of a texts file, with the
    page and the band (None if not named) of the last page marker before it."""
    result = []
    page = band = None
    for paragraph in re.split(r"\n\s*\n", text):
        # Keep the indentation: an indented paragraph is a quotation in a note
        paragraph = paragraph.strip("\n").rstrip()
        if match := PAGE_RE.match(paragraph):
            page, band = int(match.group(1)), match.group(2)
        elif paragraph:
            result.append((page, band, paragraph))
    return result


def is_prose(paragraph: str) -> bool:
    """An English paragraph: not a heading, a footnote, a verse note, an
    indented quotation, a comment, or verse."""
    return (not paragraph.startswith(NOT_VERSE + ("<!--",))
            and not VERSE_NOTE_RE.match(paragraph)
            and not verse_block(paragraph))


def english(paragraph: str) -> str:
    """A paragraph as plain text: without comments, footnote references, and
    hard line breaks."""
    text = FOOTNOTE_REF_RE.sub("", COMMENT_RE.sub("", paragraph))
    return " ".join(row.removesuffix("\\").strip() for row in text.splitlines())


def numbered(lines: list[Line], text: str, path: Path, resync: bool) -> Line:
    """The next verse line, numbered by the count of lines so far. A printed
    number must match the count, or, with resync, sets it (after a gap)."""
    no = lines[-1].no + 1 if lines else 1
    if match := NUMBER_RE.search(text):
        number = int(match.group(1))
        if number != no and not resync:
            raise ValueError(f"{path}: line {no} numbered {number}")
        no, text = number, text[: match.start()]
    return Line(no, text)


def carlyle_passages(canto: int) -> list[Passage]:
    """One passage per page of texts/en: the verse printed on the page and
    the English prose above it. The pages before the first verse (the
    argument) are left out."""
    (path,) = CARLYLE_DIR.glob(f"*-canto-{canto:02d}.md")
    pages: dict[int, tuple[list[Line], list[str]]] = {}
    lines: list[Line] = []
    for page, _, paragraph in paragraphs(path.read_text()):
        verse, prose = pages.setdefault(page, ([], []))
        if texts := verse_block(paragraph):
            for text in texts:
                lines.append(numbered(lines, text, path, False))
                verse.append(lines[-1])
        elif is_prose(paragraph) and paragraph != CARLYLE_END:
            prose.append(english(paragraph))
    passages = []
    for page, (verse, prose) in pages.items():
        if not passages and not verse:
            continue  # the argument
        if not verse or not prose:
            raise ValueError(f"{path}: p. {page} has no {'prose' if verse else 'verse'}")
        passages.append(Passage(verse[0].no, verse[-1].no, verse, " ".join(prose)))
    return passages


def carlyle_english(passages: list[Passage]) -> tuple[str, list[int]]:
    """The English of the pages in one text, and the position in it where
    each page's English ends."""
    text, ends = "", []
    for passage in passages:
        if text and not text.endswith("—"):
            text += " "
        text += passage.english
        ends.append(len(text))
    return text, ends


def cut_positions(text: str, spec: str) -> list[int]:
    """The positions in text of the cut marked | in spec, `words before|words
    after`, whitespace aside."""
    before, after = spec.split("|")
    pattern = r"\s+".join(map(re.escape, before.split())) + r"(?=\s+" \
        + r"\s+".join(map(re.escape, after.split())) + ")"
    return [m.end() for m in re.finditer(pattern, text)]


def carlyle_blocks(canto: int, path: Path | None = None) -> list[Passage]:
    """The blocks of one canto of texts/en: lines of the Italian and the
    English that renders them, cut as editions/en-blocks.txt gives (see
    scripts/align_carlyle.py)."""
    passages = carlyle_passages(canto)
    text, _ = carlyle_english(passages)
    lines = [line for passage in passages for line in passage.lines]
    path = path or BLOCKS_PATH
    cuts = []
    for row in path.read_text().splitlines():
        row = row.split("\t#")[0].rstrip()
        if not row or row.startswith("#") or not row.startswith(f"{canto}:"):
            continue
        spec_line, spec = row.split("\t")
        no = int(spec_line.split(":")[1])
        found = cut_positions(text, spec)
        if len(found) != 1:
            raise ValueError(f"{path}: {spec_line}: the cut `{spec}` occurs {len(found)} times")
        if cuts and (no <= cuts[-1][0] or found[0] <= cuts[-1][1]):
            raise ValueError(f"{path}: {spec_line}: not after the cut before it")
        if no >= lines[-1].no:
            raise ValueError(f"{path}: {spec_line}: not before the last line")
        cuts.append((no, found[0]))
    blocks = []
    first, position = lines[0].no, 0
    for no, cut in cuts + [(lines[-1].no, len(text))]:
        block = [line for line in lines if first <= line.no <= no]
        blocks.append(Passage(first, no, block, text[position:cut].strip()))
        first, position = no + 1, cut
    return blocks


def carlyle_lines(canto: int) -> list[Line]:
    """The Italian verse of one canto of texts/en, without the English prose,
    the notes, the page comments, the indentation, and the line numbers."""
    return [line for passage in carlyle_passages(canto) for line in passage.lines]


def oelsner_passages(canto: int, source: str = "en-oelsner") -> list[Passage]:
    """One passage per spread of a Temple Classics volume (source: en-oelsner,
    en-purgatorio, or en-paradiso): the Italian of an even
    page and the English of the odd page facing it, which renders exactly
    the tercets that begin on the even page (a passage may thus end before
    the last line of its page, or run past it). The argument and the notes
    are left out."""
    lines, italian, english_pages = read_oelsner(canto, source)
    last = lines[-1].no
    by_no = {line.no: line for line in lines}
    # The tercets that begin on each page; the canto's last line, set alone,
    # belongs to the last tercet
    firsts = {page: [line.no for line in verse if line.no % 3 == 1 and line.no != last]
              for page, verse in italian.items()}
    passages = []
    for page, nos in firsts.items():
        if not nos or not (paras := english_pages.get(page + 1)):
            continue  # no tercet begins here
        end = last if nos[-1] + 3 >= last else nos[-1] + 2
        verse = [by_no[no] for no in range(nos[0], end + 1) if no in by_no]
        passages.append(Passage(nos[0], end, verse, " ".join(paras)))
    return passages


def oelsner_lines(canto: int, source: str = "en-oelsner") -> list[Line]:
    """The Italian verse of one canto of a Temple Classics volume."""
    return read_oelsner(canto, source)[0]


def read_oelsner(canto: int, source: str = "en-oelsner"):
    """The verse lines of a canto of a Temple Classics volume (texts/<source>),
    the verse lines of each page, and the English paragraphs of each odd page."""
    (path,) = OELSNER_DIRS[source].glob(f"*-canto-{canto:02d}.md")
    text = path.read_text().split("\n## Notes\n")[0]
    italian: dict[int, list[Line]] = {}
    english_pages: dict[int, list[str]] = {}
    lines: list[Line] = []
    argument = False
    for page, band, paragraph in paragraphs(text):
        if paragraph.startswith("## Argument"):
            argument = True
        elif texts := verse_block(paragraph):
            argument = False
            for row in texts:
                lines.append(numbered(lines, row, path, True))
                italian.setdefault(page, []).append(lines[-1])
        elif band == "text" or not argument:
            argument = False
            if is_prose(paragraph) and page % 2:
                english_pages.setdefault(page, []).append(english(paragraph))
    return lines, italian, english_pages


def source_lines(source: str, canticle: str, canto: int) -> list[Line]:
    if canticle not in SOURCES[source]["canticles"]:
        raise ValueError(f"source {source} has no {canticle}")
    if source == "grc":
        return grc_lines(canto)
    if source == "en":
        return carlyle_lines(canto)
    if source in OELSNER_DIRS:
        return oelsner_lines(canto, source)
    return [Line(line.no, line.text) for line in ref(f"{canticle} {canto}")]
