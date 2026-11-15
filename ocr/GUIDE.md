# Guide: checking an OCR transcription by the shortest path

General lessons from the checks of `ocr/la`, `ocr/en`, `ocr/grc`, `ocr/en-oelsner` and
`ocr/en-purgatorio` (their SUMMARY.md files), for a new project. The flow the older checks
followed in detail is [PLAN.md](PLAN.md); the steps below are the standard flow, as
`en-purgatorio` ran it from the scan to the converted text in one day
([en-purgatorio/PLAN.md](en-purgatorio/PLAN.md), [DONE.md](en-purgatorio/DONE.md)).

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

The standard flow, in order (each step below):

| Step | What | Done by |
|---|---|---|
| Before 0 | Choose the scan; render its pages | Claude (`iascan.py`, `iapdf.py`) |
| 0 | Setup: conventions, tables, tools, the converter's settings | Claude |
| 1 | The readings: the base, Tesseract, GLM-OCR, Internet Archive; the structure (INDEX.md) | a strong model (base), the user (OCRs), Claude |
| 2 | Convert at once; the mechanical checks | Claude |
| 3 | The trial on 25 pages: is a retype needed? | Claude counts, the user decides |
| 4 | The comparison of all pages | Claude |
| 5 | The read-through, in two passes | Claude |
| 6 | The figures | Claude |
| 7 | Close: SUMMARY.md, the READMEs, the commits | Claude |

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

Render the chosen scan's PDF as `NNN.png`, NNN the PDF page = the leaf of the OCR
([scripts/iapdf.py](scripts/iapdf.py), 300 dpi); it checks the page count against the
OCR's leaves.

### 0. Setup: decided once, not changed later

- The transcription's conventions: line-end hyphens, running heads, marginal labels,
  italics, maps and tables. For a volume of a series already done, take them over whole.
- Misprints are kept as printed, marked `{{printed|fixed}}`, and listed in a table.
- The tools:
  - a page extractor, a line cropper for the images, and a word-by-word comparison script;
  - a script that applies fixes from a table, and one that checks the misprint marks
    against their table;
  - the converter, with its report kept as a baseline. For another volume of a series,
    make the converter run on a volume's settings (pages, counts, plates, end matter)
    and check that the old volume's output stays the same byte for byte; what is new is
    a setting, not a branch in the code.
- One TSV of decisions (`page line form decision note`).
- Settled readings go into the PLAN ("Settled readings") and are not asked again.

### 1. The readings and the structure

- **The base** from a strong vision model at once, from the images alone: a task file
  with the conventions in a few basic rules (one printed line per line, spell as
  printed, the labels, italics and figures as agreed; read only the page images; no git;
  write only the page files and a report listing the uncertain places). In
  `en-purgatorio` agy's Orchestrator mode (Gemini 4 Argon directing workers) did 449
  pages in three runs.
- **Tesseract** (with its word boxes, to crop lines for checking) and **GLM-OCR**, by
  their Makefiles; both are cheap and kept as readings.
- **Internet Archive's OCR** (`iascan.py pages`), as a column beside the other readings
  that does not vote. It costs nothing, but in `en-oelsner` it read only 134 of the 355
  word corrections of the check (Tesseract 168, GLM-OCR 228), 6 of them alone, and
  differed from the final text more than Tesseract; its use is a hint at a place already
  listed (numbers, accents).
- **The structure** (INDEX.md, README "Layout"): from the OCR's page heads
  (`iascan.py heads`) and the printed contents or index of plates.

### 2. Convert at once, and run every mechanical check first

- The counts of the structure: lines and verse numbers (the printed numbers against the
  count), the table of contents.
- The layout: a translation's paragraphs against the tercets of the facing page, a note
  number at a line start after a non-blank line, a note or paragraph at a page top after
  a finished sentence (continued or new: flush left or indented, in the image), the
  line-end hyphens the word list cannot decide.
- In `en-oelsner` these searches came at the end and found what the batches had missed;
  in `en-purgatorio` the converter came after the read-through and still found a stray
  paragraph break and the end matter's faults. They belong at the start.

### 3. The trial: is a retype needed?

- On the first 25 pages of the text: read the base line by line against the image (or
  retype it, if the output is not filtered), and compare it with the other readings.
