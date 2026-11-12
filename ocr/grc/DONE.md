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

## Step 1–2: retype 06 (2026-11-10)

- **Pages** (25): `109`–`133` (cantos XII–XV). la-el-agy on **Gemini 3.8 Flash**. All
  written. It wrote the breathing of 33 capitals as a separate character (`᾿Αλλ` for
  `Ἀλλ`, on `128`–`133`): joined in a copy before the comparison, not counted as places.
- **Compared**: `cmpread.py`, 108 places (138 before the joining); each read in the image,
  the marks as in retype 04, and beside sure ones: rough with grave is a caret with a dot
  at its top (`ἣ` 129 13, as `ὃ`), smooth with grave a comma and a back stroke (`ἂν` 132
  8); the coronis with circumflex `3`-shaped (`τοὖργον`, `κᾆτα`); the hook under the
  circumflex open to the right for the rough breathing (`οὗτος`, `Οἷον`), to the left for
  the smooth (`ἦς` 132 12).
- **Decided** (readcheck.tsv, 105 rows):
  - **Misread**, 86, all in the base: accents (enclitics `ἔνθ᾽ ἐστι`, `εἰσι`, `Ἀζελήν
    ἐστιν`, `βούλομαί σε`, `λαιμόν τ᾽`, `ἤ σε`, `εἴ σ᾽`, `ἀλγεινά θ᾽`, `Κατεσπάραξάν
    τ᾽`, `ποτάμιόν τι`, `ἐρείπιός τις`, `ἐκώλυσέ με`, `ὄν σοι`, `ἄν σοι` twice,
    `γενήσεταί σοι`, `ἐστί μοι`; `δρυμὼν`, `χεὶρ`, `βλαβερὰν`, `εἶ`, `ἀπεῖργον`,
    `ἑταίρα`, `χρονοτρίβει`, `ἀφεῖλ᾽`, `Προσέφυγεν`, `ἀναγνοὺς`, `Προστάτα`,
    `λυσσόων`, `θῇς`, `Εἶπέ`, `γεγηρακὸς`, `ῥοῶν` twice, `φῄς`, `εἶπας`, `Δεδιότες`,
    `συγκαθῖσαι`, `Αὔτ᾽`, `πρωῒ`, `Παταυῗνοι`), breathings (`αὑτοῦ` four times,
    `αὑτῆς`, `ἑψάνης`, `Ἔστης`, `Ἔνθ᾽` twice, `Ἑνὸς`, `Ἕξομεν`, `ἁλλομένων`,
    `Οἵασπερ`, `ἕξοι`, `ἕπου`, `ἕπεσθαί`, `ἣ`), crasis (`κὠζώδεις`, `τοὖργον`,
    `τοὖρος`, `κᾆτα` twice, `κἀν`, `ἆρ᾽`), `ῤῥ` three times, the iota subscript
    (`σιγᾷν`, `περᾷν`, `αὐτοχειρίᾳ`; `Στήσητ᾽` without), words (`Ἐπίστρεψον`, `ζέον`,
    `Λάνος`, `βλάψῃ`, `ἐπιστρέψῃ`, `Μέσον`, `δεικνύων`, `Ἐδίδων`, `ψαυέσθω`), the
    nested quotes of `123` 6, the aphaeresis mark of `᾿ρυθρότης`, a second `91` at the
    foot of `111`, not printed, removed, the page number put after the running head
    (`117`, `129`), and a breathing that was a separate character (`132` 8).
  - **Misprints**, 8 (misprints.tsv): `110` and `124` `ᾀεὶ` and `120` `Ἐσᾳεὶ` (an iota
    subscript, as `107`), `111` `ᾈττίλαν` (one under the capital, as `038`; first
    decided a blot and printed, read as a subscript by the user in the image), `112` `ΩΔΗ 1Γ΄.` and `124` `ΩΔΗ 1Δ΄.` (the figure `1` for the
    `Ι` in the heading and a running head), `113` `δε` without its accent, `118`
    `πρῶτυς`.
  - **Printed**, 11: the retype's errors (below), the signatures `H` and `H 2` as the
    base writes them, and the `Ὃν` of `124` 20 left as the base, as `Ὃς`.
