# Plan: checking `ocr/la` after its completion

This is the plan for `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), now that it is complete. The completed work (the verse, the two-OCR markup, the
batches, the retyping, the line checks and the conversion), the checks after it (check 1,
the verse check, the italics and check 2) and the read-through are recorded in [DONE.md](DONE.md); the
steps of the read-through, for the other texts, are under "Read-through".
The "procedure" steps and the "items" cited below are those of DONE.md. The conversion into
`texts/la/` is described in [texts/PLAN.md](../../texts/PLAN.md) ("`texts/la/`"). A short
account of the whole work, for checking the other texts, is in [SUMMARY.md](SUMMARY.md).

**A new session starts here**: read "State". The rules and conventions below are settled:
apply them, do not ask again.

## State (2026-11-08)

`ocr/la` is complete (`0001`–`1296`) and converted into `texts/la/001`–`110`. The checks
for errors that both OCRs share (check 1, the verse check, the italics, check 2) are done
(DONE.md); what they do not cover is under "Known limits".

The read-through ("Read-through") is done: 0001–1296 are read and decided (2026-11-05 –
2026-11-08; DONE.md, "Read-through", with the commits of each range); the trial pages 0601–0614 were read
again with the batches. `Eunce` (0799–0867) is the edition's spelling throughout
Serravalle's text (the editors print `Eu[n]ce` on 0867), so it is kept as printed. The
pages after the index (1291–1296) are blank or the library's, with nothing to read.

The misprints are marked in the pages ("Misprint marks", 2026-11-08): 1,050 marks
`{{printed|fixed}}` in 580 pages, listed with 3 unapplied rows in `misprints.tsv`, which
replaces the table "Suspected misprints"; `texts/la` has the fixed side. A `{{…|…}}` in
`ocr/la` is a misprint mark. The old markup's `{{ocr|glm}}` (DONE.md, "The method") lived
only in work copies in `tmp/`, never in a committed page, and its scripts are retired: on a
marked page `markprep.py` stops at its assert and `markresolve.py` refuses to write.

## Checks

The checks list candidates by script, and every candidate is decided in the image
(`ocr/la/scripts/view.py word`), never from the sense or from another edition. A candidate is one of:

- **misread**: `ocr/la` differs from the print; correct `ocr/la`;
- **printed**: `ocr/la` is as printed; a misprint is marked and listed ("Misprint marks"),
  a form of the edition (a spelling of the manuscript, a variant of the quotation) is only
  recorded;
- **other**: not a reading at all (a split word, a name, Italian in the Latin); recorded.

The decisions are kept in a table per check in `ocr/la/` (`page line form decision note`),
committed with the fixes: those of the checks done are described in DONE.md ("The checks");
the read-through's is `readcheck.tsv`, every flagged place with its decision (`misread`
with the old form in the note, `was …`; `misprint`; `printed`), sorted by page and line.

The misprints are gathered in `misprints.tsv` whatever found them (the markup, a check, by
chance); a `misprint` row of a table is also a row there, with its mark in the page.

## Read-through

Decided with the user (2026-11-05): one last reading of the whole of `texts/la` for sense,
for misreadings and misprints together. It is the final pass over the text: no further
pass with another aim is planned. It covers what the checks cannot see ("Known limits"):
a misreading into a common word (0085 `terret`), a rare word with no common neighbour, a
common spelling written for the rare printed one. The commentary has not been read whole
before: check 2, group 3, judged only its candidates. The same steps then serve
`ocr/en`, `ocr/en-oelsner` and `ocr/grc` ([SUMMARY.md](SUMMARY.md), "For the other texts").

- **Reader**: la-el-agy reads the text, not the images, and flags places; it corrects
  nothing. Every flagged place is decided in the image as above (misread, misprint,
  printed); a damaged letter is restored by the sense.
- **Done** (DONE.md, "Read-through"): the tools, the trial on 0595–0614, the batches of
  0001–1296.
- **Steps** for each batch of 25 pages (`FIRST`–`LAST`):
  1. `uv run ocr/scripts/pages.py texts/la FIRST LAST -o tmp/read/FIRST-LAST.md` writes the
     pages for the reader; the task file names it and the TSV to write (page, the phrase
     as written, the reason) ([ocr/scripts/README.md](../scripts/README.md), "The
     read-through").
  2. `ocr/scripts/findline.py` finds the lines of the flagged phrases in `ocr/la`; the
     rows of `misprints.tsv` for the batch's pages are looked up, so that a listed
     misprint is not listed twice.
  3. Decisions, each in the image (`ocr/scripts/wordcrop.py ocr/la OUT.png PAGE:TEXT[:N]`,
     a zoom of `ocr/la/PAGE.png` where a letter is unclear): a misreading is corrected in `ocr/la` with
     `ocr/scripts/txtfix.py` (`PAGE:LINE old new`); a misprint is marked in the page and gets
     a row in `misprints.tsv` ("Misprint marks"; "found by the read-through"); every decision
     is a row of `readcheck.tsv`.
     The settled readings: Serravalle's Latin, its grammar and his way of translating the
     verse are printed; so are the edition's Italian readings and a visible accent. An
     Italian verse that differs from Dante where the Latin shows the right reading, an
     accent missing with none visible, and a sure non-word are misprints. A line-end hyphen
     kept inside an essay line is a misreading.
     Before a place is decided printed or a misprint:
     - a quotation of the poem outside the verse (a lemma of the commentary, of the
       appendix 1271–1287, a verse quoted in an essay) is compared with the verse of the
       main text and its Latin, found by searching `ocr/la` for the phrase: 1277 `ne porta
       al fuoco`, first kept as printed for want of a verse beside it, has `el fuoco` on
       0884 (`portat ignem`), and the comment above it carries fire upward: a misprint;
     - a form that looks wrong on many pages is searched across the text before it is
       listed: 0799–0867 `Eunce` is the edition's spelling (`Eu[n]ce` on 0867), and the OCR
       had normalized it to `Eunoe` on 0810;
     - a sentence that breaks off or a paragraph that ends in mid-sense is checked in the
       image for the column order: a paragraph continued across columns had been put out of
       order on 0474, 0519, 0547, 0602 and 1134.
  4. After the fixes: `texts/scripts/convert_la.py` (no `NO NUMBER` line since the marks
     number 0099 ×2, 0363 and 0856), `ocr/la/scripts/seqcheck.py 79 1270` (0897 tercet 31
     unnumbered in print, its number a mark), `ocr/la/scripts/check.py 79 1287` and
     `ocr/la/scripts/misprints.py`, each compared with its previous output.
  5. The status in "State" is updated. Commits, `ocr/la` and `texts/la` apart, only when
     the user asks: after a range they set, not after each batch.
- **The other texts**, after `la`: the same steps, a trial of a few pages each, the images
  `ocr/{dir}/NNN.png`, the records in each `ocr/{dir}/`; what no check has read there is
  mainly prose (SUMMARY.md).
- **The reader's task** (basic rules only, not new ones each round): flag, do not
  correct; the medieval spellings (`michi`, `nichil`, `e` for `ae`) and the old Italian
  ones are the edition's and not errors; the printed punctuation is not normalized; no
  subagents and no git commands; the TSV written as a file (a script it runs takes `-o`,
  no shell redirection). Within a range the user has set, each batch is sent when the last
  one is decided; after the user switches the reader's model, wait for their signal.

## Misprint marks

Decided with the user (2026-11-08): the misprints are corrected in `texts/la`, while
`ocr/la` keeps the print with the correction beside it. Done the same day (steps below).

- **The mark**: `{{printed|fixed}}` in the page, the printed text on the left, so that
  every mark resolved to its left side gives the print back. A mark stays within one line
  and does not cross an italic mark (`*{{a|b}}*`, not `{{*a|*b}}`); a misprint over a line
  break is marked on each line (1031 `{{corrupti-|corruptibi-}}` / `lium`); an addition has
  an empty left side (0099 `{{|32}}`); a whole line is one mark (0133).
- **Reading it**: the scripts that compare `ocr/la` with the image or with Tesseract
  (`check.py`, `seqcheck.py`, `lexcheck.py`, `lines.py`, `lostcheck.py`, `ocr/scripts/findline.py`,
  `ocr/scripts/wordcrop.py`, …) take the left side: `unmark()` of `check.py`, `seqcheck.py`,
  `lostcheck.py`, `lemmacheck.py` and `survey.py` (and so `lines.py`, `lexcheck.py`,
  `italicmark.py`) resolves the marks before it removes the italic marks, and `findline.py`
  does the same; `wordcrop.py` reads Tesseract's words only. `texts/scripts/convert_la.py`
  takes the right side (`fixed()`), the vocabulary of its hyphen joins included.
- **The list**: `ocr/la/misprints.tsv` replaces the table "Suspected misprints", one row per
  mark: `page line printed fixed applied source note`.
  - `applied`: `yes`, the mark is in the page; `no`, listed only (the fixed form is not
    certain, as two readings equally possible), with the reason in `note`: 0138
    `morirer` (perhaps the manuscript's spelling), 0259 `tra loro e'l` and 0790 `'n qua`
    (the edition's wording not certain).
  - `source`, where the fixed form comes from, in this order: `page`, the Latin, the verse
    or the commentary of the same page; `edition`, the edition elsewhere, its spelling or
    plainly the word meant (a turned letter, a missing accent); `dante`, Dante's text, only
    where the edition does not decide it; `other`, a source named in the note (the
    Vulgate, 0613; the Gospel, 1243). The fixed form is in the edition's spelling (`el`,
    `chiamata`), never a modern one.
  - `ocr/la/scripts/misprints.py` checks that every `yes` row is one mark at its page and
    line, and every mark a `yes` row; with `--fix-lines` it writes the new line of a mark
    that has moved.
- **Conversion** (step 1): the 852 rows of the table gave 1,053 rows. A row with several
  places became one row per place; the place of each mark was found in its line, and where
  the table's line or phrase did not give it, decided by hand. Left out: 9 rows, 4 of them
  places already corrected as misreadings (0716 `tuuc`, 0630 `Figlinolo`, 0655 `Figlinol`,
  1182 `57`; 1042 `mici`, read `miei` in the image) and 5 that repeated another row (1264,
  0652 ×2, 0773); 31 places listed twice by two checks were merged (the fixed forms
  agreed). Two places that `ocr/la` had written in the fixed form are now the print with a
  mark: 0127 `{{umanita|umanità}}`, 0897 `{{|31 }}`. One fixed form differs from the table:
  0249 `comprehendidi` is `comprehendi` (a syllable doubled; Dante `s'i' ben m'accorsi`),
  not `comprehendisti`.
