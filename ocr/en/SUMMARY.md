# Summary: how `ocr/en` was checked

A short account of the check of `ocr/en`, Carlyle's prose translation of the Inferno with
the Italian text and his notes (1889), by the flow of [ocr/PLAN.md](../PLAN.md)
(2026-11-08 – 2026-11-10). The plan and the settled readings are in [PLAN.md](PLAN.md),
every batch and every decision in [DONE.md](DONE.md), the transcription's conventions in
[README.md](README.md).

## 1. The starting point

`ocr/en` was GLM-OCR proofread against the images by Gemini 3.8 Flash, then a final check
(README.md, "Credits"). Its Italian verse had been compared line by line with
dante-corpus and its footnote markers restored (texts/PLAN.md, "`texts/en/`"). No second
reading had been compared, and the English prose and notes had not been read again.

## 2. The steps

| Step | Method | Decided |
|---|---|---|
| 0. Setup | the tables, `convert_en.py` taught the misprint marks, `misprints.py` made to take the directory, Tesseract's word boxes (`-l eng+ita`), the shared tools tried, a retype template | the baseline of `convert_en.py` kept |
| 1–2. Retype and compare | every page retyped from the image alone by la-el-agy (Gemini 3.8 Flash), 22 batches; `ocr/scripts/cmpread.py` aligns the base, the retype and Tesseract word by word; every difference decided in stacked crops. `431`–`455` and the index were read against the image by la-el-claude (Opus 5.5) instead | 47 misread, 62 misprints, 63 printed |
| 3. Read-through | the whole of `texts/en` read for sense by la-el-agy (Gemini 3.8 Flash): a trial of 19 pages, then 20 batches of 25 scans; 66 places flagged in the batches, each decided in the image | 8 misread, 42 misprints, 24 printed; one fault of `convert_en.py` |
| Index survey | every reference of the index looked up in the verse by a script; the 93 whose name is not near the verse read one by one | 2 misprints, 1 printed |

Each place was decided in the image as **misread** (corrected in `ocr/en`), **misprint**
(kept as printed, marked `{{printed|fixed}}` and listed) or **printed** (kept); every
decision is a row of [readcheck.tsv](readcheck.tsv).

## 3. What was found

- **Misreadings of the base** were few and small: a letter (`375` `ei` for `el`, `484`
  `Mordred` for `Mordrec`), points and quotes, words joined in a tight line, a paragraph
  split in two, small capitals in normal case. The retype found most of them; the
  read-through found the rest (8).
- **Misprints**: 109 rows in [misprints.tsv](misprints.tsv), all marked (`misprints.py`:
  109 rows, 109 marks, no problems). Many the base had corrected silently (turned `n`s,
  `c` for `e`), found by the retype; the read-through found misprints no comparison sees: a
  closing period or quote not printed, a wrong letter in the Italian (`186` `le`, `269`
  `s’ er`, `371` a period inside a sentence), a word doubled (`279` `the the`), a wrong
  word in the English (`228` `glorious heaven`), and 12 wrong references in the index (10
  by the read-through, 2 by the survey). The
  source of each fix is given: `edition` 80, `dante` 24, `other` 5 (a source named, as
  Virgil).
- **Printed, not corrected**: a wrong reference by the author in a note (`054` `Ibid. v.
  118`, `240` `Acts viii. 33`, `242` `Æn. i. 103`, `318` `i. 29`) or in the index where no
  slip of the type explains it (`480` `Bolognese`, `482` `Greece`, `485` `Rhone`); the
  edition's spellings and the Latin of its sources (`218` `Astream`).
- **`convert_en.py`**: the continued notes of the front matter (pages beginning with the
  end of the previous page's last note) had become prose; fixed with a table of the pages
  (`CONT_BLOCKS`, `CONT_VERSE`). Otherwise its output kept the baseline after every batch.

## 4. Learnt for the other texts

- **The retype was worth it** even for a proofread base: it found the misprints the
  proofreading had corrected silently, and the few misreadings, at about 25 pages a batch
  with no loss of care in the later pages.
- **The read-through flagged few places** (1–4 a batch in the cantos), as the comparison
  came first; most flags were real. The reader's claims about the print ("the edition
  prints …") were often false, and its verse numbers often off: every place was decided in
  the image, every verse number taken from `texts/en`.
- **A flag leads to a search**: a misprint of one kind was searched across the text
  (notes without a closing period, `Lit` without its period, a space before a colon), and
  a wrong reference in the index led to a survey of all references by script.
- **A wrong reference** is a misprint only when a slip of the type explains it (a numeral
  dropped or added, a number taken from the line above) and the right place is certain;
  otherwise it is the author's, as printed.
