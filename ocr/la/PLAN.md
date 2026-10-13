# Plan: completing `ocr/la`

This is the plan and the state of the proofreading of `ocr/la`, the transcription of
Serravalle's translation and commentary (1891). The conversion into `texts/la/` (layout,
conversion notes, `convert_la.py`) is planned in [texts/PLAN.md](../../texts/PLAN.md)
("`texts/la/`"). That plan's "Procedure for `la`" describes the first method, delegation
by batches; this file records where that method got to and the method that replaces it.

## Goal

- Complete `ocr/la` for scans `0079`–`0232` (Inferno I–XIII, batches 1–2 of
  texts/PLAN.md):
  - the missing verse columns, transcribed from the images;
  - the commentary checked against the print, letter by letter.
- Then write `texts/convert_la.py`, run its checks, and update the READMEs and both plans.
- Batch 3 onward (`0233`–`1290`) is on hold until the method below has been proven on
  batches 1–2.

## State (2026-10-12)

The work so far is committed in seven steps:

1. **Checked pages** (`f4f5b28`).
2. **Outlier fixes** (`eadde5b`).
3. **Delegate edits checked** (`5ab4057`): the edits made by delegates after the last check,
   each checked in the images. A change that GLM-OCR also reads was accepted (that triage
   held in every chunk so far); the others (165 word changes, 77 punctuation changes, 66
   deletions, 62 blank-line or line-break changes), the added verse blocks and restored
   passages (aligned word by word with GLM-OCR, the differing words and the text absent
   from GLM-OCR read in the image) were looked at one by one. Wrong edits or wrong text in
   them were corrected (17 places, listed in the commit message), and 17 changes of
   apostrophe spacing were reverted to the file's spacing. Only the edits were checked:
   the text they did not touch is as unproofread as before.
4. **Markup method on 0195–0208** (`3cf7bad`, 2026-10-13; also `410ace9` for 0108 and 0175):
   see step 4 below.
5. **Markup method on 0209–0232, 0115, 0141** (`c9d1cc1`, 2026-10-13): the same.
6. **Markup method on 0079–0103** (`91a4c39`, 2026-10-13), then the printed lines
   (`611a5dc`): the same, and the line ends compared with Tesseract's.
7. **Rules and blank lines on 0079–0103 and 0209–0232** (`cf35bb3`): every page `la_check.py`
   listed looked at in the image.

| Scans | State | Commit |
|---|---|---|
| `0079`–`0103` | Verse completed and the GLM-OCR differences resolved (batch 1, by la-el-codex), checked by la-el-claude; the later delegate edits checked (commit 3). The two-OCR marks resolved by the markup method, every change checked in the image (0084: five passages `ocr/la` had dropped; 0079: signature `4`). Line ends compared with Tesseract's: 0083 and 0094 broken into printed lines, 0092's broken words joined. Text that both OCRs read alike is not checked. Blank lines checked against the rules (step 7). | 1, 3, 6, 7 |
| `0104`–`0194` | Proofread letter by letter (by la-el-agy, chunks c6–c12); every change checked by la-el-claude in the images. 0162 and 0172 are blank pages. Exceptions below. | 1 |
| `0115`, `0141` | The delegate's small edits checked; the two-OCR marks resolved by the markup method (no change). | 3, 5 |
| `0128`, `0140` | Not changed by the delegate, not checked in the images. | — |
| `0195`–`0208` | Two passes by la-el-codex (c13, c13b) plus fixes by la-el-claude (0197 `Ammodo`, `circulecto`; 0201 `[in]`, `qu[em]libet`; 0204 `nobilia` ×2; 0208 blank lines after the indented lemma pairs); the edits checked (commit 3). The two-OCR marks resolved by the markup method (steps 1–4), every change checked in the image. Text that both OCRs read alike is not checked. | 3, 4 |
| `0108`, `0175` | `riconoscuto` and the space before a semicolon fixed (found while measuring). | 4 |
| `0209`–`0232` | Verse completed (batch 2) and the GLM-OCR differences followed (c4; c5 for 0209–0220, line by line), by la-el-codex; the edits checked (commit 3). The two-OCR marks resolved by the markup method, every change checked in the image (0214: a trailing blank line dropped; 0227: the running head cut to `CAPITULU` restored with the page number, its duplicate before the Latin verse removed). Text that both OCRs read alike is not checked. Blank lines checked against the rules (step 7). | 3, 5, 7 |
| `0239`, `0263`, `0287`, `0357`, `0472`, `0513`, `0546`, `0561`, `0562` | Whole columns, verse blocks or footnotes missing from `ocr/la`, found by the GLM-OCR outlier check and restored from the images. The rest of these pages is not proofread. | 2 |
| other pages | Not touched since the transcriber's notes were deleted (commit `029b55c`). | — |

