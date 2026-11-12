# Done: checking `ocr/en-oelsner`

The record of the check ([PLAN.md](PLAN.md)), step by step.

## Step 0: setup (2026-11-13)

- **Tables**: [misprints.tsv](misprints.tsv) (`page line printed fixed applied source
  note`) and [readcheck.tsv](readcheck.tsv) (`page line form decision note`), the columns
  of ocr/PLAN.md ("Decisions"). `misprints.py ocr/en-oelsner`: 0 rows, 0 marks, 0 problems.
- **`convert_en_oelsner.py`** taught the marks: `fixed()` with the regex of
  `convert_grc.py` (the corrigenda form included), applied to each page and to the hyphen
  vocabulary (of `ocr/en-oelsner` and `ocr/en`). Its report before and after, the
  baseline, is 22 lines `ENGLISH NOTES NOT STARTING WITH A NUMBER` (the continued notes
  of `023`–`401`); `texts/en-oelsner` unchanged.
- **Tesseract**: [tesseract/Makefile](tesseract/Makefile), as `ocr/en`'s (`-l eng+ita`),
  run over the 404 pages of `texts/en-oelsner`.
- **GLM-OCR**: [glm-ocr/Makefile](glm-ocr/Makefile), as `ocr/la`'s; run over all pages by
  the user. Tried on the six trial pages first: it repeated text (`024`, `025`), dropped
  a word (`014` `The`), normalized (`Eneid`; `403` a period after `10` that is not
  printed), and found nothing the retype and Tesseract did not.
- **`ocr/scripts/cmpread.py`**: the marks of bold and italics (`**`, `*`, `_`) dropped for
  every text; `--verse-numbers` drops a number of one to three digits at a line end, alone
  or in parentheses, in all three readings (the tercet numbers). Its output on `grc`
  retype 14 unchanged but for a stray `*` of Tesseract. Tried on a copy of `014`–`015`
  with a word changed, a label moved, the tercet numbers in other forms and an italic
  added: the word listed, the label as a pair of places, the rest not.
- **The shared tools** tried: `pages.py texts/en-oelsner 14 15` (the band markers, the
  labels as comments), `findline.py` (a phrase over a line-end hyphen on `014` 10–11, a
  phrase on a label's line, a phrase in italics on `024`), `txtfix.py` on a copy (a mark
  on a label's line, the label kept), `wordcrop.py` with the Tesseract boxes.
- **`cmpread.py -g`** (step 0.7): GLM-OCR as a fourth reading; class A when Tesseract or
  GLM-OCR agrees with the retype; class D where the base and the retype agree and
  Tesseract and GLM-OCR read the same other form; a GLM-OCR page outside 1.3 times the
  base's length left out. Tried: on copies of `015` with an error put in both the base and
  the retype (`stubbern`, a comma made a period), both listed as D; the labels both OCRs
  set elsewhere not listed; for D the ligatures folded (both OCRs write `Æneas` as
  `AEneas` or `Aeneas`, `058`). On the first 75 GLM-OCR pages, `011` (3.5 times the base)
  and `058` (1.9 times, its notes written twice) left out, the others within 0.87–1.05;
  the user ran the two again, and they are used. Without `-g`, the output
  on `grc` retype 14 and on retype 01 unchanged. `check_outlier.py` flags most Italian
  pages here (they have more lines than the English): not used.
- **[TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md)** for `en-oelsner`: lines as printed with the
  hyphens, the running heads, page numbers and signature marks; the labels `**Label**`;
  the tercet numbers and italics not written.

## Step 1–2: retype 01, the trial (2026-11-13)

- **Pages** (6): `014`, `015` (a canto's first spread: the argument, the labels, the verse
  and the English), `024` (notes), `025` (a map), `249` (a genealogical table, printed
  sideways), `403` (an essay with a footnote). Retyped by **Claude (Opus 5.5)** from the
  images alone, each page in three strips at twice its size (the table rotated).
- **Compared** (`cmpread.py --verse-numbers`): `014` and `015` without a difference; the
  map and the table differ in the order of their names, so they were read name by name in
  the image instead.
- **Decided** (readcheck.tsv, 10 rows):
  - **Misread**, 7: `025` the map rewritten as printed (the base had expanded `R.` to
    `River`, lowered the capitals, made `S. MARINO` and `MONTE FELTRO` one name, added a
    `River Ombrone` not on the map, and left out `R. Adige` and `R. Reno`); `249` four
    printed periods (`ESTE.`, `II.,`, `VIII.,`, `(nat.).`); `403` 40 `edited,` without
    the comma.
  - **Misprints**, 2 (misprints.tsv): `403` 16 `10` without its period before `The
    primary division`, and `024` 47 `117)` the last note of Canto I without its period;
    the base had added both.
  - **Printed**, 1: `403` 4 `THE`, small capitals after the drop capital, the base's case
    kept ("Settled readings").
- **The retype** erred in one place: `MONTE` written twice on the map (`MONTE S. MARINO`
  and `MONTE FELTRO`; the large `MONTE` belongs to `FELTRO`).
- **The trial's lessons**: the verse and the English of `014`–`015` agreed with the base
  word for word (they had been compared with dante-corpus and `texts/en`); the notes, the
  essays, the maps and the tables are where the base differs, and where it normalized. The
  batches are 25 pages.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`002`, `022`, `036`). `misprints.py`: 2 rows, 2 marks, 0 problems.
