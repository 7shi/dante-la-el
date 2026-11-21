# Plan

The grammar commentaries still to be made, in this order; step 1 (`grammar/en/`) and step 2 (`grammar/en-oelsner/`, `grammar/en-purgatorio/`, `grammar/en-paradiso/`) are done (see [DONE.md](DONE.md)). Each is written in English by [scripts/grammar.py](README.md#scriptsgrammarpy); the user runs the model, and each set is reviewed once all its cantos are done. The translations they need from `commentary/` are planned in [commentary/PLAN.md](../commentary/PLAN.md), and what remains on the reports of `editions/` in [editions/PLAN.md](../editions/PLAN.md).

| Step | Output | Source | Explained against | Canticles |
|---|---|---|---|---|
| 3 | `commentary/en-grc/`, then `grammar/grc/` | Musurus's Greek (`texts/grc/`) | Oelsner's Italian and English beside the Greek and a literal English of it (`commentary/en-grc/`) | Inferno |
| 4 | `grammar/el-grc/` | Musurus's Greek (`texts/grc/`) | the Modern Greek translation of it (`commentary/el-grc/`) | Inferno (Purgatorio and Paradiso: see the step) |
| 5 | `grammar/la/` | Serravalle's Latin (`texts/la/`) | the Italian of the same edition; both with a new English translation | Inferno, Purgatorio, Paradiso |

## Sync with main

The `el` and `commentary` branches have been merged into `main` (see [DONE.md](DONE.md)), and work continues on a fresh `commentary` branch from `main`. If `translations` or other work on `main` changes `texts/en*`, run `fix_quote_blocks.py`, check any affected English quotes and bullets in `grammar/`, and check the reports as [editions/PLAN.md](../editions/PLAN.md) says.

## 3. grammar/grc

The main subject is how Musurus translated the Italian into Greek, so that learners of Italian and of Greek can follow a translation of the poem into the older language. As the commentary is written in English, both sides are given with a literal English translation, and the Greek is explained against the Italian:

- **(it, en-oelsner)**: the Italian of Oelsner's edition with Oelsner's English, tercet by tercet. Oelsner's English renders his own Italian, so the two are kept together: Oelsner's English is not set beside the Italian of dante-corpus, whose readings differ from his in many lines (see [editions/it-carlyle.md](../editions/it-carlyle.md)). Which Italian text Musurus translated is not known, so no edition matches the Greek everywhere; where the Greek follows another reading, the commentary says so.
- **(grc, en-grc)**: the Greek with a literal English translation of it, `commentary/en-grc/`. Musurus departs from the Italian in places, so the English of the Italian cannot stand for the Greek.

Steps:

1. Generate and check `commentary/en-grc/` (all 34 cantos; see [commentary/PLAN.md](../commentary/PLAN.md)). Note: `translations/en/grc/` (merged on `main` in `524fe966`) already provides a line-by-line English translation of Musurus's Greek; decide before starting step 3 whether to reuse it instead of generating `commentary/en-grc/`.
2. A new mode of `grammar.py` for `grammar/grc/` (how it is called, beside the existing grc mode of step 4, is settled then): the Greek and `en-grc` line by line, Oelsner's Italian and English by tercet (`source.oelsner_passages`), sent passage by passage, with the repair of a rejected answer and the rejections listed at the end of a run, as in the en mode.
3. Trial on a canto or two, tune the prompt, then the whole Inferno.

`commentary/el-grc/` is not quoted in `grammar/grc/`: a third translation beside each line would make the commentary too complex. It has a commentary of its own in step 4. Where `el-grc` and `en-grc` read a line differently, the Greek may be hard there; this can be used when reviewing.

## 4. grammar/el-grc

`commentary/el-grc/` is a Modern Greek translation of Musurus's Greek, made for speakers of Modern Greek. `grammar/el-grc/` compares the two in English: Musurus's Greek explained line by line, and how the Modern Greek renders its forms and constructions. This is what the grc mode of `grammar.py` was first written for (`make grammar CANTICLE=inferno SOURCE=grc`, with the default `LANG=el`), and it is kept apart from `grammar/grc/`, whose subject is the translation from the Italian.

- Before starting step 4, check `commentary/el-grc/` against the `texts/grc/` misprint fixes applied on `main` (`524fe966`, 14 cantos) with `make check-quotes` and update any affected lines.
- The grc mode still works by sections of about 30 lines and retries a rejected answer from scratch; it is reworked like the en mode (repair of a rejected answer, rejections listed at the end of a run), keeping its own check that every line and its translation are quoted unchanged.
- The model does not change the translation; where it finds `el-grc` wrong, it writes a `Translation note:`. After the run: `make grammar-notes` lists them, the `.txt` of `commentary/el-grc/` is corrected by hand, and `make fix-grammar-quotes` rebuilds the quotes.
- Trial on a canto or two, tune the prompt, then the whole Inferno.

Musurus translated only the Inferno, so `commentary/el-grc/` has no Purgatorio or Paradiso. In their place, `commentary/el/purgatorio/` and `commentary/el/paradiso/` (the model's Modern Greek translation of the Italian of dante-corpus) could serve, with the existing it mode of `grammar.py` (`make grammar CANTICLE=purgatorio`, with `LANG=el`, into `grammar/el-it/`); whether they are to be explained is open.

## 5. grammar/la

Serravalle's Latin translation (`texts/la/`) of all three canticles, printed line by line beside the Italian of Bartolommeo da Colle's manuscript. The aim is much the same as with Musurus's Greek in step 3: to let learners of Italian and of Latin follow a medieval translation of the poem. So both sides get an English translation, and the Latin is explained against the Italian:

- **(it, en)**: the Italian of this edition with a new English translation of it, line by line. The Italian differs widely from the modern text and from Oelsner's (see [texts/la/README.md](../texts/la/README.md)), so no existing English renders it.
- **(la, en-la)**: the Latin with a literal English translation of it, `commentary/en-la/`.
- The two sources of `commentary/scripts/source.py` and both English translations are made and checked first (see [commentary/PLAN.md](../commentary/PLAN.md)).
- The mode of `grammar.py` is to follow the one made for `grammar/grc/` in step 3; the details are settled after that step has been tried.
- The Purgatorio and the Paradiso are done as in step 2: the Inferno first, then the other two canticles.

## After the merge into main

- Update the root README for this directory.