### Found during the check of commit 3, outside the edits (to do)

- 0208:63 `ruinosum`: the scan shows `rainosum`; taken as a damaged `u`.

## Standing rules

- Transcribe only from the images. Never copy from dante-corpus, other editions, memory, or
  GLM-OCR: this edition's Italian and Latin forms differ, and copying replaces them with
  common ones.
- Keep the print, misprints included (see "Suspected misprints"). Only damaged letters are
  restored (`ungu'atas` → `ungulatas`, 0143).
- Commits: `ocr/la` separately from `texts`.
- Python is run with `uv run`. Scripts for delegates take `-o OUT`, and their task files use no shell redirection (a redirect asks for approval each time).
- No local paths in repository files.
- Delegate tasks forbid subagents and any git command that changes the repository or uses
  the network (see texts/PLAN.md, "Delegated work").
- Paid API calls (`ocr/la_markup.py`, image questions) are run by the user. Never discard a
  saved answer, never repeat a call that cannot help, and test with fakes first.

## Conventions settled during the check

- **Page head**: the page number on the first line, a blank line, then the running head.
  Signature marks at the page foot stay.
- **Lines**: one file line per printed line. Paragraph-per-line pages (essays such as 0092,
  0102, 0150, 0161, 0171, 0196, 0206) stay so, with broken words joined (no `del- l'`); a
  paragraph broken by a column change keeps the break (0102 `mo-`, 0171 `per-`).
- **Small capitals**: in uppercase (`EXPOSITIO LIBRI`, `IOHAN.`), as in ocr/en.
- **Tercet numbers**: superscript, as printed; where the print has none (0099), none is
  added.
- **Brackets**: printed brackets stay as printed (`stet[era]t`, `qu[em]libet`). A runover
  verse word goes on its own line starting with `[`.
- **Punctuation**: no space before `:` or `;`. Apostrophe spacing as in the file. No accents
  added that the scan does not show.
