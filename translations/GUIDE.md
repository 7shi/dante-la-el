# Guide: translating OCR-checked texts into Japanese

General lessons from translating Carlyle's *Inferno* (`en`) and the three Temple Classics
volumes (`en-oelsner`, `en-purgatorio`, `en-paradiso`) in `translations/ja/`, for reuse in
other projects. The project-specific rules and current state are in [PLAN.md](PLAN.md) and
[DONE.md](DONE.md); the steps below are the reusable standard workflow.

## Principles

- **Translate from converted section files (`texts/`), never from raw `ocr/`.** The input
  should already have paragraphs joined within pages, headings and footnotes marked,
  sections split into files, and OCR errors fixed, while keeping page markers
  (`<!-- p. N (NNN) -->`) that trace back to the page scans (`ocr/{dir}/NNN.png`).
- **Keep translations separate and structurally aligned.** A translation file holds the
  target language only—no copied source prose or untranslated verse—while keeping headings,
  page markers, footnote IDs, image paths, and paragraph order 1-to-1 with `texts/`. This
  allows a downstream HTML converter to pair source and translation side by side.
- **Let scripts handle structure and page joins; keep delegate prompts short.** A
  lightweight model drafts the translation from a short cold-start task file, while scripts
  handle cross-page paragraph joining, structural diffing (`scripts/pages.py`), and
  per-chapter proper-name filtering (`scripts/proper_names.py`).
- **Never edit `texts/` or `ocr/` on the translation branch.** Record suspected misprints
  and OCR leaks in tables (`misprints.tsv`, `for-main.tsv`) after checking the scan image;
  apply source fixes on `main` and bring them over cleanly.
- **Unify proper names across volumes with aligned TSV tables.** Maintain 1-to-1
  `texts/{dir}/PROPER_NAMES.tsv` ⇔ `translations/{lang}/{dir}/PROPER_NAMES.tsv` tables plus
  a shared conventions note (`PROPER_NAMES.md`), and audit all sections (not only the main
  text) once a volume or series is complete.

## Steps

The standard flow, in order:

| Step | What | Done by |
|---|---|---|
| 0 | Setup: branch, style rules, scripts (`pages.py`, `proper_names.py`), record TSVs | Coordinator |
| 1 | Trial on 2–3 representative files (preface + chapters) | Delegate + Coordinator |
| 2 | Prepare inputs (`pages.py prepare`), resolve `joins.tsv`, draft in batches (`{stem}.{md,tsv,txt}`) | Coordinator + Lightweight delegate |
| 3 | Batch review, verify misprints in scans, land with `pages.py finish` & `check` | Coordinator |
| 4 | Front/back matter, plates, and indexes (aligned with in-volume captions) | Coordinator |
| 5 | Cross-volume proper-name audit and aligned `PROPER_NAMES.tsv` generation | Coordinator |
| 6 | Non-English / classical editions (two-stage workflow: EN reference + direct JA) | Delegate + Coordinator |
| 7 | Close: update `DONE.md` & `PLAN.md`, clean `tmp/`, commit | Coordinator |

### 0. Setup: decided once, not changed mid-volume

- **Branch isolation**: work on a dedicated `translations` branch touching only
  `translations/` (and untracked `tmp/` for delegate I/O). Anything that belongs in `ocr/`
  or `texts/` goes into `translations/for-main.tsv`.