- **An earlier decision corrected**: `011` 11, the `Δάνος` of the table of contents,
  decided printed in retype 02, is `Λάνος` as in the argument of `112`: the italic Λ has
  serifs at its feet, the Δ a solid base (`Διτός`, `075`); `convert_grc.py` compares the
  two. The row of readcheck.tsv was changed to misread.
- **The retype** (Flash) erred in about 12 places in 25 pages: breathings (`Αὑτοῦ`,
  `αὑτὸ`, `Οἶον`, `ἧς`), the coronis dropped (`θατέρου` twice, `τοῦργον`, `τοῦρος`), the
  iota subscript added (`ζῴων`, and `ᾆρ᾽` for a speck), `ὦ` for `ὁ`, and a prime in the
  signature `H 2`. It found all eight misprints. The task of retype 07, sent before the
  decision of `111` was changed, lists `ᾈττίλαν` among the retype's errors: looked at
  when retype 07 is decided (subscripts it may have dropped). Retypes 03–05 (Flash):
  about 13, 16 and 10.
- `convert_grc.py`: output as the baseline; `texts/grc` regenerated. `misprints.py`: 34
  rows, 34 marks, 0 problems.

## Step 2: retype 07 (2026-11-12)

- **Pages** (25): `134`–`158` (cantos XV–XVIII). la-el-agy on **Gemini 3.8 Flash**,
  returned 2026-11-10 and decided now. All written; no breathing written as a separate
  character this time, so the copy before the comparison changed nothing.
- **Compared**: `cmpread.py`, 111 places (A 51, B 60); each read in the image, the marks
  at eight times their size and, where doubtful, at twelve times in the pixels beside a
  sure one of the same page: the rough breathing on a small letter is a `c` with its tail
  to the right (`ὁ`, `ἑκατόν`), the smooth a `)` with its tail to the left (`ἐπὶ`,
  `ἐγὼ`); the roman capital with rough breathing and acute a loop with a stroke (`Ἵν`
  145, as on `097` and `106`; `Ἅλις` 156; `Ὅτε` 139), with rough breathing and
  circumflex as `ᾯπερ` (`Ὧδε` 146).
- **Decided** (readcheck.tsv, 108 rows; the places of one quote counted once):
  - **Misread**, 95, all in the base: accents (enclitics `φανήσεταί σοι`, `ὄμνυμί σοι`,
    `κάτωθέν μου`, `κἀτενίζω σέ`; `ἄν` three times, `ἔστ᾽`, `ἔμ᾽`, `εἴμ᾽`, `Εἴ γ᾽`,
    `εἴτ᾽`, `ἄλλ᾽`, `ἄπελθ᾽`, `ἀπών`, `καθὼς`, `σπιλάς`, `οἰκτράν`, `καταφρονήτους`,
    `ἠκουόμεθα`, `γεγόνασιν`, `ἀποῤῥωγάδος` / `ἀποῤῥωγάδα`, `συνεῖναι`, `φλοῖσβον`,
    `Κακιανιμῖκος`, `αὐλῶνας`, `Ἀτμὸν`, `Τοιόνδ᾽`, `καθεδούμενον`), breathings and
    their accents (`Ἢ`, `Οἳ`, `Ἦμεν`, `Ἐν`, `Ἐπ᾽` twice, `Ἐστίν`, `Ἔγωγ᾽`, `Ἵν᾽` twice,
    `Ἅλις`, `Ὧδε`, `ὅς`, `Εἷς`, `Εἶπέ` twice, `ἑλεῖν`, `εἱστήκει`, `Ἑβδόμου`,
    `ἑστιᾷν`, `ἑλιγμῶν`, `εἱπόμην`, `αὑτοῦ`, `ἠμύνοντο`, `ᾄδετ᾽`), crasis (`κἀν`,
    `κἀμέτρους`, `τοὖργον`, `καὐτίκ᾽`, `τἀκάτιον`, `κᾆτα`, `Τοὐμβαδὸν`, `τοὖρος`), `ῤῥ`
    six times, the iota subscript (`ᾐσθάνθη`, `ᾐσθάνθην`, `σιγᾷν`, `διῄρητ᾽`,
    `Συνῄνεσ᾽`, `ᾬχετο`; `προσηνὴς` without), words (`Τόπον`, `τοιᾶσδ᾽`,
    `τρίῤῥυγχον`, `διαγράψω`, `Κακόβοθρον`, `ἔκραξεν`, `Ἔκραξε`, `δεισαλέας`, a `δ’`
    not printed on `155` 5), quotes (`‘ ἤμην,’` 139 14; the nested quotes of `146` 22 and
    `147` 2; a closing `’` on `153` 21), an upper dot (`148` 19), the base's own
    separate breathings joined (`137` 18, `144` 7 and 18, `148` 15 and 22), a second
    `121` at the foot of `141`, not printed, removed, the page number of `157` put after
    the running head, and a period not printed in the running head of `158`.
  - **Misprints**, 4 (misprints.tsv): `134` `δὶ` (a grave for the elision mark), `139`
    `Εἰπόμην` (the smooth breathing for the rough), `146` `και` and `147` `ἀλλ` (the
    grave and the elision mark did not print).
  - **Printed**, 9: the retype's errors (below) and the signatures `I`, `K`, `K 2` as the
    base writes them.