- **Checks** (step 4): `check.py` unchanged; `seqcheck.py` adds 0897 (its tercet 31 now
  unnumbered, as printed); `convert_la.py` has no `NO NUMBER` line any more, its runover and
  hyphen reports show the fixed words, and `HYPHEN_MISSING` is empty (0639 `vir`, 1165 `pere`
  are marks whose fixed side has the hyphen); the 0668 heading is `LA LIBERTÀ UMANA …`.
  `texts/la` resolved to the left side is `texts/la` before the marks but for 0127 and
  0897. 105 files of `texts/la` changed.
- **Steps** (all done):
  1. The table "Suspected misprints" converted into `misprints.tsv` by a script, the rows
     with several places split; `applied` and `source` decided row by row.
  2. The `yes` rows written into `ocr/la` as marks by a script, each place asserted.
  3. The scripts above and `convert_la.py` taught the marks; the check script.
  4. The checks of the read-through (step 4 there) compared with their previous output: no
     change but the marked words in `texts/la`.
  5. Commits apart: the scripts, `ocr/la` (pages, TSV, PLAN), `texts/la`.
  6. The place of the marks checked: the 729 marks placed by likeness (printed and fixed
     forms with a similarity of 0.7 or more), each line as printed and as fixed, read by a
     delegate in one task. 20 marks sat on the wrong words (0175 `pena` lost, 0599
     `voler voler`, 0426 the fix on `crepa` for `reo`, …); moved, with their TSV rows, the
     fixed forms unchanged. The checks of step 4 gave the same output.

