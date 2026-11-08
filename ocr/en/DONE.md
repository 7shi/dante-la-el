# Done: checking `ocr/en`

The record of the check of `ocr/en` planned in [PLAN.md](PLAN.md), step by step.

## Step 0: setup (2026-11-08)

- **Tables**: [misprints.tsv](misprints.tsv) (`page line printed fixed applied source
  note`) and [readcheck.tsv](readcheck.tsv) (`page line form decision note`), the columns
  of `ocr/la` (ocr/PLAN.md, "Decisions"); empty.
- **The baseline** of `texts/scripts/convert_en.py`, before any change: `texts/en` as
  committed (`e4b60b88`), and its output, no `ERROR` and no `NO MARKERS` line, eight
  `HYPHEN` lines (the undecided joins across a page break):

  ```
  HYPHEN 021->022: fur-nish -> furnish
  HYPHEN 081->082: un-ceasing -> unceasing
  HYPHEN 149->150: con-jured -> conjured
  HYPHEN 207->208: in-sanest -> insanest
  HYPHEN 281->282: ar-gumentum -> argumentum
  HYPHEN 295->296: fellow-citizens -> fellow-citizens
  HYPHEN 314->315: castle-signals -> castle-signals
  HYPHEN 418->419: ver-dant -> verdant
  ```

- **`convert_en.py`** taught the misprint marks: `fixed()` as in `convert_la.py`, applied
  to each page and to the hyphen vocabulary. Its output and `texts/en` unchanged.
- **`misprints.py`** moved from `ocr/la/scripts/` to [ocr/scripts/](../scripts/README.md),
  taking the directory (`uv run ocr/scripts/misprints.py ocr/en`); the page names are the
  digits of the page files (four in `la`, three in `en`). `ocr/la`: 1,053 rows, 1,050
  marks, no problems, as before; `ocr/en`: no rows, no marks.
- **Tesseract**: [tesseract/Makefile](tesseract/Makefile), `-l eng+ita`, over the pages of
  `texts/en` (taken from its page markers): 469 TSVs; four nearly empty, the pages with
  a title only (`005`, `006`, `010`, `477`).
- **The shared tools** tried on `ocr/en`:
  - `pages.py texts/en 55 57`: the pages cut at the markers `<!-- p. [1] (055) -->`, the
    front matter and the index (`<!-- p. [423] (477) -->`) too.
  - `findline.py ocr/en`: phrases found in prose, verse notes and the index; a phrase
    across a page break was not found, as the prose that runs over the page is printed
    above the verse and the notes. Taught to join each line of a page with the first line
    of the next (`063` `Grey-` / `064` `hound`: `063 3-064:1`).
  - `txtfix.py ocr/en` (a dry run, `-n`): a row applied to `072`; nothing written.
  - `wordcrop.py ocr/en … -t ocr/en/tesseract`: bands of the verse (`072` `Lontana`), the
    prose (`063` `Grey`) and the two columns of the index (`479`); a narrow page is padded
    in black on the right. A word Tesseract reads otherwise is not found (`056` `Chè`,
    read `Ché`; 0 hits): a word beside it is asked for instead.
- **The retype template**: [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md), from `la`'s: the
  conventions of [README.md](README.md) and the errors of `la`'s retypes; output
  `tmp/en-retypeNN/PAGE.txt`.
