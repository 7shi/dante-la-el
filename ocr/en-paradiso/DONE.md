# Done: checking `ocr/en-paradiso`

The record of the check ([PLAN.md](PLAN.md)), step by step.

## Step 0: setup (2026-11-15)

- **The conventions** of `en-purgatorio` taken over whole (README.md, "Transcription");
  its settled readings to be checked on the trial.
- **misprints.tsv and readcheck.tsv**: the headers, with the columns of `en-purgatorio`.
- **The converter and the crop script**: `PARADISO` settings in
  `texts/scripts/convert_en_oelsner.py` (the verses per canto, the pages of each canto,
  the plates, the images and their names, the front and end matter, from INDEX.md) and
  an empty box list in `crop_en_oelsner_images.py`. The decisions by hand (the first line
  of each figure among the notes, the hyphens, the note paragraphs at page tops) wait
  for the base (step 2), the boxes for step 6. The *Inferno*'s and the *Purgatorio*'s
  output checked unchanged: the Markdown, the images, and the *Inferno*'s report byte for
  byte.

## Step 1: the readings and the structure (begun 2026-11-15)

- **Internet Archive's OCR**: `iascan.py pages`, all 436 leaves into `ia-ocr/` (the
  file = the leaf).
- **INDEX.md** and README.md "Layout": from `iascan.py heads` and the printed Index to
  Maps, Diagrams and Tables (p. 419). The first page of each canto from the running heads
  (all 33 found); the leaf where the notes begin from the first note lines in `ia-ocr/`,
  read in the images where the OCR had missed them (Cantos II, XV, XXXI); the figures,
  the front and end matter and the pages left out read in contact sheets of the images.
  Five figures are printed in another canto's pages than the one they illustrate (the
  caption names it). The first lines of the cantos are to be added from the base.
- **GLM-OCR**: the user, with `glm-ocr/Makefile`, now through `ocr/scripts/glmocr.py`.
- **The base** of the trial's pages (`012`–`036`): la-el-agy from the task file, after
  the *Purgatorio*'s. Its report: all 25 pages read by the orchestrator and written by
  the executor in a plan-execute mode (no workers), none corrected, none empty, 17
  uncertain places (worn tercet numbers and page numbers, blotted letters); each was
  right.
- **The base of the other pages**: la-el-agy in two runs, `005`–`227` (the front matter
  and Cantos I–XVII, 196 pages) and `228`–`430` (Cantos XVIII–XXXIII and the end matter,
  203 pages), from task files with the settled readings, the tables printed sideways
  (read turned upright, one person or couple per line) and the scheme on `423` (one box
  per line). Subagents through `invoke_subagent` on the same model (Gemini 4 Hydrogen);
  in the first run the first batch (`005`–`041`) ran before agy switched to that call.
  No page empty; 105 and 103 uncertain places reported, left to steps 2 and 4. agy also
  evened the spacing before `; : ! ?` and round `=` across 34 pages of the first run,
  as the settled readings write them.

## Step 3: the trial on `012`–`036` (2026-11-15)

The first 25 pages of the cantos (Cantos I–II and the first page of III, pp. 2–26, with
the diagram of p. 12), to decide whether the base needs a retype.

- **The comparison**: `cmpread.py` with GLM-OCR as the second reading (`-i ia-ocr`,
  `--verse-numbers`): 84 places (A 16, B 58, C 10), almost all the marginal labels and
  running heads placed elsewhere, the accents GLM-OCR dropped (`sì`, `lì`) and the words
  hyphenated at line ends; GLM-OCR also wrote a paragraph twice on `034`. The places that
  might differ in substance (`020` `lì`, the diagram's `SUN` on `022`, the closing quote
  on `019`, the run on `034`) were decided in the image: the base was right.
- **The read**: all 25 pages line by line against their images (each page in two
  halves; the doubtful marks in crops).
- **Found**: 4 errors of the base in 25 pages, none of a word.
  - `020` 26: the three-dot mark before the general note written `*.*`; `∵`, as
    `en-purgatorio` writes it (449).
  - `020` 38, `023` 33, `035` 22: `=` printed close to its words (`Apollo=the Sun=God`)
    written with spaces.
  - And 2 misprints, kept as printed by the base and marked: `022` 5 the note number
    `37-39` without its period; `026` 20 `unita` (Canto II 36) ending the tercet
    without a stop.
- **Decided** (the user): no retype. The marks found (`∵`, `=` close) go into PLAN.md,
  "Settled readings", and into the task file for the other pages.

## Step 2: convert at once; the mechanical checks (2026-11-15)

`convert_en_oelsner.py paradiso` on the whole base, into `texts/en-paradiso/`.

- **The converter made ready for the volume**: the page numbers (printed page = leaf −
  10, the epigraph `011` p. [1]; `PAGE_OFFSET` and `EPIGRAPH` per volume, 12 and 13 for
  the other two) and the running heads `PARADISO`, `DANTE’S PARADISE` and
  `EDITORIAL NOTE` with a page number (the title `EDITORIAL NOTE` of the *Purgatorio*,
  without one, stays a title). Before this the heads were read as verse and the verse
  counts went wrong on every page.
