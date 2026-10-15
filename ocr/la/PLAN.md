# Plan: completing `ocr/la`

This is the plan and the state of the proofreading of `ocr/la`, the transcription of
Serravalle's translation and commentary (1891). The conversion into `texts/la/` (layout,
conversion notes, `convert_la.py`) is planned in [texts/PLAN.md](../../texts/PLAN.md)
("`texts/la/`"); its batch table (step 2 of "Procedure for `la`") defines the batches used
here. That plan's delegation by batches was the first method; this file records where it got
to and the method that replaced it.

**Goal**: complete the rest of `ocr/la` (`0233`–`1296`, and the front matter `0001`–`0078`)
and convert it into `texts/la/`. The verse and the paid steps of the markup method
(procedure, steps 1–4) now run over all these pages at once; the review and the steps after
it (5–11) go batch by batch (batches 3–10, `0233`–`1270`, then the front matter and
appendix, batch 11).

**A new session starts here**: read "State" and "Remaining work", and go on from the first
open item. The conventions and rules below are settled: apply them, do not ask again.

## State (2026-10-15)

**Batches 1–2 (`0079`–`0232`, Inferno I–XIII) are complete**, and the procedure below is
established on them. `texts/la/008`–`020` are converted from them.

"Complete" means, for every page of 0079–0232 (0128, 0140, 0162, 0172 are blank):

- both verse columns present, with their tercet numbers checked by `la_check.py`;
- every disagreement of `ocr/la` with GLM-OCR resolved by the markup method, each change
  checked in the image (0104–0194 had also been proofread letter by letter before);
- blank lines checked against the printed rules, line breaks against Tesseract's lines,
  and dots before a lowercase word made commas (`la_lines.py`);
- the final checks (page heads, characters, accents, long lines) done.

Not covered (see "Known limits"): text that both OCRs read alike and wrongly (0085 `terret`
for printed `territ` was found by chance); italics are not transcribed. A full check of the
italic lemmas against the verse of their page, and a lexicon check, are proposed, not done.

**The rest (2026-10-14/15)**:

- **Markup** (paid, by the user) done for every page (`0001`–`1296`, 1234 pages without
  the 62 blank ones). Re-checked with `-r 0` (in a work directory `tmp/la-mark6/`, since
  deleted): 3843 differences reported as missed in 841 pages (890 of them spacing only),
  far more than on batches 1–2; 0941's answer is not valid JSON.
- **`la_markprep.py`** ran over 1074 pages (21371 questions for the model): fixed for a
  page file without a final newline (306 pages; the ending of `ocr/la` is kept), a vote
  peak outside Tesseract's words, and superscript digits taken for a signature. Nine pages
  stop it, because `{`, `}` or `|` in a text break the `{{…|…}}` marks (Remaining work,
  item 4).
- **Verse, misplaced Latin blocks** (by la-el-agy, checked): of the 74 pages that
  `la_survey.py` gave as Latin missing, 48 had the Latin block elsewhere on the page and it
  was moved (whole lines only; checked: the non-blank lines of each page are the same set);
  25 had it in place (`la_survey.py` false positives: glosses written `(^1)` or run over two
  lines end its verse block early, e.g. 0262, 0345); only 0836 lacks the Latin.
- **Verse, crops**: `ocr/la_versecrop.py` cropped the missing column of the 337 pages
  without the Italian and of 0836 (`tmp/la-verse/crops/`, `crops.tsv`); the crops whose
  line counts differed were checked by la-el-agy and la-el-claude, and the script fixed
  (bottom lines lost, the Italian cut where the two columns overlap, 0625).
- **Markup answers to redo**: the pages whose lines change (`tmp/la-verse-missing.txt`,
  386 pages: the 337 without the Italian, 0836, and the 48 with a moved Latin block) were
  moved, all their files, into `tmp/la-markup/bak/`; `tmp/la-markup/` holds the other 848.

Data ready (in `tmp/`, not in git; see "Tools"):

- `tmp/la-tess/`: Tesseract's word boxes for every page (`0001`–`1296`);
- `ocr/la/glm-ocr/`: GLM-OCR for every page (committed);
- `tmp/la-markup/`: the store of the user's paid markup answers, the latest set per page
  (848 pages; keep). See "Markup answers";
