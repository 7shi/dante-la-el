"""Survey of the verse blocks of the ocr/la canto pages: which columns are transcribed.

    la_survey.py [--cantos | --work FIRST LAST] [-o OUT]

For each canto text page (the pages of the Latin-and-Comentum column of ocr/la/INDEX.md),
reads the verse block at the top (up to the first prose paragraph, skipping running heads,
page numbers and the gloss lines), splits it into tercets, and classifies each tercet as
Italian or Latin by its similarity to the Italian text of dante-corpus and by Latin/Italian
function words. The corpus locates the Italian lines only; this edition's Italian differs
from it and is never copied from it.

- default: one line per page: both (both columns, same number of lines), both-diff (line
  counts differ), la-only (the Italian is missing), it-only (the Latin is missing), none (no
  verse), with the corpus lines of the Italian and the tercet numbers of the Latin;
- --cantos: one line per canto: corpus lines, Italian lines found, Latin lines, page classes;
- --work FIRST LAST: the work list of a batch, a Markdown table row for each page to complete.

dante-corpus (https://github.com/7shi/dante-corpus) is read through its API, as an editable
dependency in ../dante-corpus (see README.md)."""

import argparse
import collections
import itertools
import re
import statistics
import sys
import unicodedata
from pathlib import Path

import dante_corpus
from rapidfuzz import fuzz, process

ROOT = Path(__file__).resolve().parent / "la"
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}
SUPD = "⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉"
SUP = str.maketrans(SUPD, "01234567890123456789")
NUM = re.compile(r"^\s*(?:<sup>|\^?\(|\*|\^)?\s*([⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]{1,3}|\d{1,3})\s*(?:</sup>)?\s*(?:\)|\^|\*|\.)?\s*[_*]*\s*(?=[A-ZÀ-Ý«\"'\[¿“‘])")
FOOT = re.compile(r"^\s*\((?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\d+)\)\s*")
IT = set("che il lo la gli le di del della dei dal dalla al alla nel nella e è per mi ti si io ma poi più così perchè sì ch l d ond un tu el ed o".split())
LA = set("et est quod qui que quia ad cum sed ego me michi mihi tibi sibi sum sunt erat fuit ille illa ipse iste ista nec neque ut sicut tantum ita eius ab ex de non in".split())


def roman(s):
    n = 0
    for a, b in zip(s, s[1:] + " "):
        v = ROMAN[a]; n += -v if ROMAN.get(b, 0) > v else v
    return n


def cantos():
    """(cantica, canto, first page, last page) from INDEX.md."""
    out, cantica = [], None
    for line in (ROOT / "INDEX.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            cantica = ("inferno" if "Infern" in line else "purgatorio" if "Purgator" in line
                       else "paradiso" if "Paradis" in line else None)
        m = re.match(r"\| \*\*Canto ([IVXL]+)\*\* \|", line)
        if m and cantica:
            files = re.findall(r"\[(\d+)\.txt\]", line.split("|")[4])
            out.append((cantica, roman(m[1]), int(files[0]), int(files[-1])))
    return out


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalpha())


def latin_score(line):
    """>0 Latin-like, <0 Italian-like."""
    w = re.findall(r"[a-zà-ÿ]+", unicodedata.normalize("NFC", line.lower()))
    if not w: return 0
    cons = sum(1 for x in w if len(x) > 2 and x[-1] in "mstrx" and x not in ("per", "con", "non")) / len(w)
    apos = line.count("'") + line.count("’")
    it = sum(x in IT for x in w); la = sum(x in LA for x in w)
    return cons * 2 + (la - it) / len(w) - 0.3 * apos


# ---- the verse block of a page ----

def is_head(l):
    t = re.sub(r"[\d⁰¹²³⁴⁵⁶⁷⁸⁹^\s]+", " ", l.replace("[Header]", "")).strip().strip("*_#")
    if not t: return True
    return re.fullmatch(r"\d+", t) or re.fullmatch(r"[\dA-Z .,]+", t) and t.upper() == t


def verse_block(lines):
    """Indices of the verse block lines at the top of the page."""
    groups, cur = [], []
    for i, l in enumerate(lines):
        if l.strip() and not re.fullmatch(r"[\s_\-—=–.]+", l): cur.append(i)
        elif cur: groups.append(cur); cur = []
    if cur: groups.append(cur)
    block = []
    for g in groups:
        ls = [lines[i] for i in g]
        if all(is_head(l) for l in ls): continue
        if all(re.match(FOOT.pattern + r"[a-zà-ÿ'’]", l) for l in ls): continue
        ls = [l for l in ls if not is_head(l)]
        body = [NUM.sub("", l).strip().lstrip("_*") for l in ls]
        upper = sum(1 for b in body if b[:1].isupper() or b[:1] in "«\"'[¿“‘(`|^")
        if upper >= 0.8 * len(body) and sum(len(l) < 100 for l in ls) >= 0.8 * len(ls):
            block += g
        else:
            break
    return block


def page_lines(p):
    """The lines of page p, side-by-side columns split, and the source line of each."""
    raw = (ROOT / f"{p:04d}.txt").read_text(encoding="utf-8").splitlines()
    lines, src, right = [], [], []  # right: right columns of side-by-side lines, emitted after the run
    for n0, l in enumerate(raw + [""]):
        l = l.rstrip()
        parts = re.split(r"\t+|(?<=\S)\s{3,}(?=\S)", l) if l.strip() else [l]
        if len(parts) >= 2 and len(parts[0].strip()) > 15:
            lines.append(parts[0]); src.append(n0)
            right.append((" ".join(parts[1:]), n0)); continue
        if right:
            lines.append(""); src.append(n0)
            for x, k in right: lines.append(x); src.append(k)
            lines.append(""); src.append(n0); right = []
        lines.append(l); src.append(n0)
    return lines, src


