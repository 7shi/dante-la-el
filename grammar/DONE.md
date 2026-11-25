# Done

The items of [PLAN.md](PLAN.md) that are done.

## 1. grammar/en

`make grammar CANTICLE=inferno SOURCE=en`: the Italian of Carlyle's edition (`texts/en/`) compared block by block with his English (`editions/en-blocks.txt`): where the English departs from a word-for-word rendering, and how. Cantos 1–2 were tried and the prompt tuned on them; then all 34 cantos of the Inferno were generated (gpt-6-astra).

The review (2026-11-16):

- Checked by script over all 34 cantos: every canto has its summary; the sections run from line 1 to the last line of the canto with no gap or overlap; every Italian word in italics in a bullet is found in the lines of its range (one bullet takes up a word of a later line of the same block, *Quante … lucciole*, XXVI 25–29). No bullet is out of form, and there are no translation notes. Bullets per line (1.3–1.7) and the length of the summaries (340–455 words) are even over the cantos.
- No bullet is given only to a subject supplied from the verb ending or to an article before a possessive left out; these are summed up in the summaries. The bullets whose rendering differs from the translation only in an article (about 160) are kept, as words supplied or left out.
- Read: cantos IX 43–54, XXI 65–76, XXXIII 1–21 in full, and 40 bullets drawn at random from all cantos. The renderings, the word order, the changes of construction, and the choices of words are described correctly; where a reading is open, it is given as Carlyle's (*dov’ era* IV 105, *Vedi* XXVII 24). Nothing was corrected.

## Rebase onto main

The el branch was rebased onto main (903e1f18), which added to `texts/` what the later steps need:

- the leaf of Oelsner's Inferno with pp. 385–386 (canto XXXIV), so that `source.oelsner_passages` reads every spread of the Inferno;
- three misprints of Oelsner's Italian corrected (`abbandono` II 34, `corrono` XV 122, `rimanga` XXIX 22);
- `texts/en-purgatorio/` and `texts/en-paradiso/`, the Temple Classics Purgatorio and Paradiso, with Oelsner's Italian and Okey's English facing it tercet by tercet.

The reports of `editions/` were checked and updated after it (see [editions/DONE.md](../editions/DONE.md)).

## Merge into main and texts/en update