- **Colon or semicolon**: in commits 1–3 decided on a crop at full resolution, enlarged; a
  semicolon has a comma tail, often faint. From the markup method on, a `:`/`;`
  disagreement of the two OCRs is decided by a context rule, not the image (see step 3):
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
  - not at a column change unless a rule stands there;
  - before a signature mark at the page foot;
  - not inside a verse quotation of an essay (0220);
  - page-end rules: 0097, 0099, 0107 (right column, after `scilicet,`), 0110 (right,
    after `influentia.`), 0121 (right, after `invicem.`): not written (no blank, no `—`;
    0225's `—` line dropped).
- **Gloss line `(¹) …`**: under the Italian block or under the Latin block (11+ pages have
  it under the Latin block); `convert_la.py` must accept both.
- **Curly `’`**: left in `ocr/la`, normalized by `convert_la.py`.

## Suspected misprints

The file keeps what is printed; whether to correct these is decided later. Line numbers
refer to `ocr/la/PAGE.txt` at the time of the check.

| Page | Line | Printed | Expected | Note |
|------|------|---------|----------|------|
| 0113 | 62 | `Ledit ventum:` | `Dedit ventum:` | Lemma of the Latin verse `Terra lacrymosa dedit ventum`; the image shows an `L`, and GLM-OCR reads `Ledit` too. |
| 0099 | 11, 14 | (no number) | `³²`, `³³` | The Italian tercets 32 and 33 have no number; the Latin column has `³²` and `³³`. |
| 0127 | 41, 82, 89 | `umanita`, `piu`, `finalita` | `umanità`, `più`, `finalità` | No accent visible in the scan, while other accents on the page (`è`, `poichè`) are clear. The file has the accents. |
| 0133 | 53 | `de quibus nora tu vis scire` | `nova` | Italic lemma; the image shows `nora`; the Latin verse has `nova`. |
| 0142 | 72 | `et regola et qualitas` | `regula` | Italic lemma; the image shows `regola` (the Italian form); the Latin verse has `Regula`. |
| 0135 | 105 | `verecumdabatur` | `verecundabatur` | Printed `m`. Possibly the edition's spelling. |
| 0136 | 26 | `ractus` (Latin verse 34) | `raptus` | `ct` for `pt` may be the manuscript's spelling. |
| 0138 | 81 | `morirer` | `morerer` | May be the manuscript's spelling. |
| 0144 | 78 | `illa umbra sit malus frustum` | `maius` | The image shows `malus` clearly; the sense needs `maius`. |
| 0146 | 6 | `Verrauno al sangue` | `Verranno` | `u` for the first `n` (a turned letter). |
| 0147 | 79 | `infra tres solos` | `soles` | The lemma (Latin verse 23) has `soles`. |
| 0150 | 20 | `si specchieranuo le coscienze` | `specchieranno` | `u` for the second `n` (a turned letter). |
| 0154 | 71 | `nuove traraglia` | `travaglia` | Italic lemma; `r` for `v`. |
| 0164 | 36 | `per que mostratur sibi civitas` | `monstratur` | Possibly the manuscript's spelling. |
| 0167 | 5 | `persona orgoglosa` | `orgogliosa` | Possibly the manuscript's spelling (cf. `Figluol`). |
| 0177 | 84 | `ad sinistrum fiancum` | `flancum` | The image shows the `fi` ligature; GLM-OCR and the earlier file had `flancum`. |
| 0188 | 62 | `honeste, honorabilis:` | `honorabiliter` | The sense (adverbs) needs `honorabiliter`. |
| 0204 | 41 | `te volre:` | `volve` | Italic lemma (Latin verse `te volve`); `r` for `v`, as 0154. |
| 0205 | 34 | `aranzare` | `avanzare` | Italic lemma; `r` for `v`. |
| 0208 | 58 | `quod lucus,` | `locus` | The sense needs `locus`. |
| 0189 | 54–55 | `re-` / `spondidi sibi` | `respondi` | Italic lemma; the Latin verse 17 has `Respondi`. |

## What the delegation taught

The batches of texts/PLAN.md were delegated through herdr: batch 1 and the GLM-difference
passes of batch 2 (c1–c5) to la-el-codex, the letter-by-letter chunks c6–c12 to la-el-agy,
c13/c13b to la-el-codex. Each chunk was checked by a word diff against a snapshot taken
before it, with the suspicious items checked in the images.

- **Reports are not reliable.** They listed passages as restored that were already there,
  changes that were not made, and once a verse found on no page of the chunk. Only the diff
  was used.
- **la-el-agy (c6–c12)**: word corrections, restored passages, column order and re-lining
  were nearly always right. Its errors:
  - printed colons made semicolons, about one in four of its `:`/`;` changes;
  - printed spellings normalized (`Figluol` → `Figliuol`, `che'nalzai` → `che 'nalzai`);
  - misprints "corrected" from the sense (`malus` → `maius`, `traraglia` → `travaglia`,
    `honorabilis` → `honorabiliter`);
  - spaces added before colons or after apostrophes; printed tercet numbers or signature
    marks deleted;
  - fewer than 20 items a chunk to correct, decreasing to 1–2 in c11–c12.
- **la-el-codex (c13, c13b)**: cautious but incomplete. It followed only the GLM-OCR
  differences, so errors shared by both OCRs (`Anmodo`, `circuleto`) and differences hidden
  in brackets were left.
- **Delegation by open-ended tasks is not continued.** The user prefers scripted
  processing; the questions that need judgement are made narrow and checkable (below).

## Sources for checking

- **GLM-OCR** (`ocr/la/glm-ocr/`, committed; run with its [Makefile](glm-ocr/Makefile)): an
  independent OCR of every page. It joins the lines of a paragraph, drops the Latin verse
  and many turnover lines (`[fenno?` 0165, `[suum dampnum.` 0100), sometimes a whole column
  (the right column of 0263), and has its own misreadings. A means of checking only.
  - Outlier check (`uv run ocr/check_outlier.py ocr/la/glm-ocr/*.txt`): runaway pages
    (loops, garbage) were fixed by hand from the images without looking at `ocr/la` (0046,
    0096, 0241, 0373, 0385, 0461, 0477, 0490). Pages that ended in a loop were cut at its
    start, so the text inside the loop is lost: 0357, 0513, 0561, 0562, 0647, 0791, 0884,
    1044, 1093, 1158, 1240, 1275, 1277, 1280, 1281, 1286. Trailing dots were removed from
    0392 and 1020.
  - The same check found pages where `ocr/la` lacks a column, a verse block or footnotes
    (the commit 2 pages above). `ocr/la` 1240 (no commentary) and 1286 (ends at
    `(Genesis`) look incomplete and are not fixed.
- **Tesseract** (`tesseract PAGE.png OUT -l lat+ita tsv`, run locally): used only for the
  word boxes, to locate a place in the image. Its readings are poor in general, but it does
  not normalize spellings (13 of the 15 suspected misprints read as printed), so for the
  letter marks of step 3 its word is a second vote beside the model.

## The method: two-OCR markup, then image decisions

`ocr/la` (Gemini 2.5 Flash) and GLM-OCR fail in different ways, so their disagreements point
to errors. Each disagreement is written into the page as `{{ocr|glm}}`: the `ocr/la`
reading on the left, the GLM-OCR reading on the right, one side empty for text found on one
side only. The text outside the marks is `ocr/la` unchanged, so resolving every mark to its
left side gives the page back exactly.

**Workflow** (the scripts in `ocr/`; WORK is a work directory in `tmp/`, TESS the directory
of Tesseract's `PAGE.tsv` files, e.g. `tmp/la-tess`):

```sh
uv run ocr/la_markup.py -m MODEL -o WORK/markup PAGE...   # paid: the marks
uv run ocr/la_markprep.py WORK PAGE... -t TESS            # steps 2-3: trivial marks, crops, ask.txt
uv run ocr/la_markdecide.py WORK -m MODEL                 # paid: the model's verdicts
uv run ocr/la_markresolve.py WORK -t TESS                 # routes; review.tsv; WORK/out/
# la-el-claude decides review.tsv in the images into WORK/mine.tsv (and WORK/fixes.tsv),
# then reruns la_markresolve.py, checks the word diff of WORK/out/, and adds --write
```

The paid calls are run by the user; saved answers are reused, so a rerun asks only for
what is missing. To re-check saved markup answers after `ocr/la` has changed, run
`la_markup.py -r 0` on a copy of WORK/markup (no call is made; the marked pages are
rewritten). Checked on 0195–0208: the scripts give the committed pages exactly.

### Step 1: markup (`ocr/la_markup.py`) — done for 0195–0208

- The LLM returns only a JSON list of differences (`line`, `end_line`, `ocr`, `glm`,
  `after`); the script places them, so it cannot alter the text.
- Each answer is checked: the right sides must give the words of GLM-OCR (line-end hyphens,
  hyphens after a letter and spacing around apostrophes ignored). On problems, a fixing call
  sends only the problem places; `-r` caps the calls a page (default 2). A rerun resumes from
  the saved answers (`NNNN.json`, `NNNN.r2.json`, …, all kept).
- 0195–0208 (model `gpt-6-luna`; answers in `tmp/la-markup/`): all 14 pages pass, 355 marks;
  349 after the edits of commit 3 (re-checked with `-r 0`).

### Step 2: trivial marks (`ocr/la_markprep.py`) — done for 0195–0208

Resolved to the left side without the image: page numbers and running heads, tercet numbers
(A only or `1`/`1.`, on blocks whose numbers are in order), signature marks, `Digitized by
Google`, spacing next to apostrophes and after punctuation and line-end hyphens (a space
between two words, `quanto lor` / `quantolor`, is not ignored; a mid-line hyphen, 0207
`introy-tu`, is kept), `'`/`’`, `(¹)`/`(1)`, and the same text placed differently.

0195–0208: 155 of 349 resolved, 194 left.

### Step 3: image decisions (`ocr/la_markprep.py`, `ocr/la_markdecide.py`)

**Locating**: line mapping by pixel profiles failed on pages with verse blocks. Instead,
the words around a mark are looked up in Tesseract's word boxes: every context word votes
for the place (near words weigh more, the mark's own words little: on 0200 the `ocr/la`
gloss repeats a verse line, and matching it sent the crop to the verse); the context is
widened (6, 15, 30 words) while the place is not clear; an ambiguous place is settled by
the order of the located marks around it. The crop is the printed line with its
neighbours, at the scan's own resolution. 0195–0208: all but 3 located, all at the right
place in the crops checked.

**Why crops at 1×**: a model shrinks a whole page (about 1900×2800) to roughly half its
width. A crop keeps the scan's pixels; enlarging (3×, or the word alone at 8×) did not help.

**Deciding**: one call per mark with a new `Client` (llm7shi 0.24.0, `images=`): the crop,
the passage with the place as `⟦…⟧`, the two readings in an order fixed by a hash, so the
side is not given away; the model writes the print first, then chooses.

**Measured** on labelled marks of 0104–0194 (the corrections of commit 1; model
`gpt-6-luna`, 2026-10-13; answers in `tmp/la-label/ans/`):

| Set | Result |
|---|---|
| letters | 45/48; wrong: `flammæ` for printed `flamme`, and in 0108 the print had neither side (`riconoscuto`, fixed in `ocr/la`) |
| punct | 24/28; wrong: an accent added (`solvitís`); the rest are conventions |
| comma | 9/14; the other 5 read the dot that the scan shows (the commas convention) |
| colon, 1× / 3× / 8× | 33/40, 32/40, 36/40; every error a faint semicolon tail read as `:` |
| misprints, 1× / 8× / 8× without passage | 9/15, 9/15, 7/15: the model reads the common form (`Dedit` for printed `Ledit`) |

A context rule for `:`/`;` (naive Bayes on the neighbouring words, trained on 0104–0194,
cross-validated by page) is right 70% of the time.

### Step 4: routes and resolving (`ocr/la_markresolve.py`) — done for 0195–0208

| Mark | Decided by |
|---|---|
| `:` against `;` only | the context rule; no image, no model; errors accepted |
| `.` against `,` only | la-el-claude, from the context (no image) |
| letters | the model and Tesseract's word: taken when both pick the same side; else la-el-claude in the image |
| other punctuation, accents | the model; when it picks the side with an added accent, la-el-claude in the image |
| one side only, not located, dropped passages, the model's `neither` | la-el-claude in the image |
| any model decision that changes `ocr/la` | confirmed by la-el-claude in the image (`mine.tsv`) |

0195–0208 (`tmp/la-mark2/`): rule 6, model 174 asked, 112 taken (80 of them keeping
`ocr/la`, unchecked); to la-el-claude 82. Of the model's 32 changes, 7 were wrong (0202
`eo` and 0208 `eos` read `co`, `cos`; five tercet numbers given a dot the print lacks; the
`1`/`1.` rule now resolves these). Compared with la-el-claude's reading of the 94 marks it
was shown, the model differed in 27 (about a third): mostly normalizing (`rispettivi` for
printed `respettivi`, `Anmodo`, `corum`, `quizzant`), and Tesseract shares GLM-OCR's c/e
errors (`Tune`, `adhue`, `co`).

0209–0232, 0115, 0141 (`tmp/la-mark3/`): 231 trivial marks resolved, rule 20, model 338
asked, 207 taken (all keeping `ocr/la`, unchecked); to la-el-claude 190 (34 commas, 156 in
the image or from the model's answer). Of the 18 changes the model and Tesseract agreed on,
3 were wrong (`si` for printed `sì`, `denota re'tur` for `denota[re]tur`, `codem`). Where
Tesseract disagreed, the model picked GLM-OCR's side 17 times, rightly only twice
(`fui[t]`, `decimo.`); the others were misreadings (`staute`, `Molo`, `Nibil`, `soffliò`,
`introtyu`). Both OCRs wrong: 0220 `ecclissi`. Also fixed: 0227 `dicat: Tu` (a difference
the markup missed), 0231 `dicebat,`, 0232 `E sì che`. The markup left 6 differences
unmarked (`la_markup.py` reports them as missed); 5 were artefacts of marks across a
line-end hyphen.

0079–0103 (`tmp/la-mark4/`): 311 trivial marks resolved, rule 13, model 177 taken (all
keeping `ocr/la`, unchecked), to la-el-claude 184 (31 commas). Of the model's 39 changes,
9 went against a convention (small capitals, superscript tercet numbers, broken words on
an essay page) or needed a `text:` form, and 2 were wrong (`compiunge`, `De'acie` from a
speck). Where Tesseract disagreed, the model picked GLM-OCR's side 10 times, rightly once
(`compaxione`). `ocr/la` had dropped words that GLM-OCR has: five on 0084 (`Tempus erat in
principio matutini: idest, incipiebat`, `secundum`, `in vere`, `magis aliis`, `daret`),
0086 `est`, 0087 `viam`, 0099 `hunc`, 0102 `umana`. Such a one-sided right reading comes
without its space or line break: decide it as `text: daret`, `text:⏎secundum`. Found after
the marks: 0083 `penitēre` (kept by the model), 0099 `iu-⏎ditium`, 0101 `at-` and `[est]`
(both OCRs).

Line ends: 0083 and 0094 had paragraph lines (Gemini joined the printed lines and dropped
the line-end hyphens). They were broken at Tesseract's line ends letter by letter, putting
the hyphen back inside a word, and a check of every line end against Tesseract's (a line
whose last word Tesseract reads only inside a line) found four more wrong breaks (0083,
0084, 0099, 0101); its other hits were Tesseract joining the two columns.

Beyond the marks: GLM-OCR's dropped passages hid `ocr/la` errors (0203: `Nonne quid` for
`Numquid`, `consilia tione`, two commas), and `ocr/la` dropped words at a line start that
GLM-OCR has (0199 `Venimus super`, 0200 `Fili mi,`, 0202 `quo`): these go in `fixes.tsv`.

