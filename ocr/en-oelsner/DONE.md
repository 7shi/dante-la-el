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

## Step 1–2: retype 06 (2026-11-13)

- **Pages** (25): `113`–`137` (the rest of Canto X, Canto XI with the zodiac diagram
  `133`, the opening of Canto XII). Retyped by **Claude (Opus 5.5)** from the images
  alone, in three strips at twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 29 places, A 9, B 16, C 2, D 2. No
  GLM-OCR page left out. After the fixes, 23 places: the diagram `133` (its lines in
  another order; GLM-OCR left out there, 81 tokens against the base's 128), two page
  numbers and six class D places, all as printed.
- **Decided** (readcheck.tsv, 23 rows; the seven places of `133` in one row, the label of
  `119` in two):
  - **Misread**, 18:
    - In the verse: `124` `Fotin` (was `Fotín`); `126` `coscïenza`, `128` `spezïal`
      (the diaeresis missing); `130` `note,` (was `note’`); `134` `discoscesa` (was
      `discoscęsa`); `136` `gìa` (was `già`).
    - In the argument and the English: `119` the label `Prophetic vision of those in
      Hell` (split in two, `those in Hell` four lines below); `135` `All` (a stray quote
      before it).
    - The first letters cut by the scan edge, decided by the room, the stroke left and
      the sense: `135` `for from` (was `or`), `such` (was `Such`); `137` `so`, `on`,
      `the` (were capitals) and `But` (was `but`, a new sentence).
    - In the notes: `120` `in this verse,` (left out at the start of a line); `132`
      `sqq.` (was `199.`), `ii. 15` (was `ii. 5`).
    - The diagram `133` rewritten as printed, as `037`: raised dots, not periods
      (`·S·`, `·HORIZON`), and the times `10 p·m·`, `6 a·m·` (the base `10pm`, `6am`).
  - **Misprint**, 0.
  - **Printed**, 4: two class D places (`116` a straight apostrophe, `131` the label
    `Usury` set in the text); `120`, `130` the page number on its own line in the base.
- **The retype** made no error found by the comparison.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`011`, `012`, `013`). `misprints.py`: 8 rows, 8 marks, 0 problems.

## Step 1–2: retype 07 (2026-11-13)

- **Pages** (25): `138`–`162` (the rest of Canto XII, Canto XIII, the opening of Canto
  XIV). Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at twice
  the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 40 places, A 26, B 10, C 0, D 4. No
  GLM-OCR page left out. After the fixes, 10 places, all decided.
- **Decided** (readcheck.tsv, 26 rows; the verse numbers of `154` in one, each moved
  label in one):
  - **Misread**, 17:
    - In the verse: `148` `dovrebb’` (was `dovrebbi'`); `152` `spelta;` (the semicolon
      missing), `Arpíe` (the accent missing); `154` `sanguinenti` (was `sanguimenti`),
      `miè` (was `mie`), the verse numbers written `^121` (11 lines); `158` `a randa`
      (was `a' randa`, a speck); `160` `l’ eternale` (was `l'etternale`).
    - In the English: `153` `again:` (was `again;`), `like` (was `Like`; the scan cuts
      the first letter); `155` `braches` (was `branches`).
    - The labels: `149` `Pier delle Vigne`, `155` `Florence` and `161` `Their
      punishment` each on the wrong line; `159` a stray `plain` (from the label `The
      sandy plain`) removed.
    - In the notes: `144` `. .` (was `. . .`); `145` `Æn.` (was `Aen.`).
  - **Misprint**, 1 (misprints.tsv): `150` `taccia` for `faccia` (v. 85), the first
    letter printed as `t`, as `042` `tastidiosi`; the base had kept the printed form.
  - **Printed**, 8: three class D places (`138` `morì`, `152` `sì`, `158` `già`) and
    `141` the label `Murderers` set in the text by the others; `139` the label `The
    Centaurs` (between two lines; the base's place kept); `143` the label
    `Highway-men` (printed over two lines; the column would hold the word unbroken, so
    the hyphen is kept); `144`, `160` the page number on its own line in the base.
- **The retype** made three errors: `139` the label `The Centaurs` one line higher (it
  stands between the lines); `143` `Highwaymen` (the hyphen dropped); `150` `faccia`
  from the sense (the misprint above).
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`013`, `014`, `015`). `misprints.py`: 9 rows, 9 marks, 0 problems.