- **Style sheet** (in `PLAN.md`): fix once per volume or series:
  - Register and tense (e.g. plain written Japanese である調, past tense where the source
    is, literal translation with natural readability, no em-dashes `——`).
  - Speech registers (plain vs. polite form, pronouns such as `thou` → あなた, recurring
    forms of address).
  - Quotation marks (`「」`, nested `『』`, unclosed opening quote when a speech continues
    into the next paragraph) and footnote reference placement (immediately after the target
    word, before `。`, `、`, or `」`).
  - Citation and foreign-phrase policy: keep bibliographic references (`Canto xii. 37-41`,
    `Convito, Tr. iv. c. 23`, parenthetical author citations) as written; keep quoted
    Italian/Latin/Greek phrases as written with a gloss in `（）` if the source lacks one.
  - Edition-specific markup: marginal labels (`<!-- label: ... -->` translated inside the
    comment on translated paragraphs), editorial brackets (`[...]` stripped if purely
    textual markers), and trailing `\` line breaks preserved in maps, diagrams, and tables.
- **Tools**:
  - [`scripts/pages.py`](scripts/pages.py):
    - `prepare`: joins paragraphs split across page markers and reports doubtful places.
    - `check`: compares page markers, headings, footnote IDs, and paragraph counts/footnote
      references (ignoring untranslated verse).
    - `finish`: restores `<!-- first paragraph joined to p. X (NNN) -->` comments after
      page markers whose first paragraph was joined upward.
  - [`scripts/proper_names.py`](scripts/proper_names.py): filters `PROPER_NAMES.tsv` to the
    names occurring in a single chapter/canto for compact inclusion in delegate prompts.
- **Record TSVs**:
  - `joins.tsv` (`file`, `page`, `join`, `note`): explicit `yes` / `no` overrides for
    cross-page paragraph joins.
  - `ja/{dir}/misprints.tsv` (`file`, `page`, `text`, `reason`): verified misprints and
    author errors found during translation.
  - `for-main.tsv` (`file`, `page`, `part`, `text`, `change`): editable-text misprints and
    OCR/transcription errors to fix on `main`.

### 1. Trial on 2–3 representative files

- Run the full flow (`prepare` → delegate → `check` → review → `finish`) on one essay or
  preface and two chapters before scaling up.
- Note recurring delegate errors (dropped words, shifted clauses, wrong heading format,
  wrong speech register, misplaced quotation marks, translated citations) and add a short
  checklist for the batch review.
- Verify `pages.py` edge cases early (e.g. lone verse lines ending in a line number, prose
  blocks with `\` line breaks, or notes starting after a truncated reference).

### 2. Prepare inputs and cold-start task files

- Run `pages.py prepare texts/{dir}/{file} -o tmp/translate/{dir}/in/{file}` on all target
  files.
- Inspect every **doubtful** page boundary (and any suspicious auto-join, such as an index
  line ending in a page number before a colophon on the next page) against the scan image,
  and record `yes` or `no` in `joins.tsv`; re-run `prepare` so the input reflects the
  decision.
- Hand each chapter/canto over **whole in one pass** (argument, prose, glosses, notes, plus
  the untranslated original verse for reference only) so terminology agrees across sections.
- Generate self-contained cold-start task files (`tmp/translate/{dir}/task-{NNN}.md`) with:
  - the essential style rules only (no `pages.py` internals or git instructions);
  - the chapter's filtered proper-name list (`proper_names.py`);
  - three output paths in `tmp/translate/{dir}/out/`:
    1. `{stem}.md`: the translation;
    2. `{stem}.tsv`: suspected misprints (`page`, `text`, `reason`);
    3. `{stem}.txt`: unclear points and work notes.

### 3. Batch review and landing

- Review delegate outputs in batches (e.g. 10 files at a time), paragraph by paragraph
  against `tmp/translate/{dir}/in/{file}`:
  1. **Structure check**: run `pages.py check texts/{dir}/{file} tmp/translate/{dir}/out/{file}`.
     - Ordinary prose files must report `same structure`.
     - Files with `\`-broken map captions, diagrams, genealogical tables, or page-numbered
       index lines trigger expected `+V` in `pages.py check` (because `is_verse` treats
       short `\`-broken blocks and short number-ending lines as verse). On those files,
       verify 1-to-1 block alignment and check that no trailing `\` line breaks were lost.
  2. **Systematic scan for recurring delegate errors**:
     - Chapter heading format (e.g. `# 第一歌`–`# 第三十四歌`, not `# 歌二十` or `# 第23歌`).
     - Marginal labels (`<!-- label: ... -->`): count, placement, and consistent wording.
     - Speech register, forbidden pronouns/titles, and unclosed/extra `「」` or `」。`
       across multi-paragraph speeches.
     - Nested quotations rendered as `『...』`.
     - Cross-paragraph clause shifts or duplicated sentences across tercet boundaries.
     - Bibliographic citations in notes left untranslated (not katakana-ized), and author
       initials (`H. O.`, `P. H. W.`) kept as initials.
     - Editorial square brackets `[...]` removed where agreed.
  3. **Verify `{stem}.tsv` and `{stem}.txt` against scans (`ocr/{dir}/NNN.png`)**:
     - Confirmed editable-text misprint → translate by the intended reading, record in both
       `misprints.tsv` and `for-main.tsv`.
     - Misprint inside a scan image (e.g. map label) or author's factual error (wrong date)
       → record in `misprints.tsv` only (not `for-main.tsv`; author errors are translated
       as printed).
     - OCR/transcription leak not in the print (e.g. signature mark or stray page number)
       → record in `for-main.tsv` only.
  4. **Land**: run `pages.py finish texts/{dir}/{file} tmp/translate/{dir}/out/{file} -o translations/ja/{dir}/{file}`
     and re-run `pages.py check` on the landed file.

