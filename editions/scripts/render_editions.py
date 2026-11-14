"""
Render the tables of the reports in editions/ from the judgments made by
hand on the differences that compare_editions.py collects.

- it: editions/judge-it.txt sorts the lines of the Inferno whose Italian
  differs in words between Carlyle's edition and dante-corpus into
  categories (content, function, order, inflection). A table lists the lines
  of one category: Carlyle's line and dante-corpus's with the differing words
  in bold (the segments that are not forms of the same word, or all if every
  one is), and the text that Oelsner's line reads with at those words (the
  closer in spelling), or his line if it reads with neither or partly with
  each.
- en: editions/judge-en.txt sorts the differences in words between Carlyle's
  English and Oelsner's, numbered as compare_editions.py en lists them, into
  categories (F, W, O, N, M, A, S; unlisted ones are W), and gives for the
  revisions that follow Oelsner's Italian (F) the Italian line. A table lists
  the differences of the given categories, those close together merged into
  one row: the line range of Carlyle's page, both texts with the differing
  words in bold and a few words of context, whether Oelsner's brackets mark
  the change, and with --italian the Italian lines of both editions.

The rest of the reports is written by hand.
"""

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

# The scripts shared with the commentaries
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "commentary" / "scripts"))

from compare_editions import is_form, plain, word_differences
from source import oelsner_lines, source_lines


def roman(n: int) -> str:
    out = ""
    for value, numeral in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= value:
            out += numeral
            n -= value
    return out


def read_judgments(path: Path) -> list[tuple[str, list[str]]]:
    """(category, items) of every line of a judgment file, without comments."""
    result = []
    for line in path.read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            category, *items = line.replace(":", " ", 1).split() \
                if line.split()[0].endswith(":") else line.split()
            result.append((category, items))
    return result


# --- it ---

def it_tokens(text: str):
    """(start, end, plain form) of every word of a line."""
    return [(m.start(), m.end(), plain(m.group())) for m in re.finditer(r"[^\W\d_]+", text)]


def opcodes(a, b):
    return SequenceMatcher(None, [t[2] for t in a], [t[2] for t in b],
                           autojunk=False).get_opcodes()


def bold(text: str, tokens, ranges) -> str:
    spans = []
    for k in sorted({k for i, j in ranges for k in range(i, j)}):
        if spans and spans[-1][1] == k:
            spans[-1][1] = k + 1
        else:
            spans.append([k, k + 1])
    out, pos = [], 0
    for i, j in spans:
        start, end = tokens[i][0], tokens[j - 1][1]
        out += [text[pos:start], f"**{text[start:end]}**"]
        pos = end
    return "".join(out) + text[pos:]


def aligned(tokens, i: int, j: int, other) -> str:
    """The words of other aligned with the words i..j of tokens."""
    out = []
    for op, a1, a2, b1, b2 in opcodes(tokens, other):
        if op == "equal":
            lo, hi = max(a1, i), min(a2, j)
            if lo < hi:
                out += other[b1 + lo - a1:b1 + hi - a1]
        elif (a1 < j and a2 > i) or (a1 == a2 == i) \
                or (i == j and a1 <= i <= a2 and op != "delete"):
            out += other[b1:b2]
    return " ".join(t[2] for t in out)


def agree(tc, td, segments, oelsner: str | None) -> str:
    if oelsner is None:
        return "(missing)"
    to = it_tokens(oelsner)
    votes = set()
    for i1, i2, j1, j2 in segments:
        c = " ".join(t[2] for t in tc[i1:i2])
        d = " ".join(t[2] for t in td[j1:j2])
        o = aligned(tc, i1, i2, to)
        rc = SequenceMatcher(None, o, c).ratio()
        rd = SequenceMatcher(None, o, d).ratio()
        votes.add("Carlyle" if rc > rd else "dante-corpus" if rd > rc else "?")
    return votes.pop() if len(votes) == 1 and "?" not in votes else oelsner


def it_row(spec: str) -> str:
    canto, no = map(int, spec.split(":"))
    c = source_lines("en", "inferno", canto)[no - 1].text
    d = source_lines("it", "inferno", canto)[no - 1].text
    o = {line.no: line.text for line in oelsner_lines(canto)}.get(no)
    tc, td = it_tokens(c), it_tokens(d)
    segments = [(i1, i2, j1, j2) for op, i1, i2, j1, j2 in opcodes(tc, td) if op != "equal"]

    def words(tokens, i, j):
        return " ".join(t[2] for t in tokens[i:j])

    keep = [s for s in segments
            if not is_form(words(tc, s[0], s[1]), words(td, s[2], s[3]))] or segments
    return (f"| {roman(canto)} {no} | {bold(c, tc, [(s[0], s[1]) for s in keep])} | "
            f"{bold(d, td, [(s[2], s[3]) for s in keep])} | {agree(tc, td, keep, o)} |")


