# Plan: Translations in `translations/{en,ja}/`

Project plan for translating the editions in [`texts/`](../texts/) into
`translations/en/{dir}/` (for `grc` and `la`) and `translations/ja/{dir}/`, first on the
`translations` branch (merged into `main` up to the `la` trial), then on the `la` branch
(merged on 2026-11-28); work now continues on `main`, with no branch. The reusable
workflow, script usage (`pages.py`, `proper_names.py`), review checklist, and issue
disposition rules are documented in [`GUIDE.md`](GUIDE.md); completed work is recorded in
[`DONE.md`](DONE.md).

## State (2026-11-28)

- **Done** ([`DONE.md`](DONE.md)): all four English volumes (`ja/en/` `001`–`041`,
  `ja/en-oelsner/` `001`–`041`, `ja/en-purgatorio/` `001`–`040`, `ja/en-paradiso/`
  `001`–`039`), Musurus's Greek *Inferno* (`{en,ja}/grc/` `001`–`038`, 38 files),
  cross-volume proper-name audit and `PROPER_NAMES.tsv` tables, [`GUIDE.md`](GUIDE.md),
  and all `en*` (`71c2b827`) and `grc` `for-main.tsv` fixes merged and applied on `main`.
- **Next / In progress**: `la` (Serravalle Latin edition, 110 files), following the two-stage workflow
  in [`GUIDE.md`](GUIDE.md) Step 6. Trial completed (`006-epistola.md`, `008-inferno-canto-01.md`);
  the delegated draft of the other 108 files was not landed (see [`la` delegation
  result](#la-delegation-result)): the verse has gone through `commentary/en-la-la/`, now
  checked (2026-11-28), and the prose is to be delegated again in smaller units.

## Project-specific conventions

General workflow, cross-page joining, delegate task format, review checks, and misprint
handling follow [`GUIDE.md`](GUIDE.md). Project-specific decisions:

### Scope and files

- **Branches, now ended**: on `translations`, only `translations/` was touched (with the
  explicit exception of `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`); on
  `la` (from `main` at `8e162c88`, 2026-11-26, merged 2026-11-28), `commentary/` and
  `translations/`. The rest of `la` is done on `main`, with no branch (its verse goes
  through `commentary/en-la-la/` first). Everything to fix in `ocr/` or `texts/` is still
  recorded in [`for-main.tsv`](for-main.tsv) and applied together (step 4 below).
- **What is translated**: prefaces, essays, arguments, and notes (plus English prose and
  verse glosses for the English volumes, now complete), and translations of the Greek
  (`grc`) and Latin (`la`) verse translations (as reading aids to be paired alongside the
  Greek/Latin text, not to replace it). The Italian verse itself is not translated.
  As with `en*`, files under `translations/{en,ja}/{dir}/` hold target-language text only
  (no copied source text, to keep translation output compact); pairing with the
  English/Greek/Latin source text (including any adjustments for `en*`) is deferred until
  after `la` is done.
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
- **Numbers**: use Arabic numerals rather than kanji numerals (e.g., `# 第1歌`, `12音節`,
  `1881年10月`, `3頭の獣`, `第2の死`, `ボニファティウス8世`), except inside fixed kanji
  compounds, established terms, and idiomatic expressions (such as `一貫`, `万人`, `万物`,
  `第一質料`, `黄道十二宮`, `もう一つ`, `誰一人`, `一度も`).
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

## Settled conventions for `la` (Serravalle, 110 files)

- **Scope**: Translate all Latin front/back matter, *Summarium*, Latin tercet translations
  (as reading aids), Latin commentary, and all 1891 Italian editorial matter (`002`, `003`,
  end-of-canto essays, and `(1) ...` manuscript gloss lines under the tercets). **Skip
  Italian verse tercets only.**
- **Latin tercet format**: Preserve tercet number (`1 `, `2 `, …), `&emsp;` indentation on
  lines 2–3 (and line 4 where present), and trailing `\` line breaks 1-to-1 with the Latin
  source.
- **Lemmas (`*...*`) and incipit quotations**: Keep Italian lemmas and standalone Italian
  incipit lines verbatim in Italian; translate Latin lemmas and standalone Latin incipit
  lines into the target language (EN keeps `*...*`; JA renders translated lemmas in `「…」`).
- **Headings**: Keep `#` level (`# Infernus` → `# Inferno` / `# 地獄篇`,
  `# Capituli N Summarium` → `# Summary of Canto N` / `# 第N歌 要約`,
  `# Capitulum N` → `# Canto N` / `# 第N歌`, essay titles translated).
- **`pages.py` support**:
  - `prepare` / `finish` / `check` automatically skip leading verse blocks and `(1) ...`
    gloss lines when joining cross-page commentary paragraphs in `texts/la/`, and skip stray
    signature marks (`III`/`IV`/`V`/`2`/`3`, logged in [`for-main.tsv`](for-main.tsv)).
  - `check --skip-italian-tercets` skips Italian tercets (the first block of each numbered
    tercet pair) and verifies Latin tercets and all other verse blocks 1-to-1 (`V:N`).
  - All 7 doubtful boundaries and `110-index.md` p. 1236 (1290) are decided in
    [`joins.tsv`](joins.tsv).
- **Two-stage workflow** ([`GUIDE.md`](GUIDE.md) Step 6):
  1. Stage 1 (`translations/en/la/`): translate `la` into English, conforming proper names
     to `texts/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv` (and `texts/en/PROPER_NAMES.tsv`).
  2. Stage 2 (`translations/ja/la/`): translate directly from `texts/la/` into Japanese,
     using `translations/en/la/` as reference for cross-checking and refinement (not relay
     translation), conforming proper names to `translations/ja/en-{oelsner,purgatorio,paradiso}/PROPER_NAMES.tsv`
     and [`ja/en/PROPER_NAMES.md`](ja/en/PROPER_NAMES.md).
- **Trial completed**: `006-epistola.md` and `008-inferno-canto-01.md` landed in
  `translations/{en,ja}/la/` (`pages.py check --skip-italian-tercets` → `same structure`).
- **Delegation**: the remaining 108 files were delegated to Codex whole, one file per task
  (2026-11); see the result below.

### `la` delegation result

- **Structure**: all 216 outputs (`en`, `ja`) reported `same structure`, and the Japanese
  style audit found no polite forms or dashes.
- **Prose condensed**: compared block by block with the source (English/source length; the
  reviewed trial `008` has no block below 0.79), many commentary paragraphs and essays were
  summarized rather than translated, a source paragraph of 2,000 characters becoming one
  sentence. 14 files are condensed throughout (`036`, `043`, `045`, `056`, `062`, `066`,
  `076`, `078`, `082`, `084`, `086`, `091`, `094`, `109`), 10 in many paragraphs (`054`,
  `068`, `072`, `073`, `079`, `087`, `093`, `099`, `101`, `108`), 23 in one or two; the
  Japanese is shortened on its own in a few more. The delegate's notes admitted this for
  some files only. Paragraphs were also merged and a verse quotation duplicated to keep the
  block count (`097`), and blocks shifted (`039`).
- **Verse sound by tercet**: the 4,711 Latin tercets (14,233 lines) all have the source's
  line count, with English about as long as the Latin line for line; but words are moved
  between the lines of a tercet (often in Japanese), and in `039` the English tercet numbers
  skip 22 while the Japanese text is shifted.
- **Decision**: the verse is checked line by line in `commentary/en-la-la/` first (see
  [commentary/PLAN.md](../commentary/PLAN.md)), and the verse of `translations/en/la/` is
  taken from it as it is: the Latin tercets have no gloss markers (`(1)` stands in the
  Italian only, as in the trial `008`), so none are added. The prose (summaries, commentary,
  essays, front and back matter) is translated anew, and the delegate is shown the prose only,
  without the verse, so that verse and prose cannot be mixed up; the translated prose and the
  checked verse are then put together in the order of the source. It goes in smaller units
  (parts of a canto) with one added rule (no summarizing, condensing, or omitting), and each
  output passes length-ratio, duplicate-block, and lemma checks before review. The draft is
  kept until then as a reference for spotting omissions.
- **Prose parts**: [`scripts/la_prose.py`](scripts/la_prose.py) `split` gives the prose of a
  file as `pages.py prepare` does, with each run of tercet pairs replaced by a placeholder
  `<!-- verse N-M -->` (by which the verse is put back), cut into parts of about 10,000
  characters (the 108 files make 362 parts); `check` compares a translated part with its
  input (structure, then the paragraphs short for their source, repeated, or, in English,
  with fewer italic spans). The parts are delegated to agy, English first and then Japanese
  from the source, part by part. Still to be written: putting a file together from its parts
  and the verse of `commentary/en-la-la/`, without gloss markers, before
  `pages.py finish`.

## Remaining steps

1. `la` (Latin front/back matter, verse-translation reading aids, and commentary; 110 files):
   the verse from `commentary/en-la-la/` (now checked); the prose translated anew from the prose
   alone, in smaller units, checked, and put together with the verse; then `translations/en/la/` → `translations/ja/la/`. Unify on landing:
   三行連 (not 三行詩), half-width `(1)` markers, `# 煉獄篇` for *Purgatorium*, one rendering
   of *Preambula* (`007`, `042`) distinct from *Notizie Preliminari* (`003`).
2. `translations/README.md` (structure, excluded files, usage).
3. HTML side-by-side conversion pairing `texts/` and `translations/{en,ja}/`.
4. Resolve all `for-main.tsv` items (`ocr/` → reconvert `texts/`).

Commits when the user asks.