- **The retype** (Flash) erred in about 8 places in 25 pages: `κείνοι`, `Ποιῇ`,
  `Γιγδουγγέρας`, `Μαρουλίου`, `ποικιλόδερματον`, `ἐστωσάν`, and two misprints corrected
  from the sense (`Εἱπόμην`, `ἀλλ᾽`). It found the other two misprints, and none of its
  readings was a dropped iota subscript (the task's `ᾈττίλαν` line, "Open points" in
  PLAN.md). Retypes 03–06 (Flash): about 13, 16, 10 and 12.
- `convert_grc.py`: its report as the baseline; `texts/grc` regenerated (cantos XV–XVIII).
  `misprints.py`: 38 rows, 38 marks, 0 problems.

## Step 2: retype 08 (2026-11-12)

- **Pages** (25): `159`–`183` (cantos XIX–XXII). la-el-agy on **Gemini 3.8 Flash**,
  returned 2026-11-10 and decided now. All written; no breathing written as a separate
  character, the copy before the comparison changed nothing. The base wrote some
  breathings as a separate `’` (`’Ηκροᾶτο`, `165`) or twice, once as a quote mark
  (`’Ὠθεῖν`, `176`, `180`): joined as found.
- **Compared**: `cmpread.py`, 114 places (A 54, B 60); each read in the image as in
  retype 07.
