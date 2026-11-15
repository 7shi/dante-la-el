# Done: checking `ocr/en-purgatorio`

The record of the check ([PLAN.md](PLAN.md)), step by step.

## Step 5: the trial on `014`–`038` (2026-11-15)

The first 25 pages of the cantos (Cantos I–III, pp. 2–26, with the two diagrams of pp. 12
and 13), to decide whether the base needs a retype.

- **The base**: la-el-agy in its Orchestrator mode (Gemini 4 Argon directing workers,
  Gemini 4 Hydrogen by the mode's description; asked, none could name its model), from a
  task file with the conventions of PLAN.md, step 2. Five workers wrote five pages each;
  the orchestrator checked every page against its image and changed two places (the
  diagram's `BETWEEN 10 & 11 A.M.`, the spacing of `1 : 63-65`), both right. Its report
  listed about 50 uncertain places; none was wrong.
- **The other readings**: Tesseract and GLM-OCR (`make` in `tesseract/` and `glm-ocr/`),
  Internet Archive's OCR (`iascan.py pages`, all 462 leaves into `ia-ocr/`).
- **The check**: `014`–`018` retyped from the images alone; no difference from the base.
  Retyping the rest stopped (the output of whole pages was filtered); `019`–`038` were
  read line by line against their images instead, small marks and the diagram labels in
  crops at four to six times their size. `cmpread.py` with GLM-OCR as the second reading
  (`-i ia-ocr`, `--verse-numbers`): 87 places (A 19, B 54, C 14), mostly the marginal
  labels and running heads placed elsewhere and accents GLM-OCR dropped; about ten
  decided in the image.
- **Found**: 2 errors of the base in 25 pages.
  - `020` 8 `fora` for the printed `fuora`: Tesseract, GLM-OCR and Internet Archive all
    read `fuora` (class A).
  - `021` 18: the blank line before `for ’twere` (a new tercet) missing; no reading
    compares paragraph breaks.
  - And a misprint every reading passed: `020` 8 `che fatta tu` for `fu` (Canto I 89),
    the letter printed as a `t`; marked `{{tu|fu}}`.
- **Internet Archive's column** agreed with the others on `fuora` and decided nothing
  alone.
- **Decision** (the user): no retype (PLAN.md, "Decisions"). The fixes are rows of
  [readcheck.tsv](readcheck.tsv) and [misprints.tsv](misprints.tsv) (`misprints.py
  ocr/en-purgatorio`: 1 row, 1 mark, 0 problems).

## Step 6: the comparison of the rest (2026-11-15)

The other 424 pages (`007`–`013`, `039`–`455`), compared at once, without batches.

- **The base**: la-el-agy in the same mode, in two runs from task files (`039`–`239`;
  `007`–`013` and `240`–`455`), workers writing about eight pages each.
- **The comparison**: `cmpread.py` with GLM-OCR as the second reading (`-i ia-ocr`,
  `--verse-numbers`): 1429 places (A 332, B 858, C 239). Mostly as in the trial: the
  marginal labels and running heads placed elsewhere, the accents GLM-OCR and Tesseract
  dropped, GLM-OCR's joined lines and repeated blocks (`225`). A second run with
  Tesseract's lines as the retype listed the places where Tesseract and Internet Archive
  read the same against the base and GLM-OCR. The places left after that filtering
  (about 60) were decided in the image; the 17 accents GLM-OCR and Internet Archive
  dropped against the base were all printed as the base has them.
- **Found**: 19 errors of the base (readcheck.tsv).
  - Spellings made modern: `condicion`, `agevolmente`, `ecstasy`, `poter`, `behooves`,
    `behooved`, `familiari`, `esempio` (twice), `ence` for `ance`.
  - Misprints corrected silently, now marked: `Hermaphoditus`, `pitv`, `Belaqua`.
  - Other misreadings: `Phililistines`, `p!unged`, `115-126`, `§ 1.`.
  - Lost text: a line (`067`, `fore robbest thou me?`) and a two-line note (`319`, note
    51).
- **Not compared here**: the paragraph breaks and the verse counts (step 4), the tables'
  line division.

## Step 7: the read-through (2026-11-15)

All 449 pages (`007`–`455`) read for sense in `ocr/` (no converter yet), in two passes:
first the doubtful places listed (168), then each decided in the image, 100 pages at a
time (GUIDE.md, step 3).

- **Misreadings** (70 rows of readcheck.tsv):
  - accents agy dropped where the `ì` is printed as a dotless `ı` with a faint accent
    (`sì`, `dì`, `così`, `partì`; 12);
  - the blank line before the page number or signature at the foot, missing on 43 of
    agy's pages from `240` on;
  - a missing paragraph break (`051`), stray quotes (`199`, `276`), `pescata`, `HoIy`,
    `--`;
  - the colon in citations written `N: N` on 5 pages that had `N : N` (printed spaced
    on both sides everywhere).
- **Misprints** (90 marks, misprints.tsv now 94 rows): tercet numbers (`146`, `3`, `117`,
  `93`, `35`); marginal labels (`Girone`, `Girone I` for II, `irone`); letters in the
  Italian (`motte`, `torcessse`, `piauger`, `sirrocchia`, `essse`, `Menrenti`, `verderti`,
  `n ciel`) and accents not printed (`ricomincio`, `giu`, `appario`); letters and spaces
  in the English (`woulds`, `Lonis`, `tnere`, `Tne`, `humanrace`, `fourages`, `feel`,
  `of of`, `I` printed twice); quotations (`erescit`, `beatudinem`); missing stops and
  quotes in the notes. Then (the user: what is clearly wrong is a misprint) 22 more of
  the places first kept: apostrophes set after the space (`s 'arrestasse`, `ond 'ei`,
  `guardere 'io`, `ch 'è`), missing spaces (`Fat,of`, `little,a`, `mesi,i.e.,`),
  `twixt` (twice), `la dolce assenzio`, `intelligence`, `remind`, stray or missing
  stops, and the editor's slips whose right form is sure (`Matt. xxviii. 46`,
  Euripides `480-441`, `De Vulg. El. 10: 12-16`).
- **Kept as printed**: Italian elisions set close (`d'udir`, `s'avviva`, 13) and split
  elisions before an enclitic (`rife' mi`, `leva' mi`, 18), the edition's way (PLAN.md,
  "Settled readings"). The places doubted and kept, 34, are rows `printed` of
  readcheck.tsv with the doubt in the note; those whose right form is not sure are
  marked `undecided` there: `Purg. xxviii. 121-12` (cut short, `069`), `Metam. xiv. 139`
  (`189`), the note numbers that differ from the verses (`159`, `160`, `173`, `238`),
  `§ I.` / `§ 2.`, `exchange of friends`, and two stops (`115`, `185`).