- **The figures**: those below the notes from their first line (`FIGURE_FROM`: `069`,
  `098`, `099`, `110`, `111`, `151`, `406`, `407`); the diagram on `022`, printed between
  two notes, shown after the note before it with its labels (`FIGURE_BETWEEN`, new).
- **The verse count** of each canto and **the tercet numbers**: all 33 as in the
  standard text, no error.
- **The English paragraphs against the tercets**: 15 English pages whose notes start
  without a verse number, all notes continued from the Italian page.
- **The note paragraphs at a page top** after a finished sentence: `035` continued
  (flush left), `057` new (indented), in the image.
- **Line-end hyphens**: 85 the word list could not decide, read through; 10 decided by
  hand (`HYPHEN_FIXED`: `establishment`, `signature`, `endowment`, `interchange` joined;
  `new-create`, `diverse-natured`, `things-to-see`, `a-moving`, `three-stringed`,
  `tooth-grips` kept). `Ghibil-line` (`070`) and `Com-machio` (`277`) are printed so;
  left to the read-through.
- **The end matter**: the scheme of the heavens on `423` kept line by line
  (`LINES_FROM`, new); the index on `429`, printed without space between its entries,
  one paragraph per entry (`INDEX_ENTRIES`, new); the footnote on `420` linked
  (`FOOTNOTES`; the converter drops the `¹` the base writes before the note).
- **Fixed in the base** (readcheck.tsv): `250` the page number `240`, printed sideways at
  the left edge, written `§` at the foot; `331` the signature mark `X` written `x` (the
  signatures run U 315, X 331, Y 347).
- The *Inferno*'s and the *Purgatorio*'s output unchanged.

## Step 4: the comparison (2026-11-15)

All 424 pages of the base (`005`–`430`) at once, without batches.

- **The readings**: GLM-OCR over all 436 leaves (the user, `ocr/scripts/glmocr.py`);
  `--check` listed 6 pages with a repetition, the poem's own (`338`, `339` `il loco
  mio`) or GLM-OCR's, which `cmpread.py` leaves out by their length (`006`, `201`,
  `217`, `429`).
- **The comparison**: `cmpread.py` with GLM-OCR as the second reading (`-i ia-ocr`,
  `--verse-numbers`): 1422 places (A 402, B 925, C 95), as in the *Purgatorio* mostly
  the marginal labels and running heads placed elsewhere, the accents GLM-OCR dropped,
  its repeated runs and its misreadings of `fi` and `fl` (`siamma`). A second run with
  Tesseract's lines (joined from its word boxes) as the second reading; from the two,
  the places where two of GLM-OCR, Tesseract and Internet Archive read the same against
  the base, the accents, ligatures, `l`/`1`/`I`, labels and heads left out: 129, each
  decided in the image (most a comma for a period or a straight quote, read alike by
  Tesseract and Internet Archive). Then the places where all three differ from the base,
  and the 95 runs of class C: no line lost by the base.
- **agy's uncertain places** (208 in the two reports): 64 where a reading differs,
  decided with the rest; the 144 others where every reading agrees with the base, read
  for a misprint or a missing mark the comparison cannot see (a hyphen, a stop).
- **Found** (readcheck.tsv): 16 errors of the base and 15 misprints marked.
  - The Italian made as the standard text has it (10): the spellings `egualemente`,
    `donde`, `reddire`, `servigio`, `millesmo`, `Jesù`, `produtto`, `vuoli`, and two
    semicolons (after `vista`, `Paradiso`) made a colon and a comma. Also `behooves` for
    `behoves`, `whereof` for `wherefrom`, `IX.` for `XIX.` (a map's caption), `ard`
    for `and`, a faint line-end hyphen (`includ-`) and a word space (`they descended`).
  - Misprints corrected silently by the base, now marked (5): `bide`, `Imolose`,
    `43-45,`, `congruance`, `giù`.
  - Misprints kept by the base unmarked, now marked (10): `him.`, `Repnblic` (a turned
    `u`), `be` for `he`, `second.`, `fa,montando`, `1302` and two Italian lines without
    their stop, `them` without its hyphen, `all.`.
  - Of the first batch of the base (`005`–`041`, before agy's subagents switched to
    `invoke_subagent`), one error (`040`).
- **Decided printed**: `334` `ego` (the italic `o` worn open, as the `e` before it);
  `050` `possendo`, `254` `can` (broken letters); `083` `Modĕna`; `418` the label
  `Empir`, `211` `The Pere gate`, left to the read-through.
- The converter's report unchanged against step 2; the *Inferno*'s and the
  *Purgatorio*'s output not touched.

## Step 5: the read-through (2026-11-15)

All 424 pages of the base (`005`–`430`) read for sense in `ocr/`, in two passes (GUIDE.md,
"Read-through for sense"): first the doubtful places listed (94, with a list of the
words found in neither the other two volumes, the Commedia nor a word list), then each
decided in the image, by crops of its line.

- **Misprints** (39 marks, misprints.tsv now 56 rows): in the Italian `ch` for `che`,
  `cio`, `sara` (accents not printed), `comforti`, `quante` for `quanto`, `se'` and `chi'`
  for `s'` and `ch'`, `Aberichi` (the English has `Alberichi`), two lines ending a tercet
  without their stop, and the tercet number `100` printed `10` (XXV); in the English
  `vengence`, `lead` for `led`, `abbott`, `aud` (a turned `n`), `witholding`, `therewas`,
  `Ostragoths`, `Ghibil-line`; the labels `Empir` (`Empireo`) and `The Pere gate`
  (`Pera`, as in the Italian, the English, the notes and the map; the user); citations
  (`ii. 6; 40`, `ix. i`, `2 Cor,`, `sqq;`); missing or wrong stops and brackets in the arguments, the
  notes and the end matter, and the signatures of the editorial note (`P H. W.`, `H. O`).
- **Misreadings** (4): `of the` dropped at a line end (`155`), a comma for the printed
  period (`288`), `6,7` for the spaced `6, 7` (`347`), and a map's label (`098`).
  And in the Tables of Kings (`250`–`253`, found after the read-through, when Table I
  and IV were compared): the thick letters of the persons named in Canto XIX (16
  names, and the head note's own `Thick letters`) written plain, and the head
  note's `Paradise XIX.` made `Paradiso`.
- **Kept as printed** (33 rows `printed`): spellings the edition prints (`Bernadone`,
  `Cassale`, `d’Aquaspata`, `Guinivere`, `Rachael`, `Gesù` beside `Jesù`), elisions set
  close (`fe'da`), `’t is` and spaced dashes, `Cf. l. 6` (`083`: the Troad of lines
  67-68 is the mountains of line 6, whence the eagle came), the dates of Frederick in
  Tables I and IV (`1296` and `1295`: both current, proclaimed king in December 1295,
  crowned in March 1296; the user) and `month!` within a sentence (`337`; the user).
