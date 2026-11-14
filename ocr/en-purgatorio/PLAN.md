# Plan: transcribing and checking `ocr/en-purgatorio`

The transcription and the check of the Temple Classics *Purgatorio* (README.md): the Italian
edited by H. Oelsner, Thomas Okey's prose translation, Wicksteed's arguments, Oelsner's
notes. It follows [../GUIDE.md](../GUIDE.md), with the experience of
[../en-oelsner/](../en-oelsner/) (its PLAN.md, DONE.md and SUMMARY.md), which has the same
layout. `ocr/en-paradiso` follows the same plan afterwards, with the tools made here.

The work done is to be recorded in DONE.md, as the steps go.

**A new session starts here**: read "State". The rules of ocr/PLAN.md ("Decisions",
"Read-through") apply.

## State (2026-11-15)

The scan is chosen (README.md, "Choice of the scan"). The pages are rendered as `NNN.png`
(NNN the PDF page = the leaf of Internet Archive's OCR, 300 dpi) by a script of the user's,
outside the repository. `ia-ocr/` is written for all pages; Tesseract and GLM-OCR run by
the user with their Makefiles (`tesseract/`, `glm-ocr/`), over all pages. The trial (step
5) is done on `014`–`038` (DONE.md): no retype; its fixes are in `readcheck.tsv` and
`misprints.tsv`. Next: steps 1 and 2, then the base of the other pages (step 3).

## The text (to be filled in by step 1)

- **Pages**: 462 leaves; the printed page = leaf − 12 (README.md). The pages to
  transcribe and those left out (covers, library leaves, blank leaves) go into INDEX.md.
- **Kinds of page**, expected from `en-oelsner`: the front matter; the cantos on facing
  pages (the Italian with marginal labels and tercet numbers on the even pages, the
  English, one paragraph per tercet, on the odd pages; the argument across the first
  spread; the notes across the page bottoms and over whole pages); the plates, diagrams
  and family tables (the Index to Plates, Tables, etc.: pp. 12, 13, 34–35, 47, 59, 86–91,
  103, 241, 376–377); the end matter (the editorial and translator's notes, the index).
- **No second edition of the translation** to compare with, unlike Carlyle's own edition
  for the *Inferno*: the English is decided against the image alone.

## The readings to compare

| Reading | By | Where |
|---|---|---|
| The base (agy's Orchestrator mode: Gemini 4 Argon, with Gemini 4 Hydrogen workers) | la-el-agy, from a task file, on its own | `NNN.txt` |
| Tesseract (`-l eng+ita`), with its word boxes | the user (a Makefile as `en-oelsner`'s) | `tesseract/` |
| GLM-OCR | the user (a Makefile as `en-oelsner`'s) | `glm-ocr/` |
| Internet Archive's OCR | Claude (`iascan.py pages`) | `ia-ocr/` |

`cmpread.py -g glm-ocr -i ia-ocr`: GLM-OCR votes (class D), Internet Archive's OCR is a
column that does not vote (GUIDE.md, step 1).

## Steps

1. **The rendering and the structure.**
   - The page count against the OCR's leaves (the script warns), a few pages looked at.
   - README.md, "Layout": the offset, the kinds of page.
   - INDEX.md: each canto's argument, text and notes; the plates and tables; the end
     matter; the pages left out. Built from Internet Archive's OCR (`iascan.py heads`)
     and the printed index.
2. **Setup** (GUIDE.md, step 0).
   - The conventions of `en-oelsner` taken over: lines as printed, line-end hyphens, the
     running heads, page numbers, signature marks and tercet numbers kept; the marginal
     labels `**Label**` at the start of their line; italics `*…*`; curly quotes `“ ”`
     and `’` in the English, `'` for the Italian elision; misprints kept as printed,
     marked `{{printed|fixed}}`. Settled readings of `en-oelsner` that apply (small
     capitals, maps name by name) go into "Settled readings" below.
   - misprints.tsv and readcheck.tsv, with the columns of ocr/PLAN.md.
   - `texts/scripts/convert_en_oelsner.py` and `crop_en_oelsner_images.py` made to run
     on a volume's settings (verses per canto, each canto's first and last page, plates,
     images, end matter), writing `texts/en-purgatorio/`; the *Inferno*'s output checked
     byte for byte unchanged.
3. **The readings.**
   - The base: la-el-agy reads a task file and transcribes the pages of INDEX.md into
     `NNN.txt` by the conventions above, from the images alone. The rules stay basic: no
     git, Python as `uv run python`; it writes only `NNN.txt` and its report. The trial's
     25 pages (`014`–`038`) are done; the user switches its mode and signals.
   - Tesseract and GLM-OCR by the user; `ia-ocr/` by Claude.
4. **Mechanical checks first** (GUIDE.md, step 1): convert at once; the verse count and
   tercet numbers of each canto; the English paragraphs against the tercets of the facing
   page; the order of the note numbers; a paragraph starting lowercase after a page
   boundary. dante-corpus only to find a difference; the image decides.
5. **The trial: is a retype needed?** (done: no retype; DONE.md) On the first 25 pages of the cantos:
   - Claude retypes them from the images alone and decides every difference
     (`cmpread.py`), giving the checked text.
   - Against it, counted: the errors of the base that the OCRs alone would have found
     (where two or more of Tesseract, GLM-OCR and Internet Archive read the same other
     form), and those they would have missed; how often Internet Archive's column helped.
   - Few misses: the other pages are checked without a retype. Many: the retype goes on.
     The user decides on the counts; recorded under "Decisions".
6. **The batches** (GUIDE.md, step 2): 25 pages each, compared, every place decided in
   the image, readcheck.tsv and misprints.tsv filled; the converter's report against its
   baseline after each. No waiting for approval and no commits between batches.
7. **Read-through** for sense, once (GUIDE.md, step 3).
8. **Figures** (GUIDE.md, step 5): the boxes of the plates and diagrams, the images into
   `texts/en-purgatorio/images/`.
9. **Close** (GUIDE.md, step 4): SUMMARY.md; README.md ("Credits"), INDEX.md, the root
   README and texts/PLAN.md; the commits at the end, `ocr/en-purgatorio` and
   `texts/en-purgatorio` apart.

Then `ocr/en-paradiso` by the same steps; step 2 mostly reused.

## Decisions for this text

- **The scan** (the user, 2026-11-15): purgatorioofdant00dant_0, the Fourth Edition
  (November 1904), by GUIDE.md's "Choosing the scan" (README.md).
- **The base from a strong model at once** (the user, 2026-11-15): not an older model
  proofread afterwards, as `en-oelsner` was. The trial was made in agy's Orchestrator mode
  (Gemini 4 Argon directing Gemini 4 Hydrogen workers; the workers could not name their
  model).
- **No retype** (the user, 2026-11-15, on the trial's counts, DONE.md): 2 errors of the
  base in 25 pages, one found by the OCRs (`fora`), one a missing paragraph break that only
  a reading found; no word error that all the OCRs passed. The pages are checked by the
  comparison of the base with Tesseract, GLM-OCR and Internet Archive (`cmpread.py` with
  GLM-OCR as the second reading), every place decided in the image; the paragraph breaks
  and the misprints all readings pass are left to the mechanical checks (step 4) and the
  read-through (step 7).
- **All the OCRs as readings** (the user, 2026-11-15): Tesseract and GLM-OCR cost little
  and are kept; Internet Archive's OCR added as a column, not a vote.

## Settled readings

The edition's readings found in the steps go here, and are applied, not asked again.
