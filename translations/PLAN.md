# Plan: Japanese translations in `translations/ja/`

Project plan for translating the editions in [`texts/`](../texts/) into
`translations/ja/{dir}/` on the `translations` branch. The reusable workflow, script
usage (`pages.py`, `proper_names.py`), review checklist, and issue disposition rules are
documented in [`GUIDE.md`](GUIDE.md); completed work is recorded in [`DONE.md`](DONE.md).

## State (2026-11-20)

- **Done** ([`DONE.md`](DONE.md)): all four English volumes (`ja/en/` `001`–`041`,
  `ja/en-oelsner/` `001`–`041`, `ja/en-purgatorio/` `001`–`040`, `ja/en-paradiso/`
  `001`–`039`), cross-volume proper-name audit and `PROPER_NAMES.tsv` tables,
  [`GUIDE.md`](GUIDE.md), and all `for-main.tsv` fixes merged and applied on `main`
  (`71c2b827`).
- **Next**: `grc` (Greek edition, 39 files), then `la` (Latin edition, 111 files),
  following the two-stage workflow in [`GUIDE.md`](GUIDE.md) Step 6.

## Project-specific conventions

General workflow, cross-page joining, delegate task format, review checks, and misprint
handling follow [`GUIDE.md`](GUIDE.md). Project-specific decisions:

### Scope and files

- **Branch boundary**: on `translations`, only `translations/` is touched (with the
  explicit exception of `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`).
  Everything to fix in `ocr/` or `texts/` is recorded in [`for-main.tsv`](for-main.tsv)
  and applied on `main`.
- **What is translated**: prefaces, essays, arguments, and notes (plus English prose and
  verse glosses for the English volumes, now complete). The Italian verse and the verse
  translations of `grc` and `la` are not translated now.
- **Scripts and records**:
  - Run [`scripts/pages.py`](scripts/pages.py) with `uv run python translations/scripts/pages.py …`
    (or `python3 translations/scripts/pages.py …` when `uv run` cannot see `../dante-corpus`
    in a sandbox).
  - Cross-page join overrides: [`joins.tsv`](joins.tsv).
  - Proper-name references: [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md),
    `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`,
    `ja/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`, and
    [`scripts/proper_names.py`](scripts/proper_names.py).
  - Verified misprints/author errors: `ja/{dir}/misprints.tsv`; items for `main`:
    [`for-main.tsv`](for-main.tsv).

### Style (Japanese)

- Plain written Japanese (である調), literal with readability (avoid Japanese em-dashes
  `——`), past tense where the source is; narrator is 私.
- **Speech**: plain form (常体) for all speakers (except Dante’s speeches to Virgil in
  `en`, which use polite form 敬語). `thou` / respectful `you` (`voi`) is あなた (never
  お前); plural `ye`/`you` is あなたがた.
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

## Not settled

- **`grc` (39 files)** and **`la` (111 files, ~1,300 scans)**:
  - How italics, Greek/Latin lemmas, and cross-page commentary structure are handled with
    `pages.py`.
  - Two-stage workflow ([`GUIDE.md`](GUIDE.md) Step 6):
    1. Translate `grc` / `la` into English first, conforming proper names to
       `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` and
       `translations/ja/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` (plus
       [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md)).
    2. Translate directly from `grc` / `la` into Japanese, using the English translation
       as reference for verification and refinement (not relay translation).

## Remaining steps

1. `grc` (Greek prologue, arguments, and notes; 39 files).
2. `la` (Latin commentary and front/back matter; 111 files).
3. `translations/README.md` (structure, excluded files, usage).
4. HTML side-by-side conversion pairing `texts/` and `translations/ja/`.
5. Resolve any new `for-main.tsv` items on `main` and merge.

Commits when the user asks.
