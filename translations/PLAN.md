# Plan: Japanese translations in `translations/ja/`

Project plan for translating the editions in [`texts/`](../texts/) into
`translations/ja/{dir}/` on the `translations` branch. The reusable workflow, script
usage (`pages.py`, `proper_names.py`), review checklist, and issue disposition rules are
documented in [`GUIDE.md`](GUIDE.md); completed work is recorded in [`DONE.md`](DONE.md).

## State (2026-11-20)

- **Done** ([`DONE.md`](DONE.md)):
  - `ja/en/` (`001`–`041`, Carlyle's *Inferno*): all 41 files translated, checked, and committed; `for-main.tsv` items resolved.
  - `ja/en-oelsner/` (`001`–`041`, Temple Classics *Inferno*): all 41 files (title page, Cantos I–XXXIV, end matter, and index) translated, reviewed, checked, and committed (5 misprints in `ja/en-oelsner/misprints.tsv`; `for-main.tsv` items resolved on `main`).
  - `ja/en-purgatorio/` (`001`–`040`, Temple Classics *Purgatorio*): all 40 files (title page, Cantos I–XXXIII, end matter, and index) translated, reviewed, checked, and committed (10 misprints/author errors in `ja/en-purgatorio/misprints.tsv`, 1 entry in `joins.tsv`; `for-main.tsv` items resolved on `main`).
  - `ja/en-paradiso/` (`001`–`039`, Temple Classics *Paradiso*): all 39 files (title page, Cantos I–XXXIII, end matter, and index) translated, reviewed, checked, and committed (6 misprints in `ja/en-paradiso/misprints.tsv`, 1 entry in `joins.tsv`; `for-main.tsv` items resolved on `main`).
  - Proper-name audit & tables: generated `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` and `ja/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` (449 / 363 / 379 poem-body entries), unified transliterations across all sections of all four English volumes, and moved `ja/PROPER_NAMES.{md,tsv}` to `ja/en/PROPER_NAMES.{md,tsv}`.
- **Next**:
  - Plan and execute the `grc` and `la` translations (see [`GUIDE.md`](GUIDE.md) Step 6).

## Project-specific conventions

General workflow, cross-page joining, delegate task format, review checks, and misprint
handling follow [`GUIDE.md`](GUIDE.md). Project-specific decisions:

### Scope and files

- **Branch boundary**: on `translations`, only `translations/` is touched (with the
  explicit exception of `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`).
  Everything to fix in `ocr/` or `texts/` is recorded in [`for-main.tsv`](for-main.tsv)
  and applied on `main`.
- **What is translated**: prefaces, essays, arguments, and notes; for the English editions,
  also the English prose translation of the poem (translated from the English, not from the
  Italian) and the glosses under the verse (`1\. Bruno, brown, dark, obscure.`, 97 in `en`).
  The Italian verse and the verse translations of `la` and `grc` are not translated now.
- **Scripts and records**:
  - Run [`scripts/pages.py`](scripts/pages.py) with `uv run python translations/scripts/pages.py …`
    (or `python3 translations/scripts/pages.py …` when `uv run` cannot see `../dante-corpus`
    in a sandbox).
  - Cross-page join overrides: [`joins.tsv`](joins.tsv).
  - Proper-name conventions & per-canto filter: [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md),
    `ja/{dir}/PROPER_NAMES.tsv`, and [`scripts/proper_names.py`](scripts/proper_names.py).
  - Verified misprints/author errors: `ja/{dir}/misprints.tsv`; items for `main`:
    [`for-main.tsv`](for-main.tsv).

### Style (Japanese)

- Plain written Japanese (である調), literal with readability (avoid Japanese em-dashes
  `——`), past tense where the English is; narrator is 私.
- **Speech**:
  - `en`: plain form (常体), except Dante’s speeches to Virgil, which are in polite form
    (敬語 / です・ます調).
  - Temple Classics (`en-oelsner`, `en-purgatorio`, `en-paradiso`): plain form (常体) for
    every speaker.
  - `thou` / respectful `you` (Italian `voi`) is あなた (never お前); plural `ye`/`you` is
    あなたがた.
- **Virgil and titles**: `"Master"` in speech is 師よ (`"My Master"` is 我が師よ; never
  先生); `"Master"` in narration is 師 (`"my Master"` is 我が師); `"Guide"` is 導き手;
  `"Escort"` is 案内人; `"Leader"` is 先導者.
- **Quotation marks and footnotes**: `「」` and nested `『』` (unclosed opening `「` when a
  speech continues into the next paragraph); footnote references (`[^N-M]`) immediately
  after the target word, before `。`, `、`, and `」`.
- **Proper names and citations**: katakana per [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md)
  and `ja/{dir}/PROPER_NAMES.tsv`; work titles in `『』` (*Comedy* = 『喜劇』); keep
  bibliographic references and parenthetical commentator citations (`Benv. da Imola`,
  `Ottimo Com.`, `Ovid, *Metam*.`) as written (katakana when used as sentence subjects);
  `Lit.:` → 直訳では, `"See X"` → `X を参照`, `"Compare X"` → `X と比較せよ`.
- **Temple Classics markup**: translate `<!-- label: ... -->` inside the comment on English
  paragraphs (leave Italian verse labels out); omit editorial revision brackets `[...]`;
  preserve trailing `\` line breaks in map captions, diagrams, and genealogical/chronological
  tables.

## Not settled

- **Classical editions (`la` and `grc`)**: the Latin commentary of `la` (about 1,300 scans),
  the Greek prologue, arguments, and notes of `grc`, and how words in italics are handled
  there. Follow the two-stage workflow in [`GUIDE.md`](GUIDE.md) Step 6, conforming Stage 1
  English proper names to `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` and
  `translations/ja/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` (plus
  [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md)).

## Remaining steps

1. `la` and `grc`.
2. A README of `translations/`, and the conversion into HTML.

Commits when the user asks.