The `el` branch was merged into `main`, and the `translations/for-main.tsv` fixes in `texts/en/` (`c3119649`, including three missing quotation marks in Carlyle's English in cantos II and VII) were checked against `grammar/en/`:

- `fix_quote_blocks.py -s en -d en -n` reported no changes to the Italian quote blocks.
- The three missing quotation marks in Carlyle's English were restored in `grammar/en/008-canto-02.md` (lines 78 and 108) and `grammar/en/013-canto-07.md` (line 66).
- Work continues on the `commentary` branch, branched from `main` (`8498fc85`).

## 2. grammar/en-oelsner

`make grammar CANTICLE=inferno SOURCE=en-oelsner`: the Italian of the Temple Classics Inferno (`texts/en-oelsner/`, edited by Oelsner) compared spread by spread (`source.oelsner_passages`) with Carlyle's English revised by Oelsner (keeping his square brackets; see [editions/en-carlyle-oelsner.md](../editions/en-carlyle-oelsner.md) and [editions/it-carlyle.md](../editions/it-carlyle.md)). All 34 cantos of the Inferno were generated (`gpt-6-astra`).

The review (2026-11-19):

- `fix_quote_blocks.py -s en-oelsner -d grammar/en-oelsner -n` reported no changes, and `grammar.py --notes` found no translation notes.
- Checked by script over all 34 cantos: every canto has its summary; the sections match `source.oelsner_passages` from line 1 to the last line of the canto with no gap or overlap; the English joined per section matches the source word for word; every double-quoted phrase in the bullets and summaries is found in the English. Bullets per line (1.23–1.60, mean 1.41) and the length of the summaries (354–431 words, mean 392) are even over the cantos.
- No bullet is given only to a subject supplied from the verb ending, an article before a possessive left out, or capitals, punctuation, or spelling. The bullets whose rendering differs from the translation only in an article (148) are kept. Of the three Italian phrases not matching verbatim within their range, two are an unelided or shortened form (*non par che* VI 45, *tante nuove travaglie e pene, quante* VII 19–20) and one takes up a word of the next range of the same block (*Quante … lucciole* XXVI 25–28). Oelsner's bracketed revisions are handled cleanly against the Italian.
- Read: cantos II 13–45, XVII 109–134, and XXXIII 1–39 (with summaries of I, IX, and XXXIII) in full, and 40 bullets drawn at random from all cantos.
- Corrected (3 files):
  - `029-canto-28.md` (lines 75, 79): balanced emphasis markers (`*`) inside two quoted English spans.
  - `033-canto-32.md` (line 93): normalized the literal gloss of *il nome tuo* to `‘the name thy’ → “thy name”`.
  - `034-canto-33.md` (line 15 and summary): recognized Old Italian dative *i* (‘to him’) in *perchè i son tal vicino* rather than treating “to him” as supplied, and replaced that summary example with *di sopra* → “above on earth”.

## 2. grammar/en-purgatorio

`make grammar CANTICLE=purgatorio SOURCE=en-purgatorio`: the Italian of the Temple Classics Purgatorio (`texts/en-purgatorio/`, edited by Oelsner) compared spread by spread (`source.oelsner_passages`) with Thomas Okey's English translation. All 33 cantos of the Purgatorio were generated (`gpt-6.2-astra`).

The review (2026-11-20):

- `fix_quote_blocks.py -s en-purgatorio -d grammar/en-purgatorio -n` reported no changes, and `grammar.py --notes` found no translation notes.
- Checked by script over all 33 cantos: every canto has its summary; the sections match `source.oelsner_passages` from line 1 to the last line of the canto with no gap or overlap; the English joined per section matches the source word for word; every double-quoted phrase in the bullets and summaries is found in the English with balanced emphasis markers (`*`, `_`). Bullets per line (1.24–1.53, mean 1.36) and the length of the summaries (246–324 words, mean 286) are even over the cantos.
- No bullet is given only to a subject supplied from the verb ending, an article before a possessive left out, or capitals, punctuation, or spelling. The bullets whose rendering differs from the translation only in an article (133) are kept. Of the four remaining Italian phrases not matching verbatim within their range, all take up words of the end of the preceding line carried over into the English of that range (*ma, se a voi piace cosa ch' io possa* V 60–61, *io scoppio* XVI 54, *ch' io venni presta ad ogni tua question* XXVIII 84, *ed esso mi rispose* XXIX 57).
- Read: cantos III 115–145, XVI 1–39, and XXX 1–39 (with summaries of III, XVI, and XXX) in full, and 40 bullets drawn at random from all cantos.
- Corrected (6 files):
  - `003-canto-02.md` (line 118): fixed Italian typo *apparsen ali* → *apparser ali*.
  - `004-canto-03.md` (line 601, summary): fixed doubled article in `becomes a “sharp a sting” in the exclamation “how sharp a sting”` → `becomes “how sharp a sting” in the exclamation`.
  - `006-canto-05.md` (line 154): removed soft hyphen (`U+00AD`) in *facciangli onore*.
  - `015-canto-14.md` (line 204): fixed Italian typo *ad a lor* → *a lor*.
  - `020-canto-19.md` (line 317): corrected *agli alti saliri* to the source reading *verso gli alti saliri* and dropped the claim of a preposition change.
  - `031-canto-30.md` (line 226): fixed Italian typo *ad ben far* → *a ben far*.

## Merge into main and texts/en-* update (71c2b827)

The `commentary` branch was merged into `main` (`b565e9da`), and the `translations/for-main.tsv` fixes in `texts/en-oelsner/` and `texts/en-purgatorio/` (`71c2b827`) were applied:

- `fix_quote_blocks.py -s en-oelsner -d grammar/en-oelsner` updated `grammar/en-oelsner/010-canto-09.md` (closing quotation mark on line 131); `en-purgatorio` had no Italian quote-block changes.
- Restored missing closing quotation marks in the English of `grammar/en-oelsner/008-canto-07.md` (line 66) and `grammar/en-purgatorio/` (`023-canto-22.md` line 154, `028-canto-27.md` line 142, `032-canto-31.md` line 12).
- Fixed the displaced turnover `[discerned!` in the English of `grammar/en-purgatorio/013-canto-12.md` (lines 61–63) and updated the bullet for *che lì si discerne*.
- `grammar/en-paradiso/` has not been generated yet, so the `texts/en-paradiso/` fixes will be picked up automatically.
- Work continues on the `commentary` branch, recreated from `main` (`b565e9da`).

## 2. grammar/en-paradiso

`make grammar CANTICLE=paradiso SOURCE=en-paradiso`: the Italian of the Temple Classics Paradiso (`texts/en-paradiso/`, edited by Oelsner) compared spread by spread (`source.oelsner_passages`) with Philip H. Wicksteed's English translation. All 33 cantos of the Paradiso were generated (`gpt-6.2-astra`).

The review (2026-11-21):

- `fix_quote_blocks.py -s en-paradiso -d grammar/en-paradiso -n` reported no changes, and `grammar.py --notes` found no translation notes.
- Checked by script over all 33 cantos: every canto has its summary; the sections match `source.oelsner_passages` from line 1 to the last line of the canto with no gap or overlap; the English joined per section matches the source word for word; every double-quoted phrase in the bullets and summaries is found in the English with balanced emphasis markers (`*`, `_`). Bullets per line (1.24–1.54, mean 1.40) and the length of the summaries (246–344 words, mean 292) are even over the cantos.
- No bullet is given only to a subject supplied from the verb ending, an article before a possessive left out, or capitals, punctuation, or spelling. The bullets whose rendering differs from the translation only in an article (123) are kept. Of the remaining Italian phrases not matching verbatim within their range, two give an unelided form (*se egli avesse sol da sè dimesso* VII 115–117, *che uscir dovea* XII 64–66), one joins a word hyphenated across a line break (*differentemente danzando* XXIV 16–17), and ten take up words of the end of the preceding line carried over into the English of that range (*e così stolto ritrovar puoi* V 68–69, *e le palle dell' oro* XVI 110–111, *e già era buon cittadino Giuda ed Infangato* XVI 122–123, *sapete quale è quello dubbio* XIX 32–33, *in quella sola* XXII 65–66, *Quel medesmo* XXIV 104–105, *per che* XXVII 5–6, *quella* and *pria venne* XXVII 11–12, *ch’* XXX 146–147).
- Read: cantos I 1–45, XVII 40–72, and XXXIII 1–39 and 136–145 (with summaries of I, XVII, and XXXIII) in full, and 40 bullets drawn at random from all cantos.
- Corrected (8 files):
  - `004-canto-03.md` (line 404): dropped the stray prefix `*a più su* — in the text,` before `*donna più su*`.
  - `005-canto-04.md` (line 306): removed soft hyphen (`U+00AD`) in *possendo ritornare*.
  - `008-canto-07.md` (lines 310–311): folded the no-op `- *l' umana creatura* → “the human creature”: literal.` bullet into the preceding bullet on *Di tutte queste cose s' avvantaggia l' umana creatura*.
  - `010-canto-09.md` (line 227): fixed *lo pesasse* to the source reading *il pesasse*.
  - `011-canto-10.md` (line 261): fixed corrupted Thai characters in *cinger la figlia di Latona vedem talvolta*.
  - `012-canto-11.md` (line 58): fixed split word *fer mossi* → *fermossi*.
  - `016-canto-15.md` (line 514): cleaned up self-correction phrasing in `- *Saria tenuta allor tal maraviglia* ‘would be held then such a marvel’ → “Then” … “would have been as great a marvel”`.
  - `034-canto-33.md` (lines 455–456): merged the empty-quote bullet `- *guardando* ‘in looking’ → “”` into the preceding bullet on *s' avvalorava in me, guardando*.

## 3. grammar/grc

`make grammar CANTICLE=inferno LANG=en SOURCE=grc`: Musurus's Greek (`texts/grc/`) explained against the Italian of Oelsner's edition with his English (`texts/en-oelsner/`, spread by spread by `source.oelsner_passages`), each Greek line followed by its English from `translations/en/grc/`. Canto 1 was tried first (`de236eb7`); then all 34 cantos of the Inferno were generated (`gpt-6.2-astra`, `465ca7d6`).

The review (2026-11-26):

- `fix_quote_blocks.py -s grc -d grammar/grc -n` reported no changes, and `grammar.py --notes` found no translation notes.
- Checked by script over all 34 cantos: every canto has its summary; the sections match `source.oelsner_passages` from line 1 to the last line of the canto with no gap or overlap; every range has its Italian quote, Oelsner's English, the Greek and its English as quoted from the sources, and a list of bullets with no nesting; the English joined per section matches the source word for word. No invisible or stray characters, and no unbalanced `*` or quotation marks. Bullets per line (1.07–1.21, mean 1.13) and the length of the summaries (308–422 words, mean 350) are even over the cantos. Bold (`**…**`, about 100 times) is used for contrastive emphasis (*designated **as***, *genitive **singular***) and is kept.
- Every italic quotation of two or more words was looked up in the lines of its range. The Italian ones not found there take up a neighbouring line or reorder a phrase, except one, corrected below. Of the Greek ones, about 70 take up a neighbouring line (Musurus's lines do not always match the Italian line for line), and the rest resolve crasis or elision (*καὶ ἐγώ* for *κἀγώ*) or give dictionary forms. The crasis resolutions were all checked.
- The main fault was in explanations of elision before a rough breathing: for *ἔνθ᾽*, *ἐνταῦθ᾽*, *ἄπιθ᾽*, and *εἴθ᾽* the model often claimed that *τ* had been aspirated to *θ*, though the *θ* belongs to the word, and in several places it called smoothly breathed words (*ὀλολυγμούς*, *ἔδει*, *ἤλθομεν*, *ἦν*, *ἐντεῦθεν*, *ἠχεῖ*) rough. Every claim of a rough breathing was then checked by script against the breathing of the word named.
- Read: cantos XVII 1–21 and XXXIV 85–139 (with the summary of XXXIV) in full, and 40 bullets drawn at random from all cantos.
- `texts/grc/` (and `ocr/grc/252.txt`) had *οὐμὸς* in XXX 143, where the page has *οὑμὸς*: a misread, corrected on `main` (see [Breathings of texts/grc](#breathings-of-textsgrc)); the bullet gives *οὑμός*.
- Corrected (24 files):
  - The Greek koronis (`᾽`) used as the apostrophe in 37 Italian elisions in the bullets of cantos XI, XVIII, XXI, and XXXI (*l᾽ occhio*) replaced by `’`.
  - *ἔνθα*, *ἐνταῦθα*, *ἄπιθι*, *εἴθε* claimed as aspirated on elision (26 bullets in 21 files): now simply elided. Three of these were garbled beyond the claim (`012-canto-09.md` line 126, `021-canto-18.md` line 88, `030-canto-27.md` line 392) and were rewritten.
  - `017-canto-14.md` (line 39): *ἀφίγμεθα* is perfect, not aorist; the garbled note on aspiration before *εἰς* was removed.
  - `036-canto-33.md` (line 559): *ἠχεῖ* is not rough-breathed.
  - `023-canto-20.md` (line 245): split word *ciasc heduno* → *ciascheduno*.
  - `015-canto-12.md` (line 342): *the supplied e ria e folle* → *Oelsner’s e ria e folle* (the Greek follows the reading *ira folle*).
  - `033-canto-30.md` (line 974): *οὐμός* → *οὑμός*, as printed.
  - `025-canto-22.md` (line 813): *ἡμῶν* with *σὺ μόνος* is partitive (‘you alone of us’), not comparative.

## Merge of PR #1 (en-grc) and grammar/grc update

PR #1 (`commentary/en-grc/`, the literal English of Musurus's Greek checked with `check-lines`, and its fixes reflected in `translations/en/grc/`) was merged into `main` (`807c3794`), after `grammar/grc/` had been merged (`b01e124e`). `commentary/en-grc/` and the verse of `translations/en/grc/` now have the same words line for line; `grammar/grc/` goes on quoting `translations/en/grc/`.

- `fix_quote_blocks.py -s grc -d grammar/grc` rewrote the English of 363 Greek lines in all 34 cantos (most of them words moved to another line, particles added, or words the Greek does not have dropped).
- No bullet refers to the English of the Greek; the bullets on the lines whose English changed most (a word moved across lines, as *τὴν σὴν βίβλον* I 83–84 or *ὄφει ἐχθρῷ* IX 76–77) explain the Greek itself and stand as written.
- The checks of the review were run again with no findings.
- After the verse of `translations/en/grc/` took the quote marks of the Greek (`198d3447`), `fix_quote_blocks.py` rewrote the English of 2,497 Greek lines in all 34 cantos (quote marks and apostrophes only); the checks were run again with no findings.

## Breathings of texts/grc

Before step 4, the breathings of `texts/grc/` were checked, as [PLAN.md](PLAN.md) set out after *οὐμὸς* was found in XXX 143; the list and the images are recorded in [ocr/grc/DONE.md](../ocr/grc/DONE.md) ("After the close: the breathing check").

- Listed: the words with both breathings (17 forms; all but two homographs used rightly), the reflexive *αὑτ-* kept apart as Musurus's usage, the crasis forms, and the words beginning with a vowel with no breathing.
- Seen in the images and decided: *οὑμὸς* (XXX 143), a misread, corrected; *Ἱερεμίου* (note to I. 45), printed smooth, marked as a misprint; *χἁπαλοὺς* (XXX 66), printed with the rough breathing, kept as printed (the bullet explains it so).
- On `main` (`23f607ee`): `ocr/grc/252.txt` and `289.txt`, `misprints.tsv`, `readcheck.tsv`, and `texts/grc/` reconverted (two lines changed).
- Here: `fix_quote_blocks.py -s grc -d grammar/grc` rewrote XXX 143 in `033-canto-30.md`, and its bullet now gives *οὑμός* as printed; the note is not in `grammar/`. `make check-quotes LANG=el SOURCE=grc`: 0 mismatches; no line of `commentary/el-grc/` depends on the breathing.

## Step 4 preparation: commentary/el-grc and the misprint fixes

`commentary/el-grc/` was checked against the `texts/grc/` misprint fixes of `main` (`524fe966`, 19 verse lines) and *οὑμὸς* (XXX 143), line by line with the Greek before and after.

- Three lines still rendered the misprint, and were corrected: IX 96 (*ἣ*, ‘but which’, for *ἢ*), XIV 132 (*τοίων* ‘such’ for *ποίων*), XIX 5 (*ὑμᾶς* ‘you’ for *ἡμᾶς*); the other lines already followed the corrected reading.
- XIV 132 and XIX 5 were wrong in the same way in `commentary/en-grc/` and `translations/en/grc/` (and `translations/ja/grc/` on `main`): now "from such streams" and "for you". `fix_quote_blocks.py` updated `grammar/grc/`, and the bullet on XIX 5 no longer contrasts the English (“not "for us"”).
- *Κογνάζε* (XXI 119), marked as a misprint for *Καγνάζε* in `524fe966`, is printed *Κογνάζ-* in both its places (XXII 106 *Κογνάζος*): Musurus's spelling, so the mark was reverted on `main`, and `grammar/grc/024-canto-21.md` quotes and explains *Κογνάζε*.
- `make check-quotes` with `LANG=el` and `LANG=en`, `SOURCE=grc`: 0 mismatches.
