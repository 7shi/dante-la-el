# Done: checking `ocr/en-oelsner`

The record of the check ([PLAN.md](PLAN.md)), step by step.

## Step 0: setup (2026-11-13)

- **Tables**: [misprints.tsv](misprints.tsv) (`page line printed fixed applied source
  note`) and [readcheck.tsv](readcheck.tsv) (`page line form decision note`), the columns
  of ocr/PLAN.md ("Decisions"). `misprints.py ocr/en-oelsner`: 0 rows, 0 marks, 0 problems.
- **`convert_en_oelsner.py`** taught the marks: `fixed()` with the regex of
  `convert_grc.py` (the corrigenda form included), applied to each page and to the hyphen
  vocabulary (of `ocr/en-oelsner` and `ocr/en`). Its report before and after, the
  baseline, is 22 lines `ENGLISH NOTES NOT STARTING WITH A NUMBER` (the continued notes
  of `023`–`401`); `texts/en-oelsner` unchanged.
- **Tesseract**: [tesseract/Makefile](tesseract/Makefile), as `ocr/en`'s (`-l eng+ita`),
  run over the 404 pages of `texts/en-oelsner`.
- **GLM-OCR**: [glm-ocr/Makefile](glm-ocr/Makefile), as `ocr/la`'s; run over all pages by
  the user. Tried on the six trial pages first: it repeated text (`024`, `025`), dropped
  a word (`014` `The`), normalized (`Eneid`; `403` a period after `10` that is not
  printed), and found nothing the retype and Tesseract did not.
- **`ocr/scripts/cmpread.py`**: the marks of bold and italics (`**`, `*`, `_`) dropped for
  every text; `--verse-numbers` drops a number of one to three digits at a line end, alone
  or in parentheses, in all three readings (the tercet numbers). Its output on `grc`
  retype 14 unchanged but for a stray `*` of Tesseract. Tried on a copy of `014`–`015`
  with a word changed, a label moved, the tercet numbers in other forms and an italic
  added: the word listed, the label as a pair of places, the rest not.
- **The shared tools** tried: `pages.py texts/en-oelsner 14 15` (the band markers, the
  labels as comments), `findline.py` (a phrase over a line-end hyphen on `014` 10–11, a
  phrase on a label's line, a phrase in italics on `024`), `txtfix.py` on a copy (a mark
  on a label's line, the label kept), `wordcrop.py` with the Tesseract boxes.
- **`cmpread.py -g`** (step 0.7): GLM-OCR as a fourth reading; class A when Tesseract or
  GLM-OCR agrees with the retype; class D where the base and the retype agree and
  Tesseract and GLM-OCR read the same other form; a GLM-OCR page outside 1.3 times the
  base's length left out. Tried: on copies of `015` with an error put in both the base and
  the retype (`stubbern`, a comma made a period), both listed as D; the labels both OCRs
  set elsewhere not listed; for D the ligatures folded (both OCRs write `Æneas` as
  `AEneas` or `Aeneas`, `058`). On the first 75 GLM-OCR pages, `011` (3.5 times the base)
  and `058` (1.9 times, its notes written twice) left out, the others within 0.87–1.05;
  the user ran the two again, and they are used. Without `-g`, the output
  on `grc` retype 14 and on retype 01 unchanged. `check_outlier.py` flags most Italian
  pages here (they have more lines than the English): not used.
- **[TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md)** for `en-oelsner`: lines as printed with the
  hyphens, the running heads, page numbers and signature marks; the labels `**Label**`;
  the tercet numbers and italics not written.

## Step 1–2: retype 01, the trial (2026-11-13)

- **Pages** (6): `014`, `015` (a canto's first spread: the argument, the labels, the verse
  and the English), `024` (notes), `025` (a map), `249` (a genealogical table, printed
  sideways), `403` (an essay with a footnote). Retyped by **Claude (Opus 5.5)** from the
  images alone, each page in three strips at twice its size (the table rotated).
- **Compared** (`cmpread.py --verse-numbers`): `014` and `015` without a difference; the
  map and the table differ in the order of their names, so they were read name by name in
  the image instead.
- **Decided** (readcheck.tsv, 10 rows):
  - **Misread**, 7: `025` the map rewritten as printed (the base had expanded `R.` to
    `River`, lowered the capitals, made `S. MARINO` and `MONTE FELTRO` one name, added a
    `River Ombrone` not on the map, and left out `R. Adige` and `R. Reno`); `249` four
    printed periods (`ESTE.`, `II.,`, `VIII.,`, `(nat.).`); `403` 40 `edited,` without
    the comma.
  - **Misprints**, 2 (misprints.tsv): `403` 16 `10` without its period before `The
    primary division`, and `024` 47 `117)` the last note of Canto I without its period;
    the base had added both.
  - **Printed**, 1: `403` 4 `THE`, small capitals after the drop capital, the base's case
    kept ("Settled readings").
- **The retype** erred in one place: `MONTE` written twice on the map (`MONTE S. MARINO`
  and `MONTE FELTRO`; the large `MONTE` belongs to `FELTRO`).
- **The trial's lessons**: the verse and the English of `014`–`015` agreed with the base
  word for word (they had been compared with dante-corpus and `texts/en`); the notes, the
  essays, the maps and the tables are where the base differs, and where it normalized. The
  batches are 25 pages.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`002`, `022`, `036`). `misprints.py`: 2 rows, 2 marks, 0 problems.