## Step 1–2: retype 08 (2026-11-13)

- **Pages** (25): `163`–`187` (the rest of Canto XIV, Canto XV, Canto XVI to v. 123).
  Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at twice the
  size.
- **Compared** (`cmpread.py -g --verse-numbers`): 38 places, A 26, B 9, C 0, D 3. No
  GLM-OCR page left out. After the fixes, 12 places, all decided.
- **Decided** (readcheck.tsv, 35 rows):
  - **Misread**, 24:
    - In the verse: `164` `si` (was `sì`); `174` `opera`, `rimaser` (were `opra`,
      `rimasèr`); `176` `servo` (was `serva`, under a pencil stroke), `'Tesoro,'` (was
      `'Tesoro',`); `180` `Ricominciar` (was `Ricomminciar`); `182` `fussi` (was
      `fossi`); `184` `disse` (was `disse,`); `186` `parve`, `discoscesa` (were `parvé`,
      `discosesa`).
    - In the English: `163` `breast.` (no closing quote printed); `171` `ere` (was
      `where`), `in` (was `In`); `173` `“There`; `183` `, more` (left out at the line
      end); `185` `tell` (was `Well`), `“The`, `and the` (was `and, the`), `“If`, `see`
      (was `See`); `187` `"Surely,"`. Most at the left edge, where the scan cuts the
      first letter or the quote.
    - In the notes: `169` `in Crete,` left out (and `‘old man’` given quotes not printed),
      `.` (was `. . .`; one dot printed); `179` `by Dante` left out at the line end.
  - **Printed**, 11: six page numbers on their own line in the base (`164`, `168`,
    `172`, `174`, `176`, `182` — `172` after the running head); three class D places
    (`169` `Æn.`, `172` `sì`, `tenea`); `169` `17-21` (the retype broke it at the line
    end as printed); `185` `For` (the first letter cut; the base's capital kept, as
    `texts/en`).
- **The retype** made no clear error; `185` `for` (a cut capital) was a judgment the
  base's reading decided.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`015`, `016`, `017`). `misprints.py`: 9 rows, 9 marks, 0 problems.

## Step 1–2: retype 09 (2026-11-13)

- **Pages** (25): `188`–`212` (the end of Canto XVI, the map of Romagna, Canto XVII,
  Canto XVIII). Retyped by **Claude (Opus 5.5)** from the images alone, in three strips
  at twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 39 places, A 15, B 17, C 0, D 7. No
  GLM-OCR page left out. After the fixes, 18 places, all decided.
- **Decided** (readcheck.tsv, 30 rows):
  - **Misread**, 22:
    - In the verse: `188` `Commedìa`; `200` `falconiere` (was `Falconiere`) and the
      dash after `cali!”`; `206` `apprese` (no colon printed), `conio.”` (the quote left
      out); `208` `viene`, `soprasta` (were `vienè`, `soprastà`), a stray `òl;` after
      `senno`; `210` `riguardar` (was `rigurardar`).
    - In the English: `195` `breeses` (was `breezes`); `199` `then`, `there`, `nor`,
      `than` (the scan cuts the first letters; the base had `Then`, `here`, `or`,
      `Than`); `201` `so`; `203` `well,` (was `well;`, a speck); `209` `what`.
    - In the notes: `200` `Guelfs`, `Ubbriachi` (were `Guelphs`, `Ubriachi`).
    - The signature marks `M` (`189`) and `N` (`205`) left out; on `205` the page
      number `193` was at the foot, now beside the running head.
    - The map (`191`): the lower `R. Po` left out.
  - **Misprint**, 1 (misprints.tsv): `189` `decription` for `description` (note 94-102);
    the base had corrected it silently.
  - **Printed**, 7: two page numbers on their own line (`188`, `208`); `196` `sì` (the
    accent worn; the retype `si`); `202` `Every` / `thing` (the line end cut, as
    `texts/en`); `206` `la`, `207` `us,` (class D, specks); `207` `If` (the first
    letter cut; the base's capital kept, as `texts/en`).
- **The retype** made one error: `196` `si` (the worn accent read as none).
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`017`, `018`, `019`). `misprints.py`: 10 rows, 10 marks, 0 problems.

## Step 1–2: retype 10 (2026-11-13)

