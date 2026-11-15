# Guide: checking an OCR transcription by the shortest path

General lessons from the checks of `ocr/la`, `ocr/en`, `ocr/grc` and `ocr/en-oelsner`
(their SUMMARY.md files), for a new project. The flow these checks followed in detail
is [PLAN.md](PLAN.md).

## Principles

- **Decide only the places where readings differ, in the image.** Comparing independent
  readings and judging each difference against the scan is faster and surer than having
  a person or a model read every page to proofread it.
- **A comparison with another edition is not a check of the transcription.** Where
  `en-oelsner` had been compared with dante-corpus and Carlyle's edition, the base had
  drifted towards their standard forms; only the image tells the edition's reading from
  a misreading.
- **One pass for all kinds of decision.** Italics, line breaks, misprints and words are
  decided together in the same pass. Separate passes per kind leave earlier decisions
  stale and read the same text again and again.

## Steps

### Before 0. Choosing the scan

In `en-oelsner` a missing leaf and an edition that had rewritten two pages of plates
were found only at the end; both are cheap to find before any work. Of every scan of
the book (Internet Archive lists several copies and printings), fetch the OCR the
library already provides (`_djvu.xml`, with its pages, and `_djvu.txt`) and check
([scripts/iascan.py](scripts/iascan.py)):

- **The edition**: the list of editions or reprints on the title verso. The year in the
  catalogue record may be wrong (a copy dated 1899 was the reprint of 1910).
- **Missing and repeated leaves**: the printed page number of each leaf (from the head
  or foot) minus the leaf index should stay constant; a change marks a missing,
  repeated or inserted leaf. Leaves whose text repeats another's are repeated scans.
- **Revisions between printings**: a word diff of two printings' OCR, keeping only the
  blocks of five words or more, leaves the rewritten passages above the OCR noise. A
  reprint not called a new edition can still be revised; plates and the index to them
  are worth comparing too.
- **The image**: the same printed page from each candidate side by side, one text page
  and one figure: show-through, contrast, margins cut, pages binarized.

Choose the latest complete printing with the cleanest images, and record the reasons,
the candidates and the offset in the directory's README. If the best scan still lacks a
leaf, the leaf is supplied from another copy of the same printing.

### 0. Setup: decided once, not changed later

- The transcription's conventions: line-end hyphens, running heads, marginal labels,
  italics, maps and tables.
- Misprints are kept as printed, marked `{{printed|fixed}}`, and listed in a table.
- The tools:
  - a page extractor, a line cropper for the images, and a word-by-word comparison script;
  - a script that applies fixes from a table, and one that checks the misprint marks
    against their table;
  - the converter, with its report kept as a baseline.
- One TSV of decisions (`page line form decision note`).
- Settled readings go into the PLAN ("Settled readings") and are not asked again.

### 1. Base OCR and word boxes

- OCR with a strong vision model; run Tesseract too, for its word boxes (to crop lines
  for checking).
- Take the scan's OCR from Internet Archive too (`iascan.py pages`), as a column beside
  the other readings that does not vote. It costs nothing, but in `en-oelsner` it read
  only 134 of the 355 word corrections of the check (Tesseract 168, GLM-OCR 228), 6 of
  them alone, and differed from the final text more than Tesseract; its use is a hint at
  a place already listed (numbers, accents). Count it again on the first batch of a new
  scan, whose OCR may be better or worse.
- **Convert at once, and run every mechanical check first:**
  - the counts of the structure (lines, verse numbers, the table of contents);
  - the layout: a note number at a line start after a non-blank line, a paragraph
    starting lowercase after a page boundary, and the like.
  - In `en-oelsner` these searches came at the end and found what the batches had
    missed; they belong at the start.

### 2. Compare: where most errors are found

- Align the base with the other readings (Tesseract, GLM-OCR, Internet Archive) word by
  word, and decide each difference in the image. In `en-purgatorio`, a base from a strong
  model checked this way had 21 errors in 449 pages (2 in the trial of 25, 19 in the
  rest).
- **No retype as a rule.** Retyping every page from the image alone was a transitional
  step, needed while the base was an existing OCR of doubtful quality (`ocr/la`, `ocr/en`,
  `ocr/grc`, `en-oelsner`, made or proofread by older models). Retype only in that case:
  then Claude itself, reading each page in strips at twice the size, erred least (0–3
  places in 25 pages), and in `en-oelsner` 401 of the 435 misreadings were found by
  comparing the base, the retype and Tesseract.
- Work in batches of 25 pages; after each, compare the converter's report with the
  baseline.
- Read small marks (accents, breathings) at eight to twelve times their size, beside a
  sure example of the same type.
- Read maps and tables name by name, not by line order.

### 3. Read-through for sense: once

- Read the converted text for sense; before the converter exists, read the pages in
  `ocr/` themselves (as in `en-purgatorio`). It finds:
  - misprints that every reading passed because all agreed with the print (one to five
    in 25 pages);
  - layout errors: notes run together, stray blank lines, spaces at brackets.
- Two passes: first read every page and only list the doubtful places
  (`PAGE:LINE text — guess`); then decide the list in the image, in batches (100 pages
  in `en-purgatorio`). Reading stays fast while nothing is cropped, and the list shows
  which doubts recur.
- Each place is decided as in "Decided in advance": a misreading is corrected in `ocr/`
  and recorded in the decision TSV; a misprint is marked `{{printed|fixed}}` and listed
  in the misprint table too; a reading as printed is kept with no record.
- Doubts that recur across the book (an Italian elision with no space after the
  apostrophe, a split elision before an enclitic, the spacing at a colon in citations)
  are not decided place by place: search every place at the end and decide them
  together, in the image.
- The converter's own faults (joins across pages and lines) also show in its output;
  fix the converter, not `ocr/`.

### 4. Close

- A SUMMARY.md: each step's method and counts, what was found, what was learnt.
- Commit once at the end, the transcription and the converted texts apart.

### 5. Figures

- Cut maps and plates from the scans by a script with fixed boxes, make the paper
  white, and save as JPEG; keep the captions as text. Nothing is placed in `texts/` by
  hand, so that a new conversion rebuilds everything.

## What can be left out

- **Delegating a proofreading of the base by reading it.** Delegates changed colons to
  semicolons, modernized spellings, and reported checks they had not made; their work
  has to be verified by a diff against a snapshot, which costs more than it saves.
- **Relying on a fourth reading (GLM-OCR and the like).** It normalized and repeated
  text, and its vote alone decided nothing. It is cheap to run, so it can be kept as a
  vote, but nothing is decided by it without the image.
- **Whole-page retypes**, when the base is from a strong model (step 2). By weaker
  models, never: their errors only add places to compare.
- **Waiting for approval between batches, and commits in the middle.**

## Decided in advance

- Batches of 25 pages, fixed after a trial of about 20.
- Three decisions only: **misread** (corrected in `ocr/`), **misprint** (kept as
  printed, marked and listed), **printed** (kept).
- A spelling that looks like the edition's own is searched in every place before it is
  decided (`ᾀεί` in `grc`), not decided from one place.
