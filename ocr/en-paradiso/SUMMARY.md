# Summary: how `ocr/en-paradiso` was made and checked

A short account of the transcription and the check of `ocr/en-paradiso`, the Temple
Classics *Paradiso* (the reprint of November 1910): the Italian edited by H. Oelsner,
Philip H. Wicksteed's prose translation and arguments, the notes by both (2026-11-15). It
follows the standard flow of [../GUIDE.md](../GUIDE.md), as
[../en-purgatorio/](../en-purgatorio/) ran it, with the tools made there. The plan and the
settled readings are in [PLAN.md](PLAN.md), every step in [DONE.md](DONE.md), the layout
and the conventions in [README.md](README.md), the structure in [INDEX.md](INDEX.md).

## 1. The starting point

The scan was chosen first, from the OCR Internet Archive provides for each copy
(README.md, "Choice of the scan"): the reprint of November 1910, complete and the
cleanest, with notes revised against the earlier printings. The base was made by a
strong model, agy's Orchestrator mode, from the images alone, by the conventions of
`en-purgatorio`, first the trial's 25 pages, then the rest in two runs; Tesseract,
GLM-OCR and Internet Archive's own OCR were the readings to compare with it. The
converter and the crop script of the other two volumes were given the volume's settings
before the base existed, so the text was converted as soon as it was there.

## 2. The steps

| Step | Method | Found |
|---|---|---|
| 0–1. Setup, readings, structure | the conventions and tables of `en-purgatorio`; INDEX.md from Internet Archive's running heads and the printed index; the base by agy | — |
| 2. Convert at once; mechanical checks | `convert_en_oelsner.py paradiso`: verse counts and tercet numbers (all right), English paragraphs against the tercets, notes at page tops, line-end hyphens, the end matter | 2 misread |
| 3. Trial (`012`–`036`) | 25 pages read line by line against the images, the base compared with GLM-OCR | 4 misread (marks and spacing), 2 misprints; no retype (the user) |
| 4. Comparison (all 424 pages) | `cmpread.py`, GLM-OCR as the second reading, Internet Archive as a column; a second run with Tesseract's lines; the places where two OCRs agree against the base (129), and agy's 208 uncertain places, decided in the image | 16 misread, 15 misprints |
| 5. Read-through (all pages, in `ocr/`) | two passes: the doubtful places listed (94, with a list of the words found in no other volume, the Commedia or a word list), then decided in crops; the remaining doubts decided with the user | 9 misread, 39 misprints, 33 kept as printed |
| 6. Figures | twelve images cut from the scan by fixed boxes; the map labels read in enlarged crops | 3 misread |
| 7. Close | the Italian verse against the standard text word by word, the near misses decided in the image | 2 misprints |

Each place was decided in the image as **misread** (corrected), **misprint** (kept as
printed, marked `{{printed|fixed}}`, listed in [misprints.tsv](misprints.tsv)) or
**printed** (kept); every decision is a row of [readcheck.tsv](readcheck.tsv): 34
misread, 58 misprints, 41 printed (`misprints.py`: 58 rows, 58 marks, no problems).

## 3. What was found

- **The base was good**: 34 misreadings in 424 pages, few of them words. The trial found
  only marks (`∵`, `=` set close). The comparison found the words, and above all the
  Italian made as the standard text has it (10 of its 16: `servizio` for the printed
  `servigio`, `Gesù` for `Jesù`, a colon for a semicolon). The read-through and the
  figures found what no OCR compares: the thick letters of the Tables of Kings written
  plain and `Paradise` made `Paradiso` in their head note; `of the` dropped at a line
  end; map labels (`SANTHELLA` for `SANNELLA`, a fragment written twice).
- **Misprints now**: 59 rows, all marked, after the fixes from the translations and the
  review of 2026-11-28, which took the author's errors and the edition's own spellings
  back to the print (DONE.md, "The author's errors back to the print"). The counts below
  are those of the close.
- **Misprints**: 58, two thirds from the read-through: accents and letters in the Italian
  (`ch`, `cio`, `sara`, `comforti`), English spellings (`vengence`, `abbott`,
  `witholding`, `Ostragoths`), a tercet number (`10` for `100`), citations and stops in
  the notes, the signatures of the editorial note, two labels (`Empir`, `The Pere gate`).
  The base had corrected five silently. Two in the verse (`Oppreso`, `comtemplante`, the
  first lines of Cantos XXII and XXXII) were passed by every reading and by the
  read-through, and found only when the verse was set against the standard text.
- **The edition's readings**, kept (PLAN.md, "Settled readings"): elisions set close,
  `’t is` spaced, `=` set close, the colon in citations written `N: N`; the Italian as
  printed where it differs from the standard text. Two dates differ between the tables
  (Frederick of Sicily from 1296 in Table I, 1295 in Table IV): both are current, and
  both are kept.

## 4. Learnt for the other texts

- **A strong base, a comparison and a read-through suffice**, as in `en-purgatorio`: no
  retype; the comparison found the words, the read-through the misprints.
- **A strong base still makes the edition's text the standard one**: in the Italian
  spellings and stops, and even the English title in a table (`Paradise`). A form that
  differs from the standard text is checked in the image, not trusted either way.
- **Type is not only words**: the thick letters of a table, a key to the persons it
  marks, were lost by every reading; the tables and labels are read for their type as
  well as for their names.
- **The verse against the standard text, word by word, after the read-through** lists
  the near misses (a letter or two, rare in the volume's own Italian); almost all are
  the edition's readings, but the list costs little and found two misprints in first
  lines, where a reader's eye runs ahead.
- **Converting before the base is checked** paid off again: every step worked on the
  converted text with the converter's report as a baseline, and the output of the other
  two volumes was checked unchanged at each change of the scripts.