- **Decided** (readcheck.tsv, 109 rows):
  - **Misread**, 101, all in the base: accents (enclitics `εἰδώς με`, `ἐμπνέουσί μοι`,
    `μού τις`, `μή σ᾽`, `πρός μ᾽`, `Ὑπό θ᾽`; `ἔστ᾽` / `ἔσθ᾽` five times, `ἔστι`,
    `εἴμ᾽` twice, `εἴσ᾽`, `εἴ γ᾽`, `Οὔ`, `ἔμ᾽`, `εἴωθας`, `δή`, `μή`, `χρηστούς`,
    `Μαντώ`, `Μιχαὴλ`, `ἐμέ`, `κάλως`, `πλουτίσαι`, `προὶξ`, `δηκτικωτέροις`,
    `δαίμον᾽`, `προσεῖχον`, `Ἀῤῥητῖνοι`, `Ἀλικῖνε`, `Καλκαβρίνα`, `κευθμώνων`,
    `δυσμόθεν`, `Κάϊν`, `πλωΐμων`, `εἶς`), breathings and their accents (`Ἠρξάμην`,
    `Ὑπ᾿`, `Ἅμ᾽`, `Ὅδ᾽`, `Εἵλκυσέ`, `ἣ` twice, `ὅρον`, `ἕκτης`, `ὢ`, `ἆρα`, `Ἆρον,
    ἆρον`, `Ὧδ᾽`, `εἷς`, `αὑτοῦ`, `αὑτῆς`, `Ἁβρῶς`, `Ἁψῖδος`, `ἁρπάγας`), crasis
    (`κἀν`, `κὠχυρὸν`, `κἀρτέμον᾽`), `ῤῥ` twice, the iota subscript (`εἴσῃ`, `σῇ`,
    `ᾖς`, `αἰσχύνῃ`, `ᾔτησε`, `ᾜτησαν`, `ζῇ`, `κατῴκει`, `᾿μῇ`, `θείᾳ`, `τέχνῃ`;
    `βελόνης` without), words (`Μέσον`, `Δολοφόνον`, `ἔκραξε` twice, `ἔστρεψε`,
    `ἐγεννήθην`, `Λελυμένοις`, `ὑποσπόνδως`, `Παρόντ᾽ αἴσθωνται`, `Δραγιγνάζος`,
    `Καριάττος`, `διαφέρετ᾽`), punctuation (upper dots `162` 11, `164` 6, `167` 21;
    commas `164` 15, `177` 4; the nested quotes of `167` 21–22), the base's separate
    breathings joined (`165` 11, 15, 22; `176` 6, 15, 17; `180` 5, 6), a second `157`
    at the foot of `177`, not printed, removed, and the roman `^` mark as rough
    breathing and grave (`Οὓς` 165, `Ἃς` 172; first decided printed with the base's
    acute, then settled with the user by the grammar, PLAN.md "Settled readings").
  - **Misprints**, 5 (misprints.tsv): `165` `ᾀεὶ` (held with the others, "Open points"
    in PLAN.md), `173` `ἀπατεῶνες` (the period before the dash of the argument did not
    print; the table of contents has it), `175` `Ζιτας` and `183` `Ἡγητωρ` (the acute did
    not print), `183` `ᾜδειν` (an iota subscript under the capital).
  - **Printed**, 3: the retype's errors (below).
- **The retype** (Flash) erred in about 5 places in 25 pages: `ᾗ` for `ἣ`, `Ἴσπαλιν`,
  `Τυβάλδῳ`, an upper dot for a period (`163` 10) and one added to the argument of `173`.
  It read the roman `^` mark as rough with grave (`Οὓς`, `Ἃς`), as now settled. It found
  all five misprints. Retypes 03–07 (Flash): about 13, 16, 10, 12 and
  8.
- `convert_grc.py`: its report as the baseline; `texts/grc` regenerated (cantos XIX–XXII).
  `misprints.py`: 43 rows, 43 marks, 0 problems.

## Step 2: retype 09 (2026-11-12)

- **Pages** (25): `184`–`208` (cantos XXII–XXV). la-el-agy on **Gemini 3.8 Flash**,
  returned 2026-11-10 and decided now. All written; 35 breathings written as a separate
  character, joined in the copy before the comparison. The base had a straight quote for
  an elision mark (`189` 7), and its ornament lines at the opening of canto XXV (`205`):
  both changed as found.
- **Compared**: `cmpread.py`, 96 places (A 59, B 37); each read in the image as in
  retype 07, the roman breathings beside sure ones of the same pages.