### Known limits

- Errors shared by both OCRs (`Anmodo`, `circuleto`) are not marked. Proposed checks: a
  lexicon check (a rare form one or two letters from a common one, across all of `ocr/la`)
  and a lemma check (an italic lemma in the commentary against the Latin verse of the page).
- Italics are not transcribed: the quotations (lemmas) in the commentary are printed in
  italics, but neither `ocr/la` nor GLM-OCR marks them (GLM-OCR has `*…*` on one page
  only). They are not looked for in the images (too many to check): whether a passage of
  the commentary is a quotation is to be decided from the text alone (e.g. matched
  against the verse of the page, as the lemma check above), later.
- Line breaks and the Latin verse block are not covered by the markup (GLM-OCR joins lines
  and drops the Latin verse). They need a line-count check per column.

## Next steps

1. (done: the scripts promoted into `ocr/`; 0209–0232, 0115, 0141 by the markup method;
   0128 and 0140 are blank.)
2. (done: 0079–0103 by the markup method, `tmp/la-mark4/`; the steps, for the next
   batch:)
   - the user runs `uv run ocr/la_markup.py -m gpt-6-luna -o tmp/la-mark4/markup $(seq -f %04g 79 103)`;
   - `la_markprep.py tmp/la-mark4 PAGES -t tmp/la-tess` (a page whose marks do not give
     `ocr/la` stops it: compare and fix the page, e.g. a trailing blank line as on 0214);
     check the differences the markup reports as missed;
   - test `la_markdecide.py --fake`, delete the fake answers, then the user runs it with
     `-m gpt-6-luna`;
   - `la_markresolve.py`; decide `review.tsv` in `mine.tsv` (commas from the context, every
     model change checked in the image, letters where the model and Tesseract differ
     checked when the model would change `ocr/la` or the reading is doubtful) and
     `fixes.tsv`; the word diff of `out/` against `ocr/la`; `--write`; `la_check.py`;
     commit the pages, then PLAN.