## Steps 1 and 2: the structure and the converter (2026-11-15)

- **The structure** (step 1): [INDEX.md](INDEX.md) from the page heads and the printed
  Index to Plates, Tables, etc. (p. 442): the front matter, the 33 cantos with their pages,
  the leaf where the notes begin and their first line, the plates, tables and diagrams, the
  end matter, the leaves left out. README.md has "Layout", "Transcription" and "Credits".
  The offset is constant (printed page = leaf − 12, pp. 2–443).
- **The converter made general** (step 2): `texts/scripts/convert_en_oelsner.py` keeps the
  settings of each volume apart (`INFERNO`, `PURGATORIO`) and takes the volume as an
  argument (`purgatorio`; the *Inferno* by default); `crop_en_oelsner_images.py` likewise.
  The *Inferno*'s output, its report and its seven images stay the same byte for byte.
  New for the *Purgatorio*: the running heads `*PURGATORIO*`, `DANTE’S PURGATORY` and
  `CHRONOLOGY OF “PURGATORIO”`; the diagrams printed below the notes of a page
  (`FIGURE_FROM`); the signature mark above the page number of `253`; italic spans
  joined across a line end (`ITALIC_JOIN`).

## Step 4: the mechanical checks (2026-11-15)

On the converted text, `texts/en-purgatorio/` (after the read-through, not before it as
the plan had it: the converter did not exist yet).

- **The verse count** of each canto: all 33 as in the standard text, no error.
- **The tercet numbers** printed in the Italian against the count: all agree. One number
  stands on the second line of its tercet, `134` on `170` (Canto XIII 133–134): the first
  line is long; printed so, and the converter computes the numbers.
- **The English paragraphs against the tercets**: the converter takes as many paragraphs
  as tercets begin on the facing page, and lists the English pages whose notes start
  without a verse number (23). All but one were notes continued from the Italian page;
  on `213` the canto's last line (`So turned he back…`, XVI 145) had a blank line before
  it, made a paragraph of its own: a misreading (readcheck.tsv).
- **The note paragraphs at a page top** after a finished sentence (9): decided in the
  image, continued (flush left) on 7 pages, new (indented) on `267`; listed in the
  converter.
- **Line-end hyphens**: 62 joins the word list could not decide, read through; 10 decided
  by hand (`HYPHEN_FIXED`).
- **The end matter**: on `451` the italics were reversed (the note is printed in italic,
  the titles and names in roman; the base had set every line in italic), rewritten; the
  signatures (`443`, `451`–`453`) and `PAGE` on `454` set apart by a blank line, as
  printed. 7 rows `misread` in readcheck.tsv in all.

## Step 8: the figures (2026-11-15)

`crop_en_oelsner_images.py purgatorio` cuts nine figures from the scan itself (clean, no
show-through) into `texts/en-purgatorio/images/`: the six diagrams below the notes (`024`,
`025`, `046`, `047`, `059`, `115`), the plate of the Zodiac (`071`) and the two pages of
the map (`388`, `389`), each without its caption; the boxes found from the ink of each
page and checked in a contact sheet. The family tables stay text. The labels of the
diagrams and the map stay as text, line by line, after the image.

## Step 9: the close (2026-11-15)

[SUMMARY.md](SUMMARY.md) written; README.md ("Credits"), INDEX.md, the root README,
ocr/README.md and texts/PLAN.md, texts/README.md, texts/scripts/README.md updated.
