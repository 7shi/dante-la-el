# Plan: checking `ocr/la` after its completion

This is the plan for `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), now that it is complete. The completed work (the verse, the two-OCR markup, the
batches, the retyping, the line checks and the conversion) and the checks after it (check 1,
the verse check, the italics and check 2) are recorded in [DONE.md](DONE.md); the
read-through still to do is under "Read-through". The "procedure" steps and the "items"
cited below are those of DONE.md. The conversion into
`texts/la/` is described in [texts/PLAN.md](../../texts/PLAN.md) ("`texts/la/`"). A short
account of the whole work, for checking the other texts, is in [SUMMARY.md](SUMMARY.md).

**A new session starts here**: read "State". The rules and conventions below are settled:
apply them, do not ask again.

## State (2026-11-05)

`ocr/la` is complete (`0001`–`1296`) and converted into `texts/la/001`–`110` (DONE.md).
What the completed method cannot see are errors that both OCRs share: `ocr/la` was proofread
by marking where it disagrees with GLM-OCR, so a word that both read alike and wrongly is
not marked (0085 `terret` for printed `territ`, 0197 `circuleto` for `circulecto`, both
corrected outside the markup). The checks of "Checks" looked for them (decided with the user,
2026-11-01).

Done (DONE.md): check 1 (lemmas against the verse: 1,271 candidates, 9 misread, and about
80 more errors found in the same lines and by the searches they led to), the verse check
(the Latin verse against the Italian text, then every line of both verse columns read again
from the image: about 250 lines misread and 46 misprints), the italics (marked `*…*`
over the whole volume from the slant of the print, the flagged lines decided in the image:
4,232 pairs on 908 pages; "Italics" under "Conventions settled during the check") and
check 2 (rare forms near common ones: 22,567 candidates, the first two groups decided in
the image and the third read for sense, 149 misread and 94 misprints). What they do not
cover is under "Known limits".

Next: the read-through ("Read-through"), planned with the user on 2026-11-05; the tools
are made (step 0) and the trial is done (step 1); the batches (step 2) are next.

## Checks

The checks list candidates by script, and every candidate is decided in the image
(`ocr/la/scripts/view.py word`), never from the sense or from another edition. A candidate is one of:

- **misread**: `ocr/la` differs from the print; correct `ocr/la`;
- **printed**: `ocr/la` is as printed; a misprint goes into "Suspected misprints", a form of
  the edition (a spelling of the manuscript, a variant of the quotation) is only recorded;
- **other**: not a reading at all (a split word, a name, Italian in the Latin); recorded.

The decisions are kept in a table per check in `ocr/la/` (`lemmacheck.tsv`,
`versecheck.tsv`, `lexcheck.tsv`: `page line form decision note`), committed with the
fixes. What each table holds and who reads it:

- `lemmacheck.tsv` (check 1): only the candidates decided `printed`; a misread candidate was
  corrected and is no longer a candidate. `scripts/lemmacheck.py` reads it and leaves out what is
  decided (matched by page and form, as line numbers shift), so a rerun lists only new
  candidates.
- `versecheck.tsv` (verse check): every decided line, `misread` (corrected; the note has
  the old form, `was …`), `misprint` and `printed` (mostly the lines listed by step 0). A
  record only: `scripts/versecheck.py` compares every line and does not read it.
- `lexcheck.tsv` (check 2): `page line form decision note`, as `lemmacheck.tsv`; its forms
  are left out by `scripts/lexcheck.py`.
- `readcheck.tsv` (the read-through, not yet made): every flagged place decided, as
  `versecheck.tsv`.

The misprints are gathered in "Suspected misprints" whatever found them (the markup, a
check, by chance); a `misprint` row of a table is also a row there.

Check 1, the verse check, the italics and check 2 are done (DONE.md: their records, and
"The checks" for their order and what later work takes from them).

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
- **Steps**:
  0. Preparation (done): `ocr/scripts/pages.py` writes the pages of `texts/la` for a
     range, cut at the page markers, for the reader; `ocr/scripts/findline.py` finds the
     lines of the flagged phrases in `ocr/la` (the marks removed first);
     `ocr/scripts/txtfix.py` applies the fixes (`PAGE:LINE old new`)
     ([ocr/scripts/README.md](../scripts/README.md), "The read-through").
  1. Trial (done, 2026-11-05): 0595–0614 (19 pages, 12,723 words) as they were at
     `b772857`, before the checks after completion (`89ac4a3`, the first OCR, has too
     many errors to stand for what is left). Of the 40 word corrections made there since
     (spacing aside), 16 were flagged; of the 24 missed, 10 are spellings the OCR had
     normalized (`Quae` for `Que`, `condemnati`), which no reading for sense can see, and
     most of the rest accents (`despiciébat`, `fuggíro`, `sian` for `siàn`). The other 39
     flags fell on text that every check had passed: 10 misread (a line out of place on
     0602, `da` for `datur`, `ingre-` for `inge-`, accents of the essay), 9 misprints (4
     already listed), 20 printed (mostly Serravalle's Latin against the verse). The pages
     count as read; their decisions are the first rows of `readcheck.tsv`.
  2. Batches over the whole of `texts/la`, whole pages, their size set by the trial. The
     reader writes a TSV: page, the phrase as written, the reason.
  3. Decisions: a misreading is corrected in `ocr/la`; a misprint goes into "Suspected
     misprints"; every decision is a row of `readcheck.tsv`.
  4. After the fixes: `texts/scripts/convert_la.py`, `ocr/la/scripts/seqcheck.py 79 1270` and
     `ocr/la/scripts/check.py 79 1287`, each compared with its previous output; a commit per
     batch, `ocr/la` and `texts/la` apart.
  5. The other texts, after `la`: the same steps, a trial of a few pages each, the images
     `ocr/{dir}/NNN.png`, the records in each `ocr/{dir}/`; what no check has read there
     is mainly prose (SUMMARY.md).
- **The reader's task** (basic rules only, not new ones each round): flag, do not
  correct; the medieval spellings (`michi`, `nichil`, `e` for `ae`) and the old Italian
  ones are the edition's and not errors; the printed punctuation is not normalized; no
  subagents and no git commands; the TSV written as a file (a script it runs takes `-o`,
  no shell redirection). Each request is sent after the user's signal.

## Standing rules

- Transcribe only from the images. Never copy from dante-corpus, other editions, memory, or
  GLM-OCR: this edition's Italian and Latin forms differ, and copying replaces them with
  common ones.
- Keep the print, misprints included (see "Suspected misprints"). Only damaged letters are
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
| 0153 | 107 | `per rim, idest per fortitudinem` | `vim` | Italic lemma; an `r` with no entry stroke, unlike the initial `v` of `volvens` on the page, as 0154 and 0204; found by check 2. |
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
| 0049 | 93 | `dicti prioratus nolumus anteferri` | `volumus` | Document (a papal letter); `n` for `v`; found by check 2. |
| 0050 | 26 | `detensione et tuitione` | `defensione` | Document; a `t`, not reaching the height of the `d`; found by check 2. |
| 0053 | 45 | `M. de Pisis Gradis de mandato` | `Gratis` | Document, the chancery note; found by check 2. |
| 0054 | 31 | `vel mixti, iudicti vel indicendi` | `indicti` | Document; `u` for `n`, unlike the `n` of `indicendi`; found by check 2. |
| 0095 | 67 | `si eris valnes.` | `valens` | Commentary; `n` and `e` transposed; found by check 2. |
| 0097 | 89 | `In angelica fuvella:` | `favella` | Italic lemma (Italian verse `favella`); an italic `u`, open at the top, unlike the `a` of `angelica`; found by check 2. |
| 0125 | 33 | `omnium honorum statutorum` | `bonorum` | Commentary; `h` for `b`; found by check 2. |
| 0148 | 77 | `*Oculos reclos retorsit in obliquum*` | `rectos` | Italic gloss; a tall italic `l`, as in `Oculos`, for `t`; the Latin verse 31 above has `Rectos`; found by check 2. |
| 0216 | 30 | `arere, idest in bonis aliorum` | `avere` | Italic lemma; its second letter is the italic `r` of its fourth, as 0154 and 0204; found by check 2. |
| 0190 | 56 | `dominus Guido, esset mortaus;` | `mortuus` | Commentary; `a` for `u`; found by check 2. |
| 0242 | 33 | `Et quamquem tu veneris multum` | `quamquam` | Latin verse; italic; `e` for `a`; found by check 2. |
| 0258 | 19 | `Già era in loco, dore:` | `dove` | Italic lemma; the italic `r` of `era` beside it, as 0154 and 0204; found by check 2. |
| 0269 | 38 | `Sxus azurrina, sive de` | `Sus` | Commentary; an `x` added; found by check 2. |
| 0274 | 108 | `cum cauda, veluit Virgilius` | `voluit` | Found by check 2. |
| 0295 | 70 | `*piumbat*, id st perpendiculariter` | `est` | Commentary; the `e` not printed; found by check 2. |
| 0299 | 31 | `(11) da Virgllio.` | `Virgilio` | Footnote; `l` for `i`; found by check 2. |
| 0329 | 25 | `Così si ritrhaen sotto e bollori.` | `ritrahen` | Quoted verse; `h` and `a` transposed; found by check 2. |
| 0356 | 94 | `non se fiuxit, idest intelli-` | `finxit` | Commentary; `u` for `n`; found by check 2. |
| 0377 | 69 | `indutus vestibus mulicbribus.` | `muliebribus` | Commentary; `c` for `e`, no bar; found by check 2. |
| 0382 | 93 | `ad intraveder *la nuoca*` | `nuova` | Essay; italic; `c` for `v`; found by check 2. |
| 0409 | 16 | `quod generat maximes feto-` | `maximos` | Commentary; `e` for `o`; found by check 2. |
| 0473 | 49 | `Frater` / `loannes predictus, episcopus Firmanus` | `Ioannes` | Commentary; an `l` with a top serif to the left only, as the `l` of `millesimo`, for `I`; found by check 2. |
| 0475 | 31 | `tutta la classica antichità adoro la *Tellus*` | `adorò` | Essay; the accent not printed; found by check 2. |
| 0490 | 89 | `Invocando Dantes Cailiopem, rogat` | `Calliopem` | Commentary; `i` for `l`; found by check 2. |
| 0511 | 78 | `ruptus michi crat` | `erat` | Commentary; `c` for `e`; found by check 2. |
| 0514 | 68 | `erat` / `deior, et magis aspera` | `peior` | Commentary; `d` for `p`; `peior` later in the line; found by check 2. |
| 0515 | 81–82 | `ad Lu-` / `cillum:` | `Lucilium` | Commentary (Seneca's letters); a second `l`, not an `i`; found by check 2. |
| 0521 | 4 | `*delectacionem, rel per dolorem*` | `vel` | Italic lemma; an italic `r` for `v`; found by check 2. |
| 0527 | 6 | `quando colui da l'altro canco,` | `fianco` | Italian verse; `c` for `fi`; found by check 2. |
| 0533 | 16 | `muitos spiritus` | `multos` | Commentary; `i` for `l`; found by check 2. |
| 0535 | 74 | `quia vulgus signorat` | `ignorat` | Commentary; an `s` added; found by check 2. |
| 0542 | 87 | `Sed ih quemlibet pulverem` | `in` | Commentary; `h` for `n`; found by check 2. |
| 0582 | 70 | `ad contitendum, neminem` | `confitendum` | Commentary; `t` for `f`, the height of the other `t`; found by check 2. |
| 0589 | 48 | `ne, voleus recedere` | `volens` | Commentary; `u` for `n`; found by check 2. |
| 0609 | 4 | `*sice pariter, sicut boves*` | `sive` | Italic lemma; an italic `c` for `v`; found by check 2. |
| 0613 | 81 | `*di sparento*, idest pavefactione` | `spavento` | Italic lemma (Italian verse `spavento`); an italic `r`, unlike the italic `v` of `sapevamo` (0640); found by check 2. |
| 0622 | 50 | `dixit` / `uod ad introytum` | `quod` | Commentary; the `q` not printed; found by check 2. |
| 0625 | 54 | `tertia pars huius cupituli` | `capituli` | Commentary; `u` for `a`; found by check 2. |
| 0630 | 16 | `Figlinolo; poi a Michele` | `Figliuolo` | Essay; `n` for `u`; found by check 2. |
| 0640 | 52 | `famiam, qued in uno loco` | `quod` | Commentary; the third letter has no visible bar (`qucd` or `qued`); found by check 2. |
| 0655 | 32 | `Dolce di madre, dicer: Figlinol mio,` | `Figliuol` | Italian verse; `n` for `u`, as 0630; found by check 2. |
| 0677 | 23 | `Perchè di giugner lui ciascum contende` | `ciascun` | Italian verse; `m` for `n`; found by check 2. |
| 0746 | 96 | `ubi poniuntur illi qui tardaverunt` | `puniuntur` | Commentary; `o` for `u`; found by check 2. |
| 0753 | 18 | `Dal Troso (11) fu, e purga per digiuno` | `Torso` | Italian verse; `r` and `o` transposed; found by check 2. |
| 0762 | 5 | `ma splendito o commovente` | `splendido` | Essay; `t` for `d`; found by check 2. |
| 0799 | 20 | `cauto; dixit ipsa` | `canto` | Commentary; `u` for `n`; found by check 2. |
| 0830 | 80 | `aliis scentiis: dereliquisti me` | `scientiis` | Commentary; the `i` not printed; found by check 2. |
| 0848 | 4 | `A disbramarsi la decente sete,` | `decenne` | Italian verse; `t` for `n`; found by check 2. |
| 0850 | 9 | `Colpa di quella ch'al presente orese,` | `crese` | Italian verse; `o` for `c`; found by check 2. |
| 0877 | 89 | `Qui utres, licent sint eiusdem` | `licet` | Commentary; an `n` added; found by check 2. |
| 0887 | 8 | `. . . fu iunocente l'umana radice,` | `innocente` | Quoted verse; `u` for `n` (a turned letter), as 0146; found by check 2. |
| 0893 | 30 | `(33) a similitudiue` | `similitudine` | Gloss; `u` for `n`; found by check 2. |
| 0894 | 28 | `(44) comprhender` | `comprehender` | Gloss; the `e` not printed; found by check 2. |
| 0894 | 95 | `quod non est dicendam.` | `dicendum` | Commentary; `a` for `u`; found by check 2. |
| 0898 | 77 | `ymaginem omuium faciendorum` | `omnium` | Commentary; `u` for `n`; found by check 2. |
| 0904 | 11 | `de la luua` | `luna` | Gloss; `u` for `n` (a turned letter), as 0146; found by check 2. |
| 0916 | 39 | `famescente et exsitente inter` | `existente` | Commentary; `s` and `i` transposed; found by check 2. |
| 0917 | 54 | `demum redunt ad stellas` | `redeunt` | Commentary; the `e` not printed; found by check 2. |
| 0929 | 91 | `idest ad suum arbitrum, aliquis` | `arbitrium` | Commentary; the `i` not printed; found by check 2. |
| 0958 | 48 | `brutorum et animam plantaram.` | `plantarum` | Commentary; `a` for `u`; found by check 2. |
| 0963 | 108 | `quando cautatur ad duplum` | `cantatur` | Commentary; `u` for `n`; found by check 2. |
| 0966 | 79 | `(fluvius est divideus Marchiam` | `dividens` | Commentary; `u` for `n`; found by check 2. |
| 0966 | 96 | `brachium maris, ubi surt` | `sunt` | Commentary; `r` for `n`; found by check 2. |
| 0980 | 7 | `Vogla di sè a te puot'esser suia.` | `fuia` | Italian verse; `s` for `f`; found by check 2. |
| 0980 | 87 | `Mediterrancum incipit` | `Mediterraneum` | Commentary; `c` for `e`; found by check 2. |
| 0981 | 87 | `draginta aunis` | `annis` | Commentary; `u` for `n`; found by check 2. |
| 0992 | 51 | `in regno Apulic, prope` | `Apulie` | Commentary; `c` for `e`; found by check 2. |
| 1008 | 26 | `scendentale sua iuce` | `luce` | Essay; `i` for `l`; found by check 2. |
| 1019 | 51 | `benigna plus pauperiibus` | `pauperibus` | Commentary; an `i` added; found by check 2. |
| 1022 | 16 | `capitulo Dampuamus.` | `Dampnamus` | Commentary; `u` for `n`; found by check 2. |
| 1031 | 69–70 | `corrupti-` / `lium` | `corruptibilium` | Commentary; `bi` not printed at the line end; found by check 2. |
| 1035 | 55 | `Dottore deila Scolastica` | `della` | Essay; `i` for `l`; found by check 2. |
| 1042 | 106 | `quia contitetur se` | `confitetur` | Commentary; `t` for `f`, the height of the other `t`, as 0582; found by check 2. |
| 1050 | 10 | `(1) voloutà.` | `volontà` | Gloss; `u` for `n`; found by check 2. |
| 1050 | 69 | `remisse trabere,` | `trahere` | A `b`, unlike the `h` of `trahit` on the page; found by check 2. |
| 1066 | 102 | `vel infirmate vestra` | `infirmitate` | Commentary; `it` not printed; found by check 2. |
| 1085 | 10 | `vidit cam pulcherrimam.` | `eam` | Commentary; `c` for `e`; found by check 2. |
| 1099 | 6 | `nè scripse onchiostro,` | `inchiostro` | Italian verse; `o` for `i`; found by check 2. |
| 1099 | 71 | `in iustitia et elementia regnum` | `clementia` | Commentary; `e` for `c`; found by check 2. |
| 1108 | 95 | `danza dei cicli, e di tutte` | `cieli` | Essay; `c` for `e`; found by check 2. |
| 1165 | 79 | `Sancti Iacobi, diceus: Inde` | `dicens` | Commentary; `u` for `n`; found by check 2. |
| 1214 | 71 | `idco dicit Iob` | `ideo` | Commentary; `c` for `e`; found by check 2. |
| 1217 | 13 | `Com'a'Giuderi, tal eclypsi rispose.` | `Giudei` | Italian verse; an `r` added; found by check 2. |
| 1224 | 62 | `scilicet visus, magit tremit` | `magis` | Commentary; `t` for `s`; found by check 2. |
| 1234 | 23 | `Quod d viditur in quatuor partes` | `dividitur` | Commentary; the first `i` not printed, a space; found by check 2. |
| 1246 | 86 | `Eva, mater omuium:` | `omnium` | Commentary; `u` for `n`; found by check 2. |
| 1248 | 5 | `E dal septomo grado in giù` | `septimo` | Italian verse; `o` for `i`; found by check 2. |
| 1255 | 40 | `seute che merita` | `sente` | Essay; `u` for `n`; found by check 2. |
| 1260 | 40 | `quod conserves ei sanes,` | `sanos` | Latin verse; italic; `e` for `o`; found by check 2. |
| 1264 | 59–60 | `et mi-` / `mium admiratione` | `nimium` | Commentary; `m` for `n`; found by check 2. |
| 1269 | 4 | `prima die mensi februarii` | `mensis` | Colophon; the `s` not printed (`mensis ianuarii` in the next line); found by check 2. |
| 1277 | 47 | `nisi maun Conditoris sui` | `manu` | Commentary; the tops of the letters are damaged, their feet show `maun`; found by check 2. |
| 1281 | 27 | `sed etiam in omuibus inferioribus` | `omnibus` | Commentary; `u` for `n`; found by check 2. |
| 1283 | 117 | `cut nix liquetit ex calore` | `liquefit` | Commentary; `t` for `f`, the height of the other `t`, as 0582; found by check 2. |
| 0596 | 57, 71 | `sublimita`, `d'intellettualita` | `sublimità`, `d'intellettualità` | Essay; no accent visible; found by the read-through. |
| 0599 | 21 | `(4) si veuce.` | `vence` | Gloss of `s'adona`; `u` for `n`; found by the read-through. |
| 0607 | 37 | `quel mesto grido informo la scienza` | `informò` | Essay; no accent visible; found by the read-through. |
| 0613 | 95–96 | `filium Na-` / `bar` | `Nabat` | Commentary (Vulgate `filius Nabat`); `r` for `t`; found by the read-through. |

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
  the reader passed over may remain. The read-through ("Read-through") is planned for what
  these checks leave.
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
checks and the checks after completion. The conversion into `texts/la/` is
`texts/scripts/convert_la.py` (procedure, step 11).

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
