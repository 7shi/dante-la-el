<!--
Template for a retype of ocr/en-oelsner (ocr/en-oelsner/PLAN.md, step 1). Claude retypes the
pages itself (PLAN.md, "Decisions for this text"); the template gives the conventions
and, if the user switches to la-el-agy, the task to send. For la-el-agy, copy it to
tmp/herdr-task-en-oelsner-retypeNN.md and fill in:
- NN: the retype number (01 is the trial); N: the number of pages; PAGES: the list.
- "Background": from retype 02 on, the errors found in the last retype (word printed /
  word written), in one or two lines; drop the paragraph for the trial.
- "Errors made in earlier retypes": add the last retype's errors only when they are a new
  kind. Keep the rules basic: no new detailed rules each round.
Remove this comment before sending.
-->
# Task: retype N pages (ocr/en-oelsner), retype NN

**From**: la-el-claude (a Claude Code agent), on behalf of the user.

## Background

The book is the Temple Classics Inferno (London, 1903): the Italian on the even pages,
Carlyle's English prose on the odd pages, tercet by tercet, with the editor's marginal
labels and notes. Each page is retyped from its image alone; the retype is then compared
word by word with the existing transcription and with Tesseract by a script, and every
difference is decided in the image. A word copied exactly as printed, even when it looks
wrong, is what helps; a word corrected or normalized is a new error.

The last retype (retype NN-1) was close to the print. Not as printed: `WORD` for printed
`WORD` (WHY).

This time N pages: **PAGES**.

**Errors made in earlier retypes of other books (avoid them):**

- Spellings normalized or modernized (`Figluol` became `Figliuol`, `havete` became
  `avete`); misprints corrected from the sense; the grammar's form written for the
  printed one.
- A colon written as a semicolon, a period as a comma.
- A speck read as a mark, an accent added to an Italian word that has none in the print.
- Letters misread in a word that still makes sense (`contemplor` became `contempor`).
- Lines lost at the top or bottom of the page or at a crop boundary, and a line written
  twice where two crops overlap.

## Task

Retype pages **PAGES** from their images alone, one page at a time.

- Read each `ocr/en-oelsner/PAGE.png` in parts: crops of the page, enlarged, so that every
  line is read (crops may be made with a script under `tmp/en-oelsner-retypeNN/crops/`).
- Write `tmp/en-oelsner-retypeNN/PAGE.txt` for each page, as soon as it is done, before
  starting the next. Do all N pages, then report once.
- After writing a page, check its first and last line, and the lines at every crop
  boundary, against the image.

An Italian page and an English page (a scheme, not real text):

```
4 INFERNO

**Proemio** the first verse of the Italian on this page
the second verse
…

73-75. A note, as printed at the foot of the page, its lines as printed, a word broken
at the line end keeps its hy-
phen.
```

```
CANTO I 5

**Dante** the English of the first tercet, its lines as printed,
broken where the print breaks them.

the English of the next tercet …
```

## Rules

- **Lines as printed**: every printed line on its own line, broken where the print breaks
  it; a word broken at a line end keeps its hyphen (`de-` / `serted`). No indentation.
- Copy **letter by letter as printed**: the edition's spellings in English and Italian
  (`Chè`, `giugne`, `colour`), its accents, and its misprints. Do not correct, modernize
  or complete from the sense, and do not let the known poem or translation decide a word.
  A worn or broken letter is still that letter: write it, and list it in the report.
- **Punctuation as printed**: a colon is two round dots, a semicolon a dot above a comma;
  enlarge every mark at a word's end. Dashes as printed (`—`).
- **Quotation marks and apostrophes curly**, as printed: `“ ” ‘ ’`. Not balanced: a
  quotation left open on the page stays open. In the Italian, a space after an apostrophe
  only where the print has one (`ch’ io`, `dell’ altre`): decide each by itself.
- **The running head** as printed, on the first line, with its page number (`4 INFERNO`,
  `CANTO V 57`, `12 NOTES`); a page number printed at the foot on its own last line. A
  printer's signature mark at the foot (`B`, `2 C`) on its own last line.
- **Marginal labels** (the editor's sidenotes, `Proemio`, `Selva oscura`, `Dante`,
  `The Carnal Sinners`): written once, whole, in bold at the start of the line where the
  label begins: `**Label** text of the line`.
- **Not written**: the tercet numbers in the margin of the Italian, the italics (no `*`,
  no `_`), rules and ornaments.
- **Blank lines**: one between paragraphs (the argument, each English tercet, each note, a
  heading); none between the lines of the Italian verse, except where the print leaves a
  space.
- **Footnote markers** as superscript digits where printed (`translation.¹`); the
  footnote at the page end as `1 text…`.
- **Maps, plates and tables**: every printed word, line by line, from the top down and from
  left to right; the names of a map one per line; a genealogical table by its entries.
- A letter that cannot be read: the best reading, listed in the report.

## Scope

- Read: only the images of the pages above (crops made with a script under
  `tmp/en-oelsner-retypeNN/crops/` are fine; delete nothing).
- Do not read any text of these pages or of this translation: not `ocr/en-oelsner/*.txt`,
  `ocr/en-oelsner/tesseract/`, `ocr/en/`, `texts/`, `Inferno/`, the other `tmp/`
  directories, nor any Dante text on disk or on the web. The transcription must come from
  the image alone, since it is checked against the other readings afterwards.
- Write: only the output files and crop images under `tmp/en-oelsner-retypeNN/`, and the
  report `tmp/herdr-report-en-oelsner-retypeNN.md`.
- No commit, push, delete or rename; stay inside the repository.
- **Do not use subagents; do all the work yourself.** (A subagent's tool calls need manual
  approval, and herdr drops your name when one runs.)
- Do not run git commands that change the repository or use the network (`pull`, `fetch`,
  `checkout`, `restore`, `stash`, …).
- Do not write shell redirections (`>`, `>>`) in commands; they need approval each time.
  Run Python with `uv run`.

## Report

Write `tmp/herdr-report-en-oelsner-retypeNN.md`: for each page, the number of lines
written, the words or letters you were unsure of (word and line), anything unusual (a
damaged area, a line cut by a crop). Report from the files you wrote. Then, once:

```
herdr agent prompt la-el-claude "Reply from la-el-agy: done, report in tmp/herdr-report-en-oelsner-retypeNN.md"
```

A question before starting: `herdr agent prompt la-el-claude "Question from la-el-agy: ..."`,
then stop. Send the report once, then stop.
