# Summary: how `ocr/en-purgatorio` was made and checked

A short account of the transcription and the check of `ocr/en-purgatorio`, the Temple
Classics *Purgatorio* (Fourth Edition, 1904): the Italian and the notes edited by H.
Oelsner, Thomas Okey's prose translation, Wicksteed's arguments (2026-11-15). It follows
[../GUIDE.md](../GUIDE.md), with the experience of [../en-oelsner/](../en-oelsner/). The
plan and the settled readings are in [PLAN.md](PLAN.md), every step in [DONE.md](DONE.md),
the layout and the conventions in [README.md](README.md), the structure in
[INDEX.md](INDEX.md).

## 1. The starting point

The scan was chosen first, from the OCR Internet Archive provides for each copy
(README.md, "Choice of the scan"): the Fourth Edition, complete and clean. Unlike
`en-oelsner`, the base was made at once by a strong model, agy's Orchestrator mode
(Gemini 4 Argon directing Gemini 4 Hydrogen workers), from the images alone, by the
conventions of `en-oelsner`; Tesseract, GLM-OCR and Internet Archive's own OCR were the
readings to compare with it.

## 2. The steps

| Step | Method | Found |
|---|---|---|
| 5. Trial (`014`–`038`) | 5 pages retyped by Claude from the images, the other 20 read line by line against them; the base compared with the OCRs (`cmpread.py`) | 2 errors of the base, 1 misprint; no retype (the user) |
| 6. Comparison (the other 424 pages) | `cmpread.py`, GLM-OCR as the second reading, Internet Archive as a column; a second run with Tesseract's lines filtered the noise; about 60 places decided in the image | 19 errors of the base (16 misread, 3 misprints corrected silently) |
| 7. Read-through (all 449 pages, in `ocr/`) | two passes: the doubtful places listed (168), then decided in the image 100 pages at a time; the recurring doubts searched over the book and decided together | 70 misread, 90 misprints, 34 kept as printed |
| 1–2. Structure, converter | INDEX.md; `convert_en_oelsner.py` and `crop_en_oelsner_images.py` made to run on a volume's settings, the *Inferno*'s output unchanged byte for byte | — |
| 4. Mechanical checks | on the converted text: the verse count, the tercet numbers, the English paragraphs against the tercets, the note paragraphs at page tops, the line-end hyphens, the end matter | 7 misread |
| 8. Figures | nine images cut from the scan by fixed boxes | — |

Each place was decided in the image as **misread** (corrected), **misprint** (kept as
printed, marked `{{printed|fixed}}`, listed in [misprints.tsv](misprints.tsv)) or
**printed** (kept); every decision is a row of [readcheck.tsv](readcheck.tsv): 95 misread,
94 misprints, 34 printed (`misprints.py`: 94 rows, 94 marks, no problems).

## 3. What was found

- **The base was good**: 95 misreadings in 449 pages, and few of words. The comparison
  found the words (`fora` for `fuora`, spellings made modern: `condicion`, `poter`,
  `esempio`, `behooves`; a lost line and a lost note). The read-through found what all
  the readings shared or none compared: accents on the dotless `ı` (12), a stray or
  missing paragraph break, and above all the layout at the page foot (the blank line before
  the page number, missing on 43 pages). The mechanical checks found a stray paragraph
  break no reading compares (`213`), reversed italics (`451`) and the signatures.
- **Misprints**: 94, almost all from the read-through: tercet numbers, marginal labels,
  letters in the Italian and the English, missing stops and quotes in the notes, the
  editor's slips whose right form is sure. The base had corrected three silently.
- **The edition's readings**, kept (PLAN.md, "Settled readings"): Italian elisions set
  close (13) and split before an enclitic (18); the colon in citations printed spaced,
  written `N: N`. The places doubted whose right form is not sure are rows `printed`,
  marked `undecided`.

## 4. Learnt for the other texts

- **A strong base and a comparison suffice**: no retype was needed; the comparison with
  three OCRs found the word errors, the read-through the rest.
- **Run the mechanical checks as soon as a converter exists**: here the converter came
  after the read-through, and the checks still found a paragraph break and the end
  matter's faults. For `en-paradiso` the converter is ready: convert first.
- **A converter made general by settings**, checked against the old output byte for byte,
  costs little; what is new for a volume is a setting, not a branch in the code.
- **The figures** of a clean scan are cut from it directly; the ink of the page finds
  the boxes, a contact sheet checks them.
