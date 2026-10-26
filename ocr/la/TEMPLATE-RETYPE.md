<!--
Template for a retype task sent to la-el-agy (way B, Procedure step 6).
Copy to tmp/herdr-task-retypeNN.md and fill in:
- NN: the retype number (the last one was 58); N: the number of pages; PAGES: the list.
- "Background": the errors found in the last retype (word printed / word written, why),
  then what kind of pages this is and what the OCRs did wrong on them.
- "Notes per page": title pages, page heads, figures, ornaments, odd layouts; drop the
  examples that do not apply. Keep one layout example that matches the pages.
- Add the last retype's errors to "Errors made in earlier retypes" when they are a new kind.
Remove this comment before sending.
-->
# Task: retype N pages (ocr/la), retype NN

**From**: la-el-claude (a Claude Code agent), on behalf of the user.

## Background

The last retype (retype NN-1) was close to the print. One word was not as printed:

- `igualmente` for printed `equalmente`: the first letters misread and the word turned
  into another spelling. Read every letter of each word, even when the word makes sense
  without it.

Enlarge every mark at a word's end, copy an odd spelling as printed even when it looks
wrong, count the lines of every column against the image, and invent nothing.

This time N pages (KIND OF PAGES): **PAGES**.

In the OCRs of these pages, whole lines are lost, sentences rewritten, words replaced and
Latin spellings normalized (`coeli` for printed `celi`, `æ` and `ae` for printed `e`):
write only what the image shows. Notes per page:

- PAGE: the first page of a canto: the title `CAPITULUM …` (no page number printed), then
  the verse. In the commentary, the quotations that open each part (after `que incipit
  ibi:`) are followed by one blank line, with none before them.
- PAGE: a title page: an ornamental band at the top (not written), then the title lines,
  each followed by one blank line, then the text.
- PAGE: no blank line between tercets, although the print may space them.
- PAGE: the canto ends on this page; an ornament at the end is not written.
- PAGE: a word printed in an ornament (`FINIS`): a blank line, then the word; the ornament
  itself is not written.
- Wherever the page number stands after the running head, the page head is still: the
  number, a blank line, the running head. A page with no printed number starts with the
  running head. The `Digitized by Google` mark at the foot is not written.

Each page has (canto pages) the Italian verse, the gloss lines, the Latin verse, then the
two commentary columns (left column top to bottom, then the right one); (commentary pages)
the two commentary columns only. Copy every gloss mark with its number, in its place, with
a space before it, and count the glosses below against the marks.
- Do the pages one at a time, and write each page's file as soon as it is done, before
  starting the next. Do all N pages, then report once.
- A word printed at the right end of a verse line that belongs to the line above (a
  runover, `[quando`) goes on its own line right after the line it continues.

Take special care that every line of both commentary columns and of the verse is there
once, in its place and in order. After writing a page, count its lines per column against
the image.

**Errors made in earlier retypes of this kind (avoid them):**

- A period before a lowercase word: this edition often prints a period there (`dicit.
  et`); write what is printed (a comma there is not counted as an error, but do not guess:
  look at the mark).
- A colon written as a semicolon (`dicens: Etiam` became `dicens; Etiam`); and a space put
  before a colon (`dicens : Etiam`).
- Spellings normalized: `s'affrecta` became `s'affecta`, `Figluol` became `Figliuol`,
  `linto` became `liuto`, `havete` became `avete`, `mictit` became `mittit`, `opportet`
  became `oportet`, `fluminorum` became `fluminum`, `equalmente` became `igualmente`.
- Letters dropped or misread in a word that still makes sense: `contemplor` became
  `contempor`; `Dentro` became `Bentro` (and was reported as a misprint).
- An italic `v` read as `r` (`ritrovi`, `vedute`, `diverse` were first written with `r`):
  in the italic type `v` looks like `r` in the scan; read the same glyph the same way
  everywhere.
