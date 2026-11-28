"""Hand over the prose of texts/la without its verse, in parts, and check the translations.

split: read texts/{dir}/{file} as `pages.py prepare` gives it (paragraphs joined over the
pages), put a placeholder `<!-- verse N-M -->` in the place of each run of numbered tercet
pairs (the Italian and the Latin of tercets N to M), and cut the result into parts of about
--size characters, at a placeholder, a heading, or a page marker where it can, else between
paragraphs. Each part is written as {stem}-{PP}.md into the output directory. The other
verse (title pages, verse quoted in the prose, scribal verses) stays in the parts and is
translated with its line breaks.

check: compare a translated part with its input: the structure (markers, placeholders,
headings, footnote IDs, verse line counts, paragraphs and their footnote references) must
be the same; each paragraph is listed when it is short for its source (translation/source
length below --min-ratio, which is set by language), when it repeats a paragraph of the
part, or (English only) when it has fewer italic spans than the source, as the lemmas are
kept in italics (titles and quotations may add more).

The verse is put back later from commentary/en-la-la/ by the placeholders.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pages  # noqa: E402

PLACEHOLDER = re.compile(r"^<!-- verse (\d+)-(\d+) -->$")
ITALIC = re.compile(r"(?<![*\w])\*(?!\s)[^*\n]+?(?<!\s)\*(?![*\w])")
MIN_RATIO = {"en": 0.8, "ja": 0.3}


def tercet_pairs(bs):
    """Indexes of the numbered tercet pairs: {Italian index: (number, Latin index)}."""
    out = {}
    for i, b in enumerate(bs[:-1]):
        if not pages.is_verse(b):
            continue
        m = pages.TERCET_NUM.match(b.strip())
        n = bs[i + 1].strip()
        m2 = pages.TERCET_NUM.match(n)
        if m and m2 and pages.is_verse(n) and m.group(1) == m2.group(1):
            out[i] = int(m.group(1))
    return out


def prose(src):
    """The blocks of src with the tercet pairs replaced by placeholders."""
    bs = pages.blocks(pages.prepare(src)[0])
    pairs = tercet_pairs(bs)
    out, i = [], 0
    while i < len(bs):
        if i in pairs:
            first = last = pairs[i]
            i += 2
            while i in pairs:
                last = pairs[i]
                i += 2
            out.append(f"<!-- verse {first}-{last} -->")
        else:
            out.append(bs[i])
            i += 1
    return out


def is_cut(block):
    return bool(PLACEHOLDER.match(block) or block.startswith("#")
                or pages.MARKER.match(block))


def split(bs, size):
    """Cut the blocks into parts of about size characters: a part ends before a
    placeholder, heading, or marker once it has size characters, or anywhere between
    blocks once it has 1.5 × size."""
    parts, cur, n = [], [], 0
    for b in bs:
        if cur and ((n >= size and is_cut(b)) or n >= size * 1.5):
            parts.append(cur)
            cur, n = [], 0
        cur.append(b)
        n += len(b)
    if cur:
        if parts and n < size / 4:
            parts[-1].extend(cur)  # a short tail goes to the part before
        else:
            parts.append(cur)
    return parts


def shape(bs):
    out = []
    for b in bs:
        b = b.strip()
        if b.startswith("<!--"):
            out.append(b)
        elif b.startswith("#"):
            out.append(b.split(" ", 1)[0])
        elif b.startswith("[^"):
            out.append(b.split(":", 1)[0])
        elif pages.is_verse(b):
            out.append(f"V:{len(b.splitlines())}")
        else:
            out.append("P" + "".join(sorted(pages.REF.findall(b))))
    return out


def length(text):
    return len(re.sub(r"\s+", "", text))


def check(source, translated, lang, min_ratio):
    """Return (structure diff, paragraph notes)."""
    import difflib
    a, b = pages.blocks(source), pages.blocks(translated)
    diff = list(difflib.unified_diff(shape(a), shape(b), "input", "translation",
                                     lineterm=""))
    notes = []
    if diff:
        return diff, notes
    seen = {}
    for n, (s, t) in enumerate(zip(a, b), 1):
        if not shape([s])[0].startswith("P"):
            continue
        head = s.strip()[:40].replace("\n", " ")
        ratio = length(t) / max(length(s), 1)
        if length(s) >= 40 and ratio < min_ratio:
            notes.append(f"block {n}: short ({ratio:.2f}): {head}")
        key = re.sub(r"\s+", " ", t.strip())
        if len(key) >= 20 and key in seen:
            notes.append(f"block {n}: same as block {seen[key]}: {head}")
        seen.setdefault(key, n)
        if lang == "en" and len(ITALIC.findall(s)) > len(ITALIC.findall(t)):
            notes.append(f"block {n}: italics {len(ITALIC.findall(s))} -> "
                         f"{len(ITALIC.findall(t))}: {head}")
    return diff, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("split", help="write the parts for the translator")
    s.add_argument("source", type=Path, nargs="+", help="texts/la/{file}.md")
    s.add_argument("-o", "--output", type=Path, required=True, help="directory")
    s.add_argument("--size", type=int, default=10000,
                   help="characters per part (default 10000)")
    c = sub.add_parser("check", help="compare a translated part with its input")
    c.add_argument("input", type=Path, help="the part given to the translator")
    c.add_argument("translation", type=Path, help="the translator's output")
    c.add_argument("--lang", choices=sorted(MIN_RATIO), required=True)
    c.add_argument("--min-ratio", type=float,
                   help="shortest translation/source length of a paragraph "
                        "(default: en 0.8, ja 0.3)")
    a = ap.parse_args()

    if a.cmd == "split":
        a.output.mkdir(parents=True, exist_ok=True)
        total = 0
        for src in a.source:
            parts = split(prose(src), a.size)
            for k, part in enumerate(parts, 1):
                path = a.output / f"{src.stem}-{k:02d}.md"
                path.write_text("\n\n".join(part) + "\n", encoding="utf-8")
            print(f"{src.name}\t{len(parts)}")
            total += len(parts)
        print(f"{total} parts", file=sys.stderr)
    else:
        ratio = a.min_ratio if a.min_ratio is not None else MIN_RATIO[a.lang]
        diff, notes = check(a.input.read_text(encoding="utf-8"),
                            a.translation.read_text(encoding="utf-8"), a.lang, ratio)
        print("\n".join(diff) if diff else "same structure")
        for n in notes:
            print(n)
        sys.exit(1 if diff or notes else 0)


if __name__ == "__main__":
    main()