## Step 1–2: retype 02 (2026-11-13)

- **Pages** (25): `007`, `008`, `010`, `011`, `013` (the front matter), `016`–`023`,
  `026`–`037` (Cantos I–II, their notes, the diagram of Hell); the trial pages `014`,
  `015`, `024`, `025` left out. Retyped by **Claude (Opus 5.5)** from the images alone,
  in three strips at twice the size; the title-page imprint and the diagram enlarged
  further.
- **Compared** (`cmpread.py -g --verse-numbers`): 44 places, A 19, B 19, C 3, D 3. GLM-OCR
  was left out on `037` (47 tokens against the base's 62: the diagram).
- **Decided** (readcheck.tsv, 33 rows):
  - **Misread**, 26:
    - In the verse, where the base had normalized: `016` `sembiava` (was `sembrava`),
      `pelle` / `l' ora` (was `pelle.` / `L' ora`); `020` `Vedi` (was `VEDI`),
      `ammoglia` (was `ammòglia`); `028` `folle;`, `viltade` (was `viltàde`, a speck),
      `venni,`; `030` `l’ amico`; `034` `proposto` (was `proposito`).
    - In the English: `021` `Euryalus, and` and `wounds;`; `023` `o happy` (no quotation
      mark); `031` `my obeying,` and `forbearest` (was `forbears`); `035` `St Paul is
      called` (two words left out).
    - In the notes: `022` `Convito` twice (was `Convitio`); `034` `xii. 2` (no period;
      the sentence goes on overleaf).
    - Running heads: `022` `10` (was `IO`), `023` `11` (was `II`), `034` `22` (left out).
    - `021` a transcriber's note on a reader's pen mark removed.
    - `011` the imprint: raised dots between all the words and letters (`J · M`, `W · C`),
      none after `CO:`.
    - `037` the diagram rewritten as printed (as `025`): no heading (`MAP OF HELL` was
      show-through), raised dots, the circles `0`–`7`, `VIII`, `IX` (the base had `1.`–`7.`,
      `VIII.`–`XII.`).
  - **Misprint**, 1 (misprints.tsv): `034` 47 `vi` without its period (`Æn. vi 757`); the
    base had added it.
  - **Printed**, 6: `013` the library's stamped number, kept; `019` two class D places (a
    label set elsewhere by both OCRs); `026` `sì` (class D, both OCRs `si`); `020` and
    `028` the page number on its own line in the base; `022` the asterism written `* * *`.
- **The retype** made no error in the words; it left out the stamped number on `013`.
- **Unlike the trial**, the verse had misreadings the comparison with dante-corpus had
  passed (`sembrava`, `proposito`, `ammòglia`, `viltàde`): the base had taken the
  standard form where the edition prints another.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`001`, `002`, `003`). `misprints.py`: 3 rows, 3 marks, 0 problems.

## Step 1–2: retype 03 (2026-11-13)

- **Pages** (25): `038`–`062` (Cantos III–IV, the opening of Canto V). Retyped by
  **Claude (Opus 5.5)** from the images alone, in three strips at twice the size.
  Before the deciding, the GLM-OCR pages that had repeated a note (`123`, `144`, `156`,
  `190`, `212`, `213`) were run again by the user; none repeats now.
- **Compared** (`cmpread.py -g --verse-numbers`): 35 places, A 22, B 8, C 1, D 4. No
  GLM-OCR page left out.
- **Decided** (readcheck.tsv, 35 rows):
  - **Misread**, 23:
    - In the verse: `044` `similemente` (was `similmente`); `048` `discernea`; `050`
      `ubbidiente;`; `052` `poeta;`; `054` `volsersi`, `Traemmoci`; `056` `quale,`, `si`
      (was `sì`); `060` `cinghia`, `essa;`, `vuolsi` (were `cinghìa`, `vuolsì`).
    - In the English and the arguments: `039` `a great River` (the scan cuts the
      letter; was `the`), `glaring` (was `flaring`); `046` `medieval` (was `mediæval`).
    - In the notes: `047` the two dots after `fece` (the base had four); `056` `1 Peter`
      (was `I`), `Nicod.,`; `058` `106-110.` (was `105`), `sqq.` twice (was `199.`),
      `510` (was subscript).
    - The labels: `049` no period after `slumber`.
    - `048` a transcriber's note on a reader's pen mark removed.
  - **Misprint**, 3 (misprints.tsv): `038` the label `Porta dell` / `Inferno` without the
    apostrophe; `042` `tastidiosi` (v. 69); `062` `comforta` (v. 44). The base had
    corrected all three.
  - **Printed**, 9: four class D places (`039` `demon`, cut by the scan edge; `042` `sì`,
    `044` `costì`, `060` `Così`, accents both OCRs lack); `040`, `054`, `058` the page
    number on its own line in the base; `039` the opening single quote and `052`
    `quando’`, where the retype was wrong.
