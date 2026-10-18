"""Mark where two OCRs of the same ocr/la page disagree, without looking at the image.

For each page, ocr/la/NNNN.txt (Gemini 2.5 Flash) and ocr/la/glm-ocr/NNNN.txt (GLM-OCR)
are given to an LLM, which returns only the list of disagreements, as JSON. The script
writes each one into the ocr/la text as {{ocr|glm}}: left the ocr/la reading, right the
GLM-OCR reading, one side empty where a run of text is found on one side only.

The LLM does not copy the page, so the text outside the marks is ocr/la unchanged by
construction. Each answer is checked:

- a difference that cannot be placed (its text is not found on the given line) is left out;
- the right sides are compared with the words of GLM-OCR (line breaks, line-end hyphens and
  spacing ignored); where they still differ, the LLM missed a difference.

When the check finds problems, the LLM is given its answer and the problems with their line
numbers, and asked only for the entries of those places (at most --rounds calls a page).
The placed entries are kept, so nothing is asked twice. Every answer is saved
(OUTDIR/NNNN.json, then NNNN.r2.json, ...), and a page with saved answers is resumed from
them: running the command again asks only for what is still missing.
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

from pydantic import BaseModel, Field

from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals
from llm7shi.utils import parse_model_args

ROOT = Path(__file__).resolve().parent / "la"
# Set to a path to record usage; None means "don't record"
USAGE_PATH = None
MARK = re.compile(r"\{\{([^{}|]*)\|([^{}|]*)\}\}")


def clean_glm(s):
    """GLM-OCR's LaTeX superscripts `$^{(1)}$` as `(1)` and its stray `|` dropped (0021,
    0344, 0467): a mark cannot hold `{`, `}` or `|`. Applied to the text and to the `glm`
    of every entry, saved answers included."""
    return re.sub(r"\$\^\{([^{}]*)\}\$", r"\1", s).replace("|", "")


def mark_line(t, m):
    """The ocr/la line of mark m of the marked page t: counted on the left sides, since a
    right side may hold line breaks."""
    return MARK.sub(lambda x: x.group(1), t[:m.start()]).count("\n") + 1


class Difference(BaseModel):
    line: int = Field(description="number of the OCR A line where the difference starts")
    end_line: int = Field(description="for a run of whole OCR A lines missing from B (such "
                          "as the Latin verse block): the last line of the run; otherwise 0")
    ocr: str = Field(description="the text of OCR A, copied exactly from that line (empty if "
                     "the text is only in B; ignored when end_line is set)")
    glm: str = Field(description="the text of OCR B at that place, copied exactly (empty if "
                     "the text is only in A)")
    after: str = Field(description="the OCR A text on that line right before the place: "
                       "needed when ocr is empty (empty if the B text belongs at the start "
                       "of the line) or when ocr occurs more than once on the line; "
                       "otherwise empty")


class Differences(BaseModel):
    differences: list[Difference]


PROMPT = """Above are two OCR transcriptions of the same printed page.

- OCR A keeps the line breaks of the print; each line is given with its number.
- OCR B joins the lines of each paragraph, and often lacks the Latin verse block.

List every place where B reads differently from A, in the order of A.

- Include every difference of letters, accents, apostrophes, brackets, punctuation and
  capitals, however small. Do not decide which side is right; do not correct either side.
- Keep each difference as short as possible: a single word where only one word differs.
  Join differences only when they are next to each other on the same line.
- Copy `ocr` exactly from the given line of A (without the line number), and `glm` exactly
  from B. If the same `ocr` text occurs more than once on the line, give `after` too.
- Text found only in B: `ocr` empty, `glm` the text, and `after` the A text right before
  the place where it belongs.
- Whole lines of A missing from B (such as the Latin verse block): one entry with `line`
  the first line, `end_line` the last line, and `glm` empty.
