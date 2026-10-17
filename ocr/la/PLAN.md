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

## State (2026-10-17)

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
- **Markup of the 48 pages with a moved Latin block** (paid, by the user, default rounds):
  re-checked with `-r 0`: 207 differences missed in 43 pages (44 spacing only); without
  0598, about 3–4 a page, as on the other pages (left to the extra round, item 5).
- **Italics written `*…*`** (Gemini's italics; the convention does not transcribe them):
  0598 had 53 commentary lines wrapped in `*…*`, and the model's entries removing a `*`
  could not be placed (two on a line). Every `*` was removed from `ocr/la` (114 pages, 475
  lines, `tmp/la-italic-strip.txt`; only `*`, and a space left doubled or leading on two
  lines, 0569, 0691), except the printed ones: 1193 `* * *`, 1254 `Quia(*)`; and 0611
  `* Ego me moveram`, a misread tercet number (GLM-OCR `4`), left for the verse check.
  Their markup is redone: the answers of the 89 pages not already among the 386, and
  0598's second set (as `bak/0598-2.*`), were moved to `bak/`. The pages to mark are now
  `tmp/la-markup-redo.txt` (475: 47 done, 90 ready in `tmp/la-markup-ready.txt`, 338 after
  the verse).
- **Markup of the 90 ready pages** (paid, by the user, default rounds): re-checked with
  `-r 0`: 351 differences missed in 62 pages (132 spacing only), 72 entries not placed in
  38 pages. Most are on two pages: 1023 (82, GLM-OCR drops the space after punctuation)
  and 1277 (57, the two OCRs break and bound the text differently; 8 not placed; look at it
  after the extra round). 0598: 0 not placed (56 before the italics fix), 1 missed. No `*`
  entry is left anywhere. Left to the extra round, item 5.
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
  - **la-el-agy** (`tmp/herdr-task-verse2.md`, the crops only, no text of the pages) on 5
    of these pages (0169 0188 0200 0202 0227, 111 lines, `tmp/la-verse/agy/`): letters 0,
    punctuation 0, tercet numbers 0 (Luna, third prompt: 25, 1, 14); one accent, 0200
    `dietrò`, which it reported itself as unsure (a speck above the `o`, not an accent:
    the file's `dietro` stands). Read independently: its apostrophe spacing and number
    forms differ from the file's.
- **Verse inserted** (Remaining work, items 1–2): batches 1–2 of
  la-el-agy, 50 pages (0237–0390, the first 50 Italian pages of `crops.tsv`), 920 lines,
  5 words not as printed, all found by the check and fixed: 0273 `Ch'havea` (`C'havea`),
  0284 `dirieto` (`dirietro`), 0378 `departii` (`dipartii`), 0378 `mornorando` and 0390
  `ninico` (`mormorando`, `nimico`: an `m` whose worn first stem it took for an `n`, with
  a stroke-width argument in its report). No accent, punctuation or tercet number wrong.
  Its notes of "unsure" or "measured" letters are not a sign of a right reading: look at
  them.
  Batch 3 (0397–0459, `tmp/herdr-task-verse5.md`), 25 pages, 495 lines: 2 not as printed,
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
  Batch 4 (0468–0549, `tmp/herdr-task-verse6.md`), 25 pages, 466 lines: 4 not as printed,
  0501 `Rïvidil` (`Rividil`: a smudged dot on `i`), 0527 `mío` (`mio`: the same), 0536
  `calan do` (`calando`: a worn `d` bowl), 0539 `sopragjunto` (`sopragiunto`: a speck below
  `i`). Conversely, the printed grave accents on `0501` `càgion`, `0507` `andavàn`, `sà`,
  `0536` `Fàccianli` were rightly kept. Latin blocks: numbers added/fixed on 0494 (`28`–`33`),
  0514 (`19`), 0535 (`8`→`3`), 0539 (`47`–`50`→`27`–`30`); 0505 `Si[c]`, a stray blank line
  removed and `[cumque` added; 0527 `[facit.` moved before `31` and `_` stripped; 0535
  `[gnum.` added; 0536 `[raucum;` put on its own line and `[verterunt,` fixed; 0547 missing
  `vertice` added.
  Batch 5 (0551–0615, `tmp/herdr-task-verse7.md`), 25 pages, 499 lines: 4 not as printed,
  0557 `[perduto` and 0558 `[quante.` written inline at the end of the next line instead of
  on their own line after the line they continue, 0600 `nòi` (`noi`: an interlinear speck),
  0605 `Salvani` (`Selvani`). Printed grave accents on `0569` `Vèr`, `dèi`, `0580` `fòr`,
  `0589` `salivàmmo`, `0600` `ànno` rightly kept. Latin blocks: 0558 numbers `12`–`13` and
  missing `[me adhereo.` added; 0569 `[gradum,`, 0579 `[quantulum,`, 0593 `[me moveam:` put
  on their own lines; 0579 missing `incendium` (`ymaginatum`) added; 0589 broken line
  rejoined; 0601 `[transitus,` and `[est parcus.` fixed; 0605 `[explanas;`, `qui[a] fuit
  presumptuosus`, `[ausus.`, `Priusquam` fixed and 4 garbled commentary lines at the end of
  the verse block removed.
  Batch 6 (0616–0677, `tmp/herdr-task-verse8.md`), 25 pages, 467 lines: 2 not as printed,
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
  Batch 7 (0687–0748, `tmp/herdr-task-verse9.md`), 25 pages, 484 lines: 2 not as printed,
  0712 `ch'a 'l` (`ch'a'l`), 0732 `dùbitar` (`dubitar`: a faint speck under `più` on the
  line above). Printed `0733` `insieine` (for `insieme`) and grave accents on `0701`
  `perdèsi`, `0707`/`0721` `andavàn`, `0714` `accusiàn`, `Lodiàn`, `brigavàn`, `0721`
  `volgèmo`, `0732` `pentèmi` rightly kept. Latin blocks: numbers fixed on 0701
  (`⁶¹`–`⁶⁷`→`41`–`47`, plus missing blank line after header added) and 0735
  (`⁸¹`–`⁸⁶`→`31`–`36`); stray blank line removed in 0736; `Etipse`→`Et ipse` and
  `aduggíat`→`aduggiat` in 0709; runover lines fixed/added in 0688 (`niam.`→`[niam.`),
  0699 (`[trem tibi`), 0714 (`[passim.`→`[passum.` on its own line), 0723 (`[locutus fui.`
  and `[quitur.` on their own lines), 0746 (`[luntate.`).
  Batch 8 (0753–0831, `tmp/herdr-task-verse10.md`), 25 pages, 470 lines: 4 apostrophe
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
  Batch 9 (0832–0911, `tmp/herdr-task-verse11.md`), 25 pages, 429 lines (entering Paradiso):
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
  Batch 10 (0919–0982, `tmp/herdr-task-verse12.md`), 25 pages, 463 lines: 1 not as printed,
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
  Batch 11 (0987–1078, `tmp/herdr-task-verse13.md`), 25 pages, 462 lines: 2 words and 2
  elision spaces not as printed: 1054 `simiglianze` for the printed `simiglanze` (the
  edition's `gl`), 1042 `miei` for the printed `mici` (see "Suspected misprints"); 1042
  `m'accors' io` for `m' accors' io`, 1045 `degl' ochi` for `degl'ochi`. Also kept as printed:
  1053 `s'àdempia` (a grave on the `a`, see "Suspected misprints"), 1039 `nôi`, 1053
  `se' tanto` (gap as narrow as most). Latin blocks: 1053 numbers `16`–`24` (one less in the
  OCR); 1041 `[corporum;` (no closing bracket in the print). `la_check.py 0983 1078`: the
  batch's pages are clean but for reports caused by neighbouring pages outside the batches:
  1053 (1052's Latin ends at 9), 1063 (1062), 1068 (1064–1066 with plain numbers, 1067
  `²⁵Se` without a space).
  Batch 12 (1079–1144, `tmp/herdr-task-verse14.md`), 25 pages, 486 lines: 4 words not as
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
  Batch 13 (1145–1230, `tmp/herdr-task-verse15.md`), 25 pages, 443 lines: 1 word not as
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
  Batch 14 (1235–1265, `tmp/herdr-task-verse16.md`), 12 pages, 223 lines, the last Italian
  batch: no letter wrong; 4 gaps at apostrophes not as printed (1252 `Tutt' è` written
  tight; 1252 `negl'ochi`, `cogl'ochi`, 1261 `doppo'l` written spaced). 1252's last
  tercet was cut by the crop and read in the full page. Latin blocks: 1235 `[rem et
  florem,` on its own line; 1252 the blank lines between tercets removed, tercet 39 added
  (missing; a stray `39` stood before the commentary's `Sed venias ammodo.`), `Honerare`;
  1261 a wrong `16` on the second line of 15 removed, numbers `16`–`21` one less.
  `la_check.py 1231 1270`: clean.
  **0836** (Latin, `tmp/herdr-task-verse17.md`), 6 lines: as printed. Inserted under the
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
  fixed in `ocr/la` and `tmp/la-verse/agy/` (`tmp/la-verse/apos-fixes-b1-10.tsv`), in 87
  pages. Most `'l`/`'n` written spaced though tight (`che'l`, `e'l`, `Disse'l`, `fra'l`,
  `se'ntendi`), also `fa'che`, `co'ghiottoni`, `va'via`, `trov'una`, `Perch'un`; four the
  other way (0540 `Quell' humido`, 0777 `l' homero`, 0928 `c' hai`, found by chance:
  tight-written elisions were not listed); two letters: 0615 `lo 'inviarci`, 0789
  `lo'intesi` (both written `'nt…`/`'nv…` without the printed `i`).
- **Gloss lines missing** (listed again 2026-10-18, `tmp/la-gloss-missing.tsv` by
  `tmp/la-verse/glosslist.py`): of the inserted pages whose verse has gloss marks, 201 have
  no gloss line and 22 lack some marks in it (223 pages, `tmp/la-gloss/pages.txt`). A first
  count (125 and 14) missed the marks `¹²³` (not in the range `⁰-⁹`) and took verse lines
  beginning with a mark for gloss lines. The gloss lines in place are often OCR noise
  (0237 `(¹) al. peró. — (⁶) meglo.` for seven glosses), so all 223 pages are transcribed
  anew: `tmp/la-gloss/glosscrop.py` cut the band under the verse, full width
  (`tmp/la-gloss/crops/`); la-el-agy transcribes it in 5 batches of 45
  (`tmp/herdr-task-gloss1.md`, into `tmp/la-gloss/agy/`); the new lines replace the old.
  Check: `tmp/la-gloss/gcheck.py` lists the words found in no other reading of the band
  (Tesseract, GLM-OCR, old gloss lines; accents ignored) and gloss numbers that differ from
  the verse marks; `tmp/la-gloss/gshow.py` stacks crops of them. Insert:
  `tmp/la-gloss/ginsert.py PAGES [-n]` (old gloss lines replaced where they stand, else the
  lines after the Italian block, with a blank line before).
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

Data ready (in `tmp/`, not in git; see "Tools"):

- `tmp/la-tess/`: Tesseract's word boxes for every page (`0001`–`1296`);
- `ocr/la/glm-ocr/`: GLM-OCR for every page (committed);
- `tmp/la-markup/`: the store of the user's paid markup answers, the latest set per page
  (896 pages; keep). See "Markup answers";
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
     present), transcribe, and measure against `ocr/la`; then all pages. Prepared: the
     crops of the Italian of 0079–0232 are in `tmp/la-verse/trial/crops/` (121 pages; 0119,
     0188, 0215, 0231 counted differently; 0215 and 0231 looked at: fine, 0231 has specks
     at the left edge); the trial (paid, by the user), then the measure:
     `uv run ocr/la_verseread.py tmp/la-verse/trial/crops -m gpt-6-luna` (add `-n 5` for a
     first look), then `uv run ocr/la_verseread.py tmp/la-verse/trial/crops -m gpt-6-luna --check`
     (no calls once answered). All pages: `uv run ocr/la_verseread.py tmp/la-verse/crops -m gpt-6-luna`.
   - **Trial done** (State). Decided (the user, 2026-10-15): the verse of the 338 pages
     (`tmp/la-verse/crops/`: 337 Italian, 0836 Latin) is transcribed by **la-el-agy**, not
     by Luna, in batches of 20–30 pages, with the task of `tmp/herdr-task-verse2.md` (the
     crops only; no text of the pages, of GLM-OCR or of the poem; superscript tercet
     numbers, `(¹)`, runover lines `[`; letters it is unsure of in the report), into
     `tmp/la-verse/agy/PAGE.txt`. 0836 needs the Latin wording of the rules. The Luna
     answers and `la_verseread.py` stay as they are (not used further).
   - **Batches**: 25 Italian pages each, in the order of `crops.tsv`; the task of batch N
     is `tmp/herdr-task-verse{N+2}.md` (the previous one with the new pages, and the
     words of the last batch that were not as printed), the report
     `tmp/herdr-report-verse{N+2}.md`.
     - **Done**: batches 1–14, all 337 Italian pages (`0237`–`1265`, State).
     - **Done too**: Latin `0836` (row 338), and the gaps at apostrophes of batches 1–10
       (State). The verse of all 338 pages is in.
     - **Commits**: batches 4–10 were committed together after batch 10 (the user,
       2026-10-17); batches 11–14 and 0836 in `4c6f2f5`.
     - **Next**: item 3 (item 4's 0458 and 0727 are fixed). In any later verse check, look at every
       apostrophe written with a space; the print sets the gaps both ways.
2. **Verse check**, after each batch of item 1 (la-el-claude, by script first): compare
   each transcription with GLM-OCR, which reads the Italian verse (as a check only), and
   its tercet numbers with those of the Latin column of the page; look in the image only at
   the disagreements and at the letters la-el-agy reported unsure (a crop per place).
   dante-corpus only points at places to look at: this edition's forms differ from it, and
   a difference is not a reason to change. 0836 (Latin, no GLM-OCR reading of the verse):
   checked in the image. Then insert the blocks (Italian block, gloss line, Latin block;
   see the conventions) and run `la_check.py` (tercets) until it reports only known
   exceptions.
   - **How** (batches 1–2): `uv run tmp/la-verse/vcheck.py PAGES` (in `tmp/`, not in git)
     aligns each line with GLM-OCR's lines and lists the word differences, and compares
     the tercet numbers and line count with the Latin block; `-t` compares with
     Tesseract's words in the crop instead, for the pages whose GLM-OCR has no Italian
     verse (about a quarter). Most differences are OCR noise (gloss marks, `'l`, accents
     GLM-OCR drops: `sì`/`si`, `Così`/`Cosi`, taken as la-el-agy reads them). The letter
     differences, about 20 a batch: `uv run tmp/la-verse/vshow.py OUT.png PAGE:WORD[:la]
     ...` stacks the printed lines in one image (`:la`, the Latin column), a 4× crop of
     the word where unclear. Fix `tmp/la-verse/agy/PAGE.txt`, then
     `uv run ocr/la_verseinsert.py PAGES -d tmp/la-verse/agy -n`: it lists every Latin
     number it would add or change, and pages whose Latin line count differs (fix the
     Latin block first, in the image); look at the changed numbers in the image, then
     run it without `-n`. `la_check.py` over the range: the reports on the inserted pages
     (a stray blank line in a block, a gloss line taken as verse); those on other pages
     are for the batch procedure.
   - **Gloss lines**: done (2026-10-18, State): the 223 pages of `tmp/la-gloss/pages.txt`
     have the gloss lines transcribed from the image, in place of the old ones.
3. **Markup of the 475 pages** (paid) of `tmp/la-markup-redo.txt`, as procedure step 2,
   with the default rounds (the extra round of item 5 is for all pages together). Done:
   137 (the 48 with a moved Latin block and the 90 of `tmp/la-markup-ready.txt`, 0598 in
   both); the other 338 (`tmp/la-markup-verse.txt`), whose verse and gloss lines are now
   in: their old answers no longer fit, so they are called afresh into `tmp/la-mark6/`.
4. **Pages that stop `la_markprep.py`**: 0063 `{et}`, 0727 `{dicit}`, 0822 `{firmaret}`,
   0399 a `}}` line, 0458 and 1245 `|` (in `ocr/la`): check in the image and fix `ocr/la`
   (0458 and 0727, among the 338 of item 3, fixed on 2026-10-18: 0727 `[dicit]` as printed;
   0458's commentary, whose two columns were run together line by line, retyped from the
   scan); 0021 `||`, 0344 and 0467
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
| 0976 | 14 | `Cimisa fui chiamata` | `Cunisa` | Italian verse; an `i` dot right after `C` and five stems before `s` (Tesseract `Cimisa`, GLM-OCR `Cinisa`); the commentary has `Cunizza`. |
| 1042 | 11 | `Agl' ochi mici,` | `miei` | Italian verse; a clear `c` (GLM-OCR `mici` too). |
| 1053 | 23 | `s'àdempia` | `s'adempia` | Italian verse; a grave accent over the `a` (Tesseract `s'àdempia`). |

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
- `ocr/la_versecrop.py PAGE... -t TESS -o OUTDIR [-c it|la]`: crops the verse column
  missing from a page (found from the other column's lines in Tesseract's words and the
  blank band between the columns), for its transcription; `crops.tsv` lists the boxes and
  the line counts to look at (Remaining work, item 1). `-c` crops that column also where
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