## Standing rules

- Transcribe only from the images. Never copy from dante-corpus, other editions, memory, or
  GLM-OCR: this edition's Italian and Latin forms differ, and copying replaces them with
  common ones.
- Keep the print, misprints included: a misprint is marked `{{printed|fixed}}` ("Misprint
  marks"), its left side the print. Only damaged letters are
  restored (`ungu'atas` → `ungulatas`, 0143).
- Commits: `ocr/la` separately from `texts`.
- Python is run with `uv run`. Scripts for delegates take `-o OUT`, and their task files use no shell redirection (a redirect asks for approval each time).
- No local paths in repository files.
- The italic marks `*…*` are in `ocr/la`: a script that reads it removes them first
  (`unmark()`, as `scripts/check.py`), and a correction keeps them (a word corrected inside a
  run stays inside it).
- Delegate tasks forbid subagents and any git command that changes the repository or uses
  the network (see texts/PLAN.md, "Delegated work").
- Paid API calls (`ocr/la/scripts/markup.py`, `ocr/la/scripts/markdecide.py`) are run by the user. Never
  discard a saved answer, never repeat a call that cannot help, and test with fakes first.
  With a `gpt-` model, do not add `--save-usage`.

## Conventions settled during the check

- **Page head**: the page number on the first line, a blank line, then the running head.
  Signature marks at the page foot stay.
- **Lines**: one file line per printed line. Paragraph-per-line pages (essays such as 0092,
  0102, 0150, 0161, 0171, 0196, 0206) stay so, with broken words joined (no `del- l'`); a
  paragraph broken by a column change keeps the break (0102 `mo-`, 0171 `per-`).
- **Small capitals**: in uppercase (`EXPOSITIO LIBRI`, `IOHAN.`), as in ocr/en.
- **Tercet numbers**: plain digits (`1`, `2`, …), as printed; where the print has none
  (0099), none is added.
- **Brackets**: printed brackets stay as printed (`stet[era]t`, `qu[em]libet`). A runover
  verse word goes on its own line starting with `[`, directly after the line it ends
  (decided with the user, 2026-11-01), even where the print sets it on the row of the
  next line (0100 `[suum dampnum.` after `vel ad fugiendum`, not after `Quomodo ego…`):
  `convert_la.py` joins it to the line above. 16 that stood after the next line, or at
  the end of it (0411 `…non vides. [sum est,`), were moved: 0100, 0239 ×2, 0389 ×2, 0411,
  0416, 0439, 0444, 0456, 0457 ×2, 0472, 0556, 0642, 0648 (all 409 verse and prose
  `[…` lines of 0079–1270 looked at in the image).
- **Punctuation**: no space before `:` or `;`. Apostrophe spacing as in the file. No accents
  added that the scan does not show.
- **Gloss marks**: `word (1) word`, a space on both sides, none before a following
  punctuation mark or `)` (decided with the user, 2026-11-02). The print sets a mark after
  the word it glosses, with a space that shrinks to nothing in a tight line; 121 of the
  8,487 marks, set without a space (`ch'io (1)mi`, `uno(1)`, `n'(1)`), were spaced.
- **Colon or semicolon**: in commits 1–3 decided on a crop at full resolution, enlarged; a
  semicolon has a comma tail, often faint. From the markup method on, a `:`/`;`
  disagreement of the two OCRs is decided by a context rule, not the image (see "Image
  decisions"):
  the edition uses `:` also as a stop stronger than `;` (`…ad peccandum: et hoc…`, 35
  times `: et` in 0104–0194), so the choice cannot be fixed by sentence structure, and it
  matters little to the text. Applied also to 0091 (`sedes;`, `infernales;` changed;
  `habuisti;`, `dixisti:` kept), where the scan seemed to show the other mark.
- **Commas**: a dot that should be a comma, with the comma tail lost in the scan, is
  taken as a comma (0112 and others; GLM-OCR also reads commas there). Decided from the
  context: a dot inside a running sentence is a comma.
- **Blank lines**:
  - at each printed rule;
  - at a section gap without a rule (0155);
  - after an indented lemma pair or quotation (0164, 0208, 0094, 0095, 0222), not before it;
    this includes the quotations that open each part of a chapter's commentary (0104, 0116,
    0130, 0152, 0186, 0199);
  - not at a column change unless a rule stands there (0138, 0177, 0187, 0194);
  - before a signature mark at the page foot;
  - in an essay, before and after a quotation (0102, 0220), but not inside a verse quotation
    (0220; 0150, broken by `quando`, `e`), nor inside a sentence (0196);
  - page-end rules: 0097, 0099, 0107 (right column, after `scilicet,`), 0110 (right,
    after `influentia.`), 0121 (right, after `invicem.`): not written (no blank, no `—`;
    0225's `—` line dropped).
- **Gloss line `(1) …`**: in plain digits, under the Italian block or under the Latin block
  (11+ pages have it under the Latin block); `convert_la.py` must accept both.
- **Curly `’`**: left in `ocr/la`, normalized by `convert_la.py`.
- **Figures**: a line `[figure]` where the figure stands, then each printed label on a
  line of its own (column after column, top to bottom), a blank line after; headings
  that are not printed are not added (1245). The labels carry no italic marks, whatever
  their print (1044, 1245, 1247). 1044 and 1247 are in this form since their
  retyping.
- **Italics** (DONE.md, "Italics"; settled with the user, 2026-11-01 – 2026-11-04):
  - every italic as printed, marked `*…*`: the lemmas and translations of the commentary,
    the incipits, titles of works and sources abridged, quotations and emphasis in the
    essays and the front matter. Not marked: small capitals (`DROUILHET DE SIGALAS`), the
    figure labels, and a page wholly in italic (the dedication 0013–0014: its type, not
    an emphasis). Fidelity in every detail is not sought: marks set by the script's
    conditions are accepted where the image was not asked.
  - each line keeps its own pair (`*dedit ven-*` / `*tum*:`); `convert_la.py` joins a pair
    broken at a line end into one.
  - punctuation, a mechanical convention instead of the print: the stop that ends a lemma
    (`:`, `,`, `.`, `;`, `?`, `!`) and a closing `etc.` stay outside; punctuation inside the
    lemma stays inside (`*Quando Deus, sive amor divinus*:`), so a stop at a line end
    inside a run that goes on to the next line goes inside (`*… tristis rivus,*` /
    `*quando descendit …*`), but not where the line is a lemma paragraph of its own and
    the next line begins the next lemma (0110 `*… vociferando*:` / `*Vae vobis …*:`).
  - an Italian lemma and its Latin one side by side are two pairs (`*Mosse dapprima*.
    *Movit primitus*:`), as are two quotations; a source abridged is one pair, its inner
    periods inside (`*IV Sent., dist. XLV, cap. III. De officiis sepulturae*`), the period
    after its last letter outside.
  - roman beside or inside a run, as printed: the elided article `l'` (`l'*obscuratum*`),
    `sè` and `Nè` (their accent makes them measure italic), a gloss (`*vitatis partite*? (idest
    divise) *si …*`).
  - a mark cannot close after a digit (`unmark()` keeps a `*` after a digit: 1283 `154*`,
    printed), so an italic number at a run's end stays outside (0022 `*Flor*. 10.`).

## Suspected misprints

The table that stood here (852 rows, page, line, printed, expected, note) is now
`ocr/la/misprints.tsv`, one row per place, each place marked in its page ("Misprint
marks"). The table is in the history of this file before the marks (2026-11-08).

## Known limits

- Errors shared by both OCRs (`Anmodo`, `circuleto`, 0085 `terret`) are not marked by the
  markup method; the checks ("Checks" above, DONE.md) looked for them, within the
  limits below.
- Italics are marked from the slant measured by `ocr/la/scripts/italic.py`, and only the lines
  `ocr/la/scripts/italicmark.py` flags were decided in the image (some pages read whole: the
  notizie 0022, 0027, 0029, 0031, 0033–0038; DONE.md, "Italics"): an unflagged word measured wrongly may keep a wrong mark, and the
  punctuation at a run's edge follows the convention ("Italics" under "Conventions"), not
  the print. The 453 same-line `*a*. *b*` and `*a*: *b*` were decided by sense (DONE.md,
  "Italics", the same-line pairs read); the 332 a script took for an Italian and a Latin
  lemma were skimmed as a list, not read one by one. Not marked: the dedication 0013–0014 (wholly
  italic), the figure labels, an italic digit at a run's end.
- Check 2 lists a form found once or twice, near a form found at least 5 times: a
  misreading into a common word (0085 `terret` is a real word, printed on 0489), a rare
  word with no common neighbour, a common spelling written for the printed rare one
  (`mihi` for `michi`) and a misreading repeated three times or more are not candidates.
  Its group 3 (Tesseract read the form itself; 19,817 words, 0.8% misread in the trial) was
  read for sense by la-el-agy, not in the image: only the 185 words it flagged were looked
  at, so a misreading that still gives a sense (a real word, a name, a verse word) or that
  the reader passed over may remain. The read-through ("Read-through", done) read for what
  these checks leave; it does not see a misreading that reads well (an OCR normalization,
  an accent; DONE.md, "Read-through").
- Check 1 needs a lemma of 3 words with 2 equal to the verse, and a word within an edit
  distance of 2: 0154 `nuove traraglia` (2 words; the Latin verse has `travagle`, 3 edits)
  is not found.
- The Latin verse is not covered by the markup (GLM-OCR drops it). The verse check read
  every line of it, and of the Italian verse, again from the image (DONE.md, "Verse
  check"), each line by one reader; a word that the first OCR and the reader both read
  alike and wrongly is not found.
- `scripts/survey.py` ends a page's verse block at a gloss line it does not recognize (`(^1)`,
  or a gloss run over two lines), and then reports the Latin as missing (25 pages, "Record of the preparation").
- Line breaks and the Latin verse block are not covered by the markup (GLM-OCR joins lines
  and drops the Latin verse): the verse is completed before the markup (procedure, step 1),
  and line breaks are checked by `scripts/lines.py` (step 8).

## Sources for checking

- **GLM-OCR** (`ocr/la/glm-ocr/`, committed; run with its [Makefile](glm-ocr/Makefile)): an
  independent OCR of every page. It joins the lines of a paragraph, drops the Latin verse
  and many turnover lines (`[fenno?` 0165, `[suum dampnum.` 0100), sometimes a whole column
  (the right column of 0263), and has its own misreadings. A means of checking only.
  - Outlier check (`uv run ocr/scripts/check_outlier.py ocr/la/glm-ocr/*.txt`): runaway pages
    (loops, garbage) were fixed by hand from the images without looking at `ocr/la` (0046,
    0096, 0241, 0373, 0385, 0461, 0477, 0490). Pages that ended in a loop were cut at its
    start, so the text inside the loop is lost: 0357, 0513, 0561, 0562, 0647, 0791, 0884,
    1044, 1093, 1158, 1240, 1275, 1277, 1280, 1281, 1286. Trailing dots were removed from
    0392 and 1020.
  - The same check found pages where `ocr/la` lacks a column, a verse block or footnotes
    (the commit 2 pages above). `ocr/la` 1240 and 1286, which looked incomplete
    then, are complete in the image (checked 2026-11-05): 1240 has both commentary
    columns, and 1286 ends at `Et`, as printed, the text going on to the next page.
- **Tesseract** (`ocr/la/tesseract/`, committed; run with its [Makefile](tesseract/Makefile),
  `-l lat+ita`, only the words kept, in the columns block_num, par_num, line_num, left, top,
  width, height, text): used only for the word
  boxes, to locate a place in the image. Its readings are poor in general, but it does
  not normalize spellings (13 of the 15 suspected misprints read as printed), so for the
  letter marks of the image decisions its word is a second vote beside the model.

## Tools

The scripts are in `ocr/la/scripts/`, described in the order of use in
[scripts/README.md](scripts/README.md): the verse columns, the two-OCR markup, the page
checks, the checks after completion and the misprint marks (`misprints.py`). The
conversion into `texts/la/` is `texts/scripts/convert_la.py` (procedure, step 11).

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