- **Pages** (25): `213`–`237` (the end of Canto XVIII, Canto XIX, Canto XX). Retyped by
  **Claude (Opus 5.5)** from the images alone, in three strips at twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 59 places, A 36, B 11, C 1, D 11. No
  GLM-OCR page left out. After the fixes, 16 places, all decided.
- **Decided** (readcheck.tsv, 49 rows):
  - **Misread**, 34:
    - In the verse: `218` `‘Non` (was `“Non`), `Laggiù` (was `Lagguìù`), `coi` (was
      `co’`); `220` `‘Maccabei’` (the opening quote left out), `retro.’`, a stray `dì`
      before `chè`; `222` `si` (was `sì`); `226` the tercet numbers 4–16 written at the
      line starts (5 lines); `228` `Teban`, the handwritten note `(handwritten: ? /)`
      removed; `230` `dove nacqu’` (was `do m’acqu’`, a stain), `gìo`, `discese.`;
      `232` `mattìa`.
    - In the English: `213` `magnas,`; `214` `(1-12)`; `215` `you:`, `on the` left out;
      `219` the label `Boniface VIII.` two lines low, a stray `then`; `227` `the` left
      out; `229` the label `Amphiaräus` five lines low, `looks` (was `looks,`),
      `Carrarese`; `231` `hair[y skin]`, `[A]pennine` (the brackets left out); `235`
      `remember:`.
    - In the notes: `223` `lo scritto` (was `Io`); `235` `Tignalga`, `Mincio` (were
      `Tignaga`, `Minicio`); `236` `ii:`, `Tragedia`, `tragediam`, `comediam` (were
      `Tragœdia` etc.).
    - The signature marks `O` (`221`) and `P` (`237`) left out.
  - **Misprint**, 1 (misprints.tsv): `234` the label `Cerchio VII.` for `VIII.`; the
    base had it as printed, now marked.
  - **Printed**, 14: four page numbers on their own line (`216`, `220`, `228`, `232`);
    class D accents and stops (`213` `.`, `216` `sì`, `217` `:`, `218` `costì`, `228`
    `sì` twice, `232` `altrimenti`, `234` `malìe`, `237` `Forlì`); `229` the labels
    `Tiresias`, `Aruns`; `234` `113` (the comparison's verse-number reading).
- **The retype** made no clear error.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`019`–`021`). `misprints.py`: 11 rows, 11 marks, 0 problems.

## Step 1–2: retype 11 (2026-11-13)

- **Pages** (25): `238`–`262` (Canto XXI, Canto XXII, the table of the House of Este,
  the opening of Canto XXIII). Retyped by **Claude (Opus 5.5)** from the images alone,
  in three strips at twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 40 places, A 33, B 6, C 0, D 1. No
  GLM-OCR page left out. After the fixes, 5 places, all decided.
- **Decided** (readcheck.tsv, 32 rows):
  - **Misread**, 26:
    - In the verse: `238` `Commedìa`; `242` `atuffare`; `244` `quatto quatto`, `face.`
      (no closing quote); `246` `Calcabrina`, `Ciriatto` (also `254`); `252`
      `impegolate`; `254` `sdrucia.`, `inforco.”`; `256` `digrigna;`, `Farfarello` (no
      comma), `l’ali;`; `258` `Irato`.
    - In the English: `241` `compressed` left out (two lines joined), `writhing
      convolved` (was `` `writhing` convoluted ``); `245` `cliff`; `247` `Calcabrina`,
      `Ciriatto`; `251` the argument joined into one line, restored; `253` `ship:`,
      `servant of a lord` (the quotes were specks); `257` `come.` (no closing quote);
      `259` `All` (was `Each`), `flying after` left out.
    - In the notes: `260` a stray `¶` before four notes; `261` `at` (was `At`).
    - The signature mark `Q` (`253`) left out.
  - **Misprint**, 1 (misprints.tsv): `239` `58-139).` without the opening parenthesis;
    the base had corrected it silently.
  - **Printed**, 5: two page numbers on their own line (`254`, `256`); `239` `THus`
    (small capitals, the base's case kept); `252` `arroncigliò`; `256` `lui:` (class D).
- **The retype** made one error: `252` `arronciglò` for `arroncigliò`.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`022`, `023`). `misprints.py`: 12 rows, 12 marks, 0 problems.