def keep(text):
    """Not a gloss line, running head, page number, runover word or variant note."""
    t = text.strip()
    return not (FOOT.match(t) or re.match(r"^\(['’\d⁰¹²³⁴⁵⁶⁷⁸⁹]+\)", t) or re.fullmatch(r"[A-Z .,]+", t)
                or re.fullmatch(r"[\d⁰¹²³⁴⁵⁶⁷⁸⁹]+", t) or t.startswith("[") and len(t) < 25
                or " — (" in t or re.match(r"^\((?:al\.|i\.)", t))


def survey():
    pages = []
    for cantica, n, first, last in cantos():
        corpus = [norm(l.text) for l in dante_corpus.canto(cantica, n).lines()]
        for p in range(first, last + 1):
            lines, src = page_lines(p)
            items = []
            for i in verse_block(lines):
                l = lines[i]; m = NUM.match(l)
                text = re.sub(r"[_*]", "", l[m.end():] if m else l).strip()
                _, s, k = process.extractOne(norm(text), corpus, scorer=fuzz.ratio)
                items.append(dict(line=src[i] + 1, num=int(m[1].translate(SUP)) if m else None,
                                  text=text, best=k + 1, sim=round(s)))
            terc = []
            for it in (x for x in items if keep(x["text"])):
                if it["num"] is not None or not terc or len(terc[-1]) >= 3: terc.append([it])
                else: terc[-1].append(it)
            tt = []
            for t in terc:
                v = statistics.mean(x["sim"] for x in t) - 30 * statistics.mean(latin_score(x["text"]) for x in t)
                tt.append(dict(lang="it" if v >= 65 else "la", num=t[0]["num"], n=len(t),
                               best=[x["best"] for x in t]))
            it = [t for t in tt if t["lang"] == "it"]; la = [t for t in tt if t["lang"] == "la"]
            nit = sum(t["n"] for t in it); nla = sum(t["n"] for t in la)
            c = "none" if not tt else "both" if it and la else "it-only" if it else "la-only"
            if c == "both" and nit != nla: c = "both-diff"
            pages.append(dict(page=p, cantica=cantica, canto=n, nlines=len(corpus), cat=c,
                              it=it, la=la, nit=nit, nla=nla))
    return pages


# ---- reports ----

def by_page(pages):
    out = []
    for p in pages:
        itbest = [t["best"][0] for t in p["it"]]
        out.append(f"{p['page']:04d} {p['cantica'][:4]} {p['canto']:2d} {p['cat']:9s} it={p['nit']} la={p['nla']} "
                   f"itbest={itbest[:1] + itbest[-1:]} lanums={[t['num'] for t in p['la']]}")
    return out


def by_canto(pages):
    out = []
    for (cantica, n), g in itertools.groupby(pages, key=lambda p: (p["cantica"], p["canto"])):
        g = list(g)
        found = {b for p in g for t in p["it"] for b in t["best"]}
        cats = collections.Counter(p["cat"] for p in g)
        out.append(f"{cantica[:4]} {n:2d} n={g[0]['nlines']:3d} it_found={len(found):3d} "
                   f"it_lines={sum(p['nit'] for p in g):3d} la_lines={sum(p['nla'] for p in g):3d}  "
                   + " ".join(f"{c}={v}" for c, v in sorted(cats.items())))
    return out


def work(pages, first, last):
    out = []
    for p in pages:
        if not first <= p["page"] <= last or p["cat"] == "none": continue
        it, la = p["it"], p["la"]
        nums = [t["num"] for t in (la or it)]
        known = [x for x in nums if x is not None]
        rng = f"{known[0]}–{known[-1]}" if known else "none"
        notes = []
        if p["cat"] == "la-only":
            notes.append(f"Italian missing ({p['nla']} Latin lines; tercet numbers as transcribed: {rng})")
        elif p["cat"] == "it-only":
            notes.append(f"Latin missing ({p['nit']} Italian lines, corpus lines {it[0]['best'][0]}–{it[-1]['best'][0]}); "
                         "first look for a Latin verse block placed after the left commentary column and move it up")
        elif p["cat"] == "both-diff":
            notes.append(f"line counts differ: Italian {p['nit']}, Latin {p['nla']}")
        if None in nums: notes.append("some tercet numbers missing")
        if any(b - a != 1 for a, b in zip(known, known[1:])):
            notes.append(f"numbers out of sequence: {' '.join(str(x) for x in nums)}")
        if notes: out.append(f"| {p['page']:04d} | {'; '.join(notes)} |")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--cantos", action="store_true", help="one line per canto")
    g.add_argument("--work", nargs=2, type=int, metavar=("FIRST", "LAST"), help="the work list of a batch")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    a = ap.parse_args()
    pages = survey()
    out = by_canto(pages) if a.cantos else work(pages, *a.work) if a.work else by_page(pages)
    if not a.work: out.append(str(collections.Counter(p["cat"] for p in pages)))
    text = "\n".join(out) + "\n"
    if a.output: Path(a.output).write_text(text, encoding="utf-8")
    else: sys.stdout.write(text)


if __name__ == "__main__":
    main()
