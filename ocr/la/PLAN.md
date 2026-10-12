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

The work so far is committed in four steps:

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

| Scans | State | Commit |
|---|---|---|
| `0079`–`0103` | Verse completed and the GLM-OCR differences resolved (batch 1, by la-el-codex), checked by la-el-claude; the later delegate edits checked (commit 3). Not proofread letter by letter; the rule/blank-line pass is not done. | 1, 3 |
| `0104`–`0194` | Proofread letter by letter (by la-el-agy, chunks c6–c12); every change checked by la-el-claude in the images. 0162 and 0172 are blank pages. Exceptions below. | 1 |
| `0115`, `0141` | The delegate's small edits checked; the pages are not proofread. | 3 |
| `0128`, `0140` | Not changed by the delegate, not checked in the images. | — |
| `0195`–`0208` | Two passes by la-el-codex (c13, c13b) plus fixes by la-el-claude (0197 `Ammodo`, `circulecto`; 0201 `[in]`, `qu[em]libet`; 0204 `nobilia` ×2; 0208 blank lines after the indented lemma pairs); the edits checked (commit 3). The two-OCR marks resolved by the markup method (steps 1–4), every change checked in the image. Text that both OCRs read alike is not checked. | 3, 4 |
| `0108`, `0175` | `riconoscuto` and the space before a semicolon fixed (found while measuring). | 4 |
| `0209`–`0232` | Verse completed (batch 2) and the GLM-OCR differences followed (c4; c5 for 0209–0220, line by line), by la-el-codex; the edits checked (commit 3). Not proofread. | 3 |
| `0239`, `0263`, `0287`, `0357`, `0472`, `0513`, `0546`, `0561`, `0562` | Whole columns, verse blocks or footnotes missing from `ocr/la`, found by the GLM-OCR outlier check and restored from the images. The rest of these pages is not proofread. | 2 |
| other pages | Not touched since the transcriber's notes were deleted (commit `029b55c`). | — |

### Found during the check of commit 3, outside the edits (to do)

- 0091: `sedes:`, `habuisti;`, `infernales:`, `dixisti:` look like `sedes;`, `habuisti:`,
  `infernales;`, `dixisti;` in the scan (committed in commit 1); decide at 3×.
- 0085:81: one file line holds two printed lines (`magnanimus … et` / `hoc opus nobile
  fecit.`).
- 0231: the running head stands before the page number.
- Commas kept where the scan shows a dot (the open "commas" convention): 0089 `crescens,`,
  `octo,`; 0211 `alta,`; 0213 `plectitur,`, `scorta,`; 0224 `Imperatoris,`; 0231 `dicunt,`
  (an edit to `dicunt.` was reverted for consistency).
- 0208:63 `ruinosum`: the scan shows `rainosum`; taken as a damaged `u`.

## Standing rules

- Transcribe only from the images. Never copy from dante-corpus, other editions, memory, or
  GLM-OCR: this edition's Italian and Latin forms differ, and copying replaces them with
  common ones.
- Keep the print, misprints included (see "Suspected misprints"). Only damaged letters are
  restored (`ungu'atas` → `ungulatas`, 0143).
- Commits: `ocr/la` separately from `texts`.
- Temporary scripts take `-o OUT` and are run with `uv run`; no shell redirection.
- No local paths in repository files.
- Delegate tasks forbid subagents and any git command that changes the repository or uses
  the network (see texts/PLAN.md, "Delegated work").
- Paid API calls (`ocr/la_markup.py`, image questions) are run by the user. Never discard a
  saved answer, never repeat a call that cannot help, and test with fakes first.

## Conventions settled during the check

- **Page head**: the page number on the first line, a blank line, then the running head.
  Signature marks at the page foot stay.
- **Lines**: one file line per printed line. Paragraph-per-line pages (essays such as 0150,
  0161, 0171, 0196, 0206) stay so, with broken words joined (no `del- l'`).
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
  matters little to the text.
- **Commas**: a dot that should be a comma, with the comma tail lost in the scan, is
  taken as a comma (0112 and others; GLM-OCR also reads commas there). Decided from the
  context: a dot inside a running sentence is a comma.
- **Blank lines**:
  - at each printed rule;
  - at a section gap without a rule (0155);
  - after an indented lemma pair (0164, 0208);
  - not at a column change unless a rule stands there;
  - page-end rules are listed in `tmp/la-checks/pageend-rules.txt`.
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

### Step 1: markup (`ocr/la_markup.py`) — done for 0195–0208

