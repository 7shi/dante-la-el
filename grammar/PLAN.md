# Plan

The grammar commentaries still to be made, in this order. Each is written in English by [scripts/grammar.py](README.md#scriptsgrammarpy); the user runs the model, and each set is reviewed once all its cantos are done.

| Step | Output | Source | Explained against | Canticles |
|---|---|---|---|---|
| 1 | `grammar/en/` | the Italian of Carlyle's edition (`texts/en/`) | Carlyle's English | Inferno |
| 2 | `grammar/en-oelsner/` | the Italian of Oelsner's edition (`texts/en-oelsner/`) | Oelsner's revision of Carlyle's English | Inferno |
| 3 | `commentary/en-grc/`, then `grammar/grc/` | Musurus's Greek (`texts/grc/`) | Oelsner's Italian and English beside the Greek and a literal English of it (`commentary/en-grc/`) | Inferno |
| 4 | `grammar/el-grc/` | Musurus's Greek (`texts/grc/`) | the Modern Greek translation of it (`commentary/el-grc/`) | Inferno |
| 5 | `grammar/la/` | Serravalle's Latin (`texts/la/`) | undecided | Inferno (Purgatorio and Paradiso undecided) |

## 1. grammar/en

`make grammar CANTICLE=inferno SOURCE=en`: the Italian of Carlyle's edition compared block by block with his English (`editions/en-blocks.txt`): where the English departs from a word-for-word rendering, and how. Cantos 1–2 were tried and the prompt tuned on them; all 34 cantos have been generated and reviewed.

## Rebase onto main

The el branch has been rebased onto main, which added to `texts/` what the later steps need: the leaf of Oelsner's Inferno with pp. 385–386 (canto XXXIV), so that `source.oelsner_passages` reads every spread of the Inferno; three misprints of Oelsner's Italian corrected; and `texts/en-purgatorio/` and `texts/en-paradiso/`, the Temple Classics Purgatorio and Paradiso, with Oelsner's Italian and Okey's English facing it tercet by tercet. The comparison of the English was run again: the added leaf brings three differences in words (all `W`), and the reports were updated.

The texts are not settled yet: errors of transcription found while translating on the translations branch (`translations/for-main.tsv`) go into `ocr/` and `texts/` on main. The el branch is to be rebased again once the translations branch has been merged into main, and before it is merged itself. If `texts/en/` or `texts/en-oelsner/` change, `compare_editions.py en` is run again, the numbers of `editions/judge-en.txt` are checked against the new list, and the tables and counts of `editions/en-carlyle-oelsner.md` are updated; a change to the English of `texts/en/` may also call for a block of `grammar/en/` to be made again.

## 2. grammar/en-oelsner

The same comparison for Oelsner's edition: his English against his own Italian, which differs from Carlyle's in many readings (see [editions/en-carlyle-oelsner.md](../editions/en-carlyle-oelsner.md): the English follows Oelsner's Italian where the two differ, so each English is read with its own Italian).

- A source `en-oelsner` in `commentary/scripts/source.py` and `grammar.py`, cut by `source.oelsner_passages`: the Italian of an even page and the English of the odd page facing it. No hand-checked cuts are needed, since Oelsner prints the English one paragraph per tercet; whether a spread is small enough for one call, or is to be cut by tercets, is to be decided on a trial.
- The Italian of the two editions is compared in [editions/it-carlyle.md](../editions/it-carlyle.md); a block on a line where Oelsner reads otherwise than Carlyle needs no special handling, as each commentary keeps to its own edition.

## 3. grammar/grc

The main subject is how Musurus translated the Italian into Greek. As the commentary is written in English, both sides are given with a literal English translation, and the Greek is explained against the Italian:

- **(it, en-oelsner)**: the Italian of Oelsner's edition with Oelsner's English, tercet by tercet. Oelsner's English renders his own Italian, so the two are kept together: Oelsner's English is not set beside the Italian of dante-corpus, whose readings differ from his in many lines (see [editions/it-carlyle.md](../editions/it-carlyle.md)). Which Italian text Musurus translated is not known, so no edition matches the Greek everywhere; where the Greek follows another reading, the commentary says so.
- **(grc, en-grc)**: the Greek with a literal English translation of it. Musurus departs from the Italian in places, so the English of the Italian cannot stand for the Greek. `commentary/en-grc/inferno/<NN>.txt` is made like `commentary/el-grc/` (`make generate CANTICLE=inferno LANG=en SOURCE=grc`, one line per line of the Greek) and checked with `check-quotes` and `check-lines` before it is used.

Steps:

1. Generate and check `commentary/en-grc/` (all 34 cantos).
2. A new mode of `grammar.py` for `grammar/grc/` (how it is called, beside the existing grc mode of step 4, is settled then): the Greek and `en-grc` line by line, Oelsner's Italian and English by tercet (`source.oelsner_passages`), sent passage by passage, with the repair of a rejected answer and the rejections listed at the end of a run, as in the en mode.
3. Trial on a canto or two, tune the prompt, then the whole Inferno.

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
- The Purgatorio and the Paradiso: the Temple Classics volumes (`texts/en-purgatorio/`, `texts/en-paradiso/`) give Oelsner's Italian with Okey's English, as `texts/en-oelsner/` does for the Inferno, so the Latin of all three canticles could be set beside them; whether to go beyond the Inferno is decided with the rest of this step.

## After the merge into main

On the el branch the files of main are not changed; these wait for the merge:

- Update the root README for `commentary/`, `grammar/`, and `editions/`.
- Check against the page images the twelve unmarked one-word changes listed at the end of [editions/en-carlyle-oelsner.md](../editions/en-carlyle-oelsner.md); corrections go into `ocr/en/` or `ocr/en-oelsner/`.