- **The retype** made three errors: `“` for the printed `‘` (`039`), `quando` for
  `quando’` (`052`), three dots for two (`047`).
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`004`, `005`, `006`). `misprints.py`: 6 rows, 6 marks, 0 problems.

## Step 1–2: retype 04 (2026-11-13)

- **Pages** (25): `063`–`087` (the rest of Canto V, Canto VI, Canto VII to v. 81).
  Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at twice the
  size.
- **Compared** (`cmpread.py -g --verse-numbers`): 27 places, A 13, B 7, C 0, D 7. No
  GLM-OCR page left out.
- **Decided** (readcheck.tsv, 27 rows):
  - **Misread**, 16:
    - In the verse: `064` `Cleopatras` (was `Cleopätras`), `colombe,`; `068` `morisse;`;
      `074` `fiacco;`; `078` `E il duca` (was `E 'l`).
    - In the English: `073` `tormented` (missing); `083` `all,` (was `all, and`), `fear
      hurt` and `he shall` (missing); `087` no closing quote after `souls.` (Virgil's
      speech goes on).
    - In the notes: `068` `Æneas` twice (was `Aeneas`), `Sichæus`; `077` a speck in the
      margin read as `.`; `079` `Guelfs` (was `Guelſs`); `081` `but,`.
  - **Misprint**, 1 (misprints.tsv): `080` `parte selveggia` in the note on vv. 64-69
    (`selvaggia` in v. 65); the base had corrected it.
  - **Printed**, 10: five class D places (`067` `Caïna`, `078` `udirà`, `Sì`, `084` `lì`,
    accents both OCRs lack; `085` `surge wherewith`, run together by both); `067`, `075`
    and `083` labels placed elsewhere; `074`, `086` the page number on its own line in
    the base.
- **The retype** made no error the comparison found. Two printed forms that base and
  retype share are left for the read-through: `070` `shore or the Adriatic` (`of`?) and
  `072` `dell’ un de lati` (`de’`?).
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`006`, `007`, `008`). `misprints.py`: 7 rows, 7 marks, 0 problems.

## Step 1–2: retype 05 (2026-11-13)

- **Pages** (25): `088`–`112` (the rest of Canto VII, Cantos VIII and IX, the opening of
  Canto X). Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at
  twice the size (`100`, a short page, from a crop of its lower half).
- **Compared** (`cmpread.py -g --verse-numbers`): 27 places, A 22, B 2, C 0, D 3. No
  GLM-OCR page left out.
- **Decided** (readcheck.tsv, 26 rows; the two places of `093` `[through the water]` in
  one):
  - **Misread**, 20:
    - In the verse: `090` `‘Tristi` (was `“Tristi`); `092` `senno;`, `quella,`; `094` no
      closing quote after `incinse.` (the speech goes on); `106` `sponde;` (was
      `sponde:`), `rattento` (was `rattenro`), `Gli occhi` (was `Gliocchi`), `volsimi`
      (was `volsmi`); `110` `eresiarche` (was `eresiarchi`), `e sepolto` (was `è`).
    - In the argument and the English: `093` `summit,` (was `summit, and`), `turn[ed]`,
      `[through the water]` (brackets missing); `102` `DANTE` (was `D ANTE`, a drop
      capital); `105` the label's `Furies` set at the end of a line.
    - In the notes: `090` `sino a'` (apostrophe missing), `Convito` (was `Convivio`);
      `100` note `68.` (was `63.`); `111` `the angel` (was `Angel`).
  - **Misprint**, 1 (misprints.tsv): `101` `punished Within` in the note on v. 68, the
    period not printed; the base had added it.
  - **Printed**, 6: three class D places (`090` `Cf`, `098` `sicurtà`, `102` `sì`); `094`,
    `106` the page number on its own line in the base; `093` `Phlegyas` (below).
- **The retype** made one error: `093` an opening quote before `Phlegyas, Phlegyas,”`,
  added from the sense; none is visible (the line starts in the gutter shadow).
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`008`, `009`, `010`). `misprints.py`: 8 rows, 8 marks, 0 problems.
