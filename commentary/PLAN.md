# Plan

The translations still to be made in this directory, for the grammar commentaries of [`grammar/`](../grammar/) (see [grammar/PLAN.md](../grammar/PLAN.md), which gives the order). Each is generated with `make generate`, or, for a literal English translation of a printed translation (`en-grc/`, `en-la-la/`), converted from an English translation made in [`translations/en/`](../translations/en/), and checked with `check-quotes` and `check-lines` before it is used; the user runs the model. This directory is the reference for such a translation: the fixes of `check-lines` are reflected in the verse of `translations/en/`, so that the two stay the same.

| Translation | Of | For |
|---|---|---|
| `en-la-it/` | the Italian of Bartolommeo da Colle's manuscript (`texts/la/`), three canticles | `grammar/la/` (step 5) |
| `en-la-la/` | Serravalle's Latin (`texts/la/`), three canticles | `grammar/la/` (step 5) |

## en-grc

A literal English translation of Musurus's Greek, one line per line of the Greek. The English of `translations/en/grc/` is made first, since there the translation is made together with its layout; `en-grc/` has been converted from it, checked with `check-quotes` and `check-lines` (four rounds over the Inferno: 285, 61, and 26 lines fixed, the last round leaving only issues rejected or with no fix), and the fixes reflected in `translations/en/grc/` (see [README.md](README.md)). It is done; `en-la-la/` is made the same way (see below).

Musurus departs from the Italian in places, so the English of the Italian cannot stand for the Greek; `grammar/grc/` sets this translation beside the Greek, quoting it from `translations/en/grc/`, which has the same words.

## The Italian and the Latin of texts/la

Serravalle's Latin translation is printed line by line beside the Italian of Bartolommeo da Colle's manuscript, in all three canticles. `grammar/la/` explains the Latin against the Italian, both with an English translation. As `texts/la/` holds both languages, the two sources are named after the edition and the language, `la-la` (the Latin) and `la-it` (the Italian), and their translations go to `en-la-la/` and `en-la-it/` (`<lang>-<source>`, as `en-grc/`).

- `scripts/source.py` reads them (`la-la`, `la-it`): the verse of the cantos of `texts/la/` (`008`–`041`, `043`–`075`, `076`–`108`; the Latin and the Italian interleaved per tercet), one source for each language, with line numbers counted from the tercet numbers (14,233 lines in each language, as in dante-corpus).
- `en-la-la/`: a literal English translation of the Latin, one line per line of the Latin. It has been taken from the English of the Latin tercets in a delegated draft of `translations/en/la/` (2026-11), line by line as it was, for all three canticles. The draft was not landed: its prose was condensed in many places, but its verse kept the tercets, with words moved between lines. Its quote marks have been removed, as the Latin has none, and so have the gloss markers the draft added (`(1)`: in `texts/la/` they stand in the Italian only, pointing to its glosses); `check-quotes` finds no mismatch. The gaps of the draft were filled by `make generate`: the blank Purgatorio 24, line 154, and Paradiso 12, lines 1–27, left in Latin. The first round of `check-lines` has been run over all three canticles at once (3,443 issues: 1,000, 1,257, and 1,186), and its fixes applied issue by issue after review (about 4,600 lines), some rejected or rewritten; it also replaced Paradiso 19, lines 1–6, which the draft had taken from the opening of Paradiso 3. The second round, over the changed cantos, found 1,030 issues (305, 382, and 343), mostly small words left out (`et`, `sic`, possessives) or added; its fixes were applied the same way (about 1,100 lines). The third round found 359 issues (110, 140, and 109), of the same kind, among them a `said` added to the verbless speech tags (`Et ego ad eum`), now left out; about 390 lines were changed. The fourth round found 160 issues (47, 63, and 50), again small words left out or added; about 170 lines were changed. The fifth round found 54 issues (23, 24, and 7), nearly all small words; 49 lines were changed, and the rounds end here.
- `en-la-it/`: a new literal English translation of the Italian, one line per line of the Italian, generated with `make generate LANG=en SOURCE=la-it`. The Italian of this edition differs widely from the modern text and from Oelsner's (see [texts/la/README.md](../texts/la/README.md)), so no existing English renders it: neither Oelsner's and Okey's English nor `en/` (which renders dante-corpus). It is used in `grammar/la/` only; `translations/` does not translate the Italian verse.
- The work is done on `main`, with no branch (the `la` branch, from `main` at `8e162c88`, was merged on 2026-11-28), together with the `la` prose of `translations/` (see [translations/PLAN.md](../translations/PLAN.md)); anything to fix in `ocr/` or `texts/` found on the way is still recorded in `translations/for-main.tsv`, to be applied together.

The steps, each canticle in turn, the Inferno first, then the Purgatorio and the Paradiso, as `grammar/la/` goes:

1. `en-la-la/`: done for all three canticles at once (the gaps filled, five rounds of `check-lines`, and the dashes and brackets left from the draft removed, keeping the parentheses that stand in the Latin).
2. `en-la-it/`: `make generate LANG=en SOURCE=la-it` over the canticle, then `check-quotes` and `check-lines` as above.
3. Once a canticle of `en-la-la/` is checked, the verse of `translations/en/la/` is taken from it as it is, without gloss markers, as the Latin has none (see [translations/PLAN.md](../translations/PLAN.md)); a fix found later is made here first and reflected there.

## en/

`en/` (the commentary and the line-by-line English translation of the Italian of dante-corpus, generated by the model for all three canticles) was made while the Temple Classics gave no English beyond the Inferno. With the printed English of the Purgatorio and the Paradiso (`texts/en-purgatorio/`, `texts/en-paradiso/`) it is no longer needed for that, but it is kept, as it cost much to generate; how it is to be used is open.

## After the merge into main

- Update the root README for this directory.
