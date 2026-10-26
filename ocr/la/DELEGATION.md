# Tasks delegated to la-el-agy (`ocr/la`)

From 2026-10-15 to 2026-10-20, la-el-claude sent la-el-agy (Antigravity CLI, through
herdr) 41 tasks on `ocr/la`, each written to a task file with a report file in return:

| Series | Tasks | Work |
|---|---|---|
| verse 0–1 | 2 | move misplaced Latin verse blocks (whole lines only); check the verse crops |
| verse 2–17 | 16 | transcribe the missing verse column from crops: a trial of 5 pages, 14 batches of 25 Italian pages (337 in all), 0836's Latin |
| gloss 1–5 | 5 | transcribe the gloss lines under the verse from bands (223 pages) |
| retype 1–18 | 18 | retype whole pages that had lost text: a trial of 6, batches of 10, two of 4 (commentary-only pages, the front matter); 164 pages |

The task and report files (in `tmp/`) were deleted on 2026-10-20; this file keeps what is
needed to write such a task again. The results of each batch (what was not as printed,
what was fixed) are in [PLAN.md](PLAN.md) ("Record of the preparation" and "Remaining work", items 1–2, 6).

## How a task is sent

- The task goes to a file (`tmp/herdr-task-<task>.md`); the agent gets one short prompt
  naming it (`herdr agent prompt la-el-agy "…"`). The reply arrives as a prompt to la-el-claude; do not poll. Corrections wait for the
  next task file.
- One batch at a time. After a trial, each next task starts with the feedback on the last
  batch: what was right, then every place not as printed with its page and word, then the
  rule it breaks. The rules of the last task are repeated, with any new one.
- Every batch is checked by script before it is used (below); the report is not trusted.

## Parts of a task file

1. **Title and sender**: `# Task: … (ocr/la), batch N`, `**From**: la-el-claude (a Claude
   Code agent), on behalf of the user.`
