<!--
Template for a retype task sent to la-el-agy (ocr/en/PLAN.md, step 1).
Copy to tmp/herdr-task-en-retypeNN.md and fill in:
- NN: the retype number (01 is the trial); N: the number of pages; PAGES: the list.
- "Background": from retype 02 on, the errors found in the last retype (word printed /
  word written), in one or two lines; drop the paragraph for the trial.
- "Errors made in earlier retypes": add the last retype's errors only when they are a new
  kind. Keep the rules basic: no new detailed rules each round.
Remove this comment before sending.
-->
# Task: retype N pages (ocr/en), retype NN

**From**: la-el-claude (a Claude Code agent), on behalf of the user.

## Background

The book is Carlyle's prose translation of Dante's Inferno, with the Italian text and his
notes (London, 1889). Each page is retyped from its image alone; the retype is then
compared word by word with the existing transcription and with Tesseract by a script, and
every difference is decided in the image. A word copied exactly as printed, even when it
looks wrong, is what helps; a word corrected or normalized is a new error.

The last retype (retype NN-1) was close to the print. Not as printed: `WORD` for printed
`WORD` (WHY).

This time N pages: **PAGES**.

**Errors made in earlier retypes of other books (avoid them):**

- Spellings normalized or modernized (`Figluol` became `Figliuol`, `havete` became
  `avete`); misprints corrected from the sense.
- A colon written as a semicolon, a period as a comma; a space put before `:` or `;`.
- A speck read as a mark, an accent added to an Italian word that has none in the print.
- Letters misread in a word that still makes sense (`contemplor` became `contempor`).
- Lines lost at the top or bottom of the page or at a crop boundary, and a line written
  twice where two crops overlap.

## Task

Retype pages **PAGES** from their images alone, one page at a time.

- Read each `ocr/en/PAGE.png` in parts: crops of the page, enlarged, so that every line is
  read (crops may be made with a script under `tmp/en-retypeNN/crops/`).
- Write `tmp/en-retypeNN/PAGE.txt` for each page, as soon as it is done, before starting
  the next. Do all N pages, then report once.
- After writing a page, check its first and last line, and the lines at every crop
  boundary, against the image.

A canto page (a scheme, not real text):

```
the English prose, one paragraph per line, with its markers where printed,¹ …

the first verse of the Italian on this page
the second verse
…

60. A verse note, as printed below the verse.

the end of a footnote continued from the page before, without a number …

1 The first footnote of this page …

2 The second footnote …
```

## Rules

- Copy **letter by letter as printed**: the edition's spellings in English and Italian
  (`Chè`, `fe’`, `giugne`), its accents, and its misprints. Do not correct, modernize or
  complete from the sense, and do not let the known poem decide a word. A worn or broken
  letter is still that letter: write it, and list it in the report.
- **Punctuation as printed**: a colon is two round dots, a semicolon a dot above a comma;
  enlarge every mark at a word's end. The print sets a thin space before `:` and `;`:
  write none (`word:`). Dashes as printed (`—`).
- **Quotation marks and apostrophes curly**, as printed: `“ ” ‘ ’`. Not balanced: a
  quotation left open on the page stays open. In the Italian, a space after an apostrophe
  only where the print has one (`ch’ io`, `ch’ivi`, `dell’ altre`): decide each by itself.
- **Prose**: one paragraph per line; no indentation. A word broken at a line end is joined
  (`ascend-` / `ing` → `ascending`), keeping the hyphen only where the word itself has one
  (`She-wolf`); the last word of the page, if broken, keeps its hyphen (`Grey-`).
- **Italian verse**: one verse per line, no blank line between tercets, no indentation.
- **Blocks** apart by one blank line: a heading, a paragraph block, the verse, a verse note,
  each footnote, a quotation set off in a note (a verse quotation one line per verse).
- **Verse notes** (printed below the verse, `60. Word, …`): as printed, with the number
  and the period.
- **Footnotes** at the end of the page: `1 text…` (plain digit and a space). A footnote
  continued from the previous page comes first, without a number.
- **Footnote markers** in the prose as superscript digits where printed: `wood;²`.
- **Not written**: the running head, the page number, the verse numbers in the margin, the
  rules, ornaments, italics (no `*`, no `_`).
- **Headings** as printed, each on its own line (`ARGUMENT.`, `CANTO I.`, a title of the front
  matter). Small capitals in running text in uppercase; the first word of a canto
  in normal case.
- **The index**: one entry per line, as printed (`— Name, xx. 10.`, a dash for a repeated name).
- A letter that cannot be read: the best reading, listed in the report.

## Scope

- Read: only the images of the pages above (crops made with a script under
  `tmp/en-retypeNN/crops/` are fine; delete nothing).
- Do not read any text of these pages or of this translation: not `ocr/en/*.txt`,
  `ocr/en/tesseract/`, `ocr/en-oelsner/`, `texts/`, `Inferno/`, the other `tmp/`
  directories, nor any Dante text on disk or on the web. The transcription must come from
  the image alone, since it is checked against the other readings afterwards.
- Write: only the output files and crop images under `tmp/en-retypeNN/`, and the report
  `tmp/herdr-report-en-retypeNN.md`.
- No commit, push, delete or rename; stay inside the repository.
- **Do not use subagents; do all the work yourself.** (A subagent's tool calls need manual
  approval, and herdr drops your name when one runs.)
- Do not run git commands that change the repository or use the network (`pull`, `fetch`,
  `checkout`, `restore`, `stash`, …).
- Do not write shell redirections (`>`, `>>`) in commands; they need approval each time.
  Run Python with `uv run`.

## Report

Write `tmp/herdr-report-en-retypeNN.md`: for each page, the number of lines written, the
words or letters you were unsure of (word and line), anything unusual (a damaged area, a
line cut by a crop). Report from the files you wrote. Then, once:

```
herdr agent prompt la-el-claude "Reply from la-el-agy: done, report in tmp/herdr-report-en-retypeNN.md"
```

A question before starting: `herdr agent prompt la-el-claude "Question from la-el-agy: ..."`,
then stop. Send the report once, then stop.
