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

## Step 1–2: retype 03 (2026-11-10)

- **Pages** (25): `033`–`037`, `039`–`058` (cantos II–V; `038` was in retype 01).
  la-el-agy on **Gemini 3.8 Flash** (Argon's quota reached; sent as a comparison of the
  two models, asked by the user). All written.
- **Compared**: `cmpread.py`, 76 places; each read in the image. The doubtful breathings
  and accents were read beside sure ones: the roman rough breathing with acute (`Ἕως`,
  041 10) against the smooth with acute (`Ἔπειτα`, 042 15); the italic diaeresis with
  acute (`πρωΐα`, 023).
- **Decided** (readcheck.tsv, 76 rows):
  - **Misread**, 56, all in the base: accents (`ἔστι` twice, `βαθεῖα`, `συμμίγδην`,
    `Καίσαρ`, `Νῖνον`, `Σουλτάνος`, `προσκάλει`, `πραΰς`, enclitic accents `ἅπτεταί μου`,
    `Οὐδείς ποτ᾽`, `ποιητής μοί`, `Εἴ ποθ᾽`), breathings (`αὐτῷ` printed smooth,
    `οὑτωσὶ`, `αὗται`, `αὑτῆς` twice, `Ἕως`, `Ὅ`, `ἕκτος`, `Ἤλθομεν`, `ἤρκεσ᾽`,
    `ἠρεμοῦντος`), `ῤῥ` four times, the iota subscript (`ᾐσθάνοντ᾽`, `ᾐσθάνθην`,
    `ἐρᾷν`, `σκέπτῃ`), words (`προσυπισχνοῦνται`, `πελιδνοῦ`, `ἵξεται` for `ἵζεται`,
    `διήστραψε`, `κρυψίνουν`, `Κορνηλίαν`, `Προϊστάμενον` for `Προϊσταμένω`,
    `μωλωπίζει`, `βαθύγνοφος` for `βαθύγνωφος`, its broken letter read as omicron), the
    nested quotes `‘“` of `034`, the periods of the running heads of `033` and `054`,
    the signature `Γ` of `037` added and `C 2` of `039` without a period.
  - **Misprints**, 3 (misprints.tsv): `035` `ΩΔΠ` in the running head, `035` `συῦ`,
    `046` `ἀνδρῶν;`.
  - **Printed**, 17: the retype's errors (below), and two low marks between words
    (`033` 10, `040` 20), a spacing quad's, not periods.
- **The retype** (Flash) erred in about 13 places in 25 pages: periods read as `·` (4),
  breathings and accents (`Οὔκ`, `πῖπτον`, `Οὕτως` for `Οὗτος`, `Οὗτως` / `Οὗτω` for
  `Οὕτως` / `Οὕτω`, `Δαυῒδ`, `Λαϋινίᾳ`, `πλῆθός` for a speck), a Latin `o` in
  `Ποιούμενoι`; the two `Ὃς`, whose accent the roman type does not tell, left as the base.
  Argon (retype 02) erred in about 15 places in 25 pages.
- `convert_grc.py`: output as the baseline; `texts/grc` regenerated. `misprints.py`: 13
  rows, 13 marks, 0 problems.

## Step 1–2: retype 04 (2026-11-10)