### 4. Front/back matter, plates, and indexes

- Translate title pages, colophons, and trailing plate/map/table indexes **after** the
  chapters are landed, so every index entry matches the settled in-volume map, diagram, and
  table captions word for word.
- Keep `![alt](images/NNN.jpg)` image paths identical to `texts/{dir}/` (translate only the
  alt text), and verify that the set of referenced images in `translations/ja/{dir}/`
  matches `texts/{dir}/` with zero missing or extra entries.

### 5. Cross-volume proper-name audit and aligned TSVs

- Once a volume (or series) is translated, extract proper-name occurrences from the aligned
  main-text blocks and generate 1-to-1 alphabetical tables:
  - `texts/{dir}/PROPER_NAMES.tsv` (`Name<TAB>canto:line,...`)
  - `translations/{lang}/{dir}/PROPER_NAMES.tsv` (`Name<TAB>Rendering1[<TAB>Rendering2...]`)
- Run an automated variant scan across **every section** (main text, marginal labels,
  arguments, notes, maps, genealogies, appendices) to catch inconsistencies that only
  appear in notes or tables.
- Decide contested forms once (e.g. modern Italian vs. Latin/Greek forms, origin-country
  rule for medieval figures), apply fixes globally across all volumes, and record the
  settled rules in `PROPER_NAMES.md`.

### 6. Non-English / classical source editions (two-stage workflow)

When translating editions in classical or non-English languages (such as Greek `grc` or
Latin `la` commentaries and arguments) alongside already-translated English editions:

1. **Stage 1 — English reference translation**: translate the source into English first,
   conforming all proper names to the English volumes' `PROPER_NAMES.tsv` tables.
2. **Stage 2 — Direct target-language translation refined with English**: translate
   directly from the original (`grc` / `la`) into Japanese, using the Stage 1 English
   translation as a cross-check and refinement reference rather than relay-translating from
   English.

### 7. Close

- Update `translations/DONE.md` (methods, counts, misprint/join summaries) and
  `translations/PLAN.md` (current state and remaining steps).
- Remove disposable working files in `tmp/` once everything is verified and committed.
- Commit logical milestones (per volume, cross-volume audit, indexes) cleanly on the
  `translations` branch; resolve `for-main.tsv` separately on `main`.

## What to avoid

- **Teaching delegates about cross-page joins or git.** Let `pages.py` join/restore page
  markers and keep delegates restricted to writing `{stem}.{md,tsv,txt}` in `tmp/`.
- **Splitting or merging paragraphs to make target prose flow better.** Keep 1-to-1
  paragraph alignment so side-by-side HTML pairing stays automatic and lossless.
- **Translating indexes before the body.** Translating them last guarantees caption
  agreement with zero rework.
- **Auditing proper names in the main text only.** Notes, maps, and genealogical tables
  consistently hide spelling variants missed by body-only scans.
- **Editing `texts/` on the translation branch.** It mixes concerns and creates merge
  conflicts when `main` reconverts `texts/` from `ocr/`.

## Decided in advance

- **Directory symmetry**: `texts/{dir}/{file}` ⇔ `translations/{lang}/{dir}/{file}`, and
  `texts/{dir}/PROPER_NAMES.tsv` ⇔ `translations/{lang}/{dir}/PROPER_NAMES.tsv`.
- **Three issue dispositions** during review:
  1. **Editable-text misprint**: translate intended reading, log in `misprints.tsv` +
     `for-main.tsv`.
  2. **Image-internal misprint / author error**: log in `misprints.tsv` only.
  3. **OCR / transcription error**: log in `for-main.tsv` only.
- **Structural verification**: `pages.py check` (`same structure`) for prose files; explicit
  1-to-1 block count + trailing `\` check for files containing maps, diagrams, tables, or
  page-numbered indexes.