```sh
uv run ocr/la_markup.py -m MODEL -o tmp/la-markup --save-usage PAGE...
```

- The LLM returns only a JSON list of differences (`line`, `end_line`, `ocr`, `glm`,
  `after`); the script places them, so it cannot alter the text.
- Each answer is checked: the right sides must give the words of GLM-OCR (line-end hyphens,
  hyphens after a letter and spacing around apostrophes ignored). On problems, a fixing call
  sends only the problem places; `-r` caps the calls a page (default 2). A rerun resumes from
  the saved answers (`NNNN.json`, `NNNN.r2.json`, …, all kept).
- Result for 0195–0208 (model `gpt-6-luna`): all 14 pages pass, 355 marks.
- Re-checked against the current `ocr/la` (`markcheck.py` on a copy, 2026-10-13): the edits
  of commit 3 removed 6 marks (0200 `Aliquod`; 0202 `philantropia`, `imbursat:`, `sotios`;
  0204 `vostr'arte`, `Methaphi-`) and changed only spacing on 0196: 349 marks. Output:
  `tmp/la-mark2/markup/`.

### Step 2: trivial marks (`tmp/la-checks/markpost.py`) — done for 0195–0208

Resolves to the left side, without the image:

- A-only page numbers and running heads (lines 1–3) and B-only `Digitized by Google`;
- A-only tercet numbers (digits at the start of a line of a verse block), only on pages where
  `tercets.py` reports nothing;
- A-only signature marks (the digits of the last line), only when the page 8 before or after
  ends with the number before or after (0151 `13` … 0239 `24`);
- differences only in spaces next to an apostrophe, spaces after punctuation, and a
  line-end hyphen on the left (against a hyphen, a space or nothing on the right). A space
  between two words (`quanto lor` / `quantolor`) goes to the image; a mid-line hyphen on the
  left (0207 `introy-tu`) is kept;
- `'` against `’`, `(¹)` against `(1)`;
- an A-only and a B-only mark with the same text (a line placed differently, such as the
  gloss line of 0204).

0195–0208 (349 marks, narrowed rules, 2026-10-13): 143 resolved (54 tercet numbers, 2
signatures, 31 spacing, 32 notes, 15 heads, 6 moved, 2 quotes, 1 Google), 206 left. Against
the first rules only `quanto lor` changed (now left for the image); `tercets.py` reports
nothing for 0195–0208. Output: `tmp/la-mark2/post/` and `post.log`; the answers in
`tmp/la-markup/` are not touched. (The first run, 144 of 355, is in `tmp/la-markup-post/`.)

### Step 3: image decisions — located for 0195–0208; deciding written, to be measured

**Locating** (`tmp/la-checks/marklocate.py`): line mapping by pixel profiles failed on pages
with verse blocks. Instead, the words around a mark (the left sides) are looked up in
Tesseract's word boxes:

- every context word votes for the place of the mark; near words weigh more, the mark's own
  words little (0200: the `ocr/la` gloss repeats a verse line, `Vedi ch'a ciò penso.`, and
  matching it sent the crop to the verse);
- the context is widened (6, 15, 30 words) while the place is not clear; an ambiguous place
  is settled by the order of the located marks around it;
- the crop is the printed line with its neighbours, at the scan's own resolution, widened
  along the row (Tesseract may cut a line into pieces) and 60 px at the sides (tercet
  numbers it missed).

0195–0208: 208 of 211 located (0195:19, 0203:50 and the end of the 0203:52 passage not).
An alignment check of the Tesseract line flags 20 (verse rows, runover lines, broken
words); all 20 and a random sample of 30 of the rest were at the right place in the crops.
Output: `tmp/la-markcrops/` (crops and `locate.tsv`); `marksheet.py` stacks crops into
sheets for looking through them. Re-run on the 206 marks of the narrowed step 2
(`tmp/la-mark2/crops/`, `locate.tsv`): 202 located, the same boxes as before; not located
0195:19, 0203:50, 0203:52 (`order`: 0203:49).

**Why crops**: a model shrinks a whole page (about 1900×2800) to roughly half its width, and
the tail of a semicolon (a few pixels) is lost. A crop keeps the scan's pixels. Enlarging
beyond them adds no information; whether it still helps the model is to be measured. What
the scan itself has lost cannot be recovered by any crop: such places are answered
"unreadable" and decided otherwise.

**Deciding** (`tmp/la-checks/markdecide.py`): one small call per mark, through llm7shi
0.24.0 (`images=`), a new `Client` per mark so that images do not pile up in the history:

