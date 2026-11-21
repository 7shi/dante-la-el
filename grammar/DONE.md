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
