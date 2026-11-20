"""Join the paragraphs that run over a page for the translator, and put the markers back.

prepare: read texts/{dir}/{file}, join each paragraph split at a page marker into the
page where it begins (the marker follows it), write the result for the translator, and
list the joins.

finish: read the translator's output, add after each marker that followed a joined
paragraph the comment `<!-- first paragraph joined to p. X (NNN) -->`, and write it.

A paragraph is taken as running over when the next page begins with prose and either that
prose begins in lower case or the last prose of the page before (before its verse, glosses
and footnotes, if any) does not end in punctuation. A page ending in a weak stop (; : , —)
followed by prose in upper case is reported as doubtful, not joined, until it is decided in
the image and written in translations/joins.tsv (`file`, `page`, `join` yes or no, `note`;
`file` as `{dir}/{file}`, `page` as in the marker, `40 (094)`). A paragraph may run over several pages; all their
markers follow it.

The verse (lines ending in a backslash) is handed over as it is, for reference; it is not
translated, and the check expects it left out of the translation. A footnote's further
paragraphs, indented by four spaces, belong to it.
"""

import argparse
import re
import sys
from pathlib import Path

MARKER = re.compile(r"^<!-- p\. (\S+) \((\d+)\) -->$")
END = tuple(".!?:;”’)—")
REF = re.compile(r"\[\^[^\]]+\](?!:)")


def blocks(text):
    out = []
    for b in re.split(r"\n\s*\n", text.strip("\n")):
        if not b.strip():
            continue
        if b.startswith("    ") and out:
            out[-1] += "\n\n" + b  # a further paragraph of a footnote
        else:
            out.append(b)
    return out


def load(src):
    return blocks(src.read_text(encoding="utf-8"))


DECISIONS = Path(__file__).resolve().parent.parent / "joins.tsv"


def decided(src):
    """The doubtful places of src decided in joins.tsv: {marker: True to join, False not}."""
    out = {}
    key = f"{src.resolve().parent.name}/{src.name}"
    if DECISIONS.exists():
        rows = DECISIONS.read_text(encoding="utf-8").splitlines()[1:]
        for row in rows:
            f, page, join, *_ = row.split("\t")
            if f == key:
                out[f"<!-- p. {page} -->"] = join == "yes"
    return out


LONE_VERSE = re.compile(r"^(&emsp;)?[^\[\n]{1,90} \d{1,3}$")


def is_verse(block):
    """Lines ending in a backslash; or a verse block of one line, which has no backslash
    but ends in its line number (`Sì mi parlava, ed andavamo introcque. 130`)."""
    b = block.strip("\n")
    if any(len(l) > 100 for l in b.splitlines()):
        return False  # prose with line breaks (p. 368 of Canto XXX); verse lines are short
    return "\\\n" in b or b.rstrip().endswith("\\") or bool(LONE_VERSE.match(b))


def is_prose(block):
    first = block.lstrip()
    if first.startswith(("#", "<!--", "[^", "![", ">", "|")):
        return False
    return not is_verse(block)


GLOSS = re.compile(r"^\d{1,3}\\\. ")
LA_GLOSS = re.compile(r"^\(\d+\) ")
SIG_MARK = re.compile(r"^(?:[0-9]{1,2}|[IVX]{1,4})$")
TERCET_NUM = re.compile(r"^(?:\[)?(\d{1,2}) ")


def is_la_src(src):
    return src.resolve().parent.name == "la"


def last_prose(bs, i):
    """The last prose block of the page that ends before the marker bs[i]; the glosses
    under the verse (`12\\. Alto, high, …` or `(1) costui.`) and stray signature marks
    are not counted."""
    for j in range(i - 1, -1, -1):
        if MARKER.match(bs[j]) or bs[j].startswith("#"):
            return None
        if (is_prose(bs[j]) and not GLOSS.match(bs[j])
                and not LA_GLOSS.match(bs[j]) and not SIG_MARK.match(bs[j].strip())):
            return j
    return None


def first_prose(bs, i, skip_verse=False):
    """The first prose block after the marker bs[i]. When skip_verse is True (used for
    `la`), verse blocks and gloss lines immediately following the page marker are skipped."""
    if not skip_verse:
        return i + 1 if i + 1 < len(bs) and is_prose(bs[i + 1]) else None
    for k in range(i + 1, len(bs)):
        b = bs[k]
        if MARKER.match(b) or b.startswith(("#", "[^")):
            return None
        if is_verse(b) or GLOSS.match(b) or LA_GLOSS.match(b):
            continue
        return k if is_prose(b) else None
    return None


def joins(bs, dec={}, skip_verse=False):
    """(i, j, k): the marker bs[i], the prose bs[j] that runs on, its continuation bs[k].
    dec: the decided places (decided())."""
    out = []
    for i, b in enumerate(bs):
        if not MARKER.match(b):
            continue
        k = first_prose(bs, i, skip_verse=skip_verse)
        if k is None:
            continue
        j = last_prose(bs, i)
        if j is None:
            continue
        if b in dec:
            if dec[b]:
                out.append((i, j, k))
        elif bs[k].lstrip()[:1].islower() or not ending(bs[j]).endswith(END):
            out.append((i, j, k))
    return out


def ending(block):
    return REF.sub("", block).rstrip()


def doubtful(bs, dec={}, skip_verse=False):
    """Markers not joined where the page before ends in a weak stop (; : , —), and not
    decided."""
    joined = {i for i, _, _ in joins(bs, dec, skip_verse=skip_verse)}
    out = []
    for i, b in enumerate(bs):
        if not MARKER.match(b) or i in joined or b in dec:
            continue
        k = first_prose(bs, i, skip_verse=skip_verse)
        if k is None:
            continue
        j = last_prose(bs, i)
        if j is not None and ending(bs[j]).rstrip("”’").endswith(tuple(";:,—")):
            out.append((i, k))
    return out


