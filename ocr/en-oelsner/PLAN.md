# Plan: checking `ocr/en-oelsner`

The check of `ocr/en-oelsner`, the Temple Classics Inferno (1903): the Italian edited by H.
Oelsner, Carlyle's prose translation revised by him, and his notes. It follows the flow of
[ocr/PLAN.md](../PLAN.md) and is the last of the three texts, after `ocr/en`
([../en/SUMMARY.md](../en/SUMMARY.md)) and `ocr/grc` ([../grc/SUMMARY.md](../grc/SUMMARY.md)).
The work done is recorded in [DONE.md](DONE.md), to be written as the steps go. The
conversion into `texts/en-oelsner/` is described in [texts/PLAN.md](../../texts/PLAN.md)
("`texts/en-oelsner/`"), the transcription in [README.md](README.md), and the structure in
[INDEX.md](INDEX.md).

**A new session starts here**: read "State". The rules of ocr/PLAN.md ("Decisions",
"Read-through") apply.

## State (2026-11-13)

Step 0 (setup) done, and the trial (retype 01: `014`, `015`, `024`, `025`, `249`, `403`)
decided (DONE.md). GLM-OCR is run over all pages by the user, in page order (its
batches 1–5); `cmpread.py` takes it (step 0.7, done). Retypes 02 (`007`–`037`), 03
(`038`–`062`), 04 (`063`–`087`), 05 (`088`–`112`), 06 (`113`–`137`), 07 (`138`–`162`), 08 (`163`–`187`), 09 (`188`–`212`), 10 (`213`–`237`), 11 (`238`–`262`), 12 (`263`–`287`) and 13 (`288`–`312`) decided. Next: retype 14, the
batches of 25 pages in page order from `313`, each decided once GLM-OCR has read its pages ("Steps" 2).

## The text

- **Pages**: 416 scans; 404 of them are in `texts/en-oelsner`, and only these are checked.
  The excluded scans are `001`–`006`, `009`, `012` and `413`–`416`: covers, library leaves
  and blank leaves (texts/PLAN.md, "Files"). The leaf with pp. 385–386 (Canto XXXIV) is
  missing from the scan and is not checked.
- **Kinds of page**:
  - The front matter (`007`, `008`, `010`, `011`, `013`): a few lines each.
  - The cantos `014`–`402`, on facing pages:
    - The even pages carry the Italian verse, with the editor's marginal labels and the
      tercet numbers.
    - The odd pages carry the English, one paragraph per tercet, with their own labels.
    - The argument runs across the first spread of a canto.
    - The notes, keyed to verse numbers, run across the page bottoms and over whole pages,
      quoting Italian and Latin.
  - The maps, plates and tables printed after some cantos (`025`, `037`, `133`, `191`,
    `249`, `284`, `321`, `345`): their captions and names.
  - The end matter (`403`–`412`): Wicksteed's two essays (`405` a table), the two plates,
    the editorial note, and the index to the maps.
- **Its transcription**: Gemini 2.5 Flash, proofread against the images by GPT-6 Luna,
  then a final check (README.md, "Credits"). Lines are as printed, with line-end hyphens,
  running heads, page numbers, signature marks and tercet numbers. The marginal labels are
  `**Label**` at the start of their line, and italics are `*…*` (on some pages `_…_`).
  For the conversion, `ocr/en-oelsner` was normalized: labels, paragraph breaks, and
  transcriber's notes deleted (texts/PLAN.md, "Conversion notes").
- **Checked already** (texts/PLAN.md, "Conversion notes"):
  - The Italian lines against dante-corpus.
  - The English against `texts/en`, Carlyle's own edition of the translation; every
    difference had to be an Oelsner revision or a variant. That comparison was made
    before `ocr/en` was checked (2026-11-08 – 2026-11-10).
  - The English paragraphs of each page against the tercets of the facing page.
  - The verse count of every canto.
- **What no check has read**: the notes, the arguments, the labels, the end matter, and
  any misreading in the verse or the English that a comparison passed as a variant. The
  notes are the most text not compared with anything.
- **No corrigenda** are printed in the book (no list of errata in `ocr/en-oelsner`).

## The readings to compare

