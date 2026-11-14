# Plan

The grammar commentaries still to be made, in this order. Each is written in English by [scripts/grammar.py](README.md#scriptsgrammarpy); the user runs the model, and each set is reviewed once all its cantos are done.

| Step | Output | Source | Explained against | Canticles |
|---|---|---|---|---|
| 1 | `grammar/en/` | the Italian of Carlyle's edition (`texts/en/`) | Carlyle's English | Inferno |
| 2 | `grammar/en-oelsner/` | the Italian of Oelsner's edition (`texts/en-oelsner/`) | Oelsner's revision of Carlyle's English | Inferno |
| 3 | `commentary/en-grc/`, then `grammar/grc/` | Musurus's Greek (`texts/grc/`) | Oelsner's Italian and English beside the Greek and a literal English of it (`commentary/en-grc/`) | Inferno |
| 4 | `grammar/el-grc/` | Musurus's Greek (`texts/grc/`) | the Modern Greek translation of it (`commentary/el-grc/`) | Inferno |
| 5 | `grammar/la/` | Serravalle's Latin (`texts/la/`) | undecided | Inferno (Purgatorio and Paradiso on hold) |

## 1. grammar/en

`make grammar CANTICLE=inferno SOURCE=en`: the Italian of Carlyle's edition compared block by block with his English (`editions/en-blocks.txt`): where the English departs from a word-for-word rendering, and how. Cantos 1–2 were tried and the prompt tuned on them; the rest of the Inferno is being generated. To do: review all 34 cantos once they are done.

## 2. grammar/en-oelsner

The same comparison for Oelsner's edition: his English against his own Italian, which differs from Carlyle's in many readings (see [editions/en-carlyle-oelsner.md](../editions/en-carlyle-oelsner.md): the English follows Oelsner's Italian where the two differ, so each English is read with its own Italian).

- A source `en-oelsner` in `commentary/scripts/source.py` and `grammar.py`, cut by `source.oelsner_passages`: the Italian of an even page and the English of the odd page facing it. No hand-checked cuts are needed, since Oelsner prints the English one paragraph per tercet; whether a spread is small enough for one call, or is to be cut by tercets, is to be decided on a trial.
- Canto XXXIV: pp. 385–386 are missing from the scan, and no other copy has been found, so the gap stays for now. The Italian of p. 384 (lines 19–51) has no English, and the Italian of p. 386 (lines 52–84) is missing, though its English (p. 387) is there. The commentary must state the gap where it falls (lines 19–84, pp. 385–386 missing from the scan) rather than skip it silently; these lines are explained from Carlyle's edition in `grammar/en/`.
- The Italian of the two editions is compared in [editions/it-carlyle.md](../editions/it-carlyle.md); a block on a line where Oelsner reads otherwise than Carlyle needs no special handling, as each commentary keeps to its own edition.

## 3. grammar/grc

The main subject is how Musurus translated the Italian into Greek. As the commentary is written in English, both sides are given with a literal English translation, and the Greek is explained against the Italian:

- **(it, en-oelsner)**: the Italian of Oelsner's edition with Oelsner's English, tercet by tercet. Oelsner's English renders his own Italian, so the two are kept together: Oelsner's English is not set beside the Italian of dante-corpus, whose readings differ from his in many lines (see [editions/it-carlyle.md](../editions/it-carlyle.md)). Which Italian text Musurus translated is not known, so no edition matches the Greek everywhere; where the Greek follows another reading, the commentary says so.
- **(grc, en-grc)**: the Greek with a literal English translation of it. Musurus departs from the Italian in places, so the English of the Italian cannot stand for the Greek. `commentary/en-grc/inferno/<NN>.txt` is made like `commentary/el-grc/` (`make generate CANTICLE=inferno LANG=en SOURCE=grc`, one line per line of the Greek) and checked with `check-quotes` and `check-lines` before it is used.

Steps:

1. Generate and check `commentary/en-grc/` (all 34 cantos).
2. A new mode of `grammar.py` for `grammar/grc/` (how it is called, beside the existing grc mode of step 4, is settled then): the Greek and `en-grc` line by line, Oelsner's Italian and English by tercet (`source.oelsner_passages`), sent passage by passage, with the repair of a rejected answer and the rejections listed at the end of a run, as in the en mode.
3. Canto XXXIV, where Oelsner's pp. 385–386 are missing: lines 19–84 take the Italian and the English of Carlyle's edition instead, as printed, and the commentary states that they do. Carlyle's English is not revised after Oelsner's manner: a text made up so would be neither edition. Oelsner's English of lines 52–84 (p. 387) survives, but not his Italian of them, so it is not used either: it would pair one edition's English with the other's Italian. Carlyle's English is cut by pages, so its part for lines 19–84 is cut by hand at the tercets (before line 19 and after line 84), as `editions/en-blocks.txt` was.
4. Trial on a canto or two, tune the prompt, then the whole Inferno.

`commentary/el-grc/` is not quoted in `grammar/grc/`: a third translation beside each line would make the commentary too complex. It has a commentary of its own in step 4. Where `el-grc` and `en-grc` read a line differently, the Greek may be hard there; this can be used when reviewing.

## 4. grammar/el-grc

`commentary/el-grc/` is a Modern Greek translation of Musurus's Greek, made for speakers of Modern Greek. `grammar/el-grc/` compares the two in English: Musurus's Greek explained line by line, and how the Modern Greek renders its forms and constructions. This is what the grc mode of `grammar.py` was first written for (`make grammar CANTICLE=inferno SOURCE=grc`, with the default `LANG=el`), and it is kept apart from `grammar/grc/`, whose subject is the translation from the Italian.

- The grc mode still works by sections of about 30 lines and retries a rejected answer from scratch; it is reworked like the en mode (repair of a rejected answer, rejections listed at the end of a run), keeping its own check that every line and its translation are quoted unchanged.
- The model does not change the translation; where it finds `el-grc` wrong, it writes a `Translation note:`. After the run: `make grammar-notes` lists them, the `.txt` of `commentary/el-grc/` is corrected by hand, and `make fix-grammar-quotes` rebuilds the quotes.
- Trial on a canto or two, tune the prompt, then the whole Inferno.

## 5. grammar/la

Serravalle's Latin translation (`texts/la/`), printed line by line beside the Italian of Bartolommeo da Colle's manuscript. How it is to be explained is left open until `grammar/grc` and `grammar/el-grc` have been tried:

- The Italian of this edition differs widely from the modern text and from Oelsner's (see [texts/la/README.md](../texts/la/README.md)), and there is no English translation of it; whether the Italian side takes Oelsner's English, or something else, is undecided.
- A literal English of the Latin (`commentary/en-la/`, made like `commentary/en-grc/`) would be the counterpart of `commentary/en-grc/`.
- `commentary/scripts/source.py` has no `la` source yet: it is to read the Latin verse of `texts/la/` (interleaved with the Italian per tercet, with counted tercet numbers).
- The Purgatorio and the Paradiso have no English beside the Italian (both Carlyle's and Oelsner's editions are of the Inferno alone); they are on hold.

## After the merge into main

On the el branch the files of main are not changed; these wait for the merge:

- Update the root README for `commentary/`, `grammar/`, and `editions/`.
- Check against the page images the twelve unmarked one-word changes listed at the end of [editions/en-carlyle-oelsner.md](../editions/en-carlyle-oelsner.md); corrections go into `ocr/en/` or `ocr/en-oelsner/`.
