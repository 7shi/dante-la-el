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

The work so far is committed in three steps:

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

| Scans | State | Commit |
|---|---|---|
| `0079`–`0103` | Verse completed and the GLM-OCR differences resolved (batch 1, by la-el-codex), checked by la-el-claude; the later delegate edits checked (commit 3). Not proofread letter by letter; the rule/blank-line pass is not done. | 1, 3 |
| `0104`–`0194` | Proofread letter by letter (by la-el-agy, chunks c6–c12); every change checked by la-el-claude in the images. 0162 and 0172 are blank pages. Exceptions below. | 1 |
| `0115`, `0141` | The delegate's small edits checked; the pages are not proofread. | 3 |
| `0128`, `0140` | Not changed by the delegate, not checked in the images. | — |
| `0195`–`0208` | Two passes by la-el-codex (c13, c13b) plus fixes by la-el-claude (0197 `Ammodo`, `circulecto`; 0201 `[in]`, `qu[em]libet`; 0204 `nobilia` ×2; 0208 blank lines after the indented lemma pairs); the edits checked (commit 3). Not proofread: sampled columns showed about 1 error in 15–20 lines. The test bed of the markup method (steps 1–2 done, step 3 started). | 3 |
| `0209`–`0232` | Verse completed (batch 2) and the GLM-OCR differences followed (c4; c5 for 0209–0220, line by line), by la-el-codex; the edits checked (commit 3). Not proofread. | 3 |
| `0239`, `0263`, `0287`, `0357`, `0472`, `0513`, `0546`, `0561`, `0562` | Whole columns, verse blocks or footnotes missing from `ocr/la`, found by the GLM-OCR outlier check and restored from the images. The rest of these pages is not proofread. | 2 |
| other pages | Not touched since the transcriber's notes were deleted (commit `029b55c`). | — |

### Found during the check of commit 3, outside the edits (to do)

- 0091: `sedes:`, `habuisti;`, `infernales:`, `dixisti:` look like `sedes;`, `habuisti:`,
  `infernales;`, `dixisti;` in the scan (committed in commit 1); decide at 3×.
- 0085:81: one file line holds two printed lines (`magnanimus … et` / `hoc opus nobile
  fecit.`).
- 0199:47 `circulum:` (print `circulum,`?) and 0205:46 `orizontam` (print `orizzontam`):
  also among the markup marks of 0195–0208.
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
- **Colon or semicolon**: decided only on a crop at full resolution, enlarged; a semicolon
  has a clear comma tail. A `:`→`;` change that GLM-OCR also reads as `;` was always right;
  one where GLM-OCR keeps `:` was wrong in most cases (c10: 5 of 7).
- **Commas**: a dot that should be a comma, with the comma tail lost in the scan, was
  accepted as a comma (0112 and others; GLM-OCR also reads commas there). Open to the
  user's decision.
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
  word boxes, to locate a place in the image. Its readings are poor and are not a third
  vote, though they are shown with the crop.

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

### Step 2: trivial marks (`tmp/la-checks/markpost.py`) — done for 0195–0208

Resolves to the left side, without the image:

- A-only page numbers and running heads (lines 1–3), tercet numbers and signature marks
  (digits at a line start), and B-only `Digitized by Google`;
- differences only in spacing and line-end hyphens (a mid-line hyphen on the left, as
  0207 `introy-tu`, is not ignored);
- `'` against `’`, `(¹)` against `(1)`;
- an A-only and a B-only mark with the same text (a line placed differently, such as the
  gloss line of 0204).

0195–0208: 144 of 355 resolved, 211 left. Writes to `tmp/la-markup-post/`; the answers in
`tmp/la-markup/` are not touched.

To do before relying on it:
- check the tercet numbers it resolves with `tercets.py` (it does not compare their values);
- limit the spacing rule to apostrophes, spaces after punctuation and line-end hyphens; a
  space inside a word sequence (`quanto lor` / `quantolor`) goes to the image.

### Step 3: image decisions — locating done for 0195–0208

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
sheets for looking through them.

**Why crops**: a model shrinks a whole page (about 1900×2800) to roughly half its width, and
the tail of a semicolon (a few pixels) is lost. A crop keeps the scan's pixels. Enlarging
beyond them adds no information; whether it still helps the model is to be measured. What
the scan itself has lost cannot be recovered by any crop: such places are answered
"unreadable" and decided otherwise.

**Deciding** (to write): one small call per mark, through llm7shi 0.24.0 (`images=`), a new
`Client` per mark so that images do not pile up in the history:

- input: the crop, the left and right readings;
- answer: `left`, `right`, `neither` (with the reading), `unreadable`, `wrong place`;
- possibly ask for the reading first and the choice second, to avoid anchoring on the
  options;
- record the answers in a TSV (`page`, `line`, `left`, `right`, `verdict`).

Measure first on a labelled set: the pages checked in commit 1 (0104–0194), where
`git diff 314883d f4f5b28` shows the corrections. Measure the
`:`/`;` decisions on crops at 1× against 3×.

**What stays with la-el-claude** (in the harness, looking at the images): the marks not
located, GLM-OCR's dropped passages (A-only over several lines; they need several crops),
and the answers `neither`, `unreadable`, `wrong place`. Expected about one in ten.

### Step 4: apply and verify (to write)

- Resolve the marks from the decisions into `ocr/la`; check that no `{{` is left.
- Re-run `tercets.py`, `rules.py` and the GLM-OCR diffs.
- Commit the checked pages.

### Known limits

- Errors shared by both OCRs (`Anmodo`, `circuleto`) are not marked. Proposed checks: a
  lexicon check (a rare form one or two letters from a common one, across all of `ocr/la`)
  and a lemma check (an italic lemma in the commentary against the Latin verse of the page).
- Line breaks and the Latin verse block are not covered by the markup (GLM-OCR joins lines
  and drops the Latin verse). They need a line-count check per column.

## Next steps

1. 0195–0208: re-run `markcheck.py` on a copy of the saved answers first: commit 3 changed
   0200, 0202 and 0204 after the markup was made; then narrow the step 2 rules; write the decision step; measure it on 0104–0194;
   decide the 211 marks; apply; check the leftovers in the images.
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
  (classifies the marks), `markpost.py`, `marklocate.py`, `marksheet.py` (above).
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
`la-tess/`, `la-markcrops/`.