- **The base**: `ocr/en-oelsner` itself, its fixes kept unless the image says otherwise.
- **The retype**: every page from the image alone, by Claude (step 1). It does not use
  any other reading, so it does not wait for them.
- **Tesseract** (`-l eng+ita`, with `lat` on the notes if the trial shows it helps): the
  third vote, and the word boxes for `wordcrop.py`.
- **GLM-OCR** (`ocr/en-oelsner/glm-ocr/`, run by the user with its
  [Makefile](glm-ocr/Makefile), the la way): the fourth reading, compared with the others
  after the retype (step 2). On the trial pages it repeated text (`024`, `025`), dropped
  words and normalized (`Eneid`, a period after `10` on `403`), and found nothing new;
  it is used for two things, not alone:
  - a vote beside Tesseract's, so that a place where the retype differs from the base
    is decided with two independent readings in view;
  - the places where the base and the retype agree and GLM-OCR and Tesseract both differ
    from them: an error the base and the retype share, which no other comparison shows.

  A page where it ran away (a loop, a repeated block) is found by its length against the
  base and is not used (`cmpread.py --glm-ratio`, below). `check_outlier.py`, used for
  `ocr/la/glm-ocr`, does not fit this book: it compares the pages with each other, and the
  Italian pages have many more lines than the English.

## Steps

0. **Setup**:
   1. `misprints.tsv` and `readcheck.tsv` with the columns of ocr/PLAN.md ("Decisions");
      `DONE.md`.
   2. `texts/scripts/convert_en_oelsner.py` taught the marks: `fixed()` with the regex of
      `convert_grc.py`, the corrigenda form included, and applied to each page and to the
      hyphen vocabulary. Its output before any change is kept as the baseline; `texts/en-oelsner`
      must be unchanged by this. `uv run ocr/scripts/misprints.py ocr/en-oelsner`: 0 rows.
   3. `ocr/en-oelsner/tesseract/`: a Makefile as `ocr/en/tesseract/Makefile`, with
      `-l eng+ita`, run over the 404 pages.
   4. `ocr/scripts/cmpread.py` made ready for this text: the marks of bold and italics
      (`**`, `*`, `_`) dropped for every text, so that labels and italics do not count;
      with `--verse-numbers`, a number of one to three digits at a line end, alone or in
      parentheses (`(7)`), dropped in all three readings, as the tercet numbers of the base
      are transcribed in several forms. The running heads and page numbers are compared
      (the retype writes them as printed). Tried on a copy of a page with a word changed
      and a label moved: the word listed, the italics and the tercet numbers not; a label
      moved by a line shows as a pair of places (gone, added), decided as any other.
   5. The shared tools tried on `ocr/en-oelsner`: `pages.py texts/en-oelsner` (its band
      markers `<!-- p. 2 (014), text -->`), `findline.py`, `wordcrop.py -t
      ocr/en-oelsner/tesseract`, `txtfix.py`. `txtfix.py` must not disturb a label on the
      line it changes.
   6. [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md) for `en-oelsner`, from
      [../en/TEMPLATE-RETYPE.md](../en/TEMPLATE-RETYPE.md), with the conventions of
      `ocr/en-oelsner`: lines as printed, with the hyphens, the running heads, page numbers
      and signature marks; labels `**Label**` at the start of their line; the tercet
      numbers and the italics not written; blank lines between paragraphs; the maps and
      tables line by line. It also lists the errors seen in the retypes of `en` and `grc`
      (spellings normalized, misprints corrected, colons made semicolons, the grammar's
      form for the printed one, accents added to the Italian). Output is one file per
      page, `tmp/en-oelsner-retypeNN/PAGE.txt`; the comparison is run with
      `--verse-numbers`.
   7. `ocr/scripts/cmpread.py` taught a fourth reading: `-g DIR` (here
      `ocr/en-oelsner/glm-ocr`), normalized as the retype; its words given beside
      Tesseract's in each place. Class A when Tesseract or GLM-OCR agrees with the retype
      against the base; a new class **D** for a place where the base and the retype agree
      and GLM-OCR and Tesseract both read the same other form (words both lack are not
      listed: a label they set elsewhere). A GLM-OCR page whose length is not within 1.3
      times the base's is left out, said so on stderr. Without `-g` the output is
      unchanged (checked on `grc` retype 14 and `en-oelsner` retype 01).
