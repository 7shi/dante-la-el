# Scripts for `ocr/la`

The scripts that made and checked `ocr/la`, Serravalle's translation and commentary
(1891). Run them from the repository root with `uv run ocr/la/scripts/NAME.py`. They find
`ocr/la` (pages, images, `tesseract/`) from their own place, and import each other from
this directory (`import lemmacheck as L`). A script that reads `ocr/la` removes the italic
marks `*…*` first (`check.unmark()`). The paid calls (`markup.py`, `markdecide.py`) are
run by the user (PLAN.md, "Standing rules").

The sections follow the order of use. "Procedure" and "item" refer to
[DONE.md](../DONE.md) ("Procedure for a batch", "Work items"); the checks are those of
[PLAN.md](../PLAN.md) ("Checks") and DONE.md. TESS is Tesseract's directory of word lists,
`ocr/la/tesseract`; WORK a work directory of the markup method.

## 1. The verse columns (item 1)

The Italian or Latin verse was missing from many canto pages; these found the gaps and
transcribed them from the image.

- `survey.py [--cantos | --work FIRST LAST] [-o OUT]`: the survey of the verse blocks
  (texts/PLAN.md, step 1): which pages lack the Italian or the Latin column, per page, per
  canto, or as the work list of a batch. It reads dante-corpus as a dependency in
  `../dante-corpus` (README.md).
- `versecrop.py PAGE... -t TESS -o OUTDIR [-c it|la]`: crops the verse column missing from
  a page (found from the other column's lines in Tesseract's words and the blank band
  between the columns), for its transcription; `crops.tsv` lists the boxes and the line
  counts to look at. `-c` crops that column also where the file has it (the trial).
- `verseread.py CROPS [PAGE...] -m MODEL [-n N] [--fake] [--check]`: transcribes each crop
  with a model, from the image only (tercet number and text of each line apart;
  superscripts and `(¹)` written by the script): `CROPS/read/PAGE.txt`, the answers
  `PAGE.MODEL.json` reused on a rerun. `--check` compares with the same column of `ocr/la`
  (`read/check.txt`).
- `verseinsert.py PAGE... -d DIR [-n]`: inserts the checked Italian verse (`DIR/PAGE.txt`)
  before the page's Latin block; the Latin tercet numbers made superscript and set to the
  Italian's line by line, every number added or changed listed (to check in the image); a
  page whose Latin line count differs is left as it is.

## 2. The two-OCR markup (procedure, steps 2–7)

`ocr/la` and GLM-OCR fail in different ways: their disagreements are marked in the page
and decided (DONE.md, "The method").

- `markup.py -m MODEL -o WORK/markup PAGE...` (paid): marks where the two OCRs of a page
  disagree, `{{ocr|glm}}`, without looking at the image; the model returns only a list of
  differences, so it cannot alter the text.
- `markprep.py WORK PAGE... -t TESS`: resolves the trivial marks, makes the crops of the
  others and `WORK/ask.txt` (steps 2–3).
- `markdecide.py WORK -m MODEL [-n N] [--fake]` (paid): asks a model, mark by mark, which
  reading the crop shows.
- `markresolve.py WORK -t TESS [-p FIRST LAST] [--light] [--write]`: routes the marks,
  writes `review.tsv` and `WORK/out/`; with `--write` also `ocr/la/PAGE.txt`.
- `view.py review|context|next|word|strip`: views for the review and the checks (steps 6,
  8; one stacked PNG per call); `view.py word` is the view for deciding a word in the image.
- `mine.py WORK PAGE K=DECISION[|NOTE] …`: appends review decisions to `WORK/mine.tsv`
  (step 6).
- `retype.py WORK PAGE FILE NOTE [--old PART]`: a `fixes.tsv` row replacing a page (or a part
  of it) of `WORK/out/` by its retyped text (step 6).

## 3. The page checks (steps 8–9)

Run over every page after a change; their output is compared with the previous run.

- `lines.py FIRST LAST -t TESS [-o OUT]`: rules without a blank line, printed lines broken
  in two, dots before a lowercase word (step 8).
- `check.py FIRST LAST [-d DIR]... [-v] [-o OUT]`: tercet numbers (order, every third line,
  continuity across pages) and the section rules of the images against the blank lines
  (the rule count often misses right-column and page-end rules: look at a listed page).
- `lostcheck.py FIRST LAST -t TESS [-g GLM] [-d DIR ...] [-n N] [-v] [-o OUT]`: text lost
  from a page: runs of 4+ words of Tesseract and GLM-OCR found nowhere in the page file,
  matched loosely (three-word runs, similarity 75) and in any order; `both` (the two OCRs
  agree) is lost text, `tess`/`glm` mostly one OCR's noise. It does not see lines out of
  order or run together. `-d` reads another directory first (e.g. `WORK/out`).
- `seqcheck.py FIRST LAST [-d DIR ...] [-v] [-o OUT]`: per page, verse blocks whose tercet
  numbers skip, Italian and Latin numbers that differ, plain-digit tercet numbers,
  leftovers (`(1)`, `<sup>`, `[For `, a `—` line, double spaces), indented lines.

The conversion into `texts/la/` (step 11) is `texts/convert_la.py`, outside this directory.

## 4. The checks after completion

For errors that both OCRs share (PLAN.md, "Checks"; DONE.md, one section each).

- **Check 1**: `lemmacheck.py FIRST LAST [-v] [--crops DIR] [--readings DIR] [-o OUT]`: the
  lemmas of the commentary against the verse they quote; `--crops` writes the line images
  of the candidates, `--readings` compares a reader's `DIR/readings.tsv`. Its helpers
  (tokens, Tesseract boxes, crops) serve the later checks.
- **Verse check**:
  - `versepairs.py [FILES] [-d DIR | -o OUT]`: the verse of the cantos in `texts/la`, the
    Italian and the Latin line side by side, one TSV per canto (step 0).
  - `versecheck.py FIRST LAST [--italian] (--crops DIR | --page-crops DIR | --readings DIR
    [-o OUT] | --page-readings DIR [-o OUT])`: the line or page images of the Latin (or
    Italian) verse, and the comparison of a reader's `DIR/readings.tsv` with `ocr/la`.
- **Italics**:
  - `italic.py FIRST LAST -t TESS [-o OUT] [-v] [--boxes DIR]`: the italic words of the
    commentary by their slant (step 1).
  - `italicmark.py SLANT -d OUTDIR [-o FLAGS] [--pages SPEC] [--join]`: the marks set from
    `italic.py -v`, and the lines to look at in the image (step 3).
- **Check 2**:
  - `lexcheck.py FIRST LAST [-o OUT] [-g G]`: rare forms near common ones, in three groups by
    Tesseract's word.
  - `lexcrop.py LIST FIRST LAST [-g G] (--crops DIR [--labels] | --readings READ [-o OUT] |
    --lines OUT)`: for group 2 the crops of the candidates' words with the masked lines
    (`context.tsv`) for a blind reader, and the comparison of the reader's TSV with the
    forms; for group 3 each word in its lines, for a reader by the sense.