- input: the crop (1×, or enlarged with `-k`), the passage around the place with the place
  shown as `⟦…⟧` (8 words a side, left sides), and the two readings as "Reading 1/2" in an
  order fixed by a hash of the mark, so the side (ocr/la or GLM-OCR) is not given away;
- answer: the printed text first (`reading`), then `1`, `2`, `neither`, `unreadable`,
  `wrong place`; mapped back to `left`/`right` in the TSV;
- not asked: marks not located and A-only runs over a line or more than 8 words (GLM-OCR's
  dropped passages: 4 on 0195–0208);
- each answer saved as `PAGE-LINE-K.kK.MODEL.json` and reused on a rerun; `--fake` answers
  without calling (`.fake.json`); `-n` caps the new calls, `--only` lists the marks to ask.

Tested with `--fake` on 0195–0208 (199 questions; the hash puts side 1 on the left 103
times) and on the labelled set; the `images=` path (a `Path` at 1×, bytes at 3×) checked
through llm7shi's message conversion. No paid call yet.

**Labelled set** (`tmp/la-label/`, by `labsample.py` from `mkmarks.py` against
`314883d` for 0104–0194; the left side is the checked text, so the right answer is always
`left`): short marks (one line, ≤3 words a side), sampled by class with seed 1: colon 40,
comma 15 (a dot read in the scan; the "commas" convention, so `right` may be the scan's
truth), punct 30, letters 50; 133 located (`lablocate.tsv`, `labcrops/`). Plus the 15
suspected misprints above as `{{printed|expected}}` (`labm/`), to measure whether the model
reports the print. Scored by `markscore.py LABELS.tsv DECIDE.tsv... -o OUT`.

**Measured** (model `gpt-6-luna`, 2026-10-13; answers in `tmp/la-label/ans/`, scores in
`tmp/la-label/score-*.txt`):

| Set | Result |
|---|---|
| letters, 1× | 45/48; wrong: `flammæ` for printed `flamme`, and in 0108 the print had neither side (`riconoscuto`, fixed in `ocr/la`) |
| punct, 1× | 24/28; wrong: an accent added (`solvitís`); the rest are conventions (`³⁶`/`36`, `'`/`’`, the line-end hyphen of a paragraph-per-line page) |
| comma, 1× | 9/14; the other 5 read the dot that the scan shows (the commas convention) |
| colon, 1× / 3× / 8× tight crop | 33/40, 32/40, 36/40; every error a faint semicolon tail read as `:`; the answers change between runs |
| misprints, 1× / 8× / 8× without passage | 9/15, 9/15, 7/15: the model reads the common form (`Dedit` for printed `Ledit`, `nova` for `nora`) |

The 8× crops (`tightcrop.py`: the word, enlarged by nearest neighbour) and `--no-passage`
did not help; they are kept only as a record. A context rule for `:`/`;` (naive Bayes on
the neighbouring words, trained on 0104–0194, cross-validated by page) is right 70% of the
time, 87% for the 23% it is most sure of; it called all 4 true colons of the colon set `;`.

**Decided routes** for the marks left after step 2:

| Mark | Decided by |
|---|---|
| `:` against `;` only | the context rule; no image, no model; errors accepted |
| `.` against `,` only | la-el-claude, from the context (no image) |
| letters | the model (1× crop) and Tesseract's word: taken when both pick the same side; else la-el-claude in the image (labelled: 46 of 63 taken, 1 of them wrong) |
| other punctuation, accents | the model; when it picks the side with an added accent, la-el-claude in the image |
| not located; GLM-OCR's dropped passages | la-el-claude in the image |

### Step 4: apply and verify — done for 0195–0208

`tmp/la-checks/markroute.py` routes the marks (`route.tsv`); la-el-claude's decisions go
into `mine.tsv` (`left`, `right`, or `text:` with the printed text), replacements after
resolving into `fixes.tsv`; `tmp/la-checks/markapply.py` resolves them into
`tmp/la-mark2/out/`, then the pages are copied to `ocr/la` and the word diff is checked.

0195–0208 (206 marks after step 2): rule 6, model 174 asked; taken from the model 112
(the `left` ones unchecked, as decided); to la-el-claude 82 (comma 6, one-sided or not
located 20, model and Tesseract differing 33, accent added 21, model `neither` 8). Every
decision that changes `ocr/la` was checked in the image: of the model's 32, 7 were wrong
and reverted (0202 `eo` and 0208 `eos` read `co`, `cos`; five 0208 tercet numbers given a
dot that the print lacks).

