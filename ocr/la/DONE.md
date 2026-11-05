# Done: completing `ocr/la`

The record of how `ocr/la`, the transcription of Serravalle's translation and commentary
(1891), was completed and converted into `texts/la/` (2026-10-10 – 2026-11-01): the state at
the end, the work items, the procedure for a batch, the two-OCR markup method, what the
delegation taught, and the history. It was the body of [PLAN.md](PLAN.md) until the work
was done; PLAN.md now holds the checks planned after it; check 1, the verse check,
the italics and check 2, done, are recorded here ("Check 1", "Verse check", "Italics", "Check 2"),
with their order and what later work takes from them ("The checks"). Sections cited here that are not in
this file ("Standing rules", "Conventions settled during the check", "Suspected misprints",
"Known limits", "Sources for checking", "Tools") are in PLAN.md. "Remaining work" in the
text below means "Work items" here.

The work began with the batches of texts/PLAN.md ("Procedure for `la`", its batch table
and its delegation, batches 1–2); the two-OCR markup method replaced that delegation. The
goal was then to complete the rest (`0233`–`1296` and the front matter `0001`–`0078`):
the verse and the paid steps of the markup (procedure, steps 1–4) over all these pages at
once, the review and the steps after it (5–11) batch by batch.

## Summary (2026-11-01)

**All of `ocr/la` is complete** (`0001`–`1296`: the front matter, batches 1–11, the
appendix and the index) and converted by `texts/convert_la.py` into `texts/la/001`–`110`,
which cover the whole volume (scans `0007`–`1290`). Every work item is done;
nothing is pending.

- Batches 1–3 (`0079`–`0348`) were completed first (item 8, batch 3); batches 4–11 and the
  front matter were written from the mark decisions (item 8; steps 5–7 and the scripted
  checks of step 9 over every page of `tmp/la-mark7`), their broken pages retyped from the
  scan as each batch went (retypes 19–58, mostly la-el-agy, la-el-agy2 and la-el-agy3; in
  batch 11 also 17 pages by la-el-claude; in the front matter 0051–0053 and 0065).
- Tercet numbers and gloss marks are plain digits across all pages (item 9), and
  `texts/la` writes them so too.
- Steps 8 (`la_lines.py` and the image checks) and 11 (`texts/convert_la.py`) were done for
  every batch and the front matter (item 10; batches 4–6 2026-10-27, the rest 2026-11-01).
- `la_check.py`, `la_seqcheck.py` and `la_lostcheck.py` over 0001–1296 give no hits but the
  known exceptions (Suspected misprints, the printed brackets of 0545 and 0861, 1293's
  barcode, Tesseract's noise and figure labels); `convert_la.py` reports no `ERROR` (its
  `NO NUMBER` lines are the tercets 0099 leaves unnumbered in print).

The checks for what the method does not cover ("Not covered" below) are planned in
PLAN.md ("Checks").

"Complete" means, for every page (blank pages aside):

- both verse columns present, with their tercet numbers checked by `la_check.py`;
- every disagreement of `ocr/la` with GLM-OCR resolved by the markup method against
  the image (0104–0194 had also been proofread letter by letter before);
- blank lines checked against the printed rules, line breaks against Tesseract's lines,
  and dots before a lowercase word made commas (`la_lines.py`);
- the final checks (page heads, characters, accents, long lines) done.

Not covered (see "Known limits"): text that both OCRs read alike and wrongly (0085 `terret`
for printed `territ` was found by chance); italics were not transcribed. A check of the
italic lemmas against the verse of their page (check 1), a second reading of all the
verse from the image (the verse check) and the italics, marked `*…*` (2026-11-04), are
done (below), and so is a lexicon check (check 2, below).

Data: `ocr/la/glm-ocr/` (GLM-OCR for every page) and `ocr/la/tesseract/` (Tesseract's word
boxes for every page), both committed; the working data in `tmp/` (the paid answers) are
listed under "Tools".

## Check 1: lemmas against the verse (2026-11-01)

The first of the checks planned in PLAN.md ("Checks") after the completion, for errors
that both OCRs share. Done over 0079–1270 in 10 batches: 1,271 candidates, each decided in
the image with an independent reading of its lines by la-el-agy. Nine candidates were
misread in `ocr/la`; the readings of the same lines found about 80 more errors outside the
candidates, most in the Latin verse (not covered by the two-OCR markup: GLM-OCR drops it),
and the searches they led to (accented Latin and Italian words over all pages; repeated
runs of lines, after 1202 had a second copy of a verse block). The decisions are in
`ocr/la/lemmacheck.tsv`; the misprints found are in PLAN.md ("Suspected misprints").
The plan as it was written, the procedure per batch and the results follow.

### Plan and steps (`ocr/la_lemmacheck.py`)

The commentary quotes the verse it explains, in italics (not transcribed): a lemma is a
run of words from the Latin verse of the page, often a whole half-line (0113 `Ledit ventum:`
for the verse's `dedit ventum`, 0133 `nora`, 0142 `regola`, 0154 `traraglia`, 0389 `corum`;
all printed so, see "Suspected misprints"). Where a lemma and its verse differ by a letter or
two, one of them is likely misread.

1. **Script**: for each page with verse, the Latin verse lines of the page and of the page
   before (a lemma can quote a tercet set on the previous page), and the commentary of the
   page (the prose after the verse block and the gloss line). Align the commentary to the
   verse word by word: a run of at least 3 commentary words of which most equal verse
   words in order (case, punctuation and `u`/`v`, `i`/`j` ignored) is a lemma. In a lemma,
   list each word that differs from its verse word by an edit distance of 1–2 (letters, not
   spacing): page, line, commentary form, verse form, the verse line, both contexts. Also
   the Italian verse against the commentary, for the Italian quotations in the glosses.
   Options: `FIRST LAST`, `-o OUT`, `-v` (the lemmas found, for the trial).
2. **Trial** on batch 1 (`0079`–`0114`) and on the pages of the known cases (0113, 0133,
   0142, 0154, 0389): each must be listed. Look at the lemmas found (`-v`) on a few pages
   against the image, to tune the run length and the share of equal words (too loose takes
   ordinary prose that shares words with the verse).
3. **Run** over 0079–1270 (the cantos). If the list is longer than about 300, go batch by
   batch (the batches of DONE.md, item 8), committing each.
4. **Decide** every candidate in the image, both sides: the lemma and the verse word. A
   misread verse word is corrected too (it was transcribed from the images alone, so a
   verse error is possible). Record the decision in `lemmacheck.tsv`.
5. **Checks** after the fixes: `la_check.py`, `la_seqcheck.py` over the changed pages (no
   new hits), and the diff (only the decided words changed).
6. **Commit**: `ocr/la` (the fixes and `lemmacheck.tsv`), the script separately, then
   `texts` (regenerated by `uv run texts/convert_la.py`; its `HYPHEN` list read again), then
   PLAN.md (State, the results under the check, Suspected misprints).

Steps 1–3 are done: the script lists 1,240 candidates over 0115–1270 after batch 1, so
the run went batch by batch (batches 2–10, all decided).

### Per batch

Steps 4–6, the image reading delegated to la-el-agy; decided with the user,
2026-11-01):

1. **Crops**: `uv run ocr/la_lemmacheck.py FIRST LAST --crops DIR` writes every line of a
   candidate, the lemma's and the verse's (and the next line for a word broken by a
   hyphen), as `L0001.png`… in a shuffled order, so that the reader never sees a lemma
   beside its verse; `DIR/lines.tsv` maps them back (id, page, line, likeness). The lines
   are located by Tesseract (`ocr/la/tesseract/`); a line it cannot locate (likeness under
   0.8: a runover, a line Tesseract misread) gets no image and goes to `DIR/unlocated.tsv`.
   The images go to a working directory under `tmp/` (not committed).
2. **Task**: a task file for la-el-agy: read every image letter by letter as printed, from
   the images alone (no `ocr/la`, no Dante text), and write `readings.tsv`
   (`L0001<TAB>line`); a crop showing two whole lines is read as both, joined by ` / `.
   It carries feedback on the previous batch: every line the delegate misread, with the
   printed form. Its usual errors are a letter changed toward a familiar or grammatical
   word (`Figliuol` for `Figluol`, `bonam` for `bonum`, `eorum` for the misprint `corum`)
   and a letter or mark dropped at a line end.
3. **Send** only on the user's signal (the user switches the delegate's model by hand),
   with the rules of the delegation (no subagents, no git changes, no shell redirects).
4. **Compare**: `uv run ocr/la_lemmacheck.py FIRST LAST --readings DIR -o OUT`. A candidate
   that both read alike is decided `printed`. Every difference is decided in an enlarged
   crop: `DIFFERS` (the candidate) and the `c>`/`v>` line diffs (any other word of the
   line). The lines of `unlocated.tsv` are read in the page image. Most real misreads so
   far were outside the candidates, in the same lines, often in the Latin verse (accents
   not printed, `mihi` for `michi`).
5. **Fix and record**: correct `ocr/la`; append one row per candidate to `lemmacheck.tsv`
   (`printed`, note `verse PAGE:LINE FORM`; a misread candidate under its printed form with
   `misread X before this check`), and one row per misread found outside the candidates.
   A misprint also goes into "Suspected misprints"; a misprint listed there that the image
   does not bear out is taken out (0205 `aranzare`). An error that may recur on other pages
   is searched for over all pages (batch 4: accented Latin words).
6. **Checks**: `la_check.py` and `la_seqcheck.py` over the changed pages give the same
   output as before the fixes; the rerun of the batch lists no candidate.
7. **Commit**, as step 6: `ocr/la`, then `texts`, then PLAN.md (State, the results row,
   Suspected misprints). No push unless asked.
8. **Next batch**: its crops and task file are prepared at once, and wait for the signal.

What the reading by la-el-agy taught: it was letter-exact on 96–100% of the lines, and
its readings found most of the errors outside the candidates. Its errors were a letter
changed toward a familiar or nearby form (`figlio` for `figlo`, `exoneret` for
`exponeret`, `Phetonte` for `Phetont`, `L'affecto` for `L'affetto` after the verse) and
crops cut short at a line end. In batch 9 its first readings of 60 images (L0001–L0060)
were not readings of those images at all, and its report did not say so: every batch's
readings are first matched to their lines (the similarity of each reading to its line in
`ocr/la`; under 0.8 it is not a reading of that image), and such lines are read again.

### Results

| Batch | Pages | Candidates | Misread | Notes |
|-------|-------|-----------:|--------:|-------|
| 1 | 0079–0114 | 33 | 0 | outside the candidates: 0095 `omme` → `omne` |
| 2 | 0115–0232 | 107 | 1 (0124 `altera` → `altèra`) | outside: 0123 `Mihi` → `Michi` (verse), 0190 `ccensa` → `censa`, 0205 `aranzare` → `avanzare` (listed as a misprint before; the image shows an italic `v`) |
| 3 | 0233–0348 | 131 | 0 | outside: 0249 `comprehendisti` → `comprehendidi` (verse; the lemma has it too) |
| 4 | 0349–0478 | 148 | 1 (0444 `de-`/`scrivere` → `scribere`) | outside: 14 lines, most in the Latin verse (0368 `Insìmul`, `faciei`; 0406 `Sciâs`; 0425 `emictiunt`; 0426, 0471 `mihi` for `michi`; 0432 `Priùs`; 0436 `subcinctum`; 0458 `Capraia` for `Capra[ra]`; 0471 `Priùsquam`), 0412 `Così` ×2, 0446 `molles,` (for `mol-`/`les,`) and an added `Et`. The Latin accents not printed led to a search of all pages for accented Latin words: 0461 `Ianuâ`, 0471:103 `Priùsquam`, 0640 `Nimìs` corrected; 0546 `Deûm` is printed |
| 5 | 0479–0608 | 135 | 5 (0521 `per-`/`mitteret` → `micteret`; 0547 `summítas`; 0568 `discerneham`; 0575 `Tilonis` → `Titonis`; 0603 `Egu-`/`bii,` → `Eugubii,` on one line) | outside: 15 lines, most in the Latin verse (0490 `Aeris` → `Aieris`; 0492, 0526 `societate` → `sotietate`; 0493 `ream,` → `ream;`; 0496, 0569 `mihi` → `michi`; 0506 `Quicunque` → `Quicumque`; 0540 `aëre` → `aiere`; 0541 `disfécit`; 0582 `plantas` → `planctas` ×2; 0591 `timetúr`; 0592 `procedebat` → `precedebat`; 0595 `ride[n]t` → `vide[n]t`). The batch 4 accent search had missed acute accents: a search for them corrected 11 more (0490 `devenít`, `habuít`; 0541:33 `aëre`; 0591:55 `imprimítur`; 0597 `despiciébat`; 0614 `martyríi`; 0662 `Mísit`; 0719 `rumorís`; 0734 `Redít`, `redít`; 0742 `utiliús`); 0926 `quómodo` is printed. The same search over the Italian words: 0526 `Phetón`, 0614 `fuggíro`, 0805 `Parríano` corrected, 0614 `lí` → `lì`; 0247 `félli`, 0366 `Férsi`, 0418 `Minós`, 0739 `cóntemperare`, 0948 `sí` are printed |
| 6 | 0609–0740 | 140 | 2 (0670 `Recordcris` → `Recorderis`; 0716 `tunc` → `tuuc`, a turned `n`) | outside: 10 lines (0628 `paucum` → `paucam`; 0639 `societatis` → `sotietatis`; 0649 `ditiores` → `dictiores`; 0653 `somno` → `sompno`, all in the Latin verse; 0653:75–76 `potes te su-` / `stinere;` → `potes` / `te sustinere;`, and `medium` → `mediam`; 0686 `non sentitur` → `uon seutitur`, turned `n`s; 0730 `rimaso` → `remaso`; 0734 `concordabat` → `concorda[ba]t`) |
| 7 | 0741–0870 | 149 | 0 | outside: 5 lines, all in the Latin verse (0748 `tibi` left out; 0749 `societatem` → `sotietatem`; 0772 `ymnpo` → `ympno`; 0777 `inditum` → `inditium`; 0807 `Xerxes` → `Xerses`). The italic `c` without the eye of an `e` is kept as printed (0764 `volca`, 0777 `Fericbat`, 0855 `iciuna`) |
| 8 | 0871–1010 | 135 | 0 | outside: 5 lines (0943 `volvit` → `voivit`, a dotted `i`; 0976 `Brentae` → `Brente`, Latin verse; 0978 `Ferrariensem` → `ferrariensem`; 0978:89–90 `parti-` / `alem scilicet` → `partia-` / `lem, scilicet`; 1001 `dicum` → `dicam`) |
| 9 | 1011–1140 | 155 | 0 | outside: 2 lines, both in the Latin verse (1053:52 `Contemplando perpeduo, et qui me assidet, idest me` → `Cum perpetua visione, et qui me sitibundum facit`, a whole line not of the print; 1129 `litore` → `lictore`). The delegate's first readings of 60 images (L0001–L0060) were not of those images and were read again |
| 10 | 1141–1270 | 138 | 0 | outside: 5 lines (1144 `attrahatur` → `attrahitur`, 1146 `spendorum` → `splendorum`, 1164 `gyrarit` → `gyravit`, all in the Latin verse; 1207 `scipso` → `seipso`, a damaged `e`). 1202 had a second copy of the Latin verse 24–29 between the two commentary columns (since the first OCR; it read `aeris`); removed. A search for repeated runs of three lines over all pages found no other |

## Verse check: the verse read again (2026-11-01 – 2026-11-03)

The second of the checks planned in PLAN.md ("Checks"), decided with the user on
2026-11-01 for the Latin verse and on 2026-11-02 for the Italian. Step 0 compared the
Latin verse with the Italian text (503 lines listed, 25 misread, 6 misprints); then every
line of both verse columns of 0079–1270 was read again from the image, in a trial and 10
batches, the Italian by la-el-agy and the Latin by la-el-agy2, and compared with `ocr/la`
by `ocr/la_versecheck.py`: 227 lines misread and 40 misprints, each a row of
`ocr/la/versecheck.tsv`; the misprints are in PLAN.md ("Suspected misprints"). The plan
as it was written, with the results of step 0 and of each batch, follows.

### Plan and steps (`ocr/la_versecheck.py`)

The Latin verse has had one reading only: the first OCR's (la-el-agy's on 0836), outside
the markup, as GLM-OCR drops it. Check 1 read again only the lines that a lemma quotes and
found about 40 errors there (`mihi` for `michi`, `societate` for `sotietate`, accents not
printed, `spendorum` for `splendorum`, a whole line not of the print on 1053), so the
other lines likely hold as many. Every line of the Latin verse is read again from the
image and compared. The Italian verse, though in the markup (GLM-OCR reads it), is read
again too (decided with the user, 2026-11-02): the trial found accents that both OCRs
dropped (`Si` for `Sì`) and a misprint read as the sense (`miei` for `mici`). It is
compared with the print only: the edition's Italian is one manuscript's
(texts/la/README.md, "The Italian text") and differs from modern editions in most lines.

0. **Text against the Italian** (decided with the user, 2026-11-01), before any image:
   the Latin verse is a line-by-line translation of the Italian beside it, so a misread
   that changes the sense (1053's whole line, `spendorum`, `gyrarit`)
   shows against the Italian. `uv run ocr/la_versepairs.py -d DIR` writes each canto's
   verse as pairs (`canto page tercet line italian latin`; 100 cantos, 14,233 lines, all
   tercets paired). la-el-agy reads the pairs, a cantica a task, and lists the lines where
   the Latin clearly does not say what the Italian says (another line's words, a word of
   unrelated sense, a word missing or added that changes the sense, a word that is no
   Latin), not the translation's freedoms or the manuscript's spellings (`michi`, `e` for
   `ae`). The text only: no images, no other Dante text. Each listed line is then decided
   in the image (`ocr/la_view.py word`), corrected if misread, and recorded in
   `versecheck.tsv`; the rate of real errors among the listed lines and among check 1's
   verse errors (how many the list would have found) decides with the user whether the
   reading from the image (steps 1–4) is still needed, and for which lines.
   - **Inferno** (008–041, 4,720 lines; done): 110 lines listed. 20 were the runover
     words set beside the next line (the pairs had them on the wrong line; the
     convention under "Brackets" now places them, and all pages were done). Of the
     other 90: 3 misread (0095 `invetis` → `iuvetis`; 0402 `ridet` → `videt`, in the
     verse and in its lemma, so check 1 could not see it; 0450 `promererar` →
     `promerear`), 4 misprints (Suspected misprints: 0085 `co`, 0227 `est`, 0259
     `prerogatiram`, 0439 `leravit`), 83 printed so (the translator's: `plus` for
     `men`, `puppim`/`proram` swapped, `-didi` perfects). None of check 1's Inferno
     verse errors was listed: they are all spellings and accents (`mihi`, `Insìmul`,
     `emictiunt`, `Capra[ra]`), which leave the sense alone; step 0 finds only
     misreadings that change a word.
   - **Purgatorio** (043–075, 4,755 lines; done): 226 lines listed, 70 of them only for
     the editor's brackets (`[quod]`, `relarg[a]vit`). 18 misread: 0492 `Excundo` →
     `Exeundo`; 0496 `perpende di` → `perpendi de`; 0540 `Fugiendos` → `Fugiendo`;
     0556 `accol lectiones` → `accollectiones` (verse and lemma); 0568 `deviahat` →
     `deviabat`; 0569 `voluit` → `volvit`; 0582 `Respondiit` → `Respondit`; 0605 `quifa`
     → `qui[a]`; 0617 `Tune` → `Tunc` (verse and lemma; the search found 6 more in the
     commentary: 0217, 0383, 0537, 0719, 0729, 1185); 0624 runover `[nationem],` →
     `[nationem,`; 0634 `s[c]iugat` → `sciugat` (the lemma prints `[s]ciugat`); 0637
     `Vidissem` → `Vidisses`; 0639 `reminifcor` → `reminiscor` (verse and lemma); 0640
     the runover `[delectat` was missing; 0642 runover `[spieit:` → `[spicit:`; 0651
     `introyu` → `introytu`, `Respondera` → `Respondere`; 0723 `planetas` → `planctas`
     (`ct` for `t`, as 0582). 2 misprints (Suspected misprints: 0530 `quiu`, 0606 `cum`),
     206 printed so (`ventrum` for `centro`, `Metellus` for `Marcel`, the Italian words
     left in the Latin: `balzo`, `soggiorno`, `sprazzo`). Most misreadings this time
     were letters (`c`/`e`, `h`/`b`, `f`/`s`), which made a non-word; check 1's
     Purgatorio verse errors were again spellings and accents, but for 0592
     `procedebat` and 0595 `ride[n]t`, fixed before the pairs were written.
   - **Paradiso** (076–108, 4,758 lines; done): 167 lines listed. 4 misread: 1026
     `Cœlum` → `Celum`; 1053 `arrosoruit` → `arrosonuit`, and the runover `[cennum` was
     missing (the commentary 1054 has `arrosonuit`); 1194 `&` → `et`; 1229 `redolel` →
     `redolet`. No misprint; 0956 `fuitvel` is set without a space. 163 printed so (the
     Italian words left in the Latin: `bieci`, `gaggiorum`, `vivagnis`, `soggiornum`;
     `adymat`, `badalucchem`, `scioliis`, `dicenduum` as printed). 21 of the notes named a
     word that is in neither column (`Dante nos` for `Dinanzi a noi`, `amovi`,
     `impingit`): la-el-agy's notes invented them, and those lines were found printed so.
     Check 1's Paradiso verse errors (1053's whole line, `spendorum`, `gyrarit`) were
     fixed before the pairs were written, so whether the list would have found them is
     not known.
   - **Over the three canticas**: 25 misread among 503 listed lines (14,233 lines), most
     of them letters that made a non-word (`Excundo`, `redolel`) or a word of another
     sense (`ridet` for `videt`); 6 misprints. The spellings and accents that were most
     of check 1's verse errors leave the sense alone and are not found by step 0.