def render_it(judgments, category: str, out):
    items = dict(judgments)[category]
    print("| Line | Carlyle | dante-corpus | Oelsner |\n|---|---|---|---|", file=out)
    for spec in items:
        print(it_row(spec), file=out)


# --- en ---

def detok(tokens: list[str]) -> str:
    s = " ".join(tokens)
    s = re.sub(r" ([,.;:!?’”)—])", r"\1", s)
    s = re.sub(r"([“‘(—]) ", r"\1", s)
    return re.sub(r" - ", "-", s)


def show(tokens: list[str], spans, lo: int, hi: int) -> str:
    """tokens[lo:hi] with the spans in bold, and … where the text goes on."""
    marks = {k for i, j in spans for k in range(i, j)}
    out = []
    k = lo
    while k < hi:
        if k in marks:
            j = k
            while j < hi and j in marks:
                j += 1
            out.append("**" + detok(tokens[k:j]) + "**")
            k = j
        else:
            out.append(tokens[k])
            k += 1
    return ("… " if lo > 0 else "") + detok(out) + (" …" if hi < len(tokens) else "")


def render_en(judgments, categories: str, italian_column: bool, out):
    diffs = word_differences()
    category = {}
    italian = {}
    for cat, items in judgments:
        for item in items:
            number, _, line = item.partition(":")
            category[int(number)] = cat
            if line:
                italian[int(number)] = int(line)
    # Differences close together (at most 5 words apart) merge into one row
    groups: list[list[int]] = []
    for n in range(1, len(diffs) + 1):
        if category.get(n, "W") not in categories:
            continue
        d, prev = diffs[n - 1], diffs[n - 2] if n > 1 else None
        if groups and groups[-1][-1] == n - 1 and prev.canto == d.canto \
                and d.i1 - prev.i2 <= 5:
            groups[-1].append(n)
        else:
            groups.append([n])
    head = "| Lines | Carlyle | Oelsner | Marked |"
    if italian_column:
        head += " Italian (Carlyle / Oelsner) |"
    print(head, file=out)
    print("|---" * head.count(" |") + "|", file=out)
    for group in groups:
        ds = [diffs[n - 1] for n in group]
        first = ds[0]
        ca = first.ca
        wb = [t for t, _ in first.ob]
        c = show(ca, [(d.i1, d.i2) for d in ds], max(0, min(d.i1 for d in ds) - 5),
                 min(len(ca), max(d.i2 for d in ds) + 5))
        o = show(wb, [(d.j1, d.j2) for d in ds], max(0, min(d.j1 for d in ds) - 5),
                 min(len(wb), max(d.j2 for d in ds) + 5))
        # An ending Oelsner bracketed alone (lord[s]) is a token of its own:
        # join it to its word again
        o = re.sub(r"(\w)( \*\*| )(s|d|ed|ing|y|ly|wards)\b(?![’'])",
                   lambda m: m.group(1) + m.group(2).strip() + m.group(3), o)
        o = o.replace("A pennine", "Apennine")
        marked = [d.marked for d in ds]
        cells = [f"{roman(first.canto)} {first.page.start}–{first.page.end}", c, o,
                 "yes" if all(marked) else "no" if not any(marked) else "partly"]
        if italian_column:
            c_lines = {line.no: line.text for line in source_lines("en", "inferno", first.canto)}
            o_lines = {line.no: line.text for line in oelsner_lines(first.canto)}
            nos = sorted({italian[n] for n in group if n in italian})
            cells.append("<br>".join(f"{no}: {c_lines[no]} / {o_lines[no]}" for no in nos))
        print("| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |", file=out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("mode", choices=["it", "en"],
                        help="it: a table of editions/judge-it.txt; en: of editions/judge-en.txt")
    parser.add_argument("judgments", type=Path, help="The judgment file")
    parser.add_argument("category",
                        help="it: a category (content, function, order, inflection); "
                             "en: one or more category letters (e.g. F, or OA)")
    parser.add_argument("--italian", action="store_true",
                        help="en: add the column of the Italian lines (for F)")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default=sys.stdout,
                        help="Output file (default: standard output)")
    args = parser.parse_args()
    judgments = read_judgments(args.judgments)
    if args.mode == "it":
        render_it(judgments, args.category, args.output)
    else:
        render_en(judgments, args.category, args.italian, args.output)


if __name__ == "__main__":
    main()
