# Plan: checking `ocr/la` after its completion

This is the plan for `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), now that it is complete. The completed work (the verse, the two-OCR markup, the
batches, the retyping, the line checks and the conversion), the checks after it (check 1,
the verse check, the italics and check 2) and the part of the read-through done so far
are recorded in [DONE.md](DONE.md); the read-through still to do is under "Read-through".
The "procedure" steps and the "items" cited below are those of DONE.md. The conversion into
`texts/la/` is described in [texts/PLAN.md](../../texts/PLAN.md) ("`texts/la/`"). A short
account of the whole work, for checking the other texts, is in [SUMMARY.md](SUMMARY.md).

**A new session starts here**: read "State". The rules and conventions below are settled:
apply them, do not ask again.

## State (2026-11-08)

`ocr/la` is complete (`0001`–`1296`) and converted into `texts/la/001`–`110`. The checks
for errors that both OCRs share (check 1, the verse check, the italics, check 2) are done
(DONE.md); what they do not cover is under "Known limits".

The read-through ("Read-through") is done: 0001–1296 are read and decided (0001–0400
in `43a1f60`, `9b91553`; DONE.md, "Read-through"); the trial pages 0601–0614 were read
again with the batches. `Eunce` (0799–0867) is the edition's spelling throughout
Serravalle's text (the editors print `Eu[n]ce` on 0867), so it is kept as printed. The
pages after the index (1291–1296) are blank or the library's, with nothing to read.

## Checks

The checks list candidates by script, and every candidate is decided in the image
(`ocr/la/scripts/view.py word`), never from the sense or from another edition. A candidate is one of:

- **misread**: `ocr/la` differs from the print; correct `ocr/la`;
- **printed**: `ocr/la` is as printed; a misprint goes into "Suspected misprints", a form of
  the edition (a spelling of the manuscript, a variant of the quotation) is only recorded;
- **other**: not a reading at all (a split word, a name, Italian in the Latin); recorded.

The decisions are kept in a table per check in `ocr/la/` (`page line form decision note`),
committed with the fixes: those of the checks done are described in DONE.md ("The checks");
the read-through's is `readcheck.tsv`, every flagged place with its decision (`misread`
with the old form in the note, `was …`; `misprint`; `printed`), sorted by page and line.

The misprints are gathered in "Suspected misprints" whatever found them (the markup, a
check, by chance); a `misprint` row of a table is also a row there.

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
- **Done so far** (DONE.md, "Read-through"): the tools, the trial on 0595–0614, the
  batches of 0001–0400.
- **Steps** for each batch of 25 pages (`FIRST`–`LAST`):
  1. `uv run ocr/scripts/pages.py texts/la FIRST LAST -o tmp/read/FIRST-LAST.md` writes the
     pages for the reader; the task file names it and the TSV to write (page, the phrase
     as written, the reason) ([ocr/scripts/README.md](../scripts/README.md), "The
     read-through").
  2. `ocr/scripts/findline.py` finds the lines of the flagged phrases in `ocr/la`; the
     rows of "Suspected misprints" for the batch's pages are looked up, so that a listed
     misprint is not listed twice.
  3. Decisions, each in the image (`ocr/scripts/wordcrop.py ocr/la OUT.png PAGE:TEXT[:N]`,
     a zoom of `ocr/la/PAGE.png` where a letter is unclear): a misreading is corrected in `ocr/la` with
     `ocr/scripts/txtfix.py` (`PAGE:LINE old new`); a misprint goes into "Suspected
     misprints" ("found by the read-through"); every decision is a row of `readcheck.tsv`.
     The settled readings: Serravalle's Latin, its grammar and his way of translating the
     verse are printed; so are the edition's Italian readings and a visible accent. An
     Italian verse that differs from Dante where the Latin shows the right reading, an
     accent missing with none visible, and a sure non-word are misprints. A line-end hyphen
     kept inside an essay line is a misreading.
  4. After the fixes: `texts/scripts/convert_la.py` (only the four `NO NUMBER` lines, 0099
     ×2, 0363, 0856), `ocr/la/scripts/seqcheck.py 79 1270` and
     `ocr/la/scripts/check.py 79 1287`, each compared with its previous output.
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
| 0832 | 89 | `corum pluvium` | `eorum pluviam` | Commentary; the image shows `c`; the verse has `eorum pluviam` (`pluvium` found by the read-through). |
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
| 0023 | 19 | `vi giunse nel 1493, perchè` | `1393` | Editors' preface; he stayed four years and left in 1398; found by the read-through. |
| 0023 | 19 | `nel 1498 n'era partito.` | `1398` | Editors' preface; the same page has `Da Firenze, nel 1398, partì`; found by the read-through. |
| 0026 | 38 | `da Clemente V dal 1381` | `Clemente VII` | Editors' preface; the Avignon antipope of 1378–1394; found by the read-through. |
| 0026 | 39 | `conclave, settembre 1399,` | `1394` | Editors' preface; Benedict XIII followed Clement in 1394 (the same sentence); found by the read-through. |
| 0027 | 13 | `nona sessione (13 marzo 1415)` | `maggio` | Editors' preface; 0026 has `sessione IX, del 13 maggio 1415`; found by the read-through. |
| 0027 | 33 | `al 16 gennaio 1417` | `6 gennaio` | Editors' preface; the paragraph before has `il 6 gennaio dell'anno seguente`; found by the read-through. |
| 0034 | 24 | `la scrittura della seconda mano` | `terza` | Editors' preface; the third hand writes to the end of the Purgatorio (0034, line 5); found by the read-through. |
| 0037 | 26 | `finiva la vita nel 1417.` | `1447` | Editors' preface; Eugene IV died in 1447; found by the read-through. |
| 0041 | 36 | `Ritlettendo noi` | `Riflettendo` | Editors' preface; a `t`, without the hook of an `f`; found by the read-through. |
| 0045 | 60 | `suis, moto simili,` | `motu` | Document; found by the read-through. |
| 0046 | 9, 18, 89, 98, 119 | `aliarum nunc teneantur`, `impedire valeat`, `conferirent`, `alicuius nunc teneantur`, `nos eum tecum` | `minime`, `impediri`, `conferrent`, `minime`, `enim` | Document; found by the read-through. |
| 0047 | 24, 33, 61, 94, 97 | `discretioni nostre`, `quod introduci`, `integre respondi` (twice), `indultum, quos` | `vestre`, `interdici`, `responderi`, `quod` | Document; found by the read-through. |
| 0048 | 39, 42, 106, 120, 121, 126 | `impedi valeat`, `Nunc tamen intentionis`, `preiudicium gravari`, `nos eum tecum`, `si tibi ingere`, `qualiacumque,fecerint,` | `impediri`, `Nostre`, `generari`, `enim`, `vigore`, `fuerint` | Document; found by the read-through. |
| 0049 | 98 | `alicuius anime teneantur` | `minime` | Document; found by the read-through. |
| 0050 | 20, 65 | `in dorsibus, nostris`, `ecclesiasticam apposita postposita` | `diversis`, `appellatione` | Document; found by the read-through. |
| 0051 | 48, 58 | `(31 april. 1409)`, `(31 April. 1409)` | `30` | Dates of Doc. 21 and 22; April has 30 days (Doc. 22 has `ultima dicti mensis Aprilis`); found by the read-through. |
| 0052 | 88, 109 | `partecipantes . . . Carnales.`, `Ei adhuc remanserunt` | `Cardinales`, `Et` | Document; found by the read-through. |
| 0053 | 58 | `Apostolum, magnum genus,` | `gerens` | Document (`magnum gerens singularis devotionis affectum`); found by the read-through. |
| 0059 | 18 | `per me transferreretur` | `transferretur` | Serravalle's preface; found by the read-through. |
| 0060 | 13 | `ineptum et prosumptuosum` | `presumptuosum` | Serravalle's preface; found by the read-through. |
| 0084 | 42 | `in principio matini.` | `matutini` | Lemma; the verse and the gloss have `matutini`; found by the read-through. |
| 0088 | 38, 113 | `maxime nimicantur lupis`, `in orbem terram;` | `inimicantur`, `terrarum` | Commentary (`inimicatur lupis` elsewhere; Wisdom 2:24 `in orbem terrarum`); found by the read-through. |
| 0090 | 19 | `Con lor ti lasserò nel mio partire:` | `lei` | Italian verse I 123 (the Latin `Cum ea`); found by the read-through. |
| 0092 | 9 | `e di la finalmente` | `di là` | Essay; no accent visible; found by the read-through. |
| 0094 | 48, 49 | `matitunale` (twice) | `matutinale` | Commentary; found by the read-through. |
| 0096 | 14 | `Perchè se del veder io m'abbandono,` | `venire` | Italian verse II 34 (the Latin `ad veniendum`, the next line `la venuta`); found by the read-through. |
| 0097 | 13, 65 | `Tal che del domandar io la richiesi.`, `*che di te me dolui*` | `di comandar`, `dolve` | Italian verse II 54 (the Latin `ut preciperet`); the italic lemma has the Latin `dolui` for the verse's `dolve` (line 10); found by the read-through. |
| 0100 | 68, 92 | `*Le la volgare schira*`, `*prompliorem ad veniendum*` | `De la volgare schiera`, `promptiorem` | Italic lemmas (the verse has `schiera`); `prompliorem` an `l`, as tall as the ascenders; found by the read-through. |
| 0102 | 10 | `Non disprezzo dunque, si veramente` | `sì` | Essay; no accent visible; found by the read-through. |
| 0125 | 96 | `*Le quale*: idest de quali` | `Del quale` | Italic lemma (the Italian verse 47 has `del quale`), as 0100 `Le la volgare`; found by the read-through. |
| 0127 | 50, 55, 83 | `si manifesto`, `La Trinita`, `piu ridicole` | `manifestò`, `Trinità`, `più` | Essay; no accent visible; found by the read-through. |
| 0130 | 19, 64 | `*Cosi discesi del cerchio primaio*`, `*Cosi*:` | `Così` | Italic lemmas; the dot as on the other `i`s, and GLM-OCR reads `Cosi` too; found by the read-through. |
| 0133 | 10 | `Ombre portate da la decta briga?` | `Genti, che l'aura nera sì gastiga?` | Italian verse V 51 repeats V 49 (line 8); the Latin has `Gentes`; found by the read-through. |
| 0136 | 13 | `e 'l mondo ancor m'offende` | `modo` | Italian verse V 102 (the Latin `modus`); found by the read-through. |
| 0139 | 19, 31, 35, 39, 43, 44, 85 | `moltiplicita`, `gia`, `necessita`, `costringera`, `serenita`, `profondita`, `puo` | with the accent | Essay; no accent visible; found by the read-through. |
| 0145 | 100 | `*Ego respondidi:` | `respondi` | Italic lemma (the Latin verse 58 has `respondi`); found by the read-through. |
| 0153 | 13, 43 | `Fe'la vendetta dell'eterno strupo.`, `penas quoquot vidi` | `superbo`, `quotquot` | Italian verse VII 12 (the Latin `superbi stupri`; the essay on 0161 quotes `superbo strupo`); Latin verse VII 20; found by the read-through. |
| 0159 | 47 | `*Si spesso vien*` | `Sì` | Italic lemma; no accent visible; found by the read-through. |
| 0161 | 4, 14, 15 | `E segui`, `tratto gia`, `chi penso`, `s'immagino`, `a' di nostri` | `seguì`, `trattò già`, `pensò`, `s'immaginò`, `dì` | Essay; no accent visible; found by the read-through. |
| 0168 | 14 | `dentro all'altre fosse` | `alte` | Italian verse VIII 76 (the Latin `ad altas fossas`); found by the read-through. |
| 0175 | 15, 19 | `Perch'io teneva la parola tronca`, `Che sol per pena la speranza cionca?` | `traeva`, `ha la speranza` | Italian verse IX 14 and 18 (the Latin `trahebam`, `spem habet`); line 19 is a syllable short; found by the read-through. |
| 0183 | 3, 29 | `soltanto, si ancora`, `questa volonta`, `si duplico`, `la societa` | `sì`, `volontà`, `duplicò`, `società` | Essay; no accent visible; found by the read-through. |
| 0192 | 5 | `se riposi mai nostra semenza` | `vostra` | Italian verse X 94 (the Latin `vestrum semen`); found by the read-through. |
| 0193 | 7, 13 | `E nel futuro tenete altro modo.`, `di nostro stato humano` | `presente`, `vostro` | Italian verse X 99 and 105 (the Latin `in presenti`, `de vestro statu`); found by the read-through. |
| 0196 | 8, 13 | `a que' di in Firenze`, `per sempre svani` | `dì`, `svanì` | Essay; no accent visible; found by the read-through. |
| 0201 | 20, 21 | `Qualunque prima sè`, `e froda la sua facultade` | `priva`, `fonde` | Italian verse XI 43–44 (the Latin `privat se`, `fundit`); found by the read-through. |
| 0202 | 19 | `in eterno è consumcto.` | `consunto` | Italian verse XI 66; not a word; found by the read-through. |
| 0205 | 9 | `Per sua natura, e per lo suo seguace` | `sè` | Italian verse XI 110 (the Latin `Per se naturam`); found by the read-through. |
| 0208 | 10, 14 | `la roccia disconscesa,`, `di Creta (3) era discesa,` | `discoscesa`, `distesa` | Italian verse XII 9 and 12 (the Latin `erat distensa`; the rhyme); found by the read-through. |
| 0211 | 86 | `quod lux et amicitia,` | `lis` | Empedocles' strife and love (`amor et discordia`); found by the read-through. |
| 0213 | 71 | `Demum temptarit:` | `temptavit` | Italic lemma (Latin verse `temptavit`); `r` for `v`, as 0154 and 0204; found by the read-through. |
| 0214 | 16, 77 | `Perpendidisti ne vos,`, `magnus miscicus et cognitor erbarum` | `Perpendistis`, `medicus` | Latin verse XII 80 (`vos`); the commentary, not a word; found by the read-through. |
| 0215 | 26 | `Vi vidi gente sotto` | `Io` | Italian verse XII 103 (the Latin `Ego vidi`); found by the read-through. |
| 0218 | 57 | `qui fixit, idest sciscit cor,` | `scidit` | Not a word (`Ille scidit` in the verse); found by the read-through. |
| 0223 | 96 | `Virgo est intructuosa,` | `infructuosa` | Not a word; found by the read-through. |
| 0224 | 96 | `et oinnia facta Imperii` | `omnia` | Not a word; the dot of `i` visible; found by the read-through. |
| 0232 | 7 | `a cui vedemmo di questi di volersi` | `dì` | Essay; no accent visible; found by the read-through. |
| 0239 | 10 | `al tuo dolor furor compito.` | `furor dolor` | Italian verse XIV 66 (the Latin `tuo furori dolor`); found by the read-through. |
| 0241 | 56 | `idest magnus, reglius, idest antiquus` | `veglius` | Italic lemma (Italian `veglio`); `r` for `v`, as 0154, 0204 and 0213; found by the read-through. |
| 0242 | 99 | `que culpa, pentula, purgata` | `pentuta` | Italic lemma (Italian `pentuta`); found by the read-through. |
| 0249 | 87 | `respectu vice infernalis` | `vite` | No stroke of `t` visible; found by the read-through. |
| 0255 | 30, 39 | `non è bonta vera`, `e pero non è colpa` | `bontà`, `però` | Essay; no accent visible; found by the read-through. |
| 0259 | 25 | `sì che tra loro e'l collo` | `'n contrario` | Italian verse XVI (the Latin `in contrarium collum`); found by the read-through. |
| 0261 | 5 | `fossi stato dal loco coperto,` | `foco` | Italian verse XVI (the Latin `ab igne coopertus`); found by the read-through. |
| 0263 | 24 | `Prima da monte volto inver levante` | `Veso` | Italian verse XVI (the Latin `a monte Veso`); found by the read-through. |
| 0267 | 3, 23, 25 | `la societa così`, `non dovra vantarsi`, `da cui si vigorosa` | `società`, `dovrà`, `sì` | Essay; no accent visible; found by the read-through. |
| 0269 | 22 | `venenosam, biffurgutam ad instar` | `bifurcatam` | Not a word; found by the read-through. |
| 0272 | 60–61 | `bivarus se assen-/ctat,` | `assectat` | Not a word (Latin verse `se assectat`); found by the read-through. |
| 0273 | 11, 22 | `fuori scoppiano el lor duolo:`, `par che l'orechie (5) si pasca.` | `scoppiava`, `l'occhio` | Italian verse XVII (the Latin `exibat dolor`, `oculus`); found by the read-through. |
| 0275 | 9 | `c'ha già l'unghia morte,` | `smorte` | Italian verse XVII (the commentary `smorte`); found by the read-through. |
| 0276 | 9 | `sì quinci mi tolse;` | `si` | Italian verse XVII (the Latin `inde se tollit`); found by the read-through. |
| 0277 | 12 | `Rota (2), e discendo,` | `discende` | Italian verse XVII (the Latin `Rotat et descendit`); found by the read-through. |
| 0279 | 68 | `è realtà, e realta potente` | `realtà` | Essay; no accent visible; found by the read-through. |
| 0283 | 17 | `Così da una de le roccie scogli` | `imo` | Italian verse XVIII (the Latin `ab ymo roccie`); found by the read-through. |
| 0301 | 54 | `Ideo stes ibis, idest remane,` | `ibi` | Commentary; found by the read-through. |
| 0303 | 16 | `ed altri arrivino fino credere,` | `fino a credere` | Essay; found by the read-through. |
| 0303 | 34, 40, 72, 73 | `puo`, `felicita`, `piu`, `legittimita` | `può`, `felicità`, `più`, `legittimità` | Essay; no accent visible; found by the read-through. |
| 0323 | 20 | `Et elli havean del cul facto trombetta.` | `havea` | Italian verse XXI (the Latin `Et ille fecerat`); found by the read-through. |
| 0325 | 20 | `colla volonta` | `volontà` | Essay (a quotation); no accent visible; found by the read-through. |
| 0330 | 22 | `Io fui del regno di Ravenna nato.` | `Navarra` | Italian verse XXII (the Latin `de regno Navarre`); found by the read-through. |
| 0337 | 28 | `et vadunt veilata facie,` | `velata` | Commentary; found by the read-through. |
| 0344 | 29 | `Ego fui natus ed adultus` | `et` | Latin verse (the commentary `natus et adultus`); found by the read-through. |
| 0349 | 45 | `ut quisque fugiat cum et libenter` | `eum` | Commentary; found by the read-through. |
| 0350 | 6 | `Quando la brina in su la terra sempra` | `assempra` | Italian verse XXIV (the Latin `exemplatur`); found by the read-through. |
| 0351 | 20 | `Dolce, ch'io vidi prima a piè del ponte.` | `monte` | Italian verse XXIV (the Latin `ad pedem montis`); found by the read-through. |
| 0353 | 13 | `E cieco più assai che quel di pria.` | `erto` | Italian verse XXIV (the Latin `altus`); found by the read-through. |
| 0354 | 32 | `et sanguis adhuc scipantur.` | `stipantur` | Latin verse (the commentary `stipantur`); found by the read-through. |
| 0359 | 14 | `delle nobili facolta,` | `facoltà` | Essay; no accent visible; found by the read-through. |
| 0369 | 90 | `*Aborra*, idest obetrat.` | `oberrat` | Commentary; found by the read-through. |
| 0389 | 111 | `deponere vel eta recolligere sartas,` | `vela et` | Commentary (the verse `vela et`); found by the read-through. |
| 0392 | 58 | `Et ira vestitus eundo me rancuro.` | `ita` | Latin verse (the commentary `et ita vestitus`); found by the read-through. |
| 0394 | 75 | `o sulla possibilità della cosa, fondo` | `fondò` | Essay; no accent visible; found by the read-through. |
| 0398 | 23 | `Modum nunc bolgie turpis.` | `none` | Latin verse (the commentary `none bolgie`); found by the read-through. |
| 0363 | 9 | `Ribiadendo sè stessa sì dinanzi,` | `Ribadendo` | Italian verse XXV (the commentary `ribadendose`); found by the read-through. |
| 0366 | 21 | `Dov'in nessun l'ymagine perversa` | `Due e` | Italian verse XXV (the Latin `Duo et`); found by the read-through. |
| 0366 | 89 | `cum lentu passu.` | `lento` | Commentary (the verse `cum lento passu`); found by the read-through. |
| 0367 | 15 | `Del misero Sabellio e di Massidio,` | `Nasidio` | Italian verse XXV (the Latin `Nassidio`, the commentary `Nasidio`); found by the read-through. |
| 0367 | 16 | `Et attend' a udir quel ch'or si toccha.` | `scocca` | Italian verse XXV (the Latin `scoccatur`); found by the read-through. |
| 0368 | 12 | `Che si perdea ella, e la sua pelle` | `là` | Italian verse XXV (the Latin `ibi`); found by the read-through. |
| 0368 | 26 | `42 Quel ch'era dietro, el trasse ver le tempie;` | `dritto` | Italian verse XXV (the Latin `rectus`); found by the read-through. |
| 0378 | 28 | `E delli sensi humani (12) e del valore:` | `vizi` | Italian verse XXVI (the Latin `vitiis`); found by the read-through. |
| 0379 | 18 | `(7) di Vi-` | `Gi-` | Footnote; `Vi-`/`bilterra` for `Gibilterra`; found by the read-through. |
| 0382 | 30 | `gloria al Newton, e dall'averla cosi mirabilmente espressa nel` | `così` | Essay; no accent visible; found by the read-through. |
| 0389 | 105 | `scivi omnia, et ita duxi corum artes,` | `eorum` | Commentary (the verse `eorum artes`); found by the read-through. |
| 0392 | 28 | `E sì vestito (19) andando mi raccuro (20).` | `rancuro` | Italian verse XXVII (the Latin `me rancuro`); found by the read-through. |
| 0393 | 5 | `44 Quand'ebbe suo desir così compiuto,` | `dir` | Italian verse XXVII (the Latin `dictum`); found by the read-through. |
| 0394 | 25 | `trare in Forli, si rendeva penitente nell'Ordine Francescano.` | `Forlì` | Essay; no accent visible; found by the read-through. |
| 0394 | 28 | `non sarebbe stata si forte, che non ricadesse;` | `sì` | Essay; no accent visible; found by the read-through. |
| 0397 | 80 | `Christi, memor corum, que viderat` | `eorum` | Commentary; found by the read-through. |
| 0407 | 36 | `di merito, di gloria, di felicita, riduconsi ad un giuoco ignobile` | `felicità` | Essay; no accent visible; found by the read-through. |
| 0407 | 64 | `futura; della quale bensi, non possedendola noi in proprio, e` | `bensì` | Essay; no accent visible; found by the read-through. |
| 0407 | 66 | `essere degni. E così l'odio pon è che il sentimento esagerato di` | `non` | Essay; found by the read-through. |
| 0410 | 46 | `Et ego dixi Po te,` | `Poete` | Commentary lemma; a gap for the `e`; found by the read-through. |
| 0416 | 10 | `Arder a tal, ch'io havea per figlolo.` | `che l'` | Italian verse XXIX (the Latin `qui eum`); found by the read-through. |
| 0417 | 5 | `45 Ma perchè sappi (1) che sì ti seconda` | `chi` | Italian verse XXIX (the Latin `quis`); found by the read-through. |
| 0418 | 31 | `Si che la faccia mia ben ti risponda:` | `Sì` | Essay; no accent visible; found by the read-through. |
| 0418 | 32 | `Si vedrai ch'io son l'ombra di Capocchio,` | `Sì` | Essay; no accent visible; found by the read-through. |
| 0418 | 54 | `e presenti quel che la scienza e l'arte arriverebbero a trovare:` | `presentì` | Essay; no accent visible; found by the read-through. |
| 0418 | 57 | `stabili che l'uomo possa arrivare, affinchè cresca ogni dì più` | `stabilì` | Essay; no accent visible; found by the read-through. |
| 0418 | 62 | `Si vedrai ch'io son l'ombra di Capocchio,` | `Sì` | Essay; no accent visible; found by the read-through. |
| 0424 | 20 | `25 Ivi (12) è Romena (13) là, dov'io lassai` | `falsai` | Italian verse XXX (the Latin `falsificavi`); found by the read-through. |
| 0424 | 25 | `Per Fonte Blanda (17) non darei la vista.` | `Branda` | Italian verse XXX (the Latin `Fontem Brandam`); found by the read-through. |
| 0426 | 26 | `41 A te sia reo la sete onde ti crepa,` | `rea` | Italian verse XXX (the Latin `rea sitis`); found by the read-through. |
| 0429 | 86 | `flettendo, trova anche di presente si rispetto alle prime come` | `sì` | Essay; no accent visible; found by the read-through. |
| 0429 | 89 | `senza posa aspira, e nei cui splendori trovera da ultimo il suo` | `troverà` | Essay; no accent visible; found by the read-through. |
| 0429 | 90 | `appagamento, la piena sua felicita.` | `felicità` | Essay; no accent visible; found by the read-through. |
| 0431 | 33 | `primo Nembroth, et quilibet corum habet cornu` | `eorum` | Commentary; found by the read-through. |
| 0440 | 32 | `Cosi in Cristo e per Cristo, nella cui virtù,` | `Così` | Essay; no accent visible; found by the read-through. |
| 0444 | 10 | `Me' (5) sreste stati qui (6) pecore o zebe (7).` | `sareste` | Italian verse XXXII; found by the read-through. |
| 0451 | 3 | `Severissimo sempre l'Alighieri si ne'concetti e si ne'modi di` | `sì` (twice) | Essay; no accent visible; found by the read-through. |
| 0451 | 27 | `ha di più caro, sempre conchiudendo che quel fuoco restera` | `resterà` | Essay; no accent visible; found by the read-through. |
| 0451 | 32 | `Non fece al corso suo si grosso velo` | `sì` | Essay, a verse quoted; no accent visible; found by the read-through. |
| 0451 | 93 | `quasi delitto, a cui la natura umana, cosi finita nel bene come` | `così` | Essay; no accent visible; found by the read-through. |
| 0458 | 5 | `26 Quand'ebbe (1) decto ciò, cho gl'ochi torti` | `con` | Italian verse XXXIII; found by the read-through. |
| 0464 | 14 | `bacio dell'infame che cosi lo consegnava in mano a' nemici!` | `così` | Essay; no accent visible; found by the read-through. |
| 0464 | 29 | `me Christus (*Ad Gal*. II). » Cosi fu inesorabile con ogni ma-` | `Così` | Essay; no accent visible; found by the read-through. |
| 0471 | 103 | `*Prima che de l'abisso me direlle*.` | `divella` | Commentary lemma; an italic `r` for `v` (the verse `divella`); found by the read-through. |
| 0475 | 36 | `divinita nel suo centro, senza un fatto e una tradizione per` | `divinità` | Essay; no accent visible; found by the read-through. |
| 0475 | 55 | `Ma libera da Lui, che si la sprona.` | `sì` | Essay, a verse quoted; no accent visible; found by the read-through. |
| 0475 | 68 | `commesso col voler addiventare simile all'Altissimo. Gli da tre` | `dà` | Essay; no accent visible; found by the read-through. |
| 0476 | 13 | `(scriveva un profondo filosofo e teologo), nè pertanto puo se-` | `può` | Essay; no accent visible; found by the read-through. |
| 0494 | 11 | `Hor che di là dal mar io fo dimora,` | `mal fiume` | Italian verse I (the Latin `ultra malum flumen`); found by the read-through. |
| 0496 | 8 | `41 Quando noi fummo la du' (1) la rogiada` | `là` | Italian verse I; no accent visible; found by the read-through. |
| 0505 | 9 | `Perchè l'ombra sorrise e si ritrassi,` | `ritrasse` | Italian verse II (the Latin `se retraxit`); found by the read-through. |
| 0506 | 12 | `Inamoroso all’amoroso canto,` | `Memoria o uso` | Italian verse II (the Latin `Memoriam et usum`); found by the read-through. |
| 0507 | 19 | `Questi senza mostrar l'usato argoglo,` | `Queti` | Italian verse II (the Latin `Quiete`); found by the read-through. |
| 0507 | 25 | `Com'huom che va ne sà dove s'arrescha (4):` | `nè` | Italian verse II; no accent visible on `ne`; found by the read-through. |
| 0508 | 72 | `nostro amore, il quale dall'amor di lui si parti e nello stesso` | `partì` | Essay; no accent visible; found by the read-through. |
| 0514 | 10 | `Che 'nverso 'l ciel più alta si dissala?` | `Sì che possa salir chi va senz'ala?` | Italian verse III; a wrong line (the Latin `Ita quod possit ascendere qui vadit sine ala`); found by the read-through. |
| 0515 | 20 | `29 Si vid'io a venir muover la testa` | `Sì` | Italian verse III; no accent visible; found by the read-through. |
| 0523 | 106 | `spiribus remanentibus, statim quod a nobis *schiera*, idest` | `spiritibus` | Commentary; found by the read-through. |
| 0525 | 16 | `Tanto che l'anghio sotto a' piè mi fue.` | `'l cinghio` | Italian verse IV (the Latin `cingulum`); found by the read-through. |
| 0526 | 11 | `22 Tu yederesti 'l zodiaco rubechio` | `vederesti` | Italian verse IV; `y` for `v`; found by the read-through. |
| 0527 | 11 | `27 Chè 'l mezzo cerchio del monte superno,` | `moto` | Italian verse IV (the Latin `motus`); found by the read-through. |
| 0527 | 18 | `Quand'havemo ad andar, che 'l poggio sale` | `Quant'` | Italian verse IV (the Latin `Quantum`); found by the read-through. |
| 0527 | 24 | `Tanto, che 'n andar ti fie leggiero,` | `su andar` | Italian verse IV (the Latin `sursum ire`); found by the read-through. |
| 0527 | 60 | `vadat ad ymum, quando illi` | `unum` | Commentary (the verse `Ad unum`); found by the read-through. |
| 0531 | 31 | `prima e nativa fonte di verita;` | `verità` | Essay; no accent visible; found by the read-through. |
| 0535 | 21 | `Venian genti innanzi a noi um poco,` | `un` | Italian verse V; `m` for `n`; found by the read-through. |
| 0539 | 16 | `Perch'io vo'tra costor con lieta fronte.` | `bassa` | Italian verse V (the Latin `demissa`); found by the read-through. |
| 0541 | 16 | `Nell'altro, e sciolse al mio pecto la croce,` | `Nell'Arno` | Italian verse V (the Latin `In Arnum`); found by the read-through. |
| 0542 | 62 | `qui eum extollerunt, non in marmoreum` | `extulerunt` | Essay, a Latin quotation; found by the read-through. |
| 0545 | 6 | `Volgendo allora qua e là la faccia,` | `a loro` | Italian verse VI (the Latin `eis`); found by the read-through. |
| 0545 | 18 | `Menar di qua, la donna di Brabante,` | `Mentr'è` | Italian verse VI (the Latin `Dum est`); found by the read-through. |
| 0550 | 6 | `Monandi e Filippeschi, uom senza cura:` | `Monaldi` | Italian verse VI (the Latin `Monaldos`); found by the read-through. |
| 0551 | 8 | `43 Fiorenze mia, ben puoi esser contenta` | `Fiorenza` | Italian verse VI (the Latin `Florentia`); found by the read-through. |
| 0551 | 59 | `custos thesauri Tarpec.` | `Tarpei` | Commentary; `c` for `i`; found by the read-through. |
| 0553 | 17 | `anzi nella vita di la sono più vive che mai` | `là` | Essay; no accent visible; found by the read-through. |
| 0553 | 21 | `una sola cosa con quello di la.` | `là` | Essay; no accent visible; found by the read-through. |
| 0553 | 25 | `ut mitiges ci a diebus malis.` | `ei` | Essay, a psalm quoted; the same `c` as in `ci` on the page; found by the read-through. |
| 0563 | 10 | `Questi ha ne'regni suoi miglor uscita.` | `rami` | Italian verse VII (the Latin `in ramis`); found by the read-through. |
| 0564 | 35 | `Mentre che l'orizzonte il di tien chiuso.` | `dì` | Essay, a verse quoted; no accent visible; found by the read-through. |
| 0566 | 5 | `Lo dì ch'àn dicto e'dolci amici: A Dio;` | `a' dolci` | Italian verse VIII (the Latin `dulcibus amicis`); found by the read-through. |
| 0566 | 6 | `2 Così lo nuovo peregrin d'amore` | `E che` | Italian verse VIII (the Latin `Et quod`); found by the read-through. |
| 0567 | 19 | `Quasi aspectando tacito et humile:` | `pallido` | Italian verse VIII (the Latin `pallidum`); found by the read-through. |
| 0570 | 7 | `Le quai convien che, misero, ancor brami.` | `misera` | Italian verse VIII (the Latin `misera`); found by the read-through. |
| 0570 | 8 | `26 Per lei assai di lei vi si comprende,` | `di lieve` | Italian verse VIII (the Latin `de levi`); found by the read-through. |
| 0571 | 18 | `Dicendo: Vedi la 'l nostro adversaro;` | `là` | Italian verse VIII; no accent visible; found by the read-through. |
| 0572 | 20 | `40 Chiamato fui Currado Melespina:` | `Malaspina` | Italian verse VIII (the Latin `Malaspina`); found by the read-through. |
| 0572 | 88 | `de parte vicina, scis, die` | `dic` | Commentary (the verse `dic illud`); found by the read-through. |
| 0573 | 13 | `Del pregio di bontade e della spada.` | `della borsa` | Italian verse VIII (the Latin `burse`); found by the read-through. |
| 0574 | 12 | `l'aveva si cara, invocando` | `sì` | Essay; no accent visible; found by the read-through. |
| 0579 | 8 | `9 Fra me pensava: Forse questa siede` | `fiede` | Italian verse IX (the Latin `ferit`); found by the read-through. |
| 0579 | 10 | `Disdegnan di portarne suso in piede.` | `Disdegna` | Italian verse IX (the Latin `Dedignatur`); found by the read-through. |
| 0579 | 11 | `10 Poi mi parea, che giù rotata un poco,` | `più` | Italian verse IX (the Latin `magis rotando`); found by the read-through. |
| 0579 | 14 | `11 Ivi parea che d'ella et io ardesse,` | `ch'ella` | Italian verse IX (the Latin `quod ipsa et ego`); found by the read-through. |
| 0581 | 14 | `27 Come l'ochio più e più v'apersi,` | `E come` | Italian verse IX; `E` left out (the Latin `Et sicut`); found by the read-through. |
| 0594 | 6 | `L'ymagine di tante humilitadi` | `L'ymagini` | Italian verse X (the Latin `Ymagines`); found by the read-through. |
| 0594 | 22 | `E non so io che, nel veder, vaneggio.` | `non so che, sì nel veder` | Italian verse X (the Latin `nescio quid, ita in videre`); found by the read-through. |
| 0599 | 8 | `4 Come del suo buon voler gl'angeli tuoi` | `del suo voler` | Italian verse XI; `buon` added (the Latin `de suo velle`); found by the read-through. |
| 0605 | 37 | `[ecplanas:` | `explanas` | Latin verse 40, runover; found by the read-through. |
| 0615 | 35 | `Quantum ego calcavi quousquam inclinatus ivi.` | `quousque` | Latin verse 23 (Italian `fin che`); found by the read-through. |
| 0616 | 28 | `Ma quinci e quindi l'altra pietra rade.` | `l'alta` | Italian verse XII (the Latin `alta petra`); found by the read-through. |
| 0617 | 12 | `Et esser mi parea troppo pur lieve,` | `più` | Italian verse XII (the Latin `magis levis`); found by the read-through. |
| 0619 | 6 | `poichè dalla virtu ammirata nasce` | `virtù` | Essay; no accent visible; found by the read-through. |
| 0619 | 9 | `doci dalla servitu del peccato` | `servitù` | Essay; no accent visible; found by the read-through. |
| 0619 | 20 | `Egli guardo, e` | `guardò` | Essay, a verse quoted; no accent visible; found by the read-through. |
| 0619 | 26 | `Si vid'ei li, ma di miglior sembianza,` | `Sì`, `lì` | Essay, a verse quoted; no accents visible; found by the read-through. |
| 0619 | 42 | `e l'infinita della virtu, il nulla` | `l'infinità`, `virtù` | Essay; no accents visible; found by the read-through. |
| 0619 | 56 | `e pero Dio, virtu infinita e somma` | `però`, `virtù` | Essay; no accents visible; found by the read-through. |
| 0619 | 58–59 | `Da cio segue, come profondamente gia avvisava Agostino,` / `che nell'umilta stia` | `ciò`, `già`, `umiltà` | Essay; no accents visible; found by the read-through. |
| 0619 | 64 | `Quindi dall'umilta nasce la carità` | `umiltà` | Essay; no accent visible; found by the read-through. |
| 0619 | 72 | `termine non puo essere` | `può` | Essay; no accent visible; found by the read-through. |
| 0619 | 77 | `giogo di servitu, contrazione` | `servitù` | Essay; no accent visible; found by the read-through. |
| 0622 | 50 | `uod ad introytum huius circuli` | `quod` | Commentary; `q` left out; found by the read-through. |
| 0623 | 19 | `Com poco tempo, per la vogla pronta.` | `Con` | Italian verse XIII (the Latin `Cum`); found by the read-through. |
| 0625 | 11 | `17 E poi che fummo um poco più avanti,` | `un` | Italian verse XIII; found by the read-through. |
| 0625 | 54 | `hec est tertia pars huius cupituli` | `capituli` | Commentary; found by the read-through. |
| 0626 | 8 | `23 E com'agl'ochi non approda el sole,` | `agl'orbi` | Italian verse XIII (the Latin `orbis`); found by the read-through. |
| 0629 | 20 | `Però col pregio tuo talhor mi giova` | `priego` | Italian verse XIII (the Latin `cum rogamine tuo`); found by the read-through. |
| 0630 | 46 | `E pero il Poeta` | `però` | Essay; no accent visible; found by the read-through. |
| 0636 | 10 | `Che non trovan ingegno che le occupi (6).` | `temono` | Italian verse XIV (the Latin `non timent`); found by the read-through. |
| 0637 | 7 | `Da quel che parte el perigo e gl'affanni;` | `l'assanni` | Italian verse XIV (the Latin `assannet`); found by the read-through. |
| 0637 | 23 | `29 Seme d'invidia cotal pigla mieto (6).` | `Di mia semenza`, `paglia` | Italian verse XIV (the Latin `De meo semine tales paleas`); found by the read-through. |
| 0637 | 97 | `o gens humana, exselamando dicit` | `exclamando` | Commentary; found by the read-through. |
| 0639 | 47–48 | `vir` / `tuosus` | `vir-` | Commentary; no hyphen printed at the line end (`texts/la` joins it: `HYPHEN_MISSING` in `convert_la.py`); found by the read-through. |
| 0640 | 52 | `qued in uno loco esset guelfus` | `quod` | Commentary; found by the read-through. |
| 0641 | 16 | `Che dovria l'hom tener dentr'a suo meta (6).` | `sua` | Italian verse XIV (the Latin `sua metam`); found by the read-through. |
| 0643 | 68 | `insieme possesso e liberta, comunanza` | `libertà` | Essay; no accent visible; found by the read-through. |
| 0643 | 93 | `non puo` | `può` | Essay; no accent visible; found by the read-through. |
| 0643 | 96 | `e quelle piu gravi` | `più` | Essay; no accent visible; found by the read-through. |
| 0647 | 16 | `Salendo, su per lo mondo, parechio` | `modo` | Italian verse XV (the Latin `per modum`); found by the read-through. |
| 0647 | 22 | `Perchè a veder la mia luce fu racta.` | `a fuggir la mia vista` | Italian verse XV (the Latin `ad fugiendum mea visio`); found by the read-through. |
| 0647 | 25 | `Ex co quia per nos circumdatus erat` | `eo` | Latin verse 3; an italic `c` for `e`; found by the read-through. |
| 0652 | 9 | `37 E lui (7) vedea chinarsi (3) per la morte,` | `(8)` | Italian verse XV; the note mark, the note is `(8) in ginocchione`; found by the read-through. |
| 0652 | 75–76 | `et sic de Phsi-` / `strato` | `Phisistrato` | Commentary; found by the read-through. |
| 0656 | 29–30 | `e vi sara` / `perdonato` | `sarà` | Essay; no accent visible; found by the read-through. |
| 0660 | 15 | `Per tornar bella a colui che mi (8) fece,` | `ti` | Italian verse XVI (the Latin `te`); found by the read-through. |
| 0660 | 20 | `13 Allora incominciai (11): Con quelle fascia (12),` | `quella` | Italian verse XVI (the Latin `illa`); found by the read-through. |
| 0664 | 100–101 | `bene exem-` / `plicare` | `exemplificare` | Commentary; found by the read-through. |
| 0666 | 72 | `boni viri. Couradus` | `Conradus` | Commentary; `u` for `n`; found by the read-through. |
| 0668 | 1 | `LA LIBERTA UMANA E LA SUPREMA SUA LEGGE` | `LIBERTÀ` | Essay title; no accent visible; found by the read-through. |
| 0669 | 16 | `ex co quod` | `eo` | Commentary; `c` for `e`; found by the read-through. |
| 0671 | 5 | `4 Sì, pareggiando e miei com passi fidi` | `con` | Italian verse XVII; found by the read-through. |
| 0673 | 5 | `14 Come si piange 'l son (1), ove di bucto` | `frange` | Italian verse XVII (the Latin `frangitur`); found by the read-through. |
| 0677 | 23 | `Perchè di giugner lui ciascum contende (14).` | `ciascun` | Italian verse XVII; found by the read-through. |
| 0679 | 16 | `In verita, chi guardi` | `verità` | Essay; no accent visible; found by the read-through. |
| 0679 | 39 | `fuori della realta` | `realtà` | Essay; no accent visible; found by the read-through. |
| 0679 | 57 | `linga aridita del deserto` | `aridità` | Essay; no accent visible; found by the read-through. |
| 0682 | 5 | `Ne la mia vista s'io parea conto (2):` | `contento` | Italian verse XVIII (the Latin `contentus`); found by the read-through. |
| 0685 | 16 | `Come per verdi frondi in pianta vita.` | `viva` | Italian verse XVIII (the Latin `viva`); found by the read-through. |
| 0685 | 19 | `Et è prima appettibile l'effecto,` | `l'affecto` | Italian verse XVIII (the Latin `affectus`); found by the read-through. |
| 0686 | 74 | `uon sentitur, idest cognoscitur` | `non` | Commentary; `u` for `n`; found by the read-through. |
| 0687 | 12 | `Cortese più che nulla mantovana,` | `Pietola più che villa` | Italian verse XVIII (the Latin `Piectola plus quam villa`); found by the read-through. |
| 0687 | 14 | `29 Perch'io quella ragion ch'aperta e chiara` | `piana` | Italian verse XVIII (the Latin `apertam et planam`); found by the read-through. |
| 0689 | 15 | `Che tosto piangerà quel ministero,` | `monastero` | Italian verse XVIII (the Latin `monasterium`); found by the read-through. |
| 0691 | 45 | `dalla radicalita del sentimento` | `radicalità` | Essay; no accent visible; found by the read-through. |
| 0691 | 61 | `della virtu, della scienza` | `virtù` | Essay; no accent visible; found by the read-through. |
| 0691 | 67 | `ma questa dualita` | `dualità` | Essay; no accent visible; found by the read-through. |
| 0694 | 5 | `Vinto da terra, o talhor dall'autumpno (1);` | `da Saturno` | Italian verse XIX (the Latin `a Saturno`); found by the read-through. |
| 0694 | 40–41 | `Ego me iam genutlexeram;` / `Io m'era ingionecchiato,` | `genuflexeram`, `inginocchiato` | Commentary, the incipits of the third part; found by the read-through. |
| 0697 | 92 | `*Animas domns*: idest potestatem` | `domnas` | Italic lemma (the verse `domnas`); found by the read-through. |
| 0701 | 59 | `*Già era ingionecchiato*:` | `inginocchiato` | Italic lemma (the verse `inginocchiato`); found by the read-through. |
| 0703 | 90 | `non resta di la che` | `là` | Essay; no accent visible; found by the read-through. |
| 0710 | 11 | `23 Karlo (6) venne in Italia, e, per vicenda (7),` | `ammenda` | Italian verse XX (the Latin `emendationem`); found by the read-through. |
| 0715 | 19 | `Finchè 'l tremar cessò, et io 'l compresi.` | `el compièsi` | Italian verse XX (the Latin `ille completus est`); found by the read-through. |
| 0716 | 6 | `Mi fe' desiderando di sapere,` | `desideroso` | Italian verse XX (the Latin `avidum`); found by the read-through. |
| 0717 | 62 | `un progresso di eternita` | `eternità` | Essay; no accent visible; found by the read-through. |
| 0717 | 73 | `sara traslatato` | `sarà` | Essay; no accent visible; found by the read-through. |
| 0717 | 81 | `gli spiriti gia beati` | `già` | Essay; no accent visible; found by the read-through. |
| 0720 | 8 | `E conduceami a la giusta vendecta.` | `condoleami` | Italian verse XXI (the Latin `condolebam`); found by the read-through. |
| 0720 | 37 | `E 'l savio duca: Omai viggio la rethe,` | `veggio` | Italian verse XXI; found by the read-through. |
| 0721 | 19 | `Chi v'à per la sua scala tante scorte?` | `tanto` | Italian verse XXI (the Latin `tantum`); found by the read-through. |
| 0722 | 5 | `9 Ma per colei (1) che dì e nocte fila.` | `perchè lei` | Italian verse XXI (the Latin `Sed quia illa`); found by the read-through. |
| 0722 | 10 | `Però ch'al nostro mondo non adochia.` | `modo` | Italian verse XXI (the Latin `ad modum`); found by the read-through. |
| 0722 | 17 | `13 Sì mi diè, domandando, per la cuna` | `cruna` | Italian verse XXI (the Latin `crunam`); found by the read-through. |
| 0723 | 24–25 | `Che, tutt'è libero a mutar convento,` / `L'alma sorpiendo` | `tutta libera`, `sorprende` | Italian verse XXI (the Latin `tota libera`); found by the read-through. |
| 0723 | 105 | `*que se moreat*` | `moveat` | Italic lemma (the verse `moveat`); found by the read-through. |
| 0727 | 16 | `Forse (10) a cantar degl'huomini e de' Dei.` | `Forza` | Italian verse XXII (the Latin `fortia`); found by the read-through. |
| 0728 | 8 | `E condoliemi alla giusta vendetta.` | `condoleami` | Essay, a verse quoted; found by the read-through. |
| 0730 | 8 | `Con Sitio senza o i o forniro.` | `senz'altro ciò` | Italian verse XXII; found by the read-through. |
| 0731 | 19 | `La pura fede in tucto mi scagiona:` | `E come amico omai meco ragiona` | Italian verse XXII, a wrong line (the Latin `Et sicut amicus ammodo michi ratiocineris`); found by the read-through. |
| 0732 | 12 | `Esser, ch'io fossi avaro in la tua vita,` | `altra` | Italian verse XXII (the Latin `in alia vita`); found by the read-through. |
| 0732 | 15–16 | `Troppo da me; a questa dismisura` / `E miglar (1) di lunari` | `e questa`, `Miglar` | Italian verse XXII (the Latin `et hanc`, `Milliaria`); found by the read-through. |
| 0732 | 28 | `Tragge 'l pensier vivendo, nelli stremi!` | `penter` | Italian verse XXII (the Latin `penitere`); found by the read-through. |
| 0733 | 7 | `insieme qui suo veder secca.` | `verde` | Italian verse XXII (the Latin `cum viridi`); found by the read-through. |
| 0733 | 25 | `(9) tocha — (9) crystiana.` | `(10)` | The notes; the second mark; found by the read-through. |
| 0734 | 47 | `Apparuerunt michi postmodum tanctum sancti,` | `tantum` | Latin verse 28; found by the read-through. |
| 0735 | 11 | `33 Dimmi dov'è Terentio nostro amico,` | `antico` | Italian verse XXII (the Latin `antiquus`); found by the read-through. |
| 0735 | 39 | `Quem musse lactaverunt` | `muse` | Latin verse; found by the read-through. |
| 0736 | 11 | `39 Tacevansi amendue li poeti,` | `amendue già` | Italian verse XXII; `già` left out (the Latin `iam`); found by the read-through. |
| 0736 | 15 | `Rimase indietro, et a la quinta el temo (12),` | `e la quinta era al` | Italian verse XXII (the Latin `et quinta erat`); found by the read-through. |
| 0737 | 12 | `Cadea dell'altra (4) roccia (5)` | `alta` | Italian verse XXII (the note `al. alta`, the Latin `alta`); found by the read-through. |
| 0737 | 68 | `reperuimus in medio strate` | `reperimus` | Commentary; found by the read-through. |
| 0738 | 21 | `(3) Giovanni — (5) al. ond'elli è — (6) Matth. XI cap. — (7) a noi è.` | `(4)`, `(5)`, `(6)` | The notes, numbered one too high (the verse marks `(4)`–`(6)`); found by the read-through. |
| 0739 | 5–64 | `reita`, `prodigalita`, `virtu`, `un di`, `verita`, `potra`, `puo`, `sara`, `eternita` | `reità`, … | Essay; no accents visible on the page; found by the read-through. |
| 0742 | 5 | `Chi dietro agl'ucellin lor (3) vita perde;` | `sua` | Italian verse XXIII (the Latin `suam`); found by the read-through. |
| 0744 | 21 | `Crisiton esset factus siccus,` | `Erisiton` | Latin verse (Italian `Herysithone`); an italic `C` for `E`; found by the read-through. |
| 0745 | 11–12 | `riconosciuto 'l viso (2);` / `Ma nella faccia sua` | `al viso`, `voce` | Italian verse XXIII (the Latin `ad faciem`, `in voce`); found by the read-through. |
| 0746 | 11 | `22 Tuct'esta gente che piangendo è tanta,` | `canta` | Italian verse XXIII (the Latin `cantat`); found by the read-through. |
| 0746 | 20 | `25 Chè quella vogla agl'alberi ci mena,` | `all'albero` | Italian verse XXIII (the Latin `ad arborem`); found by the read-through. |
| 0746 | 96 | `ubi poniuntur illi qui tardaverunt` | `puniuntur` | Commentary; found by the read-through. |
| 0747 | 10 | `E liberato m'ha di questi (3) giri.` | `degl'altri` | Italian verse XXIII (the Latin `de aliis`); found by the read-through. |
| 0747 | 14 | `32 Chè la Bardaggia di Sardigna assai` | `Barbagia` | Italian verse XXIII (the Latin `Barbagia`); found by the read-through. |
| 0747 | 66 | `planctu diructo, idest continuato.` | `dirupto` | Commentary (the verse `dirupto`); found by the read-through. |
| 0747 | 96 | `in pulpitu e` | `pulpito et` | Commentary; found by the read-through. |
| 0749 | 6 | `Salendo e riguardando la montagna (1),` | `rigirando` | Italian verse XXIII (the Latin `circumeundo`); found by the read-through. |
| 0750 | 7–32 | `cosi buona`, `ci da`, `si cara e si diletta` | `così`, `dà`, `sì` | Essay; no accents visible; found by the read-through. |
| 0753 | 12 | `Di nominar ciascun, da ch'è si munta` | `sì` | Italian verse XXIV; no accent visible; found by the read-through. |
| 0753 | 18 | `Dal Troso (11) fu, e purga per digiuno` | `Torso` | Italian verse XXIV (the Latin `De Torso`); found by the read-through. |
| 0755 | 7 | `La mia città, com' huom che la riprenda.` | `come ch'huom` | Italian verse XXIV (the Latin `quamquam homo`); found by the read-through. |
| 0756 | 13 | `E per magrezza e per volar leggiera.` | `voler` | Italian verse XXIV (the Latin `voluntatem`); found by the read-through. |
| 0757 | 13 | `Ciò che 'l mi dir più dichiarar non puote.` | `mio` | Italian verse XXIV (the Latin `meum dicere`); found by the read-through. |
| 0758 | 8 | `35 Parvemi rami gravidi e vivaci` | `Parvermi` | Italian verse XXIV (the Latin `Apparuerunt`); found by the read-through. |
| 0758 | 19 | `Che tanti pianti e lagrime rifiuta.` | `prieghi` | Italian verse XXIV (the Latin `preces`); found by the read-through. |
| 0758 | 58 | `*E quando innanti nui*` | `innanti a nui` | Italian lemma (the verse); found by the read-through. |
| 0761 | 68 | `cotesta verginita, amore si vivo` | `verginità`, `sì` | Essay; no accents visible; found by the read-through. |
| 0762 | 5 | `ma splendito o commovente` | `splendido` | Essay; found by the read-through. |
| 0762 | 26 | `la bellezza e la verginita.` | `verginità` | Essay; no accent visible; found by the read-through. |
| 0764 | 18 | `*era onde 'l salir non volca storpio*` | `volea` | Italian lemma (the verse `volea`); an italic `c` for `e`; found by the read-through. |
| 0764 | 37 | `E già venute all'ultima tortura,` | `venuti` | Essay, a verse quoted (the verse `venuti`); found by the read-through. |
| 0765 | 19 | `Là dove l'huopo di mirar non toccha?` | `nutrir` | Italian verse XXV (the Latin `nutriendi`); found by the read-through. |
| 0765 | 42 | `Comsumpsit se in consumptione unius torris,` | `Consumpsit` | Latin verse; found by the read-through. |
| 0767 | 20 | `18 L'anima facta alla virtute activa,` | `Anima facta la` | Italian verse XXV (the Latin `Anima facta virtus activa`); found by the read-through. |
| 0769 | 6–7 | `E sappia che` / `L'articolar del cerchio è perfecto,` | `sappi`, `cerebro` | Italian verse XXV (the Latin `scias`, `cerebri`); found by the read-through. |
| 0770 | 8 | `30 Tosto che 'l loco lì lo certo scrive,` | `la circonscrive` | Italian verse XXV (the Latin `circumscribit`); found by the read-through. |
| 0770 | 16 | `Virtualmente all'alma che ristecte:` | `l'alma` | Italian verse XXV (the Latin `anima`); found by the read-through. |
| 0771 | 11 | `39 Ond'ir ne convenia dall'alto schiuso` | `dal lato` | Italian verse XXV (the Latin `a latere`); found by the read-through. |
| 0771 | 45 | `*E già venuto*` | `venuti` | Italian lemma (the verse `venuti`); found by the read-through. |
| 0773 | 12–84 | `possibilita`, `li`, `da`, `Bensi`, `verita`, `unita`, `svani`, `forni`, `cio`, `attivita` | `possibilità`, … | Essay; no accents visible on the page; found by the read-through. |
| 0773 | 77–78 | `sim-` / `beleggiate` | `simboleggiate` | Essay; found by the read-through. |
| 0774 | 6 | `una comunicazione pero, che` | `però` | Essay; no accent visible; found by the read-through. |
| 0776 | 11 | `*Mentre che si per l'orlo*` | `sì` | Italian lemma (the verse `sì`); no accent visible; found by the read-through. |
| 0777 | 16 | `Di non usar dove (2) non fusser arsi (3).` | `uscir` | Italian verse XXVI (the Latin `exeundi`); found by the read-through. |
| 0777 | 19 | `Risponde a me che 'n sete et in foco ardo.` | `Rispondi` | Italian verse XXVI (the Latin `Responde`); found by the read-through. |
| 0778 | 9 | `Venne gente col viso intorno a questa,` | `incontro` | Italian verse XXVI (the Latin `contra`); found by the read-through. |
| 0778 | 16 | `Forse a spiar lor vita e lor fortuna.` | `via` | Italian verse XXVI (the Latin `viam`); found by the read-through. |
| 0780 | 7 | `Quando rozzo e selvatico in se inurba` | `s'inurba` | Italian verse XXVI (the Latin `se inurbat`); found by the read-through. |
| 0780 | 23 | `29 In opbrobrio di noi, per noi si legge,` | `obbrobrio` | Italian verse XXVI; found by the read-through. |
| 0781 | 9 | `Son Guido Guininzelli; e già mi purgo,` | `Guinizelli` | Italian verse XXVI (the Latin `Guinizelli`); found by the read-through. |
| 0783 | 8 | `42 Così fer molti antichi di Guidone,` | `Guictone` | Italian verse XXVI (the Latin `Guictone`); found by the read-through. |
| 0785 | 46–82 | `volonta`, `totalita`, `realta`, `puo`, `di`, `porra`, `sara`, `avra`, `ardera`, `cosi`, `pero` | `volontà`, … | Essay; no accents visible on the page; found by the read-through. |
| 0788 | 7 | `Sì stava il sol, onde il giron sen giva,` | `giorno` | Italian verse XXVII (the Latin `dies`); found by the read-through. |
| 0790 | 12 | `Volgeti 'n qua, e vien entra sicuro.` | `oltre` | Italian verse XXVII (the Latin `ultra`); found by the read-through. |
| 0790 | 21 | `Mi volse al savio duca, udendo 'l nome` | `volsi` | Italian verse XXVII (the Latin `Volvi me`); found by the read-through. |
| 0792 | 18 | `Chè la natura del mondo (4) ci affranse` | `monte` | Italian verse XXVII (the Latin `montis`); found by the read-through. |
| 0792 | 31 | `Fasciati tutti quindi da la grotta.` | `quinci e quindi` | Italian verse XXVII (the Latin `hinc et inde`); found by the read-through. |
| 0793 | 64 | `fascidiati, idest circumdati` | `fasciati` | Commentary; found by the read-through. |
| 0796 | 12 | `Lo tuo piacer omai prende per duce:` | `prendi` | Italian verse XXVII (the Latin `apprehendas`); found by the read-through. |
| 0797 | 35–72 | `volonta`, `altresi`, `si per`, `di la`, `si che` | `volontà`, … | Essay; no accents visible (the second `sì per`, line 63, has one); found by the read-through. |
| 0799 | 20 | `cauto; dixit ipsa` | `canto` | Commentary; found by the read-through. |
| 0804 | 18 | `Per la pianetta, in sul lito` | `pineta` | Italian verse XXVIII (the Latin `Per pinetam`); found by the read-through. |
| 0804 | 19 | `Quand' Euro e Scirocco` | `Eolo` | Italian verse (the Latin `Eolus Eurum`); found by the read-through. |
| 0804 | 29 | `tremulando frondes pinte` | `prompte` | Latin verse (the Italian and the commentary `prompte`); found by the read-through. |
| 0804 | 64 | `per pinctam` | `pinetam` | Commentary; found by the read-through. |
| 0805 | 18 | `cosa che desia` | `disvia` | Italian verse (the Latin `deviat`); found by the read-through. |
| 0807 | 14 | `Maraviglando tieni` | `tienvi` | Italian verse (the Latin `tenet vos`); found by the read-through. |
| 0807 | 94 | `qui potest disnebriare` | `disnebiare` | Commentary (the verse `disnebiare`); found by the read-through. |
| 0808 | 46–47 | `motus celi, movens arborem` | `aierem` | Commentary; the motion moves the air, which strikes the trees; found by the read-through. |
| 0808 | 84 | `et sonus, sane, inpugnant` | `silve` | Commentary (the verse `sonus silve`); found by the read-through. |
| 0809 | 9 | `L'exaltation dell'acqua` | `exalation` | Italian verse (the Latin `Exalationes`); found by the read-through. |
| 0809 | 30 | `Propter suam difultam` | `difaltam` | Latin verse (the commentary `diffaltam`); found by the read-through. |
| 0814 | 34 | `Lo spatio dentro a le quatro` | `a lor` | Italian verse XXIX (the Latin `eorum quatuor`); found by the read-through. |
| 0815 | 60 | `parvum passuum cum parvo` | `passum` | Commentary (the verse `Parvum passum`); found by the read-through. |
| 0816 | 5 | `ubbidia la terra al cielo` | `e 'l cielo` | Italian verse (the Latin `terra et celum`); found by the read-through. |
| 0816 | 21 | `Et hora me aïuti` | `E Urania` | Italian verse (the Latin `Eurania me adiuvet`); found by the read-through. |
| 0816 | 32 | `Sensisset prius` | `Sensissem` | Latin verse (the Italian `Havrei`); found by the read-through. |
| 0816 | 73–74 | `*tra tante delitie*` | `primitie` | Commentary, the lemma (the verse `tra tante primitie`); found by the read-through. |
| 0817 | 9 | `Che l'obliquo comun` | `obiecto` | Italian verse (the Latin `obiectum comune`); found by the read-through. |
| 0817 | 12 | `candelabri accese` | `apprese` | Italian verse (the Latin `apprehensa`); found by the read-through. |
| 0818 | 7 | `vien dirieto a noi` | `a lor` | Italian verse (the Latin `retro illas`); found by the read-through. |
| 0818 | 13 | `come specchi anco` | `specchio` | Italian verse (the Latin `sicut in speculo`); found by the read-through. |
| 0818 | 22 | `et Elya il cinto` | `Delia` | Italian verse (the Latin `et Delia cinctum`); found by the read-through. |
| 0818 | 55 | `ita effectu vive lucis` | `in aspectu` | Commentary, the lemma (the verse `In aspectu vive lucis`); found by the read-through. |
| 0819 | 21 | `ch'altra possa mi strigne` | `spesa` | Italian verse (the Latin `alia expensa`); found by the read-through. |
| 0819 | 25 | `Venire a lui con nube` | `con vento` | Italian verse (the Latin `cum vento`); found by the read-through. |
| 0819 | 41 | `pennatum sex aliis` | `alis` | Latin verse (the commentary `sex alis`); found by the read-through. |
| 0820 | 13 | `Sì che nullo offendendo` | `a nulla fendendo` | Italian verse (the Latin `findendo nullum`); found by the read-through. |
| 0820 | 28 | `ab ipso descedit` | `discedit` | Latin verse (the commentary `discedit`); found by the read-through. |
| 0820 | 82 | `septem candelabria` | `candelabra` | Commentary; found by the read-through. |
| 0822 | 59 | `de rosis et de liliis` | `aliis` | Commentary (the verse `de aliis floribus`; the next line `isti vero non`); found by the read-through. |
| 0823 | 75 | `alle gia fatte` | `già` | Essay; no accent visible; found by the read-through. |
| 0826 | 42 | `ponitur interpretatio Beatricis` | `increpatio` | *Summarium* (0830 `ponitur increpatio quam fecit domina`); found by the read-through. |
| 0827 | 10 | `La rovistata voce` | `revestita` | Italian verse XXX (the Latin `Revestitam`); found by the read-through. |
| 0827 | 12 | `Si levar gente, a voce` | `cento` | Italian verse (the Latin `centum`); found by the read-through. |
| 0828 | 13 | `E ricidea in giù` | `ricadea` | Italian verse (the Latin `recadebat`); found by the read-through. |
| 0828 | 16 | `Vestito di color` | `Vestita` | Italian verse (the Latin `Vestita`); found by the read-through. |
| 0829 | 25 | `Per gl'alti legni` | `altri` | Italian verse (the Latin `Per alia ligna`); found by the read-through. |
| 0830 | 5 | `che lì m'appario` | `pria` | Italian verse (the Latin `que prius`); found by the read-through. |
| 0832 | 16 | `Secondo che le rote son compagne` | `stelle` | Italian verse XXXI (the Latin `stelle sunt sotie`); found by the read-through. |
| 0833 | 23 | `Alto facto (10) di Dio` | `fato` | Italian verse (the Latin `Altum fatum`); found by the read-through. |
| 0834 | 20 | `L'occhio lo sostenea` | `la` | Essay, a quotation (the verse on 0828 `la`); found by the read-through. |
| 0834 | 74 | `la verita e` | `verità` | Essay; no accent visible; found by the read-through. |
| 0840 | 95–96 | `rerum falla-`/`rium` | `fallacium` | Commentary (the verse `Rerum fallacium`); found by the read-through. |
| 0841 | 18 | `sè stessa l'antica` | `più sè stessa antica` | Italian verse (the Latin `plus se ipsam antiquam`); found by the read-through. |
| 0841 | 78 | `modo longeest pulchrior` | `longe est` | Commentary; no space visible; found by the read-through. |
| 0842 | 50 | `et [de] me subrisit` | `submersit` | Latin verse (the commentary `submersit`); found by the read-through. |
| 0843 | 27 | `Negl'altri, gl'altri tre` | `Negl'atti, l'altre` | Italian verse (the Latin `In actibus, alie tres`); found by the read-through. |
| 0845 | 31 | `intendere cio che` | `ciò` | Essay; no accent visible; found by the read-through. |
| 0849 | 18 | `Che procedeva` | `precedeva` | Italian verse XXXII (the Latin `precedebat`); found by the read-through. |
| 0849 | 19 | `piegasse al carro` | `il carro` | Italian verse (the Latin `plicaret currus`); found by the read-through. |
| 0850 | 19 | `Ne' bolchi loro` | `boschi` | Italian verse (the Latin `nemoribus`); found by the read-through. |
| 0850 | 41 | `propter multitudinem` | `altitudinem` | Latin verse (the Italian `per altezza`, the commentary `altitudinem`); found by the read-through. |
| 0850 | 72–73 | `*mormorare a tulli*` | `tutti` | Commentary, the lemma (the verse `a tucti`); found by the read-through. |
| 0851 | 8 | `E volti al temo` | `volto` | Italian verse XXXII (the Latin `Et conversus`); found by the read-through. |
| 0851 | 16 | `Giunct'à li suoi corsier senz'altra stella` | `Giunga` … `sott'altra` | Italian verse (the Latin `Coniungat` … `sub alia stella`; the essay on 0858); found by the read-through. |
| 0851 | 19 | `Che primavera le ramora` | `prima avea` | Italian verse (the Latin `Que prius habebat`; the essay on 0858); found by the read-through. |
| 0852 | 38 | `in montem Thaber` | `Thabor` | Commentary (line 87 `Thabor`); found by the read-through. |
| 0853 | 27 | `lasciata lì dal plaustro` | `del` | Italian verse (the Latin `plaustri`); found by the read-through. |
| 0854 | 10 | `Di quella torma onde Chrysto` | `Roma` | Italian verse (the Latin `Illius Rome`); found by the read-through. |
| 0857 | 21 | `superciliis circum pintis` | `promptis` | Latin verse (the commentary `circum promptis`); as 0804 `pinte`; found by the read-through. |
| 0858 | 14 | `per altezza ammirato` | `ammirata` | Essay, a quotation (`la sua chioma`); found by the read-through. |
| 0861 | 7 | `Rispose, con la rota come foco` | `colorata` | Italian verse XXXIII (the Latin `colorata sicut ignis`); found by the read-through. |
| 0862 | 46 | `a verecundia nolo` | `volo` | Commentary (the verse `Volo quod tu ammodo`); found by the read-through. |
| 0863 | 6 | `e Spingi, e metti persuade` | `men ti` | Italian verse (the Latin `minus te persuadet`; the essay on 0869); found by the read-through. |
| 0863 | 32 | `Et scis memor` | `sis` | Latin verse (the commentary `Et sis memor`); found by the read-through. |
| 0864 | 19 | `t'abbagla al lume` | `il lume` | Italian verse (the Latin `obfuscat te lumen`); found by the read-through. |
| 0865 | 54–55 | `si non scultum, saltem depictum` | `scriptum` | Commentary (the verse `si non scriptum`); found by the read-through. |
| 0865 | 94 | `subridendo respondidit` | `respondit` | Commentary; found by the read-through. |
| 0866 | 7 | `alla tua vogla rude` | `veduta` | Italian verse (the Latin `tue visioni rudi`); found by the read-through. |
| 0866 | 44 | `Supra supra frigidos rivos` | `Supra suos` | Latin verse (the commentary `supra suos rivos`); found by the read-through. |
| 0876 | 24 | `Verum quantum de suo regno` | `sancto` | Latin verse I (the Italian `regno sancto`, the commentary `de regno sancto`); found by the read-through. |
| 0877 | 18 | `(2) Cyheron` | `Cytheron` | Gloss (note 6 `Cytheron`); found by the read-through. |
| 0879 | 27 | `cum tribus circulis` | `crucibus` | Latin verse (the Italian `tre croci`, the commentary `cum tribus crucibus`); found by the read-through. |
| 0879 | 29 | `se mundane terre` | `cere` | Latin verse (the Italian `cera`, the commentary `mundane cere`); found by the read-through. |
| 0880 | 42 | `Esse aditum` | `additum` | Latin verse (the commentary `esse additum`); found by the read-through. |
| 0880 | 43 | `uno alio celo ornasset` | `sole` | Latin verse (the Italian `d'un altro sol`, the commentary `alio sole`); found by the read-through. |
| 0881 | 7 | `di lassu remote` | `lassù` | Italian verse; no accent visible; found by the read-through. |
| 0881 | 88 | `*Si ergo eram solus de me*` | `ego` | Commentary, the lemma (the verse `Si ego eram`); found by the read-through. |
| 0882 | 19 | `Mai fulgure (40), fuggendo (41) 'l primo sito` | `Ma` … `proprio` | Italian verse (the Latin `Sed fulgur fugiens a proprio situ`); found by the read-through. |
| 0883 | 17 | `Ha un ordine (29)` | `Hanno ordine` | Italian verse (the Latin `Habent ordinem`); found by the read-through. |
| 0884 | 50 | `iste actus sagiptat` | `arcus` | Latin verse (the Italian `arco`, the commentary `iste arcus`); found by the read-through. |
| 0886 | 11 | `se si si vedesse` | `se si` | Gloss; a word doubled; found by the read-through. |
| 0892 | 68 | `una sagipta, que escit` | `quiescit` | Commentary (the verse `quiescit`); found by the read-through. |
| 0894 | 23 | `(19) l'apprhensiva` | `apprehensiva` | Gloss; as `comprhender` (line 28); found by the read-through. |
| 0894 | 65 | `ubi clavis semper non aperit` | `sensus` | Commentary (the verse `clavis sensus`); found by the read-through. |
| 0894 | 73 | `te pingere sagipte` | `pungere` | Commentary (the verse `pungere sagipte`); found by the read-through. |
| 0895 | 15 | `Lograsso (25)` | `Lo grasso` | Italian verse; no space visible; found by the read-through. |
| 0897 | 21 | `Da la nieve (45)` | `De la` | Italian verse II (the Latin `Nivis`); found by the read-through. |
| 0898 | 13 | `Da lui distincte (22) e da lui (24)` | `(23)` | Italian verse; the note number repeated (the notes run 22, 23, 24); found by the read-through. |
| 0901 | 52–95 | `per cosi dire`, `E cosi`, `ogni`/`di meglio` | `così`, `dì` | Essay; no accents visible; found by the read-through. |
| 0902 | 30 | `della Trinita` | `Trinità` | Essay; no accent visible; found by the read-through. |
| 0905 | 6 | `Sè a me tanto streto` | `A sè me` | Italian verse III (the Latin `Ad se me tantum strictum`); found by the read-through. |
| 0908 | 7 | `Sicchè transfigurar` | `raffigurar` | Italian verse (the Latin `ad refigurandum`); found by the read-through. |
| 0910 | 12 | `Fuor mi rapitten` | `rapiron` | Italian verse (the Latin `rapuerunt`); found by the read-through. |
| 0910 | 41 | `sic ei fuit abrecta` | `abrepta` | Latin verse (the commentary `abrepta`); found by the read-through. |
| 0910 | 57–58 | `ad complacentiam`/`confirmat` | `conformat` | Commentary (the verse `conformat`); found by the read-through. |
| 0912 | 44 | `Posto cio` | `ciò` | Essay; no accent visible; found by the read-through. |
| 0912 | 62 | `dominatrice dell'alto` | `dell'atto` | Essay; found by the read-through. |
| 0919 | 10 | `da non esser decisa` | `derisa` | Italian verse IV (the Latin `non deridenda`); found by the read-through. |
| 0919 | 40 | `Habet plus veneni` | `minus` | Latin verse (the Italian `men`, the commentary `minus veneni`); found by the read-through. |
| 0922 | 22 | `parlar mi monda` | `m'inonda` | Italian verse (the Latin `me inundat`); found by the read-through. |
| 0923 | 106 | `dicentem, rexpexit` | `respexit` | Commentary (the verse `respexit`); found by the read-through. |
| 0923 | 110 | `idest defici` | `defeci` | Commentary; found by the read-through. |
| 0928 | 21 | `Apre la mente` | `Apri` | Italian verse V (the Latin `Aperias mentem`); found by the read-through. |
| 0929 | 17 | `permutanza crede stolta` | `credi` | Italian verse (the Latin `credas`); found by the read-through. |
| 0931 | 79 | `E si *come saietta*` | `sì` | Commentary, the lemma; no accent visible; found by the read-through. |
| 0931 | 92–93 | `in`/`limine illius` | `lumine` | Commentary (the verse `in lumine illius`); found by the read-through. |
| 0932 | 24 | `Nel primo lume` | `proprio` | Italian verse (the Latin `In proprio lumine`); found by the read-through. |
| 0934 | 33 | `Si, certo` | `Sì` | Essay; no accent visible; found by the read-through. |
| 0934 | 61 | `in possente unita` | `unità` | Essay; no accent visible; found by the read-through. |
| 0936 | 38 | `Ormai poi coniudicare` | `iudicare` | Commentary, the division (0944 `Omai poi iudicare`); found by the read-through. |
| 0937 | 41–42 | `de quibus privatus exivit` | `primitus` | Commentary (the verse on 0936 `primitus`); found by the read-through. |
| 0940 | 52 | `trigintiquatuor milliaria` | `trigintaquatuor` | Commentary; found by the read-through. |
| 0944 | 90–91 | `Hor, nunc,`/`id respice` | `hic` | Commentary (the verse `hic respice`); found by the read-through. |
| 0945 | 28 | `Apponit, et alter` | `Opponit` | Latin verse VI (the Italian `oppone`, the commentary `opponit`); found by the read-through. |
| 0945 | 71 | `artem sub illo signo` | `alio` | Commentary (the verse `Sub alio signo`); found by the read-through. |
| 0945 | 93 | `quod radii veteris` | `veri` | Commentary (the verse `Veri amoris`); found by the read-through. |
| 0948 | 78 | `evangelica equita` | `equità` | Essay; no accent visible; found by the read-through. |
| 0948 | 84 | `a que' di!` | `dì` | Essay; no accent visible; found by the read-through. |
| 0950 | 72 | `splendore tuo inneffabili` | `ineffabili` | Commentary; found by the read-through. |
| 0951 | 80 | `moverunt ad suam corouam` | `coream` | Commentary; a turned `n` (`corouam`); 0950 `ad suam coream`; found by the read-through. |
| 0956 | 59 | `fuitvel erit` | `fuit vel` | Latin verse VII; no space visible; found by the read-through. |
| 0958 | 6 | `Creata fu la materia informante` | `virtù` | Italian verse (the Latin `virtus informans`); found by the read-through. |
| 0962 | 14 | `hor da poppa or da` | `coppa` | Italian verse VIII (the Latin `a coppa`); found by the read-through. |
| 0962 | 55–56 | `continuans dicta di-`/`cens` | `dicendis` | Commentary (the formula, as 0974 `continuat dicta dicendis`); found by the read-through. |
| 0963 | 43–44 | `Depin-`/`gitur a latus` | `alatus` | Commentary; found by the read-through. |
| 0965 | 10 | `um poca di quiete` | `un` | Italian verse; found by the read-through. |
| 0965 | 71 | `cum priucipibus celestibus` | `principibus` | Commentary; `u` for `n`; found by the read-through. |
| 0967 | 47–48 | `attendendissent` | `attendissent` | Commentary; `nd` doubled; found by the read-through. |
| 0968 | 5 | `Facto m'è lieto` | `m'ài` | Italian verse (the Latin `Fecisti me letum`); found by the read-through. |
| 0968 | 71 | `*Perch'io disse*` | `dissi` | Commentary, the lemma (0967 `Perch'io dissi`); found by the read-through. |
| 0968 | 90 | `rum, ad aliud, quod tu petis` | `illud` | Commentary (the verse `ad illud quod tu petis`); found by the read-through. |
| 0969 | 23 | `un nasce Absalon` | `Solon` | Italian verse (the Latin `Solon`); found by the read-through. |
| 0975 | 5 | `E gia la vista` | `già` | Italian verse IX; no accent visible; found by the read-through. |
| 0975 | 17 | `De! mette al mio voler` | `metti` | Italian verse (the Latin `mictas`); found by the read-through. |
| 0975 | 104–105 | `vel experentiam` | `experientiam` | Commentary; found by the read-through. |
| 0976 | 25 | `Sì ch'altra vita a la prima relinqua` | `la prima` | Italian verse IX (the Latin `prima relinquat`); found by the read-through. |
| 0980 | 55 | `semper cum incantu` | `cantu` | Commentary (the verse `cum cantu`); found by the read-through. |
| 0981 | 52 | `iniurando Sicheo` | `iniuriando` | Commentary (the verse `Iniuriando Sicheo`); found by the read-through. |
| 0981 | 61 | `fuit a Denophonte` | `Demophonte` | Commentary (the verse `a Demophonte`); found by the read-through. |
| 0981 | 82 | `*Sed adhuc ut omnes tuas voluntates*` | `ad hoc` | Commentary, the lemma (the verse `Sed ad hoc ut`); found by the read-through. |
| 0990 | 49 | `nostre sunt infime` | `infirme` | Commentary, quoting the verse (`infirme`); found by the read-through. |
| 0990 | 74–75 | `ita de-`/`gestum` | `digestum` | Commentary (the verse `digestum`); found by the read-through. |
| 0992 | 5 | `E dentro alcun sentii` | `all'un` | Italian verse X (the Latin `intra unum`; the lemma `all' un`); found by the read-through. |
| 0995 | 53 | `horologium, quos nos vocet` | `quod` | Commentary (the verse `quod nos vocet`); found by the read-through. |
| 0995 | 54–55 | `ut`/`ipsum amet` | `ipsam` | Commentary (the verse `ut ipsam amet`); found by the read-through. |
| 0996 | 103 | `ha detto Gesu` | `Gesù` | Essay; no accent visible; found by the read-through. |
| 0999 | 66–67 | `quidam ad`/`ad civile` | `ad` | Commentary; a word doubled over the line end; found by the read-through. |
| 0999 | 105 | `de tuo radio resplendeo` | `suo` | Commentary (the verse `de suo radio`); found by the read-through. |
| 1001 | 34–35 | `ad unam facem` | `ad unum finem` | Commentary (the verse `ad unum finem`); found by the read-through. |
| 1003 | 93 | `Francisci paupertatem` | `Franciscum et Paupertatem` | Commentary quoting the verse (`Franciscum et Paupertatem`); found by the read-through. |
| 1005 | 10 | `Tornassi al fructo` | `Tornossi` | Italian verse XI 105 (the Latin `Redivit`); found by the read-through. |
| 1006 | 43 | `Si quiquid dixi` | `quidquid` | Latin verse (the commentary `quidquid`); found by the read-through. |
| 1008 | 32, 34, 67, 79, 82, 88 | `gia`, `delia`, `di`, `puo`, `pero`, `piu` | `già`, `della`, `dì`, `può`, `però`, `più` | Essay; no accent visible; `li` for `ll`; found by the read-through. |
| 1011 | 61 | `sequi iuria civilia` | `iura` | Commentary; found by the read-through. |
| 1016 | 60 | `ad sinum verbi.` | `ad suum ubi` | Commentary (the verse `ad suum ubi`); found by the read-through. |
| 1019 | 11 | `Adunando; ma contra` | `Addimandò` | Italian verse XII 94 (the Latin `Petivit`); found by the read-through. |
| 1021 | 15 | `Crysostimo, et Anselmo` | `Crysostomo` | Italian verse XII 137 (the commentary `Chrisostomus`); found by the read-through. |
| 1023 | 22, 50, 70 | `all'atfetto`, `cosi la sola`, `cosi è` | `affetto`, `così`, `così` | Essay; `t` for `f`; no accent visible; found by the read-through. |
| 1026 | 8 | `Che soverchia dell'arte` | `dell'aere` | Italian verse XIII 6 (the Latin `aeris`); found by the read-through. |
| 1027 | 7, 88 | `al primo el'altro`, `celum adiuvant,` | `e l'altro`, `avivant` | Italian verse XIII 18; the commentary quoting the Latin verse `Celum avivant`; found by the read-through. |
| 1028 | 11, 12, 33 | `Compiè 'l cantor`, `Et attesarsi a noi`, `une palec sunt` | `cantar`, `attesersi`, `palee` | Italian verse XIII 28 and 29 (the Latin `cantum`, `attenderunt`); the Latin verse (the commentary `palee`); found by the read-through. |
| 1030 | 73, 99 | `quasi speculator,`, `et admiuistrat minus` | `speculatus`, `administrat` | Commentary (the verse `Quasi speculatus`); `u` for `n`; found by the read-through. |
| 1031 | 98 | `sive a medio` | `sine medio` | Commentary (`sine medio celi` on the same page; `non concurrente celo`); found by the read-through. |
| 1032 | 5 | `s'io non processi avanti` | `procedessi` | Italian verse XIII 88 (the commentary `procedessi`); found by the read-through. |
| 1034 | 27 | `prius quam sit matura:` | `sint` | Latin verse (the Italian `sien`, the commentary `sint`); found by the read-through. |
| 1039 | 95 | `et nobis, scilicet` | `vobis` | Commentary (the verse `et vobis`); found by the read-through. |
| 1041 | 100 | `scientiticorum,` | `scientificorum` | Commentary; `t` for `f`; found by the read-through. |
| 1043 | 7 | `El so' litario stato` | `Esso litare` | Italian verse XIV 93 (the Latin `Ipsum`); found by the read-through. |
| 1044 | 7, 76 | `quel arbor balenar`, `in profundo mari,` | `albor`, `Marti` | Italian verse XIV 108 (the Latin `albedine`); the commentary glossing `stelle Martis`; found by the read-through. |
| 1046 | 37 | `facerem intentionem de` | `mentionem` | Commentary; found by the read-through. |
| 1047 | 9 | `aggiungera` | `aggiungerà` | Essay; no accent visible; found by the read-through. |
| 1052 | 45 | `fuit, fuit, scilicet` | `fuit, scilicet` | Commentary; a word printed twice; found by the read-through. |
| 1054 | 6, 37 | `la prima qualità`, `qui nos illuminat` | `equalità`, `vos` | Italian verse XV 74 (the Latin `equalitas`); the commentary (the verse `qui vos illuminat`); found by the read-through. |
| 1055 | 38 | `Tu illo abbrevies` | `illi` | Latin verse (the commentary `illi`); found by the read-through. |
| 1057 | 11, 35, 37 | `L'altra trhaendo`, `trahendo collo comam`, `de Fiesols,` | `traendo`, `colo`, `Fiesolis` | Italian verse XV 124; the Latin verse (the commentary `colo`, `Fiesolis`); found by the read-through. |
| 1058 | 23 | `Disvolutus a gente fallaci` | `a mundo` | Latin verse (the Italian `dal mondo`, the commentary `a mundo`); found by the read-through. |
| 1063 | 17 | `rivi sempr' è d'allegrezza` | `s'empie` | Italian verse XVI 19 (the Latin `impletur`); found by the read-through. |
| 1064 | 13, 17, 35 | `questa mondana favella`, `Al sol Leone`, `sub sua plancta.` | `moderna`, `suo`, `planta` | Italian verse XVI 33 and 37 (the Latin `moderna`, `suum`); the Latin verse (the commentary `sub sua planta`); found by the read-through. |
| 1066 | 39 | `ad substituendum putredinem` | `sustinendum` | Commentary (the verse `ad sustinendum`); found by the read-through. |
| 1067 | 5, 73–74 | `Se tu rigardi`, `idest defe-`/`runt` | `riguardi`, `defecerunt` | Italian verse XVI 73 (`riguardi` where it is quoted again); the commentary; found by the read-through. |
| 1068 | 25, 92 | `Alle carole Sitii`, `et Galla (aliud` | `curule`, `Galli` | Italian verse XVI 108 (the Latin `curules`); the commentary (the verse `Galli`); found by the read-through. |
| 1069 | 15, 19, 77 | `agl' Uberti Donato`, `cittadino Guida et`, `agnus mansuctus,` | `ad Ubertin`, `Guido`, `mansuetus` | Italian verse XVI 119 and 123 (the Latin `Ubertino`, `Guido`); the commentary, `c` for `e`; found by the read-through. |
| 1070 | 18, 57, 109 | `Quilibet de pulchro`, `reinconfortat`, `erat honerata ipsa` | `Quilibet qui de`, `reconfortat`, `honorata` | Latin verse (the Italian `Ciascun che`, the commentary `Quilibet qui`); the commentary (the verse `reconfortat`, `honorata`); found by the read-through. |
| 1071 | 12 | `Chel guarda 'l ponte` | `Che` | Italian verse XVI 146 (the Latin `Que`); found by the read-through. |
| 1072 | 23, 40, 84, 109, 111 | `Si come voi`, `vola alia giustizia`, `Cosi all'orazion`, `Ma si come`, `Si che la sua` | `Sì`, `alla`, `Così`, `sì`, `Sì` | Essay; no accent visible; `li` for `ll`; found by the read-through. |
| 1073 | 11, 20 | `respondidit`, `recipiet cum benigne` | `respondit`, `eum` | Commentary; `c` for `e`; found by the read-through. |
| 1075 | 11, 84 | `O cara pietra mia`, `sed adhuc ut` | `piota`, `ad hoc` | Italian verse XVII 13 (the Latin `planta`); the commentary (the verse `ad hoc`); found by the read-through. |
| 1076 | 17, 47, 81 | `in chi la gente`, `O cara plancta mea`, `fugere fortuniam,` | `che`, `planta`, `fortunam` | Italian verse XVII 31 (the commentary lemma `in che`); the commentary (the verse `O cara planta mea`); found by the read-through. |
| 1077 | 59, 73 | `per correntem infra`, `cum bono ventu` | `torrentem`, `vento` | Commentary (the verse `per torrentem`); found by the read-through. |
| 1080 | 71 | `tacendo, mostrarit se` | `monstravit` | Commentary lemma (the verse `se monstravit`); found by the read-through. |
| 1081 | 14, 94, 95 | `son intimo amico`, `vel proprio,`, `se setiet omnino` | `timido`, `proprie`, `sentiet` | Italian verse XVII 118 (the Latin `timidus`); the commentary (the verse `proprie`, `sentiet`); found by the read-through. |
| 1083 | 27 | `delle nostri azioni` | `nostre` | Essay; found by the read-through. |
| 1087 | 16 | `col sereno aspecto` | `secondo` | Italian verse XVIII 18 (the Latin `secundo`); found by the read-through. |
| 1088 | 79 | `quod omnino musa` | `omnis` | Commentary (the verse `omnis musa`); found by the read-through. |
| 1089 | 7, 78, 85 | `era forza de paleo`, `mortuus est Sitii`, `inter infedeles,` | `ferza`, `siti`, `infideles` | Italian verse XVIII 42 (the Latin `ferza`); the commentary; found by the read-through. |
| 1090 | 35 | `Suum exponeret verecundia` | `exoneret` | Latin verse (the commentary `exoneret`); found by the read-through. |
| 1093 | 6, 34, 73 | `d'imgiglarsi`, `Effectus sint celi`, `qui totum radium` | `d'ingiglarsi`, `sit`, `tuum` | Italian verse XVIII 113; the Latin verse (the commentary `sit`); the commentary (the verse `tuum`); found by the read-through. |
| 1097 | 63 | `vis tu indicare` | `iudicare` | Commentary; `n` for `u`; found by the read-through. |
| 1098 | 54 | `contexeatur` | `contexatur` | Commentary; found by the read-through. |
| 1103 | 32, 69 | `O tu qui es,`, `Quomodo ego credis` | `quis es`, `ergo` | Latin verse (the commentary `quis es`); the commentary; found by the read-through. |
| 1105 | 13 | `regno di Plaga` | `Praga` | Italian verse XIX 117 (the Latin `Prage`); found by the read-through. |
| 1106 | 36 | `Patrui et patris,` | `fratris` | Latin verse (the Italian `fratel`, the commentary `fratris`); found by the read-through. |
| 1111 | 35 | `angelicis quisquillis,` | `squillis` | Latin verse (the commentary `squillis`); found by the read-through. |
| 1114 | 54, 69 | `propter meram penitentiam`, `et sie in hoc` | `veram`, `sic` | Commentary (the verse `veram`); found by the read-through. |
| 1116 | 51 | `si alius illa non` | `illam` | Commentary (the verse `illam`); found by the read-through. |
| 1117 | 7, 8, 53 | `[a] divina speme`, `Divina speme, che`, `fuerunt ibi pro` | `di viva`, `Di viva`, `sibi` | Italian verse XX 108 and 109 (the Latin `vive spei`); the Latin verse (the commentary `sibi`); found by the read-through. |
| 1118 | 20 | `mentre che parlo,` | `parlò` | Italian verse XX 145; found by the read-through. |
| 1119 | 65, 69 | `Tutti pero,`, `ma bensi` | `però`, `bensì` | Essay; no accent visible; found by the read-through. |
| 1124 | 7, 35 | `ogni militia morta`, `[bonum` | `malitia`, `lumen` | Italian verse XXI 27 (the Latin `malitia`); the Latin verse (the Italian `lume`, the commentary `lumen`); found by the read-through. |
| 1126 | 68, 96 | `ab omni creatura vista`, `dixi eo*.` | `creata`, `ego` | Latin verse (the commentary `creata`); the commentary lemma (the verse `dixi ego`); found by the read-through. |
| 1129 | 39 | `et que retro eos` | `qui` | Latin verse (the commentary `qui`); found by the read-through. |
| 1130 | 32, 50, 51 | `puo`, `aveva vèduta,`, `che senti in` | `può`, `veduta`, `sentì` | Essay; no accent visible; a grave accent printed on the `e`; found by the read-through. |
| 1133 | 103 | `Ergo stabant sicut` | `Ego stabam` | Commentary (the verse `Ego stabam`); found by the read-through. |
| 1134 | 24 | `Et maior et loculentior` | `luculentior` | Latin verse (the Italian `luculenta`, the commentary `luculentior`); found by the read-through. |
| 1135 | 77, 106 | `sic michi dilactavit`, `nec quod ad se` | `dilatavit`, `quoad` | Commentary (the verse `dilatavit`; `quoad` after it); found by the read-through. |
| 1137 | 8 | `Iordan volt'e retrorso` | `volt'è` | Italian verse XXII 94 (the Latin `conversus est`); found by the read-through. |
| 1138 | 68 | `largita intrandi idest altam` | `in` | Commentary (the verse `Intrandi in altam`); found by the read-through. |
| 1140 | 10, 31, 32, 59, 73 | `è di la e`, `senti il bisogno`, `de'suoi di,`, `societa`, `societa` | `di là`, `sentì`, `dì`, `società`, `società` | Essay; no accent visible; found by the read-through. |
| 1142 | 7 | `onde si pasca,` | `li pasca` | Italian verse XXIII 5 (the Latin `ipsos pascat`); found by the read-through. |
| 1145 | 22 | `odor s'aperse'l bel` | `si prese` | Italian verse XXIII 75 (the Latin `apprehensum fuit`); found by the read-through. |
| 1147 | 18, 22, 32, 33 | `Sì rigirava,`, `Nell'habito di Dio`, `lacerata sonat,`, `ad sonum unius lire` | `Si sigillava`, `alito`, `tonat`, `illius` | Italian verse XXIII 110 and 114 (the Latin `Sigillabatur`, `anhelitu`); the Latin verse (the commentary `tonat`, `illius`); found by the read-through. |
| 1148 | 9, 38 | `Co'la sua fiamma,`, `O quantum est ubertas` | `cima`, `quanta` | Italian verse XXIII 125 (the Latin `summitate`, the essay on 1149 `cima`); the Latin verse (the commentary `quanta`); found by the read-through. |
| 1149 | 18, 22, 76, 86, 93 | `cosi belle`, `cosi pura`, `e si caro`, `cima si,`, `cantando si dolce` | `così`, `così`, `sì`, `sì`, `sì` | Essay and its quoted verse; no accent visible; found by the read-through. |
| 1153 | 36 | `cum bona fine;` | `fide` | Commentary (`possessor male fidei` after it); found by the read-through. |
| 1154 | 9, 17 | `canto tanto vivo,`, `el corpo benedecto` | `divo`, `foco` | Italian verse XXIV 23 and 31 (the Latin `divino`, `focus`); found by the read-through. |
| 1155 | 10, 21 | `Per aiutarla,`, `dell'alto primo pilo` | `approvarla`, `dall'alto` | Italian verse XXIV 48 and 59 (the Latin `approbare`, `ab alto`); found by the read-through. |
| 1157 | 26, 41 | `Perche l'hai tu`, `Istum carum iocale` | `Perchè`, `Istud` | Italian verse XXIV 99, no accent visible; the Latin verse (the commentary `Istud`); found by the read-through. |
| 1159 | 94 | `veritas que hic pluit` | `hinc` | Commentary (the verse `hinc pluit`); found by the read-through. |
| 1161 | 83 | `oggi miro in tutte` | `mirò` | Essay; no accent visible; found by the read-through. |
| 1165 | 29, 89–90 | `vivum lumen`, `pere` / `grini,` | `unum`, `pere-` | Latin verse (the commentary `unum lumen`); the commentary, no hyphen printed at the line end (`texts/la` joins it: `HYPHEN_MISSING` in `convert_la.py`); found by the read-through. |
| 1166 | 26, 39, 62 | `die quid est spes`, `bene in amore trahit`, `maiorem caritatem.` | `dic`, `in amorem`, `claritatem` | Gloss, `e` for `c`; the Latin verse (the commentary `in amorem`); the commentary (the verse `claritatem`); found by the read-through. |
| 1168 | 6, 35, 38 | `el nome suo:`, `in aliis vestram`, `Subitus et depressus,` | `tuo`, `in alios`, `densus` | Italian verse XXV 74 (the Latin `tuum`); the Latin verse (the commentary `in alios`, `densus`); found by the read-through. |
| 1169 | 98, 111 | `*noritia*`, `Volvit se in cantum` | `novitia`, `Misit se` | Commentary, italic `r` for `v`; the commentary lemma (the verse `Misit se`); found by the read-through. |
| 1170 | 9, 36 | `Mostrò la vista sua`, `In terra est meum` | `Mosse`, `In terra terra est` | Italian verse XXV 116 (the Latin `movit`); the Latin verse (the Italian `In terra è terra`, the commentary `In terra terra est`); found by the read-through. |
| 1172 | 9, 53, 57, 58 | `piu`, `isvellatamente`, `capacita`, `puo` | `più`, `isvelatamente`, `capacità`, `può` | Essay; no accent visible; `ll` for `l`; found by the read-through. |
| 1173 | 26 | `die michi` | `dic` | Commentary; `e` for `c`; found by the read-through. |
| 1175 | 19 | `per istum divam` | `istam` | Latin verse (the commentary `istam`); found by the read-through. |
| 1176 | 20, 26, 90 | `all'esentia`, `amorem suum leviter`, `in me exprimatur.` | `essentia`, `sive`, `imprimatur` | Italian verse XXVI 31; the Latin verse (the commentary `sive leviter sive fortiter`); the commentary (the verse `imprimatur`); found by the read-through. |
| 1177 | 11, 13, 24, 55, 91 | `del beato autore`, `farò sentir ogni`, `ancor m'accorsi`, `probatur ista probatio`, `respondidisti` | `verace`, `veder`, `anzi`, `fundatur`, `respondisti` | Italian verse XXVI 40, 42 and 53 (the Latin `veracis`, `videre`, `imo`); the commentary (the verse `fundatur`); found by the read-through. |
| 1178 | 42 | `quero ego tantum` | `amo` | Latin verse (the Italian `amo`, the commentary `amo`); found by the read-through. |
| 1181 | 8, 14, 21, 33, 77 | `tornar a questi lumi`, `nullo affecto`, `Un s'appellava`, `nongintis`, `istud consilium` | `tutti i`, `effecto`, `I`, `nongentis`, `concilium` | Italian verse XXVI 121, 127 and 134 (the Latin `omnia`, `effectus`, `I`); the Latin verse (the commentary `nongentis`); the commentary (the verse `concilium`); found by the read-through. |
| 1183 | 34, 51, 79, 80 | `cóngiunta`, `quanto piu`, `ogni`/`di più`, `un di in` | `congiunta`, `più`, `dì`, `dì` | Essay; an accent printed over the `o`; no accent visible; found by the read-through. |
| 1185 | 38 | `celum novum in` | `nonum` | Commentary; `u` for `n`; found by the read-through. |
| 1186 | 6, 51 | `Ciò ch'io udiva`, `mortali offendi.` | `vedeva`, `affonde` | Italian verse XXVII 4 (the Latin `videbam`); the commentary lemma (the verse `affonde`); found by the read-through. |
| 1187 | 10, 48 | `cambiansersi`, `secure delitie!` | `cambiassersi`, `divitie` | Italian verse XXVII 15; the commentary (the verse `divitie`); found by the read-through. |
| 1188 | 42 | `De sanguine Lini` | `De sanguine meo, Lini` | Latin verse; a word left out (the Italian `mio`, the commentary `de sanguine meo`); found by the read-through. |
| 1189 | 13, 81, 103 | `O vendetta di Dio`, `figuram sigilli`, `o bone principium` | `difesa`, `figura`, `bonum` | Italian verse XXVII 57 (the Latin `defensio`); the commentary (the verse `figura`, `bonum`); found by the read-through. |
| 1190 | 15 | `E seguì finche` | `finchè` | Italian verse; no accent visible; found by the read-through. |
| 1191 | 19 | `sed sol procedebat` | `precedebat` | Latin verse (the commentary `precedebat`); found by the read-through. |
| 1192 | 14, 43, 49, 101 | `sue vicissime`, `Quod Deum apparebat`, `virtus quam ipsum pluit`, `hic incipit` | `vivissime`, `Deus`, `que`, `hinc` | Italian verse XXVII 100; the Latin verse (the commentary `Deus`, `que`); the commentary (the verse `Hinc`); found by the read-through. |
| 1193 | 94–95 | `bozzacchia-`/`nes` | `bozzacchiones` | Commentary (the verse `bozzacchiones`); found by the read-through. |
| 1194 | 24, 109 | `O vero fructo`, `nunc mens yemalis` | `E`, `mensis` | Italian verse XXVII 148 (the Latin `Et`); the commentary; found by the read-through. |
| 1196 | 52, 68 | `non puo`, `(IAN. III)` | `può`, `IOAN.` | Essay; no accent visible; found by the read-through. |
| 1199 | 87 | `apparet hic, idest` | `hinc` | Commentary (the verse `hinc`); found by the read-through. |
| 1200 | 10 | `Già di lunghezza` | `larghezza` | Italian verse XXVIII 32 (the Latin `largitate`); found by the read-through. |
| 1201 | 90 | `ipsa dicitura est` | `dictura` | Commentary; found by the read-through. |
| 1202 | 37, 70 | `ubi est levior`, `secundum maioritatem` | `lenior`, `minoritatem` | Latin verse (the commentary `lenior`); the commentary (the verse `minoritatem`); found by the read-through. |
| 1206 | 32, 76, 89 | `rise (2).`, `de grado in gradum`, `sunt duo alie` | `(12)`, `gradu`, `due` | Italian verse XXVIII 135 (the footnote is `(12)`); the commentary (the verse `gradu`, `due`); found by the read-through. |
| 1207 | 12 | `Et si tanto veridice` | `tantum` | Latin verse (the commentary `tantum`); found by the read-through. |
| 1211 | 26 | `In ista eternitate` | `sua` | Latin verse (the Italian and the commentary `sua`); found by the read-through. |
| 1213 | 29, 74 | `Hieronimus nobis scripsit`, `vobis bonum tractum` | `vobis`, `longum` | Latin verse (the Italian `vi`, the commentary `vobis`); the commentary (the verse `longum`); found by the read-through. |
| 1214 | 71 | `idco dicit Iob` | `ideo` | Commentary; the `c` is printed; found by the read-through. |
| 1215 | 30, 69 | `Potest contemplari satis`, `que Deos vult` | `Potes`, `Deus` | Latin verse (the Italian `Puoi`, the commentary `potes`); the commentary; found by the read-through. |
| 1216 | 109 | `hoc effectus est` | `effusus` | Commentary (`effusus est` above); found by the read-through. |
| 1217 | 13, 34 | `Com'a'Giuderi`, `Sicut vides, eclipsatio` | `Giudei`, `Iudeis` | Italian verse XXIX 102; the Latin verse (the commentary `sicut Iudeis`); found by the read-through. |
| 1218 | 38, 73 | `promissionem cucurreretur`, `alicuius textis, ad omnem professionem` | `curreretur`, `testis`, `promissionem` | Latin verse (the commentary `curreretur`); the commentary (the verse `testis`, `promissionem`); found by the read-through. |
| 1219 | 15, 43 | `Segue l'effecto d'amare`, `quod unquam fuit` | `l'affecto`, `nunquam` | Italian verse XXIX 140 (the Latin `affectum`); the commentary (the verse `nunquam`); found by the read-through. |
| 1224 | 30, 57, 62 | `Talis, qualis ipsam`, `passu vinctum me`, `magit tremit` | `qualem`, `victum`, `magis` | Latin verse (the commentary `qualem`); the commentary (the verse `victum`, `magis`); found by the read-through. |
| 1226 | 32 | `sicut inebrietate ab` | `inebriate` | Latin verse (the commentary `inebriate`); found by the read-through. |
| 1228 | 27, 97, 102 | `triumphum celi veracis`, `bene optimus illis`, `flos optimus;` | `regni`, `opimus`, `opimus` | Latin verse (the Italian `regno`, the commentary `regni veracis`); the commentary (the verse `opimus`); found by the read-through. |
| 1229 | 77–78 | `amplitudine et lati-`/`tudine` | `altitudine` | Commentary (the verse `altitudine`); found by the read-through. |
| 1230 | 31, 83 | `postea adeo sustinebitur`, `magis intra, idest` | `a Deo`, `infra` | Latin verse (the commentary `a Deo`); the commentary (the verse `infra`); found by the read-through. |
| 1231 | 68, 70, 73 | `puo tenersi`, `in realta si gran`, `oscurita, anzi cecita` | `può`, `realtà`, `sì`, `oscurità`, `cecità` | Essay; no accent visible; found by the read-through. |
| 1234 | 23 | `Quod d viditur` | `dividitur` | Commentary; a gap for the `i`; found by the read-through. |
| 1235 | 34, 84, 85 | `reliquum tantum album`, `tot floribus`, `inde transcendebat` | `totum`, `foliis`, `reascendebat` | Latin verse (the Italian `tutto`, the commentary `totum`); the commentary (the verse `foliis`, `reascendebat`); found by the read-through. |
| 1239 | 81 | `non ascendebat ad me` | `descendebat` | Commentary (the verse `descendebat`); found by the read-through. |
| 1240 | 10 | `A chi prego` | `che` | Italian verse XXXI 96 (the Latin `Ad quod`); found by the read-through. |
| 1241 | 43 | `Per equalem motum` | `modum` | Latin verse (the Italian `modo`, the commentary `modum`); found by the read-through. |
| 1242 | 24, 27 | `ad corum cantus`, `tantam habundatiam` | `eorum`, `habundantiam` | Latin verse; the `c` is printed (the commentary `eorum`, `habundantiam`); found by the read-through. |
| 1243 | 48, 70, 72 | `che si piccoli`, `a liberta, la quale`, `(Ioan. VIII, 131)` | `sì`, `libertà`, `32` | Essay; no accent visible; John 8:32; found by the read-through. |
| 1246 | 86 | `mater omuium` | `omnium` | Commentary; found by the read-through. |
| 1247 | 23 | `In ordinem quem` | `ordine` | Latin verse (the commentary `In ordine`); found by the read-through. |
| 1248 | 5 | `dal septomo grado` | `septimo` | Italian verse XXXII 16 (the Latin `septimo`); found by the read-through. |
| 1249 | 21 | `a gradu in gradum*` | `inferiori` | Commentary lemma (the verse `a gradu inferiori`); found by the read-through. |
| 1250 | 12, 46 | `Causal puncto`, `amplius anxia` | `Casual`, `ausa` | Italian verse XXXII 53 (the Latin `Casualis`); the Latin verse (the Italian and the commentary `ausa`); found by the read-through. |
| 1251 | 36 | `et clarum nobis notatur` | `vobis` | Latin verse (the Italian `vi`, the commentary `vobis`); found by the read-through. |
| 1253 | 32, 46 | `quasi duo radices`, `Tantum contenta de` | `due`, `contentam` | Latin verse (the commentary `due radices`, `contentam`); found by the read-through. |
| 1254 | 8 | `E dirizzremo gl' ochi` | `dirizzeremo` | Italian verse XXXII 142; found by the read-through. |
| 1255 | 40, 87 | `stesso seute che`, `in quel di cono-` | `sente`, `dì` | Essay; no accent visible; found by the read-through. |
| 1259 | 83, 91 | `saum desiderium`, `petitionem pre-`/`curris` | `suum`, `precurrit` | Commentary (the verse `Suum`, `precurrit`); found by the read-through. |
| 1260 | 42 | `Vincat tua misericordia` | `custodia` | Latin verse (the Italian `guardia`, the commentary `custodia`); found by the read-through. |
| 1261 | 47 | `a[d] mentem non reddit` | `redit` | Latin verse (the commentary `redit` on 1262); found by the read-through. |
| 1262 | 101 | `intellectu creatu` | `creato` | Commentary; found by the read-through. |
| 1264 | 29, 59–60 | `afficiebatur accensa`, `et mi-`/`nium admiratione` | `efficiebatur`, `nimium` | Latin verse (the commentary `efficiebatur`); the commentary; found by the read-through. |
| 1266 | 7, 22 | `E tanto, che non basta`, `ad dicenduum parum` | `È`, `dicendum` | Italian verse XXXIII 123 (the Latin `Est`); no accent visible; the Latin verse; found by the read-through. |
| 1267 | 50 | `nondum et inventa` | `est` | Commentary (`nondum est inventa` on 1266); found by the read-through. |
| 1269 | 4 | `die mensi februarii` | `mensis` | Colophon (`mensis` in the next line); found by the read-through. |
| 1270 | 28, 47, 71 | `de'di nostri`, `ma altresi con`, `nella realta delle` | `dì`, `altresì`, `realtà` | Essay; no accent visible; found by the read-through. |
| 1276 | 58 | `et concenptum mirabilem` | `concentum` | Appendix (Bartholomaeus a Colle); found by the read-through. |
| 1277 | 47 | `maun Conditoris` | `manu` | Appendix; found by the read-through. |
| 1280 | 100 | `S'elli era l'opinione` | `erra` | Appendix lemma (the commentary `errant`); found by the read-through. |
| 1281 | 27, 48, 104 | `in omuibus inferioribus`, `et etiam in qualitate`, `formas corum` | `omnibus`, `quantitate`, `eorum` | Appendix; `in quantitate corporum` below; the `c` is printed; found by the read-through. |
| 1283 | 28, 46, 117 | `esser li rifracto`, `magis retrum quam`, `nix liquetit` | `lì`, `retro`, `liquefit` | Appendix lemma; no accent visible; the commentary; found by the read-through. |
| 1285 | 112 | `circam Deum` | `circa` | Appendix; found by the read-through. |
| 1289 | 113 | `Premanenza di affettuose` | `Permanenza` | Index; found by the read-through. |

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
  the reader passed over may remain. The read-through ("Read-through") reads for what
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
checks and the checks after completion. The conversion into `texts/la/` is
`texts/scripts/convert_la.py` (procedure, step 11).

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
