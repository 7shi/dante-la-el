# Plan: checking `ocr/en`

The check of `ocr/en`, Carlyle's prose translation of the Inferno with the Italian text and
his notes (1889), by the flow of [ocr/PLAN.md](../PLAN.md): the first of the three texts
(decided with the user, 2026-11-08). The work done is recorded in [DONE.md](DONE.md) (to be
written as the steps go); the conversion into `texts/en/` is described in
[texts/PLAN.md](../../texts/PLAN.md) ("`texts/en/`"), the conventions of the transcription in
[README.md](README.md).

**A new session starts here**: read "State". The rules of ocr/PLAN.md ("Decisions",
"Read-through") apply.

## State (2026-11-09)

Step 1 done to `400` (retypes 01–18, DONE.md). Next: the batches of about 25 pages from
`401` (the pages retyped in retype 03 left out), each checked and decided as it comes back,
the next batch sent first.

## The text

- **Pages**: 514 scans; 469 of them are in `texts/en` (`005`–`486` without the pages
  excluded in texts/PLAN.md, "Files"). Only these are
  checked; Bohn's catalogue (`487`–`510`), the covers and the blank pages are not.
- **Kinds of page**: the front matter (prefaces, manuscripts and editions, comments and
  translations: English prose with quotations); the cantos `055`–`476` (an argument, the
  English prose above, the Italian verse, the verse notes `1. …`, the footnotes `1 …`);
  the index of proper names (`477`, `479`–`486`, one entry per line).
- **Its transcription**: GLM-OCR, proofread against the images by Gemini 3.8 Flash, then a
  final check (README.md, "Credits"); then the curly quotes as printed, the footnote
  markers restored on every page, and the Italian verse compared with dante-corpus (every
  line aligned; the five below 0.75 similarity are readings of this edition: texts/PLAN.md,
  "Procedure"). A word-level misreading in the verse that still aligns, and any misreading
  in the English and the notes, may remain.
- **Not transcribed**: the italics, the running heads, the page numbers, the verse
  numbers (README.md, "Notes on the transcriptions"). The checks do not add them.

## The readings to compare

- **The base**: `ocr/en` itself, with its fixes kept unless the image says otherwise.
- **The retype**: every page from the image alone by la-el-agy on Gemini 3.8 Flash (step 1).
  The proofreading of `ocr/en` was a correction of GLM-OCR's text, so it kept what it did
  not see; a retype from the image alone is a reading of its own.
- **Tesseract** (`-l eng+ita`), the third vote and the word boxes for `wordcrop.py`.
- GLM-OCR is not a second reading here: it is the source of the base. Its raw output is
  in the history (`c5e60ce5`, before the proofreading `b817a2be`) and is not needed.

## Steps

0. **Setup**:
   1. `ocr/en/misprints.tsv` and `ocr/en/readcheck.tsv` with the columns of `la`
      (ocr/PLAN.md, "Decisions"); `ocr/en/DONE.md`.
   2. `ocr/la/scripts/misprints.py` made to take the directory (moved to `ocr/scripts/`),
      and `texts/scripts/convert_en.py` taught the marks (`fixed()` as in
      `convert_la.py`; its hyphen vocabulary from the fixed side). The output of
      `convert_en.py` before any change kept as the baseline; `texts/en` unchanged by
      these script changes.
   3. `ocr/en/tesseract/`: a Makefile as `ocr/la/tesseract/Makefile`, with `-l eng+ita`
      and the three-digit page names, run over the 469 pages.
   4. The shared tools tried on `ocr/en`: `pages.py texts/en` (its page markers
      `<!-- p. 2 (056) -->`), `findline.py`, `wordcrop.py -t ocr/en/tesseract`, `txtfix.py`.
   5. `TEMPLATE-RETYPE.md` for `en`, from [../la/TEMPLATE-RETYPE.md](../la/TEMPLATE-RETYPE.md):
      the conventions of README.md (one paragraph per line, one verse per line, blocks
      apart by blank lines, no running heads, page numbers or verse numbers, the footnote
      markers as superscript digits where printed, the footnotes `1 …` at the page end, a
      continued note first and unnumbered, small capitals in uppercase, curly quotes as
      printed, no italics); the errors of `la`'s Flash retypes (spellings normalized,
      misprints corrected, colons made semicolons, specks read as marks, accents added to
      the Italian); output one file per page, `tmp/en-retypeNN/PAGE.txt`.
1. **Retype** (la-el-agy, Gemini 3.8 Flash; the user sets the model and gives the signal
   before each batch; the model of each batch recorded in DONE.md):
   - **Trial**: 5 pages of different kinds: a preface page (`011`), a canto opening with
     the argument (`055`), a canto page with a verse note, a note continued and long notes
     (`072`), a page of a continued note only (`454`), an index page (`479`). Checked by
     eye and by the script of step 2; the batch size is set from it (`la`'s retypes: 7–11
     pages; Flash grew worse on longer batches).
   - **Whether to go on** (decided with the user, 2026-11-09): the trial and retype 02
     (front matter) found no misreading; ten canto pages across the book (retype 03) found
     one (`375` `ei` for `el`), which the comparison with dante-corpus had let pass. To
     `100` (retypes 04–06, 25–28 pages each, no loss of care in the later pages): a few
     misreadings (a word, a colon, breaks kept at a line end, points), small capitals in
     normal case against README.md, and misprints the base had corrected silently (turned
     `n`s). The retype goes on over the whole text, 25 pages a batch.
   - **Batches** in page order; on each reply the next batch is sent first, then the
     returned one checked (pages present, none mixed up).
2. **Compare and decide**, batch by batch as the retypes come back:
   - A script `ocr/scripts/cmpread.py` (new, for all texts): for each page, the words of
     `ocr/en`, the retype and Tesseract, normalized first (quotes straight or curly,
     dashes, spacing, the superscript markers set aside: they were checked already), and
     aligned word by word. It lists every place where the base differs from the retype,
     with Tesseract's word beside it, in classes: **A**, the retype and Tesseract agree
     against the base; **B**, the retype alone differs; **C**, a run of words one reading
     lacks (lost text, a line doubled). Tesseract alone differing is not listed unless the
     trial shows it finds errors.
   - Decided in the image ("Decisions"), in stacked crops (`wordcrop.py`): A and C each
     one; B with care, as the retype's habits above are its likely cause. Fixes and marks
     with `txtfix.py`; every decision a row of `readcheck.tsv` (note `cmp A`, `cmp B`,
     `cmp C`).
   - After each batch: `convert_en.py` and `misprints.py` compared with the baseline (the
     verse count, the footnote numbering and references).
3. **Read-through** (ocr/PLAN.md, "Read-through") over `texts/en`: a trial of about 20
   pages, then batches of 25 scans (about 19); decisions as in step 2 (note `read`).
4. **Close**: the state here, DONE.md, a SUMMARY.md; texts/PLAN.md "Status" and the README
   of `ocr/en` (the check in "Credits"); commits, `ocr/en` and `texts/en` apart, when the
   user asks.

## Settled readings

The edition's readings found in the steps go here, and are applied, not asked again.

- **Small capitals** in running text in uppercase (README.md), the base's normal case
  corrected where a retype shows them (`DIVINA`, `MSS.`, `OTTIMO`); the first word of a
  section or a canto in normal case (`The`, `Abati`).
- **A misprint the base had corrected silently** (a turned `n`, `Lion` for `Licn`) is
  marked and listed when found; it is not sought, as `texts/en` corrects it anyway.