1. **Retype** every page from the image alone (Claude; "Decisions for this text"):
   - **Trial**: 6 pages of different kinds:
     - a canto opening with the argument and labels (`014`, `015`);
     - a page of notes with italics (`024`);
     - a map (`025`);
     - a genealogical table (`249`);
     - an essay page (`403`).

     The pages are checked by eye and by `cmpread.py`. The trial decides two things: the
     batch size (25 pages for `en` and `grc`), and whether GLM-OCR helps.
   - **Batches** in page order, about 16 of 25 pages. The retype goes on without waiting
     for the deciding: a batch is decided (step 2) once GLM-OCR has read its pages, so a
     batch whose GLM-OCR pages are not there yet is retyped and its deciding left for
     later. Each batch is decided in full once; no batch is decided before GLM-OCR and
     looked at again afterwards. If the user switches to la-el-agy: on each reply the
     next batch is sent first, then the returned one checked (pages present, none mixed
     up).
2. **Compare and decide**, batch by batch, as for `en` and `grc`, with GLM-OCR added:
   - Before a batch: its GLM-OCR pages all present (a page left out as a run-away is
     listed by `cmpread.py`; the user may run it again).
   - `uv run ocr/scripts/cmpread.py ocr/en-oelsner tmp/en-oelsner-retypeNN -g ocr/en-oelsner/glm-ocr --verse-numbers -o tmp/en-oelsner-cmpNN.tsv`.
   - Classes A, C and D are decided each one, B with care. GLM-OCR's habits (normalized
     forms, a period or a word added, the names of a map in its own order) are known
     from the trial: its vote alone does not decide, the image does.
   - Fixes and marks are made with `txtfix.py`, and every decision is a row of
     `readcheck.tsv` (note `cmp A`, `cmp B`, `cmp C`, `cmp D`).
   - After each batch, `convert_en_oelsner.py` (its errors and lists) is compared with the
     baseline, and `misprints.py ocr/en-oelsner` is run.
   - A misprint the base had corrected silently is marked and listed when found, as for
     `en`.
3. **Read-through** (ocr/PLAN.md, "Read-through") over `texts/en-oelsner`: a trial of
   about 20 pages, then batches of 25 scans; decisions as in step 2 (note `read`).
   - A place in the English may be compared with `texts/en`, which is now checked. A
     difference is a revision unless the image shows a misreading or a misprint.
   - A place in the Italian may be compared with dante-corpus. The edition's readings
     differ from it, so the image decides.
4. **Close**:
   - The state here, DONE.md, and a SUMMARY.md.
   - texts/PLAN.md "Status", and the README of `ocr/en-oelsner` (the check in "Credits").
   - ocr/PLAN.md "State": all three texts done.
   - Commits, `ocr/en-oelsner` and `texts/en-oelsner` apart, when the user asks.

## Decisions for this text

- **The retyper and the reader** (the user, 2026-11-13): Claude (Opus 5.5) itself, as
  `grc` from retype 12 on: the retype written from the page images alone, without the
  base, each page read in strips at twice its size; the read-through read by Claude
  too. The user may switch to la-el-agy partway, after seeing how it goes; the model of
  each batch is recorded in DONE.md either way. The batches follow one another without a
  signal (no delegate).
- **GLM-OCR in the comparison** (the user, 2026-11-13): run over all pages by the user;
  the retype does not wait for it (it reads the image alone), the deciding of each batch
  does, so that every batch is compared once with all four readings.
- **The italics** are set aside by `cmpread.py`: only the words are compared (as the
  superscript markers of `en`), an italic misplaced in the base left as it is (Claude's
  recommendation; the user did not object, 2026-11-13).

## Settled readings

The edition's readings found in the steps go here, and are applied, not asked again.

- **Small capitals** (the first word after a drop capital, `THE` on `403`; a name in a
  table, `OBIZZO` on `249`): the base's case is kept, as `ocr/en-oelsner` set no rule for
  them; a difference of case alone is not corrected.
- **Maps and tables**: their names are read in the image one by one; the order of the lines,
  which the print does not set, is not compared; the names as printed, the abbreviations (`R. Piave`) and
  the capitals (`VERONA`) included (`025`).