- Apostrophe gaps normalized: `che'nalzai` became `che 'nalzai`, `co'denti` became
  `co' denti`, `Com'a'Giuderi` became `Com'a' Giuderi`. Decide each gap by itself from the
  image.
- Leading spaces (indentation) at a paragraph start: write none.
- Lines lost at the top or bottom of a column or at a crop boundary, and a line written
  twice where two crops overlap.
- Printed tercet numbers deleted (Italian or Latin verse), or a signature mark at the foot
  deleted. Every tercet of the verse has its number: count them.
- Blank lines put between all the tercets of a page.
- A gloss mark written tight to its word: `(1)` always has a space before it.

Reminders: check the first and last line of every column and at every crop boundary; no
indentation; no blank line between tercets; enlarge every mark at a word's end; copy letters
as printed.

## Task

Retype pages **PAGES** from their images alone, one page at a time.

- Read each `ocr/la/PAGE.png` in parts: crops of each column, enlarged, so that every line
  is read (crops may be made with a script under `tmp/la-retypeNN/`).
- Write `tmp/la-retypeNN/agy/PAGE.txt` for each page.
- Layout of a canto page (shortened; note: no blank line between tercets):

```
194

INFERNI

7 Guardar l'un l'altro sotto nuova luna;
E sì ver noi aguzzavan le cigla,
Come 'l vechio sartor fa ne la cruna (1).
8 Sì adochiato da cotal famigla,
…

(1) dell'ago. — (2) del vestimento. — (3) o.

7 Respicere unus alium sub nova luna;
Et ita versus nos acuebant supercilia,
…

mus une aciei animarum, que veniebant prope aggerem,
et quelibet nos respiciebat, sicut consuevit de sero respi-
…
auctor ibant lente.

Facit comparationem de luna nova. Quando luna est co-
niuncta soli, non lucet nisi modicum; ideo tunc ambulantes
…
```

- Layout of a commentary page (shortened):

```
1220

CANTICA PARADISI

in quinto Methamorphoseos, fuit unus ex satiris caudatus,
qui, inventa fistula, quam Pallas proiecerat (quia cum in
…
quam tamen recedendo a linea eclyptica, que est in medio
zodiaci, cuius amplitudo extenditur duodecim gradibus, ita
…
```

## Rules

- Copy **letter by letter as printed**: the edition's spellings (Italian `decto`, `ochi`,
  `figlo`, `huomini`, `h` and `y` kept, `um` for `un`; Latin `michi`, `nichil`, `hystoria`,
  `Ytalia`, `e` for `ae`, `ci` for `ti`; `u` and `v` as printed), misprints, printed
  brackets (`mir[r]o`, `[non]`). Do not correct, modernize or complete from the sense; do
  not let the known poem, the other column or the verse above decide a word. Do not apply
  the typical spellings as rules either: write what each word shows. In the past,
  `liuto` was written for printed `linto`, `avete` for `havete`, `mittit` for `mictit`,
  `oportet` for `opportet`, and an italic lemma was copied from the verse instead of as
  printed (`Torcendo` for printed `Torciendo`): avoid this.
- A worn or broken letter is still that letter; report it, but write the letter. Count the
  stems of `m`/`ni`/`in`/`iu`/`un` and look for the dots.
- Punctuation as printed. A colon is two round dots; a semicolon has a dot above a comma,
  with a tail below the line; a comma has a tail; a period is a round dot. **A period
  before a lowercase word is common in this edition**: enlarge every mark at a word's end.
  Writing periods as commas and colons as semicolons was the most frequent error before.
  No space before `:` or `;`.
- Accents only where printed (small: look at each vowel); a speck is not an accent.
  `æ` only where printed. Use only Latin letters.
- **Apostrophe gaps**: a space after an apostrophe (or before `'l`, `'n`) only where the
  gap is as wide as the space between two words; the small white the apostrophe itself
  leaves is no space. Decide each one by itself.
