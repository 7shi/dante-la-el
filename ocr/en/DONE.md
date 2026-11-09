# Done: checking `ocr/en`

The record of the check of `ocr/en` planned in [PLAN.md](PLAN.md), step by step.

## Step 0: setup (2026-11-08)

- **Tables**: [misprints.tsv](misprints.tsv) (`page line printed fixed applied source
  note`) and [readcheck.tsv](readcheck.tsv) (`page line form decision note`), the columns
  of `ocr/la` (ocr/PLAN.md, "Decisions"); empty.
- **The baseline** of `texts/scripts/convert_en.py`, before any change: `texts/en` as
  committed (`e4b60b88`), and its output, no `ERROR` and no `NO MARKERS` line, eight
  `HYPHEN` lines (the undecided joins across a page break):

  ```
  HYPHEN 021->022: fur-nish -> furnish
  HYPHEN 081->082: un-ceasing -> unceasing
  HYPHEN 149->150: con-jured -> conjured
  HYPHEN 207->208: in-sanest -> insanest
  HYPHEN 281->282: ar-gumentum -> argumentum
  HYPHEN 295->296: fellow-citizens -> fellow-citizens
  HYPHEN 314->315: castle-signals -> castle-signals
  HYPHEN 418->419: ver-dant -> verdant
  ```

- **`convert_en.py`** taught the misprint marks: `fixed()` as in `convert_la.py`, applied
  to each page and to the hyphen vocabulary. Its output and `texts/en` unchanged.
- **`misprints.py`** moved from `ocr/la/scripts/` to [ocr/scripts/](../scripts/README.md),
  taking the directory (`uv run ocr/scripts/misprints.py ocr/en`); the page names are the
  digits of the page files (four in `la`, three in `en`). `ocr/la`: 1,053 rows, 1,050
  marks, no problems, as before; `ocr/en`: no rows, no marks.
- **Tesseract**: [tesseract/Makefile](tesseract/Makefile), `-l eng+ita`, over the pages of
  `texts/en` (taken from its page markers): 469 TSVs; four nearly empty, the pages with
  a title only (`005`, `006`, `010`, `477`).
- **The shared tools** tried on `ocr/en`:
  - `pages.py texts/en 55 57`: the pages cut at the markers `<!-- p. [1] (055) -->`, the
    front matter and the index (`<!-- p. [423] (477) -->`) too.
  - `findline.py ocr/en`: phrases found in prose, verse notes and the index; a phrase
    across a page break was not found, as the prose that runs over the page is printed
    above the verse and the notes. Taught to join each line of a page with the first line
    of the next (`063` `Grey-` / `064` `hound`: `063 3-064:1`).
  - `txtfix.py ocr/en` (a dry run, `-n`): a row applied to `072`; nothing written.
  - `wordcrop.py ocr/en … -t ocr/en/tesseract`: bands of the verse (`072` `Lontana`), the
    prose (`063` `Grey`) and the two columns of the index (`479`); a narrow page is padded
    in black on the right. A word Tesseract reads otherwise is not found (`056` `Chè`,
    read `Ché`; 0 hits): a word beside it is asked for instead.
- **`ocr/scripts/cmpread.py`** (step 2), written while the trial retype runs; tried on
  pages altered by hand: a changed word, a lost verse line (class C), a mark's printed side
  and Tesseract's agreeing word (class A) found; spacing, quotes and the note markers
  ignored; a retype identical to the base gives no place. Tesseract's words hyphenated at a
  line end are joined.
- **The retype template**: [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md), from `la`'s: the
  conventions of [README.md](README.md) and the errors of `la`'s retypes; output
  `tmp/en-retypeNN/PAGE.txt`.

## Step 1: retype, the trial (2026-11-08)

- **Retype 01** (la-el-agy, Gemini 3.8 Flash): `011`, `055`, `072`, `454`, `479`, all five
  written, none mixed up; the blocks, the verse, the verse note, the continued notes and the
  two index columns as the template asks.
- **`cmpread.py`**: 3 places, all class B, none A or C:
  - `011` `The` (the retype `THE`) and `479` `Abati` (`ABATI`): small capitals, the first
    word of a section in normal case (README.md): printed.
  - `055` `Lion`: the print has `Licn` (a `c` for the `o`), which the retype copied and
    Tesseract read `Lion`: a misprint, marked `{{Licn|Lion}}` and listed.