What the check showed:
- In la-el-claude's share the model was wrong in about a third of the letter marks,
  mostly by normalizing (`rispettivi` for printed `respettivi`, `Anmodo`, `corum`,
  `quizzant`, `illuc`); Tesseract shares GLM-OCR's c/e errors (`Tune`, `adhue`, `co`), so
  agreement of the two is not proof, and the `right` decisions must all be checked.
- GLM-OCR's dropped passages hid ocr/la errors (0203: `Nonne quid` for `Numquid`,
  `consilia tione`, two commas), and ocr/la dropped words at a line start that GLM-OCR has
  (0199 `Venimus super`, 0200 `Fili mi,`, 0202 `quo`).
- Tercet numbers written `1.` by GLM-OCR against `1` are not trivial in step 2 yet: add
  them to the `number` rule.

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

1. Promote into `ocr/` the scripts of the method that stay in use: `markpost.py`, `marklocate.py`, `markdecide.py`, `colrule.py`, `markroute.py` and
   `markapply.py` (Tesseract's command in the docstrings without local paths). The
   measuring tools (`tightcrop.py`, `labsample.py`, `markscore.py`) stay in `tmp/`.
2. The same for 0209–0232, 0115, 0141 (and 0128, 0140); then the letter-by-letter
   question for 0079–0103.
3. The rule/blank-line pass for 0079–0103 and 0209–0232, including 0225's trailing `—` line
   and the blank before `Similiter sicut illi` on 0228.
4. Final checks: tercets, rules; search for `æ`, accents and `—`; line counts.
5. `texts/convert_la.py` (normalizing `’`), the READMEs, texts/PLAN.md (status, a pointer
   here), and the commits.
6. Then decide whether batch 3+ uses the same method.

## Tools

In `tmp/la-checks/` (not in the repository), all run with `uv run`, output with `-o`:

- **Markup**: `markcheck.py OUTDIR PAGE -o OUT` (re-checks saved answers without the LLM;
  it rewrites `OUTDIR/PAGE.txt`, so run it on a copy), `markstats.py DIR PAGE... -o OUT`
  (classifies the marks), `markpost.py`, `marklocate.py`, `marksheet.py`, `markdecide.py`
  (above).
- **Measuring the decisions**: `labsample.py DIR PAGE... -d OUTDIR -n CLASS=N... -o OUT.tsv`
  (samples labelled marks by class), `markscore.py` (above).
- **Images**: `ov.py` (1/3 overview with 0.05 ticks), `mag.py PAGE TOP BOTTOM LEFT RIGHT -k K`
  (zoom), `strips.py` (full-resolution strips), `thirds.py` (0.8 scale; not reliable for
  `:`/`;`), `vcrop.py`.
- **GLM-OCR comparison**: `align.py`, `realdiff.py` (ignores brackets, so `qu[em]libet` was
  missed), `onesided.py`, `laverse.py`, `glmverse.py`.
- **Structure**: `tercets.py`, `rules.py` (often misses right-column rules), `ruleshots.py`,
  `setblanks.py`, `gaps.py` (`columns()`/`lines()`), `pageend-rules.txt`.
- **Edits and diffs**: `fix.py`, `subs.py PAGE OLD NEW` (a unique replacement), `worddiff.py
  BASE PAGE... -o`, `colons.py BASE PAGE... -o`, `glmchk.py WD -o`, `vsbase.py`, `own.py`,
  `added.py`, `unlisted.py`.
- **Checking edits against a base** (used for commit 3): `mkmarks.py BASE PAGE... -d DIR -o
  OUT.tsv` (the changes as `{{new|old}}` marks, classed as `wdclass.py` does, so that
  `marklocate.py` crops them), `blockdiff.py DIR PAGE... -o` (large added blocks aligned with
  GLM-OCR, only the differing words listed), `zoomsheet.py LIST.tsv -o` (crops of listed
  words, enlarged, in one sheet), `wordcrop.py`.
- **Survey and work lists** (texts/PLAN.md, step 1): `survey3.py`, `an9.py`–`an11.py`,
  `lang.py`, `worklist.py`, with `pages9.json`, `pages10.json`, `survey3.json`.

Working data in `tmp/`: `la-markup/` (the paid LLM answers; keep), `la-markup-post/`,
`la-tess/` (now also 0104–0194), `la-markcrops/` (first run), `la-mark2/` (0195–0208 after
commit 3: `markup/`, `post/`, `crops/`, `locate.tsv`), `la-label/` (the labelled set; paid
answers go in `la-label/ans/`; keep).
