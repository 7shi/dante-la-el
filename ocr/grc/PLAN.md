# Plan: checking `ocr/grc`

The check of `ocr/grc`, Musurus's Greek verse translation of the Inferno with his notes
(1882), by the flow of [ocr/PLAN.md](../PLAN.md): the second of the three texts (decided
with the user, 2026-11-10), as `ocr/en` was checked ([../en/SUMMARY.md](../en/SUMMARY.md)).
The work done is recorded in [DONE.md](DONE.md); the conversion into `texts/grc/` is
described in [texts/PLAN.md](../../texts/PLAN.md) ("`texts/grc/`"), the transcription in
[README.md](README.md).

**A new session starts here**: read "State". The rules of ocr/PLAN.md ("Decisions",
"Read-through") apply.

## State (2026-11-10)

Step 0 (setup) done (DONE.md). Step 1–2: retypes 01 (the trial) and 02 (`001`–`032`)
decided, Gemini 4 Argon; retype 03 (`033`–`058` without `038`) decided, Gemini 3.8 Flash
(Argon's quota reached; a comparison of the two models, asked by the user, 2026-11-10).
Retypes 04 (`059`–`083`) and 05 (`084`–`108`) decided, Gemini 3.8 Flash (the user's
choice, 2026-11-10). Next: retype 06 (`109`–`133`), when the user gives the signal.

## The work ahead

1. **Retypes 06–12, the cantos** (`109`–`285`, 177 pages), batches of about 25 in page
   order: 06 `109`–`133`, 07 `134`–`158`, 08 `159`–`183`, 09 `184`–`208`, 10
   `209`–`233`, 11 `234`–`258`, 12 `259`–`285`. Each batch decided as in step 2, its
   section added to DONE.md and the State updated here.
2. **Retypes 13–15, the notes** (`287`–`351` without `288`, and `292`, `343` done in the
   trial; 62 pages): 13 `287`–`313`, 14 `314`–`338`, 15 `339`–`351`. Smaller type, with
   Latin, Italian, French and a little Hebrew and Arabic: the model is chosen again with
   the user before 13 (Flash is untried on these pages), and the task names the
   languages (the template's rules already do).
3. **Read-through** (step 3), then **the corrigenda** with the user (step 4), then **the
   close** (step 5).

How a batch runs (asked by the user, 2026-11-10):

- The user sets la-el-agy's model by hand and gives the signal; nothing is sent before
  it. The task file is the last one with its pages, paths and the list of the last
  batch's errors changed; no new rules.
- When the reply comes, the batch is checked and decided before anything else is sent;
  the next batch waits for the user.
- Commits only when the user asks, `ocr/grc` and `texts/grc` apart; the last ones cover
  retypes 01–05.

## The text

- **Pages**: 351 scans; 346 of them are in `texts/grc` (texts/PLAN.md, "Files"; not `004`,
  `008`, `020`, `286`, `288`). Only these are checked.
- **Kinds of page**: the title pages (`001`–`003`); the prologue (`005`–`007`, prose); the
  table of contents (`009`–`013`, the arguments again); the corrigenda (`014`,
  `015`–`018`, tables); the cantos `021`–`285` (an argument, then the verse, about 30
  lines a page, every fifth numbered); the notes `287`–`351` (prose in smaller type,
  quoting Latin, Italian, French and a little Hebrew and Arabic).
- **Its transcription**: Gemini 2.5 Flash, proofread against the images by GPT-6.1 Sol,
  then a final check (README.md, "Credits"). Lines as printed, with the running heads,
  page numbers, verse numbers and signature marks (texts/PLAN.md, "Conversion notes"). The
  conversion checked the verse count of every canto, the printed verse numbers and the
  arguments against the table of contents, and a syllable count found the misreadings that
  break the twelve-syllable line (33 fixed). A misreading that keeps the metre, and any
  misreading in the prose, may remain; the transcription tends to replace rare forms by
  common ones and to change accents and breathings (texts/PLAN.md; README.md, "Observations
  on the OCR").

## The corrigenda later

The book prints two lists of corrections: `014` (misprints) and `015`–`018` (misprints and
the translator's revisions of words and lines). The check first follows the print, as for
`ocr/en`: a reading listed in the corrigenda is decided like any other place, as printed.
How the corrigenda are used (marks, revisions) is decided with the user after the
read-through (asked by the user, 2026-11-10).

## The readings to compare

- **The base**: `ocr/grc` itself, with its fixes kept unless the image says otherwise.
- **The retype**: every page from the image alone by la-el-agy (step 1), on Gemini 4 Argon
  (retypes 01–02), then Gemini 3.8 Flash (03–05), which erred about as often (DONE.md).
- **Tesseract** (`-l grc`; `grc+lat+ita+fra` on the notes), the third vote and the word
  boxes for `wordcrop.py`. It reads the Greek fairly (`021`: `ἀχληγορική`, `Ἐύρέθην` for
  the printed `ἀλληγορική`, `Εὑρέθην`), and found a misreading in the setup (`021`
  `συνήρης` printed, the base `στυγήρης`).
- **GLM-OCR** is not used: tried on `021` in the setup, it loses most accents and
  breathings and mixes Latin letters into the Greek (`Ο δρυμώντραχύς, αγριος`, `Tà`,
  `Bιργίλιος`), so it would add only noise to the comparison (ocr/PLAN.md, step 2: "the
  trial decides").

## Steps

0. **Setup** (done, DONE.md): the tables; `convert_grc.py` taught the marks, its baseline
   kept; `ocr/grc/tesseract/`; GLM-OCR tried and not used; `cmpread.py` and `wordcrop.py` made ready for Greek;
   [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md); the shared tools tried.
1. **Retype** (la-el-agy on Gemini 4 Argon, chosen by the user for the polytonic Greek,
   2026-11-10; the user sets the model and gives the signal
   before each batch; the model of each batch recorded in DONE.md):
   - **Trial**: 6 pages of different kinds: the prologue (`005`), the table of contents
     (`010`), a canto opening with the argument (`021`), a verse page with quotations
     (`038`), notes pages (`292`, a canto's notes starting mid-page; `343`, a footnote and a
     signature mark). Checked by eye and by `cmpread.py`; the batch size is set from it
     (`en`: 25 pages).
   - **Batches** in page order; on each reply the returned one is checked (pages present,
     none mixed up) and decided before the next is sent (asked by the user, 2026-11-10).
2. **Compare and decide**, batch by batch, as for `en` (ocr/en/PLAN.md, step 2):
   `uv run ocr/scripts/cmpread.py ocr/grc tmp/grc-retypeNN -t ocr/grc/tesseract`; the
   accents and breathings are compared, so their differences are decided too. Classes A
   and C each one, B with care; fixes and marks with `txtfix.py`; every decision a row of
   `readcheck.tsv` (note `cmp A`, `cmp B`, `cmp C`). After each batch `convert_grc.py`
   compared with the baseline and `misprints.py ocr/grc` run.
3. **Read-through** (ocr/PLAN.md, "Read-through") over `texts/grc`: a trial of about 20
   pages, then batches of 25 scans; decisions as in step 2 (note `read`).
4. **The corrigenda**, with the user (above).
5. **Close**: the state here, DONE.md, a SUMMARY.md; texts/PLAN.md "Status" and the README
   of `ocr/grc` (the check in "Credits"); commits, `ocr/grc` and `texts/grc` apart, when the
   user asks.

## Settled readings

The edition's readings found in the steps go here, and are applied, not asked again.

- **Leader dots** of the table of contents (`. . 25`) are not compared: their number is
  layout, not text.
- **The corrigenda tables** (`014`–`018`) keep the base's columns: a cell wrapped over two
  printed lines on one row, the canto and line numbers without their printed comma and
  period. Only the words of the cells are compared.
- **An iota subscript printed under a capital** where the word has none (`030` `ᾙρέθη`,
  `038` `ᾈεὶ`) is a misprint, marked; so is one under a small letter (`107` `ᾀείποτε`).
- **A low mark between two words** (or a quote and a word) is a spacing quad's, not a
  period: not written (`033` 10, `064` 19, …).
- **The roman rough breathing with an accent** prints as one `^`-like mark, grave and
  acute alike: the base's accent is kept (`Ὃς`, `Ἓν`).
- **The marks of the italic type** (read beside sure ones): smooth with circumflex is
  `3`-shaped (`ἆρ᾽`), smooth with acute a comma and a stroke (`οὔκ`), rough with acute an
  open `c` with a stroke (`αἵματ᾽`), diaeresis with acute dagger-shaped (`πρωΐα`).
- **Nested quotes** open `‘“`, go on `‚ „` at the following lines and close `”’` (`034`,
  `074`).
- **Signature marks** as the base writes them (`Ε 2`, `F`, `G 2`); `convert_grc.py` drops
  them.
