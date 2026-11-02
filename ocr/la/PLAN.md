# Plan: checking `ocr/la` after its completion

This is the plan for `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), now that it is complete. The completed work (the verse, the two-OCR markup, the
batches, the retyping, the line checks and the conversion) and the first two checks (check 1
and the verse check) are recorded in [DONE.md](DONE.md); the "procedure" steps and the
"items" cited below are those of DONE.md. The conversion into `texts/la/` is described in
[texts/PLAN.md](../../texts/PLAN.md) ("`texts/la/`").

**A new session starts here**: read "State" and go on from the first open step of "Checks".
The rules and conventions below are settled: apply them, do not ask again.

## State (2026-11-03)

`ocr/la` is complete (`0001`–`1296`) and converted into `texts/la/001`–`110` (DONE.md).
What the completed method cannot see are errors that both OCRs share: `ocr/la` was proofread
by marking where it disagrees with GLM-OCR, so a word that both read alike and wrongly is
not marked (0085 `terret` for printed `territ`, 0197 `circuleto` for `circulecto`, both
corrected outside the markup). The checks below look for them (decided with the user, 2026-11-01).

Done (DONE.md): check 1 (lemmas against the verse: 1,271 candidates, 9 misread, and about
80 more errors found in the same lines and by the searches they led to) and the verse check
(the Latin verse against the Italian text, then every line of both verse columns read again
from the image: about 250 lines misread and 46 misprints). **Next**, in this order (each
below, under "Checks"):

1. **Italics**: write `ocr/la_italic.py` (step 1), try it on batch 1 (step 2) and decide
   with the user how the extent is set; then the scope, the marks and the scripts that read
   `ocr/la` (steps 3–6).
2. **Check 2**: write `ocr/la_lexcheck.py`, its recall trial on the first transcription,
   then decide the candidates in the image.
3. **When all are done**: State, Known limits, texts/PLAN.md and texts/la/README.md, and
   the record moved to DONE.md.

## Checks

The checks list candidates by script, and every candidate is decided in the image
(`ocr/la_view.py word`), never from the sense or from another edition. A candidate is one of:

- **misread**: `ocr/la` differs from the print; correct `ocr/la`;
- **printed**: `ocr/la` is as printed; a misprint goes into "Suspected misprints", a form of
  the edition (a spelling of the manuscript, a variant of the quotation) is only recorded;
- **other**: not a reading at all (a split word, a name, Italian in the Latin); recorded.

The decisions are kept in a table per check in `ocr/la/` (`lemmacheck.tsv`,
`versecheck.tsv`, `lexcheck.tsv`: `page line form decision note`), committed with the
fixes. What each table holds and who reads it:

- `lemmacheck.tsv` (check 1): only the candidates decided `printed`; a misread candidate was
  corrected and is no longer a candidate. `la_lemmacheck.py` reads it and leaves out what is
  decided (matched by page and form, as line numbers shift), so a rerun lists only new
  candidates.
- `versecheck.tsv` (verse check): every decided line, `misread` (corrected; the note has
  the old form, `was …`), `misprint` and `printed` (mostly the lines listed by step 0). A
  record only: `la_versecheck.py` compares every line and does not read it.
- `lexcheck.tsv` (check 2): to be written as `lemmacheck.tsv`, read by `la_lexcheck.py`.

The misprints are gathered in "Suspected misprints" whatever found them (the markup, a
check, by chance); a `misprint` row of a table is also a row there.

Order: check 1 (lemmas) first, as its candidates were fewer and surer; then the verse
check, with the same procedure while it was fresh (both done); then the italics, which start
from the lemmas of check 1; then check 2, whose ranking learns from the errors checks 1
and the verse check found, and whose counts are surer once the verse is right.

### Done: check 1 and the verse check

Check 1 (lemmas against the verse, 0079–1270 in 10 batches, 2026-11-01) and the verse
check (every line of both verse columns read again from the image, 0079–1270 in 11
batches, 2026-11-01 – 2026-11-03) are recorded in DONE.md ("Check 1", "Verse check").
What the next steps take from them:

- `ocr/la_lemmacheck.py FIRST LAST -v` lists the lemmas found: the italics (step 1) match
  their runs of italic words to them.
- `lemmacheck.tsv` and `versecheck.tsv`: their forms are decided; check 2 leaves them out.
- Check 1's procedure per batch (crops in a shuffled order, read by la-el-agy from the images
  alone, compared line by line, every difference decided in the image) can serve check 2
  if its list is long. Match every reading to its line before comparing (batch 9: 60
  readings were not of their images).
- Check 1's errors were mostly a common spelling written for the printed one (`mihi` for
  `michi`, `societate` for `sotietate`, accents not printed); check 2, which looks for rare
  forms, does not find this kind (below, "Not found by this check").
- The verse check's procedure per batch (page images by `ocr/la_versecheck.py
  --page-crops`, read by la-el-agy and la-el-agy2 from the images alone, aligned by
  `--page-readings`, every difference decided in the image) can serve as well. Its
  readers' errors: a common spelling written for the printed one, a misprint corrected,
  accents left out or added, specks read as marks; in batch 11 the tercet numbers of
  three cantos left out and reported as not printed. A report is not taken as true.

### Italics (after check 1; decided with the user, 2026-11-01)

The printed italics are transcribed, the lemmas first. Check 1 finds the lemmas by their
words; the italics come from the print, so their extent is taken from the image, not from
the match (a lemma can end in `etc.`, leave out a word, or quote the Italian).

- **Mark**: `*…*` in `ocr/la`, as `ocr/en-oelsner` keeps its italics; not a table, as
  line positions shift with every fix and the italics are part of the print. Each line
  keeps its own pair, so a page stays line for line: `*dedit ven-*` / `*tum:*`, closed
  before the line end and reopened on the next line. Punctuation follows the print: inside
  the pair if it is italic, outside if roman (decided in the image as a convention on the
  first pages, then applied). The existing `*` of 1283 (`154*`, printed) is not a mark.
1. **Slant script** (`ocr/la_italic.py FIRST LAST -t TESS [-o OUT]`): for each Tesseract
   word box of the commentary, the shear that makes its vertical strokes most upright
   (the variance of the column profile, over a range of shears); a word is italic if its
   best shear is clearly slanted. Output per page: the runs of italic words, their lines
   and words, and the lemma of check 1 they match or `none`.
2. **Trial** on batch 1 (`0079`–`0114`): read the italics of a few pages by eye and
   compare. If the script separates italic from roman reliably (a missed or false word a
   page at most), it sets the extent; if not, every lemma's extent is checked in the
   image (`la_view.py word`), which is many thousands: then decide with the user first.
3. **Scope**: the lemmas, then the other italics the script finds (quotations of other
   authors, titles; in the essays, front matter and appendix too), listed by kind after
   the trial and marked if the user agrees.
4. **Write** the marks into `ocr/la` by script from the checked runs (`ocr/la_italic.py
   --write`), batch by batch; the words of each page unchanged (the diff, with `*`
   removed, is empty).
5. **Scripts** that read `ocr/la` (`la_check.py`, `la_seqcheck.py`, `la_lostcheck.py`,
   `la_lines.py`, `la_survey.py`, the two checks) remove `*` before comparing;
   `convert_la.py` keeps the marks, joins a pair broken at a line end (`*dedit ven-*` /
   `*tum:*` → `*dedit ventum:*`, and `*a*` / `*b*` → `*a b*`) and checks that every
   line has its pairs closed.
6. **Commit**: the scripts, then `ocr/la` per batch, then `texts` (texts/PLAN.md and
   texts/la/README.md: italics now transcribed), then this PLAN (the convention under
   "Conventions settled during the check", "Known limits").

### Check 2: rare forms near common ones (`ocr/la_lexcheck.py`)

A misreading that both OCRs share usually turns a word into a form that occurs nowhere
else: 0197 `circuleto` (once) beside `circulecto` (5 times, and `circulectos` 10). A form found once or twice in
the whole book, one or two letters from a form found often, is a candidate.

1. **Script**: the words of all pages (`0001`–`1296`, blank pages aside), with the
   line-end hyphens joined as `convert_la.py` joins them, counted case-insensitively. For
   each form of count 1–2, the forms at edit distance 1 (2 for forms of 8 letters or
   more) with a count of at least 5 and at least 5 times its own; listed with page, line,
   the counts, the neighbours, the context, and Tesseract's word at that place (from
   `ocr/la/tesseract/`; it does not normalize spellings, so its reading is a third vote).
   Ranked: Tesseract reading the neighbour first, then the letter pairs that the OCRs
   confuse (`c`/`e`, `n`/`u`, `r`/`t`, `rn`/`m`, `li`/`h`, `f`/`s`, `cl`/`d`), then the
   rest. Left out: the forms in "Suspected misprints", `lemmacheck.tsv`,
   `versecheck.tsv` and `lexcheck.tsv`. Options: `FIRST LAST`, `-t TESS`, `-o OUT`, `--min N` (the neighbour's
   count), `-d DIR` (read the pages from DIR instead of `ocr/la`).
2. **Trial**: a recall test on the first transcription (the pages of commit `89ac4a3`,
   exported to a scratch directory and read with `-d DIR`): of the words the proofreading
   later corrected there (`git diff 89ac4a3 -- ocr/la`, word by word), count how many the
   script lists, `circuleto` (0197) among them, and look at those it misses to tune the
   limits. Then run it on `ocr/la` and count the candidates; with the Latin of the manuscript (`michi`, `nichil`, `quedam`, `pexime`) many
   rare forms are printed so. If the list is too long to decide by eye (more than about
   2,000), first decide with the user how to narrow it (a higher `--min`, only the ranked
   groups, or paid image decisions as in DONE.md, item 7).
3. **Decide** in the image, in rank order; record in `lexcheck.tsv`. A form decided
   printed for one page is not taken as printed for another: each place is looked at.
4. **Checks** and **commit** as in check 1 (DONE.md, "Check 1", steps 5–6), batch by batch
   if long.

Not found by this check: misreadings into a common word (0085 `terret` is a real word,
printed on 0489), rare words with no common neighbour, and a common spelling written for
the printed rare one (`mihi` for `michi`: the error is the common form). Check 1 covers
part of the first kind inside lemmas.

### When all are done

Update "State" and "Known limits" (what the checks covered), texts/PLAN.md and
texts/la/README.md (the proofreading described there), and move the record of the verse
check, the italics and check 2 to DONE.md, as check 1's.

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
  that are not printed are not added (1245). 1044 and 1247 are in this form since their
  retyping.

## Suspected misprints

The file keeps what is printed; whether to correct these is decided later. Line numbers
refer to `ocr/la/PAGE.txt` at the time of the check.

| Page | Line | Printed | Expected | Note |
|------|------|---------|----------|------|
| 0113 | 62 | `Ledit ventum:` | `Dedit ventum:` | Lemma of the Latin verse `Terra lacrymosa dedit ventum`; the image shows an `L`, and GLM-OCR reads `Ledit` too. |
| 0099 | 11, 14 | (no number) | `32`, `33` | The Italian tercets 32 and 33 have no number; the Latin column has `32` and `33`. |
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
| 0208 | 58 | `quod lucus,` | `locus` | The sense needs `locus`. |
| 0249 | 52, 101–102 | `comprehendidi` | `comprehendisti` | Latin verse 16 and its lemma (`comprehen-` / `didi`) alike. |
| 0241 | 28 | `respicit tumquam suum` | `tamquam` | Latin verse; the `u` is open at the top, unlike the `a` of `quam`. |
| 0261 | 21 | `Vicit timor bonum voluntatem,` | `bonam` | Latin verse; an open `u`. |
| 0338 | 14 | `vadunt per vium.` | `viam` | Latin verse. |
| 0363 | 17 | (no number) | `6` | Italian tercet 6 has no number, as 0099. |
| 0396 | 10 | `Quis posest unquam` | `posset` | Latin verse 1. |
| 0446 | 32 | `Guctaverunt super labia` | `Gustaverunt` | Latin verse; `c` for `s`. |
| 0455 | 31 | `[ricinus.` | `vicinus` | Latin verse runover; an italic `r` for `v`. |
| 0461 | 34 | `in talem citernam;` | `cisternam` | Latin verse 45. |
| 0461 | 47 | `unius sui proximani,` | `proximi` | Latin verse. |
| 0468 | 17 | `La dextra mi parca` | `parea` | Italian verse 15; `c` for `e`. |
| 0514 | 25 | `Quant'um buon gittator` | `Quant'un` | Italian verse; `m` for `n`. |
| 0529 | 41 | `Ad humerum sinistrun` | `sinistrum` | Latin verse; `n` for `m`. |
| 0189 | 54–55 | `re-` / `spondidi sibi` | `respondi` | Italic lemma; the Latin verse 17 has `Respondi`. |
| 0190 | 78–79 | `rea-` / `censa` | `reaccensa` | Commentary, quoting the Latin verse 27 (`reaccensa`); one `c`. |
| 0686 | 74 | `uon seutitur` | `non sentitur` | Commentary; two turned `n`s (an `n` beside them in `uon` has its arch). |
| 0716 | 31 | `michi tuuc cogitando` | `tunc` | Commentary; a turned `n`; the verse has `nunc`. |
| 0730 | 20 | `di retro a noi remaso:` | `rimaso` | Commentary quoting the Italian verse 1 (`rimaso`). |
| 0764 | 18 | `non volca storpio` | `volea` | Commentary quoting the Italian verse 1 (`volea`); an italic `c` without the eye. |
| 0777 | 27 | `2 Fericbat me sol` | `Feriebat` | Latin verse; an italic `c` without the eye; the commentary has `Feriebat`. |
| 0832 | 89 | `corum pluvium` | `eorum` | Commentary; the image shows `c`; the verse has `eorum`. |
| 0855 | 20 | `apparebat iciuna.` | `ieiuna` | Latin verse; an italic `c` without the eye; the commentary has `ieiuna`. |
| 0943 | 65 | `inde se voivit in` | `volvit` | Commentary; an `i` with its dot for `l`; the verse has `volvit`. |
| 0976 | 61 | `catur Prava),` | `Piava` | Commentary; the image shows `r`; the verse has `Piave`. |
| 1126 | 64 | `[ficum,` | `fixum` | Latin verse 31, the runover word; italic; the commentary has `fixum`. |
| 1262 | 35 | `idest eccessui.` | `excessui` | Commentary; the image shows `cc`; the verse has `excessui`. |
| 0525 | 28 | `ad ventrum lista` | `centrum` | Latin verse 10; an italic `v` (rounded bottom); the commentary has `centrum`. |
| 0526 | 48 | `in sotictate` | `sotietate` | Commentary; the image shows `c` (no bar); the verse has `sotietate`. |
| 0131 | 53 | `qui fuit iustus` / `index,` | `iudex` | A turned `u`; GLM-OCR and Tesseract read `index` too. |
| 0181 | 106 | `heretici iu archis` | `in` | A turned `n`. |
| 0111 | 67 | `Racto:` | `Rapto` | Italic lemma of the Italian verse 34 (`Rapto che 'nteser`); no descender of `p`. Cf. 0107 `racta`: possibly the edition's spelling. |
| 0125 | 90 | `Orpheum, Iulium,` | `Tullium` | Italic lemma; the Latin verse 47 has `Tullium` with a full `T`; the lemma's capital has no crossbar. |
| 0976 | 14 | `Cimisa fui chiamata` | `Cunisa` | Italian verse; an `i` dot right after `C` and five stems before `s` (Tesseract `Cimisa`, GLM-OCR `Cinisa`); the commentary has `Cunizza`. |
| 1042 | 11 | `Agl' ochi mici,` | `miei` | Italian verse; a clear `c` (GLM-OCR `mici` too). |
| 1053 | 23 | `s'àdempia` | `s'adempia` | Italian verse; a grave accent over the `a` (Tesseract `s'àdempia`). |
| 0350 | 6 | `3 Quando la brina` | `2` | Italian verse; the first tercet is `1`, the Latin column has `2`. |
| 0758 | 17 | `37 Poi si partì` | `38` | Italian verse; the tercet before is `37` too, the Latin column has `38`. |
| 0810 | 51 | `45 Dabo tibi` | `46` | Latin verse; the tercet before is `45` too, the Italian column has `46`. |
| 0810 | 105 | `etatem anri` | `auri` | A turned `u` (the verse has `Etatem auri`). |
| 0827 | 74 | `Oblibanum` | `Olibanum` | The image shows `Obl`; both OCRs read it so. |
| 1182 | 5 | `57 Nel monte` | `47` | Italian verse; the page before ends at `46`, the Latin column has `47`. |
| 1281 | 103 | `formas corum` | `eorum` | Commentary; the image shows `c`, and both OCRs read `corum`. |
| 0389 | 105 | `duxi corum artes` | `eorum` | Commentary; the verse above has `eorum`; the image shows `c`. |
| 0380 | 77–78 | `expendi-` / `distis` | `expendistis` | Commentary; a syllable repeated over the line break. |
| 0423 | 15 | `[sn (12) rinverte` | `su` | Italian verse runover; the image shows `sn` (a turned `u`). |
| 0710 | 3 | `PURGATORI` | `PURGATORII` | Running head. |
| 0652 | 75–76 | `Phsi-` / `strato` | `Pisistrato` | Commentary; both OCRs read `Phsi-`. |
| 0773 | 77–78 | `sim-` / `beleggiate` | `simboleggiate` | Essay; the image shows `e`. |
| 0825 | 3 | `in isto tricesimo capitulo` | `In` | *Summarium*'s first word in lowercase, as printed. |
| 0958 | 45–46 | `complexio-` / `conibus` | `complexionibus` | Commentary; a syllable lost over the line break. |
| 0999 | 71–72 | `volupta-` / `bro` | `volutabro` | Commentary; the image shows `volupta-`. |
| 1031 | 69–70 | `corrupti-` / `lium` | `corruptibilium` | Commentary; a syllable lost over the line break. |
| 1135 | 75–76 | `sen-` / `bianza` | `sembianza` | Italic lemma; the verse has `sembianza`; the image shows `n`. |
| 1264 | 59–60 | `mi-` / `mium` | `nimium` | Commentary; the image shows `mi-`. |
| 0085 | 29 | `quod aier de co timeret` | `eo` | Latin verse 48 (Italian `ne temesse`); an italic `c` without the eye, as 0764 `volca`. |
| 0227 | 49 | `Surgit in vermen est plantam` | `et` | Latin verse 100 (Italian `et in pianta`). |
| 0259 | 47 | `prerogatiram` | `prerogativam` | Latin verse 23; an italic `r` for `v`, as 0154 `traraglia`. |
| 0439 | 40 | `in navi se leravit` | `levavit` | Latin verse 145; an italic `r` for the first `v`. |
| 0530 | 12 | `Meridianum solis, quiu in ripa` | `quia` | Latin verse 46 (Italian `ch'a la riva`). |
| 0606 | 19 | `Si bona oratio cum non adiuvat` | `eum` | Latin verse 44 (Italian `lui`); an italic `c` without the eye, as 0085 `co`. |
| 0113 | 18 | `Hac nunquam transirit anima bona` | `transivit` | Latin verse 43 (Italian `non passa`); an italic `r` for `v`, as 0259 `prerogatiram`; found by the verse reading. |
| 0086 | 6 | `E li parenti mici furo Lombardi` | `miei` | Italian verse 23; a `c` without the bar of `e` (the `e` of `parenti` has it); the Latin has `mei`; found by the verse reading. |
| 0592 | 16 | `Et plus et mimus erat` | `minus` | Latin verse 22; `m` for `n`; found by the verse reading. |
| 0605 | 14 | `Provenzan (8) Selvani;` | `Salvani` | Italian verse 41; found by the verse reading. |
| 0612 | 13 | `Che in Semnaar (6)` | `Sennaar` | Italian verse; `m` for the first `n`; found by the verse reading. |
| 0623 | 19 | `Com poco tempo` | `Con` | Italian verse; `m` for `n`; found by the verse reading. |
| 0625 | 11 | `fummo um poco` | `un` | Italian verse 17; `m` for `n`; found by the verse reading. |
| 0639 | 27 | `Quando in Farentia` | `Faventia` | Latin verse (Italian `Faenza`); an italic `r` for `v`, unlike the `v` of `parve` below; found by the verse reading. |
| 0647 | 25 | `Ex co quia per nos` | `eo` | Latin verse; an italic `c` without the eye, as 0085 `co`; found by the verse reading. |
| 0652 | 9 | `chinarsi (3)` | `chinarsi (8)` | Italian verse 37; gloss mark `(3)` for `(8)`, whose note is `in ginocchione` (the `(3)` of the page is `lapidare`); found by the verse reading. |
| 0709 | 32 | `14 Etipse:` | `Et ipse` | Latin verse; no space between the words; found by the verse reading. |
| 0725 | 16 | `[Achylle (9,` | `(9),` | Italian verse runover; the closing parenthesis of the gloss mark not printed; found by the verse reading. |
| 0734 | 47 | `postmodum tanctum sancti` | `tantum` | Latin verse 28; found by the verse reading. |
| 0737 | 21 | `[de (12.` | `(12).` | Italian verse runover; the closing parenthesis not printed, as 0725; found by the verse reading. |
| 0745 | 49 | `ipsam ita tor tam` | `tortam` | Latin verse; a space inside the word; found by the verse reading. |
| 0753 | 12 | `da ch'è si munta` | `sì` | Italian verse; no accent; found by the verse reading. |
| 0856 | 8 | (no number) | `44` | Italian tercet 44 has no number, as 0363; found by the verse reading. |
| 0878 | 12 | `miglor voci (8)` | `(18)` | Italian verse; the `1` not printed, a space left; found by the verse reading. |
| 0897 | 5 | (no number) | `31` | Italian tercet 31, the first line of the page, has no number; the file keeps `31` (Batch 8); found by the verse reading. |
| 0952 | 30 | `Isia natura suo Factori` | `Ista` | Latin verse; an `i` with its dot for the `t`; found by the verse reading. |
| 1076 | 32 | `Quare voluntas meu esset` | `mea` | Latin verse 9; found by the verse reading. |
| 1091 | 13 | `Um poco s'arrestavan` | `Un` | Italian verse; `m` for `n`, as 0623 and 0625; found by the verse reading. |
| 1124 | 9 | `uno scalco erecto` | `scaleo` | Italian verse; `c` for `e`; found by the verse reading. |
| 1143 | 26 | `Sed puucum fuit` | `paucum` | Latin verse 6; found by the verse reading. |
| 1148 | 35 | `Inde remunsere ibi` | `remansere` | Latin verse 43; found by the verse reading. |
| 1242 | 24 | `et ad corum cantus` | `eorum` | Latin verse 45; the same line has `eorum` before; found by the verse reading. |
| 1242 | 27 | `tantam habundatiam` | `habundantiam` | Latin verse 46; found by the verse reading. |
| 1206 | 32 | `medesimo rise (2).` | `(12)` | Italian verse; the marks before are (10) and (11), the commentary has (12); found by the verse reading. |

## Known limits

- Errors shared by both OCRs (`Anmodo`, `circuleto`, 0085 `terret`) are not marked by the
  markup method; "Checks" above looks for them.
- Italics are not transcribed yet: the quotations (lemmas) in the commentary are printed in
  italics, but neither `ocr/la` nor GLM-OCR marks them (GLM-OCR has `*…*` on one page
  only). "Checks", Italics, adds them: the lemmas found by check 1, their extent from the
  image.
- Check 1 needs a lemma of 3 words with 2 equal to the verse, and a word within an edit
  distance of 2: 0154 `nuove traraglia` (2 words; the Latin verse has `travagle`, 3 edits)
  is not found.
- The Latin verse is not covered by the markup (GLM-OCR drops it). The verse check read
  every line of it, and of the Italian verse, again from the image (DONE.md, "Verse
  check"), each line by one reader; a word that the first OCR and the reader both read
  alike and wrongly is not found.
- `la_survey.py` ends a page's verse block at a gloss line it does not recognize (`(^1)`,
  or a gloss run over two lines), and then reports the Latin as missing (25 pages, "Record of the preparation").
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
- **Tesseract** (`ocr/la/tesseract/`, committed; run with its [Makefile](tesseract/Makefile),
  `-l lat+ita`, only the words kept, in the columns block_num, par_num, line_num, left, top,
  width, height, text): used only for the word
  boxes, to locate a place in the image. Its readings are poor in general, but it does
  not normalize spellings (13 of the 15 suspected misprints read as printed), so for the
  letter marks of the image decisions its word is a second vote beside the model.

## Tools

- `ocr/la_markup.py`, `la_markprep.py`, `la_markdecide.py`, `la_markresolve.py`: the markup
  method (procedure, steps 2–7).
- `ocr/la_view.py review|context|next|word|strip`: views for the review and the checks
  (steps 6, 8).
- `ocr/la_mine.py WORK PAGE K=DECISION[|NOTE] …`: appends review decisions to
  `WORK/mine.tsv` (step 6).
- `ocr/la_retype.py WORK PAGE FILE NOTE [--old PART]`: a fixes.tsv row replacing a page
  (or a part of it) of `WORK/out/` by its retyped text (step 6).
- `ocr/la_lines.py FIRST LAST -t TESS [-o OUT]`: rules without a blank line, printed lines
  broken in two, dots before a lowercase word (step 8).
- `ocr/la_check.py FIRST LAST [-v] [-o OUT]`: tercet numbers (order, every third line,
  continuity across pages) and the section rules of the images against the blank lines
  (the rule count often misses right-column and page-end rules: look at a listed page).
- `ocr/la_lostcheck.py FIRST LAST -t TESS [-g GLM] [-d DIR ...] [-n N] [-v] [-o OUT]`: text
  lost from a page: runs of 4+ words of Tesseract and GLM-OCR found nowhere in the page
  file, matched loosely (three-word runs, similarity 75) and in any order; `both` (the two
  OCRs agree) is lost text, `tess`/`glm` mostly one OCR's noise. It does not see lines out
  of order or run together. `-d` reads another directory first (e.g. `WORK/out`).
- `ocr/la_seqcheck.py FIRST LAST [-d DIR ...] [-v] [-o OUT]`: per page, verse blocks whose
  tercet numbers skip, Italian and Latin numbers that differ, plain-digit tercet numbers,
  leftovers (`(1)`, `<sup>`, `[For `, a `—` line, double spaces), indented lines.
- `ocr/la_versecrop.py PAGE... -t TESS -o OUTDIR [-c it|la]`: crops the verse column
  missing from a page (found from the other column's lines in Tesseract's words and the
  blank band between the columns), for its transcription; `crops.tsv` lists the boxes and
  the line counts to look at (DONE.md, item 1). `-c` crops that column also where
  the file has it (the trial).
- `ocr/la_verseread.py CROPS [PAGE...] -m MODEL [-n N] [--fake] [--check]`: transcribes
  each crop with a model, from the image only (tercet number and text of each line apart;
  superscripts and `(¹)` written by the script): `CROPS/read/PAGE.txt`, the answers
  `PAGE.MODEL.json` reused on a rerun. `--check` compares with the same column of
  `ocr/la` (`read/check.txt`).
- `ocr/la_verseinsert.py PAGE... -d DIR [-n]`: inserts the checked Italian verse
  (`DIR/PAGE.txt`) before the page's Latin block; the Latin tercet numbers made
  superscript and set to the Italian's line by line, every number added or changed
  listed (to check in the image); a page whose Latin line count differs is left as it is.
- `ocr/la_survey.py [--cantos | --work FIRST LAST] [-o OUT]`: the survey of the verse
  blocks (texts/PLAN.md, step 1): which pages lack the Italian or the Latin column, per
  page, per canto, or as the work list of a batch. It reads dante-corpus as a dependency
  in `../dante-corpus` (README.md).
- `texts/convert_la.py`: `ocr/la` to `texts/la/` (procedure, step 11).
- `ocr/la_lemmacheck.py FIRST LAST [-v] [--crops DIR] [--readings DIR] [-o OUT]`: check 1
  (DONE.md, "Check 1"): lemmas against the verse; `--crops` writes the line images of the
  candidates, `--readings` compares a reader's `DIR/readings.tsv`.
- `ocr/la_versepairs.py [FILES] [-d DIR | -o OUT]`: the verse of the cantos in `texts/la`,
  the Italian and the Latin line side by side, one TSV per canto (verse check, step 0).
- `ocr/la_versecheck.py FIRST LAST [--italian] (--crops DIR | --page-crops DIR |
  --readings DIR [-o OUT] | --page-readings DIR [-o OUT])`: the verse check (DONE.md,
  "Verse check"): the line or page images of the Latin (or Italian) verse, and the
  comparison of a reader's `DIR/readings.tsv` with `ocr/la`.
- `ocr/la_italic.py`, `ocr/la_lexcheck.py`: to be written ("Checks").

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