- **Pages** (25): `059`–`083` (cantos V–IX). la-el-agy on **Gemini 3.8 Flash** (the
  user's choice after retype 03). All written.
- **Compared**: `cmpread.py`, 111 places; each read in the image. The italic marks were
  read beside sure ones: smooth with circumflex is `3`-shaped (`ἆρ᾽` 059 8, `Ἆ!` 068 7),
  smooth with acute a comma and a stroke (`θἄτερον`, `οὔκ`, `ὄμβρος`), rough with acute
  an open `c` with a stroke (`αἵματ᾽` 064 16).
- **Decided** (readcheck.tsv, 111 rows):
  - **Misread**, 85, all in the base: accents (enclitics `πρός με` twice, `γάρ σε`,
    `ἀνέγνωμέν τι`, `τρεπόμενός που`, `μή γ᾽`, `ὥς εἰμι`, `οὔκ εἰμι`; elisions `αὔτ᾽`,
    `ἔμ᾽`, `τἀγάθ᾽`, `μείον᾽` with its missing elision mark; `ἀναμνῆσαι`,
    `συσσωρεῦσαι`, `Αἶσχος`, `δίδαξόν`, `κυλιούσας`, `ἐρυθραινούσας`, `Κίακόν`),
    breathings (`ἑάλω`, `ἕκτος`, `ἕλους`, `ἁψῖδα`, `αὑτοῦ` / `αὑτῆς` four times, `Ὧδ᾽`,
    `Ἔνθ᾽`, `Ἐλθὲ`), crasis (`θἀτέρου` twice, `θἀτέρῳ`, `θἄτερον`, `τἆλλο`, `Κἆλλά`,
    `τᾠδηκότα`), `ῤῥ` five times, the iota subscript (`ἠχήσῃ`, `Ἐπᾴδουσαι`, `ᾆσμα`,
    `νικᾷν`, `Φοιτᾷν`), words (`συναναγινωσκόντων`, `βλάψῃ`, `θέλουσ᾽`,
    `Συνεπαίοντ᾽`, `χόρτον`, `βρόγχοις`, `ἐπιστρέψειν`, `ἔκραξ᾽`, `τοῦ Δεῖνος` for
    `Δεινοῦ`, `Αἵδ᾽` for `Αἳ δ᾽`), the raised point for the period (5), the nested quotes
    of `074` (`‘“`, then `‚ „` on the following lines, closed `”’`), an opening quote
    (`068` 11), the aphaeresis mark of `᾽τρέχομεν` (`076` 20), the periods of the running
    heads of `066` and `070`, the signature `Ε 2` of `071` without a period.
  - **Misprints**, 8 (misprints.tsv): `059` `πόθους.` (a question), `061` `τὸν ὄμβρου`,
    `065` `Τύφος`, `075` `Διτός πόλις`, `077` `ᾈείποτ᾽` and `079` `ᾍδῃ` (an iota
    subscript under the capital, as `038`), `077` `κυσμοῦσ᾽`, `079` `θλίψιν`.
  - **Printed**, 18: the retype's errors (below), five low marks between words, a
    spacing quad's, as in retype 03 (`064` 19, `078` 15, `082` 8 and 12, `083` 19), two
    faults of the alignment, and the running head of `081`, printed without a period.
- **The retype** (Flash) erred in about 16 places in 25 pages, besides the five spacing
  marks it wrote as `·`: periods read as `·` (3) or `,` (1), a period added to the head of
  `081`, `!` added (`079` 8), the Latin `E` in two signatures, breathings and accents
  (`δυνατὸν`, `Εἶσ᾽`, `αἷματ᾽`), `βροχιζούσης`, and three misprints read as the right
  form (`Τῦφος`, `Διτὸς`, `Ἅδῃ`); the `Ὃς` of `079` 17 left as the base, as in retype
  03. Retype 03 (Flash) erred in about 13, retype 02 (Argon) in about 15.
- `convert_grc.py`: output as the baseline; `texts/grc` regenerated. `misprints.py`: 21
  rows, 21 marks, 0 problems.

## Step 1–2: retype 05 (2026-11-10)

- **Pages** (25): `084`–`108` (cantos IX–XII). la-el-agy on **Gemini 3.8 Flash**. All
  written.
- **Compared**: `cmpread.py`, 92 places; each read in the image, the marks as in retype 04.
- **Decided** (readcheck.tsv, 92 rows):
  - **Misread**, 76, all in the base: accents (enclitics `φλογεράν τ᾽`, `ἐλπίς σ᾽`,
    `ἐμοί τις`, `δέ τινα`, `κατέστησάν μοι`, `πλήττονταί τ᾽`, `Ἀποφοράν·`; elisions
    `ἔμ᾽`, `πώματ᾽`, `τραύματ᾽`, `ἀποκριθῆν᾽`, `Ἅμ᾽`; `Μέγαιρ᾽`, `Τεῖνον`,
    `ὁμοῖος` / `ὁμοῖοι`, `ζῶσιν`, `διαιρεῖται`, `μανιᾷ`, `θημώνων`), breathings (`Ὁδοῦ`,
    `ὅρασιν`, `ἕπου`, `Ἧττον` / `ἧττον`, `ἥδ᾽` / `ἥδε`, `οὗπερ`, `ὡδὶ`, `Ὀπαδεῖν`,
    `αὑτοῦ` three times), crasis (`χἠ`, `τοὐμοῦ`, `τἀγγὺς`, `τἀν`, `Χὠ`, `Ταὐτῷ`), `ῤῥ`
    three times, the iota subscript (`ᾐσθάνετ᾽`, `ᾐσθάνθη`, `διέρχῃ`, `βίᾳ`, `Σκέπτῃ`,
    `᾿μῇ`; `θάλπη` without), words (`Στρέψον`, `Ἤμυν᾽ … ἀποκεκαλυμμένως`, `νεκρὼν`
    the burial ground, `Μαστρωπούς`, `συμπεπτωκυῖα`, `τάφρον`, `ἔκραξε`, `ἀλληλούϊα`,
    `τ᾽` added on `092` 18), quote marks (none on `087` 14 and before `τὰ` on `094` 10),
    raised points (`092` 11, `097` 12), the aphaeresis mark of `᾽κεῖναι`, the signature
    `F` of `085` added, and a second `83` at the foot of `103`, not printed, removed.
  - **Misprints**, 5 (misprints.tsv): `099` `Τόν`, `102` `φὴς` (listed in the corrigenda
    of `014`), `107` `ᾀείποτε` (an iota subscript, as `038` and `077`), `107` `στῆθός`,
    `108` `φλαύρα`.
  - **Printed**, 11: the retype's errors (below), the `Ἓν` of `090` 4 left as the base, as
    `Ὃς`, and the spacing of a dash.
- **The retype** (Flash) erred in about 10 places in 25 pages: the iota subscript dropped
  or added (`ἠωρημένα`, `ἀπῃρμένα`, `Ὧπερ`), `Καβαλκάντης`, `διὼν`, `ὧδὶ`, `Ἢ`, a period
  added to the argument of `089` and a period read as `·`, and the misprint `φὴς` written
  as the corrigenda's `φῂς`. It wrote the spacing marks as spaces this time (three, its
  report). Retypes 03 and 04 (Flash): about 13 and 16.
- `convert_grc.py`: output as the baseline; `texts/grc` regenerated. `misprints.py`: 26
  rows, 26 marks, 0 problems.