- No letter, word or mark of the retype against the print; the only kind of difference
  is the small capitals of a first word, which the base writes in normal case. Spacing set
  aside by the script (`072` the print's `wounded(Conv.Tr.`, written so by the retype).
- After the fixes: `misprints.py ocr/en`, 1 row, 1 mark, no problems; `convert_en.py` as
  the baseline, `texts/en` unchanged.
- Tesseract alone against the base is not listed: the trial gives it nothing to find.
- The batch size: 10 pages.
- **Retype 02** (Gemini 3.8 Flash): `005`, `009`, `010`, `012`–`018`, the title pages and
  the preface. One place, class A: `010` the base `C.`, the retype and Tesseract `C`; no
  period in the print: a misprint, marked `{{C|C.}}` and listed.
- Fifteen pages, no misreading of the base; the two finds are misprints the base had
  corrected silently, which `texts/en` corrects anyway (the user, 2026-11-08). But twelve
  of the fifteen were the front matter: retype 03 takes ten canto pages across the book
  (`095`, `136`, `175`, `215`, `255`, `295`, `335`, `375`, `415`, `445`), to decide whether
  the retype goes on.
- **Retype 03** (Gemini 3.8 Flash): ten canto pages across the book. One place, class A:
  `375` the verse `Pure ei pareva`, the retype and Tesseract `el`, as printed: a misread,
  corrected (`texts/en/033-canto-27.md` with it). The first misreading of the base: in the
  Italian, a word that still makes sense, which the comparison with dante-corpus let pass.
  The verse quotations in the notes (`255`, `415`) the retype set one verse per line, the
  base in one line: the layout only, set aside by the script.
- **Retype 04** (Gemini 3.8 Flash): 25 pages of the front matter, `019`, `021`–`044`; all
  written, none mixed up. 24 places (A 10, B 14, C 0):
  - Small capitals written in normal case by the base, against README.md ("Small
    capitals in running text are written in uppercase"): `DIVINA` (`023`, `027`), the
    titles of `026` and `027`, `MS.`/`MSS.` (`029`, `032`), `IS`, `MANY YEARS`, `OTTIMO`
    (`034`), `TRANSLATIONS` (`043`); corrected, and `272` `MSS.`, the last `mss` of the
    base, after its image.
  - `041` `1329;`: a colon in the print, corrected.
  - The retype wrong, the base as printed: `022` `Sì` (the retype `S̄i`, the accent set
    over the `S`) and `davanti` (`dauanti`), `029` `Cⁱ` (`Ci`), `032` `. . .` (`.`).
- **Retype 05** (Gemini 3.8 Flash): 25 pages, `045`–`054`, `056`–`070`; all written, none
  mixed up. 6 places, all B, no misreading of the base:
  - Misprints the base had left unmarked or corrected: `059` `coso` for `cose` (the verse,
    Inf. i. 40; the retype wrote `cose`), `051` `entrauce` (a turned `n`; the base wrote
    `entrance`). Marked and listed.
  - The retype wrong: `052` `rolling-dead` (a speck), `058` `só` (a speck), `066`
    `lascerò` for `lascierò`, `069` `. . .` for `. . . .`.
- **Retype 06** (Gemini 3.8 Flash): 28 pages, `071`, `073`–`094`, `096`–`100`; all written,
  none mixed up. 11 places (A 3, B 8, C 0):
  - Misreadings of the base: `081` `clear-ness` and `092` `quantum-cumque` (breaks at a
    line end kept), `096` `. . .` twice for printed `. . . .`. Corrected.
  - Misprints the base had corrected: `079` `accompauied`, `081` `aud`, `094` `darkuess`
    (turned `n`s), `096` `tco`. Marked and listed.
  - The retype wrong: `081` a speck read `.`, `083` `secmed`, `086` `;` for `:`, `099`
    `Heraclitus` for `Heraclítus`.
- **Retype 07** (Gemini 3.8 Flash): 24 pages, `101`–`124`; all written, none mixed up.
  5 places (A 2, B 3, C 0):
  - Misreadings of the base: `124` `PAPÈ`, the first word of Canto VII in small capitals,
    in the prose and the verse; written in normal case, the verse without the accent, as
    printed (`Papè`, `Pape`).
  - A misprint the base had corrected: `123` `chant` (the period did not print). Marked and
    listed.
  - The retype wrong: `104` `sun-light` (a break at a line end), `121` `,` for `.`.
- **Retype 08** (Gemini 3.8 Flash): 24 pages, `125`–`135`, `137`–`145`, `147`–`150`; all
  written, none mixed up. 10 places (A 4, B 6, C 0):
  - A misreading of the base: `139` `. . .` for printed `. . . .`. Corrected.
  - Misprints the base had corrected: `125` `erowds`, `126` `mect`, `129` `forth` (no
    period), `139` `Aud` (a turned `n`) and `diri` (Seneca's `dira`), `148` `ìl`; and `132`
    `piedo`, which the base had copied unmarked. Marked and listed.
  - The retype wrong: `127` `squint-eyed` (a break at a line end), `132` `vastáque` (an
    italic circumflex), `139` `Tor` (an `F` with a broken arm).
- **Retype 09** (Gemini 3.8 Flash): 24 pages, `151`–`174`; all written, none mixed up.
  6 places, all B:
  - Misreadings of the base: `151` `Vèr`, `156` `vèr`, `158` `vòlto`, where the print has
    a circumflex (`Vêr`, `vêr`, `vôlto`); `160` six points for printed seven. Corrected.
  - The retype wrong: `166` `soall` (an `h` whose ascender did not print), `169`
    `sappiamo` for `sapiamo`.
- **Retype 10** (Gemini 3.8 Flash): 24 pages, `176`–`183`, `185`–`200`; all written, none
  mixed up. 17 places (A 3, B 14, C 0), no misreading of the base:
  - Misprints the base had corrected: `177` `sccond`, `181` `tby` and `sentenza.` (the verse
    runs on), `183` `rcceive`, `187` `&c` (no period), `188` `gìa`, `197` `Fredcrick`,
    `199` `fædissima` (an italic `æ`). Marked and listed.
  - The numbers of two notes did not print (`177`, `187`); the base keeps them, as the text
    has their markers.
  - The retype wrong: `183` `fœ` for an italic `æ` (twice), `187` and `191` `Ovid,`, `191`
    and `194` `È` for the print's `E` and a grave, written `E’` by the base throughout.
- **`101`–`200` done** (retypes 07–10, 96 pages): misreadings of the base in `124`, `139`,
  `151`, `156`, `158`, `160` (a canto's first word in small capitals, circumflexes read as
  graves, points); the rest misprints the base had corrected, and the retype's own errors,
  a few a batch.
- **Retype 11** (Gemini 3.8 Flash): 24 pages, `201`–`214`, `216`–`225` (`210` blank); all
  written, none mixed up. 6 places (A 1, B 5, C 0), no misreading of the base:
  - Misprints the base had corrected: `213` `Lit..` (a period for the colon), `220` `uot`.
    Marked and listed.
  - The retype wrong: `214` `Com` (the period set close), `222` `dietro` for `diretro`,
    `225` `eye-brows` (a break at a line end).
- **Retype 12** (Gemini 3.8 Flash): 24 pages, `226`–`249`; all written, none mixed up.
  9 places (A 4, B 5, C 0):
  - A misreading of the base: `244` `Guido-guerra`, a break at a line end kept
    (`Guidoguerra` elsewhere). Corrected.
  - Misprints the base had corrected: `229` `carth`, `233` `arisiug`, `239` `Viuse`
    (Inf. xvi. 50), `243` `Po` (no period), `246` `17` (Rev. xi. 7), `248` `avca`
    (Inf. xvii. 11). Marked and listed.
  - The retype wrong: `236` `Gia’` for the small capitals `GIA` and a grave set after
    them (`Già`), `247` `lenve`.
- **Retype 13** (Gemini 3.8 Flash): 24 pages, `250`–`254`, `256`–`274`; all written, none
  mixed up. 11 places (A 3, B 8, C 0):
  - Misreadings of the base: `261` `imagine` for printed `immagine`, `270` `Thr.` and `Gn.`
    in small capitals (`THR.`, `GN.`), `272` `. . .` for printed `. . . .`. Corrected.
  - Misprints the base had corrected: `260` `belt,’` (a single closing quote), `269` `nou`
    (Inf. xviii. 117), `270` `me!” .` (a period after the quote), `273` `Giovanui`
    (Inf. xix. 17); and `270` `sozzo` (Inf. xviii. 130) and `272` `delle` (Inf. xix. 8),
    which the base had copied unmarked. Marked and listed.
  - The retype wrong: `251` `accorsi,` (a broken `i`, no comma), `258` `udì` for `udi’`,
    `265` `leggiermente`.
- **Retype 14** (Gemini 3.8 Flash): 25 pages, `275`–`294`, `296`–`300` (`284`, `298`
  blank); all written, none mixed up. 9 places (A 2, B 7, C 0):
  - Misreadings of the base: `279` `three-score`, a break at a line end kept (`threescore`,
    as `056` and 2 Macc. iv. 8), `300` `marvelously` for printed `marvel-` / `lously`.
    Corrected.
  - Misprints the base had corrected: `291` `betwecn`, `296` `herbs’`. Marked and listed.
  - The number of a note did not print (`292`); the base keeps it.
  - The retype wrong: `285` `Forlì` for `Forli`, `290` `giò` for `gìo`.
- **`201`–`300` done** (retypes 11–14, 96 pages): misreadings of the base in `244`, `261`,
  `270`, `272`, `279`, `300` (line-end breaks, small capitals, a doubled letter, points);
  the rest misprints the base had corrected or copied unmarked, and the retype's own
  errors, a few a batch.
- **`readcheck.tsv`** for retypes 11–14: the rows of their places had not been written;
  added with retype 15.
- **Retype 15** (Gemini 3.8 Flash): 25 pages, `301`–`325` (`312` blank); all written, none
  mixed up. 9 places (A 7, B 2, C 0):
  - Misreadings of the base: `308` `Scarmiglione` for printed `Scaramiglione` (so the index,
    `485`; the verse `Scarmiglione`), `309` `Trample-grace` and `far-falla`, `317`
    `house-hold`, breaks at a line end kept. Corrected.
  - Misprints the base had corrected: `301` `Lit..` (as `213`), `314` `tho`, `319` `Poeo`
    (Inf. xxii. 67). Marked and listed.
  - The retype wrong: `314` `HAVE`, the opening of a canto in small capitals.
- **Retype 16** (Gemini 3.8 Flash): 25 pages, `326`–`334`, `336`–`351`; all written, none
  mixed up. From `343` on (but `349`), eight pages written line by line as printed: the
  verse numbers, the breaks at a line end, the two columns of the footnotes side by side
  (`|`). Compared after a normalization (the numbers dropped, the columns read one after
  the other, the breaks joined): 14 places (A 2, B 12, C 0):
  - Misreadings of the base: `328` `compiò` for printed `compìo`, `336` `costa` without its
    comma. Corrected.
  - Misprints the base had corrected: `328` `casc`, `rendcre` (Inf. xxiii. 34) and
    `describcd`, `329` `rcached`, `330` `somc`, `339` `cantc`; and `350` `Lit..`, which
    the base had copied unmarked. Marked and listed.
  - The retype wrong: `338` `ὣ` (the breathing not clear; the base kept), `344` a speck,
    `349` `trans-formations`, `350` `AT`, `AL` (the opening of a canto).
- **Retype 17** (Gemini 3.8 Flash): 25 pages, `352`–`374`, `376`–`377`; all written, none
  mixed up, in the layout asked. 11 places (A 1, B 10, C 0):
  - Misreadings of the base: `353` `ecco,` and `365` `Elisha,`, a period in the print.
    Corrected.
  - Misprints the base had corrected: `363` `skort`, `368` `Foichè` (Inf. xxvi. 76); and
    `352` `Por` (Inf. xxv. 29) and `374` `un-confuso` (Inf. xxvii. 6), which the base had
    copied unmarked. Marked and listed.
  - The retype wrong: `355` `già` for `gìa`, `360` a speck, `365` `levoron`, `374` `THE`
    (the opening of a canto), `377` `Malatestino` for `Maltestino`.
- **Retype 18** (Gemini 3.8 Flash): 23 pages, `378`–`400` (`398` blank); all written, none
  mixed up, in the layout asked. 7 places (A 3, B 4, C 0):
  - A misreading of the base: `390` `round;`, a colon in the print. Corrected.
  - Misprints the base had corrected: `378` `Imolo`, `397` `cach`. Marked and listed.
  - The retype wrong: `380` `loosened` for `losened`, `384` `partìo` for `partio`, `396`
    `’` (a closing quote broken).
- **`301`–`400` done** (retypes 15–18, 98 pages): misreadings of the base in `308`, `309`,
  `317`, `328`, `336`, `353`, `365`, `390` (line-end breaks, a letter, an accent, points);
  the rest misprints the base had corrected or copied unmarked, and the retype's own
  errors, a few a batch.