- `tmp/la-verse-missing.txt` (the 386 pages whose markup is to be redone),
  `tmp/la-verse-italian-missing.txt` (337), `tmp/la-verse-latin-missing.txt` (the 74 pages
  of the Latin step), `tmp/la-verse-inplace.txt` (the 25 false positives);
- `tmp/la-verse/crops/`: the crops of the missing verse columns.

## Remaining work

In this order (decided with the user, 2026-10-15):

1. **Verse transcription** (paid, `gpt-6-luna`): a new script sends each crop of
   `tmp/la-verse/crops/` and asks for the verse of the column as printed, line by line
   (tercet numbers, gloss marks `(¹)`, runover words `[…`), from the image only: no
   dante-corpus text in the prompt. The crops of the Italian can hold the edge of the Latin
   column (tercet numbers, first letters, e.g. 0709, 1090): the prompt says to leave it out.
   - **Trial first**: crop the Italian column of checked pages (0079–0232, both columns
     present; `la_versecrop.py` needs an option to crop a column that the file has),
     transcribe, and measure against `ocr/la`; then all pages.
2. **Verse check**: compare each transcription with GLM-OCR, which reads the Italian verse
   (as a check only); decide the disagreements in the image, as in the markup method (a
   crop per place, the model's verdict, la-el-claude for what changes the text). dante-corpus
   only points at places to look at: this edition's forms differ from it, and a difference
   is not a reason to change. 0836 (Latin, one page): la-el-claude checks it in the image.
   Then insert the blocks (Italian block, gloss line, Latin block; see the conventions) and
   run `la_check.py` (tercets) until it reports only known exceptions.
3. **Markup of the 386 pages** (paid) of `tmp/la-verse-missing.txt`, as procedure step 2,
   with the default rounds (the extra round of item 5 is for all pages together). The 48
   pages with a moved Latin block (`tmp/la-verse-moved.txt`) have both columns and can be
   marked before items 1–2:
   `uv run ocr/la_markup.py -m gpt-6-luna -o tmp/la-markup $(cat tmp/la-verse-moved.txt)`;
   the other 338 after the verse is inserted.
4. **Pages that stop `la_markprep.py`**: 0063 `{et}`, 0727 `{dicit}`, 0822 `{firmaret}`,
   0399 a `}}` line, 0458 and 1245 `|` (in `ocr/la`): check in the image and fix `ocr/la`
   (0458 and 0727 are among the 386, fix them before item 3); 0021 `||`, 0344 and 0467
   `$^{(1)}$` in GLM-OCR's side: make `la_markup.py` keep such text out of the marks, or fix
   the marked page by hand; 0941: no valid answer, call again.
5. **One more markup round** (paid, before the model decisions): rerun `la_markup.py` with
   `-r 3` on all pages, so that the pages with missed differences get a fixing call (the
   pages that pass make no call). Check what is still missed.
6. **Model decisions** (paid): a new work directory over all pages, `la_markprep.py`, then
   `la_markdecide.py` (procedure, steps 3–4).
7. **Batches 3–11**: procedure steps 5–11, batch by batch.

Also seen: 0848, 0891 and 0999 have backticks in the text (0891 around its blocks,
`` `Quei gloriosi …` ``), a transcription artifact to remove in their batches.

## Procedure for a batch

Below, FIRST–LAST is the batch (e.g. 233–348), PAGES its pages without the blank ones
(their file reads `[Blank page]`; batch 3 has 0244, 0256, 0268, 0280, 0292, 0326, 0348):

```sh
PAGES=$(for n in $(seq FIRST LAST); do p=$(printf %04d $n); grep -qx '\[Blank page\]' ocr/la/$p.txt || echo $p; done)
```

WORK is the batch's work directory (`tmp/la-markN/`, a new N per batch), TESS =
`tmp/la-tess`. Paid calls are run by the user: give them the command, and test with
`--fake` first. Python is run with `uv run`.

1. **Verse**: done over all pages at once for 0233–1296 (Remaining work, items 1–2).
   `ocr/la_survey.py --work FIRST LAST` lists the pages whose Italian or Latin column is
   missing or whose numbers are wrong (it has false positives: "State"). Batches 1–2 were
   completed by delegation (texts/PLAN.md, "Procedure for `la`", step 4, and "What the
   delegation taught" below); open-ended delegation is not to be repeated. The markup method
   does not cover the Latin verse (GLM-OCR drops it), so the verse must be complete,
   transcribed from the images only, before step 2. Then `la_check.py FIRST LAST`
   (tercets) must report nothing but known exceptions.
2. **Markup** (paid). Copy the saved answers of the batch's pages from
   `tmp/la-markup/` into `WORK/markup/` and re-check them against the current
   `ocr/la` without calls: `uv run ocr/la_markup.py -r 0 -m gpt-6-luna -o WORK/markup
   PAGES`. A page whose lines have changed fails: delete its copied answers, and the user
   runs `uv run ocr/la_markup.py -m gpt-6-luna -o WORK/markup PAGES` (only the missing
   pages are called). Check the differences it reports as missed. Then move the pages
   with new answers back into `tmp/la-markup/` (see "Markup answers").
3. **Prepare**: `uv run ocr/la_markprep.py WORK PAGES -t TESS` resolves the trivial marks,
   locates the rest in the image and writes the crops and `ask.txt`. A page whose marks do
   not give `ocr/la` back stops it: compare and fix the page (`{`, `}` or `|` in a text;
   the page's final newline or blank lines are no longer a cause).
4. **Model decisions** (paid): test `uv run ocr/la_markdecide.py WORK --fake`, delete the
   fake answers (`WORK/ans/*.fake.json`), then the user runs
   `uv run ocr/la_markdecide.py WORK -m gpt-6-luna` (about 1100 questions for 85 pages; a
   rerun asks only what is missing).
5. **Routes**: `uv run ocr/la_markresolve.py WORK -t TESS` writes `WORK/review.tsv`, the
   marks left to la-el-claude.
6. **Review** every line of `review.tsv` into `WORK/mine.tsv` (`page line k decision note`;
   decision `left`, `right` or `text:…` with `⏎` for a line break) and corrections outside
   the marks into `WORK/fixes.tsv` (`page old new note`, the old text as in `WORK/out/`).
   Views: `ocr/la_view.py context WORK [CLASS]` (each mark in its text), `review WORK
   PAGE:K,…` (the crops), `word TESS PAGE:REGEX` (a place the crops missed). The rules,
   from the experience of 0079–0232 (details in "The method"):
   - `comma`: from the context; a dot inside a running sentence is a comma.
   - accents GLM-OCR dropped (`sì`/`si`): keep `ocr/la`, but look at unusual ones.
   - every change the model proposes (`changes ocr/la`) and every letter mark where the
     model picks GLM-OCR's side: in the image. Most are wrong: italic `v`/`r`, `t`/`l`,
     `c`/`e`, `n`/`u` and damaged letters misread. Keep printed forms and misprints;
     restore only damaged letters (`valit` → `vadit`).
   - a doubtful letter in an italic lemma: compare with the verse it quotes on the same page
     and that verse's letter shapes; the verse tells the intended word, the image the
     printed letter; a lemma printed unlike its verse is kept and listed in "Suspected
     misprints" (0111 `Racto`, 0125 `Iulium`).
   - one-sided text: mostly the Latin verse or turnover lines GLM-OCR drops (`left`); words
     only GLM-OCR has are checked in the image and inserted as `text: word` or
     `text:⏎word`; check afterwards that an inserted word did not land on a line of its own
     (0084 `secundum`, `in vere`, `magis aliis`).
   - small capitals in uppercase, superscript tercet numbers, broken words joined on essay
     pages: the conventions below, whatever the model says.
7. **Resolve**: rerun `la_markresolve.py WORK -t TESS` until `review.tsv` is empty; read the
   word diff of `WORK/out/` against `ocr/la` (every change must be one decided above; a dot
   taken from the image before a lowercase word is a comma, 0127); then add `--write`.
8. **Lines**: `uv run ocr/la_lines.py FIRST LAST -t TESS -o WORK/lines.txt` and look at each
   hit in the image (`la_view.py strip PAGE:Y` for rules, `word` for the others):
   - `# rules`: a rule needs a blank line after the line above it (see the blank-line
     conventions); `?` hits are mostly page-end rules (not written) or a short last line
     matched one line too early;
   - `# breaks`: a printed line broken in two; join it;
   - `# dots`: make the dot a comma unless it ends an abbreviation (`i.`, `al.`, `GEN.`,
     `Purg.`) or a sentence;
   - also blank lines at quotations (before or after, per the conventions), at column
     changes without a rule, inside essay quotations: look at the pages with indented
     quotations.
9. **Final checks**: `la_check.py FIRST LAST` (tercets and rule counts; known exceptions:
   0100, 0131, 0165); page heads (page number, blank line, running head; add missing
   numbers and heads); no `æ`; `—` only in gloss lines; accents as printed; lines over 68
   characters outside essays and gloss lines (paragraph lines to break at Tesseract's line
   ends).
10. **Commit**: the pages (`ocr/la`), the scripts if changed, then PLAN (this file: State,
    "History", misprints, any new convention), each as its own commit.
11. **Texts**: extend `texts/convert_la.py` to the batch's cantos (its output files and
    checks), run it, read its reports (`NO NUMBER`, `RUNOVER`, `HYPHEN`), update
    texts/la/README.md, texts/README.md and texts/PLAN.md; commit `texts` separately.

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
- Paid API calls (`ocr/la_markup.py`, `ocr/la_markdecide.py`) are run by the user. Never
  discard a saved answer, never repeat a call that cannot help, and test with fakes first.
  With a `gpt-` model, do not add `--save-usage`.

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
| 0131 | 53 | `qui fuit iustus` / `index,` | `iudex` | A turned `u`; GLM-OCR and Tesseract read `index` too. |
| 0181 | 106 | `heretici iu archis` | `in` | A turned `n`. |
| 0111 | 67 | `Racto:` | `Rapto` | Italic lemma of the Italian verse 34 (`Rapto che 'nteser`); no descender of `p`. Cf. 0107 `racta`: possibly the edition's spelling. |
| 0125 | 90 | `Orpheum, Iulium,` | `Tullium` | Italic lemma; the Latin verse 47 has `Tullium` with a full `T`; the lemma's capital has no crossbar. |

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

### Markup (`ocr/la_markup.py`; procedure step 2)

- The LLM returns only a JSON list of differences (`line`, `end_line`, `ocr`, `glm`,
  `after`); the script places them, so it cannot alter the text.
- Each answer is checked: the right sides must give the words of GLM-OCR (line-end hyphens,
  hyphens after a letter and spacing around apostrophes ignored). On problems, a fixing call
  sends only the problem places; `-r` caps the calls a page (default 2). A rerun resumes from
  the saved answers (`NNNN.json`, `NNNN.r2.json`, …, all kept).
- 0195–0208 (model `gpt-6-luna`; these first answers are now in `tmp/la-markup/bak/`): all
  14 pages pass, 355 marks; 349 after the edits of commit 3 (re-checked with `-r 0`).

### Markup answers (`tmp/la-markup/`)

The paid answers are kept in one place, `tmp/la-markup/`, the latest set per page
(`NNNN.json`, `NNNN.rK.json`, `NNNN.txt`; the latest is the set whose newest file is
newest). A batch copies its pages from there into `WORK/markup/` (step 2) and, after new
calls, moves each new page back as a whole set: a page already in `tmp/la-markup/` is first
moved, all its files, into `tmp/la-markup/bak/`, so that older `.rK.json` files do not mix
with the new set.

On 2026-10-15 the user's markup of 0755–1296 was added (1234 pages), and the 386 pages
of `tmp/la-verse-missing.txt`, whose lines change with the verse, were moved to `bak/`: 848
pages are left.

Consolidated on 2026-10-14 from `la-mark3/markup/`, `la-mark4/markup/`, `la-mark5/markup/`
and `la-markup/`: 0079–0754 (650 pages; 0104–0194 from `la-mark5`, the rest from
`la-mark4`). The first answers for 0195–0208 went to `bak/`. The older sets left in
`la-mark3/markup/` (26 pages) and `la-mark4/markup/` (0104–0194) are superseded.

### Trivial marks (`ocr/la_markprep.py`; step 3)

Resolved to the left side without the image: page numbers and running heads, tercet numbers
(A only or `1`/`1.`, on blocks whose numbers are in order), signature marks, `Digitized by
Google`, spacing next to apostrophes and after punctuation and line-end hyphens (a space
between two words, `quanto lor` / `quantolor`, is not ignored; a mid-line hyphen, 0207
`introy-tu`, is kept), `'`/`’`, `(¹)`/`(1)`, and the same text placed differently.

0195–0208: 155 of 349 resolved, 194 left.

### Image decisions (`ocr/la_markprep.py`, `ocr/la_markdecide.py`; steps 3–4)

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

### Routes and resolving (`ocr/la_markresolve.py`; steps 5–7)

| Mark | Decided by |
|---|---|
| `:` against `;` only | the context rule; no image, no model; errors accepted |
| `.` against `,` only | la-el-claude, from the context (no image) |
| letters | the model and Tesseract's word: taken when both pick the same side; else la-el-claude in the image |
| other punctuation, accents | the model; when it picks the side with an added accent, la-el-claude in the image |
| one side only, not located, dropped passages, the model's `neither` | la-el-claude in the image |
| any model decision that changes `ocr/la` | confirmed by la-el-claude in the image (`mine.tsv`) |

Results per batch: see "History".

## Known limits

- Errors shared by both OCRs (`Anmodo`, `circuleto`, 0085 `terret`) are not marked.
  Proposed checks: a lexicon check (a rare form one or two letters from a common one, across all of `ocr/la`)
  and a lemma check (an italic lemma in the commentary against the Latin verse of the page).
- Italics are not transcribed: the quotations (lemmas) in the commentary are printed in
  italics, but neither `ocr/la` nor GLM-OCR marks them (GLM-OCR has `*…*` on one page
  only). They are not looked for in the images (too many to check): whether a passage of
  the commentary is a quotation is to be decided from the text alone (e.g. matched
  against the verse of the page, as the lemma check above), later.
- `la_survey.py` ends a page's verse block at a gloss line it does not recognize (`(^1)`,
  or a gloss run over two lines), and then reports the Latin as missing (25 pages, "State").
- Line breaks and the Latin verse block are not covered by the markup (GLM-OCR joins lines
  and drops the Latin verse): the verse is completed before the markup (procedure, step 1),
  and line breaks are checked by `la_lines.py` (step 8).

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
  letter marks of the image decisions its word is a second vote beside the model.

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

## History of batches 1–2

### Commits

The work on batches 1–2 was committed in these steps:

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
   see "Results of the markup method per batch".
5. **Markup method on 0209–0232, 0115, 0141** (`c9d1cc1`, 2026-10-13): the same.
6. **Markup method on 0079–0103** (`91a4c39`, 2026-10-13), then the printed lines
   (`611a5dc`): the same, and the line ends compared with Tesseract's.
7. **Rules and blank lines on 0079–0103 and 0209–0232** (`cf35bb3`): every page `la_check.py`
   listed looked at in the image.
8. **Markup method on 0104–0194; rules, blank lines and line ends on 0104–0208** (`2005e58`,
   2026-10-13; the scripts' fix for marks with line breaks in `3d70144`); italic lemmas
   checked against their verse (`ff05702`).
9. **Completion of 0079–0232** (`79cae6f`, 2026-10-13): `la_lines.py` over the whole range:
   45 dots before a lowercase word made commas; 0084 three restored words that `text:⏎`
   had put on lines of their own joined back, two blank lines at rules added; 0085
   `territ`; no printed line broken in 0209–0232. The checks were promoted into
   `ocr/la_lines.py` and `ocr/la_view.py` (`a3a6e7f`).

| Scans | State | Commit |
|---|---|---|
| `0079`–`0103` | Verse completed and the GLM-OCR differences resolved (batch 1, by la-el-codex), checked by la-el-claude; the later delegate edits checked (commit 3). The two-OCR marks resolved by the markup method, every change checked in the image (0084: five passages `ocr/la` had dropped; 0079: signature `4`). Line ends compared with Tesseract's: 0083 and 0094 broken into printed lines, 0092's broken words joined. Text that both OCRs read alike is not checked. Blank lines checked against the rules (step 7); `la_lines.py` (step 9). | 1, 3, 6, 7, 9 |
| `0104`–`0194` | Proofread letter by letter (by la-el-agy, chunks c6–c12); every change checked by la-el-claude in the images. 0162 and 0172 are blank pages. Exceptions below. The two-OCR marks resolved by the markup method, every change checked in the image (step 8). Text that both OCRs read alike is not checked beyond the letter-by-letter pass. Blank lines checked against the rules, line ends compared with Tesseract's (step 8). | 1, 8 |
| `0115`, `0141` | The delegate's small edits checked; the two-OCR marks resolved by the markup method (no change). | 3, 5 |
| `0128`, `0140` | Blank pages (`[Blank page]`), as 0162 and 0172. | — |
| `0195`–`0208` | Two passes by la-el-codex (c13, c13b) plus fixes by la-el-claude (0197 `Ammodo`, `circulecto`; 0201 `[in]`, `qu[em]libet`; 0204 `nobilia` ×2; 0208 blank lines after the indented lemma pairs); the edits checked (commit 3). The two-OCR marks resolved by the markup method, every change checked in the image. Text that both OCRs read alike is not checked. Blank lines checked against the rules, line ends compared with Tesseract's (step 8: 0196 and 0199 blank lines, 0202 a printed line rejoined). | 3, 4, 8 |
| `0108`, `0175` | `riconoscuto` and the space before a semicolon fixed (found while measuring). | 4 |
| `0209`–`0232` | Verse completed (batch 2) and the GLM-OCR differences followed (c4; c5 for 0209–0220, line by line), by la-el-codex; the edits checked (commit 3). The two-OCR marks resolved by the markup method, every change checked in the image (0214: a trailing blank line dropped; 0227: the running head cut to `CAPITULU` restored with the page number, its duplicate before the Latin verse removed). Text that both OCRs read alike is not checked. Blank lines checked against the rules (step 7); line breaks checked (step 9). | 3, 5, 7, 9 |
| `0239`, `0263`, `0287`, `0357`, `0472`, `0513`, `0546`, `0561`, `0562` | Whole columns, verse blocks or footnotes missing from `ocr/la`, found by the GLM-OCR outlier check and restored from the images. The rest of these pages is not proofread. | 2 |
| other pages | Not touched since the transcriber's notes were deleted (commit `029b55c`). | — |

Found during the check of commit 3: 0208:63 `ruinosum` (the scan shows `rainosum`), taken
as a damaged `u`.

### Results of the markup method per batch

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

0104–0194 (`tmp/la-mark5/`; the markup answers copied from `la-mark4/markup/` and re-checked
with `-r 0`, new answers for 0106, 0107, 0131, 0193, whose lines had changed): 775 trivial
marks resolved, rule 49 (20 changes), model 655 taken (all keeping `ocr/la`, unchecked), to
la-el-claude 772 (162 commas, 138 accents GLM-OCR dropped, 139 one-sided, mostly the Latin
verse GLM-OCR drops or moves). These pages had been proofread letter by letter, and the
model's changes were mostly wrong. Where Tesseract agreed with it (48), 24 were right: printed
forms (`tamquam`, `com`, `l'empiezza`, `ille`, `nedum`, `honorum`, `celeberrima`,
`epicur[e]is`, `Le quale`, `Sic[vt]`), punctuation and the small capitals of `MATTH.`, and
two turned letters (`index`, `iu`, kept as suspected misprints); the others were italic
letters misread (`rides`, `tolus`, `tuli`, `multum`, `dirersa`, `correvin`) or damaged
letters (`valit`, `vulta`). Where Tesseract disagreed, the model picked GLM-OCR's side 52
times, rightly twice (`descendi`, `Thesyphone`). From the image beyond the two sides: 0116
`segondo`, 0174 `conce-⏎perat`, 0150 `medesimo` not printed. In the italic lemmas the
letters `r`/`v`, `t`/`l` and `c`/`e` are often hard to tell; they were decided by the
sense, and doubtful ones against the verse they quote on the same page (0111 `Racto`,
0125 `Iulium`: printed so, unlike the verse; listed as suspected misprints).

Rules, blank lines and line ends on 0104–0208, after the marks: the blank lines around the
quotations that open each part of a commentary were mostly wrong (before instead of after,
13 pages), and a few stood at column changes without a rule; `la_check.py`'s rules matched
to the file's lines found no missing blank line. Line ends: the check of every line end
against Tesseract's gave too many false hits here (144); instead, the three words around
each line break were looked up in Tesseract's lines, and a break inside one of its lines was
looked at: one wrong break, 0202 (`patrem, vel dominum suum. Secunda fraude utuntur illi,`
is one printed line).

Beyond the marks: GLM-OCR's dropped passages hid `ocr/la` errors (0203: `Nonne quid` for
`Numquid`, `consilia tione`, two commas), and `ocr/la` dropped words at a line start that
GLM-OCR has (0199 `Venimus super`, 0200 `Fili mi,`, 0202 `quo`): these go in `fixes.tsv`.

### Steps after the markup on batches 1–2

- Rules and blank lines on 0079–0103 and 0209–0232 (`cf35bb3`). Found on the way, for the
  final checks: page heads out of order or incomplete on 0083 (no `29`), 0085, 0086
  (`INFERNI` before the Latin verse), 0097, 0210 (no `INFERNI`), 0215 (no `161`), 0216 (no
  `162`), 0219, 0223 (no `169`), 0230. 0127 has no signature in the print.
- The final checks (`27524e4`, `ec93079`). Page heads: numbers added on 15 pages, order
  fixed on 4, `INFERNI` added on 0210 and moved on 0086; the pages without a head are
  chapter openings, summaries, essays, blank pages and the chapter-end pages 0080 and 0198.
  No `æ`; `—` only in gloss lines and 0081 `EXPOSITIO LIBRI. —`; accents: 0201 `pòne`, 0092
  `nè`, `sè` as the book's grave accents (`Bréholles` on 0232 stays). Line ends: lines over
  68 characters outside the essays and gloss lines found two more pages of paragraph lines,
  0131 and 0193, broken into printed lines (a check of every line end against Tesseract's
  lines gave too many false hits where Tesseract joins the columns). `la_check.py` still
  reports 0131 and 0165 (a Latin line starting with a printed `[`, `[Dicunt …]`, `[Et]
  dixi`, taken for a runover word) and 0100 (no numbers in 0099's print): not errors.
- `texts/convert_la.py` and `texts/la/008`–`020` (`996ff89`); regenerated after each later
  change of `ocr/la`. The script normalizes `’`, interleaves the verse per tercet with
  counted numbers (only 0099's two unprinted Italian numbers are reported), joins runover
  words and line-end hyphens (the unbroken form in `ocr/la` wins; the rare joined forms are
  listed), and splits the commentary into paragraphs by short sentence-final lines, since
  `ocr/la` keeps no indents; the rules between glosses are not reproduced. texts/README.md,
  texts/PLAN.md and texts/la/README.md updated.

## Tools

- `ocr/la_markup.py`, `la_markprep.py`, `la_markdecide.py`, `la_markresolve.py`: the markup
  method (procedure, steps 2–7).
- `ocr/la_view.py review|context|word|strip`: views for the review and the checks
  (steps 6, 8).
- `ocr/la_lines.py FIRST LAST -t TESS [-o OUT]`: rules without a blank line, printed lines
  broken in two, dots before a lowercase word (step 8).
- `ocr/la_check.py FIRST LAST [-v] [-o OUT]`: tercet numbers (order, every third line,
  continuity across pages) and the section rules of the images against the blank lines
  (the rule count often misses right-column and page-end rules: look at a listed page).
- `ocr/la_versecrop.py PAGE... -t TESS -o OUTDIR`: crops the verse column missing from a
  page (found from the other column's lines in Tesseract's words and the blank band
  between the columns), for its transcription; `crops.tsv` lists the boxes and the line
  counts to look at (Remaining work, item 1).
- `ocr/la_survey.py [--cantos | --work FIRST LAST] [-o OUT]`: the survey of the verse
  blocks (texts/PLAN.md, step 1): which pages lack the Italian or the Latin column, per
  page, per canto, or as the work list of a batch. It reads dante-corpus as a dependency
  in `../dante-corpus` (README.md).
- `tmp/tess.py RANGE [-o tmp/la-tess]` (not in git): runs Tesseract (Windows `tesseract.exe`
  under WSL) for the word boxes; done for all pages.
- `texts/convert_la.py`: `ocr/la` to `texts/la/` (procedure, step 11).

Working data in `tmp/` (not in git; keep all, `tmp/bak/` is the user's): `la-tess/`
(Tesseract's words for every page), `la-markup/` (the paid markup answers, the latest set
per page, 848 pages; see "Markup answers"), `la-verse/` (the verse crops) and the page lists
`la-verse-*.txt` (see "State"), `la-mark2/` (the work directory of 0195–0208:
answers, decisions, fixes), `la-mark3/` (the same for 0209–0232, 0115, 0141), `la-mark4/`
(the same for 0079–0103), `la-mark5/` (the same for 0104–0194; its `mine.tsv`, `fixes.tsv` and
`route.tsv` are examples of the decisions), `la-label/` (the labelled set: paid answers and
scores).
