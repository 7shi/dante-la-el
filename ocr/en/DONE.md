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
- **`ocr/scripts/cmpread.py`** (step 2), written while the trial retype runs; tried on
  pages altered by hand: a changed word, a lost verse line (class C), a mark's printed side
  and Tesseract's agreeing word (class A) found; spacing, quotes and the note markers
  ignored; a retype identical to the base gives no place. Tesseract's words hyphenated at a
  line end are joined.
- **The retype template**: [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md), from `la`'s: the
  conventions of [README.md](README.md) and the errors of `la`'s retypes; output
  `tmp/en-retypeNN/PAGE.txt`.

## Step 1: retype, the trial (2026-11-08)

- **Retype 01** (la-el-agy, Gemini 3.8 Flash): `011`, `055`, `072`, `454`, `479`, all five
  written, none mixed up; the blocks, the verse, the verse note, the continued notes and the
  two index columns as the template asks.
- **`cmpread.py`**: 3 places, all class B, none A or C:
  - `011` `The` (the retype `THE`) and `479` `Abati` (`ABATI`): small capitals, the first
    word of a section in normal case (README.md): printed.
  - `055` `Lion`: the print has `Licn` (a `c` for the `o`), which the retype copied and
    Tesseract read `Lion`: a misprint, marked `{{Licn|Lion}}` and listed.
- No letter, word or mark of the retype against the print; the only kind of difference
  is the small capitals of a first word, which the base writes in normal case. Spacing set
  aside by the script (`072` the print's `wounded(Conv.Tr.`, written so by the retype).
- After the fixes: `misprints.py ocr/en`, 1 row, 1 mark, no problems; `convert_en.py` as
  the baseline, `texts/en` unchanged.
- Tesseract alone against the base is not listed: the trial gives it nothing to find.
- The batch size: 10 pages.
- **Retype 02** (Gemini 3.8 Flash): `005`, `009`, `010`, `012`–`018`, the title pages and
  the preface. One place, class A: `010` the base `C.`, the retype and Tesseract `C`; no
  period in the print: a misprint, marked `{{C|C.}}` and listed.
- Fifteen pages, no misreading of the base; the two finds are misprints the base had
  corrected silently, which `texts/en` corrects anyway (the user, 2026-11-08). But twelve
  of the fifteen were the front matter: retype 03 takes ten canto pages across the book
  (`095`, `136`, `175`, `215`, `255`, `295`, `335`, `375`, `415`, `445`), to decide whether
  the retype goes on.
