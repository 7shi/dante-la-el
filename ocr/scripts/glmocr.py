"""Reads page images with GLM-OCR through llm7shi (Ollama), writing NNN.txt for NNN.png.

    uv run ocr/scripts/glmocr.py ocr/X/*.png -o ocr/X/glm-ocr
    uv run ocr/scripts/glmocr.py ocr/X/005.png ocr/X/006.png -o ocr/X/glm-ocr [-m ollama:glm-ocr]
    uv run ocr/scripts/glmocr.py --check -o ocr/X/glm-ocr [IMAGE...]

The same request as `ollama run glm-ocr "Text Recognition: FILE"` (the same output, checked
on a page), but llm7shi watches the stream: a page that runs away (repeats itself) is
stopped instead of filling the screen. A stopped page is written as it stood when stopped
and listed at the end, to be looked at and cut by hand (GLM-OCR runs at temperature 0, so
trying again gives the same text: there is no retry). Pages whose NNN.txt exists are
skipped; a file is written only when its page is finished or stopped, so an interrupted
run (Ctrl+C) leaves no partial file.

--check reads nothing: it lists the NNN.txt already written (all of OUT, or those of the
IMAGEs given) that show a runaway (`runaway`: a repetition, or a code fence), and the
repeated text.

Found while making it (ocr/en-paradiso, 2026-11-15, Ollama 0.30.6 server, client 0.32.15;
the output compared with `ollama run` on 020, a page of the Italian with notes):

- **No `think` at all.** llm7shi passes `think=include_thoughts`; for a model without the
  thinking capability (GLM-OCR) it falls back to `think: false`, still sent. Sending
  `think: false` changes GLM-OCR's output: on 020 the marginal label was read into the
  first line ("Salita. La provvidenza"), a stray mark began a note, the page number at
  the foot was lost; on a blank page it emitted Markdown fences without end. `ollama run`
  sends no `think`; `include_thoughts=None` makes llm7shi send none either.
- **The prompt is "Text Recognition:", no trailing space.** `ollama run` takes the image
  path out of its prompt; its output is matched only without the space left behind (as
  "Text Recognition:", "Text Recognition: [img-0]" also match). A trailing space changes
  the output too (the label in the first line again, the page foot lost).
- With both, the text equals `ollama run`'s and the plain `ollama.Client().chat()`'s
  (only the final blank line differs: the text is written stripped, with one newline).
- **Temperature 0** is the model's default (`ollama show glm-ocr`): every try gives the
  same text, a runaway included, so a stopped page is not tried again (`retries=1`).
- **Blank pages run away**: no text to read, the model repeats garbage (a CJK character,
  code fences, "the image is too blurry ..."). They are written and listed like any
  stopped page; empty such a NNN.txt by hand.
- **Code fences mark a runaway too**: GLM-OCR may restart the page inside "```markdown"
  and then repeat the page, or the fences alone, without end. llm7shi's check of the
  stream stops some of these, not all (005, the half-title, was written whole: the page
  three times between fences); so `runaway` also takes "```" anywhere as a sign.
- One page is sent per call to a fresh `Client` (`keep_history=False`), so no
  earlier page is resent. The model stays loaded in Ollama between calls; the first page
  pays for the load.
"""
import argparse
import re
import sys
from pathlib import Path

from llm7shi import Client

PROMPT = "Text Recognition:"  # no trailing space (see above)


# A repetition: a stretch of UNIT characters or more (across lines too) followed at once,
# after nothing but white space, by itself TIMES - 1 times more; or a short pattern
# repeated end to end over RUN characters or more (a character or a fence without end).
# Not llm7shi's detect_repetition, which is made to stop a stream early and safely, not to
# judge a finished page. Every page listed is looked at and cut by hand, so the check
# errs on the side of listing: missing a runaway costs more than looking at a page that
# is right. The poem's own repetitions are listed too ("me alone, me alone", "con gli
# occhi gli occhi", "non pianger anco, non pianger ancora", 10-18 characters), and dot
# leaders; GLM-OCR's repeats seen were 20 characters or more (a note's last sentence
# written twice: "See Inf. ii. 52 sqq."), but shorter ones are not ruled out.
TIMES, UNIT, RUN = 2, 10, 30


def repetition(text, times=TIMES, unit=UNIT, run=RUN):
    """The first repeated stretch of a text, or None."""
    m = re.search(r"(\S.{%d,}?)(?:\s*\1){%d}" % (unit - 1, times - 1), text, re.S)
    if m:
        return m.group(1)
    for m in re.finditer(r"(\S.{0,%d}?)\1+" % (unit - 2), text, re.S):
        if len(m.group(0)) >= run:
            return m.group(1)
    return None


def runaway(text):
    """The signs of a runaway in a page's text: a repetition, or a code fence."""
    signs = []
    r = repetition(text)
    if r:
        signs.append(f"repetition {r[:40]!r}")
    if "```" in text:
        signs.append("```")
    return signs


def check(paths):
    """Lists the files that show a runaway; returns their number."""
    found = 0
    for f in paths:
        signs = runaway(f.read_text(encoding="utf-8"))
        if signs:
            found += 1
            print(f"{f}: {', '.join(signs)}")
    print(f"{len(paths)} files checked, {found} with a runaway", file=sys.stderr)
    return found


def read(image, model):
    """One call; the response, stopped or not (resp.repetition)."""
    # include_thoughts=None: no `think` sent at all (see above: `think: false` changes the
    # output); retries=1: at temperature 0 a second try repeats the first
    client = Client(model=model, include_thoughts=None, show_params=False,
                    keep_history=False, retries=1, file=sys.stderr)
    return client(PROMPT, images=[image])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("images", nargs="*", type=Path, help="the page images (NNN.png)")
    ap.add_argument("-o", "--outdir", type=Path, required=True, help="where NNN.txt go")
    ap.add_argument("-m", "--model", default="ollama:glm-ocr",
                    help="llm7shi model name (default ollama:glm-ocr)")
    ap.add_argument("--check", action="store_true",
                    help="read nothing; list the files in OUTDIR that show a runaway")
    a = ap.parse_args()

    if a.check:
        paths = [a.outdir / f"{p.stem}.txt" for p in a.images] if a.images \
            else sorted(a.outdir.glob("*.txt"))
        check([p for p in paths if p.exists()])
        return
    if not a.images:
        ap.error("no images given")

    a.outdir.mkdir(parents=True, exist_ok=True)
    todo = [p for p in a.images if not (a.outdir / f"{p.stem}.txt").exists()]
    print(f"{len(a.images)} images, {len(a.images) - len(todo)} done, {len(todo)} to read",
          file=sys.stderr)
    stopped = []
    for i, image in enumerate(todo, 1):
        out = a.outdir / f"{image.stem}.txt"
        print(f"\n=== {image} ({i}/{len(todo)}) ===", file=sys.stderr)
        resp = read(image, a.model)
        text = resp.text.strip()
        out.write_text(text + "\n" if text else "", encoding="utf-8")
        if resp.repetition or runaway(text):
            stopped.append(image.stem)
            print(f"\n-> {out} (ran away)", file=sys.stderr)
        else:
            print(f"\n-> {out}", file=sys.stderr)
    if stopped:
        print(f"\n{len(stopped)} pages ran away (stopped or with a sign), written as they stood: "
              f"{' '.join(stopped)}", file=sys.stderr)


if __name__ == "__main__":
    main()
