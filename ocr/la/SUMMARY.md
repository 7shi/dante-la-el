# Summary: how `ocr/la` was transcribed and checked

A short account of the work on `ocr/la`, Serravalle's Latin translation and commentary
(1891), from the first transcription to the last check (2026-10-10 – 2026-11-05), written
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
  the rest are decided in the image. The paid calls were run by the user.
- **Narrow delegation.** What was still delegated was narrow and checkable: retyping
  pages the OCR had broken, and reading verse lines from the image alone. Every result was
  compared with `ocr/la` by script, and the differences were decided in the image.
- **Scripted checks** over every page: `scripts/check.py` (tercets, rules), `scripts/seqcheck.py`
  (line order), `scripts/lostcheck.py` (lost text), `scripts/lines.py` (line breaks, blank lines),
  and the warnings of `texts/convert_la.py`, which converts `ocr/la` into
  `texts/la/001`–`110`.

## 2. The checks after completion

The markup cannot see a word that both OCRs misread alike (0085 `terret` for printed
`territ`). Four checks looked for such errors (2026-11-01 – 2026-11-05):

| Check | Method | Found |
|---|---|---|
| Check 1 | the commentary's lemmas compared with the verse they quote; 1,271 candidates decided in the image | 9 misread, about 80 more errors in the same lines and by the searches they led to |
| Verse check | the Latin verse compared with the Italian, then every line of both verse columns read again from the image by delegates and compared by script | about 250 lines misread, 46 misprints |
| Italics | marked `*…*` from the slant of the print, the flagged lines decided in the image; the same-line pairs decided by sense | 4,232 pairs |
| Check 2 | a form found once or twice, near a form found at least 5 times (22,567 candidates); groups 1–2 decided in the image, group 3 read for sense by a delegate, the flagged words decided in the image | 149 misread, 94 misprints |

Each flagged place was decided in the image as one of three: **misread** (corrected in
`ocr/la`; a damaged letter is restored by the sense), **misprint** (kept as printed and
listed), or **printed** (kept, nothing to do).

## 3. What is left

- **Misprints** are not corrected in the text. The 202 rows of PLAN.md ("Suspected
  misprints") list them with page, line and the probable reading.
- **Known limits** (PLAN.md): the commentary has not been read through as a whole. Check 2
  read only its candidates (in their lines, for sense), so a misreading into a common word,
  a rare word with no common neighbour, or a common spelling written for a rare printed
  one may remain. The italics follow a mechanical convention, not the print in every
  detail.

## 4. For the other texts

- **What carries over**:
  - delegates get narrow tasks whose results can be compared by script; their reports are
    not taken as evidence;
  - a delegate flags, it does not correct: flagged places are decided in the image;
  - every place is decided as misread, misprint or printed; misprints are listed, not
    corrected;
  - each fix is followed by the scripted checks and a conversion, with their output
    compared with the previous run.
- **What differs**:
  - `ocr/en` (1,030 files), `ocr/en-oelsner` (834) and `ocr/grc` (704) have one OCR each:
    no second OCR was compared, so plain misreadings, not only shared ones, may remain;
  - parts of them have had checks of their own (texts/PLAN.md, "Status"): the Italian of
    `en` and `en-oelsner` against dante-corpus, Oelsner's English against `texts/en`, the
    Greek verse by a syllable count; what no check has read is mainly prose: Carlyle's
    English and notes, Oelsner's notes, the Greek prologue, arguments and notes.
- **Next**: one last read-through, the commentary of `ocr/la` included, for misreadings and
  misprints together. It is the final pass over each text; no further pass is planned.
