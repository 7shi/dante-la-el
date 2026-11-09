# Done: checking `ocr/grc`

The record of the check of `ocr/grc` planned in [PLAN.md](PLAN.md), step by step.

## Step 0: setup (2026-11-10)

- **Tables**: [misprints.tsv](misprints.tsv) (`page line printed fixed applied source
  note`) and [readcheck.tsv](readcheck.tsv) (`page line form decision note`), the columns
  of `ocr/la` (ocr/PLAN.md, "Decisions"); empty. `misprints.py ocr/grc`: 0 rows, 0 marks,
  0 problems.
- **The baseline** of `texts/scripts/convert_grc.py`, before any change: `texts/grc` as
  committed (`7596bcea`), and its output, eleven `TURNOVER` lines (the runovers joined to
  the line before) and nothing else:

  ```
  TURNOVER 069: ὸς τί τηρεῖς ; ” καὶ “ πρὸς τί | ῥίπτεις ; ”
  TURNOVER 081: οὺς πρὸς τὴν γῆν, τὰς ὀφρῦς τ᾽ | ἄνευ
  TURNOVER 090: ν πόθον, ὃν μοι κρύπτεις, πλη- | ρώσει.”
  TURNOVER 092:  υἱός μου; καὶ σὺν σοὶ πῶς οὐκ | ἔστι;”
  TURNOVER 158: ὄφλεις;”’—“ Ναὶ μὴν καὶ θαυμα- | σίας ! ” —
  TURNOVER 190: ᾽ οὕτως, ὥστ᾽ αὐτοὺς δοκῶ βλέ- | πειν.”
  TURNOVER 193: τρέφων ὀφθαλμούς· τάχ᾽ ἄν τιν᾽ | εὕροις.”
  TURNOVER 234: φεῦ! εἶπε,” ‘“Πᾶν πραχθὲν ἐτε- | λέσθη,”’
  TURNOVER 265:  σύ, τοὺς ἄλλους οὕτω προσβάλ- | λων;”
  TURNOVER 268: ηρανθῇ γλῶσσ’ ἥδ᾽, ᾗ φθέγγομαι | σοι.”
  TURNOVER 271: ῶς βλέπεις οὕτω, πάτερ; τί πά- | σχεις; ”’
  ```

- **`convert_grc.py`** taught the misprint marks: `fixed()` as in `convert_en.py`, applied
  to each page and to the hyphen vocabulary. Its output and `texts/grc` unchanged.
- **Tesseract**: [tesseract/Makefile](tesseract/Makefile), run over the 346 pages of `texts/grc`
  (all written; the half-titles `019` and `287` have only a few words),
  `-l grc` (with `lat+ita+fra` on the notes `287`–`351`: on the verse they made Greek words
  Latin, `Kaëaprnpiov` on `021`). It reads the Greek fairly, with errors of breathing and
  letter (`Ἐύρέθην`, `Δυκοθήρας`).
- **GLM-OCR** (`ollama run glm-ocr`) tried on `021`: most accents and breathings lost,
  Latin letters in the Greek (`'O δρυμώντραχύς, αγριος`, `Tà`); not used.
- **`ocr/scripts/cmpread.py`** made ready for Greek: Unicode NFC (tonos and oxia alike),
  the elision marks and numeral signs (`᾿ ᾽ ʹ ΄`) and `„ « »` normalized as the quotes, the
  upper dot however written (`· ˙ • ·`); a word hyphenated at a line end joined in the
  base and the retype (`ocr/grc` keeps the printed lines). Accents and breathings are
  compared. Tried on a copy of `005` with an accent and a breathing changed and a
  hyphenated word joined: the two accents listed, the join not.
- **`ocr/scripts/wordcrop.py`**: its labels drawn with Noto Sans when installed (PIL's
  default font has no Greek).
- **The shared tools** tried on `ocr/grc`: `pages.py texts/grc 21 22` (markers
  `<!-- p. [1] (021) -->`), `findline.py` (a phrase of `021` found at its line, `5 Ὁ
  δρυμὼν …`), `wordcrop.py -t ocr/grc/tesseract`. The crop of `021` line 5 shows
  `συνήρης` where the base has `στυγήρης`: left for step 2.
- **[TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md)** for `grc`, from `en`'s: lines as printed,
  with the running heads, page numbers, verse numbers and signature marks; polytonic
  Greek letter by letter; the errors of the transcription (accents, breathings, the iota
  subscript, rare forms made common).

## Step 1–2: retype 01, the trial (2026-11-10)

- **Pages**: `005`, `010`, `021`, `038`, `292`, `343` (prologue, table of contents, canto
  opening, verse, notes). la-el-agy on **Gemini 4 Argon** (chosen by the user for the
  polytonic Greek). All six written, lines as printed, the report with the unsure letters.
