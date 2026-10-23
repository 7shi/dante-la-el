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
established on them. `texts/la/008`–`020` are converted from them. **Batch 3 (`0233`–`0348`,
Inferno XIV–XXIII)** is complete too (2026-10-23; Remaining work, item 8), converted into
`texts/la/021`–`030`.

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

Data: `ocr/la/glm-ocr/` (GLM-OCR for every page) and `ocr/la/tesseract/` (Tesseract's word
boxes for every page), both committed; the working data in `tmp/` (the paid answers) are
listed under "Tools".

## Remaining work

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
   - **Trial done** (State). Decided (the user, 2026-10-15): the verse of the 338 pages
     (337 Italian, 0836 Latin) is transcribed by **la-el-agy**, not by Luna, in batches of
     20–30 pages, with the task of the trial ([DELEGATION.md](DELEGATION.md): the crops
     only; no text of the pages, of GLM-OCR or of the poem; superscript tercet numbers,
     `(¹)`, runover lines `[`; letters it is unsure of in the report). 0836 needs the Latin
     wording of the rules. The Luna answers and `la_verseread.py` stay as they are (not used
     further).
   - **Batches**: 25 Italian pages each, in page order; each task is the
     previous one with the new pages and the words of the last batch that were not as
     printed ([DELEGATION.md](DELEGATION.md)).
     - **Done**: batches 1–14, all 337 Italian pages (`0237`–`1265`, State).
     - **Done too**: Latin `0836` (row 338), and the gaps at apostrophes of batches 1–10
       (State). The verse of all 338 pages is in.
     - **Commits**: batches 4–10 were committed together after batch 10 (the user,
       2026-10-17); batches 11–14 and 0836 in `4c6f2f5`.
     - **Next**: item 6 (items 3–5 done). In any later verse check, look at every
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
   - **Gloss lines**: done (2026-10-18, State): the 223 pages
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
   further steps (item 5 on) work on `tmp/la-markup/`. Done (State).
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
   three in parallel (411 pages each). Then: `-r 0` on a copy for the counts (State), the
   long blocks (69 pages, item 3) in the image, 1245's figure. Done (2026-10-18, State): the
   long blocks led to item 6.
6. **Pages with lost text** (decided with the user, 2026-10-18): the 164 pages of the
   word check (State) are retyped from the scan by **la-el-agy**, page by page, from the
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
   State): `tmp/la-mark7/`, 22141 marks decided.
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
     0349–0394 (in `WORK/mine.tsv` and `fixes.tsv`; nothing written to `ocr/la` yet). 20 of
     45 pages retyped from the scan by la-el-claude (0349 0353 0354 0355 0363 0365 0369
     0376 0377 0381 0382 0384–0389 0391–0393): lines run together or out of order, lines
     lost, Italian and Latin swapped (0393), `[For lines …]` notes in the text (0392).
     0387 and 0388 are essay pages kept as one line per paragraph and were retyped line
     by line by mistake: join them back into paragraphs at step 8 (as 0347). 0383's
     signature is `42` (a worn `4`, as on 0399).
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
       (`tmp/la-retype23/opencode/`) and the list of its errors make 0395–0399 cheap to
       finish: fix the 25 places and add the pages with `la_retype.py`.
     Neither replaces la-el-agy for whole pages.
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
        WORK/out` (`both` hits) and `la_seqcheck.py FIRST LAST -d WORK/out`.
     2. Step 6 by way A for the pages that are sound. A small loss (a line or two, found
        by `la_lostcheck.py` or in a mark) is put in with `text:` as before.
     3. A page too broken for its marks (lines out of order or run together, columns
        mixed, more than a few lines lost) is **not retyped**: all its marks are decided
        `left|retype pending`, and the page goes into "Pages to retype" (item 10) with
        what is wrong. Its `ocr/la` stays as it is.
     4. Step 7 (`--write`) and the scripted checks of step 9 (`la_check.py`,
        `la_seqcheck.py`, `la_lostcheck.py` on `ocr/la`); hits on pending pages are left
        for item 10. Step 8 (the image checks of `la_lines.py`) and step 11 (texts) wait
        for item 10, so that each batch is checked and converted once, with its retyped
        pages in. Commit each batch's `ocr/la` (step 10) when the user asks.
     Batch 4 goes on from 0400 (0395–0399 from retype 23, as above); then batches 5–11.

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
10. **Pages to retype** (after item 9, so that the retyped pages use plain digits): the
    pages left `retype pending` in item 8 and those `la_lostcheck.py` lists, retyped from
    the scan (by la-el-agy, way B, or by la-el-claude), checked against both OCRs and
    with `la_lostcheck.py`, written to `ocr/la`; then steps 8 and 11 of each batch. The
    model decisions of these pages (`tmp/la-mark7`) are then unused. The list (page: what
    is wrong), filled in by item 8:
    - (none yet)

Also seen: 0848, 0891 and 0999 have backticks in the text (0891 around its blocks,
`` `Quei gloriosi …` ``), a transcription artifact to remove in their batches.

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
   - small capitals in uppercase, superscript tercet numbers, broken words joined on essay
     pages: the conventions below, whatever the model says.

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
     1. **Task**: `tmp/herdr-task-retypeNN.md`, made from the previous task. It holds the
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
- **Figures**: a line `[figure]` where the figure stands, then each printed label on a
  line of its own (column after column, top to bottom), a blank line after; headings
  that are not printed are not added (1245). 1044 (`[diagram]` in a line) is to be brought to this
  form in its batch (1247 is in it since its retyping).

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
- **Tesseract** (`ocr/la/tesseract/`, committed; run with its [Makefile](tesseract/Makefile),
  `-l lat+ita`, only the words kept, in the columns block_num, par_num, line_num, left, top,
  width, height, text): used only for the word
  boxes, to locate a place in the image. Its readings are poor in general, but it does
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
- **Later narrow tasks** to la-el-agy (2026-10-15–20: the verse, the gloss lines and the
  retyped pages, from the images alone, each batch checked by script): how they were
  written, their rules and its errors are in [DELEGATION.md](DELEGATION.md).

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
- `texts/convert_la.py`: `ocr/la` to `texts/la/` (procedure, step 11).

Working data in `tmp/` (not in git, temporary; `tmp/bak/` is the user's): `la-markup/` (the
paid markup answers, the latest set per page; see "Markup answers") and `la-mark7/` (the work
directory of item 7 over all pages, with the paid model decisions). The paid answers cost
money to make again: keep `la-markup/` and `la-mark7/` until step 7 is done for every batch;
the method reads them nowhere after it (later checks are against the images), so they may be
deleted then. Everything in `tmp/` but `tmp/bak/` is temporary: the data of finished
items were deleted on 2026-10-20 (their results are in `ocr/la` and the history above), and
what is left is deleted when no longer used, each time after asking the user.
