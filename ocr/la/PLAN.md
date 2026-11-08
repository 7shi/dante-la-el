# Plan: checking `ocr/la` after its completion

This is the plan for `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), which is complete and checked. It holds what any further work on `ocr/la` needs:
the state, the decisions of a check, the settled readings, the misprint marks, the rules,
the conventions and the limits. The work done is recorded in [DONE.md](DONE.md), a short
account in [SUMMARY.md](SUMMARY.md); the work on the other texts is planned in
[ocr/PLAN.md](../PLAN.md). The "procedure" steps and the "items" cited below are those of
DONE.md. The conversion into `texts/la/` is described in
[texts/PLAN.md](../../texts/PLAN.md) ("`texts/la/`").

**A new session starts here**: read "State". The rules and conventions below are settled:
apply them, do not ask again.

## State (2026-11-08)

`ocr/la` is complete (`0001`–`1296`) and converted into `texts/la/001`–`110`. All the
checks are done (DONE.md): check 1, the verse check, the italics, check 2, the read-through
(0001–1296, 2026-11-05 – 2026-11-08) and the misprint marks (2026-11-08). No work is open;
what the checks do not cover is under "Known limits".

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

Decided with the user (2026-11-05) and done (DONE.md, "Read-through"): one last reading of
the whole of `texts/la` for sense, for misreadings and misprints together; no further pass
with another aim is planned. Its steps for a batch, and the reader's task, serve the other
texts and are in [ocr/PLAN.md](../PLAN.md) ("Read-through"). What is particular to `la`:

- **Settled readings**, for deciding a flagged place: Serravalle's Latin, its grammar and
  his way of translating the verse are printed; so are the edition's Italian readings and
  a visible accent. An Italian verse that differs from Dante where the Latin shows the
  right reading, an accent missing with none visible, and a sure non-word are misprints. A
  line-end hyphen kept inside an essay line is a misreading.
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
- **Checks after a fix**: `texts/scripts/convert_la.py` (no `NO NUMBER` line since the marks
  number 0099 ×2, 0363 and 0856), `ocr/la/scripts/seqcheck.py 79 1270` (0897 tercet 31
  unnumbered in print, its number a mark), `ocr/la/scripts/check.py 79 1287` and
  `ocr/scripts/misprints.py ocr/la`, each compared with its previous output.

## Misprint marks

Decided with the user (2026-11-08): the misprints are corrected in `texts/la`, while
`ocr/la` keeps the print with the correction beside it. A misprint found later is marked in
its page and gets its row in `misprints.tsv` at once.

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
  - `ocr/scripts/misprints.py ocr/la` checks that every `yes` row is one mark at its page and
    line, and every mark a `yes` row; with `--fix-lines` it writes the new line of a mark
    that has moved.
- **The old markup** `{{ocr|glm}}` (DONE.md, "The method") lived only in work copies in
  `tmp/`, never in a committed page, and its scripts are retired: on a marked page
  `markprep.py` stops at its assert and `markresolve.py` refuses to write. A `{{…|…}}` in
  `ocr/la` is a misprint mark.
- **Done** (DONE.md, "Misprint marks"): the table converted, the marks written and checked.

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
checks, the checks after completion and the misprint marks (`misprints.py`, now in
`ocr/scripts/`). The
conversion into `texts/la/` is `texts/scripts/convert_la.py` (procedure, step 11).

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
