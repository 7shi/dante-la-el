# Plan: checking `ocr/en`, `ocr/en-oelsner` and `ocr/grc`

`ocr/la` is complete and checked ([la/SUMMARY.md](la/SUMMARY.md); the method and every
check in [la/DONE.md](la/DONE.md), the rules in [la/PLAN.md](la/PLAN.md)). This plan is the
work that follows: the same checks for the other three texts, taken from `la` without its
detours (asked by the user, 2026-11-08). The conversion into `texts/` is described in
[texts/PLAN.md](../texts/PLAN.md).

## State (2026-11-08)

Planned. `en` first (decided with the user, 2026-11-08; its plan in
[en/PLAN.md](en/PLAN.md)); the order of the other two is set later.

## The texts

`DIR` below is one of them, done one at a time.

| Text | Scans | Words in `texts/` | Checked already (texts/PLAN.md, "Status") |
|---|---|---|---|
| `en` (Carlyle, 1889) | 514 | 126,000 | the Italian against dante-corpus, the footnote markers |
| `en-oelsner` (Temple Classics, 1903) | 416 | 104,000 | the Italian against dante-corpus, the English against `texts/en` |
| `grc` (Musurus, 1882) | 351 | 48,000 | the verse counts and line numbers, misreadings found by a syllable count |

Each has one OCR, proofread once against the images by a model (the READMEs, "Credits"):
`en` GLM-OCR proofread by Gemini 3.8 Flash, `en-oelsner` Gemini 2.5 Flash by GPT-6 Luna,
`grc` Gemini 2.5 Flash by GPT-6.1 Sol. No second reading was compared, so plain
misreadings may remain, not only shared ones; what no check has read is mainly prose: Carlyle's English and notes, Oelsner's notes,
the Greek prologue, arguments and notes (la/SUMMARY.md, "What differs").

## Why three steps

Each step is needed (la/SUMMARY.md, "Known limits"): the comparison finds the misreadings
that read well (a spelling the OCR normalized, an accent, a like word), which no reading
for sense sees; the read-through finds what every reading shares (`la` 0085 `terret`) and
the misprints, which no comparison sees. The comparison comes first, so that the
read-through, the final pass, flags fewer places.

## The detours of `la` not repeated

From la/DONE.md:

- **Open-ended proofreading by delegates** (c1–c13, "What the delegation taught"): their
  changes had to be found by a diff and many undone. A delegate retypes or flags; a script
  compares; every place is decided in the image.
- **Retyping only the broken pages, found page by page** (items 6, 8, 10: retypes 19–58,
  after the markup of each batch): Gemini 3.8 Flash retyping from the image was better
  than both OCRs (retypes 28–29: lines, column order, lost text, verse and glosses), while
  the first OCR (Gemini 2.5 Flash) had lost and mixed text. Here every page is retyped
  once, at the start.