- **Decided** (readcheck.tsv, 96 rows):
  - **Misread**, 88, all in the base: accents (`Εἶπέ`, `Λατῖνον`, `ἐξεῖλε`, `Σύνεστιν`,
    `Πλείον᾽`, `καταπλὴξ`, `ὥς ἐστιν`, `μυκτῆρ᾽`, `εἴμ᾽`, `Ἀλικῖνος`, `χρυσοῦς`,
    `περιλαμπεῖς`, `προσείχομεν`, `ἔστι`, `ἔστ᾽`, `Ἰδών`, `Ἐστὶν`, `μικρόν`, `πρός`,
    `ἠδυνάτουν`, `Εἴ`, `ἀποῤῥὼξ`, `ἐμπηγνῦσιν`, `Ἔνθ᾽`, `Χαμᾶζε`, `κευθμών`,
    `ἀπαντηθείς`, `ἄνοιξον`, `εἶτ᾽`, `Περάνας`, `οἴομαι`, `χεῖρας`), breathings and their
    accents (`εἷς` three times, `ἑοῦ`, `ἆρά`, `ἆρ᾽`, `Ἤρεισ᾽`, `ἠνώρθωσε`, `ἑψητοὺς`,
    `Ἢν` twice, `αὑτῆς` / `αὑτὸν` / `αὑτοῦ` six times, `εἷρπ᾽`, `ἑνοῦται`, `ἥφθη`,
    `εἱλόμην`, `ὃ`, `ἤν`, `Ὦτ᾽`, `Ὅτ᾽`, `Ὁ`, `ἢ`, `Εὕδων`, `Οὑμὸς`, `ἑξάπους`), crasis
    (`κοὐχὶ`, `τοὐμὸν`, `κοὐρὰν`, `κοὐδαμόσ᾽`), `ῤῥ` four times, the iota subscript
    (`ᾐσθόμην`, `κἀναζῇν`, `αἰτίᾳ`), words (`Καριάτος`, `Δραγιγνάζος`, `περιέστρεψε`,
    `Ἐνεπαίχθησαν`, `Στρέφον`, `τετρυμένας`, `στρέψον`, `πάγγυμνος`, `Μέσον`, `Φλοξὶ`,
    `ἀνθρώπινον`), the aphaeresis mark (`᾽τράφην`), punctuation (upper dots `187` 13,
    `200` 7; a comma `203` 5; no comma `193` 9), and the two ornament lines of `205`
    emptied.
  - **Misprints**, 2 (misprints.tsv): `188` `ὄνυξίν` (a second acute), `198` `Κᾀεὶ` (an
    iota subscript, held with `ᾀεὶ`, "Open points" in PLAN.md).
  - **Printed**, 6: the letter-spaced `Ἤ δ η` and `Ν ῦ ν` of `189` 12, written closed up
    (PLAN.md "Settled readings"), and the retype's errors (below).
- **The retype** (Flash) erred in about 7 places in 25 pages: `Ἢν` for `Ἤν` (`186` 20),
  `ἤ` for `ἢ` (`199` 3), `Ἐπόμενος`, `μεῖζον᾽`, an upper dot for a spacing mark (`192`
  14), and two misprints set right without a mark (`ὄνυξιν`, `Κἀεὶ`). It kept the
  letter-spacing of `189` 12. Retypes 03–08 (Flash): about 13, 16, 10, 12, 8 and 5.
- `convert_grc.py`: its report as the baseline but for `193`'s turnover line, which now
  reads `στρέψον`; `texts/grc` regenerated (cantos XXII–XXV).
  `misprints.py`: 45 rows, 45 marks, 0 problems.

## Step 2: retype 10 (2026-11-12)

- **Pages** (25): `209`–`233` (cantos XXV–XXVIII). la-el-agy on **Gemini 3.8 Flash**,
  returned 2026-11-10 and decided now. All written; no breathing written as a separate
  character. The base had one (`’Ατενὴς`, `222`), the ornament lines of canto XXVI
  (`213`), a figure `0` in the signature `O 2` (`215`), and no signatures on `213`, `229`,
  `231`: changed as found.
- **Compared**: `cmpread.py`, 134 places (A 64, B 70); 22 of them the nested quotes of
  `218`–`219` and `226`–`227`, read together on the page (`‚ „`, as `074`); the others each
  in the image as in retype 07.
