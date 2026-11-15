"""Reads page images with GLM-OCR through llm7shi (Ollama), writing NNN.txt for NNN.png.

    uv run ocr/scripts/glmocr.py ocr/X/*.png -o ocr/X/glm-ocr
    uv run ocr/scripts/glmocr.py ocr/X/005.png ocr/X/006.png -o ocr/X/glm-ocr [-m ollama:glm-ocr]

The same request as `ollama run glm-ocr "Text Recognition: FILE"` (the same output, checked
on a page), but llm7shi watches the stream: a page that runs away (repeats itself) is
stopped instead of filling the screen. GLM-OCR runs at temperature 0, so a stopped page is
tried once more at --retry-temperature; if that runs away too, no file is written and the
page is listed at the end (run it again, or read it otherwise). Pages whose NNN.txt exists
are skipped; a file is written only when its page is finished, so an interrupted run
leaves no partial file.

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
- **Temperature 0** is the model's default (`ollama show glm-ocr`): a second try under the
  same settings repeats the runaway, so the retry raises the temperature, once.
- **Blank pages run away**: no text to read, the model repeats garbage (a CJK character,
  code fences, "the image is too blurry ..."). They are listed unread; give them an empty
  NNN.txt by hand, as before.
- One page is sent per call to a fresh `Client` (`keep_history=False`), so no
  earlier page is resent. The model stays loaded in Ollama between calls; the first page
  pays for the load.
"""
import argparse
import sys
from pathlib import Path

from llm7shi import Client

PROMPT = "Text Recognition:"  # no trailing space (see above)


def read(image, model, temperature):
    """One call; the response, or None if it ran away or came back empty."""
    # include_thoughts=None: no `think` sent at all (see above: `think: false` changes the
    # output); retries=1: the retry at another temperature is done by the caller
    client = Client(model=model, temperature=temperature, include_thoughts=None,
                    show_params=False, keep_history=False, retries=1, file=sys.stderr)
    resp = client(PROMPT, images=[image])
    if resp.repetition or not resp.text.strip():
        return None
    return resp


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("images", nargs="+", type=Path, help="the page images (NNN.png)")
    ap.add_argument("-o", "--outdir", type=Path, required=True, help="where NNN.txt go")
    ap.add_argument("-m", "--model", default="ollama:glm-ocr",
                    help="llm7shi model name (default ollama:glm-ocr)")
    ap.add_argument("--retry-temperature", type=float, default=0.3,
                    help="temperature of the second try after a runaway (default 0.3)")
    a = ap.parse_args()

    a.outdir.mkdir(parents=True, exist_ok=True)
    todo = [p for p in a.images if not (a.outdir / f"{p.stem}.txt").exists()]
    print(f"{len(a.images)} images, {len(a.images) - len(todo)} done, {len(todo)} to read",
          file=sys.stderr)
    failed = []
    for i, image in enumerate(todo, 1):
        out = a.outdir / f"{image.stem}.txt"
        print(f"\n=== {image} ({i}/{len(todo)}) ===", file=sys.stderr)
        resp = read(image, a.model, None)
        if resp is None:
            print(f"\n{image.stem}: ran away; again at temperature {a.retry_temperature}",
                  file=sys.stderr)
            resp = read(image, a.model, a.retry_temperature)
        if resp is None:
            print(f"\n{image.stem}: ran away again; no file written", file=sys.stderr)
            failed.append(image.stem)
            continue
        text = resp.text.strip() + "\n"  # blank page: run away above, never an empty file
        out.write_text(text, encoding="utf-8")
        print(f"\n-> {out}", file=sys.stderr)
    if failed:
        print(f"\n{len(failed)} pages not read: {' '.join(failed)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
