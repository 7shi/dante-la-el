# Summary: how `ocr/grc` was checked

A short account of the check of `ocr/grc`, Musurus's Greek verse translation of the
Inferno with his notes (1882), by the flow of [ocr/PLAN.md](../PLAN.md)
(2026-11-10 – 2026-11-13). The plan, the corrigenda and the settled readings are in
[PLAN.md](PLAN.md), every batch and every decision in [DONE.md](DONE.md), the
transcription's conventions in [README.md](README.md).

## 1. The starting point

`ocr/grc` was Gemini 2.5 Flash's OCR proofread against the images by GPT-6.1 Sol, then a
final check (README.md, "Credits"). The conversion had checked the verse count of every
canto, the printed line numbers and the arguments against the table of contents, and a
syllable count had found 33 misreadings that broke the twelve-syllable line
(texts/PLAN.md, "`texts/grc/`"). No second reading had been compared: a misreading that
kept the metre, and any in the prose (the preface, the arguments, the notes), could
remain.

## 2. The steps

| Step | Method | Decided |
|---|---|---|
| 0. Setup | the tables, `convert_grc.py` taught the misprint marks, Tesseract's word boxes (`-l grc`, with `lat+ita+fra` on the notes), `cmpread.py` and `wordcrop.py` made ready for Greek (accents and breathings compared), a retype template; GLM-OCR tried and not used | the baseline of `convert_grc.py` kept |
| 1–2. Retype and compare | every page retyped from the image alone: retypes 01–02 by la-el-agy on Gemini 4 Argon, 03–11 on Gemini 3.8 Flash, 12–15 (`259`–`351`) by Claude (Opus 5.5) itself; `cmpread.py` aligns the base, the retype and Tesseract word by word; every difference read in the image, the marks at eight to twelve times beside sure ones of the same pages | 1280 misread, 87 misprints, 129 printed |
| 3. Read-through | the whole of `texts/grc` read for sense by Claude (Opus 5.5) itself: a trial of 20 pages, then 13 batches of about 25 scans, the preface and the table of contents last | 23 misread, 19 misprints, 63 printed |
| The held decisions | `ᾀεί` and `θλίψις` (the edition's spelling, every place read), `εἶς`, `Ἢν` | 9 printed |
| 4. The corrigenda | the two lists (`014`, `015`–`018`) applied to `texts/grc` by marks in the pages, every entry a row of [corrigenda.tsv](corrigenda.tsv); the lists not converted | 92 of 94 entries applied; 6 misread |

Each place was decided in the image as **misread** (corrected in `ocr/grc`), **misprint**
(kept as printed, marked `{{printed|fixed}}` and listed) or **printed** (kept); every
decision is a row of [readcheck.tsv](readcheck.tsv) (a row may cover several words of a
line).

## 3. What was found

- **Misreadings of the base** were many, unlike `ocr/en` (47): 56–117 in a batch of
  25 pages, almost all accents and breathings that read well: enclitic accents (`δή μοι`,
  `ἐμοί τις`), elisions and crasis (`τοὐμοῦ`, `κᾆτα`), the iota subscript (`ᾐσθάνθη`,
  `ὁρᾷν`), `ῤῥ` made `ρρ`, rough and smooth exchanged. Fewer, but worse, were rare forms
  made common, keeping the metre: `021` `στυγήρης` for the printed `συνήρης`, `292`
  `ἀθανατισθεῖσα` for `ἀπαθανατισθεῖσα`, `343` `μνημονευσομένων` for
  `μνημονευθησομένων`. In the corrigenda many readings had been taken from the verse they
  correct.
- **Misprints**: 98 rows in [misprints.tsv](misprints.tsv), all marked (`misprints.py`: 98
  rows, 98 marks, no problems): accents and breathings, an iota subscript under a capital
  (`030` `ᾙρέθη`), a figure `1` for the `Ι` of a canto number, closing quotes and periods
  not printed, and slips in the Latin and Italian of the notes (`336` `Conrandin`, `348`
  `Alterigo`). The base had corrected many silently; the retype found them.
- **The edition's spellings**, not misprints: `ᾀεί` with the iota subscript (printed so in
  all 22 places), `θλίψις` with the acute, the crasis with the circumflex (`τἆλλα`); the
  roman type's one `^` mark for the rough and the smooth breathing with grave (PLAN.md,
  "Settled readings").
- **The corrigenda**: 94 entries, 92 applied (`corrigenda.tsv`; `misprints.py`: 92 marks,
  no problems); the eight misprint marks they list became corrigenda marks. The lists' own
  line numbers are wrong for 7 verse entries, so the phrase decided the place; five places
  the base had in the corrected form were read as printed. The syllable count: five verse
  lines not of twelve syllables have twelve once corrected.
- **`convert_grc.py`**: its report kept the baseline after every batch; the two corrigenda
  files are no longer written (texts/PLAN.md, "The corrigenda").

## 4. Learnt for the other texts

- **A proofread base can still hold many misreadings** where the script is hard: the
  proofreading kept the sense and the metre, not the accents and breathings. Only a
  comparison with a second reading, every place read in the image, found them.
- **The marks are read large**: the scans are small, so a breathing or an accent is read
  at eight to twelve times its size, beside a sure one of the same type and pages; the
  settled forms of the marks (PLAN.md) made the later batches faster.
- **Retypers**: Gemini 4 Argon (about 15 places in 25 pages) and Gemini 3.8 Flash (5–16)
  erred about as often, and Claude's own retype as well (3–10 in 25 pages; the
  grammar's form for the printed one, `Ἅδου` for `ᾍδου`); against them the base had
  56–117 misreadings a batch. An error the base and the retype share does not show: the
  read-through found the rest.
- **A spelling that looks wrong in one place is searched in all** before it is marked
  (`ᾀεί`, `θλίψις`): thirteen marks were removed once every place had been read.
- **The corrigenda** are applied by marks in the pages, not by rewriting them: the pages
  stay as printed, every entry is a row of a table, and a script checks the marks
  against it (ocr/PLAN.md, "Corrigenda").
