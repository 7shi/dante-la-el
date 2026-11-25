# Plan

The grammar commentaries still to be made, in this order; step 1 (`grammar/en/`), step 2 (`grammar/en-oelsner/`, `grammar/en-purgatorio/`, `grammar/en-paradiso/`), and step 3 (`grammar/grc/`) are done (see [DONE.md](DONE.md)). Each is written in English by [scripts/grammar.py](README.md#scriptsgrammarpy); the user runs the model, and each set is reviewed once all its cantos are done. The translations they need from `commentary/` are planned in [commentary/PLAN.md](../commentary/PLAN.md), and what remains on the reports of `editions/` in [editions/PLAN.md](../editions/PLAN.md).

| Step | Output | Source | Explained against | Canticles |
|---|---|---|---|---|
| 4 | `grammar/el-grc/` | Musurus's Greek (`texts/grc/`) | the Modern Greek translation of it (`commentary/el-grc/`) | Inferno (Purgatorio and Paradiso: see the step) |
| 5 | `grammar/la/` | Serravalle's Latin (`texts/la/`) | the Italian of the same edition; both with a new English translation | Inferno, Purgatorio, Paradiso |

## Sync with main

The `el` and `commentary` branches have been merged into `main` (see [DONE.md](DONE.md)), and work continues on a fresh `commentary` branch from `main`. If `translations` or other work on `main` changes `texts/en*`, run `fix_quote_blocks.py`, check any affected English quotes and bullets in `grammar/`, and check the reports as [editions/PLAN.md](../editions/PLAN.md) says.

## 4. grammar/el-grc

`grammar/el-grc/` shows English readers how Ancient Greek differs from Modern Greek: Musurus's Greek is explained in English line by line against `commentary/el-grc/`, a Modern Greek translation of it. The Greek explained is Musurus's printed text, as in `grammar/grc/`; the Modern Greek, made by the model, is set beside it as an aid, as the English of `translations/en/grc/` is in `grammar/grc/`. This is what the grc mode of `grammar.py` was first written for (`make grammar CANTICLE=inferno SOURCE=grc`, with the default `LANG=el`), and it is kept apart from `grammar/grc/`, whose subject is the translation from the Italian.

- Before starting step 4, check `commentary/el-grc/` against the `texts/grc/` misprint fixes applied on `main` (`524fe966`, 14 cantos) with `make check-quotes` and update any affected lines (the breathing check of `texts/grc/` is done and touched none: see [DONE.md](DONE.md#breathings-of-textsgrc)).
- `grammar/grc/` already explains the forms of the same Greek (tense, case, dictionary forms), so the prompt is to weight what has changed in Modern Greek (the infinitive, the dative, the participles, the optative, the vocabulary), not to explain the Greek a second time; this is tuned in the trial.
- The grc mode still works by sections of about 30 lines and retries a rejected answer from scratch; it is reworked like the en mode (repair of a rejected answer, rejections listed at the end of a run), keeping its own check that every line and its translation are quoted unchanged.
- The model does not change the translation; where it finds `el-grc` wrong, it writes a `Translation note:`. After the run: `make grammar-notes` lists them, the `.txt` of `commentary/el-grc/` is corrected by hand, and `make fix-grammar-quotes` rebuilds the quotes.
- Trial on a canto or two, tune the prompt, then the whole Inferno.

Musurus translated only the Inferno, so `commentary/el-grc/` has no Purgatorio or Paradiso. In their place, `commentary/el/purgatorio/` and `commentary/el/paradiso/` (the model's Modern Greek translation of the Italian of dante-corpus) could serve, with the existing it mode of `grammar.py` (`make grammar CANTICLE=purgatorio`, with `LANG=el`, into `grammar/el-it/`). This is left open (see [Later](#later)): there the text explained would be the model's translation, which has no printed source, whereas every other commentary here explains a printed text taken from the page images.

## 5. grammar/la

Serravalle's Latin translation (`texts/la/`) of all three canticles, printed line by line beside the Italian of Bartolommeo da Colle's manuscript. The aim is much the same as with Musurus's Greek in step 3: to let learners of Italian and of Latin follow a medieval translation of the poem. So both sides get an English translation, and the Latin is explained against the Italian:

- **(it, en)**: the Italian of this edition with a new English translation of it, line by line. The Italian differs widely from the modern text and from Oelsner's (see [texts/la/README.md](../texts/la/README.md)), so no existing English renders it.
- **(la, en-la)**: the Latin with a literal English translation of it, `commentary/en-la/`.
- The two sources of `commentary/scripts/source.py` and both English translations are made and checked first (see [commentary/PLAN.md](../commentary/PLAN.md)).
- The mode of `grammar.py` is to follow the one made for `grammar/grc/` in step 3; the details are settled after that step has been tried.
- The Purgatorio and the Paradiso are done as in step 2: the Inferno first, then the other two canticles.

## Later

Decided after the English commentaries are done, up to `grammar/la/`:

- **Whether `commentary/` is published**: the commentaries of `commentary/` are made by the model with no printed source, so whether they are published as HTML is open; `grammar/el-it/` (step 4) is decided with it.
- **A commentary for speakers of Modern Greek**: the natural audience of Musurus's Greek explained against Modern Greek. As all commentaries here are in English, a commentary in another language would add a level for the language of the commentary, as in `translations/<lang>/<source>/`: `grammar/<lang>/<source>/` (`grammar/en/grc/`, `grammar/el/grc/`, …; `grammar/scripts/` and the documents stay at the top). With it, `translations/el/grc/` would be made as `translations/en/grc/` was: a Modern Greek translation to accompany the Greek, in the layout of `texts/grc/` (front matter, arguments, and notes translated anew; the verse taken from `commentary/el-grc/`, which would then be its verse taken out line by line, as `commentary/en-grc/` is). That belongs to `translations/PLAN.md` on `main`.

## After the merge into main

- Update the root README for this directory.
