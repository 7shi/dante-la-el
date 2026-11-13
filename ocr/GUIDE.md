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
- **Convert at once, and run every mechanical check first:**
  - the counts of the structure (lines, verse numbers, the table of contents);
  - the layout: a note number at a line start after a non-blank line, a paragraph
    starting lowercase after a page boundary, and the like.
  - In `en-oelsner` these searches came at the end and found what the batches had
    missed; they belong at the start.

### 2. Retype and compare: where most errors are found

- Retype every page from the image alone, without showing the base. Claude itself,
  reading each page in strips at twice the size, erred least (0–3 places in 25 pages).
- Align the base, the retype and Tesseract word by word, and decide each difference in
  the image. In `en-oelsner`, 401 of the 435 misreadings were found here.
- Work in batches of 25 pages; after each, compare the converter's report with the
  baseline.
- Read small marks (accents, breathings) at eight to twelve times their size, beside a
  sure example of the same type.
- Read maps and tables name by name, not by line order.

### 3. Read-through for sense: once

- Read the converted text for sense. It finds:
  - misprints that every reading passed because all agreed with the print (one to five
    in 25 pages);
  - layout errors: notes run together, stray blank lines, spaces at brackets.
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
- **A fourth reading (GLM-OCR and the like).** It normalized and repeated text, and its
  vote alone decided nothing; worth it only for a hard script.
- **Whole-page retypes by weaker models.** Their errors only add places to compare.
- **Waiting for approval between batches, and commits in the middle.**

## Decided in advance

- Batches of 25 pages, fixed after a trial of about 20.
- Three decisions only: **misread** (corrected in `ocr/`), **misprint** (kept as
  printed, marked and listed), **printed** (kept).
- A spelling that looks like the edition's own is searched in every place before it is
  decided (`ᾀεί` in `grc`), not decided from one place.
