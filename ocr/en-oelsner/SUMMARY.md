# Summary: how `ocr/en-oelsner` was checked

A short account of the check of `ocr/en-oelsner`, the Temple Classics Inferno (1903): the
Italian edited by H. Oelsner, Carlyle's prose translation revised by him, and his notes,
by the flow of [ocr/PLAN.md](../PLAN.md) (2026-11-13 – 2026-11-14). The plan and the
settled readings are in [PLAN.md](PLAN.md), every batch and every decision in
[DONE.md](DONE.md), the transcription's conventions in [README.md](README.md).

## 1. The starting point

`ocr/en-oelsner` was Gemini 2.5 Flash's OCR proofread against the images by GPT-6 Luna,
then a final check (README.md, "Credits"), and normalized for the conversion (texts/PLAN.md,
"Conversion notes"). The conversion had compared the Italian with dante-corpus, the
English with `texts/en` (Carlyle's own edition), the English paragraphs with the tercets,
and the verse count of every canto. Nothing had read the notes, the arguments, the
labels, the maps and tables, or the end matter; and a misreading the comparisons passed as
an Oelsner variant could remain.

## 2. The steps

| Step | Method | Decided |
|---|---|---|
| 0. Setup | the tables, `convert_en_oelsner.py` taught the misprint marks, Tesseract's word boxes (`-l eng+ita`), GLM-OCR over all pages (run by the user), `cmpread.py` with `--verse-numbers` and `-g` (GLM-OCR as a fourth reading, class D where both OCRs agree against base and retype), a retype template | the baseline of `convert_en_oelsner.py` kept |
| 1–2. Retype and compare | every page retyped from the image alone by Claude (Opus 5.5), in three strips at twice the size: a trial of 6 pages, then 16 batches of 25; `cmpread.py` aligns the base, the retype, Tesseract and GLM-OCR word by word; every difference read in the image; the maps and tables read name by name | 401 misread, 28 misprints, 120 printed |
| 3. Read-through | the whole of `texts/en-oelsner` read for sense by Claude (Opus 5.5): a trial of 20 pages, then 15 batches of 25 scans (the last of 34, the end matter included); a search for notes run together closed it | 34 misread, 36 misprints, 47 printed |
| 5. Map images | the seven maps, diagrams and plates cut from the scans into `texts/en-oelsner/images/` (`crop_en_oelsner_images.py`) and shown where they are printed, their text kept | — |

Each place was decided in the image as **misread** (corrected in `ocr/en-oelsner`),
**misprint** (kept as printed, marked `{{printed|fixed}}` and listed) or **printed**
(kept); every decision is a row of [readcheck.tsv](readcheck.tsv) (note `cmp A`–`D` for
step 2, `read` for step 3). The leaf with pp. 385–386 is missing from the scan and was not
checked; the book prints no corrigenda.

## 3. What was found

- **Misreadings of the base**: 435 in all. The verse and the English, compared before,
  held few, but some the comparisons had passed as variants: the base had taken the
  standard form where the edition prints another (`sembiava` made `sembrava`, `proposto`
  made `proposito`, `ammoglia` given an accent). Most were in what nothing had compared:
  the notes (words, references, italics), the running heads, and above all the layout:
  - **The maps, the diagram and the tables** had been normalized: `R.` expanded to
    `River`, the capitals lowered, names joined or added or left out (`025`, `037`); they
    were rewritten name by name as printed.
  - **Notes run together**: where the base had no blank line between notes, the
    converter joined them into one paragraph (19 rows, some covering a whole page of
    notes); each set apart as printed.
- **Misprints**: 64 rows in [misprints.tsv](misprints.tsv), all marked (`misprints.py`: 64
  rows, 64 marks, no problems): a period missing after a note's verse numbers or at its
  end, quotation marks unopened or of the wrong kind, a letter in the Italian (`risposa`,
  `tuttie`, `un fossata`), a name in the notes (`Camomica`, `Sali` for Salò, `the Marte`),
  a reference (`Psalms cxxix.`, `John xii.`). The base had corrected many silently; the
  retype and the read-through found them.
- **The edition's readings**, not misprints: the small capitals after a drop capital kept
  in the base's case; the names of maps and tables as printed, abbreviations and capitals
  included (PLAN.md, "Settled readings"); the editor's spellings in the verse (`perché`
  beside `perchè`, `letanie`, `mai comforti`).
- **`convert_en_oelsner.py`**: its report kept the baseline after every batch. Four
  layout faults of the converter were found and fixed: number ranges divided at a line
  end joined with a space; a note continued after a dash on the next page joined with a
  space; a word hyphenated after a bracket (`[down]-` / `wards`); and four pages wrongly
  listed as beginning a new note (`211`, `225`, `237`, `332`), where the note continued
  from the page before was left cut (`con-` / `spiracy`).

## 4. Learnt for the other texts

- **A comparison with another edition is not a check of the transcription**: where the
  text was compared with dante-corpus and Carlyle, the base had drifted towards them; only
  the image tells the edition's reading from a misreading.
- **What nothing has compared holds the errors**: the notes, the maps, the tables and the
  end matter. A map or a table is read name by name, not by line order.
- **The retype by Claude itself** erred little (0–3 places in 25 pages, mostly a mark of
  punctuation or a misprint corrected); GLM-OCR as a fourth reading helped in class D, but
  its vote alone decided nothing.
- **The layout is part of the reading**: most misreadings the read-through found were of
  the layout (notes run together, blank lines, spacing at brackets), not of words. A
  search over all pages for a note number at a line start after a non-blank line found
  the rest at the close.
- **The converter is checked by its output**: a reading of the converted text found
  faults the conversion's own checks could not, as they were in how pages and lines are
  joined.