2. **Feedback** on the previous batch (see above).
3. **Background**: what the image shows (an 1891 edition; Dante's poem in this edition's
   own old spellings; Serravalle's Latin) and why it is transcribed.
4. **Task**: the page list in a code block; the image to read (the crop, or
   `ocr/la/PAGE.png` "in parts, crops of each column, enlarged, so that every line is
   read"); the output `tmp/…/agy/PAGE.txt`, one file per page; a layout example.
5. **Rules** (below).
6. **Scope** (fixed wording, adapted to the paths):
   - Read: only the images of the pages above (crops made with a script in the task's
     `tmp/` directory are fine; delete nothing).
   - Do not read any text of these pages: not `ocr/la/*.txt`, `ocr/la/glm-ocr/`, `texts/`,
     the other `tmp/` work directories, nor any Dante text on disk or on the web. The
     transcription must come from the image alone, since it is checked against the other
     readings afterwards.
   - Write: only the output files, crop images under the task's `tmp/` directory, and the
     report `tmp/herdr-report-<task>.md`.
   - No commit, push, delete or rename; stay inside the repository.
   - **Do not use subagents; do all the work yourself.** (A subagent's tool calls need
     manual approval, and herdr drops your name when one runs.)
   - Do not run git commands that change the repository or use the network (`pull`,
     `fetch`, `checkout`, `restore`, `stash`, …).
   - Do not write shell redirections (`>`, `>>`) in commands; they need approval each
     time. Run Python with `uv run`.
7. **Report**: for each page, the lines written (per column), the words or letters it was
   unsure of (word and line), anything unusual (a figure, a damaged area, a line cut by
   the crop). "Report from the files you wrote." Then, once:
   `herdr agent prompt la-el-claude "Reply from la-el-agy: done, report in tmp/herdr-report-<task>.md"`.
   A question before starting: `herdr agent prompt la-el-claude "Question from la-el-agy: ..."`,
   then stop. "Send the report once, then stop."

## Rules common to all transcriptions

- Copy **letter by letter as printed**: the edition's spellings (Italian `decto`, `ochi`,
  `figlo`, `huomini`, `h` and `y` kept, `um` for `un`; Latin `michi`, `nichil`, `hystoria`,
  `Ytalia`, `e` for `ae`, `ci` for `ti`), misprints, printed brackets (`mir[r]o`, `[non]`).
  Do not correct, modernize or complete from the sense; do not let the known poem, the
  other column or the verse above decide a word. Do not apply the typical spellings as
  rules either: write what each word shows.
- A worn or broken letter is still that letter (an `m` with a weak first stem; `animam`
  with a broken `m`); report it, but write the letter. Count the stems of `m`/`ni`/`in`/
  `iu`/`un` and look for the dots.
- Punctuation as printed. A colon is two round dots; a semicolon has a dot above a comma,
  with a tail below the line; a comma has a tail; a period is a round dot. **A period
  before a lowercase word is common in this edition**: enlarge every mark at a word's end.
  No space before `:` or `;`.
- Accents only where printed (small: look at each vowel); a speck is not an accent. `æ`
  only where printed. Use only Latin letters (a Cyrillic `г` once stood for `r`).
- **Apostrophe gaps**: a space after an apostrophe (or before `'l`, `'n`) only where the
  gap is as wide as the space between two words; the small white the apostrophe itself
  leaves is no space. Decide each one by itself.
- Tercet numbers in plain digits and a space (`16 Onde …`), on the first line of each
  tercet; gloss marks `(1)` in plain digits with a space before (and after, if a word
  follows), always with both brackets even where the print lost one.
- A runover word (`[` at the right end of the column, the end of a too long line) goes on
  its own line, right after the line it continues; an inline bracket (`par[t]eggiando`)
  stays in the line.
- Small capitals in uppercase; italics not marked (no `*`, no `_`). In the italic type `v`
  looks like `r` in the scan (`ritrovi`, `diverse`, `vedute`): read the same glyph the same
  way everywhere.
- A letter that cannot be read: the best reading, listed in the report.

## Rules by kind of task

**Verse from crops** (the missing column cut by `ocr/la_versecrop.py`): one file
line per printed line; leave out the running head, the rules, the gloss lines, the
commentary and the edge of the other column; a line cut by the crop is read in
`ocr/la/PAGE.png` and reported. The Latin verse (0836) takes the Latin wording of the
spelling rule and has no gloss marks.

**Gloss lines** (a band cut from the last verse lines into the commentary, full width):
one file line per printed line, from the first `(1)` to the last before the
rule, broken where the print breaks them; ` — ` (em dash, a space each side) between
glosses, also where it is printed short or broken, but only where one is printed. The
numbers (`3`/`5`/`8`/`6` look alike) are read one by one and written as printed even out of
order. If the band ends before the rule or shows no gloss, read `ocr/la/PAGE.png`.

**Whole pages** (`ocr/la/PAGE.png`):

- Page head on separate lines: the page number, a blank line, the running head (also
  where the number is printed at the right); a title sharing a printed line with the
  number: the title, then the number. Letter-spaced heads without the spaces. The rule
  under the head is not written.
- Canto pages: the Italian verse, a blank line, the gloss lines, a blank line, the Latin
  verse, a blank line, then the left commentary column top to bottom, then the right one.
  Read every verse line word by word in the image too: once the Latin verse was written
  as a translation of the Italian (1247).
- Commentary: one file line per printed line; a word broken at the line end keeps its
  hyphen; **no indentation** (no leading spaces); a new paragraph simply starts a new line.
- Blank lines: one where a short rule is printed between paragraphs or a wider gap
  between sections; a rule at the foot of the left column is a blank line after its last
  line; none at the change of column without a rule, none between ordinary paragraphs; a
  rule at the foot of the right column (the end of the page) is not written. **A rule is
  an empty line, never `—`**; a dash printed in the text is text.
- Signature mark at the foot: its own line after a blank line. A figure: a line
  `[figure]`, each printed label on its own line, then a blank line.
- Front matter (the documents, 0046–0050): `Doc. N.` and its date on two lines, a blank
  line before and after; the source note (`(Ex Arch. Vat. …)`) on its own line even when
  printed at the end of the last text line; a printed row of dots `. . . . .` (five, with
  spaces), dots after words ` . . . . .`; raised letters as plain letters (`IIII.or`),
  `ª` kept; the formulas repeat, so check each line against the image.

## Checking a batch

Each output is compared by script (scripts in `tmp/`, not kept), never taken on trust:

- Verse: against `ocr/la`'s other readings (GLM-OCR, Tesseract, the model's reading) and
  with `la_check.py` (tercet numbers); every word found in no other reading is looked at
  in the image.
- Gloss lines: the words in no other reading of the band (Tesseract, GLM-OCR, the old
  gloss lines) and the gloss numbers that differ.
- Whole pages: against GLM-OCR and the old `ocr/la` (every word that differs from both,
  every block one of them lacks, the verse with `la_check.py`), each hit in the image;
  then the page replaces the old one, its markup answers are redone and re-checked with
  `la_markup.py -r 0`.

## What la-el-agy got wrong

Few letters, but the same kinds of error batch after batch, so each task repeated them
with examples:

- **Periods written as commas** (most errors, up to 14 on one page, 1175), and colons
  written as semicolons; commas left out or added.
- **Misprints and old forms made into the expected word**: `liuto` for printed `linto`,
  `Thebanarum` for `Thebenarum`, `Cacume` for `Cachume` (from the Latin column), `avete`
  for `havete`, `mittit` for `mictit`, `oportet` for `opportet`; an italic lemma copied
  from the verse instead of as printed (0272 `Torciendo`).
- **Apostrophe gaps** both ways: first spaces where the print is tight, then, after the
  rule was stressed, none where printed.
- **Form**: indented paragraphs; rules written as `—`; the page head on one line; `--`
  for the gloss dash; tercet numbers left out of a whole page (0755); a runover word kept
  inline; no space before `(1)`.
- **Reports that do not match the files**: readings claimed that are not in the file,
  glosses and rule counts reported unlike the files. Only the files count.
- Specks read as accents or diaeresis (`nòi`, `dùbitar`, `radiïs`), ligature `fi` read as
  `t` (`tigluoli`), a work-up speck as `·`.
