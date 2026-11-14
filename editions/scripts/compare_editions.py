"""
Collect the differences between the editions of the Inferno, as material for
the reports in editions/ (which are written from it by hand: the script
sorts out what can be told mechanically and lists the rest for reading).

- it: the Italian of dante-corpus against the Italian printed in Carlyle's
  edition (texts/en, 1889), line by line, with Oelsner's Italian
  (texts/en-oelsner, 1903) beside them. Each line is sorted by its first
  kind of difference: identical; orthography only (the same letters once
  accents, apostrophes, case, punctuation, and word division are left
  aside); word forms only (every differing segment close in spelling, such
  as luogo / loco); or other words. The counts of the orthographic features
  and of the form pairs are printed, then every segment of other words.
- en: Carlyle's English (texts/en) against Oelsner's revision of it
  (texts/en-oelsner), word by word over each canto. Each difference is
  placed in the page of Carlyle's edition where it falls (the page's lines),
  and sorted: punctuation, case, spelling (close in spelling), marked
  (Oelsner's [ ] marks), and substituted, inserted, or deleted words. The
  counts are printed, then every word difference with its context and the
  lines of the page where the Italian of the two editions differs: in other
  words, or in forms close in spelling (marked as such), which may hide two
  words (tremesse / temesse, colpo / colpa); elided forms are left out. The
  English of the page missing from Oelsner's edition (canto XXXIV) is left
  out.
"""

import argparse
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

# The scripts shared with the commentaries
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "commentary" / "scripts"))

from source import (Passage, carlyle_passages, oelsner_lines, oelsner_passages,
                    source_lines)

CANTOS = range(1, 35)
# A run of Carlyle's English this long with nothing in Oelsner's, in a canto
# with lines missing from Oelsner's edition, is the English of the missing
# page, not a deletion
MISSING_RUN = 40
# Segments at least this close (difflib ratio of their letters) are taken as
# forms of the same word (luogo / loco, duo / due, ale / ali); so are an
# elided or apocopated word and its full form (il / l, io / i, ed / e,
# che / ch), and the pairs below, whose letters are not close
FORM_RATIO = 0.66
FORM_PAIRS = {("ei", "el"), ("ei", "e"), ("de", "d i"), ("ch", "c")}


def plain(text: str) -> str:
    """Lower case, without accents."""
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def it_words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", plain(text))


def segments(a: list[str], b: list[str]):
    """(a segment, b segment) of every difference between two word lists."""
    for op, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            yield " ".join(a[i1:i2]), " ".join(b[j1:j2])


def form_kind(a: str, b: str) -> str | None:
    """How two segments are forms of the same word: "elided" (an elided or
    apocopated form, or a pair of FORM_PAIRS), "close" (close in spelling
    only, which may also be two words: tremesse / temesse, colpo / colpa),
    or None (other words)."""
    if not (a and b):
        return None
    if (a, b) in FORM_PAIRS or (b, a) in FORM_PAIRS:
        return "elided"
    x, y = a.replace(" ", ""), b.replace(" ", "")
    short, full = sorted((x, y), key=len)
    if full.startswith(short) or full.endswith(short):
        return "elided"
    return "close" if SequenceMatcher(None, x, y).ratio() >= FORM_RATIO else None


def is_form(a: str, b: str) -> bool:
    return form_kind(a, b) is not None


# Orthographic features of a line pair (Carlyle, dante-corpus)
FEATURES = {
    "quotation marks in dante-corpus only":
        lambda c, d: bool(re.search(r"[«»“”]", d)) and not re.search(r"[«»“”]", c),
    "capital at the line start in Carlyle only":
        lambda c, d: c[:1].isupper() and not d[:1].isupper(),
    "space after the apostrophe in Carlyle (l’ alto)":
        lambda c, d: bool(re.search(r"\w’ \w", c)),
    "accents differ":
        lambda c, d: plain(c) == plain(d) and c.lower() != d.lower()
        or [w for w in re.findall(r"\w+", c.lower()) if plain(w) != w]
        != [w for w in re.findall(r"\w+", d.lower()) if plain(w) != w],
    "preposition and article in one word in Carlyle (della / de la)":
        lambda c, d: any(
            a.replace(" ", "") == b.replace(" ", "") and " " in b and " " not in a
            for a, b in segments(it_words(c), it_words(d))),
}