- **Left from steps 2 and 4**: `Ghibil-line` marked; `Com-machio` (`277`) kept, in
  Toynbee's words; `Empir` and `The Pere gate` marked.
- The map labels (`099`, `217`) are left to the figures (step 6).
- The converter's report: the line `HYPHEN 070: Ghibil-line` is gone (the mark joins it);
  otherwise unchanged. The *Inferno*'s and the *Purgatorio*'s output not touched.

## Step 6: the figures (2026-11-15)

- **The boxes** of the twelve figures (2 diagrams, 10 maps) in
  `crop_en_oelsner_images.py` (`PARADISO`): found from the ink of each page (a speck
  left out where it widened a box), each figure with its labels and without its caption
  and the map numbers `I`, `II` printed above the two retrospects; checked in a contact
  sheet. `uv run texts/scripts/crop_en_oelsner_images.py paradiso` writes
  `texts/en-paradiso/images/` (`022`, `069`, `098`, `099`, `110`, `111`, `125`, `151`,
  `201`, `217`, `406`, `407`); every image the Markdown links to is there.
- **The map labels** left from the read-through, read in enlarged crops: `099` `R.Tronto`
  printed close, as `R.Rhone` on `098`; on `217` `SANNELLA` (set along a street and
  crossed by it; the base had `SANTHELLA`) and `CIUFFAGNI` (the base had `GIUFFAGNI`), as
  the text names them, and a line `ER` removed, the end of the upper `? ALIGHIERI`
  written again apart.
- The tables (`250`–`253`, `383`) stay text.
- The *Inferno*'s and the *Purgatorio*'s images cut again into a scratch directory: the
  same byte for byte. The converter's report unchanged.

## Step 7: close (2026-11-15)

- **The Italian against the standard text**, word by word (dante-corpus; a list, not a
  check: each place decided in the image): the words that differ by a letter or two and
  occur at most twice in the Italian of the three volumes, about 300, almost all the
  edition's readings (`diliberarti`, `satisfare`, the diaeresis not printed). Two
  misprints the read-through had passed, both the first line of a canto: `Oppreso`
  (XXII 1) and `comtemplante` (XXXII 1), marked; six readings checked in the image and
  kept (`arrosemi`, `sfocato`, `Casino`, `assolti`, `pasciuto`, `sospinta`). Run then on
  the other two volumes too (their DONE.md); kept as `ocr/scripts/stdcmp.py`.
- **The printer's imprint** (`430`), left out by the converter, put after the index
  (`039-index-to-maps-diagrams-and-tables.md`), as the *Purgatorio*'s.
- **SUMMARY.md** written; README.md ("Credits", the state), INDEX.md (the first line of
  each canto), the root README, ocr/README.md, ocr/GUIDE.md (the lessons), texts/PLAN.md,
  texts/README.md, texts/scripts/README.md and texts/en-paradiso/README.md updated.
- The final counts (readcheck.tsv): 34 misread, 58 misprints, 41 printed;
  misprints.tsv 58 rows, `misprints.py` no problems.
