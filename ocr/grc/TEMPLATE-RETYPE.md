<!--
Template for a retype task sent to la-el-agy (ocr/grc/PLAN.md, step 1).
Copy to tmp/herdr-task-grc-retypeNN.md and fill in:
- NN: the retype number (01 is the trial); N: the number of pages; PAGES: the list.
- "Background": from retype 02 on, the errors found in the last retype (word printed /
  word written), in one or two lines; drop the paragraph for the trial.
- "Errors made in earlier retypes": add the last retype's errors only when they are a new
  kind. Keep the rules basic: no new detailed rules each round.
Remove this comment before sending.
-->
# Task: retype N pages (ocr/grc), retype NN

**From**: la-el-claude (a Claude Code agent), on behalf of the user.

## Background

The book is Constantine Musurus's Greek verse translation of Dante's Inferno, with his
notes (London, 1882), in polytonic Greek; the notes also quote Latin, Italian and French.
Each page is retyped from its image alone; the retype is then compared word by word with
the existing transcription and with Tesseract by a script, and every difference is
decided in the image. A word copied exactly as printed, even when it looks wrong, is what
helps; a word corrected or normalized is a new error.

The last retype (retype NN-1) was close to the print. Not as printed: `WORD` for printed
`WORD` (WHY).

This time N pages: **PAGES**.

**Errors made in earlier transcriptions (avoid them):**

- Accents and breathings changed: an acute for a grave or the reverse, a breathing on a
  capital read as a quotation mark, the iota subscript dropped or added (`ᾍδου` is
  printed with it and must keep it).
- Rare or archaic forms replaced by common ones (`λυπηρὸς` for printed `λυπρὸς`,
  `βραχέως` for `βραγχῶς`, `πρόνοος` for `πρόνους`); misprints corrected from the sense.
- Letters misread in a word that still makes sense, especially in proper names and in
  the canto numerals of the headings.
- A colon written as a semicolon, the upper dot `·` as a period or a semicolon; a space
  put before a mark where the print has none.
- Lines lost at the top or bottom of the page or at a crop boundary, and a line written
  twice where two crops overlap.

## Task

Retype pages **PAGES** from their images alone, one page at a time.

- Read each `ocr/grc/PAGE.png` in parts: crops of the page, enlarged, so that every line
  and every accent is read (crops may be made with a script under
  `tmp/grc-retypeNN/crops/`).
- Write `tmp/grc-retypeNN/PAGE.txt` for each page, as soon as it is done, before
  starting the next. Do all N pages, then report once.
- After writing a page, check its first and last line, and the lines at every crop
  boundary, against the image.

A verse page (a scheme, not real text):

```
18 ΩΔΗ Γ΄.
„The first line of the page, as printed.“
The second line
15 „The fifth line has its printed number before it,
…
Β΄ 2
```

## Rules

- Copy **letter by letter as printed**, with every accent, breathing and iota subscript
  as printed: Unicode polytonic Greek (`ἀ ἁ ὰ ά ᾶ ᾳ ᾍ`), never monotonic. Do not correct,
  modernize or complete from the sense, and do not let the known poem decide a word. A
  worn or broken letter is still that letter: write it, and list it in the report.
- **Lines as printed**: one printed line per line, broken where the print breaks it; a
  word hyphenated at a line end keeps its hyphen at the end of the line (`ποιή-` /
  `ματος`). No indentation. A line too long for the measure whose end is set on the next
  line, indented, is written as that next line.
- **Write everything printed on the page**: the running head and the page number as
  printed and where printed (`2 ΩΔΗ Α΄`, or `ΩΔΗ Α΄.` and `3` on two lines), the line
  numbers of the verse at the start of their line (`15 Πᾶν …`), the printer's signature
  mark at the foot (`Β΄ 2`), headings (`ΩΔΗ Α΄.`, `Εἰς ᾨδὴν Β΄.`). Not written: rules,
  ornaments, library stamps, italics (no `*`, no `_`).
- **Punctuation as printed**: the upper dot `·`, the Greek question mark `;`, the comma,
  the period, `!`, the dash `—`; a colon `:` only where two round dots are printed.
  Enlarge every mark at a word's end. The elision mark as `᾽` (`ἀλλ᾽`).
- **Quotation marks** as printed: `“` and `”`, and the `„` that opens a line inside a
  quoted speech (`„Ἀλλ᾽ ὀφείλω …`). Not balanced: a quotation left open stays open.
- **Numerals**: the Greek numeral sign as `΄` (`ΩΔΗ Α΄.`, `Ὠδ. Α΄, 35`).
- **Blocks** apart by one blank line: a heading, the argument of a canto, the verse, each
  note on the pages of notes, a footnote. A note begins with its line number as printed
  (`30. Πρὸς τί …`). An asterisk footnote as printed (`* …`).
- **Tables** (the corrigenda, `014`–`018`): a Markdown table, one printed row per line,
  cells apart by `|`, with a header separator row (`| --- | --- |`); an empty cell left empty.
- **Other languages** in the notes (Latin, Italian, French, Hebrew, Arabic) letter by
  letter as printed, with their accents; a script you cannot write, `[Hebrew]` and the
  like, listed in the report.
- A letter that cannot be read: the best reading, listed in the report.

## Scope

- Read: only the images of the pages above (crops made with a script under
  `tmp/grc-retypeNN/crops/` are fine; delete nothing).
- Do not read any text of these pages or of this translation: not `ocr/grc/*.txt`,
  `ocr/grc/tesseract/`, `texts/`, the other `tmp/` directories, nor any Dante text or
  translation on disk or on the web. The transcription must come from the image alone,
  since it is checked against the other readings afterwards.
- Write: only the output files and crop images under `tmp/grc-retypeNN/`, and the report
  `tmp/herdr-report-grc-retypeNN.md`.
- No commit, push, delete or rename; stay inside the repository.
- **Do not use subagents; do all the work yourself.** (A subagent's tool calls need manual
  approval, and herdr drops your name when one runs.)
- Do not run git commands that change the repository or use the network (`pull`, `fetch`,
  `checkout`, `restore`, `stash`, …).
- Do not write shell redirections (`>`, `>>`) in commands; they need approval each time.
  Run Python with `uv run`.

## Report

Write `tmp/herdr-report-grc-retypeNN.md`: for each page, the number of lines written, the
words or letters you were unsure of (word and line), anything unusual (a damaged area, a
line cut by a crop). Report from the files you wrote. Then, once:

```
herdr agent prompt la-el-claude "Reply from la-el-agy: done, report in tmp/herdr-report-grc-retypeNN.md"
```

A question before starting: `herdr agent prompt la-el-claude "Question from la-el-agy: ..."`,
then stop. Send the report once, then stop.
