"""Finds the lines of the page files where a reader's flagged phrases are.

FLAGS is the reader's TSV, `page<TAB>phrase<TAB>reason` (page as in the marker, `0080`), the
phrase copied from the converted text (`texts/…`). The phrase is found in the page file
`DIR/PAGE.txt` word by word, compared without case, punctuation, italic marks and
brackets, and across a line broken by a hyphen; if it is not there, the page and the next
(a phrase across the page break: the foot of the one and the top of the other, or any line
of the one and the first line of the other, as where the verse and the notes are printed
below the prose in ocr/en), then the page before are searched; if still not found,
the most similar run of words, if similar enough, is given with `~`.

Output, a TSV: page, line(s) (`12` or `12-13`), how found (`=`, `~0.85`, `-` not found),
the phrase, the reason, and the text of the lines.

    uv run ocr/scripts/findline.py ocr/la flags.tsv -o found.tsv
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
ap.add_argument("dir", type=Path, help="directory of the page files (e.g. ocr/la)")
ap.add_argument("flags", type=Path, help="TSV: page, phrase, reason")
ap.add_argument("-o", "--output", type=Path, help="output TSV (default: stdout)")
ap.add_argument("--min", type=float, default=0.75, help="least similarity for ~ (0.75)")
a = ap.parse_args()


def key(w):
    """A word compared: lowercase, letters and digits only."""
    return "".join(c for c in w.lower() if c.isalnum())


cache = {}


def words(page):
    """The page's words as (key, first line, last line), a hyphen at a line end joining the next line's
    first word; None if there is no such page."""
    if page in cache:
        return cache[page]
    f = a.dir / f"{page}.txt"
    if not f.exists():
        cache[page] = None
        return None
    # the printed side of a misprint mark `{{printed|fixed}}` or a correction `{{printed|LIST|fixed}}`
    # (ocr/PLAN.md, "Decisions"), which may span lines; no italic marks
    text = re.sub(r"\{\{([^{}|]*)\|(?:[0-9]+(?:&[0-9]+)*\|)?[^{}|]*\}\}", r"\1", f.read_text(encoding="utf-8"))
    lines = text.split("\n")
    out, carry = [], None
    for n, line in enumerate(lines, 1):
        ws = re.sub(r"(?<!\d)\*", "", line).split()
        if not ws:
            continue
        if carry:
            ws[0] = carry[0] + ws[0]
        starts = [carry[1] if carry and i == 0 else n for i in range(len(ws))]
        carry = None
        if ws[-1].endswith("-") and len(ws[-1]) > 1:
            carry = (ws[-1][:-1], starts[-1])
            ws, starts = ws[:-1], starts[:-1]
        out += [(key(w), s, n) for w, s in zip(ws, starts)]
    if carry:
        out.append((key(carry[0]), carry[1], carry[1]))
    out = [w for w in out if w[0]]
    cache[page] = (out, lines)
    return cache[page]


def furniture(line):
    """A page number or running head (`26`, `INFERNI`, `246 INFERNI`), left out when a
    phrase is searched across a page break."""
    ws = line.split()
    return 0 < len(ws) <= 3 and all(w.isdigit() or w.isupper() for w in ws)


def edge(page, first):
    """The page's words without the furniture at its top (first) or foot."""
    ws, lines = words(page)
    order = range(len(lines)) if first else range(len(lines) - 1, -1, -1)
    drop = set()
    for i in order:
        if not lines[i].strip() or furniture(lines[i]):
            drop.add(i + 1)
        else:
            break
    return [w for w in ws if w[1] not in drop]


def neighbour(page, d):
    return str(int(page) + d).zfill(len(page))