def roots(bs, dec={}, skip_verse=False):
    """For each join: the index of the block where the paragraph begins."""
    root, out = {}, []
    for i, j, k in joins(bs, dec, skip_verse=skip_verse):
        r = root.get(j, j)
        root[k] = r
        out.append((i, r, k))
    return out


def page_before(bs, i):
    for b in reversed(bs[:i]):
        m = MARKER.match(b)
        if m:
            return m.group(1), m.group(2)
    return None


def prepare(src):
    bs, dec, sv = load(src), decided(src), is_la_src(src)
    text, removed, report = list(bs), set(), []
    for i, r, k in roots(bs, dec, skip_verse=sv):
        report.append(f"{bs[i]}\t…{text[r].rstrip()[-30:]} | {bs[k].lstrip()[:30]}…")
        text[r] = text[r].rstrip() + " " + bs[k].lstrip()
        removed.add(k)
    for i, k in doubtful(bs, dec, skip_verse=sv):
        report.append(f"{bs[i]}\tdoubtful, not joined: {bs[k].lstrip()[:30]}…")
    out = [t for n, t in enumerate(text) if n not in removed]
    return "\n\n".join(out) + "\n", report


def finish(src, translated):
    bs = load(src)
    joined = {}
    for i, r, k in roots(bs, decided(src), skip_verse=is_la_src(src)):
        p, n = page_before(bs, r)
        joined[bs[i]] = f"<!-- first paragraph joined to p. {p} ({n}) -->"
    lines, missing = [], set(joined)
    for line in translated.splitlines():
        lines.append(line)
        key = line.strip()
        if key in joined:
            lines.append(joined[key])
            missing.discard(key)
    for m in sorted(missing):
        print(f"marker not found in the translation: {m}", file=sys.stderr)
    return "\n".join(lines).rstrip("\n") + "\n"


def shape(text, count_verse_lines=False, skip_italian_tercets=False):
    """The structure of a text: markers and footnote IDs as they are, headings by level,
    verse as V (or V:N with line count when count_verse_lines is True), a paragraph as P
    with the footnote references in it."""
    bs = blocks(text)
    out = []
    for i, b in enumerate(bs):
        b = b.strip()
        if skip_italian_tercets and is_verse(b):
            m = TERCET_NUM.match(b)
            if m and i + 1 < len(bs) and is_verse(bs[i + 1].strip()):
                m2 = TERCET_NUM.match(bs[i + 1].strip())
                if m2 and m2.group(1) == m.group(1):
                    continue
        if b.startswith("<!--"):
            out.extend(l for l in b.splitlines() if "paragraph joined to" not in l)
        elif b.startswith("#"):
            out.append(b.split(" ", 1)[0])
        elif b.startswith("[^"):
            out.append(b.split(":", 1)[0])
        elif is_verse(b):
            out.append(f"V:{len(b.splitlines())}" if count_verse_lines else "V")
        else:
            out.append("P" + "".join(REF.findall(b)))
    return out


def check(src, translated, keep_verse=False, skip_italian_tercets=False):
    """Compare the translator's output with the input it was given. Returns the
    differences, and the paragraphs whose footnote references come in another order (which
    Japanese word order may need; reported, not counted as a difference)."""
    import difflib
    if skip_italian_tercets:
        a = shape(prepare(src)[0], count_verse_lines=True, skip_italian_tercets=True)
        b = shape(translated, count_verse_lines=True)
    elif keep_verse:
        a = shape(prepare(src)[0], count_verse_lines=True)
        b = shape(translated, count_verse_lines=True)
    else:
        a = [x for x in shape(prepare(src)[0]) if x != "V"]  # verse is not translated
        b = shape(translated)
    norm = lambda xs: ["P" + "".join(sorted(REF.findall(x))) if x.startswith("P") else x
                       for x in xs]
    diff = list(difflib.unified_diff(norm(a), norm(b), "input", "translation", lineterm=""))
    order = [] if diff else [f"{x} -> {y}" for x, y in zip(a, b) if x != y]
    return diff, order


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare", help="write the translator's input")
    p.add_argument("source", type=Path, help="texts/{dir}/{file}.md")
    p.add_argument("-o", "--output", type=Path, required=True)
    f = sub.add_parser("finish", help="add the comments to the translation")
    f.add_argument("source", type=Path, help="texts/{dir}/{file}.md")
    f.add_argument("translation", type=Path, help="the translator's output")
    f.add_argument("-o", "--output", type=Path, required=True)
    c = sub.add_parser("check", help="compare the structure of the translation")
    c.add_argument("source", type=Path, help="texts/{dir}/{file}.md")
    c.add_argument("translation", type=Path, help="the translator's output")
    c.add_argument("--keep-verse", action="store_true",
                   help="include verse blocks (with line counts) in the comparison")
    c.add_argument("--skip-italian-tercets", action="store_true",
                   help="for `la`: skip Italian tercets and keep Latin tercets/other verse with line counts")
    a = ap.parse_args()

    if a.cmd == "prepare":
        text, report = prepare(a.source)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
        for r in report:
            print(r)
        print(f"{len(report)} joined", file=sys.stderr)
    elif a.cmd == "check":
        diff, order = check(a.source, a.translation.read_text(encoding="utf-8"),
                            keep_verse=a.keep_verse,
                            skip_italian_tercets=a.skip_italian_tercets)
        print("\n".join(diff) if diff else "same structure")
        for o in order:
            print(f"references reordered: {o}")
        sys.exit(1 if diff else 0)
    else:
        text = finish(a.source, a.translation.read_text(encoding="utf-8"))
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