def compare_it(out):
    kinds = Counter()
    features = Counter()
    forms = Counter()
    others = []
    for canto in CANTOS:
        carlyle = source_lines("en", "inferno", canto)
        corpus = source_lines("it", "inferno", canto)
        oelsner = {line.no: line.text for line in oelsner_lines(canto)}
        for c, d in zip(carlyle, corpus):
            for name, test in FEATURES.items():
                features[name] += test(c.text, d.text)
            if c.text == d.text:
                kinds["identical"] += 1
                continue
            wc, wd = it_words(c.text), it_words(d.text)
            if "".join(wc) == "".join(wd):
                kinds["orthography only"] += 1
                continue
            diffs = list(segments(wc, wd))
            other = [(a, b) for a, b in diffs if not is_form(a, b)]
            for a, b in diffs:
                if is_form(a, b):
                    forms[(a, b)] += 1
            if not other:
                kinds["word forms only"] += 1
                continue
            kinds["other words" if any(a and b for a, b in other)
                  else "a word present in one only"] += 1
            for a, b in other:
                others.append((canto, c.no, a, b, c.text, d.text,
                               oelsner.get(c.no, "(missing)")))
    print("# Lines by their first kind of difference", file=out)
    for kind, count in kinds.items():
        print(f"{kind}\t{count}", file=out)
    print("\n# Orthographic features (lines)", file=out)
    for name, count in features.items():
        print(f"{name}\t{count}", file=out)
    print(f"\n# Form pairs, Carlyle / dante-corpus ({sum(forms.values())} in "
          f"{len(forms)} pairs)", file=out)
    for (a, b), count in forms.most_common():
        print(f"{count}\t{a} / {b}", file=out)
    print(f"\n# Other words ({len(others)} segments): canto:line, Carlyle / "
          f"dante-corpus, then the lines of Carlyle, dante-corpus, Oelsner", file=out)
    for canto, no, a, b, c, d, o in others:
        print(f"{canto}:{no}\t{a or '-'} / {b or '-'}\n\tC {c}\n\tD {d}\n\tO {o}",
              file=out)


# An English token: a word (with inner apostrophes), or a punctuation mark
EN_TOKEN_RE = re.compile(r"\w+(?:['’]\w+)*|[^\w\s\[\]]")


def en_tokens(text: str) -> list[tuple[str, bool]]:
    """(token, inside Oelsner's [ ] marks) of an English text."""
    tokens = []
    marked = False
    text = re.sub(r"[_*]", "", text)  # italics, marked in texts/en-oelsner only
    for part in re.split(r"(\[|\])", text):
        if part in "[]" and part:
            marked = part == "["
            continue
        tokens += [(t.replace("'", "’"), marked) for t in EN_TOKEN_RE.findall(part)]
    return tokens


def is_word(token: str) -> bool:
    return token[0].isalnum()


@dataclass
class EnDifference:
    """One difference between Carlyle's English (ca) and Oelsner's (ob, with
    the marks) of a canto: the tokens ca[i1:i2] and ob[j1:j2], on the page
    of Carlyle's edition where it falls."""
    canto: int
    page: Passage
    i1: int
    i2: int
    j1: int
    j2: int
    ca: list[str]
    ob: list[tuple[str, bool]]
    kind: str
    marked: bool


# The kinds of difference that are not differences of words
NOT_WORDS = ("punctuation", "case or punctuation with case",
             "left out: English of a page missing from Oelsner's edition")


