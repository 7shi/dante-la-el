"""Transcribe the verse column of each crop of la_versecrop.py from the image, with a model.

    la_verseread.py CROPS [PAGE...] -m MODEL [-n N] [--fake] [--check]

Reads CROPS/crops.tsv and CROPS/PAGE.png (la_versecrop.py); without PAGE, every page of
crops.tsv with a box. For each page, one call with a new Client, so that images do not pile
up in a history: the crop at the scan's own resolution, and a prompt for its language (the
column cropped: it, la). Only the image is given, no text of the verse: the model reads the
print line by line, the tercet number and the text of each line apart. The script writes the
numbers as superscripts and the gloss marks as (¹), as in ocr/la: CROPS/read/PAGE.txt.

Every answer is saved as CROPS/read/PAGE.MODEL.json and reused on a rerun, so no call is
made twice.

--check compares each transcription with the block of the same column in ocr/la (pages
whose file has it: the trial on checked pages), the tercet numbers' form (superscript or
not), the apostrophes (’ ') and the spaces around them ignored, and writes CROPS/read/check.txt: the lines that
differ, and per page the lines read, the lines of the file and the lines that differ."""

import argparse
import difflib
import re
import sys
from pathlib import Path

from pydantic import BaseModel, Field

from llm7shi import Client
from llm7shi.response import Response
from llm7shi.usage import append_usage, find_usage_file, print_today_totals
from llm7shi.utils import parse_model_args

import la_versecrop as V

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
UNSUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


class Line(BaseModel):
    number: str = Field(description="the tercet number printed before the line, in digits; "
                        "empty if none")
    text: str = Field(description="the text of the line exactly as printed, without the "
                      "tercet number")


class Verse(BaseModel):
    lines: list[Line] = Field(description="the printed lines of the verse column, top to bottom")


LANG = {"it": "Italian", "la": "Latin (a medieval translation, with medieval spellings such "
        "as michi, Ytalia, -e for -ae)"}

PROMPT = """The image is a crop of a page printed in 1891: a column of {lang} verse, in tercets.
Transcribe it line by line, exactly as printed.

- One entry per printed line, top to bottom.
- `number`: the small number printed before the first line of a tercet, in plain digits;
  empty for the other lines.
- `text`: the line exactly as printed, letter by letter. Do not correct anything, and do
  not complete the text from a known edition.
- This edition does not follow the modern text of the poem, and you may know the poem:
  do not let that guide you. Read every word from the print, not from memory, and never
  replace it by the form you know. Its spellings are old and regular; write them so:
  - `gl` before a vowel, with no `i`: `figlo`, `vogla`, `ciglo`, `fogle` (not figlio,
    voglia, ciglio, foglie);
  - `ct` where modern Italian has `tt` or `t`: `decto`, `pecto`, `puncto`, `facto`,
    `sospecto` (not detto, petto, punto, fatto, sospetto);
  - single consonants where a modern text doubles them: `ochi`, `nochier`, `boche`,
    `aqua`; and double ones where it has one: `viddi`;
  - `h` kept: `huom`, `havea`, `trahendo`; `y` kept: `abysso`, `Chyron`;
  - `m` before a vowel or at the end of a word where modern Italian has `n`: `um`;
  - accents where a modern text has none (`Sì` at the start of a line), none where it
    has one (`pieta`);
  - misprints, as printed.
- Accents (à è é ì ò ù): they are small; look at each vowel for one, and write it where
  the print has it, only there. Apostrophes, capitals and punctuation as printed. No space
  is added or removed around an apostrophe. A colon is two round dots; a semicolon has a dot
  above a comma.
- A small raised number in brackets after a word is a gloss mark: write it as (1), (2), in
  its place in the line, with a space before it.
- A word printed apart above or below a line (the end of a line too long for the column,
  after a bracket `[`): its own entry, its text starting with `[`.
- Leave out everything that is not a line of this verse column: the running head and rules
  above it, the gloss lines below it (they begin with (1)), the commentary, and fragments of
  another column cut at the edges of the crop (numbers, single letters, parts of words)."""


def compose(v):
    """The lines as in ocr/la: superscript tercet numbers, gloss marks (¹)."""
    out = []
    for l in v.lines:
        t = re.sub(r"\(\s*(\d)\s*\)", lambda m: f"({m[1].translate(SUP)})", l.text.strip())
        n = re.sub(r"\D", "", l.number)
        out.append(f"{n.translate(SUP)} {t}" if n else t)
    return out


