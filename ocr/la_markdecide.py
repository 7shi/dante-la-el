"""Ask a model, mark by mark, which reading the print shows in the crop of the mark.

    la_markdecide.py WORK -m MODEL [-n N] [--fake]

Reads WORK/post/, WORK/locate.tsv, WORK/crops/ and WORK/ask.txt (la_markprep.py). For each
mark of ask.txt, one call with a new Client, so that images do not pile up in a history:
the crop at the scan's own resolution, the passage around the place (8 words a side, the
place shown as ⟦…⟧), and the two readings in an order fixed by a hash of the mark, so that
the side (ocr/la or GLM-OCR) is not given away. The model writes what the print shows
first, then chooses: 1, 2, neither, unreadable, or wrong place.

Measured on proofread pages: right on 45 of 48 letter marks, but it reads the common form
for a misprint (9 of 15) and misses faint semicolon tails; so la_markresolve.py takes its
answer only with Tesseract's agreement, and every change to ocr/la is checked by hand.

Every answer is saved as WORK/ans/PAGE-LINE-HASH.MODEL.json and reused on a rerun, so no
call is made twice. HASH (of the two readings) names the mark, not its index on the page,
which changes when la_markprep.py resolves more marks; the order of the readings shown
follows the same name. WORK/decide.tsv lists the verdicts (left, right, neither, unreadable, wrong
place) with the reading."""

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from llm7shi import Client
from llm7shi.response import Response
from llm7shi.usage import append_usage, find_usage_file, print_today_totals
from llm7shi.utils import parse_model_args

import la_markup as M

CTX = 8  # words of the passage on each side of the place


class Decision(BaseModel):
    reading: str = Field(description="exactly what the print shows at the marked place: "
                         "letters, accents, apostrophes, punctuation and spaces as printed; "
                         "empty if the print has nothing there")
    verdict: Literal["1", "2", "neither", "unreadable", "wrong place"] = Field(
        description="1 or 2: the reading that is exactly the print; neither: the print "
        "differs from both (then `reading` is the print); unreadable: the scan does not "
        "show it clearly enough; wrong place: the passage is not in the image")


PROMPT = """The image is a crop from a page printed in 1891 (Italian and Latin, the Latin with
medieval spellings). The passage below stands in it; two OCRs disagree at the place marked ⟦…⟧.

Passage: {passage}

Reading 1: {one}
Reading 2: {two}

Look at the place in the image and write in `reading` exactly what is printed there, letter
by letter, then choose the reading that matches the print exactly.

- Report the print, not the correct form: misprints and unusual spellings are kept.
- Check accents (à è é ì ò ù), apostrophes, capitals and punctuation.
- A colon is two round dots; a semicolon has a dot above a comma, with a tail below the
  line. A comma has a tail; a full stop is a round dot.
- A superscript number before a verse line is a tercet number.
- If the scan has lost the detail that decides it, answer `unreadable`."""


def show(s): return "(nothing)" if not s.strip() else "`" + s.replace("\n", " ⏎ ") + "`"


def passage(t, m):
    """The left-side text around mark m, the place shown as ⟦…⟧."""
    before = M.MARK.sub(lambda x: x.group(1), t[:m.start()])
    after = M.MARK.sub(lambda x: x.group(1), t[m.end():])
    return f"{' '.join(before.split()[-CTX:])} ⟦…⟧ {' '.join(after.split()[:CTX])}".strip()


def mark_name(p, line, l, r):
    return f"{p}-{line}-{hashlib.md5(f'{l}|{r}'.encode()).hexdigest()[:8]}"


def swapped(name): return hashlib.md5(name.encode()).digest()[0] % 2 == 1


class Fake:
    """Answers without calling: the reading of side 1 and verdict 1 (for tests)."""
    def __init__(self): self.usages = []

    def __call__(self, prompt, schema=None, images=None):
        one = re.search(r"^Reading 1: (.*)$", prompt[-1], re.M)[1]
        r = Response(); r.text = Decision(reading=one.strip("`"), verdict="1").model_dump_json()
        return r


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("work", type=Path, help="the work directory of la_markprep.py")
    ap.add_argument("-n", "--limit", type=int, help="ask at most N new questions")
    ap.add_argument("--fake", action="store_true", help="no calls: answer side 1 (for tests)")
    ap.add_argument("--save-usage", action="store_true", help="record usage regardless of the model")
    args = parse_model_args(parser=ap)
    w = args.work
    (w / "ans").mkdir(exist_ok=True)
    ask = (w / "ask.txt").read_text(encoding="utf-8").split()
    usage = find_usage_file() if not args.fake and (
        args.model.startswith(("openai:", "gpt-")) or args.save_usage) else None
    tag = "fake" if args.fake else re.sub(r"[^\w.-]+", "_", args.model)
    rows = ["page\tline\tk\tleft\tright\tverdict\treading\tcrop"]
    pages, clients, asked, skipped = {}, [], 0, 0
    try:
        for name in ask:
            p, line, k = name.split("-")
            if p not in pages: pages[p] = list(M.MARK.finditer((w / "post" / f"{p}.txt").read_text(encoding="utf-8")))
            m = pages[p][int(k)]
            t = m.string
            l, r = m.groups()
            assert t[:m.start()].count("\n") + 1 == int(line), name
            key = mark_name(p, line, l, r)
            ans = w / "ans" / f"{key}.{tag}.json"
            sw = swapped(key)
            one, two = (r, l) if sw else (l, r)
            if not ans.exists():
                if args.limit is not None and asked >= args.limit:
                    skipped += 1; continue
                client = Fake() if args.fake else Client(
                    model=args.model, show_params=False, keep_history=False, show_usage=True)
                clients.append(client)
                prompt = PROMPT.format(passage=passage(t, m), one=show(one), two=show(two))
                print(f"\n=== {name} ({key}) ===", file=sys.stderr)
                resp = client([prompt], Decision, images=[w / "crops" / f"{name}.png"])
                asked += 1
                ans.write_text(resp.text, encoding="utf-8")
            try:
                d = Decision.model_validate_json(ans.read_text(encoding="utf-8"))
            except ValueError:
                print(f"{name}: invalid answer in {ans}", file=sys.stderr); continue
            v = {"1": "right" if sw else "left", "2": "left" if sw else "right"}.get(d.verdict, d.verdict)
            rows.append("\t".join([p, line.lstrip("0"), k, l.replace("\n", "⏎"), r.replace("\n", "⏎"),
                                   v, d.reading.replace("\n", "⏎"), f"{name}.png"]))
    finally:
        used = [u for c in clients for u in c.usages]
        if used and usage is not None: append_usage(sum(used), args.model, usage)
        (w / "decide.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    if used:
        print(f"\n--- Total Usage ---\n{sum(used)}")
        if usage is not None: print_today_totals(usage, models=[args.model])
    print(f"asked {asked}, answered {len(rows) - 1} of {len(ask)}"
          + (f", {skipped} left for a later run" if skipped else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