3. (done: the rule/blank-line pass for 0079–0103 and 0209–0232, `cf35bb3`. Found on the
   way, for step 4: page heads out of order or incomplete on 0083 (no `29`), 0085, 0086
   (`INFERNI` before the Latin verse), 0097, 0210 (no `INFERNI`), 0215 (no `161`), 0216
   (no `162`), 0219, 0223 (no `169`), 0230. 0127 has no signature in the print.)
4. (done: the final checks, `27524e4`, `ec93079`. Page heads: numbers added on 15 pages,
   order fixed on 4, `INFERNI` added on 0210 and moved on 0086; the pages without a head
   are chapter openings, summaries, essays, blank pages and the chapter-end pages 0080
   and 0198. No `æ`; `—` only in gloss lines and 0081 `EXPOSITIO LIBRI. —`; accents: 0201
   `pòne`, 0092 `nè`, `sè` as the book's grave accents (`Bréholles` on 0232 stays). Line
   ends: lines over 68 characters outside the essays and gloss lines found two more pages
   of paragraph lines, 0131 and 0193, broken into printed lines (a check of every line end
   against Tesseract's lines gave too many false hits where Tesseract joins the columns).
   `la_check.py` still reports 0131 and 0165 (a Latin line starting with a printed `[`,
   `[Dicunt …]`, `[Et] dixi`, taken for a runover word) and 0100 (no numbers in 0099's
   print): not errors.)
5. `texts/convert_la.py` (normalizing `’`), the READMEs, texts/PLAN.md (status, a pointer
   here), and the commits.
6. Then decide whether batch 3+ uses the same method (run `tmp/tess.py` first;
   `ocr/la_survey.py --work FIRST LAST` gives the verse work list).

## Tools

- `ocr/la_markup.py`, `la_markprep.py`, `la_markdecide.py`, `la_markresolve.py`: the method
  above.
- `ocr/la_check.py FIRST LAST [-v] [-o OUT]`: tercet numbers (order, every third line,
  continuity across pages) and the section rules of the images against the blank lines
  (the rule count often misses right-column and page-end rules: look at a listed page).
- `ocr/la_survey.py [--cantos | --work FIRST LAST] [-o OUT]`: the survey of the verse
  blocks (texts/PLAN.md, step 1): which pages lack the Italian or the Latin column, per
  page, per canto, or as the work list of a batch. It reads dante-corpus as a dependency
  in `../dante-corpus` (README.md).

Working data in `tmp/`: `la-tess/` (Tesseract's words for 0079–0232), `la-markup/` (the
paid markup answers for 0195–0208; keep), `la-mark2/` (the work directory of 0195–0208:
answers, decisions, fixes), `la-mark3/` (the same for 0209–0232, 0115, 0141, with its
paid markup answers in `markup/`), `la-mark4/` (the same for 0079–0103; its `markup/` holds
the user's paid answers for 0079–0344, prepared ahead: keep), `la-label/` (the labelled set: paid answers and scores).
