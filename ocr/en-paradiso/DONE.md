# Done: checking `ocr/en-paradiso`

The record of the check ([PLAN.md](PLAN.md)), step by step.

## Step 0: setup (2026-11-15)

- **The conventions** of `en-purgatorio` taken over whole (README.md, "Transcription");
  its settled readings to be checked on the trial.
- **misprints.tsv and readcheck.tsv**: the headers, with the columns of `en-purgatorio`.
- **The converter and the crop script**: `PARADISO` settings in
  `texts/scripts/convert_en_oelsner.py` (the verses per canto, the pages of each canto,
  the plates, the images and their names, the front and end matter, from INDEX.md) and
  an empty box list in `crop_en_oelsner_images.py`. The decisions by hand (the first line
  of each figure among the notes, the hyphens, the note paragraphs at page tops) wait
  for the base (step 2), the boxes for step 6. The *Inferno*'s and the *Purgatorio*'s
  output checked unchanged: the Markdown, the images, and the *Inferno*'s report byte for
  byte.

## Step 1: the readings and the structure (begun 2026-11-15)

- **Internet Archive's OCR**: `iascan.py pages`, all 436 leaves into `ia-ocr/` (the
  file = the leaf).
- **INDEX.md** and README.md "Layout": from `iascan.py heads` and the printed Index to
  Maps, Diagrams and Tables (p. 419). The first page of each canto from the running heads
  (all 33 found); the leaf where the notes begin from the first note lines in `ia-ocr/`,
  read in the images where the OCR had missed them (Cantos II, XV, XXXI); the figures,
  the front and end matter and the pages left out read in contact sheets of the images.
  Five figures are printed in another canto's pages than the one they illustrate (the
  caption names it). The first lines of the cantos are to be added from the base.
- **GLM-OCR**: the user, with `glm-ocr/Makefile`, now through `ocr/scripts/glmocr.py`.
- **The base** of the trial's pages (`012`–`036`): la-el-agy from the task file, after
  the *Purgatorio*'s. Its report: all 25 pages read by the orchestrator and written by
  the executor in a plan-execute mode (no workers), none corrected, none empty, 17
  uncertain places (worn tercet numbers and page numbers, blotted letters); each was
  right.
- **The base of the other pages**: la-el-agy in two runs, `005`–`227` (the front matter
  and Cantos I–XVII, 196 pages) and `228`–`430` (Cantos XVIII–XXXIII and the end matter,
  203 pages), from task files with the settled readings, the tables printed sideways
  (read turned upright, one person or couple per line) and the scheme on `423` (one box
  per line). Subagents through `invoke_subagent` on the same model (Gemini 4 Hydrogen);
  in the first run the first batch (`005`–`041`) ran before agy switched to that call.
  No page empty; 105 and 103 uncertain places reported, left to steps 2 and 4. agy also
  evened the spacing before `; : ! ?` and round `=` across 34 pages of the first run,
  as the settled readings write them.

## Step 3: the trial on `012`–`036` (2026-11-15)

The first 25 pages of the cantos (Cantos I–II and the first page of III, pp. 2–26, with
the diagram of p. 12), to decide whether the base needs a retype.

- **The comparison**: `cmpread.py` with GLM-OCR as the second reading (`-i ia-ocr`,
  `--verse-numbers`): 84 places (A 16, B 58, C 10), almost all the marginal labels and
  running heads placed elsewhere, the accents GLM-OCR dropped (`sì`, `lì`) and the words
  hyphenated at line ends; GLM-OCR also wrote a paragraph twice on `034`. The places that
  might differ in substance (`020` `lì`, the diagram's `SUN` on `022`, the closing quote
  on `019`, the run on `034`) were decided in the image: the base was right.
- **The read**: all 25 pages line by line against their images (each page in two
  halves; the doubtful marks in crops).
- **Found**: 4 errors of the base in 25 pages, none of a word.
  - `020` 26: the three-dot mark before the general note written `*.*`; `∵`, as
    `en-purgatorio` writes it (449).
  - `020` 38, `023` 33, `035` 22: `=` printed close to its words (`Apollo=the Sun=God`)
    written with spaces.
  - And 2 misprints, kept as printed by the base and marked: `022` 5 the note number
    `37-39` without its period; `026` 20 `unita` (Canto II 36) ending the tercet
    without a stop.
- **Decided** (the user): no retype. The marks found (`∵`, `=` close) go into PLAN.md,
  "Settled readings", and into the task file for the other pages.

## Step 2: convert at once; the mechanical checks (2026-11-15)

`convert_en_oelsner.py paradiso` on the whole base, into `texts/en-paradiso/`.

- **The converter made ready for the volume**: the page numbers (printed page = leaf −
  10, the epigraph `011` p. [1]; `PAGE_OFFSET` and `EPIGRAPH` per volume, 12 and 13 for
  the other two) and the running heads `PARADISO`, `DANTE’S PARADISE` and
  `EDITORIAL NOTE` with a page number (the title `EDITORIAL NOTE` of the *Purgatorio*,
  without one, stays a title). Before this the heads were read as verse and the verse
  counts went wrong on every page.
- **The figures**: those below the notes from their first line (`FIGURE_FROM`: `069`,
  `098`, `099`, `110`, `111`, `151`, `406`, `407`); the diagram on `022`, printed between
  two notes, shown after the note before it with its labels (`FIGURE_BETWEEN`, new).
- **The verse count** of each canto and **the tercet numbers**: all 33 as in the
  standard text, no error.
- **The English paragraphs against the tercets**: 15 English pages whose notes start
  without a verse number, all notes continued from the Italian page.
- **The note paragraphs at a page top** after a finished sentence: `035` continued
  (flush left), `057` new (indented), in the image.
- **Line-end hyphens**: 85 the word list could not decide, read through; 10 decided by
  hand (`HYPHEN_FIXED`: `establishment`, `signature`, `endowment`, `interchange` joined;
  `new-create`, `diverse-natured`, `things-to-see`, `a-moving`, `three-stringed`,
  `tooth-grips` kept). `Ghibil-line` (`070`) and `Com-machio` (`277`) are printed so;
  left to the read-through.
- **The end matter**: the scheme of the heavens on `423` kept line by line
  (`LINES_FROM`, new); the index on `429`, printed without space between its entries,
  one paragraph per entry (`INDEX_ENTRIES`, new); the footnote on `420` linked
  (`FOOTNOTES`; the converter drops the `¹` the base writes before the note).
- **Fixed in the base** (readcheck.tsv): `250` the page number `240`, printed sideways at
  the left edge, written `§` at the foot; `331` the signature mark `X` written `x` (the
  signatures run U 315, X 331, Y 347).
- The *Inferno*'s and the *Purgatorio*'s output unchanged.