1. **Script** `ocr/la_versecheck.py FIRST LAST [--italian] --crops DIR` writes one image
   per verse line (the Latin block of `ocr/la` as `la_lemmacheck.py` finds it, or the
   Italian with `--italian`; the gloss lines at the block's end left out), enlarged 2×
   and in a shuffled order, as check 1's crops (`DIR/lines.tsv` maps them back; a line
   that Tesseract cannot locate, mostly a runover word, goes to `DIR/unlocated.tsv` and is
   read in the page image).
   `--readings DIR [-o OUT]` compares the reader's `DIR/readings.tsv` (`L0001<TAB>line`)
   with `ocr/la` line by line: the differing words (letters and accents, not the
   punctuation) and the tercet number; a line whose words agree but whose punctuation
   differs is listed as `punctuation` (in the script after batch 3, before that a short script
   in the session); apostrophe spacing is not judged (Conventions: "Apostrophe spacing as
   in the file"). This replaces the page-column crops first
   planned (`la_versecrop.py`): single lines in a shuffled order keep the reader from
   reading a known passage.
   `--page-crops DIR` writes one image per page instead (`DIR/P0115.png`: the verse block
   of the page, the box of its located lines, enlarged 2×, in page order; `DIR/pages.tsv`
   counts its lines); the reader writes its lines in order (`P0115<TAB>line`, one row per
   printed line, a runover word as its own row). `--page-readings DIR [-o OUT]` aligns
   them with the lines of `ocr/la` page by page, by the likeness of their letters, and
   compares them as `--readings` does; a line not paired is counted as not read, a
   reader's line not paired is listed as `extra`.
2. **Trial** on batch 1 (`0079`–`0114`; done, 2026-11-02):
   - Latin: 414 lines read, 8 differ. 4 misread, all toward a common form: 0095
     `Seculum` → `Seclum`, 0098 `caveas` → `caves`, 0101 `redii` → `redivi`, 0113
     `transivit` → `transirit` (a misprint, Suspected misprints). 4 reader errors: the
     known misprint `co` written `eo`; tercet numbers `36`, `33` read `38`; `eorum` written
     `corum`, the very example of the task (a task names kinds of error, never words that
     may be in the batch).
   - Italian: 413 lines read, 8 differ in words, 2 more in punctuation. 4 misread: 0096
     `Si` → `Sì` twice, 0100 `l'anno` → `l'ànno`, 0086 `miei` → `mici` (a misprint);
     0087 `dogla.` → `dogla,`, 0090 `venire,` → `venire;`. The search over all 86 Italian
     lines starting `Si` found 3 more `Sì` (0400, 0595, 0662). 4 reader errors
     (`veuir`, `14` for `44`, `proposito`, `riconosciuto`); 19 lines differ only in
     apostrophe spacing, not judged.
   - About 1% of the lines were wrong; the readings were reliable. Decided with the user:
     go on over 0115–1270, the Italian and the Latin as separate tasks, in 10 batches.
3. **Batches** (canto boundaries; lines of the Latin / Italian verse):

   | Batch | Pages | Latin | Italian |
   |---|---|---|---|
   | 2 | 0115–0232 | 1,358 | 1,346 |
   | 3 | 0233–0348 | 1,404 | 1,395 |
   | 4 | 0349–0464 | 1,477 | 1,468 |
   | 5 | 0465–0586 | 1,417 | 1,407 |
   | 6 | 0587–0692 | 1,326 | 1,319 |
   | 7 | 0693–0812 | 1,473 | 1,462 |
   | 8 | 0813–0924 | 1,338 | 1,326 |
   | 9 | 0925–1048 | 1,455 | 1,436 |
   | 10 | 1049–1150 | 1,329 | 1,319 |
   | 11 | 1151–1270 | 1,476 | 1,466 |

   **Images**: line images (`--crops`) in batch 2; page images (`--page-crops`) from batch 3
   on (decided with the user, 2026-11-02: the line images were too many and too small to
   work through, about 1,350 per task against about 92 pages; in batch 2 the Italian reader
   pasted them 10 to a sheet itself, so the lines were read side by side anyway, and at the
   smaller size it misread 24 tercet numbers against 1 in batch 1). Page images also show
   the runover words that line images could not locate, and a line printed twice on a page
   (0133:8 and 10), whose line image was cut from the wrong row. They show the context,
   so the reader may be led more by the sense (agy's main failure mode): the task says so
   plainly, and the error rate is compared with batches 1–2. The edge of the other column (line ends,
   tercet numbers) may show: the task says to leave it out.

   **Batch 2** (0115–0232; done, 2026-11-02):
   - Latin: 1,353 lines read, 26 differ in words, 5 more in punctuation. 9 misread: 0121
     `tanquam` → `tamquam`, 0170 `circumvolvitur` → `circumvolvatur`, 0214 `sociis` →
     `sotiis`, 0226 `moriendi` → `moriendo`; 0117 `dixit` → `dixit,`, 0122 `tanto.` →
     `tanto:`, 0147 `ingenia.` → `ingenia,`; and two runover words joined to their line,
     put on their own line (Conventions, "Brackets"): 0117 `ad` / `[fundum,`, 0189
     `indignatio-` / `[nem.`. Reader errors: 8 tercet numbers, 6 words (`Ciacchum`,
     `Iosaphat`, `dilatione`, `bulicame`, `Nesus`, `Lano`: common forms and corrected
     names), 2 punctuation marks; from the crops, 3 lines cut at an edge where the
     Tesseract box missed a word, 2 crops of two lines, 1 line of the other column.
   - Italian: 1,345 lines read, 40 differ in words, 18 more in punctuation. 3 misread:
     0168 `figliuolo` → `figluolo`, 0194 `perch'io` → `per ch'io`, 0216 `damni` →
     `danni` (stems counted). Reader errors: 24 tercet numbers and 5 gloss numbers (read
     on sheets of 10 lines it made itself), 10 words (misprints corrected, `Verrauno`,
     `Trhaemmoci`; common forms, `Colui`, `fui`, `lì`), 3 lines cut short. The gloss
     marks without a space were spaced (Conventions, "Gloss marks").
   - The 6 unlocated lines, read in the page image, were right. 0133:8 and 10 print the
     same line, so the line image of 8 was cut from 10.
   - The other `figliuol` forms (9, on later pages) and `soci-` are read in their batches.

   **Batch 3** (0233–0348; done, 2026-11-02; the first with page images):
   - Latin: 1,404 lines, 1,403 paired with a reading (0260:34, read in another word order,
     was left unpaired), 15 differ in words, 2 more in punctuation. 6 misread: 0240
     `introyttus` → `introytus`, `montana` → `montanea`, `vetusta.` → `vetata.`, `elegit` →
     `ellegit`, `plingebat` → `plangebat` (five in one passage, all from the first
     transcription), 0260 `Fuit maioris gradus` → `Fuit gradus maioris`. 3 misprints
     (Suspected misprints: 0241 `tumquam`, 0261 `bonum`, 0338 `vium`). Reader errors: no
     tercet numbers; 10 words (the three misprints and 0259 `prerogatiram` corrected,
     `inviscabat`/`inviscatas` read `inviscidabat`/`inviscidatas`, `respondidi`,
     `recolsit`, `corruscet`, `[tomem.`), 2 punctuation marks.
   - Italian: 1,395 lines read, all paired, 8 differ in words, 2 more in punctuation. 2
     misread: 0253 `protesi` → `protesï`, 0345 `maravigliar` → `maraviglar`. Reader
     errors: no tercet or gloss numbers; 4 words (`conoscuto`, `soglono`, `sgaglarda`
     made the common forms, the `ï` of 0318 `dïsse` left out). 4 marks read where the file
     keeps its reading: 0271 a mark over the `g` of `glurchi` (a smudge), 0276 a faint
     grave on `à`, 0262 a raised dash after `dole` (above the hyphen's height), 0275 a
     gloss mark printed `(°)` for the `(1)` of its note (kept `(1)`, the link to the note).
   - Against batch 2 (line images), the tercet-number errors fell from 8 and 24 to none;
     word errors toward the usual form stayed (10 and 4). The page images did not show
     more reading from the sense.

   **Batch 4** (0349–0464; done, 2026-11-02):
   - Latin: 1,477 lines read, 27 differ in words, 14 more in punctuation, 1 extra. 29
     misread, most from the first transcription: letters (`discosscenditur`, `ymmum`,
     `membrorum`, `abhorris`, `Reperiuimus`, `Cozzavcrunt`, `Bisscntium`, `Tribaldeilo`
     and the same in its commentary, `corrossit`, `permicit`), words (0402 `mihi` →
     `michi`, 0426 `Et` → `Sed`, 0439 `apparuit` → `apparet`, 0458 `te` and 0461 `ad
     eum` not printed), brackets (0411 `dimis[iss]es`, 0416 `applicat[ur]`), 11
     punctuation marks, and the runover 0439 `[ego.`, left out (the lines below it move
     by one). 5 misprints (Suspected misprints: 0396 `posest`, 0446 `Guctaverunt`, 0455
     `[ricinus.`, 0461 `citernam`, `proximani`). Reader errors: no tercet numbers; 5 words
     (`Repercutiendo`, `iterum`, the known misprint `leravit` corrected, `decomas`,
     `interrogaveris`), 3 punctuation marks (spaces around `;` and `,`). The reader's
     `Cochitum;` of batch 3 (0241:42) was right by the punctuation rule; the file is
     corrected, and so are the 31 other spaces before `:` or `;` the search found (21
     pages, 0374–1225, mostly commentary; Conventions, "Punctuation").
   - Italian: 1,468 lines read, 21 differ in words, 5 more in punctuation, 3 extra. 6
     misread: 0356 `Sì` → `Si`, 0400 `maraviglia` → `maravigla`, 0406 `ch’e’n` →
     `ch’è’n`, 0423 `si` → `sì`, 0433 `gl'occhi` → `gl'ochi`, 0444 `(11) :` → `(11):`.
     1 misprint: 0363 tercet 6 has no number (Suspected misprints, as 0099; `la_check.py`
     and `la_seqcheck.py` list it, `convert_la.py` reports `NO NUMBER`). Reader errors: 1
     tercet number; 9 words (common forms: `piglio` ×2, `applicar`, `trafito`,
     `sarebbono`, `scioca`; the known misprint `sn` corrected; the `ï` of 0378 left out,
     0374 `ï` added); 3 marks where the print has a smudge or a broken letter (0388
     `città`, 0389 `infamia`, 0420 `crucciata`); 2 runover words written without `[`
     (0461 prints none; the file keeps the convention).
   - The 3 extra Italian lines (0402:16, 0414:24, 0449:15) start with a gloss mark, and
     `la_lemmacheck.page_parts` took every such line for a gloss line, so the verse check
     left them out; the readings agree with the file. `page_parts` now leaves out only
     the gloss lines at the end of a verse block (`(1) al. pianto.`): 11 verse lines of
     0079–1270 start with a gloss mark, none in the Latin. Of those before batch 4, 0166:15
     was looked at in the image and agrees; `la_lemmacheck.py` gives the same output.
   - Against batch 3, the tercet-number errors stayed near none; the Latin had the most
     misread lines of any batch so far (29), from the first transcription, not from the
     reader.

   **Batch 5** (0465–0586; done, 2026-11-02):
   - Latin: 1,417 lines read, 30 differ in words, 10 more in punctuation. 29 misread, most
     from the first transcription: letters (`ellecti`, `montanea` as 0240, `atterrando`,
     `faciant`, `rubecchium`, `vocabolum`, `smiragdum`, `interrogavit`, `pavefacta`,
     `arsiccia`, `amassicciatur`, `Biasmantuam`, `permictit`; the last two also in the
     commentary 0507:70 and 0582:80), words (0492 `Qui` → `Que`, `denegatur` →
     `denegetur`, 0493 `totum` → `totam`, 0547 `Respondet` → `Respondit`, 0566 `quae` →
     `que`, 0572 `Incepit` → `Incépit`), a bracket (0506 `e[s]t`), 9 punctuation marks. 1
     misprint (Suspected misprints: 0529 `sinistrun`; 0525 `ventrum` was listed). Reader
     errors: no tercet numbers; 11 words (the misprints `sinistrun` and `ventrum`
     corrected, `Giudecca`, `cum` ×2, `Desposaverat`, `nigresiebat`, `excicatos`,
     `Biamantuam`, an accent and a bracket added), 1 punctuation mark.
   - Italian: 1,408 lines read, 21 differ in words, 10 more in punctuation. 17 misread:
     letters (`meglor`, `consiglo` ×2, `gl'ochi`, `ochi`, `andavàn`, `vogle`, `vechio`,
     `macciulla`, `A'miei`, `percuote` without the ring of `ů`), 0523 the gloss mark
     `(1)` left out (its note was on the page), 0539 `un' altro` → `un altro` (a dot at
     mid height, not an apostrophe), and 0469 five `‘l` with a space before, printed
     `’l` joined (the one other `‘`, 1022:7, made `’`). 2 misprints (Suspected misprints:
     0468 `parca`, 0514 `Quant'um`). Reader errors: no tercet numbers (one with a stray
     dot); 9 words (the two misprints corrected, `uscimmo`, `reporterò`, `trascorrer`,
     `Sì`, `Quel`; a speck read as an accent on 0492 `le`), 3 punctuation marks. 0527:10
     prints a mark over the `i` of `mio`, wider than a dot (the reader's `mĭo`); not
     plainly an accent or a diaeresis, the file keeps `mio`.
   - `la_check.py` over 0465–0586 and 1022 and `la_seqcheck.py` give the same output.

   **Batch 6** (0587–0692; done, 2026-11-02):
   - Latin: 1,326 lines read, 29 differ in words, 8 more in punctuation. 29 misread:
     letters (`Que` ×2, `[ecplanas:`, `Ylyon`, `Horestes`, `compaxus`, `riparie`,
     `tralucat`, `graminee`, `Ugolini`, `Bertenorium`, `Fulgur`, `permictit`,
     `introytum`), words (0637 `audiendum` → `videndum`, `parcens` → `parcus`, 0651
     `nomine` → `nomen`), the names of 0639 (`Prata`, `Transversarie`, `Anestasiorum`,
     `Castrocarium`, where the reader had `Castrocorium`), 0614 four gloss marks `(1)`–`(4)`
     not in the print (left from the first OCR; the notes (1)–(16) are the Italian's), 5
     punctuation marks. The commentary keeps its own forms (`Faventia`, `Traversarie`,
     `Bertennorium`, `Castrocardium`), not checked. 3 misprints (Suspected misprints: 0592
     `mimus`, 0639 `Farentia`, 0647 `co`). Reader errors: no tercet numbers; 8 words (the
     known misprints `cum` and `co` corrected, `suam`, `Filii`, `compassionem`,
     `reinfames`, `Castrocorium`, `Conium`), 2 punctuation marks (0613 a period made a
     comma, 0685 `vadit,non` spaced).
   - Italian: 1,320 lines read, 23 differ in words, 7 more in punctuation. 18 misread:
     letters (`agl'ochi`, `gl'ochi`, `ginochia`, `effecti`, `giuncto`, `ofitio`,
     `appettibile`, `figluol`), accents (`siàn`, `Cimabù`, `lì`, `fuggì` added; `manna`, `e`
     without one: 0599 a speck over the `a`), 0603 the gloss mark `(1)` left out (its note
     was on the page), 3 punctuation marks (0594 `ch',a` without a space, as printed). 5
     misprints (Suspected misprints: 0605 `Selvani`, 0612 `Semnaar`, 0623 `Com`, 0625 `um`,
     0652 the gloss mark `(3)` for `(8)`). Reader errors: no tercet numbers; 9 words (the
     four misprints corrected, `Udì`, `Dì`, `cavalier`, `fregar`, an accent on 0600 `noi`),
     3 punctuation marks (0652 the mark `(3)` made `(8)`, two spaces added after commas).
     0600:14 prints a grave over the gap between the `o` and the dotted `i` of `noi` (the
     reader's `nòi`); the file keeps `noi`, as 0527 `mio`.
   - `la_check.py` over 0587–0692 and `la_seqcheck.py` give the same output.

   **Batch 7** (0693–0812; done, 2026-11-02):
   - Latin: 1,473 lines read, 7 differ in words, 7 more in punctuation. 3 misread
     (`ammannat`, 0724 `Et, quare`, 0792 `[cta est,`). 3 misprints (Suspected misprints:
     0709 `Etipse`, 0734 `tanctum`, 0745 `tor tam`). Reader errors: no tercet numbers; 3
     words (`planetas`, `cara`, `Feriebat`), 5 punctuation marks (0770 and 0777 a period
     made a comma, 0746 `adhuc ?` closed up, 0747 the mark of `operandum·est` and 0807
     the dot of `rideo,.` left out).
   - Italian: 1,465 lines read; apart from the tercet numbers, 21 differ in words, 12 more
     in punctuation. 12 misread: letters (`ripiglammo`, `miglor`, `agl'ucellin`,
     `s'affigge`, `c'affigghono`, `maravigla`), accents (`ch'ànno`, `ridiàn` added),
     0805 `Avegna che` (was `Avegnache`), 3 punctuation marks (0742 `oggimai,chè` without
     a space, as printed). 3 misprints (Suspected misprints: 0725 `(9,` and 0737 `(12.`
     without the closing parenthesis, 0753 `si munta`). Reader errors: the tercet numbers
     left out on every page from 0752 on (242 lines; `la_seqcheck.py` checks them against
     the Latin); 12 words (`repetiam`, `insieine`, `dì'`, `hymno` ×2, `Lemosì`, `'ntesi`;
     specks read as marks: 0712 `decrèto`, 0772 `Ché`, 0781 and 0805 `chę`, 0805
     `fiumícel`), 7 punctuation marks (0722 a period made a comma, six gloss marks closed
     up to the word, which the rules space).
   - `la_check.py` over 0693–0812 and `la_seqcheck.py` give the same output.

   **Batch 8** (0813–0924; done, 2026-11-02):
   - Latin: 1,338 lines read, 3 differ in words, 7 more in punctuation. 5 misread
     (`proiïcendo`, 0818 `similitudines;`, 0842 `Postea,quando` without a space, as
     printed, 0890 `pertransit,` and `satietatem,`). Reader errors: no tercet numbers; 2
     words (`desviando`, `deveni[ur]`), 4 punctuation marks (0826 a period made a comma,
     0890 a period left out, 0844 a comma added where the `m` is broken, 0843 the mark
     before `'fecerunt` left out).
   - Italian: 1,327 lines read; apart from the tercet numbers, 6 differ in words, 7 more
     in punctuation. 5 misread: `aïuti` (the `ï` was left out), `saecta`, `ch'ànno`, 0878
     `Penneya (11),`, 0922 `[spense (3),`. 3 misprints (Suspected misprints): 0856 tercet
     44 and 0897 tercet 31 have no number, 0878 the gloss mark `(8)` for `(18)`. 0897 keeps
     its `31`, since the scripts find a verse block by the number of its first line.
     Reader errors: 1 tercet number (0814 `1`); 3 words (the misprint `orese` corrected,
     `voller`, 0853 `çondocti` read `condocti`), 4 punctuation marks (0898 the misprint
     `(22)` corrected, 0836 a space left out, 0894 a speck at mid height read as a period,
     0850 a dot far after the line end written; the file leaves it out).
   - `la_check.py` over 0813–0924 and `la_seqcheck.py` give the same output, but for
     0856, which they now list for its missing number, as 0363.

   **Batch 9** (0925–1048; done, 2026-11-02):
   - Latin: 1,455 lines read, 10 differ in words, 4 more in punctuation, 1 extra. 7
     misread (0932 `te` left out, `prius quam`, 0982 `planta,`, 1029 `secundum,`, 1034
     `Scripturas` without a comma, 1034 `intra 'consilium`, as 0843 `'fecerunt`), and 0994
     `sibi [tardo.]`, which the first OCR left inside the line: the print has the runover
     `[tarda.`, now its own line (the page's later lines move down by one;
     `lemmacheck.tsv` 0994:60 and the note 0994:47 follow; the batch now has 1,456
     lines). 1 misprint (Suspected misprints: 0952 `Isia`). Reader errors: no tercet
     numbers; 6 words (`volitione`; the printed `athletha`, `vincit`, `Quae` and the known
     misprint `palec` corrected; `fuitvel` split, where no space is printed).
   - Italian: 1,436 lines read; 13 differ in words, 5 more in punctuation, 1 in the
     tercet number. 7 misread: `parìa`, `Così` (accents left out), `meglo` (the stroke
     through the `o` is not an accent), `l'ochio` (was `l'Ochio`), `maravigla`, `famigla`,
     `consiglo`. 1026 `Ciò` and `sentì` were written with combining accents; now
     precomposed (no other page has them). Reader errors: none in the tercet numbers but
     0955 `29.`, whose period is printed (the file leaves it out); 4 words (`ïn` and `Sì`
     from specks, `Cinisa`, `Alcide` for `Alcyde`), 5 punctuation marks (0969 the gloss mark `(2)` read `(1)`, four
     gloss marks closed up to the word).
   - `la_check.py` over 0925–1048 and `la_seqcheck.py` give the same output.

   **Batch 10** (1049–1150; done, 2026-11-03):
   - Latin: 1,329 lines read, 13 differ in words, 7 more in punctuation, 6 extra. 17
     misread: six runover lines, three missing (1051 `[concordes?`, 1135 `[vestris,` and
     `[quod ego`) and three joined to their line by the first OCR (1079 `[tardum.`, 1111
     `san-` / `[ctarum!`, 1125 `in-` / `[terrogo.`), now each its own line (the batch now
     has 1,335 lines; the later line numbers of those pages in `lemmacheck.tsv`,
     `versecheck.tsv` and Suspected misprints 1135 follow); words (`opima`, `que`,
     `Mirabilius`, 1135 `quando est aperta,`, 1088 `[v]ivit` with its printed brackets,
     1144 `dilatare,eo` without a space), 6 punctuation marks (1068 `barce,`, 1088
     `folia,`, 1100 `pulchrum,`, 1142 `grati,` were periods or a semicolon; 1071
     `gloriosum,`). 3 misprints (Suspected misprints: 1076 `meu`, 1143 `puucum`, 1148
     `remunsere`). Reader errors: no tercet numbers; 2 words (`christianus`, the known
     misprint `[ficum,` corrected). 1080 `Anima. sancta` keeps its comma (Conventions,
     "Commas").
   - Italian: 1,319 lines read, 12 differ in words, 3 more in punctuation. 4 misread:
     1053 `udìo` (was `u'dio`: a broken `d`, no apostrophe), `simiglanze`, 1071
     `glorioso,`, 1081 `Conscienza` (a speck under the `i`, no dieresis). 2 misprints
     (Suspected misprints: 1091 `Um`, 1124 `scalco`). Reader errors: no tercet numbers; 8
     words (the known misprint `sactta` and `Ninphe` corrected; the `fi` ligature read as
     `t` twice, 1112 and 1126 `fisso` as DONE notes; the printed graves of `s'àdempia` and
     `udìo` left out; `udì'` twice, no accent printed), 2 brackets spaced off their word
     (`quel [lo]`, `iovia [l]`).
   - `la_check.py` over 1049–1150 and `la_seqcheck.py` give the same output.

   **Batch 11** (1151–1270; done, 2026-11-03):
   - Latin: 1,476 lines read (23 runovers, all their own lines), 11 differ in words, 3
     more in punctuation. 6 misread: 1153 `ita,quod` without a space, 1170 `abbagliaris`
     (no comma printed), 1181 `EL` (a small capital `L`; the commentary's `EL` on line
     100 corrected too), 1213 `Sancti;`, `ammodo`, 1251 `tantam`. 2 misprints (Suspected
     misprints: 1242 `corum`, `habundatiam`). Reader errors: no tercet numbers; 6 words
     (`istam`, `contempor`, `consentietur`, `baptismate` without the printed `h`, the
     known misprint `dicenduum` corrected, `Propier` for the printed `Propter`, reported
     as a misprint).
   - Italian: 1,467 lines read, 245 differ in words, 6 more in punctuation, nearly all
     from 1222–1254 (Paradiso 30–32), where the reader left out every tercet number
     (reported as not printed; they are) and wrote the gloss marks as superscripts.
     Without those, 9 misread: 1171 `felice (1)!` (was `(!)`), 1179 `(5)` (was `(3)`),
     1179 `supplìco` (the grave is printed), 1182 tercet `47` (was `57`, the error
     `la_check.py` and `la_seqcheck.py` reported), 1206 `(4) 'l notturno` (was
     `l'notturno`), 1206 `gl'ochi`, 1210 `vincto`, `Phylosophando`, 1247 `mei,`. 1
     misprint (Suspected misprints: 1206 `(2)` for `(12)`). Reader errors: 7 words
     (`inmota`, `abborre` and `specchio` for the printed `immota`, `abbhorre`, `spechio`;
     `trascorse`, `egualmente`, `reflexo`; 1177 `[S']`, 1261 `che'` from specks) and
     spaces after apostrophes in 1222–1254.
   - `la_check.py` over 1151–1270 and `la_seqcheck.py` give the same output but for the
     1182 tercet number, no longer reported.

   **Per batch**: the crops in `tmp/la-verse/bN/` (Latin) and `tmp/la-verse/bN-it/`
   (Italian); the Italian task to la-el-agy, the Latin to la-el-agy2, each carrying the
   feedback on its previous batch, sent only on the user's signal. The readings are first
   matched to their images (a reading that is not of its image is read again); every
   difference is decided in an enlarged crop (`ocr/la_view.py word`, or the page image
   where Tesseract has no box); `ocr/la` corrected; one row per misread line, and per
   reader error that looks like a variant, in `versecheck.tsv` (`page line form decision
   note`); a misprint goes into "Suspected misprints"; an error that may recur is searched
   for over all pages.
4. **Checks** and **commit** as in check 1 (steps 5–6): `la_check.py` over the batch's
   pages (the whole range takes too long) and `la_seqcheck.py` give the same output as
   before the fixes (batches 1–3 checked so); `ocr/la`, then `texts`, then PLAN.md
   (State, the results, Suspected misprints).

## Italics: the printed italics marked (2026-11-01 – 2026-11-04)

The third of the checks planned in PLAN.md ("Checks"), decided with the user on
2026-11-01, its method changed on 2026-11-03 and 2026-11-04. The italics of the whole
volume are marked `*…*` in `ocr/la` and kept by `convert_la.py` in `texts/la`: the cantos
0079–1270 in a trial batch and nine parts, set from the slant by `ocr/la_italic.py` and
`ocr/la_italicmark.py` and decided in the image where flagged; then the essays (three
parts), the appendix and the front matter, and a sweep of the runs split at a stop. The
convention that stays is in PLAN.md ("Conventions settled during the check", "Italics").
The plan as it was written, with the record of each step and part, follows.

### Plan and steps (`ocr/la_italic.py`, `ocr/la_italicmark.py`)

The printed italics are transcribed, the lemmas first. **Changed with the user
(2026-11-03)**: checking the italics page by page in the image is too slow, so a few
sample pages were looked at, the conditions under which the print uses italics were
estimated from them, and the marks are set from the text by a delegate (an LLM) under
these conditions, cross-checked by the slant script. **Changed again with the user
(2026-11-04)**: from Inferno 9 the marks are set from the slant by script
(`la_italicmark.py`), without a delegate, and only the lines it flags are decided in the
image (step 3, "Without a delegate" and "Per part"). Fidelity to the print in every
detail is not sought: marks set by mechanical conditions are accepted (the user,
2026-11-03).

- **Mark**: `*…*` in `ocr/la`, as `ocr/en-oelsner` keeps its italics; not a table, as
  line positions shift with every fix. Each line keeps its own pair, so a page stays line
  for line: `*dedit ven-*` / `*tum*:`, closed before the line end and reopened on the next
  line. **Punctuation, a mechanical convention instead of the print**: the stop that ends a
  lemma (`:`, `,`, `.`, `;`, `?`) and a closing `etc.` stay outside the pair; punctuation
  inside the lemma stays inside (`*Quando Deus, sive amor divinus*:`). An Italian lemma
  and its Latin one side by side are two pairs (`*Mosse dapprima*. *Movit primitus*:`).
  The existing `*` of 1283 (`154*`, printed) is not a mark.
- **What is italic** (batch 1, 0079–0114: the slant script's runs read against the text,
  2026-11-03): nearly all italics of the commentary are quotations of the canto's verse,
  Italian or Latin, as lemmas: at the head of a paragraph or sentence, ending at a colon
  (195 of 248 runs; a comma or `?` for most others), an explanation in roman following.
  They are often not the verse letter for letter: one or two words (`Hora:`), the Italian
  in the commentator's manuscript spelling (`Senbiava`), the Latin in his own wording
  (`Hic expellet eam:` for the verse's `Hic eam fugabit`); a lemma can stand inside a
  running sentence (0106 `conduxit me intra secretas res`, `fioche`). Roman, though they
  quote or paraphrase the verse: the commentator's own words before a colon (`Vult dicere
  ita:`), the quotations of the chapter divisions (after `ibi vulgariter:`), a quotation
  that fills a line by itself (0098 `O donna de vertù, per cui,`), and some close
  quotations inside a sentence (0106 `Diverse lingue, orribiles loquutiones`). Italic,
  though the text alone gives no sign of it: the incipit a summary quotes (0079 `quod
  incipit: In medio itineris vite nostre`), and the commentator's Latin retelling of a
  tercet set as a sentence of its own (0108 `Postquam ego, aliquos eorum noscens,
  perspexi, scilicet vidi …`, glosses and all; 0113 `Hiis finitis, obscura campania
  tremuit …`, with a roman stretch inside it). Other
  italics, rare: words cited as words (0109 etymology `ab A, quod est sine, et chaire`),
  a decretal's name (0108 `Pastoralis`); in the essays (0114) titles and emphasis. The
  titles of works (`in sexto Eneydos`, `Metheororum`) and the quotations of other authors
  (the Bible, Virgil, Aristotle) are roman: of batch 1's 58 `other` passages only those
  two kinds measured italic. The text alone cannot decide
  every case (the best text rule found missed 47 of the 195 colon lemmas and took 34 roman
  ones), hence the cross-check.
- **Spellings**: a word of a lemma spelled otherwise than in the verse is not recorded or
  looked at: check 1 compared such words (1,271 candidates, 9 misread), and a form shared
  wrongly by both OCRs is left to check 2 (decided with the user, 2026-11-03; the trial
  delegate listed 47 on 5 pages, nearly all the manuscript's forms).
1. **Slant script** (`ocr/la_italic.py FIRST LAST -t TESS [-o OUT] [-v] [--boxes DIR]`):
   done. For each commentary word, the slant of its strokes over the box of its Tesseract
   word (the box widened four times, so that a shear moves rows by fractions of a pixel);
   italic from 0.16, roman up to 0.09 (italic measures about 0.27, roman 0), unknown
   between; output per page: the runs of italic words and the lemma of check 1 they
   overlap. On the sample pages about one missed or false word a page, in lines where
   Tesseract's boxes are wrong (0087:74, a line misread; 0087:94, boxes shifted a word).
2. **Trial of the delegate** (la-el-agy, 0084 0098 0099
   0106 0107, 2026-11-03): its marks against the slant runs differed in 15 lines, decided
   in the image: the delegate was wrong in about 9 places (4 roman quotations marked, 5
   italic passages missed), the slant script in 3 (words it measured upright). These five
   pages are written into `ocr/la` with those 15 lines decided (50 pairs). Where the two
   agree nothing was looked at.
3. **Per batch**: the delegate marks the lemmas from the text (task file: the conditions
   above, with examples from pages outside the batch; output one file per page and
   `notes.tsv` of `unsure` and `other` passages); a script checks that the words are
   unchanged (`*` removed, the file is equal) and every line closed, and lists the lines
   where its marks and the slant runs differ. Those lines are decided by the reading of
   their line images, not by eye page by page.

   **Batch 1** (la-el-agy, the 28 canto pages of 0079–0113
   but the trial's 5; 2026-11-03): the files were exact and closed. Its marks and the slant
   runs differed in 52 lines, which I decided from their line crops myself (**deviation**:
   not given to a delegate, as the crops of 52 lines took less than a task would). The
   slant script was right in 43: 16 lines marked but roman (most of them lemmas inside a
   sentence: 0089 `humilis Ytalia`, 0112 `Fili mi, illi qui moriuntur in ira Dei`), 23
   italic but not marked (the incipits and retellings above, which the delegate had listed
   `unsure`; 0101 `allecte`), 4 the `other` italics (etymologies, `Pastoralis`; marked
   after the scope was widened, below, with the one-letter `A` read in the image). The
   delegate was right in 9, where the slant script measured a word wrong or Tesseract's
   boxes were wrong (0087:74, 0101:71). So where several words of a line disagree the slant
   script is nearly always right; a single word needs the image. 0092, 0102 and 0114 are
   essays (step 4). Written into `ocr/la`: 291 pairs on the 33 pages.

   **Parts** (decided with the user, 2026-11-04): the rest is done in nine parts at canto
   boundaries, each cantica in three (Inferno as 1 + 33: its first canto is the proem, so
   1–12, 13–23, 24–34), and committed part by part. Pages to mark: the canto
   pages (summary and commentary); left out: the Italian essays closing each canto, blank
   pages, the half-titles (0077, 0477, 0871) and the preamble of Purgatorio (0479–0486: no
   verse to quote; step 4). Paradiso 1's summary (0873–0874, under `INCIPIT PARADISUS`) is
   marked.

   | Part | Cantos | Pages | To mark | Essays |
   |---|---|---|---|---|
   | 1 | Inferno 1–12 | 0079–0220 | 125 (33 done in batch 1) | 13 |
   | 2 | Inferno 13–23 | 0221–0347 | 108 | 13 |
   | 3 | Inferno 24–34 | 0349–0476 | 111 | 13 |
   | 4 | Purgatorio 1–11 | 0477–0607 | 106 | 12 |
   | 5 | Purgatorio 12–22 | 0609–0739 | 113 | 12 |
   | 6 | Purgatorio 23–33 | 0741–0869 | 112 | 13 |
   | 7 | Paradiso 1–11 | 0871–1009 | about 120 | 14 |
   | 8 | Paradiso 12–22 | 1011–1140 | 112 | 13 |
   | 9 | Paradiso 23–33 | 1141–1270 | 113 | 11 |

   **Part 1, Inferno 4** (la-el-agy, 0115–0126, sent in
   about ten pages at the user's wish before whole parts; 2026-11-04): files exact and
   closed; 34 lines differed. The 19 lines where three or more words differ: 12 looked at,
   the slant script right in all; most were retellings the delegate marked after batch
   1's feedback but printed roman (0119 `Respondit, scilicet magister: Ego eram novus`,
   0126 `Euclidem geometram, scilicet vidi, …`), while like ones beside them are italic
   (0121 `Interdum vox fuit audita, que dixit:`, `Bonus magister cepit dicere:`): the text
   cannot tell them apart. The 15 lines of one or two words, all in the image: the slant
   script right in 10 (`*Smalto*,`, `*Le quale*:`), the delegate in 5 (a bracketed
   insertion inside a lemma, `[eorum]`, is italic; 0125 `Zeno` measured wrong). Written
   into `ocr/la`: 139 pairs.

   **Part 1, Inferno 5** (0129–0138, 2026-11-04): files
   exact and closed; 48 lines differed (4.8 a page, against 2.8). The 26 lines of three or
   more words: 10 looked at, the slant script right in all. Most were a verse quotation the
   delegate marked to its end where the print sets only its head in italics and the rest
   of the quotation roman, after a gloss or straight on (0134 `*Et ipse*: supple magister,
   dixit michi: Videbis quando` / `erunt plus propinqui, …`; 0137 `*vides, adhuc non me
   relinquit*: amor conduxit nos ad` / `unam mortem`); the other way, retellings printed
   italic (`*Prima harum, de quibus nora tu vis scire*, dixit`). The 22 lines of one or two
   words, all in the image: the slant script right in 16, the delegate in 6 (a lone
   capital at the line head measured about −0.20: 0131 `Non`, 0135 `Nos`, 0138 `Nos`;
   `etc.` outside the pair by the convention). Written into `ocr/la`: 137 pairs.

   **Part 1, Inferno 6** (0141–0149, 2026-11-04): files
   exact and closed; 41 lines differed (4.6 a page), all looked at in the image: the
   slant script right in 36, the delegate in 5 (0143 `*Vertunt*`, 0145 `non`, 0147
   `nunc`, a lone capital at the line head: 0145 `Vos`, 0149 `Nos`). Inferno 5's feedback
   (italics only up to the first gloss) made the delegate stop there, but here the print
   mostly goes on in italics after the gloss, the gloss alone roman (0145 `*Sed dic
   michi*: *Quis tu es in tam doloroso loco expo-*`; 0146 `*vitatis partite*? (idest
   divise) *si aliquis est in ea iustus*`; 0149 `*tamen plus ultra, idest iuditium, quam
   citra et*` with the gloss inside), while Inferno 5 has the rest roman: the text cannot
   tell where a quotation's italics end. A bracketed `(alias sum)` has `alias` roman, `sum`
   italic. Written into `ocr/la`: 140 pairs.

   **Part 1, Inferno 7** (0151–0160, 2026-11-04): the
   first-gloss rule withdrawn, the delegate marked the quotations through to their end;
   files exact and closed; 65 lines differed (6.5 a page). The 37 lines of three or more
   words: 19 looked at, the slant script right in all; nearly all were long quotations
   the delegate marked and the print sets roman (0157 `Ille, cuius scientia omnia
   transcendit, …` over seven lines; 0158 `Quare una gens imperat, scilicet dominatur, et
   alia lan-`; 0160 `Tunc bonus magister dixit: Fili, iam vides animas il-`), beside like
   ones italic (0159 `*Sed ipsa est beata, et hec non audit*;`). The 28 lines of one or
   two words, all in the image: the slant script right in 22 (single words glossed inside
   a sentence: `*troppam*:`, `*urlis* (idest`, `*per*` / `*rim*, idest …, *puppis*,
   idest`; words cited as words roman: `Pape`, `Alpha`, `Guerci`), the delegate in 6
   (0152 `Ay iustitia` in the chapter divisions, measured +0.38; 0159 `bisei` on a shifted
   box; a line-head capital `Non`; 0156 `Vanas`, 0158 `Verum`). After four cantos the
   delegate's rate does not fall: each correction moves its errors to the other side.
   Written into `ocr/la`: 110 pairs.

   **Part 1, Inferno 8** (la-el-codex at the user's wish,
   0163–0170, 2026-11-04): the task cut down to the basic rules, as finer rules only moved
   the errors; files exact (no spelling changed) and closed; 204 pairs marked, 118 lines
   differed. This canto's print sets in italics only the head of a lemma (`*E io
   dico*:`, `*Corda*:`, `*In ceno*:`, `*Cui ego*:`) and a word or two glossed inside a
   sentence (`*follem*, idest`, `*la pugna*: idest`), the Latin retelling after it roman;
   codex marked the retellings throughout. 37 lines looked at in the image (all 18 of one
   or two words): the slant script right in all. The lines were rebuilt from the slant
   by script (an unknown or one-letter word takes its measured neighbours), one fixed by
   hand (0167 `*A fangosis gentibus*:`). Written into `ocr/la`: 56 pairs.

   **Without a delegate** (2026-11-04): the same canto given to la-el-agy for comparison
   differed from the final marks as much as codex (117 lines against 118). A script that
   marks from the slant alone (the stream of a paragraph across line ends; an unknown or
   one-letter word takes its neighbours, a broken word's halves the larger slant, a
   capital just before an italic word is taken in, `etc.` stays out) and flags the lines
   to look at (Tesseract's words unlike the line; an unknown word where italic and roman
   meet; a broken word's halves unlike; a word unlike both neighbours) was tried on
   0079–0170 (82 pages) against the final marks: 26 lines differ, 23 of them flagged; 76
   lines flagged (0.93 a page, against 5–7 lines a page differing with a delegate); 3 lines
   missed (0095 `O musa` on a misread box, 0108 `ista` italic, 0167 a lone `*O*` at the
   line end). It also found two errors of the final marks, corrected in the image: 0147
   `*num*:` (the half of `do-` / `num`), 0152 `A adverbium` (roman).
   Matching the verse (la_lemmacheck's passages) adds nothing: italic and roman meeting
   inside a matched passage with no stop flags 10 lines, 8 differing, all flagged
   already; an italic run outside any passage flags 395 lines for one more (0108 `ista`);
   a passage with no italic flags 391 lines and none differing (most matched passages are
   roman retellings).

   **Part 1, Inferno 9** (0173–0182, 2026-11-04): the first canto by the script alone, as
   a test on pages it was not made from. Every commentary line was read in the image
   (the columns at 0.6 scale). The script's marks differed from the print in 3 lines: 0179
   `*s'abbica*` (the `s'` left out; flagged), 0175 `*Ego*: scilicet Dantes:` (a
   paragraph's head measured +0.04) and 0178 `ex` (+0.16, at the threshold), the last two
   not flagged. Two flags were added for them: `alone` now looks at the nearest measured
   words past an unknown one and flags a lone italic word under +0.20; `head` flags a
   paragraph's first word roman before a colon with italics after it. With them all 3
   are flagged (12 lines in all), and on 0079–0170 the flags grow from 76 to 78 lines with
   the same 3 missed. Written into `ocr/la`: 93 pairs. Seen in passing and corrected:
   0180:81 `virgula` (the verse's word) for the print's `virga`.

   **Part 1, Inferno 10–12** (0185–0195, 0197–0205, 0207–0219; 2026-11-04): by the script
   alone, the slant run over 0185–0219 at once (the essays 0196, 0206 and 0220 left out).
   43 lines flagged on 33 pages (1.3 a page; most of them single Italian words glossed
   inside a sentence, `*stia*, idest`, `*roccia*, idest`, flagged `alone`, and right), all
   decided in the image; 3 corrected, all a short word or an apostrophe at the head of an
   italic run: 0203 `ab *a*, quod est *sine*` (an etymology, the one-letter `a`), 0209
   `*a chi su fosse*`, 0212 `*s'approccia*` (as 0179 `*s'abbica*`). The 7 `box` lines
   (0187, 0192, 0194) were all roman. Written into `ocr/la`: 41, 63 and 68 pairs. Seen in
   passing and corrected: 0201:83 `Biscalia` for the print's `Biscatia`.

   **Part 2, Inferno 13–23** (0221–0346, 2026-11-04): by the script, the slant run over
   0221–0347 at once (the 13 essays left out). 348 lines flagged on 108 pages (3.2 a page:
   these cantos gloss many single Italian words inside a sentence, `*fuschi*, idest`,
   nearly all right), all decided in the image. A rule was added first, from 0226
   `m'adeschi` and 0227 `m'acchora` (as 0179 and 0212 before): an elided one-letter word
   takes the side of the word after it (`*m'adeschi*`); on 0079–0219 it changes no line
   but 0179 and 0212, now right. Then 24 lines corrected: 8 a short word at the head of
   an italic run (`*a la caccia*`, `*la lena*`, `*a brano a brano*`, `*a[d] giuocum*`); 4
   a capital taken in by the capital rule though roman (0236 `Alia *raccolta*`, 0250
   `Dicit *si*`, `de Dante *ficus*`, 0274 `Hic *distorsit*`); 6 a roman word measured
   italic (0277 `ego`, 0295 `Ziezi`, `Zeizi`, 0299 `distorsit`, 0301 `Ecclesie`, 0341
   `honeratam`); 4 italics missed (0247 `*Iam eramus a silva remoti*`, 0277 `*scroscium*`,
   0323 `*De[h]*`, 0339 `*mo, mo*`); 0240 `*paiese* de-` / `structum`, the broken Latin
   word roman. Inferno 13 (0221–0231) was read through in the image: no line the script
   did not flag was wrong. Written into `ocr/la`: 87, 80, 60, 55, 77, 83, 54, 38, 67, 52
   and 45 pairs (698). Seen in passing and corrected: 0276:66 `giocum` for the print's
   `giuocum`; 0228:57 `eraramo` for `eravamo` (the italic `v`).

   **Part 3, Inferno 24–34** (0349–0474, 2026-11-04): by the script, the slant run over
   0349–0476 at once (the essays and blank pages left out, 111 pages marked). 201 lines
   flagged (1.8 a page), all decided in the image; 24 corrected: 10 a capital taken in by
   the capital rule though roman (0352 `Nos, *pur*`, 0364 `Tota *groppa*`, `Super
   *spallas*`, 0365 `Edera *abbracciata*`, 0366 `Bononia *Rigoro*`, `Tuscia *Ramarro*`,
   0369 `Gaville, *piange*`, 0377 `Dicit *cornuta*`, 0402 `Vel *mazzerati*`, 0410 `Quid
   *pur*`); 8 a roman word measured italic (0403 `Uberti, audientes`, 0422 `et`, 0438
   `de-` / `scribat` and `et sic`, 0449 `recessit`, 0454 `Ay` twice, 0455 `comite`); 3 a
   short word left roman inside a run (0361 `*vel ad finem, verborum suorum*`, 0372
   `*poichè sì grande*`, 0425 `*non ci à*`); 2 a bracket inside a word splitting the run
   (0354 `*A[l]latro*`, 0459 `*viser[i]e*`); 1 italics missed (0461 `[ab *a*]`). The
   capital rule was tried narrowed, over 0221–0474 against the corrected pages: kept only
   at a paragraph's head it fixes 13 lines and breaks 11 (`*Non era anchora di là*`, `Ad
   *domum*`, ...), at a sentence's head it fixes 5 and breaks 6; so it stays as it is (its
   wrong lines were all flagged). Inferno 24 (0349–0358) was read through in the image: no
   line the script did not flag was wrong. Written into `ocr/la`: 44, 47, 19, 38, 52, 36,
   37, 26, 32, 26 and 40 pairs (397). Seen in passing and corrected: 0425:103–104
   `gre-` / `ppum` for the print's `grep-` / `pum`; 0444:58 `babhum` for `babbum`;
   0456:71 `dominus` for `domnus` (`domnus, idest dominus`).

   **Part 4, Purgatorio 1–11** (0487–0606, 2026-11-04): by the script, the slant run over
   0477–0607 at once (the half-title, the preamble 0479–0486, the 12 essays and blank
   pages left out by the essay rule; 106 pages marked). 144 lines flagged (1.4 a page), all
   decided in the image; 85 of them `box`, 59 of these on 0549, whose commentary under a
   verse block is printed all roman and left unmarked. 15 lines corrected: 8 a roman word
   measured italic (0507 `Nec`, 0517 `erat`, 0523 `recessit`, 0526 `zo-` / `diacum`, 0533
   `oc-` / `cupasset`, 0539 `ego`); 4 a short word left roman inside a run (0502 `*a
   poco*`, 0559 `*a guisa*`, 0599 `*nos regnum tuum*`, `*non dimictimus*`); 1 a capital
   taken in by the capital rule (0512 `Dicit *vesprum*`); 1 a verse incipit of the
   chapter divisions, printed bold (0544 `Ay Italia serva,`); 1 italics missed on a `box`
   line (0515 `*Pudicam*`). Purgatorio 1 (0487–0496) was read through in the image: no
   line the script measured was wrong, but 0489:11–12 (`*Propter currere meliorem aquam
   elevat vela*. *Per*` / `*correr miglior acqua alza le vele*:`) were not measured, as
   the line began with a tercet number the print does not have (a superscript `¹` of the
   first transcription, made `1` at item 9); the number taken out and the two lines
   marked by hand. Written into `ocr/la`: 26, 29, 27, 14, 22, 17, 22, 27, 15, 18 and 40
   pairs (257). Seen in passing and corrected: 0489:11 the number; 0493:102 `apparentia
   .in vista` for the print's `apparentia. in vista` (written `apparentia, *in vista*`,
   the dot before a lowercase word); 0526:51–52 `stric-` / `tius` for `stri-` / `ctius`;
   0572:45 `se ipsum; etsi que in limitibus demon` for the print's `se, sicut bestia que
   se linit, quia demon`. `la_check.py` changes only on 0489 (blank lines 3 to 2, the
   number taken out: the paragraph no longer counts as a verse block).

   **Part 5, Purgatorio 12–22** (0609–0738, 2026-11-04): by the script, the slant run over
   0609–0739 at once (the essays and blank pages left out, 113 pages marked). 52 lines
   flagged (0.5 a page), all decided in the image; 10 corrected: 5 a roman word measured
   italic (4 words: 0622 `pe-` / `traie`, 0640 `eo`, 0688 `Sancto Zeno`, 0731 `intra`); 2
   a capital taken in by the capital rule (0659 `Dicit, *occidat*`, 0713 `Pigmaleon
   *allocta*`); 1 italics missed (0674 `*al*` / `*niego*`); 2 a bracket inside a word
   splitting the run (0672 `*De l'empiezz[a]*`, 0733 `*O[r] quando tu cantasti cruda
   arma*`). As the bracket case came back (0354 and 0459 in part 3), `la_italicmark.py`
   now takes the pieces of a word joined by a bracket together; over the slants of parts
   1–5 this changes those four lines and 0323 `*De[h]*` (part 2, decided so in the image)
   and nothing else. Purgatorio 12 (0609–0618) was read through in the image: no italics
   wrong, but 0614 and 0617 had transcription errors (below), so the lines put back from
   the image in batch 6 (0617, 0639, 0646, 0720) were read again too: right but for
   0646's. Written into `ocr/la`: 14, 12, 22, 14, 20, 21, 16, 16, 15, 19 and 26 pairs
   (195). Seen in passing and corrected: 0614:37 `event` for the print's `evenit`, :39
   `matris` for `patris`, :40 `Ideo Almeon apparere` for `Ideo Almeon fecit apparere`, :41
   `duru` for `durum`, :50 `im potentem` for `impotentem`, :51 `miserere tur` for
   `misereretur`, :56 `animo;` and :69 `Cyrum;` for `animo:` and `Cyrum:`, :83–84 `Ab` /
   `tulit` for `Ab-` / `stulit`; 0616:82 `troyitum` for `troytum`; 0617:80 `cantauerunt`
   for `cantaverunt`, :84–85 `levis,` / `quam` for `le-` / `vis, quam` and `videbatur` for
   `videbat[tur]`; 0646:61 `anthartico` for the print's `authartico` (put back in batch
   6).

   **Part 6, Purgatorio 23–33** (0741–0869, 2026-11-04): by the script, the slant run over
   0741–0869 at once (the essays and blank pages left out, 112 pages marked). 44 lines
   flagged (0.4 a page; 16 of them box, all roman in the image), all decided in the image;
   8 corrected: 3 a roman word measured italic (0814:22 `Dum ego`, a verse of the summary
   quoted in roman; 0822 and 0840 `ego`); 1 a capital taken in by the capital rule (0795
   `Ytalicos *mancia*`); 4 italics missed, a word of one or two letters inside a lemma
   (0752 `*Nè 'l*` / `*dir l'andar …*`, 0772 `*a quando a quando*`, 0776 `*Mentre che si
   per l'orlo*`, 0805 `*parve, si com'egli*`). Written into `ocr/la`: 10, 23, 17, 17, 15,
   13, 18, 18, 15, 16 and 19 pairs (181). Seen in passing and corrected: 0859:4–5 `auc-` /
   `tor de-` for the print's one line `auctor de-` (a line too many in the summary).

   **Part 7, Paradiso 1–11** (0871–1009, 2026-11-04): by the script, the slant run over
   0871–1009 at once (the half-title, essays and blank pages left out, 122 pages marked,
   Paradiso 1's summary under `INCIPIT PARADISUS` with them). 56 lines flagged (0.5 a
   page; 23 of them box), all decided in the image; 11 corrected: 7 a roman word measured
   italic (0883 `Si ego`, 0899 `ego`, 0917 `nec diutius`, 0926 `in`, 0965 `intelligendo
   tertium celum movetis`, the Latin after the Italian quoted, 0991 `revolutiones` and
   `quando`); 1 a capital taken in by the capital rule (0956 `In *Psalmis*`); 3 italics
   missed (0877 `ab *a*, quod est sine`, 0893 `*a guisa*`, and 0925 `*Si ego [te] in-*`,
   the bracketed word italic too). Written into `ocr/la`: 19, 23, 13, 12, 13, 11, 18, 20, 19, 17 and 22 pairs
   (187).

   **Part 8, Paradiso 12–22** (1010–1140, 2026-11-04): by the script, the slant run over
   1010–1140 at once (essays and blank pages left out, 112 pages marked). 63 lines flagged
   (0.6 a page; 27 of them box), all decided in the image; 4 corrected: 2 a roman word
   measured italic (1089 `huius`, 1112 `ego`); 1 a roman word taken into a pair (1102
   `Dei, *vista*`); 1 italics split (1138 `*Tu se' si presso al*`, the Italian quoted
   whole). 1044's figure labels (`q` four times) left unmarked: letters in a figure, not
   commentary. 1026's part-division verses, flagged as box, roman in the print, as
   marked. Written into `ocr/la`: 25, 17, 15, 22, 17, 13, 18, 16, 18, 13 and 21 pairs
   (195).

   **Part 9, Paradiso 23–33** (1140–1270, 2026-11-04): by the script, the slant run over
   1140–1270 at once (essays and blank pages left out, 113 pages marked). 146 lines
   flagged, 99 of them on three pages: 1153 (82 lines, all box: the scan skewed, the
   words placed on the wrong boxes) and the figures of 1245 and 1247 (17); the other 47
   (0.4 a page; 18 box) decided in the image. 1153 read whole in the image: its
   commentary is roman but for `*Flam-*` / `*meando*:`, so the 43 pairs the script made
   there were dropped and that one written. The figure labels of 1245 and 1247 (a script
   hand) left unmarked, as 1044's. Of the other lines, 3 corrected: 1 a roman word
   measured italic (1248 `ego`); 1 a roman word taken into a pair (1189 `De *Caorsa*`); 1
   italics split (1227 `*Non è fantin che sì*`, the Italian quoted whole). Written into
   `ocr/la`: 14, 13, 18, 21, 24, 20, 12, 14, 19, 13 and 17 pairs (185).

   Per part (from Inferno 10; the script adopted by the user, 2026-11-04, in place of a
   delegate), one canto at a time:
   1. The slant runs: `la_italic.py FIRST LAST -t ocr/la/tesseract -v -o SLANT` over the
      canto's pages.
   2. `la_italicmark.py SLANT -d OUTDIR -o FLAGS`: the pages marked from the slant (the
      essays left out) and the lines to look at.
   3. The flagged lines decided in the image (line crops) and corrected in OUTDIR; the
      words unchanged and every line closed.
   4. Written into `ocr/la`; `la_check.py` over the pages and `la_seqcheck.py 79 1270`
      unchanged against a snapshot of `HEAD`; `convert_la.py` (only `NO NUMBER` 0099 ×2,
      0363, 0856); this section updated with the canto's counts. A transcription error
      seen in passing is corrected (confirmed in the image) and noted here.
   Inferno 1–8 went through a delegate (batch 1 and the records above), Inferno 9–34,
   Purgatorio and Paradiso through the script.
4. **Scope**: the canto pages, the lemmas and the `other` italics (words cited, a name
   like `Pastoralis`; widened with the user, 2026-11-04, and batch 1 reviewed). Widened
   again with the user (2026-11-04), after the parts: the essays, front matter and
   appendix too, every italic as printed. Surveyed by the slant (counts rough): the
   appendix 1271–1287 about 940 italic words (its lemmas, as in the cantos); the essays
   (Inferno 39 pages, Purgatorio 38, Paradiso 37) about 570 (titles of works, Latin
   quotations, sources abridged, emphasis); the notizie 0015–0042 about 100 a page on
   0022, 0027, 0029, 0031 and 0033–0038 (incipits, explicits, titles), few elsewhere;
   the documenta 0043–0054 a few a page (archive references); the epistola 0059 about 58
   (its address); the rest of 0007–0076 nearly none. Pages with none (the Purgatorio
   preamble 0479–0486, the index 1289–1290, the half-titles 0077, 0477, 0871) are looked
   at once in the image and recorded as such (the preamble had one: part 2). Conventions for the new kinds: titles and
   sources abridged (`Tratt. del Purg.`, `Clem. VII Antip.`) marked as printed, the
   period after the last letter as in the cantos; small capitals (`DROUILHET DE
   SIGALAS`) not italic; verse quoted in an essay as printed (mostly roman, 0382); figure
   labels unmarked; a source abridged one pair, its inner periods inside (step 2).
   Steps (committed only when all are done, with the user, 2026-11-04; split as in step 6):
   0. **Scripts**: `la_italicmark.py` given an option to mark the pages named (now it
      leaves the essays out); `la_italic.py` to skip a page it cannot locate (0001 and
      0004 fail in `locate`). The canto pages' output unchanged.
   1. **Appendix** 1271–1287, as the parts.
   2. **Essay trial** (no commit): a few pages of different kinds (0114, 0382, 0542,
      0750, 0901, 0902) read whole in the image against the script's marks, to count
      the words wrong but not flagged and the lines flagged (essay pages are one
      paragraph a line, the alignment untried there). Reported to the user, who
      decides: the flagged lines only, as in the parts, or every page read whole.
   3. **Essays**, three parts (Inferno, Purgatorio, Paradiso), by the method of step 2;
      a page stored a paragraph a line is read whole in the image (part 1: its flags
      missed too much there), the others by the flagged lines and the search.
   4. **Front matter** 0007–0076, one part: 0022, 0027, 0029, 0031 and 0033–0038 read
      whole; the rest by the flagged lines.
   Checks per part as in step 3, with `la_check.py` and `la_seqcheck.py` also over the
   pages outside 79–1270 that the part touches.

   **Step 0** (2026-11-04): `la_italicmark.py --pages SPEC`; `la_italic.py` skips a page
   with no Tesseract words. Over 0079–0100 both give the same output as before. Found on
   the appendix: `convert_la.py` measured a line's length and end with its marks, so a
   marked line could end or continue a paragraph wrongly (a printed paragraph split after
   `*Ver'è che come forma*, etc. Antipophoram facit nunc.` / `Quia posset …` joined, or
   two joined), and a page ending `*ven-*` was not carried to the next page. Now measured
   without the marks (`bare()`): 31 canto files of parts 1–9 changed back to the
   paragraphs they had before the italics (`54d95b0`, the marks removed: the same line
   count in every file but 054, whose difference is part 5's corrections on 0617).

   **Step 1, the appendix** (1271–1287, 2026-11-04): the slant run over 1271–1287 (1271
   the half-title and 1272 blank, no commentary; 15 pages marked with `--pages`). 15
   lines flagged (6 alone, 5 letter, 4 lone, 2 box), all decided in the image; 4
   corrected: 3 an italic word measured roman (1277 `*Questi ne porta al fuoco inver*`,
   1280 `*e qui*`, 1282 `*sì digiuno Esto pianeta*`), 1 a lemma's head measured roman
   (1278 `*Ver'è che come forma*`). The marked lines also searched for a lemma begun
   roman or a run across a roman word (13 lines looked at in the image): 2 more
   corrected, not flagged (1275 `*[E sì come secondo raggio suole*`, the bracket inside
   as `*[Così …*`; 1280 `Theologia, *che son li segni bui*`, a roman word taken in). The
   footnotes (1274, 1282) measured roman. Written into `ocr/la`: 12, 16, 19, 17, 19, 14,
   28, 19, 19, 19, 17, 13, 10, 20 and 2 pairs (244).

   **Step 2, the essay trial** (2026-11-04): the six pages marked with `--pages` and read
   whole in the image (40 strips). The essays are printed in two columns as the cantos,
   and the alignment held. 71 pairs; 18 lines flagged; 7 lines wrong: 5 flagged (0114
   `Ordine Agostiniano` and `co'` measured italic, `ed *Amore* dello` and `*Sapienza,
   Amor* primo` measured roman; 0750 `*tina del secolo XV a' suoi figliuoli*`), 2 not
   (0382 `DROUILHET DE SIGALAS`, small capitals measured italic; 0902 `e *Della vera …*`,
   a one-letter word taken in). Decided with the user: (a) the flagged lines only, as in
   the parts, with two new flags for the two misses (`caps`, `edge`) and the search of
   step 1; (ii) a source abridged is one pair, its inner periods inside (`*IV Sent.,
   dist. XLV, cap. III. De officiis sepulturae*`, `*Serm. CLIX, alias XVII*`, `*Lib. De
   monogam*. cap. X`), the period after the last letter outside as before; runs joined
   across a period are flagged (`join`) and decided in the image, since two lemmas or
   quotations side by side (1279 `*Veloci …*. *Quasi*`) stay two pairs. In
   `la_italicmark.py`: `--join` (the essays and front matter only), and the flags `caps`
   (a word in capitals marked italic, not a Roman numeral), `edge` (a one-letter word
   that begins or ends a run, or roman beside one, an elided letter left out) and
   `join`. Over the trial pages all 7 wrong lines are flagged (23 lines). The canto
   pages' marks are unchanged (the flags only gain `caps` and `edge`).

   **Step 3, part 1, the Inferno essays** (0092–0476, 39 pages, 2026-11-04): the slant run
   page by page, `--pages 92-476 --join`; 128 lines flagged (91 `box`). 12 pages are
   stored a paragraph a line (0092 0102 0150 0161 0171 0183 0196 0232 0243 0267 0347
   0440): `la_italic.py` aligns them in the page's stream (few words unmeasured), but every
   line is `box` and a flag cannot say which run; there 33 runs were looked at in the image
   and then the pages read whole (both halves of each page): 22 places corrected, 3 of them
   italics missed (0161 `*superbo strupo*`, `*Apoc*.`, `*strupo*`); 0150 and 0161, in a
   heavier type, had roman words measured italic (`di presente`, `creazione`, `incanto`,
   `antico`). On the other 27 pages the 36 flagged lines other than `box` decided in the
   image: 21 corrected (with the trial's on 0114 and 0382). Most often: `sè`, `co'`, `se`
   measured italic (an accent or apostrophe slants); an elided article taken in where the
   print has it roman (`l'*Itinerarium mentis in*`, `l'*ignem aeternum*`, `l'*anima
   trade*`); a title split by a roman word (`*Il Romano Pontificato nella storia
   d'Italia*`). The search (`*sè*`, `*co*`, a run begun with an elided word, a short roman
   gap): 3 more lines looked at, right (`*L'arte …*`, `*L'autre vie*`, `*d'Italia*`). 40
   lines corrected in all; 98 pairs. Checks as in the parts, all passed. Looked over again
   after part 2 for its kinds of error: the heading lines in the image (38; 0102's read with its page; all roman), and
   the search for a run begun with a roman function word, a numeral or capitals (6 lines
   looked at in the image): no change.

   **Step 3, part 2, the Purgatorio essays** (0497–0869, 38 pages, 2026-11-04): the slant
   run page by page, `--pages 497-869 --join`; 88 lines flagged (28 `box`). 3 pages stored
   a paragraph a line (0553 0574 0655), read whole in the image: 4 lines corrected (0574
   the heading `L'*AVE MARIA* DELLA SERA E IL *DE PROFUNDIS*`, marked as printed, unmarked
   by the script; `*sè*`; `« *Te lucis*...`; 0655 `Pur *Agnus Dei*`), 0553 none. On the
   other 35 pages the 66 flagged lines decided in the image (6 `box` a crop of the wrong
   line, nothing to mark): 30 corrected. Most often `sè` (17), `se`, `Nè`, `n'esce` measured
   italic; a roman word at a run's start taken in (`*Che gli*`, `*Del suo*`, `*Con
   sitio*`, `*Tanta riconoscenza*`, the numeral in `(III *Reg*.`, the
   small capitals in `(LUBIN, *Commedia*`) or an italic one left out (`*ab aeterno*`, `*si
   fractus …*`, the trial's `*tina del secolo XV a' suoi figliuoli*`); `esset` in a roman
   Latin quotation. The search found no line not flagged. 34 lines corrected; 91 pairs.
   The preamble 0479–0486, expected to have none, was run through the slant too (one
   column, every word measured roman but `ad Rom`): one italic, 0479 `(*ad Rom*. I)`,
   written in (1 pair); 0477 and 0871 none. Checks as in the parts (`la_check.py` also
   over 0477–0496), all passed.

   **Step 3, part 3, the Paradiso essays** (0887–1270, 37 pages, 2026-11-04): the slant
   run page by page, `--pages 887-1270 --join`; 63 lines flagged (5 `box`); no page stored
   a paragraph a line. The flagged lines decided in the image (the `box` ones a crop of
   another line, nothing to mark there): 23 corrected. Most often `sè` (12) and `Nè` (3)
   measured italic; a roman word at a run's start taken in (`*Sonava Osanna*`, `*Dio
   filium dilectionis Dei*`, `*Chi sè*`, `*Cristo ce*`, the elided article in
   `*l'obscuratum*` and `*l'operò, o l'opererà*`); `sozze` measured italic; a run cut
   wrong (`*in* divinis`, `*guardare e conside-*`; now `*in divinis*`, `*guardare* e
   *conside-*`). The search (as in part 2, with a run begun
   with a roman word, a numeral or capitals) found 2 more: 0984 `Vid'*egli*` (the poet's
   `io` changed and marked) and 1083 `(D'Acquisto, *Trattati di*` (small capitals taken
   in). The headings (34, and the second lines of 1008, 1023, 1047) all roman. 25
   lines corrected; 91 pairs. In passing, 0934 had three words alone on a line (`stesso`,
   `casi`, `stesso`), the line-start words restored in batch 8: each joined to its printed
   line (the words unchanged). Checks as in the parts, all passed.

   **Step 4, the front matter** (0007–0077 and the index 1289–1290, 2026-11-04): the slant
   run page by page, `--pages 7-77,1289-1290 --join`; 11 pages have no measurable word
   (0007 0008 0009 0011 0012 0043 0044 0055 0056 0058 0077: title pages in roman capitals
   and blanks, seen in the image). 148 lines flagged (24 `box`). The notizie 0022, 0027,
   0029, 0031 and 0033–0038 read whole in the image; on the rest the flagged lines decided
   (the `box` ones roman). The dedication 0013–0014 is printed wholly in italic (the
   script measures a page against its own slant, so it marked nothing there): its type,
   not an emphasis, so left unmarked (with the user, 2026-11-04). Most often a roman word taken in or an italic one left out at a run's
   edge (`*Lo Spoglio*`, `*l'Explicit …*`, small capitals `*OTTONELLI, …*`, `*HALAM, …*`,
   an archive reference `*Massarelli, De Pontif.*`, `*Ughelli, Ital. Sac.*`), an italic
   `etc.` or `[qui erant]` inside a quotation left roman, `sè` measured italic (3), the
   readings compared on 0036 (`« Che *spande* …`, `« Vedrai *gli antichi* …`), the folio
   numbers of 0033's index (`c. *127, primo latere*.`). A stop at a line end inside a run
   continued on the next line moved inside (`*… Monarchie,*` / `*de lo …*`; the rule under
   **Mark** above, which `la_italicmark.py` cannot apply: 14 lines; not 0033's entries), so that
   `convert_la.py` joins the run. A mark cannot close after a digit (`unmark()`), so an
   italic number at a run's end stays outside (0022 `*Flor*. 10.`, 0018 `… Genova* 1853`,
   0033 `*usque ad* 6.`, 0037 `*… totum opus* 1480.`). 88 lines differ from the script;
   333 pairs on 40 pages. Text errors seen in passing, corrected in the image (10 lines):
   0022 `dipi-` / `scritti` → `dipi` / `iscritti`; 0029 `hec` → `haec`; 0035 `traslatio`
   → `translatio` (0031 has `traslatio`, as printed), `LVIGI` → `LUIGI`; 0036 `danno` →
   `dànno`, `fiume_` → `fiume`, `Essi: « L'altra` → `Essi: L'altra` (no `«` printed);
   0037 `publicarit` → `publicavit` (the glyph of `predicavit` beside it); 0038
   `Preambula` → `Preàmbula`. `la_check.py` and `la_seqcheck.py` over 0007–0077 and
   1289–1290 and `la_seqcheck.py` over 79–1270 unchanged; `convert_la.py` only the
   expected warnings.

   **The split runs swept** (0079–1287, 2026-11-04), as the line-end rule of step 4
   asks for the cantos, the essays and the appendix too. Listed: 43 lines that end in
   `*` and a stop, with the next line beginning with `*`, and 9 lines with `*; *`,
   `*? *` or `*! *` inside them; each looked at in the image. Moved inside, 26 lines:
   a translation or title running on (`*… tristis rivus,*` / `*quando descendit …*`),
   an incipit with its gloss (`quod incipit: *Iam, vel nunc,*` / `*itur per …*`, 6),
   an Italian lemma running on (`*Ed ella a me:*` / `*Da tema e da vergogna*:`), 0397 `*Cum verbis,*` / `*[parole] sciolte*` (the bracket printed
   italic), 1130 `(*Trat.*` / `*del Purg*.`. Left, 17 lines: two lemmas (Latin and
   Italian, or a lemma and the next one glossed; 0247, see below), and 5 lines that are a lemma
   paragraph of their own (0110:67, 0155:76, 0180:80, 0990:65, 1104:80: the next line
   begins the next lemma's paragraph in `texts/la`, so the stop ends a lemma). Same
   line, joined into one pair, 6 lines: `*a*; *b*` in a translation (0146, 0167, 0189,
   0330) and `*De*! *…*` (0601 ×2, 0748; 0601's second `si` printed italic). Left: two
   languages (0100, 0425) and two words (0354 `*Deus*; *tropos*`). The 453 same-line
   `*a*. *b*` and `*a*: *b*` not looked at: lemma boundaries by the rule under **Mark**.
   Seen in passing, corrected in the image: 0247 `*Paduani*` → `Paduani` (roman),
   0990 `comenzo` → `comenzò`. 33 pages; `la_check.py` over 79–1287 and
   `la_seqcheck.py` over 79–1270 unchanged; `convert_la.py` only the expected warnings.

   **The same-line pairs read** (0079–1287, 2026-11-05): the 453 `*a*. *b*` and
   `*a*: *b*` the sweep left, decided by sense, not in the image (whether the stop is
   italic can hardly be seen, and the convention does not follow the print). 332, where a
   script found each run nearer the canto's verse in one language than in the other (an
   Italian lemma and its Latin one), were skimmed as a list and kept as two pairs; the other
   121 were read with their lines and the verse. Joined, 56 on 52 lines: one quotation
   running on, the verse's own stop inside, mostly a speech and its introduction (0299
   `*Tunc Virgilius dixit: Dicas sibi cito: Non sum ille,*`, 0297 `*Et ego: Tantum michi
   pulchrum est*`, as 0862 `*Ed ella a me:*` / `*Da tema e da vergogna*:` above) or
   consecutive verse lines (0123 `*… in apparentia: loquebantur tarde …*`, 0143 `*… sicut
   canes. De uno latere*`). Kept, 65: the two languages side by side where the script did
   not tell them apart (0312 `*Ed io*: *Maiestro*. *Et ego*: …`, 0159 `*Or discendiamo
   omai*: *or descendamus admodum*`, 0121 `*dixit michi*: *Honorata nominanza*`), a word of the quotation taken
   again as a lemma (0138 `*… suspicione*. *Soli*:`, 0199 `*stia*. *Stia*`), a lemma from
   earlier in the verse (0180 `*De celo missus*`, 0318 `*Antianus*`). 0990:65 and 1104:80 keep their
   Italian line-end stop outside, as the sweep left them (lemma paragraphs of their own);
   their Latin pairs on the same line are joined. Seen in passing, roman in the image, the
   marks removed: 0246 `istud`, 0782 `idest`, 1055 `hec`. 4,232 pairs remain; `la_check.py` over
   79–1287 and `la_seqcheck.py` over 79–1270 unchanged; `convert_la.py` only the expected
   warnings.
5. **Scripts** that read `ocr/la` (`la_check.py`, `la_seqcheck.py`, `la_lostcheck.py`,
   `la_lines.py`, `la_survey.py`, `la_lemmacheck.py` and so `la_versecheck.py`) remove the
   marks before reading (`unmark()`: every `*` not after a digit); `convert_la.py` keeps
   them, joins a pair broken at a line end (`*dedit ven-*` / `*tum*:` → `*dedit ventum*:`,
   `*a*` / `*b*` → `*a b*`) and reports a line whose pairs are not closed. Done
   (2026-11-03).
6. **Commit** per part, when the user says so: `ocr/la` (the part's pages), `texts/la`
   (its canto files), this PLAN, as three commits. Before part 1's, the scripts (step 5:
   `la_italic.py`, `la_italicmark.py`, `unmark()` in the readers, `convert_la.py`) as one
   commit. After part 9:
   texts/PLAN.md and texts/la/README.md (italics now transcribed), the convention under
   "Conventions settled during the check", "Known limits". The widened scope (step 4) was
   committed once, after all of it (the user, 2026-11-04): the scripts, `ocr/la`,
   `texts/la`, and the docs (this record moved to DONE.md, PLAN.md, texts/PLAN.md,
   texts/la/README.md), as four commits.

## Check 2: rare forms near common ones (2026-11-05)

The fourth of the checks planned in PLAN.md ("Checks"), for misreadings that both OCRs
share and that turn a word into a form found nowhere else. `ocr/la_lexcheck.py` listed
22,567 candidates (a form found once or twice, near a common one) in three groups by
Tesseract's word. Groups 1 (278) and 2 (2,277) were decided in the image, group 2 with a
blind reading of the crops by la-el-agy; group 3 (19,817 after them) was read for its sense
by la-el-agy, and only the 185 words it flagged were decided in the image. In all 149
misread (59 in group 1, 70 in group 2, 20 in group 3) and 94 misprints (6, 5, 83), each a
row of `ocr/la/lexcheck.tsv`; the misprints are in PLAN.md ("Suspected misprints"). The
plan as it was written, with the results of each group and batch, follows.

### Plan and steps (`ocr/la_lexcheck.py`, `ocr/la_lexcrop.py`)

A misreading that both OCRs share usually turns a word into a form that occurs nowhere
else: 0197 `circuleto` (once) beside `circulecto` (5 times, and `circulectos` 10). A form found once or twice in
the whole book, one or two letters from a form found often, is a candidate.

1. **Script**: the words of all pages (`0001`–`1296`, blank pages aside), with the
   line-end hyphens joined as `convert_la.py` joins them, counted case-insensitively. For
   each form of count 1–2, the forms at edit distance 1 (2 for forms of 8 letters or
   more) with a count of at least 5 and at least 5 times its own; listed with page, line,
   the counts, the neighbours, the context, and Tesseract's word at that place (from
   `ocr/la/tesseract/`; it does not normalize spellings, so its reading is a third vote).
   Ranked in three groups by Tesseract's word (accents aside): 1, a neighbour, or a form
   that differs from its neighbour only in accents; 2, another word; 3, the form itself.
   A letter pair that the OCRs confuse (`c`/`e`, `n`/`u`, `r`/`t`, `rn`/`m`, `li`/`h`,
   `f`/`s`, `cl`/`d`) is shown; `-g G` lists the groups up to G. Left out: the forms in "Suspected misprints", `lemmacheck.tsv`,
   `versecheck.tsv` and `lexcheck.tsv`. Options: `FIRST LAST`, `-t TESS`, `-o OUT`, `--min N` (the neighbour's
   count), `-d DIR` (read the pages from DIR instead of `ocr/la`).
2. **Trial**: a recall test on the first transcription (the pages of commit `89ac4a3`,
   exported to a scratch directory and read with `-d DIR`): of the words the proofreading
   later corrected there (`git diff 89ac4a3 -- ocr/la`, word by word), count how many the
   script lists, `circuleto` (0197) among them, and look at those it misses to tune the
   limits. Then run it on `ocr/la` and count the candidates; with the Latin of the manuscript (`michi`, `nichil`, `quedam`, `pexime`) many
   rare forms are printed so. If the list is too long to decide by eye (more than about
   2,000), first decide with the user how to narrow it (a higher `--min`, only the ranked
   groups, or paid image decisions as in item 7).
3. **Decide** in the image, in rank order; record in `lexcheck.tsv`. A form decided
   printed for one page is not taken as printed for another: each place is looked at.
4. **Checks** and **commit** as in check 1 ("Check 1", steps 5–6), batch by batch
   if long.

### Results

- Trial on `89ac4a3`: 78% of group 1 were misreadings, 24% of group 2, 0.8% of group 3;
  groups 1 and 2 held about 95% of them. On `ocr/la`: 22,567 candidates, of which group 1
  278, group 2 2,277, group 3 20,012.
- Group 1: done; 278 rows, 59 misread, 6 misprints.
- Group 2, decided in page batches (each candidate's word cropped from the image, the
  unclear ones zoomed and compared with letters of the same page): batch 1 (0001–0160)
  done, 311 rows, 5 misread, 1 misprint (0153 `rim`, found when la-el-agy's readings of
  the same crops were compared). From batch 2 the crops are read by la-el-agy, blind: it
  gets each crop and the line with the word replaced by `____` (not the `ocr/la` form) and
  writes the word as printed (`ocr/la_lexcrop.py`); every reading that differs from
  `ocr/la` is decided in the image, the rest taken as printed. Batch 2 (0161–0320): 432
  rows, 23 readings differed, 2 misread. Batch 3 (0321–0480): 278 rows, 27 readings
  differed, 13 misread (one of them two lines of a Latin footnote list on 0433, not
  printed, removed). Batch 4 (0481–0640): 343 rows, 40 readings differed, 21 misread
  (one a line on 0547, not printed, removed), 2 misprints. Batch 5 (0641–0800): 219 rows,
  21 readings differed, 9 misread (8 words; three of them damaged letters restored,
  `permictit`, `preliatus`, `Sodomis`). Batch 6 (0801–0960): 228 rows, 19 readings
  differed, 9 misread (7 words), 1 misprint. Batch 7 (0961–1120): 220 rows, 15 readings
  differed, 5 misread. Batch 8 (1121–1296): 246 rows, 18 readings differed, 6 misread
  (5 words; two of them damaged letters restored, `capitulo`, `gratis`), 1 misprint.
  Group 2 is done.
- Group 3 (19,817 after the decisions above), in the same page batches: read by la-el-agy
  for sense, not in the image (`ocr/la_lexcrop.py --lines`: each word in its line and the
  lines around it); the words it flags are decided in the image, the rest are not
  recorded. Batch 1 (0001–0160): 2,592 words, 29 flagged: 7 misprints, 22
  printed (most in the papal documents, the words of their transcription).
  Batch 2 (0161–0320): 2,614 words, 23 flagged: 5 misprints, 18 printed.
  Batch 3 (0321–0480): 2,664 words, 21 flagged: 5 misread (`Penetrò`, `illuc`, `non`,
  and two damaged letters restored, `infin`, `eam`; the `infino` of 0586, seen with
  `infin`, also corrected), 7 misprints, 9 printed.
  Batch 4 (0481–0640): 2,287 words, 24 flagged (one the `infino` above): 6 misread
  (`emictunt`, `sic[ut]`, `hic`, `Sancta` twice, and `Non`, damaged, its last letter unclear,
  corrected by the sense), 14 misprints, 3 printed (among them `tainquam`, a dot over the
  first stroke of an `m` or `in`).
  Batch 5 (0641–0800): 2,342 words, 19 flagged: 1 misread (`permictebat`), 6 misprints,
  12 printed.
  Batch 6 (0801–0960): 2,431 words, 20 flagged: 2 misread (`fore`, an `f` with its bar
  lost, and `saecta`, damaged, its third letter unclear, corrected by the sense),
  12 misprints, 6 printed.
  Batch 7 (0961–1120): 2,380 words, 28 flagged: 3 misread (`huiusmodi`, `Hic`, and
  `idest`, its `t` damaged, restored), 19 misprints, 6 printed.
  Batch 8 (1121–1296): 2,507 words, 21 flagged: 3 misread (`hec` twice, and the opening
  bracket of `auctor[em]`), 13 misprints, 5 printed.
  No group 2 candidate is left out by script (a Tesseract word that joins an elided word
  to the form, `Nellumiliare`, is still looked at: the same
  shape covers real differences, `inanz'a` against `inanza`).

Not found by this check: misreadings into a common word (0085 `terret` is a real word,
printed on 0489), rare words with no common neighbour, and a common spelling written for
the printed rare one (`mihi` for `michi`: the error is the common form). Check 1 covers
part of the first kind inside lemmas.

## The checks: their order and what later work takes from them (2026-11-05)

Moved from PLAN.md ("Checks") when the read-through was planned.

Order: check 1 (lemmas) first, as its candidates were fewer and surer; then the verse
check, with the same procedure while it was fresh; then the italics, which started
from the lemmas of check 1; then check 2, whose ranking learns from the errors checks 1
and the verse check found, and whose counts are surer once the verse is right. All are done.

Check 1 (lemmas against the verse, 0079–1270 in 10 batches, 2026-11-01), the verse
check (every line of both verse columns read again from the image, 0079–1270 in 11
batches, 2026-11-01 – 2026-11-03), the italics (the whole volume, 2026-11-01 –
2026-11-04) and check 2 (rare forms near common ones, `ocr/la_lexcheck.py`, 2026-11-05)
are recorded above ("Check 1", "Verse check", "Italics", "Check 2").
What later work takes from them:

- `lemmacheck.tsv`, `versecheck.tsv` and `lexcheck.tsv`: their forms are decided;
  `la_lexcheck.py` leaves them out, so a rerun lists only new candidates.
- Check 1's procedure per batch (crops in a shuffled order, read by la-el-agy from the images
  alone, compared line by line, every difference decided in the image) served check 2,
  group 2, with crops of the words. Match every reading to its line before comparing
  (batch 9: 60 readings were not of their images).
- Check 1's errors were mostly a common spelling written for the printed one (`mihi` for
  `michi`, `societate` for `sotietate`, accents not printed); check 2, which looks for rare
  forms, does not find this kind ("Known limits").
- The verse check's procedure per batch (page images by `ocr/la_versecheck.py
  --page-crops`, read by la-el-agy and la-el-agy2 from the images alone, aligned by
  `--page-readings`, every difference decided in the image) can serve as well. Its
  readers' errors: a common spelling written for the printed one, a misprint corrected,
  accents left out or added, specks read as marks; in batch 11 the tercet numbers of
  three cantos left out and reported as not printed. A report is not taken as true.

## Work items 1–10 (all done)

In this order (decided with the user, 2026-10-15):

1. **Verse transcription** (paid, `gpt-6-luna`): a new script sends each crop of
   the missing column and asks for the verse of the column as printed, line by line
   (tercet numbers, gloss marks `(¹)`, runover words `[…`), from the image only: no
   dante-corpus text in the prompt. The crops of the Italian can hold the edge of the Latin
   column (tercet numbers, first letters, e.g. 0709, 1090): the prompt says to leave it out.
   - **Trial first**: crop the Italian column of checked pages (0079–0232, both columns
     present), transcribe, and measure against `ocr/la`; then all pages. The crops of
     the Italian of 0079–0232 (121 pages) were transcribed with `ocr/la_verseread.py`
     (paid, by the user) and measured with its `--check`.
   - **Trial done** (Record of the preparation). Decided (the user, 2026-10-15): the verse of the 338 pages
     (337 Italian, 0836 Latin) is transcribed by **la-el-agy**, not by Luna, in batches of
     20–30 pages, with the task of the trial ([DELEGATION.md](DELEGATION.md): the crops
     only; no text of the pages, of GLM-OCR or of the poem; superscript tercet numbers,
     `(¹)`, runover lines `[`; letters it is unsure of in the report). 0836 needs the Latin
     wording of the rules. The Luna answers and `la_verseread.py` stay as they are (not used
     further).
   - **Batches**: 25 Italian pages each, in page order; each task is the
     previous one with the new pages and the words of the last batch that were not as
     printed ([DELEGATION.md](DELEGATION.md)).
     - **Done**: batches 1–14, all 337 Italian pages (`0237`–`1265`, Record of the preparation).
     - **Done too**: Latin `0836` (row 338), and the gaps at apostrophes of batches 1–10
       (Record of the preparation). The verse of all 338 pages is in.
     - **Commits**: batches 4–10 were committed together after batch 10 (the user,
       2026-10-17); batches 11–14 and 0836 in `4c6f2f5`.
     - In any later verse check, look at every apostrophe written with a space; the print
       sets the gaps both ways.
2. **Verse check**, after each batch of item 1 (la-el-claude, by script first): compare
   each transcription with GLM-OCR, which reads the Italian verse (as a check only), and
   its tercet numbers with those of the Latin column of the page; look in the image only at
   the disagreements and at the letters la-el-agy reported unsure (a crop per place).
   dante-corpus only points at places to look at: this edition's forms differ from it, and
   a difference is not a reason to change. 0836 (Latin, no GLM-OCR reading of the verse):
   checked in the image. Then insert the blocks (Italian block, gloss line, Latin block;
   see the conventions) and run `la_check.py` (tercets) until it reports only known
   exceptions.
   - **How** (batches 1–2): a scratch script aligned each line with GLM-OCR's lines and
     listed the word differences, and compared the tercet numbers and line count with the
     Latin block; or with Tesseract's words in the crop, for the pages whose GLM-OCR has no
     Italian verse (about a quarter). Most differences are OCR noise (gloss marks, `'l`,
     accents GLM-OCR drops: `sì`/`si`, `Così`/`Cosi`, taken as la-el-agy reads them). The
     letter differences, about 20 a batch, were looked at in stacked crops of the printed
     lines. Fix la-el-agy's file, then `uv run ocr/la_verseinsert.py PAGES -d DIR -n`: it
     lists every Latin number it would add or change, and pages whose Latin line count
     differs (fix the Latin block first, in the image); look at the changed numbers in the
     image, then run it without `-n`. `la_check.py` over the range: the reports on the
     inserted pages (a stray blank line in a block, a gloss line taken as verse); those on
     other pages are for the batch procedure.
   - **Gloss lines**: done (2026-10-18, Record of the preparation): the 223 pages
     have the gloss lines transcribed from the image, in place of the old ones.
3. **Markup of the 475 pages** (paid), as procedure step 2,
   with the default rounds (the extra round of item 5 is for all pages together). Done:
   137 (the 48 with a moved Latin block and the 90 ready, 0598 in both); the other 338,
   whose verse and gloss lines are now in: their old answers no longer fit, so they are
   called afresh into a work directory.
   0831's fixing call was refused by OpenAI ("flagged as potentially violating our usage
   policy"; a false flag on the commentary); the user marked it with `gemini-3.8-flash`
   instead. Its marks showed the commentary broken (a paragraph lost, the rest out of
   order, the page head reversed), so 0831 was retyped from the scan by la-el-claude
   (2026-10-18; damaged letters restored: `appropinquant`, `Foroiulianas`, `domina`) and
   leaves the markup method: done; its gemini answers are kept in `tmp/la-markup/bak2/`
   (the older ones in `bak/`), none in `tmp/la-markup/`. A page refused this
   way stops the run; the user marks it with another model. When the run is done, the
   answers move into `tmp/la-markup/`, and the
   further steps (item 5 on) work on `tmp/la-markup/`. Done (Record of the preparation).
   All 475 are now marked.
4. **Pages that stop `la_markprep.py`**: done (2026-10-18); 0941 is called in item 5.
   - In `ocr/la`, checked in the image: 0727 `[dicit]`, 0063 `[et]`, 0822 `[firmaret]`
     (printed brackets); 0399's `}}` line is the signature `44`; 0458's commentary and
     0035's footnote, whose two columns were run together line by line with `|`, put
     column after column (0458 retyped from the scan); 1245's figure, a `|` table with
     headings not printed, written as `[figure]` and its labels (conventions), and the
     blank line at its column change removed.
   - GLM-OCR's side (0021 `|Firenze`, 0344 and 0467 `$^{(1)}$`): `la_markup.py` cleans the
     GLM-OCR text and the `glm` of every entry, saved answers included (`clean_glm`).
   - The marked pages of these 9 were rewritten from their saved answers (`-r 0`); no
     marked page in `tmp/la-markup/` holds an unparsed `{{`/`}}` now, and `la_markprep.py`
     runs through them. 1245 has 8 differences missed (its figure), left to item 5.
   - 0941: its only answer was cut off (invalid JSON); moved to `tmp/la-markup/bak2/`, so
     item 5's run calls it afresh. The cause was in the sources (2026-10-18): GLM-OCR
     ended in a loop (`fluis.` then `usus…` for 640 characters, then `gend` from the
     scan's watermark), cut in `glm-ocr/0941.txt`; and `ocr/la` had lost and mixed lines
     in both commentary columns (`Epirri, et intravit …` and the `Fabii …` lines lost,
     `trino-`/`mius` split apart), so 0941 was retyped from the scan by la-el-claude
     (gloss line set off by blank lines; dots inside sentences written as commas). Against
     GLM-OCR only its misreadings are left (`Ipsse`, `Deciiis`, `tune`, …).
5. **One more markup round** (paid, before the model decisions): rerun `la_markup.py`
   with `-r 1` on all pages, so that the pages with missed differences get one more fixing
   call (the pages that pass make no call; `-r` counts the calls of this run only, the saved
   answers aside, so `-r 3` would allow three more). Check what is still missed. The pages:
   1233, every page with GLM-OCR but 0831, which is out of the method (0941 is called
   afresh), `uv run ocr/la_markup.py -r 1 -m gpt-6-luna -o tmp/la-markup PAGES`, run in
   three in parallel (411 pages each). Then: `-r 0` on a copy for the counts (Record of the preparation), the
   long blocks (69 pages, item 3) in the image, 1245's figure. Done (2026-10-18, Record of the preparation): the
   long blocks led to item 6.
6. **Pages with lost text** (decided with the user, 2026-10-18): the 164 pages of the
   word check (Record of the preparation) are retyped from the scan by **la-el-agy**, page by page, from the
   image alone (no text of the page, of GLM-OCR or of the poem), with the conventions below;
   first a trial batch of 6 ([DELEGATION.md](DELEGATION.md)), then batches of 10 in page
   order. Each batch is checked by la-el-claude by script against GLM-OCR and the old
   `ocr/la` (every word that differs from both, every block one of them lacks, the verse
   with `la_check.py`), in the image where they disagree; then the page replaces
   `ocr/la/PAGE.txt`, its markup answers move to `tmp/la-markup/bak3/`, and it is marked
   afresh (paid, by the user; default rounds, then `-r 1` as in item 5). The list came from
   a word check: runs of 15 words or more of GLM-OCR found nowhere in `ocr/la` (3-word
   shingles, digits left out); no page of batches 1–2 is on it. Check (a scratch script):
   the blocks one side lacks; each word differing from GLM-OCR, with the old file's reading.
   The front matter on the list (0046, 0048–0050, papal documents, 0048 with paragraphs
   repeated) is left for a batch of its own, with its own layout rules.
   - **Trial** (0296 0512 0709 0907 0940 1240, 2026-10-19): complete (word counts within
     a few of GLM-OCR's), every difference with GLM-OCR checked in the image: one slip
     (1240 `Christe.`, fixed); `la_check.py` tercets clean. In `ocr/la`; their answers in
     `bak3/`; markup to call (paid).
   - **Batch 2**: 0237 0238 0250 0261 0264 0266 0271 0272
     0275 0278: complete; not as printed: 0264 `Aquaquicta` (×3, printed `Aquaquieta`),
     0272 the lemma `Torciendo:` written as the verse's `Torcendo`, 0278 `e 'l` (fixed).
     Right where GLM-OCR differs: 0250 `Fiexul-` (commentary; the verse `Fexulis`), 0261
     `Bellinzo-`/`n[us]`, 0264 `discoscexa` (Latin verse). In `ocr/la`, answers in `bak3/`.
   - **Batch 3**: 0303 0307 0309 0317 0319 0329 0330 0339
     0356 0367: complete; not as printed: 0330 `porosumi`, 0367 `trafictò`, 0319
     `schegiam` (fixed). In `ocr/la`, answers in `bak3/`.
   - **Batch 4**: 0373 0375 0378 0380 0390 0401 0405 0407
     0414 0420: complete; not as printed: 0420 `liuto`, `Thebanarum` (printed `linto`,
     `Thebenarum`), 0390 `Babilone`, 0373 `Ch'è`, 0405 `su' 'l` (printed `su''l`), 0375
     `mostra 'l` (fixed). In `ocr/la`, answers in `bak3/`. `la_check.py` finds fewer
     rules than printed on many pages (0380: 2 of 4); the blank lines were checked in
     the image where they differ.
   - **Markup of batches 1–4** (36 pages; paid,
     by the user, `-r 3`, 2026-10-19): re-checked with `-r 0`: 40 differences missed in
     18 pages (15 spacing only), 3 entries not placed; the 4 long ones are GLM-OCR's
     block order (0709, 1240) and gloss line placed elsewhere (0375), not lost text.
   - **Batch 5**: 0423 0424 0435 0438 0445 0448 0460 0463
     0468 0505: complete; paragraphs indented with spaces and some gloss dashes written
     `--` (both normalized), 0505's head in print order and 0463's letter-spaced (put in
     the usual form); not as printed: 0423 `commutandum` (printed `commutundum`) and
     punctuation at phrase ends (0423, 0435, 0460, 0505, 9 places), apostrophe gaps
     (0445, 0460, 0468, 0505), 0468 `,Si`, 0445 caron for the breve of `Pĭetrapana`
     (fixed). Kept as printed: 0438 `fainam`, 0460 `Cloco`, 0423 `[sn`. In `ocr/la`,
     answers in `bak3/`; `la_check.py`'s extra rule on 0424, 0435, 0448, 0460 is the
     page-end rule. Markup (paid, by the user, `-r 3`, `done5.txt`) re-checked with `-r 0`:
     9 differences missed in 6 pages, 2 entries not placed (0445); the long ones are
     GLM-OCR's gloss lines placed elsewhere (0423, 0445, 0468) and its Latin verse block
     (0460). 0438 ends `et sic` at the scan's cut edge (GLM-OCR `sicus.`), kept.
   - **Batch 6**: 0511 0514 0524 0535 0536 0548 0551 0589
     0594 0596: complete, form right; 20 places not as printed (fixed), most of them
     punctuation (periods as commas, commas left out or added, 0596 `separarsene:`),
     words made like the other column (0524 Italian `Cachume` written `Cacume`, 0514
     `Quant'um`, 0548 `discordiis` with `ï`), apostrophe gaps (0551, 0594, 0596, 0536),
     and the rule at the foot of the left column not written (0524, 0536). Kept as
     printed: 0511 `demacrat`, `deior`, `miglor`; 0548 `mariptimas`; 0596 `uon`, `cio`,
     `sublimita` (an essay page without page number). In `ocr/la`, answers in `bak3/`
     (`done6.txt`); `la_check.py`'s extra rule on 0589 is the page-end rule. Markup
     (paid, by the user, `-r 3`) re-checked with `-r 0`: 15 differences missed in 6
     pages, 1 entry not placed (0524); the long ones are GLM-OCR's Latin verse block
     (0524, 0535), the rest GLM-OCR's spacing and splits; 0596 `ciò` checked in the image.
   - **Batch 7**: 0599 0601 0605 0615 0623 0641 0647 0649
     0650 0661: complete, form right; 11 places not as printed (fixed): periods written as
     commas (0601 `oportet.`, 0605 `siccentur.`, 0615 `diei.`, 0641 `invidi.`,
     `deglutire.`, `rebus.`), 0623 `Com poco` (written `Con`), 0641 `ideo dicit`
     (capitalized), 0647 `girat' era` (gap) and `radiis` (written with `ï`), 0599 a gloss
     dash not printed between (³) and (⁴). Kept as printed: 0650 `super eis` in the verse
     and `eas` in the commentary, `duo`/`due`. In `ocr/la`, answers in `bak3/`
     (`done7.txt`); `la_check.py`'s extra rule on 0649 is the page-end rule. Markup
     (paid, by the user, `-r 3`) re-checked with `-r 0`: 6 differences missed in 5 pages,
     none not placed; the long one is GLM-OCR's Latin verse block (0650), 0641 its gloss
     line placed elsewhere, the rest GLM-OCR's splits and misreadings at line ends.
   - **Batch 8**: 0666 0679 0699 0701 0708 0712 0714 0715
     0721 0723: complete, form right; 9 places not as printed (fixed): 0699 verse `havete`
     (written `avete`), punctuation (0701 `avaritiam:`, 0723 `terra:`, 0721 `elegerit.`),
     apostrophe gaps (0701 `puo'saper`, 0721 `cho'buon`, 0679 `de'volatili, de'quadrupedi`
     like the page's other `de'`, without a gap; 0715 `Ond' intender` with one). Kept as
     printed: 0666 `Couradus` (commentary), 0708 `Quèste`, `pubblicaret`, 0721 `figla`,
     `sorpiendo`; 0679 is an essay page (`L'AMORE VITA DELL'UNIVERSO`, signature 79). In
     `ocr/la`, answers in `bak3/` (`done8.txt`); `la_check.py`'s extra rule on 0666, 0699,
     0701, 0721, 0723 is the page-end rule; it misses one rule on 0708, 0714, 0715. Markup
     (paid, by the user, `-r 3`) re-checked with `-r 0`: 17 differences missed in 5 pages,
     1 entry not placed (0666); the long ones are GLM-OCR's verse and gloss blocks placed
     elsewhere (0666, 0699, 0708, 0721), the rest its joins of words broken at line ends
     (0679 `del-`/`l'accordo`, `que-`/`st'ora`) and misreadings.
   - **Batch 9**: 0726 0747 0755 0757 0765 0767 0768 0792
     0795 0828: complete; 0755's verse written without its tercet numbers (15–20, both
     columns, added). 18 other places not as printed (fixed): apostrophe gaps written where
     none is printed (0747 `de'martiri`, `Co'suoi`, `co'sospiri`, 0765 `all'acto`,
     `l'andar`, 0768 `quest'è`, 0792 `Che'l`, `che'n`) and left out where printed (0795
     `a' peregrin`, 0828 `m' apparve`); punctuation (periods written as commas: 0765
     `ego.`, `exempla.`, 0768 `marinus.`, 0828 `dicatur.`, `nube.`; colons as semicolons:
     0765 `recolligit:`, 0767 `humani:`, `coctura:`; 0726 verse `fiamma,` without its
     comma). Kept as printed: 0726 `calide, et` (comma set low), 0747 `Bardaggia`, 0755
     `di's'io`, `intellecto`, 0765 `mirar`, 0757 `Or va' ,`, `(³,` on 0726 and 0828. In
     `ocr/la`, answers in `bak3/` (`done9.txt`); `la_check.py` counts agree after 0755's
     numbers (it misses one rule on 0726 and 0828 and sees the page-end rule). Markup
     (paid, by the user, `-r 3`) re-checked with `-r 0`: 11 differences missed in 8 pages,
     4 entries not placed (0757, 0765), all GLM-OCR's: its Latin verse and gloss blocks
     placed elsewhere (0757, 0828), words it joined or split at line ends (0757 `in-`/
     `ceperunt`, `inisto`, 0768, 0792), and misreadings (0765 `Tune`, 0767 `-oresm`).
   - **Batch 10**: 0832 0839 0851 0856 0863 0877 0901 0906
     0912 0917: complete, tercet numbers and apostrophes right; the page head written on
     one line on 0877, 0906, 0917 (put in the usual form), 0877 two gloss dashes `--`.
     10 places not as printed (fixed): 0832 `provam` (written `probam`), 0877 `pre-`/
     `mictit` (written `mittit`), 0863 `Frantie` (written `Francie`), 0832 gloss `⁴)`
     printed without its opening bracket; punctuation (0839 `iudice.`, 0863
     `resurgerent.`, 0906 `essent,`, 0917 `posita:`, 0901 `platonica :` with a space).
     Kept as printed: 0912 `quïeta`, `E'`, 0917 `Seraphin`/`Serafin`; 0901 and 0912
     are essay pages. In `ocr/la`, answers in `bak3/` (`done10.txt`); `la_check.py`
     misses one rule on 0832 and finds a spurious one below the page on 0839. Markup
     (paid, by the user, `-r 3`) re-checked with `-r 0`: 2 differences missed, none not
     placed; both at words broken at line ends (0856 `Testa-`/`menta` next to
     `Testamento`, where `-r 0` dropped the wrong entry; 0912 `azione,`).
   - **Batch 11** (sent again to a new la-el-agy session
     after an OS crash): 0919 0921
     0922 0923 0930 0954 0968 0987 0988 0989: complete, page heads and tercet numbers
     right. 32 places not as printed (fixed), mostly punctuation: 20 periods written as
     commas or left out (0921 `caritatem.`, 0922 `hic.`, `sacra.`, `unda.`, 0930 `Ammon.`,
     `plorare.`, `faciendo.`, `Israel.`, `ducit.`, `fatua.`, 0954 `animam.`, `ingenium.`,
     0968 `oppositum.`, `carum.`, `potest.`, `virtutem.`, 0987 `dividitur.`, `planete.`,
     `Cancrum.`, 0989 `conveniebat.`), colons as semicolons (0930 `Agamennon:`,
     `dirigit:`); apostrophe gaps written where none is printed (0919 `suo'malitia`,
     `de'mortali`, 0921 `ha'l`, `fe'di`, 0923 `vo'saper`, 0989 `m'accors'`, `ch'er'entro`,
     `entra'mi`); letters (0922 `undecumque`, 0954 `influentie`). Kept as printed: 0923
     `se 'l`, 0988 `t' ò`, `ond' io so' facto`, 0989 `accors' io`. In `ocr/la`, answers in
     `bak3/` (`done11.txt`); `la_check.py`'s extra rule on 0930, 0954, 0989 is the
     page-end rule; it misses one rule on 0922 and 0968. Markup (paid, by the user,
     `-r 3`) re-checked with `-r 0`: 5 differences missed in 5 pages, 4 entries not
     placed (0954, 0968, 0987, 0988), all GLM-OCR's or the answer's: 0921's Latin verse
     block placed elsewhere, 0922 `Grecivolebant` joined, 0987 `duodecim signa: ibi sunt`
     left out by GLM-OCR, 0954 an entry overlapping the one before, 0968 `diverse` twice
     on its line, 0988 an answer reading `septentrio-` for the printed `septemptrio-`.
   - **Batch 12**: 0992 1001 1005 1006 1015 1016 1029 1032
     1040 1041: complete; paragraphs indented with four spaces on 1029, 1032, 1040 (17
     lines, unindented). 21 places not as printed (fixed): periods written as commas or
     left out (0992 `modernum.`, `crescit).`, `Theologia.`, `Renum.`, 1005 `potenti.`,
     `predicavit.`, 1006 `capituli.`, 1015 `facem.`), colons as semicolons (1006
     `Dominicus:`, 1040 `corporis:`, `qualificationem:`), commas left out (1016
     `invicem),`, `fecit,`, 1029 verse `secondo,`), apostrophe gaps left out (0992
     `s' infiora`, 1006 `com' el`, `ch' esser`), 1040 `udii` twice (written `udiì`), 1029
     `animam` (its `m` broken; reported as a misprint `aninam`), 1032 `┴.` (written `┴ .`).
     1032's two small figures in the text are written `┴` and `X` (the printed shapes, in
     `lineam rectam ut hic, ┴.` and `sicut hic, X.`). Kept as printed: 1029
     `scientia … fe-`/`cundata`, 1041 `scientiticorum`, 1040 verse `luce` against the
     commentary's `voce`. In `ocr/la`, answers in `bak3/` (`done12.txt`); `la_check.py`
     misses one rule on 0992, 1006, 1040 and 1015's signature blank, and sees the page-end
     rule on 1016. Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 3
     differences missed, none not placed, all at GLM-OCR's joins (1006 `periperolem` for
     `per iperbolem`, 1016 `can-`/`taverant`, 1032 `solem-`/`pnitatibus`).
   - **Batch 13**: 1043 1047 1052 1054 1066 1078 1080 1089
     1097 1099: complete, no indentation; 1047 an essay page (two title lines), 1097 a
     summary page (`CAPITULI DECIMINONI SUMMARIUM`, the old file's `DECIMNONI` was wrong),
     where a blank line at the column change, with no rule printed, was removed. 23 places
     not as printed (fixed): periods written as commas (1043 `Sol.`, `suum.`, 1054 `me.`,
     `posse.`, `Deo.`, 1066 `idest.`, 1080 `care.`, 1089 `cordula.`, 1097 `facit.`, 1099
     `deitate.`, `quelibet.`), colons as semicolons (1052 `intellexisse:`, `posuit:`, 1066
     `rus:`, 1078 `concordare:`), 1043 `anime;` and 1052 `mea,` swapped; apostrophe gaps
     (1052 `agl' ochi`, `noll' intesi` left out, 1054 `ne'mortali` written); 1099 verse
     `scripse` (written `scrisse`), 1066 `Imperatori` with a Cyrillic `г`, 1099 the
     misprint `elementia` (written `clementia`). Kept as printed: 1052 `intel-`/`xisse`,
     1066 `infirmate`. In `ocr/la`, answers in `bak3/` (`done13.txt`); `la_check.py` sees the page-end rule on 1066 and
     1078 and misses 1099's gap between sections. Markup (paid, by the user, `-r 3`)
     re-checked with `-r 0`: 11 differences missed in 8 pages, 1 entry not placed (1052);
     the text was right at each (1054 `supple,` and `etc ,`, printed so, checked in the
     image): GLM-OCR's Latin verse blocks placed elsewhere (1043, 1078), its joins at line
     ends (1052 `intel-`/`xisse`, 1099 `hysto-`/`[riam`) and misreadings (1047, 1066,
     1097).
   - **Batch 14**: 1104 1112 1114 1123 1143 1145 1148 1155
     1165 1175: complete, no indentation, rules and blank lines right. 45 places not as
     printed (fixed): 30 periods written as commas (14 on 1175, 7 on 1148), 7 colons as
     semicolons (1104 `crucifixus:`, 1112 `equitate:`, 1155 `nem:`, `etc.:`, `videtur:`,
     1175 `extinctus:`, `loqui:`), 1148 `affectus` (comma added) and `Virginis,` (comma
     left out), apostrophe gaps (1104 `fe’ e`, 1114 `buon’ intention`, `gl’ è` left out,
     1123 `agl’ochi`, 1175 `s’appunta`, `agl’occhi` written). The page heads of 1165 and
     1175, printed `CAPITULUM … 1111` on one line, put as title and number on two lines
     (as on 73 other pages); 1165's broken gloss mark `(¹,` written `(¹)`. The text with
     no other reading (1114, 1143, 1155, 1165) checked in the image. In `ocr/la`, answers
     in `bak3/` (`done14.txt`); `la_check.py` misses a rule on 1114, 1143, 1155 and 1165.
     Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 8 differences missed in 5
     pages, 5 entries not placed (1112, 1143, 1155, 1165); the text was right at each:
     GLM-OCR's Latin verse block placed elsewhere (1112) and a paragraph run into the
     verse (1114), its joins at line ends (1104 `dam-`, 1112 `progeni-`, 1143 `spe-`/`ra-
     rum`, `ha-`, 1155 `con-`/`cepi.`).
   - **Batch 15**: 1176 1187 1189 1190 1191 1192 1193 1211
     1214 1218: complete, no indentation. On 1189–1193 every rule was written as a line
     `—` (the report called them blank lines): turned into blank lines, 1193's rule at the
     foot of the left column added; the blank lines then checked against the image on all
     ten pages (1192's three right-column section gaps have no visible rule). 29 places
     not as printed (fixed): 13 periods written as commas or left out, 1192 `varias:`,
     `totum:` and 1214 `Deo;` swapped, 1214 `tantum,`; 12 spellings changed (1218
     `disgressi` ×4, `disgressio-`, `impinguat`, `impinguatur`, `illam`; 1176 `angusto`;
     1189 `opportet`, `corrupit`; 1193 `quinus`). Broken gloss marks (1190, 1192, 1193
     `²)`) written whole. The text with no other reading (1190, 1191, 1214) checked in the
     image. In `ocr/la`, answers in `bak3/` (`done15.txt`); `la_check.py` misses rules on
     1176, 1190, 1193 and 1211 and 1192's gaps.
     Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 14 differences missed in 7
     pages, 2 entries not placed (1176, 1193); the text was right at each (1176
     `quecumque` one word in the image): GLM-OCR's Latin verse blocks placed elsewhere
     (1187, 1193), its runover `[cinto` (1193), its lost `c` (1187 `cambi[a]-`, 1211
     `cambiando`) and spacing (1211), its joins at line ends (1189 `Chri-`/`stiani`, 1190
     `vice-`, 1193 `dele-`, 1218 `vi-`/`giliis`).
   - **Batch 16**: 1223 1224 1226 1231 1235 1236 1238 1247
     1259 1277: complete, no indentation, rules as blank lines. 1247's Latin verse was not
     as printed (a translation of the Italian: `tam pulchra est ad pedes suos`, `subtus`,
     `prout`, `Sarram, Rebeccam`, `cantoris, qui pro dolore`, …): its 8 lines retyped from
     the image; a blank line put before its `[figure]` (as on 1245). 24 places not as
     printed (fixed): 9 periods written as commas, 4 colons as semicolons, 6 apostrophe
     gaps, 1224 `metaphorice,`, 1236 a stray mark before `gnum`, 1277 `gubernas` without
     accent. The report's glosses for 1223, 1226, 1235 and 1238 do not match the files
     (the files are right). 1231 is the essay `IL LUME DI GLORIA` (Italian, one column).
     The text with no other reading (1223, 1236) is in the Tesseract words. In `ocr/la`,
     answers in `bak3/` (`done16.txt`); `la_check.py` misses one rule each on 1235
     and 1236, and 1226's gap before `Et etiam` has no rule.
     Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 10 differences missed in 4
     pages, 1 entry not placed (1247 `beccha`, a line-end split); the text was right at
     each: GLM-OCR's spacing (1223 `de mones`, 1231 `,cioè`, 1238 `Deum;quem`, 1247
     `(¹), che`), its lost or doubled letters (1231 `dell'infinite`, 1238 `medidiante`,
     1247 `Rebecha` ×2, a lost `Deus,`) and 1238's gloss mark `(')`.
   - **Batch 17**: 1280 1281 1283 1285 (commentary only, no
     rules): complete, no indentation. 11 places not as printed (fixed): 1280 `dicit.`,
     `videbuntur,`, `doverion`, `Com' aqua`; 1283 `rinfonde`, `mictit`; 1285 `viginti`,
     `intellectu.`; and three italic `v` read as `r` or a tick (1283 `ritrovi`, 1285
     `vedute`, `diverse`: this italic `v` looks like `r` in the scan, as in `rimuovi`,
     `vetro`, `Rivolto` that were written with `v`). Kept as printed: 1281 `omuibus`,
     `splendolum`, 1285 `caasantur`; 1281 `Notar` (damaged italic, GLM-OCR and Tesseract
     read `Notur`). In `ocr/la`, answers in `bak3/` (`done17.txt`).
     Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 3 differences missed in 3
     pages, 1 entry not placed (1281, overlapping); the text was right at each: GLM-OCR's
     `ruro` (1281) and `to tum` (1283); on 1285 a wrong entry (`ostendere.`, the print has
     `,`), which the re-check dropped.
   - **Batch 18**: the front matter 0046 0048 0049 0050
     (papal documents in two columns), with its own layout: number and `DOCUMENTA` as
     printed, `Doc. N.` and its date on two lines between blank lines, the source note on
     its own line, a row of dots `. . . . .`: complete (Doc. 2 end to Doc. 19 start), no
     indentation, word counts within a few of GLM-OCR's. 2 places not as printed (fixed):
     0049 `nolumus` (written `volumus`), 0048 `qualiacumque,fecerint` (no space in the
     print). Kept as printed: 0049 `inibitionem`, `(Ibid.` without its bracket, 0050
     `excomunicari`. In `ocr/la`, answers in `bak3/` (`done18.txt`).
     Markup (paid, by the user, `-r 3`) re-checked with `-r 0`: 4 differences missed in 3
     pages, none not placed. Two were dot runs written wrong, fixed after the markup: 0048
     `illi... qui` (a printed ellipsis, not a row of dots) and 0050 `eadem. . . . . .` (a
     period, then the dots); their answers no longer place on those lines (1 entry each),
     left for item 7. The others: 0048 `qualiacumque,fecerint` as printed, 0049 GLM-OCR's
     `nuliatenus` against the dot rows. With this batch the retyping of item 6 is done.
7. **Model decisions** (paid), after item 6: a new work directory over all pages,
   `la_markprep.py`, then `la_markdecide.py` (procedure, steps 3–4). Done (2026-10-22,
   Record of the preparation): `tmp/la-mark7/`, 22141 marks decided.
8. **Batches 3–11**: procedure steps 5–11, batch by batch, with WORK = `tmp/la-mark7`
   (steps 2–4 done there for all pages in item 7) and `-p FIRST LAST` on
   `la_markresolve.py`, so that only the batch's pages are routed, reviewed and written.
   - **Review in parts** (decided with the user, 2026-10-22): step 6 goes about 20 pages
     at a time; after each part, stop and report to the user (pages done, marks decided,
     pages retyped, open points) before going on.
   - **Parts retyped by la-el-agy** (decided with the user, 2026-10-22, from 0276 on):
     way B of step 6, instead of way A, deciding the marks one by one (both in "Procedure
     for a batch", step 6). Task series retype 19–.
   - **Batch 3** (0233–0348, 109 pages, 2166 marks in `review.tsv`): steps 5–9 and 11
     done (2026-10-23, `texts/la/021`–`030`). Step 6: all marks in
     `WORK/mine.tsv`, corrections in `WORK/fixes.tsv`. Step 7: the word diff of the
     mark-decided pages read (the retyped pages' differences were checked against the
     two OCRs), written to `ocr/la` (103 pages changed). Step 8: two blank lines at rules
     added (0235), 0236's commentary rebroken where inserted text had run printed lines
     together (also 0241, 0233 and 0251 at step 9), 24 dots before a lowercase word made
     commas, 0347 (an essay kept as one line per paragraph, retyped line by line) joined
     back into paragraphs. Step 9: tercet numbers 0251 `²⁶` and 0253 `³⁴`–`³⁸` (the file
     had `²⁸`, `²⁴`–`²⁸`), 0241's numbers made superscript; page numbers added on 0242,
     0247, 0249, 0253 (0249 `CAPITULO` for printed `CAPITULUM`); 0236's gloss markers made
     superscript; 0265 a blank line after the left column's last rule. Step 11 found:
     0249's running head repeated before the Latin verse (removed, as 0227), 0312's
     runover `[fidem,` after the wrong line (moved after `ita meam`), and 0324's two-line
     essay title split by a blank line (joined as on 0303; `convert_la.py` now joins a
     title printed on two lines). The 14 remaining
     `NO BLANK` hits of `la_lines.py` and the pages `la_check.py` lists with more rules
     than blank lines were looked at: page-end rules or a short last line matched early.
     0299–0322 (24 pages, 482 marks) retyped by la-el-agy (retype 20): 36 places not as
     printed fixed, among them a lost line (0313, the first line of the right column),
     dots before a lowercase word (20 times, later turned back to commas), 4 colons
     written as semicolons, missing marks (`dispositus,`, `minus,`, `baractandum.`), letters
     (`trageto`, `Veggio`, `recordar`, `malefice`, `desiït` for printed `tragecto`,
     `Veggo`, `ricordar`, `malifice`, `desiit`), 3 apostrophe gaps where the print is
     tight; verse lines indented with spaces (removed). Where both OCRs were wrong it read
     right (`Virgllio`, `fixuras`, `DECIMUMNONUM`, `dïsse`, the column order of 0318 and
     0321).
     0323–0347 (24 pages without the blank 0326, 454 marks) retyped by la-el-agy (retype
     21): 99 places against the two OCRs looked at in the image, 28 fixed (among them 10
     dots before a lowercase word, later turned back to commas), 3 colons written as
     semicolons, letters
     (`contegnum`, `porossum`, `disfatiat`, `subtraxit`, `medium`, `figlio`,
     `edipficaverunt`, `sfavillat`, `confinato` for printed `contegnam`, `porosum`,
     `disfaciat`, `substraxit`, `medio`, `figlo`, `edificaverunt`, `favillat`,
     `continato`), a space put before a footnote number where the print has none
     (`cesso(⁴)`, `lungi(¹)`), 4 apostrophe gaps (`che'l`, `e'l`, `Onde'l`, `E'l`). No
     line lost; the tercet numbers of 0333, 0335 and 0343–0346 put in superscript and
     checked in the image.
     0276–0298 (21 pages, 410 marks) retyped by la-el-agy (retype 19): 159 places
     against the two OCRs, about 130 looked at in the image; 25 places not as printed
     fixed: `seis` for `scis` (5 times, 0297), `a se` for `à sè` (0276), `dimisit` for
     `dimictit` (0278), `feggi`, `cic[r]chiis`, `vaneggiat` (0286, printed `feggia`,
     `cie[r]chiis`, a broken `vineggiat`), `s'iniccat` for `s'imiccat` (0288), the gloss
     line of 0297 (`mie`, `sì` for printed `mic`, `si`), `[infra,` for `[infra.` (0297);
     colons written as semicolons (0277, 0279, 0298 twice), periods before an uppercase
     word as commas (0279 `curro.`, 0295, 0298), 7 apostrophe gaps. Where both OCRs were
     wrong it read right (`Tunc` for their `Tune`, `orizontem`, `pietam`, `Jason`,
     `excomunicati`, `perchuote`, `qualunque`, `Çaccianimici`), and it put in the lost
     lines and the superscript tercet numbers of 0285, 0294, 0298. Left as read:
     0297 `forachiatum` (the italic fourth letter `a` or `u`).
     In 0254–0275, 10 of 20 pages were retyped whole from the scan (0254, 0255, 0259,
     0260, 0262, 0265, 0267, 0270, 0273, 0274; 0270 only put in column order): the old
     OCR there runs commentary lines together, drops lines and words, and puts columns
     and page heads out of order. On an essay page kept as one line per paragraph (0267),
     blank lines go before and after each quotation.
     What these pages showed:
     - The old OCR of `ocr/la` here is poor: u/v and `ae`/`æ` normalized (`siluam`,
       `flammæ`), words and lines lost, columns out of order; most marks go to GLM-OCR's
       side, each still looked at in the crop.
     - A page or column too broken for the marks is retyped from the scan: every mark of
       it decided `left`, and one row of `fixes.tsv` replaces the old text by the retyped
       one (0248 the whole page, 0253 the right commentary column; 0242's last two
       paragraphs of the left column moved before the right column).
     - Lost lines and words are put in as `text:` with `⏎` where the print breaks the
       line, and a `fixes.tsv` row joins what then falls on the wrong line. An inserted
       side has no surrounding spaces (`omnes{{|tales}} fuerunt`): write `text: tales`.
       A removed word leaves two spaces: after each resolve, look for `  ` in `WORK/out/`
       and fix them.
     - Page heads out of order (0241, 0251: the page number after the running head; 0236,
       0240: a running head inside the text) are put right in `fixes.tsv`.
     - Tercet numbers not superscript (`27 Tra tutto …`) on 18 pages of the batch (0240,
       0241, 0248, 0262, 0265, 0285, 0294, 0298, 0302, 0313, 0316, 0322, 0333, 0335,
       0343, 0344, 0345, 0346; listed by `grep -cP '^\d+ \(?[A-Z]'`): all but 0241 done
       in the review or the retyping; 0241 to make superscript at step 9, each number
       checked in the image (0240 printed `29` where the file had `27`).
   - **Batch 4** (0349–0478; way A, decided with the user, 2026-10-23): step 6 done for
     0349–0399. 20 of
     45 pages retyped from the scan by la-el-claude (0349 0353 0354 0355 0363 0365 0369
     0376 0377 0381 0382 0384–0389 0391–0393): lines run together or out of order, lines
     lost, Italian and Latin swapped (0393), `[For lines …]` notes in the text (0392).
     0387 and 0388 are essay pages kept as one line per paragraph and were retyped line
     by line by mistake: join them back into paragraphs at step 8 (as 0347). 0383's
     signature is `42` (a worn `4`, as on 0399). 0395–0399 are la-el-opencode's retype 23
     with its errors fixed (below). 0400–0478 (76 pages with marks; 0408, 0430, 0452, 0478
     blank, 0477 the PURGATORIUM title) by the low-cost way below, in four parts: 1859 marks
     (`light` 767 over the batch), no page retyped by la-el-claude; losses put back from
     the image on 0447, 0455, 0456, 0457 (two paragraphs), 0462 (its right column also
     before the left), 0471 (two paragraphs); verse printed side by side split (0449, 0469);
     page numbers inside the text moved into the head. 0467 was left pending and then
     retyped by la-el-agy (item 10). Written to `ocr/la` (2026-10-24, 119 pages changed).
     The step-9 checks found tercet numbers lost (0401, 0405, 0414, all of them; 0363 one),
     misread (0350, 0455) or misplaced (0402), runovers (0461, 0466), a blank line inside
     the verse (0432), and 0449's verse still side by side: its `fixes.tsv` row had tabs in
     the text, which split the row's fields (`⇥` now stands for a tab in `fixes.tsv`).
     Fixed and written again: `la_check.py` tercets, `la_seqcheck.py` (but `plain`) and
     `la_lostcheck.py` give no hits. Plain-digit numbers and curly apostrophes are left (item
     9, a later normalization).
   - **Batch 5** (0479–0609, cantos I–XI of the Purgatorio and the summary of XII; 2026-10-24) by the low-cost
     way, in six parts of about 20 pages; 0532, 0554, 0608 blank, 0488 without marks.
     Besides the marks: losses put back from the image (0490, 0496, 0499, 0504, 0519,
     0522, 0540, 0558, 0559, 0591, 0592, 0595; 0603 eleven half-lost lines, 0600 a
     paragraph run into one line and also misplaced), paragraphs moved (0515, 0528), tercet
     numbers (0529 `88`–`95` for `38`–`45`, 0563, 0606), page heads (the page number, a blank
     line, the head; numbers added, heads repeated before the Latin verse removed), and
     the rule lines (`—`, `___`) made blank lines. In the light routes that keep `ocr/la`
     where the model reads neither OCR, `ocr/la` was clearly corrupt in a few places, put
     right from the image. The broken pages were not left pending this time but retyped at
     once by la-el-agy (way B, superscript kept, decided with the user): 0538 (retype 26)
     and 0545 0549 0557 0560 (retype 27) on Gemini 4 Argon, no letter or line errors;
     0579 0583 0584 (retype 28) and 0593 0604 (retype 29) on Gemini 3.8 Flash (the user
     switches the model by hand; Argon's quota is small), 4 errors in 5 pages (a speck
     written `fosse, .`, a stray `est, .Tarpeya`, `atterent` and `s'affecta` for printed
     `atterrent`, `s'affrecta`) and apostrophe gaps opened where both OCRs had none; the
     column order and every line right on all of them, 0583's lost column top restored.
     `la_check.py` got `-d` to read the pages from `WORK/out` before they are written.
     Written to `ocr/la` (118 pages changed); step 9: no hits but 0545's bracketed tercet
     `[⁷ Vidi …]`, printed so.
   - **Batch 6** (0610–0728, cantos XII–XXI of the Purgatorio; 2026-10-25) by the low-cost
     way, in six parts of about 20 pages; 0620, 0644, 0680, 0692, 0704, 0718 blank.
     Besides the marks (201 `fixes.tsv` rows): page numbers and heads, spaces, printed line
     ends and short rules as before; losses put back from the image (0614, 0646 a line lost
     and one written twice, 0720), gloss lines joined or moved before the Latin verse
     (0628, 0634), runovers on their own line after their verse line, no blank line at a
     column change without a rule (0653, 0693, 0702, 0705, 0716). The broken pages were
     retyped at once, superscript kept: 0611 0612 0613 0625 0626 0627 0629 by la-el-agy
     (retype 30, Gemini 3.8 Flash); the rest split three ways and run at the same time
     (the task files are per agent; the `retype pending (retypeN)` notes in `mine.tsv`
     carry the part numbers, not these, so they were replaced by page):
     0635 0638 0643 0652 0659 0663 0664 0665 0672 0673 0674 by la-el-agy (retype 31),
     0675 0676 0677 0683 0685 0686 0687 0688 0689 0690 0691 by la-el-agy2 (retype 32),
     0694 0695 0696 0697 0698 0700 0703 0706 0707 0710 by la-el-agy3 (retype 33), all on
     Gemini 3.8 Flash; 0711 0713 0717 0722 0724 0725 0727 by la-el-claude (retype 34),
     since the three agents were busy. Every agy page had its lines there and in order;
     13, 18 and 15 places were put right in retypes 31–33: colons written as semicolons,
     spaces put before `:`, `;`, `?` or a gloss mark tight to its word, printed misprints
     normalized (`diminuerà`, `loquutus`, `transcorso`, `Berlingerii`, `indicabant`) and
     misprints invented (`Faciuut`, `llla`), accents added (`dualita`, `udi'`), apostrophe
     gaps opened on the essay pages (0691, 0703), blank lines where no rule is printed.
     Written to `ocr/la` (106 pages changed). Step 9: 0610's verse (a canto's first page)
     still had blank lines between the tercets and its runovers in the line, retyped from
     the scan and written again; then no hits but `plain` (0647, 0648 `13`, 0670 `3`) and
     the rule counts of `la_check.py`, which miss worn rules.
   - **Batch 7** (0729–0846, cantos XXII–XXXI of the Purgatorio; 2026-10-25) by the low-cost
     way; 0740, 0786, 0798, 0824, 0846 blank. Besides the marks, as in batch 6, and the
     light-kept audit (step 7). The broken pages were retyped at once, superscript kept:
     0731 0733 0735 0736 0737 0743 0759 0766 0771 0779 by la-el-agy (retype 35); 0780 0781
     0785 0788 by la-el-agy2 (retype 37); 0810 0812 0816 0819 0821 0827 0833 0834 0837 0838
     0841 0843 by la-el-agy (retype 38); 0739 by la-el-agy (retype 39). Every page had its
     lines there and in order; in retype 38, 20 places were put right (letters changed:
     `avegna`, `corelarium`, `Penitentic`; `[deberet]` closed; a colon for a semicolon and
     back; accents added and dropped; apostrophe gaps opened, gloss marks tight to the
     word). The commas agy wrote for dots before a lowercase word are right (convention,
     step 7): la-el-claude first put 21 of them back to dots from the image, then made
     them commas again. Retype 35 had dropped all 14 tercet numbers of 0779, missed by the
     retype check; `la_check.py` found it at step 9 (`0780 starts at 23`).
     Written to `ocr/la` (110 pages changed; 580 `fixes.tsv` rows, 27 of them whole retyped
     pages). Step 9: 18 gloss marks tight to their word given a space (0744 0755 0757 0758
     0781 0804 0817), 0779's numbers put back; then no hits but the printed tercet numbers
     of 0758 and 0810 (Suspected misprints).
   - **Batch 8** (0847–0960, the end of the Purgatorio and cantos I–VII of the Paradiso;
     2026-10-25) by the low-cost way; 0870, 0872, 0888, 0960 blank, 0871 the PARADISUS
     title. 3168 marks (`light` 1315). The broken pages were retyped at once, superscript
     kept, by way B (item 10): 0849 0853 0854 0855 0858 0860 0861 0864 0866 0869 0879–0887
     by la-el-agy2 (retype 41), 0891–0900 0904 0905 by la-el-agy (retype 42), 0909 0915
     0916 0918 0920 0926–0929 by la-el-agy2 (retype 43), 0937 0938 0939 0942 0943 0945 0946
     0951 0952 0953 0956 0957 0959 by la-el-agy3 (retype 44). Every page had its lines there
     and in order; the places put right are listed under item 10. Light-kept audit (step
     7): 62 kept rows still in `out/`, 16 on pages not retyped, cropped: the printed
     misprint `tulli` (0850, the italic lemma; `ocr/la` had `tutti`) and a gloss bracket
     broken in print (0851 `(³)`); on the six essay pages not retyped, two accents not
     printed (0912 `cio`, 0934 `unita`), the rest of the word differences with GLM-OCR as
     printed (0948 `sí` with an acute). Also 0875 and 0876 with plain-digit tercet numbers
     and gloss marks (made superscript) and 0876 a line run into the next. Written to
     `ocr/la` (103 pages changed; 322 `fixes.tsv` rows, 54 of them whole retyped pages).
     Step 9: page heads with the number at the right written head first (0857 0867 0955,
     0911 with a blank line between, 0865 without its number `811`) made number, blank
     line, head, and 0874 given its blank line after the number; then `la_check.py` with no
     tercet hits but 0861's printed bracket `[Mi disse … seco]` (read as a runover), and
     `la_seqcheck.py` and `la_lostcheck.py` with none. The same head-first form on
     earlier pages (0353 0355 0363 0365 0369 0411 0417 0421 0427 0433 0437 0439 0461 0469
     0471 0473 0591) was made number, blank line, head afterwards (in `ocr/la` and in
     `fixes.tsv`); batch 9 has it too (0963 0965 0981 0991 0995).
   - **Batch 9** (0961–1072, cantos VIII–XVI of the Paradiso; 2026-10-26) by the low-cost
     way; 1010, 1024, 1048 blank. 3137 marks (`light` 1418). The broken pages were retyped,
     superscript kept, by way B (item 10): 0964 0975 0977 0980 by la-el-agy (retype 45),
     0963 0965 0967 0969 0970 0971 0979 by la-el-agy2 (retype 46), 0981 0983 0985 0991 0993
     0997–1000 by la-el-agy3 (retype 47), 1002 1003 1004 1008 1009 1011 1013 1014 1017–1020
     by la-el-agy (retype 48), 1021 1023 1027 1028 1030 1031 1033 1035 1038 1039 by
     la-el-agy2 (retype 49), 0972 0984 0996 1042 1044–1046 1050 1055–1057 1059 1060
     1062–1065 1067 1069–1072 by la-el-agy3 (retype 50); 64 pages, the places put right
     listed under item 10. Light-kept audit (step 7): on the pages not retyped, the kept
     rows still in `out/` as printed (0976 `meae`, 0990 `Regrazia`, 1007 `scil cet` with a
     broken `i`, 1040 `molestie`); the essay pages' accents checked (1036 `remove-`, 1047
     `aggiungera` printed without the accent). Five pages not retyped had plain-digit
     tercet numbers where small superscripts are printed (0990 0994 1007 1041 1058, 40
     lines, made superscript), and 1058 two rules written `—` (made blank lines) and a
     blank line at a column change with no rule (dropped). Written to `ocr/la` (106 pages
     changed; 333 `fixes.tsv` rows for the batch, 64 of them whole retyped pages). Step 9:
     `la_check.py`, `la_seqcheck.py` and `la_lostcheck.py` with none, after 1042's
     tercet numbers were put back (la-el-agy3 had left all 14 out; the check of the
     retypes against the OCRs skipped differences in tercet numbers alone). Every page
     head is number, blank line, head. `la_retype.py` appends a row on each run, so a page
     brought in again had chained rows; they were merged into one row per page (the
     resolved pages unchanged).
   - **Batch 10** (1073–1184, cantos XVII–XXVI of the Paradiso; 2026-10-26) by the
     low-cost way, in five parts (1073–1095, 1096–1119, 1120–1141, 1142–1162, 1163–1184);
     1084, 1096, 1120, 1150, 1162, 1184 blank. 3209 marks (`light` 1408). The broken pages
     were retyped, superscript kept, by way B (item 10), all by la-el-agy (the three-agent
     split was dropped: agy's quota was low): 1074 1075 1076 1077 1079 1081 1083 1087 1090
     1091 1092 1093 1095 1098 1101 1102 1103 1105 1107 1108 1111 1115 1117 1127 1130 1133
     1138 (retype 51, which took in the requests first written as retypes 52 and 53), 1146
     1149 1151 1153 1154 1156–1159 1161 1166 1169 1172 1174 1177 1178 1180 1181 1183
     (retype 54); 46 pages, the places put right listed under item 10. Light-kept audit
     (step 7): 24 kept rows still in `out/` on pages not retyped, cropped; not as printed
     1080 `monstravit` (the italic lemma prints the misprint `mostrarit`), 1112 `Iovem.`
     (a comma), 1135 `animae` (`anime`), 1144 `oblationem, dignam` (no comma), 1152
     `sodalitio electo` and `electo` (the lemma prints `sodalitie electe` and `eletto`); on
     the essay pages not retyped (1119 1140) the accents as printed, and 1119 `fenom-` for
     printed `penom-`. No line run together, no `æ`. Written to `ocr/la` (106 pages changed;
     548 `fixes.tsv` rows for the batch, 46 of them whole retyped pages). Step 9: 1139's
     runovers `[pensa` and `[cogitat,` were at the end of the following line (each moved to
     its own line after its verse line) and `[fu chiaro]` had a `]` not printed; then
     `la_check.py` and `la_seqcheck.py` with only 1182's printed tercet number (Suspected
     misprints), `la_lostcheck.py` with none.
   - **Batch 11** (1185–1296, cantos XXVII–XXXIII of the Paradiso, the essay `La
     preghiera`, the *Fragmenta commentarii* and the index; 2026-10-26) by the low-cost
     way, in five parts (1185–1209, 1210–1233, 1234–1257, 1258–1272, 1273–1296); 1232 1244
     1256 1272 1288 1291 1292 1294–1296 blank. 3481 marks (`light` 1425). The broken pages
     were retyped, superscript kept (item 10): by la-el-agy, way B, 1199 1200 1201 1203
     (retype 55), 1217 1227 (retype 56), 1258 1262–1267 (retype 57), 1273–1276 1278 1279
     1282 1284 1286 1287 (retype 58: every *Fragmenta* page not retyped in item 6, whose
     `ocr/la` had lines lost, sentences rewritten and spellings normalized, `coeli`, `æ`;
     1275 and 1286 a paragraph a line); by la-el-claude from the image and Tesseract's
     lines, 1196 1219 1220 1221 1237 1239 1241 1245 1246 1248 1250–1255 1257 (1196 1220
     1221 1245 1255 had a paragraph a line; part 3's 13 were done without asking, and the
     user chose to keep them without a cross-check by la-el-agy). 40 pages; the places put
     right in la-el-agy's under item 10. Smaller damage by fixes: blocks lost or rewritten
     retyped from the image (1188, 1212, 1213, 1225, 1228; lines or words on 1195, 1204,
     1209, 1210, 1216, 1229, 1234), the tercet numbers missing on 1189–1193 and 1210, page
     heads, runovers, the quotation blank lines after `que incipit ibi:` (1198 1210 1222
     1234 1246), glosses after the Latin verse moved between the blocks (1215 1242), about
     35 unmarked dots before a lowercase word made commas. The pages retyped in item 6
     (1277 1280 1281 1283 1285): the light route had put the OCRs' reading over the retype
     in 4 places (`simigliante.`, `Notar`, `dictum`, the misprint `caasantur`), put back.
     The index (1289 1290): two lines lost on 1289, `Capitulum` from the light route back in
     capitals, blank lines at the column changes removed, `I N D E X` without the spaces,
     `» 663`. 1287's `FINIS`, printed in an ornament, written after a blank line. Written to
     `ocr/la` (98 pages changed; 369 `fixes.tsv` rows for the batch, 40 of them whole
     retyped pages). Step 9: `la_check.py` only 1293's barcode taken for a tercet number,
     `la_seqcheck.py` only the footnote marks `(1)` of 1274 and 1282 (printed plain, like
     the footnotes of the front matter), `la_lostcheck.py` only Tesseract's noise and the
     figure labels of 1245 and 1247.
   - **Front matter** (`0001`–`0078`, titles, dedication to Leo XIII, *Notizie
     preliminari*, *Documenta*, *Comentum* half-title and incipit, Serravalle's
     *Dedicatio* and *Preambula*, *Infernus* half-title; 2026-10-26) by the low-cost way,
     in three parts (`0001`–`0028`, `0029`–`0054`, `0055`–`0078`); 0003 0005 0006 0008
     0009 0011 0012 0044 0056 0058 0078 blank (0009 and 0044 empty in `ocr/la`), and 0046
     0048–0050 retyped in batch 18 of item 6. 1322 marks (`light` 597). The broken pages
     were retyped from the scan and added with `la_retype.py`: 0051–0053 (*Documenta*
     pages with lost paragraphs and garbled lines) and 0065 (*Preambula* page 11, whose
     39 printed lines were collapsed onto a single line). Smaller losses restored from the
     scan by fixes: 0020 (`illanguidito`), 0029 (`exiguum atque indignum, anno ab
     Incarnatione eiusdem Domini Iesu`), 0045 (`alicuius subventionis auxilio providere,
     gratiamque facere spe-`, `ante acceptationem`, `quovis modo presumant, ac decernentes
     ex tunc irritum et`, `Canonicorum iuribus,`), 0054 (`aliis, tam`, misplaced running
     head removed), 0061 (`peccare boni, virtutis amore: oderunt` and lines 19–23
     re-lined). Light-kept audit and scan checks: page heads put in the standard form
     (`NUMBER\n\nHEAD`, letter-spacing removed on 0068 0071 0072 0076, missing numbers
     added on 0017 0021 0023 0025 0071 0075, `DOCUMENTA` added on 0054), signature marks
     kept after a blank line (`IV` on 0031, `V` on 0039, `2` on 0063, `3` on 0071),
     spurious `ae`/`æ` made `e` where printed so (0024 0027 0029 0045 0068 0069),
     markdown italics stripped on 0036, guillemet spacing and Italian accents verified in
     *Notizie preliminari*, and printed spellings kept (`BUBWYCH`, `Episcope`, `dectractoriis`,
     `prosumptuosum`, `conrespondentibus`, `dampnatos`, `aierem`, `esentialem`, `Theucro`,
     `Ericteam`, `Tarquinus`, `spetialiter`, `Parisios`, `connoctativum, connoctans`,
     `preventi`, `interpetrari`, `rythimis`, `principalius`). Written to `ocr/la` (57
     pages changed). Step 9: `la_check.py` with no tercet hits, `la_seqcheck.py` only the
     printed brackets of 0016–0019, 0021, 0022 and 0035, `la_lostcheck.py` with no `both`
     hits.
   - **Delegation trials for whole-page retyping** (2026-10-23), against way B's la-el-agy
     (about 1.2 errors a page in retypes 19–21), each checked word by word against both
     OCRs and in the image:
     - la-el-codex (retype 22, 0350–0353, 0359): about 11 errors a page, spellings
       modernized (`Meglo` → `Meglio`, `exinde` → `deinde`), apostrophe gaps added.
     - la-el-opencode (retype 23, 0395–0399; GLM-5.3 cannot view images, GLM-5.3-Flash
       can): 25 errors in 5 pages. The layout was right on every page (line and column
       order, runovers, the gloss block, on two broken pages too), but it invents misprints
       and reports them as printed (`aannullorum`, `scoppzato`, `Haliì`, `consintiente`),
       adds accents (`fé'`, `fòrato`, `Giù` for `Già`), normalizes (`merla` → `merda`,
       `stropiatus` → `stroppiatus`), and lost a tercet number and two commas. Its files
       (`tmp/la-retype23/opencode/`) with the 25 places fixed, and a speck read as an
       accent (0397 `vincerè`), are 0395–0399 in WORK (step 6 of way B: marks `left`,
       pages added with `la_retype.py`, `cmp` with `final/`).
     - la-el-opencode on Nemotron 3.5 Super VL (retype 24, 0400–0404, 2026-10-24): not
       usable. About 50 word errors a page on 0400–0401 (`Proper`, `victoriariam`,
       `capttus`, `--` for the em dash), a third to a half of 0402 and 0404 lost, and on
       0403 commentary invented and repeated in place of the printed text; its report
       called the pages confirmed. `la_lostcheck.py` showed it at once (46 `both` runs).
       Nothing of it is used.
     None of them replaces la-el-agy for whole pages.
   - **What the checks can see** (2026-10-24): Tesseract's own page layout is not reliable
     (on 0399 and 0376 its blocks span both commentary columns and run their lines
     together), and cutting the columns from the image by its rules was given up (dashed,
     worn and slanted rules, overlapping verse columns). `la_lostcheck.py` finds text
     lost from a page (both OCRs have it, the file not), loosely and in any order: over
     all pages, none in 0079–0348 and none in the reviewed 0349–0394, but 30 pages of
     0349–0477 and 202 of 0478–1296 in the current `ocr/la`. It cannot see lines out of
     order or run together (about half of batch 4's broken pages); two order checks
     (place in GLM-OCR, adjacency of Tesseract's lines) were tried and gave too many false
     hits. `la_seqcheck.py` adds the format checks `la_check.py` lacks.
   - **From here to the last page, at low cost** (decided with the user, 2026-10-24):
     finish every batch through step 7 without retyping pages; the retyping waits for
     item 10. Per batch, in parts of about 20 pages with a report after each:
     1. Step 5, then a screen of the part: `la_lostcheck.py FIRST LAST -t TESS -d
        WORK/out` (`both` hits) and `la_seqcheck.py FIRST LAST -d WORK/out`; after the
        fixes also `la_check.py FIRST LAST -d WORK/out -d ocr/la` (tercets).
     2. Step 6 by way A for the pages that are sound. A small loss (a line or two, found
        by `la_lostcheck.py` or in a mark) is put in with `text:` as before. Step 5 runs
        with `--light` (from 0400): the open `check` marks take the model's `right` and most
        open `image` marks keep `ocr/la`, so only the rest is looked at; obvious misprints
        are left for the final reading for sense, and plain-digit numbers stay (item 9).
     3. A page too broken for its marks (lines out of order or run together, columns
        mixed, more than a few lines lost) is **not retyped**: all its marks are decided
        `left|retype pending`, and the page goes into "Pages to retype" (item 10) with
        what is wrong. Its `ocr/la` stays as it is.
     4. Step 7 (`--write`) and the scripted checks of step 9 (`la_check.py`,
        `la_seqcheck.py`, `la_lostcheck.py` on `ocr/la`); hits on pending pages are left
        for item 10. Step 8 (the image checks of `la_lines.py`) and step 11 (texts) wait
        for item 10, so that each batch is checked and converted once, with its retyped
        pages in. Commit each batch's `ocr/la` (step 10) when the user asks.
     Batch 4 done this way from 0400; batch 5 too, but with its broken pages retyped at
     once by la-el-agy instead of left pending (see Batch 5); then batches 6–11, each
     ending before a canto summary page and retyping its broken pages the same way:
     6 `0610`–`0728` (Purgatorio XII–XXI), 7 `0729`–`0846` (XXII–XXXI), 8 `0847`–`0960`
     (XXXII–XXXIII, Paradiso I–VII), 9 `0961`–`1072` (VIII–XVI), 10 `1073`–`1184`
     (XVII–XXVI), 11 `1185`–`1296` (XXVII–XXXIII and the end).

9. **Plain digits for tercet numbers and gloss marks** (decided with the user,
   2026-10-24; waits until item 8 has written every batch, since `tmp/la-mark7`'s marks
   and `fixes.tsv` rows hold the superscript text and would no longer match): the tercet
   numbers (`³ Se s'adunasse`) and the gloss marks (`(³)`) in `ocr/la` become plain digits
   (`3 Se s'adunasse`, `(3)`), by a script, over all pages. The superscripts are where the
   OCRs and the delegates err most (numbers lost on 0375, 0378, 0380, 0390; not superscript
   on 0379 and on 25 pages of batches 1–2), and nothing needs them: `convert_la.py` counts
   the tercet numbers and writes `texts/la` as before, `la_check.py` reads both forms.
   With it: the conventions below, `la_seqcheck.py` (it reads only superscript blocks and
   lists `(1)` as a leftover), the rules of "Whole pages" in DELEGATION.md. No line of
   prose starts with a number followed by text (all 58 such lines outside full verse
   blocks were looked at, 2026-10-24): they are verse lines, a barcode (1293), and page
   heads run into the page number, to put on two lines in their batches (0070
   `16 PREAMBULA`, 0496 `442 PURGATORII`, 0636, 0802, 0818, 1094, 1156, 1268).
   - **Done** (2026-10-26): converted across all pages of `ocr/la` (897 pages changed), with
     six fixes found by the updated checks (0427's runover `[stat:` misread as `¹⁰`,
     0446's Latin tercet `15` and 1170's Italian tercet `38` added from the image, 0490's
     and 0506's `PURGATORII` moved to the page head, 0794's double space); `la_seqcheck.py`,
     DELEGATION.md, TEMPLATE-RETYPE.md and the conventions updated. `la_seqcheck.py 1 1296`
     reports only the printed exceptions (`0099`, `0350`, `0545`, `0758`, `0810`, `1182`).
10. **Pages to retype** (after item 9, so that the retyped pages use plain digits): the
    pages left `retype pending` in item 8 and those `la_lostcheck.py` lists, retyped from
    the scan (by la-el-agy, way B, or by la-el-claude), checked against both OCRs and
    with `la_lostcheck.py`, written to `ocr/la`; then steps 8 and 11 of each batch. The
    model decisions of these pages (`tmp/la-mark7`) are then unused. The list (page: what
    is wrong), filled in by item 8:
    - 0467: Italian verse with the runovers `[te (¹²).`, `[te (¹⁶),` on the following
      tercet's line, a Latin verse line lost (`⁶ Quando nos fuimus tantum ante,`) and one
      split (`coo-` / `perte`), the head after the page number; the commentary's first
      paragraph partly lost and its two columns mixed (`la_lostcheck.py`: 2 runs).
      Retyped early (2026-10-24, before item 9, superscript kept) by la-el-agy on its
      higher model, Gemini 4 Argon (retype 25), and added to `tmp/la-mark7` by way B: 18 places against the two OCRs looked at,
      the column order and the 4 rules (one worn, after `armes.`) checked in the image;
      la-el-agy was right everywhere except 10 dots before a lowercase word, made commas.
      `la_lostcheck.py`: none.
    - Batch 5's broken pages, retyped early in the same way (retypes 26–29, see item 8,
      Batch 5): 0538 0545 0549 0557 0560 0579 0583 0584 0593 0604. Done, but for steps 8
      and 11 with the batch.
    - Batch 6's broken pages, retyped early in the same way (retypes 30–34, see item 8,
      Batch 6): 46 pages from 0611 to 0727. Done, but for steps 8 and 11 with the batch.
    - Batch 7's broken pages, retyped early in the same way (retypes 35, 37–39, see item 8,
      Batch 7): 27 pages from 0731 to 0843. Done, but for steps 8 and 11 with the batch.
    - Batch 5, queued 2026-10-25 (found by the light-kept audit, after the batch was
      written): commentary lines run together, up to a whole paragraph on one line (0510,
      0528, 0529, 0544, 0581), with the line ends around them shifted, so a line cannot just
      be cut at Tesseract's line ends: 0501 0503 0509 0510 0516 0517 0518 0522 0525 0527
      0528 0529 0530 0539 0542 0544 0555 0558 0563 0565 0567 0570 0571 0573 0580 0581
      0588. Some also have words not as printed in those lines (0571 `minorem circulum
      describit.` for `describit minorem circulum;`, 0501 `qui-` / `bus` for `quibus`) and
      `æ` for printed `e` (0517 0518 0522 0529 0571). Their marks stay decided as they are
      (most by the light route, so not in `mine.tsv`); a retype replaces the whole page
      with `la_retype.py`. The pages of batch 5 that could be put right were rebroken at the
      printed line ends and checked in the image (0479 0502 0537 0540 0550 0568 0578 0590),
      and `æ` made `e` where printed so (0490 0504 0506 0507 0541 0543 0568 0578); the
      preamble pages 0479–0486 are printed wide (lines up to about 83 characters).
    - Batches 4 and 6, queued 2026-10-25 (the same audit, after they were written): 0350
      0403 0404 0413 0415 0447 0449 0454 0455 0464 0470. Lines run together where
      Tesseract reads across the two columns, so the rebreak cannot be checked against it
      (0413, 0447, 0449, 0454, 0455; 0464 an essay page); a printed line lost (0404 `vene
      esset cum rege Frantie, quod quidam miles venit ad`) or a paragraph lost (0470, after
      `de In-`). The rest was put right and written (174 `fixes.tsv` rows): letters kept by
      the light route (0400 also two half lines lost, `monitus ut`, `ravit. Iste habebat`),
      run-together lines rebroken at the printed line ends (0349 0351 0361 0366 0368 0400
      0411 0417 0421 0432 0434 0441 0443 0453 0461 0462 0465 0469 0473 0658; every changed
      line's first and last words checked against Tesseract's line, the rest in the image),
      words invented by `ocr/la` on the essay pages (0440 `la più` for `con sublimità`, 0429
      `Assisa la` for `Assoluto padrone della`) and their accents, and `æ` made `e` (0433
      0439 0450 0454 0614 0628 0634 0642 0653 0657 0681 0719).
    - The 38 pages queued for batches 4 and 5 above are retyped early (2026-10-25, before
      item 9, superscript kept) by la-el-agy in one task (retype 40), while batch 8 goes on.
      Added to `tmp/la-mark7` by way B and written: 262 places against the two OCRs, about
      150 crops; 62 fixes. la-el-agy opened apostrophe gaps where none is printed (24:
      `che'l`, `E'l`, `Va'via`, `de'tristi`), wrote `;` for a printed `:` (8) and commas
      where none is printed (2), normalized spellings (`decomes`, `impullerunt`,
      `amplexebatur`, `permicteret`, `montanea`, `guiucti`, `[s]fresiatur`, `reclausa`,
      `Conscentie`, `loquutio-`), dropped an accent (0464 `più`) and put four page numbers
      after the running head (0525 0527 0529 0539). No line lost (`la_lostcheck.py`: none
      in both OCRs); `la_check.py` 349–609 clean. Done, but for steps 8 and 11 with the
      batch.
    - Batch 8's broken pages, retyped early in the same way while the batch goes on: 0849
      0853 0854 0855 0858 0860 0861 0864 0866 0869 0879–0887 by la-el-agy2 (retype 41),
      added to `tmp/la-mark7` by way B (written with batch 8): 194 places, about
      110 crops, 29 fixes (`;` for a printed `:` 3, apostrophe gaps 12, `quì`, `resultante`,
      `appetiit`, `Eufraten`, `pescatore`, `Seraphin` for printed `qui`, `risultante`,
      `appetivit`, `Eufratem`, `peschatore`, `Seraphim`). It read the printed misprints
      `çondocti` (0853) and `iunocente` (0887) right, and the invented sentences of
      `ocr/la` on 0855 and 0879 as printed. `la_lostcheck.py`: none in both OCRs. 0891–0900
      0904 0905 sent to la-el-agy (retype 42, 2026-10-25). Added to `tmp/la-mark7` by way B
      (written with batch 8): about 170 places against the two OCRs, about 70
      crops, 45 fixes: apostrophe gaps opened where the print has none (15: `de'mortali`,
      `a'rivi`, `fa'che`, `ch'e'tre`, `ne'cieli`, `e'l` …), letters changed (`drieto` for
      printed `dirieto` twice, `rifonde`, `sarebbono`, `nebule` for `nubecule`, `[ttat:` for
      `[ctat:`), an apostrophe added (`ch'e'` for `ch'e`), a colon for a printed semicolon,
      a comma added, gloss dashes written `--` (6), gloss marks tight to their words (4) and a
      `(¹⁴),` for the broken `(¹⁴,`, a backtick at a line end, tercet numbers broken in
      print (0895 `²⁴`, 0905 `⁵`) written as the digit seen, and blank lines where no rule
      is printed (11, on 0891 0898 0904 0905). It read the printed misprints `omuium`,
      `similitudiue`, `luua`, `callefecit` and the repeated `(²²)` right, the gloss line of
      0892 that `ocr/la` had renumbered, and the lines `ocr/la` had lost or garbled (0895's
      Latin verse, 0897's, 0905's right column) in order. `la_lostcheck.py`: none in both
      OCRs. Sent to la-el-agy2 (retype 43,
      2026-10-25): 0909 (the left commentary column lost, the page number missing), 0915
      (verse indented, lines lost), 0916 (the running head inside the text, `ae` spellings,
      plain tercet numbers), 0918 (sentences rewritten: `Luna pallos`, `Iuno castos`; line
      ends moved), 0920 (a paragraph written twice), 0926 (two paragraphs lost), 0927 0929
      (commentary run together and garbled), 0928 (every rule lost, three half lines lost).
      Added to `tmp/la-mark7` by way B (written with batch 8): 60 places against
      the two OCRs, about 45 crops, 7 fixes (apostrophe gaps 4: `e 'l`, `Se 'l`, `contr'al`,
      `c' hai`; `textus:` for a printed `textus.`; `faceret` for the printed misprint
      `faccret`; a blank line where no rule is printed). It read the printed `dammas`,
      `sompniorum`, `exsitente`, `satisfatione` and `quómodo` right, and the commentary
      that `ocr/la` had lost or garbled (0909's left column, 0927's right column) in order.
      `la_lostcheck.py`: none in both OCRs. Sent to la-el-agy3 (retype 44, 2026-10-25): 0937 (line ends lost, words changed: `vigintiduas`,
      `defendebant`; `Final Paragraph (Prose):` in the text), 0938 (the running head lost,
      line ends lost, `Albæ, Iulius Silvius`, `filius Ascanio`), 0939 (line ends lost, lines
      garbled), 0942 (the running head inside the text, a line lost, `fuit fuit`), 0943
      (commentary run together and garbled: `con- suleas`, `stuolum`), 0945 (paragraphs out
      of order, a line lost, `portavereunt`, `vadeunt`), 0946 (words lost inside lines,
      `Meridius`, `adhortar`), 0951 (lines broken at other places than in print, words
      changed: `de uno, scilicet cum uno visu`), 0952 (words changed: `mandatum` for
      printed `preceptum`, `Galatus`), 0953 (lines garbled, `differeniter` for printed
      `diversis respectibus`), 0956 (two paragraphs lost at the top of the right column),
      0957 (lines left out as `[...]`), 0959 (an essay page, sentences rewritten). Added to
      `tmp/la-mark7` by way B (written with batch 8): about 90 places against the
      two OCRs, about 60 crops, 11 fixes and the indentation: the second and third verse
      lines indented (137 lines on 0946 0951 0952 0953 0956 0957) and a gloss line started
      with a space, apostrophe gaps (`e 'l`, `chi 'l`, `se 'l` where the OCRs agree on none;
      `tutt'el` for the printed `tutt' el`), letters (`effuderunt` for `effunderunt`,
      `pubblico` for `pubblicum`, `farìa` with an accent not printed), a word lost (`patuit`),
      a comma for a printed period before a capital (`cooperante.`), the printed misprint
      `fuitvel` spaced, and a blank line at a column change with no rule (0946). It read
      `Scippio`, `sotiis`, `transcucurrerunt`, `amasia .` and the nine dots of 0959's
      quotation right, and the text `ocr/la` had lost or garbled (0939's `sibi omnes quot
      potuit`, 0956's and 0957's right columns, 0959's `dopo il peccato` line) in order.
      `la_lostcheck.py`: none in both OCRs. The rest of
      the batch's pages are decided and fixed (0954 0955 0958; 0960 is blank).
    - Batch 9's broken pages (2026-10-25/26), retyped in the same way and added to
      `tmp/la-mark7` by way B (written with batch 9). Each retype had its lines there and in
      order; the places not as printed, put right from the image:
      - la-el-agy, retype 45 (0964 0975 0977 0980): 4 (commas left out at line ends 3,
        `trigiuta` for printed `triginta`).
      - la-el-agy2, retype 46 (0963 0965 0967 0969 0970 0971 0979): 25, most apostrophe
        gaps opened where none is printed (20: `Vid' io`, `l' alta`, `Che 'l`, `vegg' io`,
        `com' ogn' altra`, `Vuo' tu`, `a' generanti`), the printed misprint `cautatur`
        corrected, `sermocinandam`, an accent added (`Sydonís`), a comma left out.
      - la-el-agy3, retype 47 (0981 0983 0985 0991 0993 0997–1000): 9 (`Alcide` for printed
        `Alcyde`, a backtick at a line end, apostrophe gaps 4, commas 3).
      - la-el-agy, retype 48 (1002 1003 1004 1008 1009 1011 1013 1014 1017–1020): 16 and two
        gloss lines moved under the Italian block (1019 1020): periods for commas (4),
        apostrophe gaps (4), accents added (1008 `dì`, `può`, `però`; 1013 `Sì` for printed
        `Si` twice),
        `paralelli` for printed `parallelli` (2), a colon for a semicolon, a stray `'`.
      - la-el-agy2, retype 49 (1021 1023 1027 1028 1030 1031 1033 1035 1038 1039): 12
        (`Bonaventura` for printed `Buonaventura`, the misprint `palec` corrected, commas 5,
        spaces before `:` and `?`), and gaps after truncations where the print has none
        (5: `ne'concordi`, `de'sillogismi`, `da'romani`, `ne'quali` twice, `fe'subito`;
        three of them first opened in the check by mistake, closed on re-check). It read `atfetto`, `admiuistrat`,
        `planctata`, `deila`, `iuce`, `sapïenza` right.
      - la-el-agy3, retype 50 (22 pages): 1045's Latin verse 40–42 written as a translation
        of the Italian (`giga et cithara`, `una melodia`, `de alta laude`, `Resurge et
        vince` for printed `gyga et harpa`, `unum melos`, `dulcis laus`, `Surge et vincas`;
        8 lines retyped from the image), as on 1247; 1042's tercet numbers all left out and
        a gloss mark tight to its word; spellings (`Aldagheriis` 2, `nobiltà`,
        `Annuntiatione` 2, `solempnio-`, `Baronii`) and printed misprints corrected
        (`mansuetus`, `alla` for printed `mansuctus`, `alia`); `;` for a printed `:` (7);
        commas (3); apostrophe gaps opened where none is printed (5) and closed where one
        is (3: 1042 `m' accors'`, `Agl' ochi`, `Ch' è`), and 19 gaps after truncations
        opened where the print has none (`de'più`, `que'lumi`, `de'venti`, `se'tu`,
        `ne'ritrosi` …); `Sì` for printed `Si`; a dot line short of its 13 dots; blank lines
        around 1062's `que incipit` quotations (6, dropped); 1044's figure written
        `[figure]` with its four `q` (a blank line put before it). It read the left column
        of 1045 that `ocr/la` had lost, and `vincto`, `spechio`, `Vechio`, `Ucillatoio`,
        `lictora`, `contitetur`, `niveitate`, `'ci` right.
    - Batch 10's broken pages (2026-10-26), all by la-el-agy, retyped and added in the same
      way (written with batch 10). The check against the OCRs flags passages "missing" where
      a retype orders the lines differently from `ocr/la`; each such flag was looked up in
      the file, and only the losses below were real.
      - retype 51 (27 pages, 1074–1138): about 35 apostrophe gaps where both OCRs read
        otherwise (most opened, five closed: 1103 `suo' voler`, 1105 `ch' asseta`, 1111
        `Ond' io`, `agl' angelici`, `com' al`), 15 spaces before `:` or `;`, about 10 `:`,
        `;` or `,` where both OCRs read otherwise; 1076's Italian verse 9–12 rewritten after
        the Latin (`sarebbe`, `in che`, `per chiare`, `del suo proprio` for printed `saria`,
        `in chi`, `con chiare`, `nel suo chiaro`; its gloss mark lost); printed misprints
        corrected (`fortuniam`, `queta`, `cicli`, `substinuit`, `reefficitur`, `reflexe)`,
        `deheret`, `senti`); punctuation and gaps from the image (`concepisti:`, `Dei:`,
        `gaudio:`, `venenum:`, `che'l`, `come'l`, `se'in`, `sic[ut]`); the first line of both
        commentary columns of 1091 lost (put back from the image); the Latin tercet numbers
        1117 `⁴³` and 1133 `⁹` left out; four gloss marks tight to their word. It read
        `Chiesa militante` (`ocr/la` had `Ecclesia`), `coctidie`, `millesmo`, `redentionem`
        right.
      - retype 54 (19 pages, 1146–1183): blank lines between all the tercets of 14 pages
        (134, dropped); spellings modernized (1146 `restrinse`, 1157 `subiunxe`,
        `trascorsa`, 1178 `svegliato`, `abborre` for printed `ristrinse`, `subgiunxe`,
        `transcorsa`, `sveglato`, `abbhorre`; 1180 `Senz'` for `Senza`); printed misprints
        corrected (1177 `respondidisti`, 1169 `noritia`, 1166's gloss `die quid`) and one
        invented (1174 `tili` for printed `fili`, reported as a misprint); accents added (1161
        `mirò`, 1177 `udì'`, 1183 `dì più`); 1157's gloss `m'ha` for `m'he`, 1181 `EL` for
        the small-capital `El`, 1161's dot line short of its 16 dots; `;` or `,` for a
        printed `:` or `.` (4); apostrophe gaps (7) and punctuation (5) where both OCRs read
        otherwise. It read `argomento`, `pubblicationem`, `necessità`, `cosi`, `piu` (the
        OCRs had them otherwise), 1159's `fecit`, and the verse and commentary that
        `ocr/la` had out of order or lost on 1154 and 1166, right.
    - Batch 11's broken pages (2026-10-26), by la-el-agy, retyped and added in the same way
      (written with batch 11); after retype 54 each task named the last retype's errors.
      - retype 55 (1199 1200 1201 1203): one error, 1201 `contempor` (twice) for printed
        `contemplor`. 1199's broken `circu't` written `circuit` (the convention).
      - retype 56 (1217 1227): 1227 `fluminum` for printed `fluminorum`, 1217 `Com'a'
        Giuderi` for the tight `Com'a'Giuderi`.
      - retype 57 (1258 1262–1267, canto XXXIII): one error, 1265 `igualmente` for printed
        `equalmente`.
      - retype 58 (the ten *Fragmenta* pages, commentary only): one error, 1284 `Bentro`
        for printed `Dentro` (reported as a misprint). 1276's `mine` with a mark like an
        accent over the `e` (a Latin word) written without it.
      la-el-claude's 17 retypes of batch 11 were checked only by itself (`cmp` with `out/`,
      the scripted checks, the accent check against Tesseract).
    - **Steps 8 and 11, batch by batch** (from 2026-10-27; `la_lines.py` writes
      `WORK/lines.txt` over the batch, the hits are looked at in the image and `ocr/la` is
      edited directly):
      - **Batch 4** (0349–0478): done, `texts/la/031`–`041`. Step 8: blank lines at 14
        printed rules (most of the `NO BLANK` and `?` hits were page-end rules or lines
        matched in the other column: a hit counts only when no blank line follows the line
        within three lines, looked up by a scratch filter), 44 dots before a lowercase word
        made commas, run-together or shifted lines rebroken at the printed line ends (0351
        0416 0418 0424 0429 0444 0456 0475 0476), words lost put back (0412 `; ita unus
        alchimista appodiatur`, 0471 `per quem ego`), letters (0412 `Ymum`, 0418 `felix`,
        0426 `Leppo`, 0465 `tunc`), 0423's broken gloss mark `(1)`; page heads: page numbers
        added on 7 pages whose number had been lost (0368 0425 0434 0436 0450 0457 0459),
        the blank line after the number on 4, the running head on 0406 and 0416. Step 11
        found: 0402's running head repeated before the Latin verse (removed, as 0249), 0417's
        Italian tercet numbers `45`, `46` lost, the hyphen joins `ad per-`/`tenebram` (0469,
        printed `ad perpetuam`), `peregri-`/`sotii` (0473, `peregrini`), `ani-`/`gentem
        fascias` (0459, `aliam`/`gentem fasciat`), `actor` for printed `ctor` (0433, after
        `au-` on 0432), `sequ[en]ti` for printed `sequ[ent]i` (0412), and **blank lines
        inside a sentence at a column change** (24 pages; a blank line after a line-end
        hyphen or before a lowercase line), which `la_lines.py` now lists (`# blanks`).
        The same check over batches 1–3 found 16 more in batch 3 (removed, `texts/la/021`–`027`
        regenerated) and 0252's left-column end set after the right column (moved).
        Kept as printed: the gap after `que incipit ibi:` before the quotation on 0362, 0410,
        0443, 0466 (a section gap, as 0258); `convert_la.py` now takes the printed `3` of
        0350 (Suspected misprints) without an error.
      - **Batch 5** (0479–0609): done, `texts/la/042`–`053` (the preambula with the
        PURGATORIUM half-title 0477, cantos I–XI; 0609, canto XII's *Summarium*, goes with
        batch 6). Step 8: 0523's commentary retyped from the scan (the end of the left column
        lost, the right column's text there garbled, the page number inside the text;
        `la_lostcheck.py` had not listed it, the words being in the verse), 37 blank lines
        inside a sentence removed, a blank line at the rule on 0548, 42 dots before a
        lowercase word made commas, lines rebroken (0489 0506 0519 0547 0559 0576), page
        numbers added on 9 pages, running heads on 0481 0495 0502. Step 11 found: 0585's
        tercet 48 unnumbered in both columns (a page without a number is not read as verse),
        and from the hyphen joins 0533 `vixis-`, `Po-`/`testate`, 0559 `voluntatem`, 0575
        `nigerri-`/`mus`, 0595 `dubi-`/`tavi`. `convert_la.py` reads the tercet in printed
        brackets of 0545 (`[7 Vidi`).
      - **Batch 6** (0610–0728): done, `texts/la/054`–`063` (cantos XII–XXI). Step 8: text
        lost in `ocr/la` put back from the scan: 0617's left column of the commentary (22
        lines, `ternus et doga` … `clinati.`), 0639 six lines (`oriebantur questiones` …
        `Tangatis de istis annulis quem vultis`), and in batch 5 a line of 0547 (`facere quis
        se stallat`); found by `la_lostcheck.py -n 5`, keeping the runs of real words (those of
        Tesseract alone too, which the default report passes over); 32 blank lines inside a
        sentence removed, blank lines at 0636's rule and after 0706's quotation, 40 dots
        before a lowercase word made commas, lines rebroken (0616 0633 0662 0728), 0610's
        broken gloss mark `(3)`. Step 11 found: 0622's commentary run into the Latin verse
        block (a blank line added), 0655's two-line essay title split by a blank line
        (joined), and from the hyphen joins 0659 `ad`/`cecos` (no hyphen printed), 0651
        `so-`/`pite`, 0621 `querebat`. `convert_la.py`: essay titles with a comma (0703),
        runover lines of three words (0663 `[in sua cura.`, 0696 `[Surge et veni,`), 0710's
        misprinted running head `PURGATORI`.
      - **Batch 7** (0729–0846): done, `texts/la/064`–`073` (cantos XXII–XXXI). Step 8: 6 blank
        lines inside a sentence removed, blank lines at the rules on 0744 and 0829 (0744's not
        listed by `la_lines.py`, found by `la_check.py -v`: a rule count above the blank lines
        not explained by a page-end rule), 21 dots before a lowercase word made commas, 0746's
        paragraph rebroken at the printed line ends; `la_lostcheck.py -n 5` found no run of
        real words. Step 11 found, from the hyphen joins: 0813 `se-`/`totaliter` (no hyphen
        printed), 0745's lemma `fo-`/`gabat` (a damaged `r` with an ink spot; the verse has
        `rogabat`), 0773 `sim-`/`beleggiate` (printed so, Suspected misprints).
        `convert_la.py`: no new case; 0736's gloss printed on three lines is joined as one.
      - **Batch 8** (0847–0960): done, `texts/la/074`–`082` (Purgatorio XXXII–XXXIII, the
        PARADISUS half-title 0871 and Paradiso I–VII). Step 8: 7 blank lines inside a sentence
        removed, a blank line at the rule on 0883, 24 dots before a lowercase word made commas
        (0932 `celi), de lumine, quod`), 0932's doubled dot `terram..`; `la_lostcheck.py -n 5`
        found no run of real words. Step 11 found, from the hyphen joins: 0935 `vi-`/`ctoriarum`
        (`ocr/la` had `ctariarum`), 0877's gloss `con-`/`templationem` (`ocr/la` had
        `temptationem`), 0958 `complexio-`/`conibus` (printed so, Suspected misprints).
        `convert_la.py`: the Paradiso (`PARADISI`, files from `076`), the half-title 0871 at the
        head of canto 1 (its signature mark `103` removed) and `INCIPIT PARADISUS` above the
        *Summarium* of 0873; 0868's `FINIT FELICITER PURGATORIUM.` and `EXPLICIT PURGATORIUM
        DANTIS.` under the two verse columns, and the scribe's verses (`Qui scripsit scribat`)
        kept line by line with their gloss line.
      - **Batch 9** (0961–1072): done, `texts/la/083`–`091` (Paradiso VIII–XVI). Step 8: 9 blank
        lines inside a sentence removed, 21 dots before a lowercase word made commas; no rule
        without its blank line, no line rebroken; `la_lostcheck.py -n 5` found no run of real
        words. Step 11 found, from the hyphen joins: 0994 `ad-`/`vocationibus` (`ocr/la` had
        `dibus`), 1053 `ven-`/`turum` (`tutum`), 1052 `intelle-`/`xisse` (`intel-`), and two
        printed so (Suspected misprints): 0999 `volupta-`/`bro`, 1031 `corrupti-`/`lium`.
      - **Batch 10** (1073–1184): done, `texts/la/092`–`101` (Paradiso XVII–XXVI). Step 8: 12
        blank lines inside a sentence removed, blank lines at six rules on 1129 (it had none),
        44 dots before a lowercase word made commas (14 on 1175, whose comma tails are lost
        throughout), 1171's run-together line rebroken, 1124's page number added;
        `la_lostcheck.py -n 5` found no run of real words. Step 11 found: 1167's running head
        set before its page number, so that its verse was not read (tercets 18–24 of canto
        XXV missing), and 1051's page number lost (read as a second canto heading); the page
        heads of a page with `CAPITULUM …` on its first line are now checked as well (none
        else in batches 7–10). From the hyphen joins: 1135's lemma `sen-`/`bianza` (printed
        so, Suspected misprints).
      - **Batch 11** (1185–1296): done, `texts/la/102`–`110` (Paradiso XXVII–XXXIII, the
        appendix and the index). Step 8: 14 blank lines inside a sentence removed, blank lines
        at five rules on 1194 and two on 1215, lines rebroken (1195 1204 1205), 1216's runover
        `[posita` set after its line (`pos-`) and its running head added, the page number set
        before the running head on 1281 1283 1285, the page-foot notes of 1274 and 1282 moved
        after the right column (they cut a word in two); `la_lostcheck.py -n 5` found no run of
        real words. Step 11 found: **1202's Latin verse missing** (tercets 24–29, transcribed
        from the scan; `la_check.py` does not see a column that is wholly missing, the
        conversion does), 1207's tercet number 46 lost in both columns (the canto's last
        tercet), and from the hyphen joins 1215 `reme-`, 1194 `dinaverunt`, 1222
        `vigintiqua-`/`tuor`, and 1264 `mi-`/`mium` (printed so, Suspected misprints).
        `convert_la.py`: figures (1044, 1245, 1247) with their labels line by line, the
        scribe's verses on 1268, and the appendix (`109-appendix.md`: the half-title, the
        headings `INCIPIT TERTIA CANTICA …`, `CANTUS II PARADISI`, `CANTUS TERTIUS`, the two
        notes as footnotes) and the index (`110-index.md`, one entry per line as printed).
      - **Front matter** (0001–0078): done, `texts/la/001`–`007`. Step 8: one dot before a
        lowercase word made a comma (0025), 0049's `(Ibid.)` joined to its printed line; no
        rule, no lost run of real words. Step 11: `convert_la.py` reads the Roman page numbers
        and the title pages line by line (no new fix in `ocr/la`); the INFERNUS half-title
        0077 is put at the head of canto 1 (`008`), as 0871 for the Paradiso, where
        texts/PLAN.md had listed it with the preambula (`007`).

Also seen: 0848, 0891 and 0999 had backticks in the text (0891 around its blocks,
`` `Quei gloriosi …` ``); gone since their retyping.

## Procedure for a batch

Below, FIRST–LAST is the batch (e.g. 233–348), PAGES its pages without the blank ones
(their file reads `[Blank page]`; batch 3 has 0244, 0256, 0268, 0280, 0292, 0326, 0348):

```sh
PAGES=$(for n in $(seq FIRST LAST); do p=$(printf %04d $n); grep -qx '\[Blank page\]' ocr/la/$p.txt || echo $p; done)
```

WORK is the batch's work directory (`tmp/la-markN/`, a new N per batch), TESS =
`ocr/la/tesseract`. Paid calls are run by the user: give them the command, and test with
`--fake` first. Python is run with `uv run`.

1. **Verse**: done over all pages at once for 0233–1296 (Remaining work, items 1–2).
   `ocr/la_survey.py --work FIRST LAST` lists the pages whose Italian or Latin column is
   missing or whose numbers are wrong (it has false positives: "Record of the preparation"). Batches 1–2 were
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
5. **Routes**: `uv run ocr/la_markresolve.py WORK -t TESS -p FIRST LAST` writes
   `WORK/review.tsv`, the marks left to la-el-claude. `-p` keeps route.tsv, review.tsv,
   `WORK/out/` and `--write` to the batch's pages (needed when WORK holds more pages than
   the batch, as `tmp/la-mark7`); `mine.tsv` and `fixes.tsv` are keyed by page and hold
   every batch's decisions.
6. **Review** every line of `review.tsv` into `WORK/mine.tsv` (`page line k decision note`;
   decision `left`, `right` or `text:…` with `⏎` for a line break) and corrections outside
   the marks into `WORK/fixes.tsv` (`page old new note`, the old text as in `WORK/out/`).
   Views: `ocr/la_view.py next WORK [N] -o OUT.png` (the next N marks not yet in
   mine.tsv: their crops and contexts), `context WORK [CLASS]` (each mark in its text),
   `review WORK PAGE:K,…` (the crops), `word TESS PAGE:REGEX` (a place the crops missed).
   Decisions go in with `uv run ocr/la_mine.py WORK PAGE K[,K…]=DECISION[|NOTE] …` (the
   line from review.tsv; a mark already decided stops it). A page too broken for its
   marks: decide them all `left`, rerun step 5, retype the page from the scan and add
   it with `uv run ocr/la_retype.py WORK PAGE FILE NOTE [--old PART]` (one fixes.tsv
   row replacing the page, or the part in PART). The rules,
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
   - small capitals in uppercase, plain-digit tercet numbers and gloss marks, broken words
     joined on essay pages: the conventions below, whatever the model says.

   **Two ways of doing step 6**, both used on batch 3. Choose one with the user at the
   start of each batch. The work goes in parts of about 20–25 pages, with a report to the
   user after each part.

   - **A. All by la-el-claude** (batch 3: 0233–0275, about 820 marks). Every mark is
     decided as above, in its crop. A page too broken for its marks is retyped from the
     scan by la-el-claude and added with `la_retype.py`. In 0254–0275 that was 10 pages out
     of 20: the old OCR there runs lines together, drops lines and words, and mixes columns
     and page heads. What it gives: every mark is seen, and no delegate errors need
     checking. What it costs: all the image work falls on la-el-claude, and broken pages
     are slow.
   - **B. Pages retyped by la-el-agy** (batch 3: 0276–0347, retypes 19–21). Each page of a
     part is retyped whole from the scan by la-el-agy ("Whole pages" in
     [DELEGATION.md](DELEGATION.md)), and la-el-claude checks the result:
     1. **Task**: `tmp/herdr-task-retypeNN.md`, made from
        [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md) (its comment says what to fill in; add a
        new kind of error from the last retype to the template too). It holds the
        rules of "Whole pages", the list of pages, the output directory
        `tmp/la-retypeNN/agy/` and the report file `tmp/herdr-report-retypeNN.md`. It
        gives feedback on the previous part's errors, with examples. It forbids
        subagents, git changes and shell redirects. Send it with `herdr agent prompt`;
        send nothing more until the reply comes.
     2. **Copy**: put each page into `tmp/la-retypeNN/final/`, with leading spaces
        stripped (la-el-agy indented verse lines in retype 20).
     3. **Compare** each page word by word with `ocr/la` and GLM-OCR, by a script
        ("Checking a batch" in DELEGATION.md). It joins hyphenated words and runovers,
        then lists the words of la-el-agy found in neither reading. It also lists the
        passages that both readings have and la-el-agy lacks: a lost line (0313).
     4. **Decide in the image**: drop the hits that are only tercet or page numbers. Crop
        the rest: for each hit, the Tesseract line most like la-el-agy's line. Look at
        each crop, and zoom with `la_view.py word` where needed. A `.`/`,` difference goes
        by the comma rule, also where the image shows a round dot (retypes 20–21 forgot
        this: 30 places turned back to commas). A `:`/`;` difference or an apostrophe gap
        takes the reading of the two OCRs when they agree.
     5. **Fix**: write the fixes as a script of asserted replacements (page, old text,
        new text, count) and apply it to `final/`.
     6. **Add to WORK**: for each page, decide all of its marks `left`
        (`K=$(awk -F'\t' -v p=$P '$1==p{print $3}' WORK/review.tsv | paste -sd,)`, then
        `la_mine.py WORK $P "$K=left|retyped by la-el-agy (retypeNN)"`). Resolve
        (step 5). Add each page with `la_retype.py WORK $P final/$P.txt NOTE`, resolve
        again, and check that `WORK/out/$P.txt` is the same as `final/$P.txt` (`cmp`).
     7. **Then steps 7–11**, as for A. Also look for what the comparison does not catch:
        - an essay page kept as one line per paragraph but retyped line by line (0347);
        - a runover placed after the wrong verse line (0312);
        - a running head repeated inside the page (0249).

     Measured on batch 3:

     | Retype | Pages | Marks | Hits looked at | Fixes |
     |---|---|---|---|---|
     | 19 | 21 | 410 | about 130 | 25 |
     | 20 | 24 | 482 | about 136 | 36 (one lost line) |
     | 21 | 24 | 454 | 99 | 28 |

     la-el-agy read many places right where both OCRs were wrong, and it put columns and
     page heads in order. The same kinds of error came back part after part ("What
     la-el-agy got wrong" in DELEGATION.md):
     - dots and commas, colons and semicolons;
     - spellings normalized;
     - apostrophe gaps;
     - indentation;
     - one lost line.

     What it costs: la-el-agy's time, plus about 100–160 crops per part for la-el-claude,
     instead of the 400–500 marks of a part decided by A. The words that la-el-agy and
     both OCRs read alike, and wrongly, are not checked. A has the same limit.
7. **Resolve**: rerun `la_markresolve.py WORK -t TESS -p FIRST LAST` until `review.tsv` is empty; read the
   word diff of `WORK/out/` against `ocr/la` (every change must be one decided above; a dot
   taken from the image before a lowercase word is a comma, 0127). Before `--write`,
   audit what the light route kept (below); then add `--write`.

   **Light-kept marks.** `--light` keeps `ocr/la` for most open letter marks, and `ocr/la`
   holds normalized or invented spellings (`solemni` for printed `solempni`, `Constantiæ`
   for `Constantiam`, `continuavit` for `continuit`), so these pass unseen. Batch 7 had 18
   such places in 0729–0808 and, rechecked with the steps below, one more letter (0744
   `carnium`), four run-together lines and one accent, batch 5 had 17 letter fixes in 0479–0609, batches 4 and 6
   about 50 together (found 2026-10-25, after they were written). Batches 1–3 (0079–0348) ran
   without `--light`, every mark decided by hand: there only the essay pages' accents were
   wrong (23 places on 9 pages, `ocr/la` and `texts/la` corrected 2026-10-25); no lines run
   together and no `æ`.
   - `route.tsv` holds only the last `-p` range: resolve the batch's range first.
   - List the letter marks the light route kept:
     `awk -F'\t' 'NR>1 && $4=="letters" && $8=="left" && $7=="light"' WORK/route.tsv`.
     Column 9 is the model's reading: `left '…'` agrees with `ocr/la`; take the rows
     where it is `neither`, `wrong place` or `unreadable`.
   - Drop the rows whose `ocr/la` text (column 5) is no longer in `WORK/out/PAGE.txt`
     (already decided otherwise, or the page retyped). Crop the rest in the image
     (the out line nearest the mark's line, or the Tesseract words) and correct what is
     not as printed in `fixes.tsv`.
   - Essay pages carry almost no marks, but `ocr/la` adds or drops accents there
     (`volontà`, `sarà`, `può`, `dì` for printed `volonta`, `sara`, `puo`, `di`; on 0508 the
     reverse, `proprieta` for `proprietà`). Align each out word with Tesseract's words, list
     those whose accents differ from Tesseract's, and crop them. `ì` against `i` (`sì`,
     `così`) and the direction of a grave or acute accent are at the edge of the scan's
     resolution: correct only clear cases. List the other word differences too and look at
     those where Tesseract reads a real word: `ocr/la` also rewrites phrases there (0440
     `fu redenzione … dottrina la più inarrivabile` for printed `fu redentore … dottrina con
     sublimità inarrivabile`).
   - Lines over 72 characters outside the glosses are lines run together, with the line
     ends around them shifted. Rebreak the paragraph at Tesseract's line ends only where
     Tesseract reads the column by itself; check each changed line's first and last words
     against Tesseract's line, and the paragraph in the image where it does not match. Queue
     the page for a retype (item 10) where Tesseract runs the columns together.
   - Resolve again and check that `WORK/out/` changed only on the corrected lines.
8. **Lines**: `uv run ocr/la_lines.py FIRST LAST -t TESS -o WORK/lines.txt` and look at each
   hit in the image (`la_view.py strip PAGE:Y` for rules, `word` for the others):
   - `# rules`: a rule needs a blank line after the line above it (see the blank-line
     conventions); `?` hits are mostly page-end rules (not written) or a short last line
     matched one line too early;
   - `# breaks`: a printed line broken in two; join it;
   - `# dots`: make the dot a comma unless it ends an abbreviation (`i.`, `al.`, `GEN.`,
     `Purg.`) or a sentence;
   - `# blanks`: a blank line inside a sentence, mostly at a column change: remove it
     (verse blocks ending before the commentary, quotations and page-end signature marks
     are listed too);
   - also blank lines at quotations (before or after, per the conventions), at column
     changes without a rule, inside essay quotations: look at the pages with indented
     quotations;
   - page heads (number, blank line, running head) and the hyphen joins that `convert_la.py`
     reports (`HYPHEN`): a join that makes no word often shows a lost or misread word;
   - lines over 68 characters (gloss lines and essays with a paragraph per line aside),
     broken where Tesseract breaks them, and a hyphen line end before a blank line (normal
     only before a page-end signature mark);
   - `la_lostcheck.py FIRST LAST -t TESS -n 5`: look at the runs of real words, those of
     Tesseract alone included (batch 6 found two lost passages that way).
9. **Final checks**: `la_check.py FIRST LAST` (tercets and rule counts; known exceptions:
   0100, 0131, 0165, 0545); page heads (page number, blank line, running head; add missing
   numbers and heads); no `æ`; `—` only in gloss lines; accents as printed; lines over 68
   characters outside essays and gloss lines (paragraph lines to break at Tesseract's line
   ends).
10. **Commit**: the pages (`ocr/la`), the scripts if changed, then PLAN (this file: State,
    "History", misprints, any new convention), each as its own commit.
11. **Texts**: extend `texts/convert_la.py` to the batch's cantos (its output files and
    checks), run it, read its reports (`NO NUMBER`, `RUNOVER`, `HYPHEN`), update
    texts/la/README.md, texts/README.md and texts/PLAN.md; commit `texts` separately.

## The method: two-OCR markup, then image decisions

`ocr/la` (Gemini 2.5 Flash) and GLM-OCR fail in different ways, so their disagreements point
to errors. Each disagreement is written into the page as `{{ocr|glm}}`: the `ocr/la`
reading on the left, the GLM-OCR reading on the right, one side empty for text found on one
side only. The text outside the marks is `ocr/la` unchanged, so resolving every mark to its
left side gives the page back exactly.

**Workflow** (the scripts in `ocr/`; WORK is a work directory in `tmp/`, TESS the directory
of Tesseract's `PAGE.tsv` files, `ocr/la/tesseract`):

```sh
uv run ocr/la_markup.py -m MODEL -o WORK/markup PAGE...   # paid: the marks
uv run ocr/la_markprep.py WORK PAGE... -t TESS            # steps 2-3: trivial marks, crops, ask.txt
uv run ocr/la_markdecide.py WORK -m MODEL                 # paid: the model's verdicts
uv run ocr/la_markresolve.py WORK -t TESS [-p FIRST LAST] # routes; review.tsv; WORK/out/
# la-el-claude decides review.tsv in the images into WORK/mine.tsv (la_view.py next,
# la_mine.py; corrections in WORK/fixes.tsv),
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
- 0195–0208 (model `gpt-6-luna`; these first answers were moved to `tmp/la-markup/bak/`):
  all 14 pages pass, 355 marks; 349 after the edits of commit 3 (re-checked with `-r 0`).

### Markup answers (`tmp/la-markup/`)

The paid answers are kept in one place, `tmp/la-markup/`, the latest set per page
(`NNNN.json`, `NNNN.rK.json`, `NNNN.txt`; the latest is the set whose newest file is
newest). A batch copies its pages from there into `WORK/markup/` (step 2) and, after new
calls, moves each new page back as a whole set: a page already in `tmp/la-markup/` is first
moved, all its files, into `tmp/la-markup/bak/`, so that older `.rK.json` files do not mix
with the new set.

On 2026-10-15 the user's markup of 0755–1296 was added (1234 pages), and the 386 pages
whose lines change with the verse were moved to `bak/`: 848
pages are left.

Consolidated on 2026-10-14 from the work directories of batches 1–2 and `la-markup/`:
0079–0754 (650 pages). The first answers for 0195–0208 went to `bak/`.

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
`gpt-6-luna`, 2026-10-13):

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
- **Later narrow tasks** to la-el-agy (2026-10-15–20: the verse, the gloss lines and the
  retyped pages, from the images alone, each batch checked by script): how they were
  written, their rules and its errors are in [DELEGATION.md](DELEGATION.md).

## Record of the preparation (items 1–7)

The state of the pages before the batches of item 8 (2026-10-14 to 2026-10-22): the
markup, the verse and gloss transcription, the model decisions. Items 1–7 of Remaining
work refer here.

- **Markup** (paid, by the user) done for every page (`0001`–`1296`, 1234 pages without
  the 62 blank ones). Re-checked with `-r 0` (in a work directory, since
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
  without the Italian and of 0836; the crops whose
  line counts differed were checked by la-el-agy and la-el-claude, and the script fixed
  (bottom lines lost, the Italian cut where the two columns overlap, 0625).
- **Markup answers to redo**: the pages whose lines change (386 pages: the
  337 without the Italian, 0836, and the 48 with a moved Latin block) were moved, all their
  files, into `tmp/la-markup/bak/`; `tmp/la-markup/` held the other 848.
- **Markup of the 48 pages with a moved Latin block** (paid, by the user, default rounds):
  re-checked with `-r 0`: 207 differences missed in 43 pages (44 spacing only); without
  0598, about 3–4 a page, as on the other pages (left to the extra round, item 5).
- **Italics written `*…*`** (Gemini's italics; the convention does not transcribe them):
  0598 had 53 commentary lines wrapped in `*…*`, and the model's entries removing a `*`
  could not be placed (two on a line). Every `*` was removed from `ocr/la` (114 pages, 475
  lines; only `*`, and a space left doubled or leading on two
  lines, 0569, 0691), except the printed ones: 1193 `* * *`, 1254 `Quia(*)`; and 0611
  `* Ego me moveram`, a misread tercet number (GLM-OCR `4`), left for the verse check.
  Their markup is redone: the answers of the 89 pages not already among the 386, and
  0598's second set (as `bak/0598-2.*`), were moved to `bak/`. The pages to mark were then
  475 (47 done, 90 ready, 338 after the verse).
- **Markup of the 90 ready pages** (paid, by the user, default rounds): re-checked with
  `-r 0`: 351 differences missed in 62 pages (132 spacing only), 72 entries not placed in
  38 pages. Most are on two pages: 1023 (82, GLM-OCR drops the space after punctuation)
  and 1277 (57, the two OCRs break and bound the text differently; 8 not placed; look at it
  after the extra round). 0598: 0 not placed (56 before the italics fix), 1 missed. No `*`
  entry is left anywhere. Left to the extra round, item 5.
- **Markup of the 338 verse pages** (paid, by the user, default rounds, 2026-10-18; 0831
  retyped instead, item 3): the answers of the 337 moved from their work directory
  (deleted when empty) into `tmp/la-markup/`. Re-checked with `-r 0`: 1011 differences
  missed in 284 pages (316 spacing only), 279 entries not placed in 162 pages; 102 are
  long blocks (a paragraph on one side only or out of order, 69 pages, most on 1191: 6;
  0309, 0779, 0882: 3), a sign that `ocr/la` may be broken there as 0831 was. Left to the
  extra round, item 5; look at the long blocks after it.
- **Extra markup round** (item 5, `-r 1` on the 1233 pages, paid, by the user,
  2026-10-18; no page refused): re-checked with `-r 0`: 2604 differences missed in 735
  pages (757 spacing only), 549 entries not placed in 316 pages. 0941: 3 missed (GLM-OCR
  misreadings), 1245: 2. The long blocks showed that `ocr/la` has **lost text** on many
  pages, as on 0831 and 0941: a word check found 164 pages where GLM-OCR has runs of 15+
  words that `ocr/la` lacks (24183 words; 95 pages over 100 words, 18 with verse lost).
  Seen in the image: 0907 (the left commentary column lost, and
  `vult beatos homines` written `que sunt beati homines`), 0940 (the Italian verse, the
  left commentary column and most of the last paragraph lost); 0709 has 356 words of
  GLM-OCR's 794. Retyped in item 6.
- **Model decisions** (item 7, done 2026-10-22) in `tmp/la-mark7/`, over 1083 pages
  (0001–0078 and 0233–1296 without the blank pages and 0831). Markup: the answers of
  `tmp/la-markup/` copied and re-checked with `-r 0`: no page failed, so no new paid
  markup; 2244 differences missed in 664 pages (2604 before item 6), 411 entries not
  placed in 254 pages (0048 and 0050 one each: their dot runs, fixed after the markup).
  `la_markprep.py -t ocr/la/tesseract` stopped on no page: resolved 10559 (number 4230,
  note 3458, quote 1570, head 785, spacing 195, moved 174, signature 88, google 59); left
  31272 (located 27828, unlocated 1537, ambiguous 800, order 725, word 382); 22141 to ask
  in 1070 pages. `la_markdecide.py -m gpt-6-luna` (paid, by the user; no question
  refused, no invalid answer): 22032 questions (identical marks share an answer), all
  22141 answered: left (`ocr/la`) 12794, right (GLM-OCR) 8097, neither 1133, wrong place
  101, unreadable 16.
- **Verse transcription, trial** (`la_verseread.py`, paid, by the user) on the Italian of
  the 121 checked pages, measured with `--check` against `ocr/la` (differences counted by
  word; "caught": GLM-OCR has the file's reading, not the model's, so the verse check
  would find it; "missed": GLM-OCR reads as the model):
  - First prompt, 5 pages: 9 wrong lines of 66, mostly the modern text of the poem
    (`havea→avea`, `aqua→acqua`, `diserta→deserta`, `ochi→occhi`) and `Sì→Si`. It also
    showed that 0085 `uscìa` had an accent the scan does not show (`940cfce`, now `uscia`).
  - Second prompt (warns against the modern text, asks for each accent), 121 pages: 334
    lines of 1755 differ; by word: letters 206 (165 caught, 16 missed), punctuation 55
    (41, 13), accents 32 (19, 9), tercet numbers 53. The model writes the modern spelling
    systematically: `gl`+vowel made `gli` (`figlo`, `vogla`), `ct` made `tt` (`decto`,
    `puncto`), single consonants doubled (`ochi`, `nochier`); `viddi→vidi`, `um→un`.
    Tercet numbers: the small superscripts are often misread, a run shifted on 0137
    (36→30); take them from the Latin column of the page when inserting.
  - Third prompt (the edition's spellings with examples), on the 20 pages with the most
    differences (their second answers in `read/bak/`, with `read/bak/check-v2.txt`):
    letters 94 → 62 (45 caught, 8 missed), punctuation 10 → 8, accents 3 → 4. `ct` and
    `gl` are still often modernized (`tucto`, `periglo`); the `viddi` example was
    over-applied (3 printed `vidi` read `viddi`). The prompt cannot hold the model off the
    modern text much further.
  - **la-el-agy** (the crops only, no text of the pages; [DELEGATION.md](DELEGATION.md))
    on 5 of these pages (0169 0188 0200 0202 0227, 111 lines): letters 0, punctuation 0,
    tercet numbers 0 (Luna, third prompt: 25, 1, 14); one accent, 0200 `dietrò`, which it
    reported itself as unsure (a speck above the `o`, not an accent: the file's `dietro`
    stands). Read independently: its apostrophe spacing and number forms differ from the
    file's.
- **Verse inserted** (Remaining work, items 1–2): batches 1–2 of
  la-el-agy, 50 pages (0237–0390, the first 50 Italian pages in page order), 920 lines,
  5 words not as printed, all found by the check and fixed: 0273 `Ch'havea` (`C'havea`),
  0284 `dirieto` (`dirietro`), 0378 `departii` (`dipartii`), 0378 `mornorando` and 0390
  `ninico` (`mormorando`, `nimico`: an `m` whose worn first stem it took for an `n`, with
  a stroke-width argument in its report). No accent, punctuation or tercet number wrong.
  Its notes of "unsure" or "measured" letters are not a sign of a right reading: look at
  them.
  Batch 3 (0397–0459), 25 pages, 495 lines: 2 not as printed,
  0404 a comma left out after `paura`, 0423 `[su` for the printed misprint `[sn`. Its
  report named a `d[e]lle` on 0397 that is in no file and no print: the report is not
  evidence. GLM-OCR reads a worn `e` as `c` (`ciclo`, `Ch'ci`, `mici`, `Briarco`): the
  scan's `Briareo` (0437) kept. Latin blocks: 0459 `52`–`58` for `32`–`38`; runover words
  not marked (0425 `[unciam,`, 0448 `[nanciam.`, `[maneat.`, misread as `nantiam`,
  `maneant`); 0459 `congeletur`; a blank line in the Latin block where the Italian has a
  runover line (0404, 0423, 0455, 0456, 0459). 0447's `[Et veniet semper, ex gelatis
  aquis].` is a whole line supplied in brackets:  `la_verseinsert.py` takes `[` followed by
  a lowercase letter as a runover, other `[` lines as verse; `la_check.py` still reports
  its tercet 25 off by one (known exception).
  Batch 4 (0468–0549), 25 pages, 466 lines: 4 not as printed,
  0501 `Rïvidil` (`Rividil`: a smudged dot on `i`), 0527 `mío` (`mio`: the same), 0536
  `calan do` (`calando`: a worn `d` bowl), 0539 `sopragjunto` (`sopragiunto`: a speck below
  `i`). Conversely, the printed grave accents on `0501` `càgion`, `0507` `andavàn`, `sà`,
  `0536` `Fàccianli` were rightly kept. Latin blocks: numbers added/fixed on 0494 (`28`–`33`),
  0514 (`19`), 0535 (`8`→`3`), 0539 (`47`–`50`→`27`–`30`); 0505 `Si[c]`, a stray blank line
  removed and `[cumque` added; 0527 `[facit.` moved before `31` and `_` stripped; 0535
  `[gnum.` added; 0536 `[raucum;` put on its own line and `[verterunt,` fixed; 0547 missing
  `vertice` added.
  Batch 5 (0551–0615), 25 pages, 499 lines: 4 not as printed,
  0557 `[perduto` and 0558 `[quante.` written inline at the end of the next line instead of
  on their own line after the line they continue, 0600 `nòi` (`noi`: an interlinear speck),
  0605 `Salvani` (`Selvani`). Printed grave accents on `0569` `Vèr`, `dèi`, `0580` `fòr`,
  `0589` `salivàmmo`, `0600` `ànno` rightly kept. Latin blocks: 0558 numbers `12`–`13` and
  missing `[me adhereo.` added; 0569 `[gradum,`, 0579 `[quantulum,`, 0593 `[me moveam:` put
  on their own lines; 0579 missing `incendium` (`ymaginatum`) added; 0589 broken line
  rejoined; 0601 `[transitus,` and `[est parcus.` fixed; 0605 `[explanas;`, `qui[a] fuit
  presumptuosus`, `[ausus.`, `Priusquam` fixed and 4 garbled commentary lines at the end of
  the verse block removed.
  Batch 6 (0616–0677), 25 pages, 467 lines: 2 not as printed,
  0617 `sospecciar` (`sospicciar`), 0634 `Si·sdebitò` (`Si sdebitò`: a work-up speck between
  words), plus missing spaces before/after gloss marks on 8 pages. Printed turned `n` on
  `0633` `iuver`, singular `0660` `fascia`, `0677` `ciascum`, and grave accents on `0617`
  `montavàn`, `0640` `sapevàn`, `0647` `andavàn`, `0674` `Procacciàn`, `porrìa`, `0675`
  `eravàn` rightly kept. `0639` `[L]a casa Traversara` starts with an inline bracket:
  `la_verseinsert.py` and `la_check.py` now take `[` without `]` as a runover (`0625`
  `[Santi.`) and `[` with `]` as verse (`0447` la, `0639` it). Latin blocks: numbers
  added/fixed on 0625 (`15`–`17`), 0626 (`⁵²`→`²²`, spaces added), 0637 (`23`–`30`), 0653
  (`42`); stray blank lines removed in 0625, 0651 (two), 0677, and a `_______` line after
  the block made blank in 0674; runover lines fixed/added in 0625 (`[cessitatem,`), 0639
  (`[curialitatem,`), 0653 (`[plicat?`), 0661 (`[ad varchum;`), 0667 (`[sapiente, dicis`).
  Batch 7 (0687–0748), 25 pages, 484 lines: 2 not as printed,
  0712 `ch'a 'l` (`ch'a'l`), 0732 `dùbitar` (`dubitar`: a faint speck under `più` on the
  line above). Printed `0733` `insieine` (for `insieme`) and grave accents on `0701`
  `perdèsi`, `0707`/`0721` `andavàn`, `0714` `accusiàn`, `Lodiàn`, `brigavàn`, `0721`
  `volgèmo`, `0732` `pentèmi` rightly kept. Latin blocks: numbers fixed on 0701
  (`⁶¹`–`⁶⁷`→`41`–`47`, plus missing blank line after header added) and 0735
  (`⁸¹`–`⁸⁶`→`31`–`36`); stray blank line removed in 0736; `Etipse`→`Et ipse` and
  `aduggíat`→`aduggiat` in 0709; runover lines fixed/added in 0688 (`niam.`→`[niam.`),
  0699 (`[trem tibi`), 0714 (`[passim.`→`[passum.` on its own line), 0723 (`[locutus fui.`
  and `[quitur.` on their own lines), 0746 (`[luntate.`).
  Batch 8 (0753–0831), 25 pages, 470 lines: 4 apostrophe
  spaces not as printed, 0792 `Che 'l` (`Che'l`), 0819 `quattr' animali`
  (`quattr'animali`), 0828 `L' occhio` (`L'occhio`) and `dentr' e` (`dentr'e`; `l' altro`,
  `dentr' una`, `m' apparve` on 0828 really are spaced). 0779's last line (`Che se ne va
  dirieto a'vostri terghi?`), cut by the crop, was read from `ocr/la/0779.png`. Printed
  `0753` `Dal Troso`, `0777` `usar` (for `uscir`), `0778` `intorno` (for `incontro`) and
  `lor vita` (for `lor via`), `0780` `in se inurba` / `opbrobrio` / `partinci`, `0783`
  Provençal lines (`Tam me bellis …`), `0792` `del mondo` (for `del monte`), `0828`
  `ricidea`, `0830` `coine` (for `come`) rightly kept. `la_verseinsert.py` now also strips
  leading indentation on the Latin verse block (`0755` onwards had 3–4 leading spaces on
  non-numbered lines). Latin blocks: numbers added on 0778 (`9`–`15`), 0780 (`23`–`29`),
  0783 (`41`–`47`), 0828 (`8`–`13`); missing blank line after header/page number added in
  0757, 0778, 0809; 0753 `die`→`dic`; 0754 `seccba`→`seccha`, `[Lucca.`→`[Lucca,`; 0757
  `Veniendò`→`Veniendo`; 0778 `mihi`→`nobis`, `Priùsquam`→`Priusquam`, `[cissem` and
  `[fortunam.` on their own lines; 0782 `[obscurum.` on its own line; 0792 `[cta est,` on
  its own line (`xi` removed); 0831 `^^777`→`777`, `Dominas`→`Domina`, `[rent:` on its own
  line.
  Batch 9 (0832–0911), 25 pages, 429 lines (entering Paradiso):
  1 apostrophe space not as printed, 0910 `più ch' al` (`ch'al`); on re-check (2026-10-17),
  0885 `lieto (⁸):` for the printed `lieto (⁸).` (no upper dot; end of the sentence). 0848
  `Dee` and 0885 `lieto` (GLM-OCR `Dec`, `liceto`) kept: a worn hairline `e`. 0842's last line (`Fummo
  ordinate a lei per sue ancelle.`), cut by the crop, was read from `ocr/la/0842.png`. On 0856,
  tercet number 44 was omitted in print in the Italian verse (kept without number as printed,
  Latin `⁴⁴` kept). Printed inline brackets on 0841 `me[n]`, 0851 `[non]`, 0867 `Eu[n]ce`, and
  printed forms on `0905` `confexion`, `0910` `suo secta`, `rapitten`, `0886`/`0911` 1-line canto
  endings rightly kept. Latin blocks: numbers added on 0881 (`22`–`26`), 0899 (`40`–`46`);
  0832 `[finem,` added; 0837 blank line after header; 0838 `permictere` and `[ante?` fixed,
  `_` removed; 0841 `_` removed; 0842 `[de]` and missing lines 2–3 of tercet 36 restored;
  0848 backticks stripped and pipe table converted to Latin block; 0856 `Talis`, `celo`,
  `quolibet` fixed, `[conem,` and `[frontem:` on their own lines; 0882 stray blank line removed,
  numbers `²⁷`–`³¹`, `[siderium,` and `[suum,` fixed; 0899 `[faciunt.` added, `Respice`, `locum`,
  `guadum.` fixed; 0905 blank line after `851`; 0907 numbers `¹⁶`–`²⁰`; 0908 `[tibundos.` added;
  0909 `²⁸`, `incelat`, `[normam,` fixed; 0910 `[num usitati,` and `[tudinem,` on their own lines,
  commentary removed; 0911 `⁴¹` fixed.
  Batch 10 (0919–0982), 25 pages, 463 lines: 1 not as printed,
  0976 `Cunisa` for the printed `Cimisa` (an `i` dot right after `C`, five stems before `s`;
  its report said there was no dot; Tesseract reads `Cimisa`, GLM-OCR `Cinisa`; kept as
  printed, see "Suspected misprints"). Its spaced elisions (`Ond' eran`, `t' ho`, `Ch' uscì`,
  `fermalv' entro`, `m' havea`, `Dentr' al`, `veggi' hor`, `ch' i'`, `s' io`, `Com' uscir`,
  `ch' a`) are spaced in print. Printed `0976` `[perto,`, `propinqua,`, `muoia,` (commas, not
  GLM-OCR's dots). Latin blocks: 0922 `extinxit`, `amasii`, `Dixi`, `callefacit` and a stray
  blank line removed; 0928 a blank line after the head, `[coperui,`, `Requirit`; 0933 number
  `43`, `Istud`, `corrosit`; 0945 `parti,` and `artem` joined to their lines (not runovers),
  `Que`, `parva`, `nostre letitie` (no `æ` in the print); 0946 `addul[c]escit`, `vita,`,
  `Provintiales`, `[cere alterius.`; 0966 numbers `19`–`24`, `stetissem`, `que`.
  Batch 11 (0987–1078), 25 pages, 462 lines: 2 words and 2
  elision spaces not as printed: 1054 `simiglianze` for the printed `simiglanze` (the
  edition's `gl`), 1042 `miei` for the printed `mici` (see "Suspected misprints"); 1042
  `m'accors' io` for `m' accors' io`, 1045 `degl' ochi` for `degl'ochi`. Also kept as printed:
  1053 `s'àdempia` (a grave on the `a`, see "Suspected misprints"), 1039 `nôi`, 1053
  `se' tanto` (gap as narrow as most). Latin blocks: 1053 numbers `16`–`24` (one less in the
  OCR); 1041 `[corporum;` (no closing bracket in the print). `la_check.py 0983 1078`: the
  batch's pages are clean but for reports caused by neighbouring pages outside the batches:
  1053 (1052's Latin ends at 9), 1063 (1062), 1068 (1064–1066 with plain numbers, 1067
  `²⁵Se` without a space).
  Batch 12 (1079–1144), 25 pages, 486 lines: 4 words not as
  printed: 1137 `trascorso` (printed `transcorso`), 1144 `uscìo` (`usciò`), 1126 `[tisso,`
  (`[fisso,`, the `fi` ligature); and the gaps at apostrophes, which the print sets both
  ways: 6 elisions written spaced though tight in print (1080 `a'tuoi`, 1087 `perch'io`,
  1114 `buon'intention`, 1124 `Dentr'al`, 1126 `Prompt'al`, 1129 `Dintorn'a`), 1137
  `dov' è` written tight, and 22 of the 47 `'l`/`'n` written with a space before though
  tight in print (`che'l`, `e'l`, `fece'l`, `Che'n`, `le'ntendi`, …). All 47 were looked
  at, and in batch 11 likewise (3 of 22 tight: 0988 `Fusse'l`, 1018 `Chè'l … che'n`, 1045
  `senza'ntender`, fixed in `ocr/la`). **Not looked at in batches 1–10**: la-el-agy may have
  written `'l` with a space where the print is tight (vcheck ignores spaces). Latin
  blocks: 1089 numbers `14`–`18` (none in the OCR), `Guilhielmum`, `visio` and `signatum`
  without the OCR's comma and full stop; 1090 tercet 23's first line added (`Taliter fuit
  in oculis meis, quando fui volutus,`), `Propter`, `exponeret`. `la_check.py 1079 1150`:
  clean but for 1134 (1132 `^ Oppresso` and 1133's numbers, outside the batches).
  Batch 13 (1145–1230), 25 pages, 443 lines: 1 word not as
  printed, 1230 `Allora` (printed `Allhora`); of the 49 lines with a spaced apostrophe,
  13 gaps tight in print (`che'l`, `Vagheggia'l`, `ma'l`, `come'l`, `Gonfia'l`, `e'l`,
  1193 `ch'e`, 1201 `de'haver`, 1226 `dagl'odori`, …); its tight `'l` (1148 `parte'l`,
  1229 `Quant'è'l`, 1167 `tutto'l`, 1145 `s'aperse'l`) are tight in print. Also as
  printed: 1180 `mici`, 1157 `transcorsa`, `Perche`. Latin blocks: 1148 tercets 41–43
  rewritten from the scan (runovers `[flammatur:`, `[patefactus.` on their own lines; the
  first two lines of 43, `Inde remansere …`, were missing; the print's italic reads like
  `remunsere`); 1188 `Title:` and the blank lines between tercets removed; 1191 number
  `28`. `la_check.py 1140 1234`: clean but for 1167 (1166 has no Latin numbers, outside
  the batches).
  Batch 14 (1235–1265), 12 pages, 223 lines, the last Italian
  batch: no letter wrong; 4 gaps at apostrophes not as printed (1252 `Tutt' è` written
  tight; 1252 `negl'ochi`, `cogl'ochi`, 1261 `doppo'l` written spaced). 1252's last
  tercet was cut by the crop and read in the full page. Latin blocks: 1235 `[rem et
  florem,` on its own line; 1252 the blank lines between tercets removed, tercet 39 added
  (missing; a stray `39` stood before the commentary's `Sed venias ammodo.`), `Honerare`;
  1261 a wrong `16` on the second line of 15 removed, numbers `16`–`21` one less.
  `la_check.py 1231 1270`: clean.
  **0836** (Latin), 6 lines: as printed. Inserted under the
  gloss line by hand (`la_verseinsert.py` handles only a missing Italian); the Italian
  block's indentation stripped, `Volgendo'l` tight as printed. The commentary had the right
  column (`solito, ostendit … cum acie.`) before the end of the left one (`ostendit quomodo
  fuit lotus … suo more`): moved, whole lines. Left to the markup: words and two lines the
  OCR dropped (`Statio non erat ex illa parte fluminis, in qua iste exercitus`, `nobiles
  Romani semper feriebant cum cuspide ensis. Ista`), `taglo`, `predecto`, `decto`,
  `Beatricis`, `supplicaverunt`.
- **Gaps at apostrophes, batches 1–10** (2026-10-18): all 478 lines of 0237–0982 with a
  spaced apostrophe (elision or `'l`/`'n`, not the truncations `se'`, `de'`, …, the
  `TRUNC` list of the scratch lister) looked at in the image: 128 places not as printed,
  fixed in `ocr/la` and in la-el-agy's files, in 87
  pages. Most `'l`/`'n` written spaced though tight (`che'l`, `e'l`, `Disse'l`, `fra'l`,
  `se'ntendi`), also `fa'che`, `co'ghiottoni`, `va'via`, `trov'una`, `Perch'un`; four the
  other way (0540 `Quell' humido`, 0777 `l' homero`, 0928 `c' hai`, found by chance:
  tight-written elisions were not listed); two letters: 0615 `lo 'inviarci`, 0789
  `lo'intesi` (both written `'nt…`/`'nv…` without the printed `i`).
- **Gloss lines missing** (listed again 2026-10-18 by a scratch script): of the
  inserted pages whose verse has gloss marks, 201 have no gloss line and 22 lack some marks
  in it (223 pages). A first
  count (125 and 14) missed the marks `¹²³` (not in the range `⁰-⁹`) and took verse lines
  beginning with a mark for gloss lines. The gloss lines in place are often OCR noise
  (0237 `(¹) al. peró. — (⁶) meglo.` for seven glosses), so all 223 pages are transcribed
  anew: a scratch script cut the band under the verse, full width; la-el-agy transcribed
  it in 5 batches of 45 ([DELEGATION.md](DELEGATION.md)); the new lines replace the old.
  Check (scratch scripts): the words found in no other reading of the band (Tesseract,
  GLM-OCR, old gloss lines; accents ignored) and gloss numbers that differ from the verse
  marks, each looked at in a crop. Insert: old gloss lines replaced where they stand, else
  the lines after the Italian block, with a blank line before.
  - **Batch 1** (0237–0421, 45 pages, 69 lines): 4 words fixed in the scan (0414
    `affrectasi`, 0403 `segnita`, 0421 `doventata`, 0242 `dell'Inferno` tight); 0397
    `do', i. dove` read with a broken `o` (as 0421). Printed: 0276 `(³)` for the verse's
    `(²)`; 0295 `³)` without `(`. Inserted (6 pages had old gloss lines, replaced);
    `la_check.py 0237 0421` tercet reports unchanged.
  - **Batch 2** (0423–0602, 45 pages): 4 fixed in the scan (0457 `tigluoli`, 0458
    `ov'entra` tight, 0502 and 0592 `³)` as printed); accents checked against Tesseract
    (`così`, `aprì` printed). `ginsert.py` first took 0503's `In exitu Israel de Egypto`
    (also a Latin line) for the end of the Italian block; fixed (the first match of the last
    verse line), 0503 redone from HEAD, all 90 placements checked; the script now skips a
    page already done and refuses an old run holding a tercet number or too long. Inserted;
    `la_check.py 0423 0602` tercet reports unchanged.
  - **Batch 3** (0605–0754, 45 pages): fixed in the scan 0710 `figluol` (the `ﬁ` ligature,
    read `t`; batch 2's 0457 `tigluoli` was the same misreading of mine, now `figluoli`), 0714
    `sì`, 0748 `dell'Inferno` tight, 0746 `(⁵)` (faint bracket). Printed: 0640 `(³)` and 0733
    `(⁹)` repeated. `ginsert.py` took commentary paragraphs beginning `(1)` (0615) for old
    gloss lines: an old run must now be close to the new lines (token_set_ratio ≥ 50). Old
    gloss lines it missed (beginning `— (¹)`, or under the Latin block with no blank line)
    were deleted by hand after a scan of the 135 pages: 0321, 0600, 0635, 0712, 0754.
  - **Batch 4** (0755–1016, 45 pages; blocks up to 12 lines, 0899 beyond the band, read in
    the full page): 0882 `dell'acre` as printed (misprint). **Gloss numbers are written
    `(n)` always**: a bracket lost in print is worn type (a trace shows on most), so `³)`,
    `(³`, bare `⁶` were made `(³)`, `(⁶)` (0295, 0502, 0592, 0733, 0831, 0832, 0837, 0841,
    0842, 0851, 0853, 0931; in `ocr/la` too for those inserted). Accents on `i` (dot or
    stroke) are hard to tell at this resolution; la-el-agy's reading kept where unclear.
    Inserted; `la_check.py 0755 1016` tercet reports unchanged.
  - **Batch 5** (1019–1264, 43 pages): no word to fix; printed and kept: 1190 `Çapricorno`,
    1230 `Symoniaco[s] cº. 19`, 1259 `de'Beati` tight, 1260 `dell' Inferno` spaced. Old
    line left on 1236 (beginning `— (³)`) deleted by hand. `la_check.py 1019 1265` tercet
    reports unchanged.
  - **Result**: all 223 pages have their gloss block once (2–12 lines); the gloss numbers
    match the verse marks except the printed slips 0276 `(³)` for `(²)`, 0640 `(³)` twice,
    0733 `(⁹)` twice. `glosslist.py` still lists 22 pages as "part": its count reads only
    lines beginning with a mark, and these glosses run over a line break.
  Found 2026-10-17: of the 218 inserted pages whose Italian has
  gloss marks, 175 have no gloss line `(¹) …` in `ocr/la` (e.g. 0881, 0966 `(⁴) gigante.`),
  though it is printed under the verse: GLM-OCR and the old file dropped it, and the verse
  task leaves it out. texts/PLAN.md says the gloss line is added if missing (Remaining work).
- **`la_check.py 0233 0915` after batch 9** (2026-10-16): tercets internal to all 25 pages of
  batch 9 are clean (0856 reports 43 then 45 due to the printed omitted number 44).
  The Latin blocks of 0233–0390 (unchecked OCR) needed: numbers made superscript;
  numbers missing though printed (0295, 0307, 0317, 0385 all; 0329 one; 0369 a `"` for
  `44`), misread (0277 `27` for `37`) or a line off (0252, 0289); a stray blank line in
  the block (0320, 0367); a runover word at the end of the next line (0329 `[corruscet.`);
  0321 tercets 31–32 with commentary text mixed in (rewritten from the scan); 0389 a gloss
  line `¹ parlare.` without its blank line. 0309 keeps its `(...)` line (no gloss line
  written).

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

0195–0208: rule 6, model 174 asked, 112 taken (80 of them keeping
`ocr/la`, unchecked); to la-el-claude 82. Of the model's 32 changes, 7 were wrong (0202
`eo` and 0208 `eos` read `co`, `cos`; five tercet numbers given a dot the print lacks; the
`1`/`1.` rule now resolves these). Compared with la-el-claude's reading of the 94 marks it
was shown, the model differed in 27 (about a third): mostly normalizing (`rispettivi` for
printed `respettivi`, `Anmodo`, `corum`, `quizzant`), and Tesseract shares GLM-OCR's c/e
errors (`Tune`, `adhue`, `co`).

0209–0232, 0115, 0141: 231 trivial marks resolved, rule 20, model 338
asked, 207 taken (all keeping `ocr/la`, unchecked); to la-el-claude 190 (34 commas, 156 in
the image or from the model's answer). Of the 18 changes the model and Tesseract agreed on,
3 were wrong (`si` for printed `sì`, `denota re'tur` for `denota[re]tur`, `codem`). Where
Tesseract disagreed, the model picked GLM-OCR's side 17 times, rightly only twice
(`fui[t]`, `decimo.`); the others were misreadings (`staute`, `Molo`, `Nibil`, `soffliò`,
`introtyu`). Both OCRs wrong: 0220 `ecclissi`. Also fixed: 0227 `dicat: Tu` (a difference
the markup missed), 0231 `dicebat,`, 0232 `E sì che`. The markup left 6 differences
unmarked (`la_markup.py` reports them as missed); 5 were artefacts of marks across a
line-end hyphen.

0079–0103: 311 trivial marks resolved, rule 13, model 177 taken (all
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

0104–0194 (the markup answers of 0079–0103's work directory re-checked
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
