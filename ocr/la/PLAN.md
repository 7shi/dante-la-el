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

1. **Italics**: the slant script, the delegate's trial and batch 1 (0079–0114) are done
   (steps 1–3); next, the nine parts (step 3, "Parts"); parts 1–7 done (0079–1009,
   the Inferno, Purgatorio and Paradiso 1–11); next part 8 (Paradiso 12–22).
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

### Italics (after check 1; decided with the user, 2026-11-01; method changed 2026-11-03)

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
   Purgatorio and Paradiso 1–11 through the script.
4. **Scope**: the canto pages, the lemmas and the `other` italics (words cited, a name
   like `Pastoralis`; widened with the user, 2026-11-04, and batch 1 reviewed). The
   essays, front matter and appendix only if the user agrees, after the parts.
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
   "Conventions settled during the check", "Known limits".

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
- `ocr/la_italic.py FIRST LAST -t TESS [-o OUT] [-v] [--boxes DIR]`: the italic words of the
  commentary by their slant ("Checks", Italics, step 1).
- `ocr/la_lexcheck.py`: to be written ("Checks").

The working data of the completed work in `tmp/` (`la-markup/`, `la-mark7/`, the paid
answers; DONE.md) are read by no step any more. Everything in `tmp/` but `tmp/bak/` is
temporary; the user clears it.