def joins(head, tail):
    """Words of each line of page head followed by the first line of page tail, a hyphen at
    the line end joining the two: a paragraph that runs over the page when the verse and
    the notes are printed below it (ocr/en)."""
    got = [words(head), words(tail)]
    if any(g is None for g in got):
        return []
    lines, first = got[0][1], None
    for n, line in enumerate(got[1][1], 1):
        if line.strip() and not furniture(line):
            first = (n, line.split())
            break
    if first is None:
        return []
    out = []
    for n, line in enumerate(lines, 1):
        ws = line.split()
        if not ws:
            continue
        a_ws = [(key(w), head, n, n) for w in ws]
        b_ws = [(key(w), tail, first[0], first[0]) for w in first[1]]
        if ws[-1].endswith("-") and len(ws[-1]) > 1:
            b_ws[0] = (key(ws[-1][:-1] + first[1][0]), head, n, n)
            a_ws = a_ws[:-1]
        out.append([w for w in a_ws + b_ws if w[0]])
    return out


def find(page, phrase):
    ph = [k for k in map(key, phrase.split()) if k]
    if not ph:
        return None
    spans = [[page], [page, neighbour(page, 1)], [neighbour(page, -1), page]]
    best = None
    for span in spans:
        got = [words(p) for p in span]
        if any(g is None for g in got):
            continue
        if len(span) == 1:
            parts = [got[0][0]]
        else:
            parts = [edge(span[0], False), edge(span[1], True)]
        ws = [(k, p, n0, n1) for p, part in zip(span, parts) for k, n0, n1 in part]
        ks = [w[0] for w in ws]
        hits = [i for i in range(len(ks) - len(ph) + 1) if ks[i:i + len(ph)] == ph]
        if hits:
            return "=", [ws[i:i + len(ph)] for i in hits]
        if len(span) == 2:
            for ws in joins(*span):
                ks = [w[0] for w in ws]
                hits = [i for i in range(len(ks) - len(ph) + 1) if ks[i:i + len(ph)] == ph]
                if hits:
                    return "=", [ws[i:i + len(ph)] for i in hits]
        target = " ".join(ph)
        for i in range(max(1, len(ks) - len(ph) + 1)):
            r = difflib.SequenceMatcher(None, target, " ".join(ks[i:i + len(ph)])).ratio()
            if best is None or r > best[0]:
                best = (r, ws[i:i + len(ph)])
    if best and best[0] >= a.min:
        return f"~{best[0]:.2f}", [best[1]]
    return None


rows = []
for n, row in enumerate(a.flags.read_text(encoding="utf-8").split("\n"), 1):
    if not row.strip():
        continue
    cols = row.split("\t")
    if len(cols) < 2 or not cols[0].strip().isdigit():
        if n > 1:
            print(f"row {n}: no page and phrase: {row!r}", file=sys.stderr)
        continue
    page, phrase = cols[0].strip(), cols[1]
    reason = cols[2] if len(cols) > 2 else ""
    got = find(page, phrase)
    if not got:
        rows.append([page, "", "-", phrase, reason, ""])
        continue
    how, matches = got
    for m in matches:
        p0, p1 = m[0][1], m[-1][1]
        n0, n1 = m[0][2], m[-1][3]
        if p0 == p1:
            where, text = (f"{n0}" if n0 == n1 else f"{n0}-{n1}"), words(p0)[1][n0 - 1:n1]
        else:
            where = f"{n0}-{p1}:{n1}"
            text = words(p0)[1][n0 - 1:] + words(p1)[1][:n1]
        text = " / ".join(t.strip() for t in text if t.strip())
        rows.append([p0, where, how, phrase, reason, text])

out = "page\tline\thow\tphrase\treason\ttext\n" + "".join("\t".join(r) + "\n" for r in rows)
if a.output:
    a.output.write_text(out, encoding="utf-8")
    c = {k: sum(1 for r in rows if r[2][:1] == k) for k in "=~-"}
    print(f"{len(rows)} rows: {c['=']} found, {c['~']} similar, {c['-']} not found: {a.output}",
          file=sys.stderr)
else:
    sys.stdout.write(out)
