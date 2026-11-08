# Summary: how `ocr/la` was transcribed and checked

A short account of the work on `ocr/la`, Serravalle's Latin translation and commentary
(1891), from the first transcription to the last check (2026-10-10 – 2026-11-08), written
as a starting point for checking the other texts. The details are in
[DONE.md](DONE.md) (the method, every batch and every check), the rules, the conventions
and the limits in [PLAN.md](PLAN.md), the tasks given to the delegates in
[DELEGATION.md](DELEGATION.md).

## 1. The transcription

- **Sources.** `ocr/la` is the first OCR (Gemini 2.5 Flash) of the scans `0001`–`1296`.
  GLM-OCR, an independent OCR of every page, and Tesseract (word boxes, a third reading)
  serve only for checking (PLAN.md, "Sources for checking").
- **Open-ended delegation, given up.** The first batches were proofread by delegates
  (la-el-agy, la-el-codex) told to correct the pages. Their reports were not reliable,
  and their changes brought errors of their own: printed colons made semicolons, printed
  spellings normalized, misprints "corrected" from the sense. Errors shared by both OCRs
  were left. Only a word diff against a snapshot showed what they had done.
- **Two-OCR markup.** The method that completed the volume: an LLM lists where `ocr/la`
  and GLM-OCR disagree (a JSON list, so it cannot alter the text), a script writes each
  difference into the page as `{{ocr|glm}}`, the trivial ones are resolved by script, and
  the rest are decided in the image. The paid calls were run by the user. The markup
  was only in work copies; the same syntax now holds the misprints (section 3).
- **Narrow delegation.** What was still delegated was narrow and checkable: retyping
  pages the OCR had broken, and reading verse lines from the image alone. Every result was
  compared with `ocr/la` by script, and the differences were decided in the image.
- **Scripted checks** over every page: `scripts/check.py` (tercets, rules), `scripts/seqcheck.py`
  (line order), `scripts/lostcheck.py` (lost text), `scripts/lines.py` (line breaks, blank lines),
  and the warnings of `texts/scripts/convert_la.py`, which converts `ocr/la` into
  `texts/la/001`–`110`.

## 2. The checks after completion

The markup cannot see a word that both OCRs misread alike (0085 `terret` for printed
`territ`). Four checks looked for such errors (2026-11-01 – 2026-11-05), and a reading of
the whole text for sense came last:

| Check | Method | Found |
|---|---|---|
| Check 1 | the commentary's lemmas compared with the verse they quote; 1,271 candidates decided in the image | 9 misread, about 80 more errors in the same lines and by the searches they led to |
| Verse check | the Latin verse compared with the Italian, then every line of both verse columns read again from the image by delegates and compared by script | about 250 lines misread, 46 misprints |
| Italics | marked `*…*` from the slant of the print, the flagged lines decided in the image; the same-line pairs decided by sense | 4,232 pairs |
| Check 2 | a form found once or twice, near a form found at least 5 times (22,567 candidates); groups 1–2 decided in the image, group 3 read for sense by a delegate, the flagged words decided in the image | 149 misread, 94 misprints |
| Read-through | the whole of `texts/la` read for sense by a delegate in batches of 25 pages (2026-11-05 – 2026-11-08); every flagged place (3,180) decided in the image | 124 misread, 989 misprints |
| Misprint marks | the misprints written into the pages by a script (2026-11-08); the fixed lines of the 729 marks the script placed by likeness (printed and fixed forms with a similarity of 0.7 or more) read by a delegate in one task | 20 marks on the wrong words (a word lost or doubled, the fix on the next word), moved |

Each flagged place was decided in the image as one of three: **misread** (corrected in
`ocr/la`; a damaged letter is restored by the sense), **misprint** (kept as printed,
marked with its fix and listed), or **printed** (kept, nothing to do).

## 3. What is left

- **Misprints** are marked in `ocr/la` as `{{printed|fixed}}` (PLAN.md, "Misprint marks"):
  the left side keeps the print, `texts/la` has the right side. `misprints.tsv` lists them
  (1,053 rows, 1,050 marked; 3 left unmarked, the fixed form not certain) with the source
  of each fix: the same page, the edition elsewhere, Dante's text, or a source named.
  `scripts/misprints.py` checks the marks against the list. The scripts that compare
  `ocr/la` with the image read the left side; `convert_la.py` writes the right side.
- **Known limits** (PLAN.md): the read-through has read the whole text, the commentary
  included, but a reading for sense does not see a misreading that reads well: a spelling
  the OCR normalized (`Quae` for `Que`), an accent added or dropped. The italics follow a
  mechanical convention, not the print in every detail.

## 4. For the other texts

- **What carries over**:
  - delegates get narrow tasks whose results can be compared by script; their reports are
    not taken as evidence;
  - a delegate flags, it does not correct: flagged places are decided in the image;
  - every place is decided as misread, misprint or printed; misprints are listed, not
    corrected;
  - each fix is followed by the scripted checks and a conversion, with their output
    compared with the previous run;
  - the order: first the checks against the images or other sources, then one reading for
    sense at the end. The read-through finds what the earlier sense checks of `ocr/la`
    found (check 2 group 3, the Latin verse against the Italian); it does not see a
    misreading that reads well, such as an OCR normalization or an accent;
  - in the read-through, before a place is kept as printed: a quotation of the poem is
    compared with the verse of the main text (1277 `al fuoco`, 0884 `el fuoco`), a form
    that looks wrong on many pages is searched across the text (`Eunce`, the edition's
    spelling), and a sentence that breaks off is checked for the column order (PLAN.md,
    "Read-through", "Settled readings");
  - a script that puts text into the pages (the misprint marks) chooses its words by
    itself: its output is read once more, line by line (20 of 729 marks were misplaced);
  - a delegate's task can be large when it is narrow: the 729 marks went in one task, the
    read-through in batches of 25 pages;
  - the tools of the read-through are shared, not tied to `ocr/la`
    ([ocr/scripts/README.md](../scripts/README.md), "The read-through"): `pages.py`,
    `findline.py`, `wordcrop.py` (it needs Tesseract's word boxes of the text), `txtfix.py`.
- **What differs**:
  - `ocr/en` (1,030 files), `ocr/en-oelsner` (834) and `ocr/grc` (704) have one OCR each:
    no second OCR was compared, so plain misreadings, not only shared ones, may remain;
  - parts of them have had checks of their own (texts/PLAN.md, "Status"): the Italian of
    `en` and `en-oelsner` against dante-corpus, Oelsner's English against `texts/en`, the
    Greek verse by a syllable count; what no check has read is mainly prose: Carlyle's
    English and notes, Oelsner's notes, the Greek prologue, arguments and notes.
- **Next**: `ocr/la` is done. The work on `ocr/en`, `ocr/en-oelsner` and `ocr/grc` is
  planned in [ocr/PLAN.md](../PLAN.md): every page retyped from the image by la-el-agy,
  compared by script with `ocr/DIR`, GLM-OCR and Tesseract, then the last reading for sense,
  each step beginning with a trial of a few pages.
