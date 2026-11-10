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
Retypes 04 (`059`–`083`), 05 (`084`–`108`) and 06 (`109`–`133`) decided, Gemini 3.8
Flash (the user's choice, 2026-11-10). Retype 07 (`134`–`158`) returned (files checked: all 25 present, none empty; undecided), retype 08 (`159`–`183`) returned (all 25 present, none empty; undecided), retype 09 (`184`–`208`) returned (all 25 present, none empty; undecided), retype 10 (`209`–`233`) returned (all 25 present, none empty; undecided). Retype 11 (`234`–`258`) returned (all 25 present, none empty; undecided). Stopped here by the user: retype 12 waits several days (rate limit); not sent until they say so. From here the
batches are sent one after another and not decided as they return ("How a batch runs"):
the returned and undecided ones are listed here as they come (none yet). Not committed
yet: retype 06.

## The work ahead

1. **Retypes 07–15, to the last page** (the user, 2026-11-10: batches of 25 pages to
   the end, all on Gemini 3.8 Flash, sent one after another; "How a batch runs"):

   | retype | pages | number | kind |
   |---|---|---|---|
   | 07 | `134`–`158` | 25 | cantos (returned, undecided) |
   | 08 | `159`–`183` | 25 | cantos (returned, undecided) |
   | 09 | `184`–`208` | 25 | cantos (returned, undecided) |
   | 10 | `209`–`233` | 25 | cantos (returned, undecided) |
   | 11 | `234`–`258` | 25 | cantos (returned, undecided) |
   | 12 | `259`–`285` | 27 | cantos, to the end of the poem |
   | 13 | `287`, `289`–`291`, `293`–`313` | 25 | notes |
   | 14 | `314`–`338` | 25 | notes |
   | 15 | `339`–`342`, `344`–`351` | 12 | notes |

   Not retyped: `286`, `288` (not in `texts/grc`), `292`, `343` (done in the trial). The
   batch 12 takes the two last pages of the poem with it, so that no batch mixes verse
   and notes. The notes are in smaller type, with Latin, Italian, French and a little
   Hebrew and Arabic; Flash is untried on them, and they go to it all the same (the
   user's choice). Their task says "the notes" for the cantos; the template's rules
   already name the languages.
2. **The deciding** of retypes 07–15 (step 2), when the user asks: batch by batch in
   page order, each with its section in DONE.md.
3. **Read-through** (step 3), then **the corrigenda** with the user (step 4), then **the
   close** (step 5).

How a batch runs (asked by the user, 2026-11-10):

- **From retype 07 on** (the user, 2026-11-10): when a reply comes, the returned batch is
  only checked for its files (every page present, none empty), not decided, and the next
  batch is sent at once, without a new signal, to the last one (retype 15). All on
  Gemini 3.8 Flash; the user says so if the model is changed. The deciding of the
  returned batches waits for the user.
  **Stop after retype 11** (the user, 2026-11-10): the Gemini 3.8 Flash rate limit is
  expected to be reached with 11, so 12 onward wait several days. When 11 returns, check
  its files and wait; retype 12 is not sent until the user says so.
- The task file is the last one with its pages and paths changed; no new rules. The list
  of the last batch's errors stays that of retype 06 while the batches are undecided,
  without its `ᾈττίλαν` line ("Open points").
- Until retype 06 (replaced by the above): the user gave the signal before each batch,
  and a returned batch was decided before the next was sent.
- Commits only when the user asks, `ocr/grc` and `texts/grc` apart; the last ones cover
  retypes 01–05.

What the batches taught about the deciding (retype 06):

- **Before the comparison** the retype is copied with its separate breathings joined to
  their capitals ("Settled readings"), and `cmpread.py` run on the copy: retype 06 had 33
  of them, 30 places of noise. The retype itself is not changed.
- **The scans are small** (about 1030 pixels wide): a breathing or an accent is read at
  eight times its size, in a crop of the word, and a doubtful one beside a sure one of
  the same type (roman or italic) from the same pages. `wordcrop.py`'s band is enough for
  letters, not for the marks.
- **An argument fixed on a canto's first page** is compared by `convert_grc.py` with the
  table of contents (`009`–`013`): a difference it reports is read in both images, and
  the table's page fixed too if it was misread (`Λάνος`, `011` and `112`).
- **`txtfix.py` does not delete a line**: a line that is not printed is emptied (an empty
  `new`), the blank line left.
- **The base's own separate breathings** (`᾽Αλλ᾽`) are known on `137`, `144` and `148`:
  joined when retype 07 is decided.

Open points, for the user:

- **`ᾀεὶ` with the iota subscript** is marked as a misprint by the settled reading, but it
  is now printed in six places (`038`, `077`, `107`, `110`, `120`, `124`), and `ἀεὶ`
  without it was read in the image only where a retype differed. It may be the edition's
  spelling. **Held until the whole text is done** (the user, 2026-11-10): until then each
  one is marked as before; then they are counted, and kept as misprints or changed to
  printed, the marks and the rows of misprints.tsv with them.
- **The task of retype 07** names `ᾈττίλαν` (`111` 4) as an error of retype 06; the user
  then read the iota subscript in the image, and it is a misprint the retype found. The
  task was already sent and is not changed: in the deciding of 07, a subscript missing
  in the retype is not taken as a vote against the base. The task of 08 drops the line.

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
  (retypes 01–02), then Gemini 3.8 Flash (03–06), which erred about as often (DONE.md).
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
  `038` `ᾈεὶ`) is a misprint, marked; so is one under a small letter (`107` `ᾀείποτε`,
  `110` and `124` `ᾀεὶ`, `120` `Ἐσᾳεὶ`). A mark under a capital, low and
  blurred, is the subscript too, not a blot (`111` `ᾈττίλαν`, read by the user).
- **A low mark between two words** (or a quote and a word) is a spacing quad's, not a
  period: not written (`033` 10, `064` 19, …).
- **The roman rough breathing with an accent** prints as one `^`-like mark, grave and
  acute alike: the base's accent is kept (`Ὃς`, `Ἓν`).
- **The marks of the italic type** (read beside sure ones): smooth with circumflex is
  `3`-shaped (`ἆρ᾽`), smooth with acute a comma and a stroke (`οὔκ`), rough with acute an
  open `c` with a stroke (`αἵματ᾽`), diaeresis with acute dagger-shaped (`πρωΐα`); rough
  with grave a caret with a dot at its top (`ἣ`, `ὃ`), smooth with grave a comma and a
  back stroke (`ἂν`); under a circumflex the hook opens to the right for the rough
  breathing (`οὗτος`), to the left for the smooth (`ἦς`, `τοὖργον`).
- **The italic capitals Λ and Δ**: the Λ has serifs at its feet that nearly meet, the Δ a
  solid base (`Λάνος` 011, 112; `Διτός` 075).
- **The figure `1` for the `Ι`** of a canto number in a heading or running head (one
  serif at the top, to the left) is a misprint, marked (`112`, `124`).
- **The page number** is written on the line after the running head, also where the base
  had it before; a number at the foot that is not printed is removed.
- **A breathing written as a separate character** before a capital (`᾿Α`) is the same
  reading as the joined letter (`Ἀ`): joined in the retype before the comparison, and in
  the base where it is met.
- **Nested quotes** open `‘“`, go on `‚ „` at the following lines and close `”’` (`034`,
  `074`).
- **Signature marks** as the base writes them (`Ε 2`, `F`, `G 2`); `convert_grc.py` drops
  them.
