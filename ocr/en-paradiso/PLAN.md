# Plan: transcribing and checking `ocr/en-paradiso`

The transcription and the check of the Temple Classics *Paradiso* (README.md): the Italian
edited by H. Oelsner, Philip H. Wicksteed's prose translation and arguments, the notes by
both. It follows the standard flow of [../GUIDE.md](../GUIDE.md) ("Steps"), as
[../en-purgatorio/](../en-purgatorio/) ran it (its PLAN.md, DONE.md and SUMMARY.md),
with the tools made there; the volumes share their layout.

The work done is to be recorded in DONE.md, as the steps go.

**A new session starts here**: read "State". The rules of ocr/PLAN.md ("Decisions",
"Read-through") apply.

## State (2026-11-15)

The scan is chosen (README.md, "Choice of the scan"): paradisoofdante00dant, the reprint
of November 1910. The pages are rendered as `NNN.png` (436, NNN the leaf of Internet
Archive's OCR, 300 dpi; by the script that became `ocr/scripts/iapdf.py`). Tesseract has run over all pages
(`tesseract/`); GLM-OCR has begun (`glm-ocr/`, a few pages, not committed). Not done yet:
`ia-ocr/`, the base, and every step below. Next: step 0 (the converter's settings) and
step 1 (the task file for the base, `ia-ocr/`, INDEX.md).

## The text

- **Pages**: 436 leaves; the printed page = leaf − 10, constant (README.md). The pages
  to transcribe and those left out go into INDEX.md.
- **Kinds of page**, expected from the other two volumes: the front matter; the cantos on
  facing pages (the Italian with marginal labels and tercet numbers on the even pages,
  the English, one paragraph per tercet, on the odd pages; the argument across the first
  spread; the notes across the page bottoms and over whole pages); the maps, diagrams and
  tables; the end matter (the editorial note, Wicksteed's papers, the Index to Maps,
  Diagrams and Tables).
- **The figures**, by the printed index (as Internet Archive's OCR reads it; the pages to
  be read in the image in step 1): diagrams of the "four circles and three crosses"
  (I 39) and of the three mirrors (II); maps of Provence, Naples and Sicily, Hungary and
  Rascia, the district about Romano, the Mediterranean (Marseilles), Assisi, the district
  about Florence, Cacciaguida's Florence, and the world east and west of Jerusalem (XXII,
  XXVII); a table of Dante's descent from Cacciaguida (XV) and tables of kings (XIX,
  pp. 240–243). The *Purgatorio*'s family tables refer to these.
- **Verses per canto** as in the standard text: 142, 148, 130, 142, 139, 142, 148, 148,
  142, 148, 139, 145, 142, 139, 148, 154, 142, 136, 148, 148, 142, 154, 139, 154, 139,
  142, 148, 139, 145, 148, 142, 151, 145.
- **No second edition of the translation** to compare with: the English is decided
  against the image alone. The 1910 reprint revised some notes against earlier printings
  (README.md); the earlier printings are not compared.

## The readings to compare

| Reading | By | Where |
|---|---|---|
| The base (a strong model: agy's Orchestrator mode, as for the *Purgatorio*) | la-el-agy, from a task file, on its own | `NNN.txt` |
| Tesseract (`-l eng+ita`), with its word boxes | the user (Makefile) | `tesseract/` |
| GLM-OCR | the user (Makefile) | `glm-ocr/` |
| Internet Archive's OCR | Claude (`iascan.py pages`) | `ia-ocr/` |

`cmpread.py -g glm-ocr -i ia-ocr`: GLM-OCR votes (class D), Internet Archive's OCR is a
column that does not vote.

## Steps

The steps of GUIDE.md, in its order; the *Purgatorio*'s step numbers are not kept.

0. **Setup** (GUIDE.md, "Setup").
   - The conventions of `en-purgatorio` taken over whole (its README.md,
     "Transcription"), and its settled readings where the edition prints the same
     (`N: N` in citations, the dotless `ı` read as `ì`), checked on the trial.
   - misprints.tsv and readcheck.tsv, with the columns of ocr/PLAN.md.
   - `convert_en_oelsner.py` and `crop_en_oelsner_images.py`: a third volume's settings
     (`PARADISO`, writing `texts/en-paradiso/`), filled in as INDEX.md is made; the
     outputs of the *Inferno* and the *Purgatorio* checked byte for byte unchanged.
1. **The readings and the structure** (GUIDE.md, "The readings and the structure").
   - The base: a task file for la-el-agy, as the *Purgatorio*'s (one printed line per
     line, spell as printed, labels, italics, figures; only the page images; no git, no
     subagents of its own beyond the mode's workers; Python as `uv run python`; it writes
     only `NNN.txt` and its report). First the trial's pages, then the rest in two or
     three runs; the user switches agy's mode and signals before each.
   - GLM-OCR finished by the user; `ia-ocr/` by Claude (`iascan.py pages`).
   - INDEX.md and README.md "Layout": from `iascan.py heads` and the printed index; the
     figures' pages read in the image.
2. **Convert at once; the mechanical checks** (GUIDE.md, "Convert at once"): the verse
   count and the printed tercet numbers of each canto; the English paragraphs against the
   tercets of the facing page; the note paragraphs at page tops (continued or new, in the
   image); the line-end hyphens the word list cannot decide; the end matter. Each place
   decided in the image; the converter's report kept as the baseline.
3. **The trial** (GUIDE.md, "The trial"): the first 25 pages of the cantos read line by
   line against the images and compared with the OCRs; the errors of the base counted.
   The user decides whether a retype is needed (recorded under "Decisions").
4. **The comparison** of all the pages (GUIDE.md, "Compare"): `cmpread.py` with GLM-OCR
   as the second reading, then Tesseract's lines to filter the noise; every place left
   decided in the image.
5. **Read-through** for sense, once (GUIDE.md, "Read-through for sense"), on the
   converted text: the doubtful places listed first, then decided in the image 100 pages
   at a time; the recurring doubts searched over the book at the end.
6. **Figures** (GUIDE.md, "Figures"): the boxes of the maps and diagrams cut from the
   scan, into `texts/en-paradiso/images/`; the tables stay text.
7. **Close** (GUIDE.md, "Close"): SUMMARY.md; README.md ("Credits"), INDEX.md, the root
   README, ocr/README.md, texts/PLAN.md and the READMEs of `texts/`; the commits at the
   end, `ocr/en-paradiso` and `texts/en-paradiso` apart.

No waiting for approval and no commits between the steps' batches.

## Decisions for this text

- **The scan** (the user, 2026-11-15): paradisoofdante00dant, the reprint of November
  1910, by GUIDE.md's "Choosing the scan" (README.md): the latest complete printing with
  the cleanest images; the 1904 scan lacks pp. 406–407.

## Settled readings

The edition's readings found in the steps go here, and are applied, not asked again.