- **Decided** (readcheck.tsv, 121 rows):
  - **Misread**, 110, all in the base: accents (`ὀφείδιόν`, `ἐκεῖνον`, `Σῖγα`, `Σῖγ’`,
    `συναφῆς`, `μυκτῆρα`, `μυκτῆρ᾽`, `Τά τ᾽`, `Βουῶσος`, `φλοξὶν`, `ἔστ᾿` / `ἔστ᾽` three
    times, `ὄφλουσι`, `φλὸξ`, `κινεῖσθε`, `τοσούτου`, `ἐξιόντος`, `σύ` twice, `Λατῖνός`,
    `χλωρούς`, `δέομαί`, `μή`, `ἔῤῥιπτε`, `κάλως`, `συμβουλάς`, `κλείειν`, `κλείεται`,
    `πυρός`, `Αὐτάς`, `ἀφηγήσαιτ᾽`, `πταῖσμ᾽`, `προεῖπέ`, `Ἐν`), breathings and their
    accents (`ἅτερος`, `οὑτωσὶ`, `Ἥττονα`, `ἅμ᾽`, `Ὁρμῶντας`, `Οὑμὸς` / `οὑμὸς` three times,
    `αὑτ-` seven times, `ἁγνὸς`, `Ἠδυνήθησαν`, `Ὅτ᾽`, `Ἥσθημεν`, `εἷλξε`, `Ἠρξάμην`,
    `εἱστήκει`, `Ἃ`, `ἠμέλει`, `ἁψῖδος`, `ἕν᾿`, `εἷς`, `Ἑκατὸν`, `Ἵν᾽`, `ἕξετε`, `Ἢν`),
    crasis (`θἀτέρου` twice, `τοὔνομα`, `Κἀκεῖνοι`, `τἀκτὸς`), `ῤῥ`, the iota subscript
    (`ζῇν`, `χαλᾷν`, `σιωπᾷν`, `ᾔτησε`, `ᾐτήσατό`, `ἐπανίδῃς`; `κἀπήρχετ᾽` and `Ἐπωάζων`
    without), words (`Ἐλθὸν`, `κἀνείλκυσέ`, `εὐωδοῦτο`, `ἵππου`, `Ἐγρηγορούσας`, `οὖσ’`,
    `ἰσχναίνειν`, `Τιλακοσσίοις`, `τετρημένον`, `τεθαυμασμένως`, `μονοφθάλμως`,
    `πρωΐας`), punctuation (upper dots `217` 17, `220` 7; a low mark after `χρόνον`, `218`
    22, a spacing quad's; the nested quotes, 22 lines), the separate breathing joined, the
    ornament lines emptied, and the signatures.
  - **Misprints**, 3 (misprints.tsv): `213` `τἆχθος` (a circumflex for the acute; unmarked
    in retype 11, the crasis lengthens the alpha), `219` `ᾀεὶ` (held, "Open points" in
    PLAN.md), `230` `Φρεγελλαις` (no accent).
  - **Printed**, 8: the retype's errors (below).
  - **`183` `ᾜδειν`** (retype 08) unmarked: the edition writes `ᾔδειν` with the
    subscript (`203` 17, `225` 6), the Attic form; its row of misprints.tsv removed and its
    readcheck row changed to misread.
- **The retype** (Flash) erred in about 9 places in 25 pages: `Ἴσπαλιν` (as in 08),
  `μοὖδωκεν`, `ᾘδειν`, `αὑτῷ`, an upper dot for a period (`214` 10) and for three spacing
  marks (`217` 12, `227` 18, `233` 16), and `τἄχθος` for the printed `τἆχθος`. It wrote the
  nested quotes `, „` with a comma. Retypes 03–09 (Flash): about 13, 16, 10, 12, 8, 5 and 7.
- Open, for the user (PLAN.md "Open points"): the roman `^` mark on `Ἢν` (`190`, `232`),
  and `εἷς` at `231` 10.
- `convert_grc.py`: its report as the baseline; `texts/grc` regenerated (cantos XXV–XXVIII).
  `misprints.py`: 47 rows, 47 marks, 0 problems.

## Step 2: retype 11 (2026-11-12)

- **Pages** (25): `234`–`258` (cantos XXVIII–XXXI). la-el-agy on **Gemini 3.8 Flash**,
  returned 2026-11-10 and decided now. All written; no breathing written as a separate
  character. The base had ornament lines at the openings of cantos XXIX and XXX (`237`,
  `245`) and no signatures on `245`, `247`: changed as found.
- **Compared**: `cmpread.py`, 104 places (A 48, B 56); each read in the image as in
  retype 07, the roman breathings beside sure ones of the same pages.
- **Decided** (readcheck.tsv, 96 rows):
  - **Misread**, 77, all in the base: accents (`πιστός`, `Υἱόν`, `Δαυῒδ`, `Εἴ`, `ἐπεῖπον`,
    `Ἤκουσά`, `καθειργμένοι`, `κλιβάνῳ`, `μαχαιρὶς`, `Εἴμ᾽`, `οὔ`, `Ἀλλά`, `δή`,
    `Ἐριννῦς`, `ἔσθ’` / `ἔστ’` / `ἔσθ᾽` three times, `Δωνάτον`, `εἰκών`, `ὁδεῦσαι`,
    `πλείον᾽`, `θλίψις`, `Ἔγκλειστοι`, `στῆθος`, `μάϊ`, `ἀάλμι`, `ὀργὴ`, `αὐτόν ἐστιν`,
    `ἅς`, `Ἤλθομεν`), breathings and their accents (`αὑτοῦ`, `Ἄλλα`, `Οὑμὸς` / `οὑμὸς`
    twice, `Ἤπερ`, `ἆρ᾽`, `Ὧδ᾽`, `ὅ`, `Ἄγος`, `ἥδε`, `ῥ` twice), crasis (`κἀτενίζων`,
    `τοὖργον`, `θἀτέρου`, `θἄτερον` twice, `χἁπαλοὺς`, `τοὔφελος`, `προὐχώρουν`,
    `τἆλλα`, `τἀσκεπὲς`), `ῤῥ` twice, the iota subscript (`φυλῇ`, `ᾜτησέ`, `ᾜτουν`,
    `Τρῳάδες`, `κοιλίᾳ`, `Τοιᾷδ’`, `ὁρᾷν`; `σώζων` without), words (`Ἔκραξε`, `Οἴμοι`,
    `τοιᾶσδ’`, `Ῥεγιῶνος`, `συνυπάρξῃ`, `διεκλόνησεν`), punctuation (the nested quotes
    of `234` 7 and `238` 15; a comma `238` 18), the ornament lines emptied (with the
    dashes of `237` 3 closed up), and the signatures.
  - **Misprints**, 8 (misprints.tsv): `234`, `252` `ᾀεὶ` and `248` `ᾈεὶ` (held, "Open
    points" in PLAN.md), `238` `δακτυλῳ` and `252` `θελειν` (no accent), `248` `Α΄` for
    `Λ΄` in the running head, `250` 7 one comma of `„`, `256` `Ρώμῃ` (no breathing).
  - **Printed**, 11: the retype's errors (below).
  - **`213` `τἆχθος`** (retype 10) unmarked: the crasis lengthens the alpha, as `τἆλλα`
    (`256` 8); its row of misprints.tsv removed and its readcheck row changed to misread
    (PLAN.md "Settled readings").
- **The retype** (Flash) erred in about 11 places in 25 pages: an upper dot for a period
  (`235` 9, 21; `257` 4), for a spacing mark (`237` 11, `242` 12) and for nothing (`243`
  3, `246` 10), `Ἥν` for `Ἣν`, `τετμημένου`, `Προυειλόμην`, `ζῴων`, `κἁπαλοὺς`. It wrote
  the nested quotes `, „` with a comma. Retypes 03–10 (Flash): about 13, 16, 10, 12, 8,
  5, 7 and 9.
- `convert_grc.py`: its report as the baseline; `texts/grc` regenerated (cantos
  XXVIII–XXXI). `misprints.py`: 54 rows, 54 marks, 0 problems.