- Tercet numbers in plain digits and a space (`16 Onde …`), on the first line of each
  tercet, as printed (also in the Latin verse); gloss marks `(1)` in plain digits with a
  space before (and after, if a word follows), always with both brackets. The gloss lines:
  ` — ` (em dash, a space each side) between glosses, only where printed; never `--`.
- A runover word (`[` at the right end of the column, the end of a too long verse line)
  goes on its own line, right after the line it continues; an inline bracket
  (`par[t]eggiando`) stays in the line.
- Small capitals in uppercase; italics not marked (no `*`, no `_`). In the italic type `v`
  looks like `r` in the scan: read the same glyph the same way everywhere.
- Page head on separate lines: the page number, a blank line, the running head (also where
  the number is printed at the right); a title sharing a printed line with the number: the
  title, then the number. Letter-spaced heads without the spaces. The rule under the head
  is not written. A page without a printed number starts with its first printed line.
- Canto pages: the Italian verse, a blank line, the gloss lines, a blank line, the Latin
  verse, a blank line, then the left commentary column top to bottom, then the right one.
  Read every verse line word by word in the image too.
- Commentary: one file line per printed line; a word broken at the line end keeps its
  hyphen; **no indentation** (no leading spaces); a new paragraph simply starts a new line.
- Blank lines: one where a short rule is printed between paragraphs or a wider gap between
  sections; a rule at the foot of the left column is a blank line after its last line;
  none at the change of column without a rule, none between ordinary paragraphs; a rule at
  the foot of the right column (the end of the page) is not written. **A rule is an empty
  line, never `—`**; a dash printed in the text is text.
- A page of running prose (an essay, in one or two columns, left column first): one file
  line per printed line, hyphens kept; the title (if printed), then one blank line; after
  that **no blank line between paragraphs**, only one before and one after each quotation
  set off from the text (none inside a verse quotation, none at the change of column).
- Footnotes of a prose page: after a blank line, `(1) …` with plain digits, as printed.
- An ornament at the end of a canto or an essay is not written.
- Signature mark at the foot: its own line after a blank line. A figure: a line `[figure]`,
  each printed label on its own line, then a blank line.
- A letter that cannot be read: the best reading, listed in the report.

## Scope

- Read: only the images of the pages above (crops made with a script under
  `tmp/la-retypeNN/` are fine; delete nothing).
- Do not read any text of these pages: not `ocr/la/*.txt`, `ocr/la/glm-ocr/`,
  `ocr/la/tesseract/`, `texts/`, the other `tmp/` work directories (`tmp/la-mark7/`,
  `tmp/la-markup/`, `tmp/bak/`), nor any Dante text on disk or on the web. The
  transcription must come from the image alone, since it is checked against the other
  readings afterwards.
- Write: only the output files and crop images under `tmp/la-retypeNN/`, and the report
  `tmp/herdr-report-retypeNN.md`.
- No commit, push, delete or rename; stay inside the repository.
- **Do not use subagents; do all the work yourself.** (A subagent's tool calls need manual
  approval, and herdr drops your name when one runs.)
- Do not run git commands that change the repository or use the network (`pull`, `fetch`,
  `checkout`, `restore`, `stash`, …).
- Do not write shell redirections (`>`, `>>`) in commands; they need approval each time.
  Run Python with `uv run`.

## Report

Write `tmp/herdr-report-retypeNN.md`: for each page, the lines written (per column), the
words or letters you were unsure of (word and line), anything unusual (a figure, a damaged
area, a line cut by a crop). Report from the files you wrote. Then, once:

```
herdr agent prompt la-el-claude "Reply from la-el-agy: done, report in tmp/herdr-report-retypeNN.md"
```

A question before starting: `herdr agent prompt la-el-claude "Question from la-el-agy: ..."`,
then stop. Send the report once, then stop.
