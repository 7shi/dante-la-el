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
