# Done: Japanese translations in `translations/ja/`

The record of completed work ([PLAN.md](PLAN.md)).

## Setup (`GUIDE.md`, `pages.py`, `joins.tsv`, `PROPER_NAMES`)

- [`GUIDE.md`](GUIDE.md): reusable post-OCR translation guide (principles, 8-step workflow, batch review checklist, issue dispositions, and two-stage classical-language workflow; cf. [`ocr/GUIDE.md`](../ocr/GUIDE.md)).

- [`scripts/pages.py`](scripts/pages.py): `prepare` (joins paragraphs across page markers and reports doubtful places), `check` (compares headings, page markers, footnote IDs, and paragraph structure, leaving verse out), and `finish` (inserts `<!-- first paragraph joined to p. ... -->` comments after page markers).
  - `is_verse` treats a one-line verse block ending in its line number as verse (`LONE_VERSE`, p. 243 of Canto XX in `en`), and treats a block with `\` line breaks whose lines exceed 100 chars as prose (p. 368 of Canto XXX in `en`).
  - Explicit `joins.tsv` decisions (`yes`/`no`) override the auto-join heuristic, and `file` entries are matched as `{dir}/{file}`.
- [`joins.tsv`](joins.tsv): decided (`yes`) for all five doubtful places in `en` (pp. 40, 45, 54, 153, 268), along with two pages where a speech runs on after a full stop with an unclosed quote (pp. 376, 402), and two `no` entries (`en-purgatorio/040-index-to-plates-tables-etc.md` p. 443 (455) and `en-paradiso/039-index-to-maps-diagrams-and-tables.md` p. 420 (430) before colophons on new pages; the earlier `no` entry for `en-purgatorio/006-canto-05.md` p. 58 (070) was retired after the truncated reference `121-12` was fixed on `main`).
- [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md), [`ja/en/PROPER_NAMES.tsv`](ja/en/PROPER_NAMES.tsv), [`ja/en-oelsner/PROPER_NAMES.tsv`](ja/en-oelsner/PROPER_NAMES.tsv), [`ja/en-purgatorio/PROPER_NAMES.tsv`](ja/en-purgatorio/PROPER_NAMES.tsv), [`ja/en-paradiso/PROPER_NAMES.tsv`](ja/en-paradiso/PROPER_NAMES.tsv), and [`scripts/proper_names.py`](scripts/proper_names.py): shared proper-name tables (aligned 1-to-1 with `texts/{en,en-oelsner,en-purgatorio,en-paradiso}/PROPER_NAMES.tsv`) and canto-filtering script for the English volumes.

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

## `ja/en-oelsner/` — Temple Classics *Inferno* (`001`–`041`, 2026-11-19 – 2026-11-20)

- **`001-title-page.md` and `041-index-to-maps-plates-and-tables.md`**: translated directly (`041` aligned with in-volume map/diagram/table captions, 14 blocks 1-to-1).
- **Cantos I–XXXIV and end matter** (`002`–`040`): prepared with `pages.py prepare` in `tmp/translate/en-oelsner/in/` and delegated to GPT-6 Luna (Codex) via cold-start task files `task-002.md`–`task-040.md` (speech in plain form [常体] for all speakers).
- **Batch review and landing** (`002`–`010`, `011`–`020`, `021`–`030`, `031`–`040`):
  - Checked all `{stem}.md`, `{stem}.tsv`, and `{stem}.txt` outputs against `texts/en-oelsner/` and `translations/ja/en/`.
  - Normalized canto headings (`# 第一歌`–`# 第三十四歌`), pronouns and titles (`あなた` / `あなたがた`, `師` / `師よ` / `我が師よ`, `導き手`), plain form in dialogue, quotation marks across multi-paragraph speeches, nested quotes (`『...』`), and `## 注` reference citations.
  - Restored and aligned all marginal labels (`<!-- label: ... -->`) on English paragraphs.
  - Preserved trailing `\` line breaks in map captions, genealogical tables (House of Este, Malatesta, Della Scala), and the classification table in `036-note-on-dantes-hell.md`.
  - Recorded 5 misprints in [`ja/en-oelsner/misprints.tsv`](ja/en-oelsner/misprints.tsv) (2 unclosed/extra quotation marks in `008-canto-07.md` and `010-canto-09.md`, 2 map-image spellings `S. Beneddeto` and `Verruchio` in `017-canto-16.md`, and `Farfarella` for `Farfarello` in the Argument of `023-canto-22.md`); all 3 editable-text items resolved on `main` (`71c2b827`).
  - Verified all files with `pages.py finish` and `pages.py check` (`same structure` on all prose-only files; expected `+V` only on files containing `\`-broken map/table blocks).

## `ja/en-purgatorio/` — Temple Classics *Purgatorio* (`001`–`040`, 2026-11-19 – 2026-11-20)

- **`001-title-page.md` and `040-index-to-plates-tables-etc.md`**: translated directly (`040` aligned with in-volume diagram/table captions, 14 blocks 1-to-1; added `p. 443 (455)` `no` entry to `joins.tsv`).
- **Cantos I–XXXIII and end matter** (`002`–`039`): prepared with `pages.py prepare` in `tmp/translate/en-purgatorio/in/` and delegated to GPT-6 Luna (Codex) via cold-start task files `task-002.md`–`task-039.md` (speech in plain form [常体] for all speakers).
- **Batch review and landing** (`002`–`010`, `011`–`020`, `021`–`030`, `031`–`039`):
  - Checked all `{stem}.md`, `{stem}.tsv`, and `{stem}.txt` outputs block-by-block against `texts/en-purgatorio/` and `translations/ja/en/PROPER_NAMES.{md,tsv}`.
  - Normalized canto headings (`# 第一歌`–`# 第三十三歌`), pronouns and titles (`あなた` / `あなたがた`, `師` / `師よ` / `我が師よ`, `導き手`, `案内人`, `先導者`), plain form in dialogue and prayers, quotation marks across multi-paragraph speeches, nested quotes (`『...』`), initial signatures (`H. O.`, `P. H. W.`, `I. G.`, `T. O.`), and `## 注` reference citations (`*v.*`, `*vv.*`, `p.`, `pp.`, `cf.` → `と比較せよ`, `See X` → `X を参照`).
  - Restored and aligned all marginal labels (`<!-- label: ... -->`) on English paragraphs, removed editorial square brackets (`[...]` / `［...］`), and preserved trailing `\` line breaks in maps, diagrams, and genealogical tables.
  - Recorded 10 verified misprints/author errors in [`ja/en-purgatorio/misprints.tsv`](ja/en-purgatorio/misprints.tsv) (checked against `ocr/en-purgatorio/*.png`); all 7 editable-text items (5 misprints + 2 transcription fixes in `013` and `036`) resolved on `main` (`71c2b827`), retiring the temporary `joins.tsv` entry for `006-canto-05.md`.
  - Verified all 39 files with `pages.py finish` and `pages.py check` (`same structure` on all prose-only files; expected `+V` [and `-P/+V` on `008` p. 86] only on files containing `\`-broken map/diagram/table blocks).

## `ja/en-paradiso/` — Temple Classics *Paradiso* (`001`–`039`, 2026-11-19 – 2026-11-20)

- **`001-title-page.md` and `039-index-to-maps-diagrams-and-tables.md`**: translated directly (`039` aligned with in-volume map/diagram/table captions, 18 blocks 1-to-1; added `p. 420 (430)` `no` entry to `joins.tsv`).
- **Cantos I–XXXIII and end matter** (`002`–`038`): prepared with `pages.py prepare` in `tmp/translate/en-paradiso/in/` and delegated to GPT-6 Luna (Codex) via cold-start task files `task-002.md`–`task-038.md` (speech in plain form [常体] for all speakers).
- **Batch review and landing** (`002`–`010`, `011`–`020`, `021`–`030`, `031`–`038`):
  - Checked all `{stem}.md`, `{stem}.tsv`, and `{stem}.txt` outputs block-by-block against `texts/en-paradiso/`.
  - Normalized canto headings (`# 第一歌`–`# 第三十三歌`), pronouns (`あなた` / `あなたがた` / `あなたたち`), plain form in dialogue and prayers, quotation marks across multi-paragraph speeches, nested quotes (`『...』`), initial signatures (`I. G.`, `P. H. W.`, `H. O.`), and `## 注` reference citations (removing `『...』` around Latin/abbreviated titles and fixing Italian/Latin leakage into English translations).
  - Restored, aligned, and unified all marginal labels (`<!-- label: ... -->`), including consistent sphere labels (`移ろいやすい者`, `名誉を求める者`, `愛欲の霊`, `思慮深い者`, `勇敢な者たち`, `正義の者たち`, `観想する者`, `救われた者たち`, `天使たち`, `勝利の教会`), and preserved trailing `\` line breaks in maps, diagrams, genealogical tables, and classification tables.
  - Recorded 6 verified misprints in [`ja/en-paradiso/misprints.tsv`](ja/en-paradiso/misprints.tsv) (checked against `ocr/en-paradiso/*.png`); all 9 editable-text items (6 misprints + 3 transcription fixes in `009`, `017`, `020`) resolved on `main` (`71c2b827`), with `ix. 1` synced in `ja/en-paradiso/020-canto-19.md`.
  - Verified all 38 files with `pages.py finish` and `pages.py check` (`same structure` on all prose-only files; expected `+V` only on files containing `\`-broken map/diagram/table blocks).

## Proper-Name Audit and Tables (English volumes, 2026-11-19)

- **Poem-body proper-name tables**:
  - Generated 1-to-1 aligned alphabetical tables for Temple Classics *Inferno* (449 entries), *Purgatorio* (363 entries), and *Paradiso* (379 entries), covering poem-body occurrences (`canto:line`) only:
    - [`texts/en-oelsner/PROPER_NAMES.tsv`](../texts/en-oelsner/PROPER_NAMES.tsv) ⇔ [`ja/en-oelsner/PROPER_NAMES.tsv`](ja/en-oelsner/PROPER_NAMES.tsv)
    - [`texts/en-purgatorio/PROPER_NAMES.tsv`](../texts/en-purgatorio/PROPER_NAMES.tsv) ⇔ [`ja/en-purgatorio/PROPER_NAMES.tsv`](ja/en-purgatorio/PROPER_NAMES.tsv)
    - [`texts/en-paradiso/PROPER_NAMES.tsv`](../texts/en-paradiso/PROPER_NAMES.tsv) ⇔ [`ja/en-paradiso/PROPER_NAMES.tsv`](ja/en-paradiso/PROPER_NAMES.tsv)
- **Cross-volume transliteration unification**:
  - Audited all sections (poem body, marginal labels, Arguments, Notes, maps, genealogical tables, and appendices) across `ja/en/`, `ja/en-oelsner/`, `ja/en-purgatorio/`, and `ja/en-paradiso/`.
  - Applied agreed unifications across 74 translation files and [`ja/en/PROPER_NAMES.tsv`](ja/en/PROPER_NAMES.tsv) (e.g., `ルーニ`, `ユノ`, `テヴェレ川`, `レテ`, `エウノエ`, `パッセロ岬`, `ペロロ岬`, `ソルデッロ`, `スカーラ`, `ウルビザーリア`, `シニガーリャ`, `プラトマーニョ`, `エリゼーオ`, `ウゴリーノ`, `マグラ川`, `アプリア`, `Valdi...` without middle dots; origin-country rule for `ベルナール`/`ベルナルド`, `シャルル・マルテル`, `アンリ`, `ジャンヌ`, `レーモン・ベランジェ`; Latin/Greek forms `ウェヌス`, `アエネイス`, `カティリナ`, `デイアネイラ`, `キンキナトゥス`, `イシドールス`, `ディオニュシウス`, `ペトルス・ロンバルドゥス`, `ベネディクトゥス十一世`).
  - Updated [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md) with all settled conventions (committed as `de2c9aea`, then moved `ja/PROPER_NAMES.{md,tsv}` into `ja/en/` to mirror the per-volume layout).

## `{en,ja}/grc/` — Musurus's Greek *Inferno* (`001`–`038`, 2026-11-20)

- **Arabic numerals unification** (`9acc78ae`): unified all four English volumes (`ja/en*`) to Arabic numerals, keeping kanji numerals only in fixed compounds and idioms.
- **`pages.py --keep-verse`** (`758566c7`): extended `translations/scripts/pages.py` to verify verse-block structure 1:1 alongside prose blocks.
- **Front/back matter (`001`–`003`, `038`) and Cantos I–XXXIV (`004`–`037`)**:
  - Completed all 38 files in two stages: Stage 1 English reference translations (`translations/en/grc/001`–`038`) → Stage 2 direct Japanese translations from Greek (`translations/ja/grc/001`–`038`, cross-checked against EN).
  - Preserved exact 1:1 line structure, `<!-- p. ... -->` page comments, trailing `\`, and 5-line numbers (`pages.py check --keep-verse` → `same structure` on `002-prologos.md` and all 34 cantos `004`–`037`; added 4 `no` entries to [`joins.tsv`](joins.tsv) for `grc/003-table-of-contents.md`).
  - Conformed proper names to `texts/en-oelsner/PROPER_NAMES.tsv` (EN) and `translations/ja/en-oelsner/PROPER_NAMES.tsv` (JA), while faithfully translating Musurus's Greek where it diverges from Dante's Italian.
  - Verified plain style (`常体`), Arabic numerals, balanced `「`/`」` quotes, and zero em-dashes across all 38 Japanese files.
  - Recorded 51 confirmed print/author misprints in [`ja/grc/misprints.tsv`](ja/grc/misprints.tsv) and 39 source/OCR/misprint items in [`for-main.tsv`](for-main.tsv) (including 3 genuine OCR/conversion fixes: `012-canto-09.md` p. 67 `Ἀλλ᾿ ἢ` → `Ἀλλ᾿ ἣ`, `021-canto-18.md` p. 138 dropped quotes, and `032-canto-29.md` p. 221 `Οὐμὸς` → `Οὑμὸς`).