## Step 1–2: retype 12 (2026-11-13)

- **Pages** (25): `263`–`287` (Canto XXIII from its argument, Canto XXIV, the opening of
  Canto XXV). Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at
  twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 64 places, A 36, B 23, C 0, D 5. No
  GLM-OCR page left out. After the fixes, 14 places, all decided.
- **Decided** (readcheck.tsv, 49 rows):
  - **Misread**, 36:
    - In the verse: `264` `io gl’` (the dash was show-through), `compiè`, `volerne`;
      `266` `viso, … meco;`; `268` `e s’ei`, `io veggio` (the `il` was show-through),
      `guance,`, `sì`, `son` (was `peson`), and false accents (`Loderíngo`, `uôm`,
      `soffíando`, `convenía`); `270` `incarcati`; `276` `accascia.` (no closing quote);
      `278` `uscìo`, `mena,`, `rena;`; `280` `si scrisse`, `amomo,`, `fasce.` (a
      handwritten `qs` removed); `282` `dipinse;`; `286` `diche”:`.
    - In the English: `263` the whole page joined into one line per paragraph, restored
      (`Yea pair`, no comma); `265` `chase.`, `as my`; `275` words left out at three
      line ends (`the Sun`, `and the`, `sister’s`); `281` `the ground,` left out,
      `Phœnix` (also `285` `phœnix`).
    - Labels: `267` `Two "Jovial Friars"`; `279` `The Thieves`; `281` `The Thieves` and
      `Their punishment` a paragraph late; `287` `Cacus` left out.
    - In the notes: `272` `Calcabrina`, `Guelf`; `284` `NOTES` (a show-through `V.`),
      `i.e.`; `285` `Serravalle`, `Montecatini`.
    - The signature marks `R` (`269`) and `S` (`285`) left out.
  - **Misprint**, 3 (misprints.tsv): `271` `answerd`; `278` the page number `206` for
    `266`; `280` `cinquencentesimo`.
  - **Printed**, 10: six page numbers on their own line (`264`, `268`, `270`, `272`,
    `276`, `282`); `270` `gì`, `272` `Podestà`, `278` and `280` `sì` (class D).
- **The retype** made three errors, all misprints corrected: `271` `answered`, `278`
  `266`, `280` `cinquecentesimo`.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`024`–`026`). `misprints.py`: 15 rows, 15 marks, 0 problems.

## Step 1–2: retype 13 (2026-11-13)

- **Pages** (25): `288`–`312` (Canto XXV from v. 22, Canto XXVI, the opening of Canto
  XXVII). Retyped by **Claude (Opus 5.5)** from the images alone, in three strips at
  twice the size.
- **Compared** (`cmpread.py -g --verse-numbers`): 36 places, A 23, B 8, C 0, D 5. No
  GLM-OCR page left out. After the fixes, 9 places, all decided.
- **Decided** (readcheck.tsv, 33 rows):
  - **Misread**, 25:
    - In the verse: `288` `cessàr`; `290` `di`; `292` a stray `Il` removed, `dura.`,
      `dirietro`, `diventaron`; `300` `Allor`, `udirti`; `302` `Eteòcle`, `audivi`;
      `304` a stray `la` removed, `Morrocco`; `310` `gía`, `Cicilian`, `mugghiò`; `312`
      `Tever`.
    - In the English: `293` `not:`, `front to` left out at a line end, `another,`;
      `295` `Sciancato:`; `303` `of you` left out; `307` `to heaven` left out.
    - In the notes: `296` `Æn.`, a stray `‘`; `297` `sqq` (no period printed); `309`
      `Caïeta`.
    - The signature mark `T` (`301`) left out.
  - **Misprint**, 1 (misprints.tsv): `308` `53, 54,` with a comma for the period after
    the verse numbers; the base had corrected it silently.
  - **Printed**, 7: two page numbers on their own line (`296`, `304`); `290` and `310`
    `sì`, `mischiâr`, `298` `graverà`, `302` `Deidamìa` (class D); `297` `serpen-`
    (italics marks keep the comparison from joining it).
- **The retype** made no clear error.
- `convert_en_oelsner.py`: the report as the baseline; `texts/en-oelsner` regenerated
  (`026`–`028`). `misprints.py`: 16 rows, 16 marks, 0 problems.