- **Readers tried one after another** (la-el-codex, opencode's models, retypes 22–24):
  one reader, la-el-agy. Its model is recorded for every batch (most of `la`'s retypes
  and readings name none); a batch run on a lower model (a rate limit, as 0351–0400 of the
  read-through) is run again on the agreed one.
- **Differences listed by a paid LLM** (the two-OCR markup, `la/scripts/markup.py`), needed
  for `la`'s two columns: the readings are aligned word by word by a script.
- **Several checks in a row, each with its own script and table** (check 1, the verse
  check, check 2): their image part is the comparison, their sense part what the
  read-through did again (la/DONE.md, "Read-through").
- **Misprints gathered in a table, marked later** by a script that chose the words (20 of
  729 marks on the wrong words, a second delegate task to find them): a misprint is marked
  in the page when it is decided, `{{printed|fixed}}` written by `txtfix.py`, and its row
  goes into `misprints.tsv` at once (la/PLAN.md, "Misprint marks").
- **Records in several places** (the PLAN table of misprints, a table per check): one table
  of decisions per text, `readcheck.tsv`, and `misprints.tsv`.

## Steps

0. **Setup**, before the first page is retyped:
   - `ocr/DIR/PLAN.md` (the state, the edition's settled readings as they are found) and
     `ocr/DIR/DONE.md`; `misprints.tsv` and `readcheck.tsv` with the columns of `la`.
   - The convert script of the text taught the marks (`fixed()`, as `convert_la.py`), and
     `misprints.py` made to take the directory (now `ocr/scripts/misprints.py DIR`); their output before any change
     is kept as the baseline.
   - The other readings, local and free: `ocr/DIR/glm-ocr/` (GLM-OCR, [Makefile](Makefile);
     not for `en`, whose base is GLM-OCR's) and `ocr/DIR/tesseract/` (word boxes, a Makefile as `la/tesseract`, with the text's
     languages and its three-digit page names; also for `wordcrop.py`).
   - A retype task template for the text, from
     [la/TEMPLATE-RETYPE.md](la/TEMPLATE-RETYPE.md): the text's conventions of `ocr/DIR`
     (labels, lines, notes, blank lines) and the errors seen in `la`'s retypes (colons made
     semicolons, spellings normalized, misprints corrected, specks read as marks).
   - The shared tools (`pages.py`, `findline.py`, `wordcrop.py`, `txtfix.py`;
     [scripts/README.md](scripts/README.md), "The read-through") tried on the text's page
     names and markers.
1. **Retype** every page from the image alone by la-el-agy on Gemini 3.8 Flash (the user
   sets the model; wait for their signal), into `tmp/`: a trial of a few pages, then
   batches. The user's signal before each batch; on each reply the next batch is sent
   first, then the returned one checked.
2. **Compare and decide**: a script aligns, page by page and word by word, `ocr/DIR` with
   the retype, GLM-OCR and Tesseract; spacing and the conventions of `ocr/DIR` are
   normalized first. `ocr/DIR` stays the base, so its earlier fixes are kept unless the
   image says otherwise. The places where `ocr/DIR` differs are decided in the image, in
   stacked crops (`wordcrop.py`): first where the retype and another reading agree against
   it; then where only the retype differs (its habits above: decided with care); where only
   GLM-OCR or Tesseract differs, the trial decides whether to look. A misreading is fixed
   with `txtfix.py`, a misprint marked with it and listed; whole lines or blocks one reading
   lacks are checked as `la/scripts/lostcheck.py` did. For the Greek, GLM-OCR and Tesseract
   may read too poorly to help; the trial decides, and the retype alone is then compared.
3. **Read-through** ("Read-through" below): a trial of about 20 pages, then batches of 25
   scans; the flagged places of a batch are decided in one or a few stacked crops.
4. **Close**: the convert script and `misprints.py` compared with the baseline; the state
   in `ocr/DIR/PLAN.md`, its DONE.md and a SUMMARY.md updated; commits, `ocr/DIR` and
   `texts/DIR` apart, when the user asks (after the whole text or a range they set).

## Decisions

Every place a step lists (a difference of the readings, a flagged phrase) is decided in the
image, never from the sense or from another edition, as one of:

- **misread**: `ocr/DIR` differs from the print; corrected with `txtfix.py`
  (`PAGE:LINE old new`), a damaged letter restored by the sense;
- **misprint**: `ocr/DIR` is as printed and the print is wrong; marked `{{printed|fixed}}`
  with `txtfix.py` and listed in `misprints.tsv` at once (`page line printed fixed applied
  source note`; the mark and the columns as in la/PLAN.md, "Misprint marks");
- **printed**: as printed, nothing to do (a spelling or a reading of the edition).

Every decision is a row of `ocr/DIR/readcheck.tsv` (`page line form decision note`; a
`misread` row has the old form in the note, `was …`), sorted by page and line. The
edition's settled readings, as they are found, go into `ocr/DIR/PLAN.md` and are applied,
not asked again.

## Read-through

One last reading of the whole of `texts/DIR` for sense, for misreadings and misprints
together, after the comparison; no further pass with another aim (decided with the user for
`la`, 2026-11-05). The reader, la-el-agy, reads the text, not the images, and flags places;
it corrects nothing. The tools are in [scripts/README.md](scripts/README.md) ("The
read-through").

- **Steps** for each batch of 25 scans (`FIRST`–`LAST`):
  1. `uv run ocr/scripts/pages.py texts/DIR FIRST LAST -o tmp/read/FIRST-LAST.md` writes
     the pages for the reader; the task file names it and the TSV to write (page, the
     phrase as written, the reason).
  2. `ocr/scripts/findline.py` finds the lines of the flagged phrases in `ocr/DIR`; the
     rows of `misprints.tsv` for the batch's pages are looked up, so that a listed
     misprint is not listed twice.
  3. Each place decided ("Decisions"), in crops by `ocr/scripts/wordcrop.py ocr/DIR OUT.png
     PAGE:TEXT[:N]`, a zoom of the page where a letter is unclear. Before a place is
     decided printed or a misprint (learnt on `la`, la/PLAN.md, "Read-through"):
     - a quotation outside its main place (a lemma of a note, a verse quoted in a note or
       an essay) is compared with the main text, found by searching `ocr/DIR` for the
       phrase (`la` 1277 `al fuoco`, the verse on 0884 `el fuoco`);
     - a form that looks wrong on many pages is searched across the text before it is
       listed: it may be the edition's spelling (`la` `Eunce`);
     - a sentence that breaks off is checked in the image for the order of columns or
       blocks (`la` 0474, 0519, 0547, 0602, 1134).
  4. After the fixes: the convert script of the text and `misprints.py`, each compared with
     its previous output.
  5. The state in `ocr/DIR/PLAN.md` updated. Commits only when the user asks, after a range
     they set.
- **The reader's task** (basic rules only, not new ones each round): flag, do not correct;
  the edition's spellings are not errors; the printed punctuation is not normalized; no
  subagents and no git commands; the TSV written as a file (a script it runs takes `-o`, no
  shell redirection). On each reply the next batch is sent first, then the returned one
  decided; after the user switches the reader's model, wait for their signal; the model of
  each batch is recorded.