- Count the errors of the base, those the OCRs would have found and those they would
  have missed. Few misses: no retype, the rest is checked by the comparison. The user
  decides on the counts. In `en-purgatorio`: 2 errors in 25 pages, no retype.
- **No retype as a rule** for a base from a strong model. Retyping every page was needed
  only while the base was an existing OCR of doubtful quality (`ocr/la`, `ocr/en`,
  `ocr/grc`, `en-oelsner`, made or proofread by older models); then Claude itself,
  reading each page in strips at twice the size, erred least (0–3 places in 25 pages),
  and in `en-oelsner` 401 of the 435 misreadings were found by comparing the base, the
  retype and Tesseract.

### 4. Compare: where most errors are found

- Align the base with the other readings (Tesseract, GLM-OCR, Internet Archive) word by
  word (`cmpread.py`), and decide each difference in the image. With a strong base, all
  the pages at once: most places are noise (labels placed elsewhere, accents the OCRs
  drop); a second run with Tesseract's lines as the second reading leaves the places
  where two OCRs agree against the base. In `en-purgatorio`: 1429 places, about 60 left
  to decide, 19 errors of the base in 424 pages.
- With a weak base, in batches of 25 pages; after each, compare the converter's report
  with the baseline.
- Read small marks (accents, breathings) at eight to twelve times their size, beside a
  sure example of the same type.
- Read maps and tables name by name, not by line order.

### 5. Read-through for sense: once

- Read the converted text for sense (or, before the converter exists, the pages in
  `ocr/`). It finds:
  - misprints that every reading passed because all agreed with the print (one to five
    in 25 pages; 90 in the 449 pages of `en-purgatorio`);
  - what no reading compares: accents a type prints faintly, blank lines (the one before
    the page number at the foot), notes run together, spaces at brackets.
- Two passes: first read every page and only list the doubtful places
  (`PAGE:LINE text — guess`); then decide the list in the image, in batches (100 pages
  in `en-purgatorio`). Reading stays fast while nothing is cropped, and the list shows
  which doubts recur.
- Each place is decided as in "Decided in advance": a misreading is corrected in `ocr/`
  and recorded in the decision TSV; a misprint is marked `{{printed|fixed}}` and listed
  in the misprint table too; a reading kept as printed is a row `printed` with the doubt
  in its note (`undecided` where the right form is not sure).
- What is clearly wrong in the print is a misprint, numbers and stops included; a doubt
  whose right form is not sure stays as printed.
- Doubts that recur across the book (an Italian elision with no space after the
  apostrophe, a split elision before an enclitic, the spacing at a colon in citations)
  are not decided place by place: search every place at the end and decide them
  together, in the image; the decision goes into "Settled readings".
- The converter's own faults (joins across pages and lines) also show in its output;
  fix the converter, not `ocr/`.

### 6. Figures

- Cut maps and plates from the scans by a script with fixed boxes, make the paper
  white, and save as JPEG; keep the captions and labels as text. The boxes can be found
  from the ink of each page and checked in a contact sheet. Nothing is placed in `texts/`
  by hand, so that a new conversion rebuilds everything.

### 7. Close

- A SUMMARY.md: each step's method and counts, what was found, what was learnt; INDEX.md,
  the README's "Credits", the root README, texts/PLAN.md.
- Commit once at the end, the transcription and the converted texts apart.

## What can be left out

- **Delegating a proofreading of the base by reading it.** Delegates changed colons to
  semicolons, modernized spellings, and reported checks they had not made; their work
  has to be verified by a diff against a snapshot, which costs more than it saves.
- **Relying on a fourth reading (GLM-OCR and the like).** It normalized and repeated
  text, and its vote alone decided nothing. It is cheap to run, so it can be kept as a
  vote, but nothing is decided by it without the image.
- **Whole-page retypes**, when the base is from a strong model (step 3). By weaker
  models, never: their errors only add places to compare.
- **Waiting for approval between batches, and commits in the middle.**

## Decided in advance

- A trial of 25 pages; then the comparison of all pages at once with a strong base, or
  batches of 25 with a weak one; the read-through's decisions in batches of 100.
- Three decisions only: **misread** (corrected in `ocr/`), **misprint** (kept as
  printed, marked and listed), **printed** (kept).
- A spelling that looks like the edition's own is searched in every place before it is
  decided (`ᾀεί` in `grc`), not decided from one place.
