# Done: Japanese translations in `translations/ja/`

The record of completed work ([PLAN.md](PLAN.md)).

## Setup (`pages.py`, `joins.tsv`, `PROPER_NAMES`)

- [`scripts/pages.py`](scripts/pages.py): `prepare` (joins paragraphs across page markers and reports doubtful places), `check` (compares headings, page markers, footnote IDs, and paragraph structure, leaving verse out), and `finish` (inserts `<!-- first paragraph joined to p. ... -->` comments after page markers).
  - `is_verse` treats a one-line verse block ending in its line number as verse (`LONE_VERSE`, p. 243 of Canto XX in `en`), and treats a block with `\` line breaks whose lines exceed 100 chars as prose (p. 368 of Canto XXX in `en`).
- [`joins.tsv`](joins.tsv): decided (`yes`) for all five doubtful places in `en` (pp. 40, 45, 54, 153, 268), along with two pages where a speech runs on after a full stop with an unclosed quote (pp. 376, 402).
- [`ja/PROPER_NAMES.md`](ja/PROPER_NAMES.md), [`ja/PROPER_NAMES.tsv`](ja/PROPER_NAMES.tsv), and [`scripts/proper_names.py`](scripts/proper_names.py): shared proper-name table and canto-filtering script for `en`, `en-oelsner`, `en-purgatorio`, and `en-paradiso`.

## `ja/en/` — Carlyle's *Inferno* (`001`–`041`, 2026-11-18 – 2026-11-19)

- **Trial** (`002-preface-first-edition.md`, `007-canto-01.md`, `008-canto-02.md`):
  - Three files of `en`, all returned with the structure unchanged and the TSVs of misprints empty. The review found a few recurring delegate errors: a word or clause left out ("See" of a reference, "our own", "all", "good"), something added (古形 in a gloss, あなたが直面し), a sense shifted ("deserted" as 荒れ果てた, "though it was late" as 遅すぎた, "So Milton" as "therefore"), and a closing quotation mark misplaced.
  - `002-preface-first-edition.md`: seven joins, one paragraph over pp. viii–x. One mistranslation ("saying, Peace, peace; when there is no peace?") and one shifted sentence ("All anger and indignation…") corrected.
  - `007-canto-01.md`: done in two passes (Argument + 24 footnotes first, then prose); one split paragraph on p. 5 joined; verse quotation line break recorded in `for-main.tsv`.
  - `008-canto-02.md`: done in one pass (Argument, prose, 9 glosses, 21 footnotes). Speech registers normalized (plain form for speeches, polite form [敬語] with 師よ for Dante’s speeches to Virgil across all cantos). Two misprints found in review (`ja/en/misprints.tsv`).
- **Prefaces and essays** (`003`–`006`): structure unchanged except for three references of `004` set apart from the verse they belong to (removed in review). Fixed katakana/translated Italian and Latin titles (*Ottimo Comento*, *Libri titulus est*) and translated references (`Inf. x. 85`). Unified edition names across essays (ニドベアティーナ版, コミーノ版, ジュンタ版).
- **Cantos III–XXXIV** (`009`–`040`): translated in one pass per canto with GPT-6 Luna (Codex) as delegate, reviewed paragraph by paragraph against `texts/en/`, and checked `same structure` with `pages.py check`.
- **Title page and index** (`001-title-page.md`, `041-index-of-proper-names.md`): translated (`041` keeping English headwords with Japanese forms from `PROPER_NAMES.tsv`).
- **`for-main.tsv` & misprints**: all `en` misprints and transcription fixes resolved on `main` and reflected in `ja/en/`.

## `ja/en-oelsner/` — Temple Classics *Inferno* (`001`–`040`, 2026-11-19)

- **`001-title-page.md`**: translated directly.
- **Cantos I–XXXIV and end matter** (`002`–`040`): prepared with `pages.py prepare` in `tmp/translate/en-oelsner/in/` and delegated to GPT-6 Luna (Codex) via cold-start task files `task-002.md`–`task-040.md` (speech in plain form [常体] for all speakers).
- **Batch review and landing** (`002`–`010`, `011`–`020`, `021`–`030`, `031`–`040`):
  - Checked all `{stem}.md`, `{stem}.tsv`, and `{stem}.txt` outputs against `texts/en-oelsner/` and `translations/ja/en/`.
  - Normalized canto headings (`# 第一歌`–`# 第三十四歌`), pronouns and titles (`あなた` / `あなたがた`, `師` / `師よ` / `我が師よ`, `導き手`), plain form in dialogue, quotation marks across multi-paragraph speeches, nested quotes (`『...』`), and `## 注` reference citations.
  - Restored and aligned all marginal labels (`<!-- label: ... -->`) on English paragraphs.
  - Preserved trailing `\` line breaks in map captions, genealogical tables (House of Este, Malatesta, Della Scala), and the classification table in `036-note-on-dantes-hell.md`.
  - Recorded 5 misprints in [`ja/en-oelsner/misprints.tsv`](ja/en-oelsner/misprints.tsv) (2 unclosed/extra quotation marks in `008-canto-07.md` and `010-canto-09.md`, 2 map-image spellings `S. Beneddeto` and `Verruchio` in `017-canto-16.md`, and `Farfarella` for `Farfarello` in the Argument of `023-canto-22.md`), and added the 3 editable-text items to [`for-main.tsv`](for-main.tsv).
  - Verified all files with `pages.py finish` and `pages.py check` (`same structure` on all prose-only files; expected `+V` only on files containing `\`-broken map/table blocks).