class Fake:
    """Answers without calling: the file's own lines of the column, or one line (for tests)."""
    def __init__(self, lines): self.usages = []; self.lines = lines

    def __call__(self, prompt, schema=None, images=None):
        ls = [Line(number=m[1].translate(UNSUP), text=m[2]) if (m := re.match(
            r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+) (.*)", l)) else Line(number="", text=l)
            for l in self.lines or ["(fake)"]]
        r = Response(); r.text = Verse(lines=ls).model_dump_json()
        return r


def file_column(p, column):
    """The lines of the file's block of that column (no runover words or gloss lines)."""
    return [l for lang, g in V.verse_groups(p) if lang == column for l in g]


def key(l):
    """A line for comparison: tercet numbers plain, apostrophes straight, spaces single,
    none around an apostrophe (its spacing is left as in the file)."""
    return re.sub(r" ?' ?", "'", " ".join(l.translate(UNSUP).replace("’", "'").split()))


def check(p, read, column):
    want = file_column(p, column)
    if not want: return None, []
    got = [l for l in read if not l.startswith("[")]
    a, b = [key(l) for l in want], [key(l) for l in got]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal": continue
        for k in range(max(i2 - i1, j2 - j1)):
            f = want[i1 + k] if i1 + k < i2 else ""
            r = got[j1 + k] if j1 + k < j2 else ""
            out.append(f"{p}\tfile: {f}\n{p}\tread: {r}")
    return (len(got), len(want), len(out)), out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("crops", type=Path, help="the directory of la_versecrop.py")
    ap.add_argument("pages", nargs="*", help="pages of crops.tsv (default: all with a box)")
    ap.add_argument("-n", "--limit", type=int, help="make at most N new calls")
    ap.add_argument("--fake", action="store_true", help="no calls: the file's lines (for tests)")
    ap.add_argument("--check", action="store_true",
                    help="compare with the same column in ocr/la (read/check.txt)")
    ap.add_argument("--save-usage", action="store_true", help="record usage regardless of the model")
    args = parse_model_args(parser=ap)
    out = args.crops / "read"
    out.mkdir(exist_ok=True)
    rows = [r.split("\t") for r in (args.crops / "crops.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    column = {r[0]: r[1] for r in rows if r[2]}
    pages = [f"{int(p):04d}" for p in args.pages] or list(column)
    usage = find_usage_file() if not args.fake and (
        args.model.startswith(("openai:", "gpt-")) or args.save_usage) else None
    tag = "fake" if args.fake else re.sub(r"[^\w.-]+", "_", args.model)
    clients, asked, skipped, report, stats = [], 0, 0, [], []
    try:
        for p in pages:
            if p not in column:
                print(f"{p}: no crop in crops.tsv, skipped", file=sys.stderr); continue
            ans = out / f"{p}.{tag}.json"
            if not ans.exists():
                if args.limit is not None and asked >= args.limit:
                    skipped += 1; continue
                client = Fake(file_column(p, column[p])) if args.fake else Client(
                    model=args.model, show_params=False, keep_history=False, show_usage=True)
                clients.append(client)
                print(f"\n=== {p} ({column[p]}) ===", file=sys.stderr)
                resp = client([PROMPT.format(lang=LANG[column[p]])], Verse,
                              images=[args.crops / f"{p}.png"])
                asked += 1
                ans.write_text(resp.text, encoding="utf-8")
            try:
                v = Verse.model_validate_json(ans.read_text(encoding="utf-8"))
            except ValueError:
                print(f"{p}: invalid answer in {ans}", file=sys.stderr); continue
            read = compose(v)
            (out / f"{p}.txt").write_text("\n".join(read) + "\n", encoding="utf-8")
            if args.check:
                s, diffs = check(p, read, column[p])
                if s: stats.append((p, *s)); report += diffs
    finally:
        used = [u for c in clients for u in c.usages]
        if used and usage is not None: append_usage(sum(used), args.model, usage)
    if args.check:
        head = [f"{len(stats)} pages; lines read {sum(s[1] for s in stats)}, in the files "
                f"{sum(s[2] for s in stats)}; lines differing {sum(s[3] for s in stats)}, "
                f"pages without a difference {sum(s[3] == 0 for s in stats)}", ""]
        head += [f"{p}\tread {a}\tfile {b}\tdiffer {d}" for p, a, b, d in stats if d]
        (out / "check.txt").write_text("\n".join(head + [""] + report) + "\n", encoding="utf-8")
        print(head[0], file=sys.stderr)
    if used:
        print(f"\n--- Total Usage ---\n{sum(used)}")
        if usage is not None: print_today_totals(usage, models=[args.model])
    print(f"asked {asked}" + (f", {skipped} left for a later run" if skipped else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
