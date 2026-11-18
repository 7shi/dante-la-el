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