def en_differences():
    """Every difference between Carlyle's English and Oelsner's, canto by
    canto, in the order of the text."""
    for canto in CANTOS:
        pages = carlyle_passages(canto)
        gap = len(oelsner_lines(canto)) < len(source_lines("en", "inferno", canto))
        ca: list[str] = []
        page_of: list[int] = []
        for index, page in enumerate(pages):
            tokens = [t for t, _ in en_tokens(page.english)]
            ca += tokens
            page_of += [index] * len(tokens)
        ob = [t for p in oelsner_passages(canto) for t in en_tokens(p.english)]
        words_b = [t for t, _ in ob]
        for op, i1, i2, j1, j2 in SequenceMatcher(None, ca, words_b,
                                                  autojunk=False).get_opcodes():
            if op == "equal":
                continue
            a, b = ca[i1:i2], words_b[j1:j2]
            if gap and op == "delete" and len(a) > MISSING_RUN:
                kind = NOT_WORDS[2]
            elif not any(map(is_word, a + b)):
                kind = "punctuation"
            elif [t.lower() for t in a if is_word(t)] == [t.lower() for t in b if is_word(t)]:
                kind = "case or punctuation with case"
            elif op == "replace" and is_form(" ".join(a).lower(), " ".join(b).lower()):
                kind = "spelling or close form"
            else:
                kind = {"replace": "substituted", "insert": "inserted",
                        "delete": "deleted"}[op]
            yield EnDifference(canto, pages[page_of[min(i1, len(page_of) - 1)]],
                               i1, i2, j1, j2, ca, ob, kind,
                               any(m for _, m in ob[j1:j2]))


def word_differences() -> list[EnDifference]:
    """The differences in words, numbered from 1 in this order in the output
    of compare_en and in the judgments of render_editions.py."""
    return [d for d in en_differences() if d.kind not in NOT_WORDS]


def compare_en(out):
    kinds = Counter()
    listed = []
    lines = {}
    for d in en_differences():
        kinds[d.kind] += 1
        if d.kind == NOT_WORDS[2]:
            continue
        kinds["marked [ ]" if d.marked else "unmarked"] += 1
        if d.kind in NOT_WORDS:
            continue
        if d.canto not in lines:
            lines[d.canto] = (
                {line.no: line.text for line in source_lines("en", "inferno", d.canto)},
                {line.no: line.text for line in oelsner_lines(d.canto)})
        c_lines, o_lines = lines[d.canto]
        a = d.ca[d.i1:d.i2]
        b = [t for t, _ in d.ob[d.j1:d.j2]]
        context = " ".join(d.ca[max(0, d.i1 - 6):d.i1]) + " [" + " ".join(a) + "] " \
            + " ".join(d.ca[d.i2:d.i2 + 6])
        italian = []
        for no in range(d.page.start, d.page.end + 1):
            if no not in o_lines:
                continue
            kinds_ = [(form_kind(x, y), x, y) for x, y in
                      segments(it_words(c_lines[no]), it_words(o_lines[no]))]
            row = f"{no}: C {c_lines[no]} | O {o_lines[no]}"
            if any(kind is None for kind, _, _ in kinds_):
                italian.append(row)
            elif close := [f"{x} / {y}" for kind, x, y in kinds_ if kind == "close"]:
                italian.append(f"{row}  (close forms: {', '.join(close)})")
        listed.append((d.canto, d.page.start, d.page.end, d.kind, d.marked,
                       " ".join(a) or "-", " ".join(b) or "-", context, italian))
    print("# Differences by kind (a difference is counted once by kind, "
          "and once as marked or unmarked)", file=out)
    for kind, count in kinds.items():
        print(f"{kind}\t{count}", file=out)
    print(f"\n# Word differences ({len(listed)}): canto, Carlyle's page lines, kind, "
          f"Carlyle / Oelsner, Carlyle's context, Italian lines of the page that "
          f"differ in other words or in forms close in spelling, which may be "
          f"other words too (C Carlyle, O Oelsner)", file=out)
    for canto, start, end, kind, marked, a, b, context, italian in listed:
        mark = " [marked]" if marked else ""
        print(f"{canto}:{start}-{end}\t{kind}{mark}\t{a} / {b}\n\t{context}", file=out)
        for row in italian:
            print(f"\t\t{row}", file=out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("mode", choices=["it", "en"],
                        help="it: the Italian of dante-corpus and Carlyle; "
                             "en: the English of Carlyle and Oelsner")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=sys.stdout,
                        help="Output file (default: standard output)")
    args = parser.parse_args()
    {"it": compare_it, "en": compare_en}[args.mode](args.output)


if __name__ == "__main__":
    main()