- Differences only in line breaks, in line-end hyphenation (`dodice-` / `simum` against
  `dodicesimum`) or in spacing are not differences."""


def widen(text, s, e):
    """Extend a span over the rest of a word broken at a line end (`di-` / `citur`), so the
    mark holds the whole word on the left, as GLM-OCR has it on the right."""
    if s < e and (s == 0 or text[s - 1] == "\n") and s >= 2 and text[s - 2] == "-":
        ps = text.rfind("\n", 0, s - 1) + 1  # start of the line before
        sp = text.rfind(" ", ps, s - 2)
        s = sp + 1 if sp >= 0 else ps  # back to the start of the line-end fragment
    if s < e and text[e - 1] == "-" and e < len(text) and text[e] == "\n":
        m = re.match(r"\n\S*", text[e:])
        e += m.end()
    return s, e


WORD = re.compile(r"\w")
BREAK = r"(?:-[ \t]*\n[ \t]*)?"  # a line-end hyphen, possibly between any two characters


def bounded(text, i, j):
    """Whether text[i:j] does not start or end inside a word."""
    return ((i == 0 or not (WORD.match(text[i]) and WORD.match(text[i - 1])))
            and (j >= len(text) or not (WORD.match(text[j - 1]) and WORD.match(text[j]))))


def find(text, lo, hi, s):
    """Spans of s starting in text[lo:hi]. Exact matches that do not cut a word are
    preferred; s written without the line break of a broken word (`quarum` for `qua-` /
    `rum`) is found too."""
    hits = [(i, i + len(s)) for i in range(lo, hi) if text.startswith(s, i)]
    whole = [h for h in hits if bounded(text, *h)]
    if whole or hits:
        return whole or hits
    pat = re.compile(BREAK.join(re.escape(c) for c in s))
    return [m.span() for m in pat.finditer(text, max(0, lo - 200), hi + 200 + len(s))
            if lo <= m.start() < hi and "\n" in m.group()]


def choose(text, hits, after, line_start):
    """Narrow the hits by the text right before them, if given."""
    if len(hits) > 1 and after.strip():
        a = after.strip()
        hits = [h for h in hits if text[line_start:h[0]].rstrip().endswith(a)] or hits
    return hits


def place(text, diffs):
    """Write the differences into text as marks.

    Return the marked text, the differences placed and those not placed, each with the
    reason."""
    lines = text.split("\n")
    starts = [0]
    for l in lines:
        starts.append(starts[-1] + len(l) + 1)
    spans, unplaced = [], []  # spans: (start, end, difference)
    taken = {}  # identical entries take the identical places in order
    for d in diffs:
        n = d.line - 1
        if not 0 <= n < len(lines):
            unplaced.append((d, "no such line"))
            continue
        if d.end_line:
            m = d.end_line - 1
            if not n <= m < len(lines):
                unplaced.append((d, "bad end_line"))
                continue
            spans.append((starts[n], starts[m] + len(lines[m]), d))
            continue
        if d.ocr == d.glm:
            continue
        lo, hi = starts[n], starts[n] + len(lines[n]) + 1
        if d.ocr:
            hits = choose(text, find(text, lo, hi, d.ocr), d.after, lo)
            key = (d.line, d.ocr, d.after)
            same = sum(1 for x in diffs if (x.line, x.ocr, x.after) == key and not x.end_line)
            if len(hits) > 1 and len(hits) == same:
                k = taken.get(key, 0); taken[key] = k + 1
                hits = [hits[k]]
            if len(hits) != 1:
                unplaced.append((d, f"`ocr` found {len(hits)} times on line {d.line}"))
                continue
            spans.append(hits[0] + (d,))
        else:
            if d.after:
                hits = find(text, lo, hi, d.after)
                if len(hits) != 1:
                    unplaced.append((d, f"`after` found {len(hits)} times on line {d.line}"))
                    continue
                pos = hits[0][1]
            else:
                pos = lo
            spans.append((pos, pos, d))
    spans = [widen(text, s, e) + (d,) for s, e, d in spans]
    spans.sort(key=lambda s: (s[0], -s[1]))
    out, placed, last, prev = [], [], 0, None
    for s, e, d in spans:
        if s < last:
            ps, pe, pd = prev
            if e <= pe and s < e:
                # inside the mark before it: apply it to that mark's B text if possible,
                # otherwise that mark already gives B for the whole span
                if pd.glm.count(d.ocr) == 1:
                    pd.glm = pd.glm.replace(d.ocr, d.glm)
                    out[-1] = out[-1][:out[-1].rindex("|") + 1] + pd.glm + "}}"
                continue
            unplaced.append((d, "overlaps the entry before it"))
            continue
        out.append(text[last:s] + "{{" + text[s:e] + "|" + d.glm + "}}")
        placed.append(d)
        last, prev = e, (s, e, d)
    out.append(text[last:])
    return "".join(out), placed, unplaced


# Ignored by the comparison: a hyphen after a letter with the spacing after it (line-end
# hyphens; GLM-OCR keeps some inside its joined lines, `qua-rum`), and the spacing around an
# apostrophe (`all' incredulità`).
IGNORE = r"(?<=\w)-\s*|\s+(?=['’])|(?<=['’])\s+"


def right_words(marked):
    """The words of the right sides, each with the OCR A line it comes from and the number
    of its mark (None outside the marks).

    Line breaks, line-end hyphens and spacing are ignored; text only in B is a word of its
    own, whatever spacing the mark has around it."""
    chars, where, line, pos = [], [], 1, 0
    for k, m in enumerate(list(MARK.finditer(marked)) + [None]):
        end = m.start() if m else len(marked)
        for c in marked[pos:end]:
            chars.append(c); where.append((line, None))
            line += c == "\n"
        if m:
            g = f" {m.group(2)} " if not m.group(1) else m.group(2)
            chars.extend(g); where.extend([(line, k)] * len(g))
            line += m.group(1).count("\n")
            pos = m.end()
    # drop what the comparison ignores, dropping the same characters from `where`
    s = "".join(chars)
    for m in reversed(list(re.finditer(IGNORE, s))):
        s = s[:m.start()] + s[m.end():]
        del where[m.start():m.end()]
    return [(w.group(), *where[w.start()]) for w in re.finditer(r"\S+", s)]


def missed(marked, glm):
    """Places where the right sides still differ from the words of GLM-OCR, as
    (first line, last line, B as the marks give it, B as it is, numbers of the marks
    involved)."""
    a = right_words(marked)
    b = re.sub(IGNORE, "", glm).split()
    aw = [w for w, _, _ in a]
    res = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, b, autojunk=False).get_opcodes():
        if op == "equal" or not a:
            continue
        near = a[max(0, i1 - 1):i2 + 1] if i1 == i2 else a[i1:i2]
        lines = [l for _, l, _ in near]
        # only the marks whose B text is wrong; a missing word next to a mark leaves it
        marks = {k for _, _, k in a[i1:i2] if k is not None}
        res.append((min(lines), max(lines), " ".join(aw[i1:i2]), " ".join(b[j1:j2]), marks))
    return res


FIX = """Your answer above was checked against the two texts. These places are still wrong:

{problems}

Return entries only for these places: the entries for each difference there, including
any of your entries listed as dropped that were right, and a corrected entry for each entry
that could not be placed. All your other entries are kept; do not repeat them."""


def review(ocr, glm, diffs):
    """Place the entries and check them.

    Return the marked text, the entries kept for the next round (those placed, except on
    the lines where B still does not come out right), the problems, and their description
    for the LLM."""
    diffs = [d.model_copy(update={"glm": clean_glm(d.glm)}) for d in diffs]
    marked, placed, unplaced = place(ocr, diffs)
    rest = missed(marked, glm)
    bad = set().union(*(r[4] for r in rest))
    kept = [d for k, d in enumerate(placed) if k not in bad]  # mark k is entry placed[k]
    marks = list(MARK.finditer(marked))
    text = [f"- line {d.line}: not placed ({why}): {d.model_dump_json()}" for d, why in unplaced]
    for lo, hi, got, want, ks in rest:
        where = f"line {lo}" if lo == hi else f"lines {lo}-{hi}"
        dropped = "".join(f"\n  Your entry dropped here: {placed[k].model_dump_json()}"
                          for k in sorted(ks))
        text.append(f"- {where}: B comes out as `{got}`, but B has `{want}`.{dropped}")
    return marked, kept, unplaced, rest, "\n".join(text)


def report(page, marked, unplaced, rest, path):
    print(f"\n{page}: {len(MARK.findall(marked))} marks, {len(unplaced)} not placed, "
          f"{len(rest)} differences missed -> {path}", file=sys.stderr)
    for d, why in unplaced:
        print(f"  not placed ({why}): {d.model_dump()}", file=sys.stderr)
    for lo, hi, got, want, _ in rest:
        print(f"  missed, lines {lo}-{hi}: the marks give `{got}`, B has `{want}`",
              file=sys.stderr)


def mark_page(client, page, outdir, rounds):
    """Ask for the differences, then for the fixes, at most `rounds` calls in all.

    The answers already saved in OUTDIR are used instead of calling again, so a page is
    resumed with only the fixing calls still needed. A fixing call that leaves the same
    problems ends the page, so no call is repeated in vain."""
    ocr = (ROOT / f"{page}.txt").read_text(encoding="utf-8").rstrip("\n")
    glm = clean_glm((ROOT / "glm-ocr" / f"{page}.txt").read_text(encoding="utf-8"))
    numbered = "\n".join(f"{i}: {l}" for i, l in enumerate(ocr.split("\n"), 1))
    prompts = ["OCR A:\n" + numbered, "OCR B:\n" + glm, PROMPT]
    answers = sorted(outdir.glob(f"{page}.*json"), key=lambda p: (len(p.name), p.name))
    diffs, previous = [], None
    for path in answers:
        try:
            new = Differences.model_validate_json(path.read_text(encoding="utf-8")).differences
        except ValueError:
            print(f"{page}: {path} is not a valid answer, ignored", file=sys.stderr)
            continue
        # as in the loop below: each fixing answer replaces what was sent back
        if previous is not None:
            diffs = review(ocr, glm, diffs)[1]
        diffs += new
        previous = path.read_text(encoding="utf-8")
    calls, before = 0, None
    while True:
        marked, kept, unplaced, rest, problems = review(ocr, glm, diffs)
        out = outdir / f"{page}.txt"
        out.write_text(marked + "\n", encoding="utf-8")
        if previous is not None:
            report(page, marked, unplaced, rest, out)
        if previous is not None and not problems:
            return True
        if previous is not None and not unplaced and not review(ocr, glm, kept)[4]:
            # the entries found wrong were only wrong: dropping them is the whole fix
            print(f"{page}: dropped {len(diffs) - len(kept)} wrong entries", file=sys.stderr)
            diffs = kept
            continue
        if calls >= rounds:
            return previous is not None
        if problems and problems == before:
            print(f"{page}: the last fix changed nothing; stopped", file=sys.stderr)
            return True
        before = problems
        if previous is None:
            ask = prompts
        else:
            ask = prompts + ["Your answer:\n" + previous, FIX.format(problems=problems)]
        resp = client(ask, Differences)
        calls += 1
        n = len(list(outdir.glob(f"{page}.*json")))
        path = outdir / (f"{page}.json" if n == 0 else f"{page}.r{n + 1}.json")
        path.write_text(resp.text, encoding="utf-8")
        if resp.data is None:
            print(f"\n{page}: no valid JSON; the answer is in {path}", file=sys.stderr)
            return previous is not None
        diffs = kept + resp.data.differences
        previous = resp.text


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("pages", nargs="+", help="page numbers, e.g. 0195 0196")
    parser.add_argument("-o", "--outdir", required=True, type=Path,
                        help="directory for the marked pages and the raw answers")
    parser.add_argument("-r", "--rounds", type=int, default=2,
                        help="LLM calls per page at most: the first answer, then fixes (default 2)")
    parser.add_argument("--save-usage", action="store_true",
                        help="record usage regardless of the model")
    args = parse_model_args(parser=parser)

    global USAGE_PATH
    if args.model.startswith(("openai:", "gpt-")) or args.save_usage:
        USAGE_PATH = find_usage_file()

    client = Client(model=args.model, show_params=False, keep_history=False, show_usage=True)
    args.outdir.mkdir(parents=True, exist_ok=True)
    try:
        failed = run(client, args)
    finally:
        # record silently, so an interrupted run still logs what it consumed
        if client.usages and USAGE_PATH is not None:
            append_usage(sum(client.usages), args.model, USAGE_PATH)

    if client.usages:
        print(f"\n--- Total Usage ---\n{sum(client.usages)}")
        if USAGE_PATH is not None:
            print("")
            print_today_totals(USAGE_PATH, models=[args.model])
    if failed:
        print("failed: " + " ".join(failed), file=sys.stderr)
        sys.exit(1)


def run(client, args):
    """Mark each page; return the pages that failed."""
    failed = []
    for page in args.pages:
        page = f"{int(page):04d}"
        if not (ROOT / "glm-ocr" / f"{page}.txt").exists():
            print(f"{page}: no GLM-OCR text, skipped", file=sys.stderr)
            continue
        print(f"\n=== {page} ===", file=sys.stderr)
        if not mark_page(client, page, args.outdir, args.rounds):
            failed.append(page)
    return failed


if __name__ == "__main__":
    main()