- **Compared** (`cmpread.py`): 36 places, A 20, B 16, C 0. Decided in the image
  (readcheck.tsv, 33 rows):
  - **Misread**, 26 fixes on 6 pages: accents and breathings (`ὄμ-βρος`, `Οὗπερ`,
    `ὀλολυγμοί`, `ἕνδεκα`, `Νεμβρώδ`, `μάϊ`, `ζαβὶ`), the iota subscript and the diaeresis
    (`ἐᾷν`, `ᾨδῇ`, `ἐποποιΐας`), `θαῤῥεῖν` normalized to `θαρρεῖν`, and words replaced
    by other words that make sense: `021` `στυγήρης` for printed `συνήρης` (the metre
    kept), `292` `ἀθανατισθεῖσα` for `ἀπαθανατισθεῖσα`, `Βεατρίζ` for `Βεάτριξ`,
    `Λατίνους` for `Λατίνοις`, `ἀνθρωπίνην` for the printed `ἀνθρώπινον`, `343` `κρύβθητι`
    for `κρύφθητι`, `μνημονευσομένων` for `μνημονευθησομένων`, `συμπίπτῃ` for `συμπέσῃ`;
    the signature mark `Β` of `021` added.
  - **Misprints**, 3 (misprints.tsv): periods not printed, `010` `ποιηταί` and
    `λαίμαργοι` before a dash, `292` the note number `28`; the base had added them.
  - **Printed**: the retype's `αὺτόν` (`343`, a smooth breathing in the print); the
    leader dots of the table of contents, not compared; the page number on the running
    head's line of `343`, the base's lines kept.
  - **Open**: `038` 18 `Ἀεὶ`: a mark under the `Α` like an iota subscript (`ᾈεὶ`, the
    retype); to be decided with the other places of `ἀεί` as the retypes come.
- The retype erred in 2 places (`αὺτόν`; `Ὠδῇ` without the subscript under the capital)
  against 26 misreadings of the base. `convert_grc.py`: output as the baseline; `texts/grc`
  regenerated (17 lines). `misprints.py`: 3 rows, 3 marks, 0 problems.

## Step 1–2: retype 02 (2026-11-10)

- **Pages** (25): `001`–`003`, `006`, `007`, `009`, `011`–`018`, `022`–`032` (title pages,
  prologue, table of contents, the corrigenda, cantos I–II). la-el-agy on **Gemini 4 Argon**.
  All written. A rule for tables was added to the task and [TEMPLATE-RETYPE.md](TEMPLATE-RETYPE.md)
  for the corrigenda: one printed row per line; the base joins a wrapped cell on one row.
- **Compared**: `cmpread.py` on the prose and verse, about 60 places outside the leader dots.
  The corrigenda tables (`014`–`018`) were compared cell by cell instead, as the
  retype's rows (one per printed line, the commas and periods of the number columns)
  made the word alignment useless; each difference was read in the image.
- **Decided** (readcheck.tsv, 105 rows):
  - **Misread**, most of them in the base: accents (`Πάρδαλίς`, `θυμῆρες`, `πλεῖστα`,
    `Νῖσός`, `ἀφεστηκότα`, `Καλεῖ`, enclitic accents `δή μοι`, `ψυχή τις`, `Οὔκ εἰμι`),
    breathings (`ἕπῃ`, `οὗπερ`, `Ἅρπυιαι`, `Ἣ`), `στεῤῥότερος`, `πρωΐα`, `τοὐμοῦ`, the
    aphaeresis `᾽κεῖνα`, words (`κάτισχνος` for `κάτισχος`, `προσενεγκόν`, `περιγράψει`,
    `εὐεπείαις`), points (`ἄμφω·`, `Χώραν` without a comma), the period of the running
    head of `022`, the signature `Β 2` without the numeral sign. In the corrigenda many
    readings had been made common or taken from the verse: `ὁ θεῖος` for `τὸ θεῖον`,
    `αὐλῶν` for `ἄλλων` (twice; the verse, 115, has `αὐλῶν`), `Ἄκρον`, `νῷ` / `φρεσὶ`,
    `τον Ἀπεννῖνον` for `τοῦ Ἀπεννίνου`, `ἀλυσίδετον` for `ἀλυσιδέτου`, `ἔννατον` /
    `ἔνατον` for `ἐννάτου` / `ἐνάτου`, the iota subscript of `ᾐσθάνθην`, `ᾐσθόμην`,
    `ἐξαπατᾷν`; the signature `Ζ` of `015` added (`convert_grc.py` drops it there too).
  - **Misprints**, 7 (misprints.tsv): `015` `ῼδαῖς` (no breathing), `017` `τον`, `023`
    `προς`, `024` `ἒνθ` (no elision mark), `030` `ᾙρέθη` and `038` `ᾈεὶ` (an iota
    subscript under a capital; the open place of retype 01), and `157` `ὀοθῶς` (XVIII
    132): the corrigenda list it (`016`, ἀντί. `ὀοθῶς`), and the image of the verse shows
    it; the base had corrected it silently.
  - **Printed**: the retype's errors (`ἅγε`, `Λάνος`, `συνυπῆρξεν`, `ἑνάτου` twice for the
    printed smooth breathing, `κτλ.` for the printed ligature `κφξ`, Greek `ΙΙ` for Roman
    `II`); the library stamp of `001`; the thousands sign `͵α` of `007`, printed under
    the alpha; the page number on the running head's line of `030` (as `343`).
- 87 misread rows (some rows cover several words), 7 misprints, 11 printed. The retype
  erred in about 15 places.
  `convert_grc.py` (the signature mark dropped on `015` as on the cantos): output as the
  baseline; `texts/grc` regenerated. `misprints.py`: 10 rows, 10 marks, 0 problems.
