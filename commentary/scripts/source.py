"""
The original text of a canto, line by line, from one of the sources:

- it: the Italian text of dante-corpus (all three canticles)
- grc: Musurus's Greek verse translation of the Inferno (1882), read from
  texts/grc/ of this repository; it is line for line, so Greek line n
  renders Italian line n and every canto has the line count of the Italian

Each line has .no (the line number) and .text, as the lines of dante-corpus.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from dante_corpus import ref

GRC_DIR = Path(__file__).resolve().parents[2] / "texts" / "grc"

# Per source:
# - name: the name of the source text, as written into the prompts
# - canticles: the canticles the source covers
SOURCES = {
    "it": {
        "name": "Italian text",
        "canticles": ["inferno", "purgatorio", "paradiso"],
    },
    "grc": {
        "name": "Ancient Greek verse translation (by Constantine Musurus, 1882)",
        "canticles": ["inferno"],
    },
}


@dataclass
class Line:
    no: int
    text: str


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


def source_lines(source: str, canticle: str, canto: int) -> list[Line]:
    if canticle not in SOURCES[source]["canticles"]:
        raise ValueError(f"source {source} has no {canticle}")
    if source == "grc":
        return grc_lines(canto)
    return [Line(line.no, line.text) for line in ref(f"{canticle} {canto}")]
