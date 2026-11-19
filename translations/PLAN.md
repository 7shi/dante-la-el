# Plan: Japanese translations in `translations/ja/`

What the editions print around the poem (prefaces, essays, arguments, notes), and for the
English editions the English prose translation of the poem, is translated into Japanese
from the section files of [`texts/`](../texts/), into `translations/ja/{dir}/`, where
`{dir}` is the directory name of `ocr/` and `texts/`. The work is done on the branch
`translations`. Completed work is recorded in [`DONE.md`](DONE.md).

## State (2026-11-19)

- **Done** ([`DONE.md`](DONE.md)):
  - `ja/en/` (`001`–`041`, Carlyle's *Inferno*): all 41 files translated, checked, and committed; `for-main.tsv` items resolved.
  - `ja/en-oelsner/` (`001`–`040`, Temple Classics *Inferno*): title page, Cantos I–XXXIV, and end matter translated, reviewed, checked, and committed (with 5 misprints in `ja/en-oelsner/misprints.tsv` and 3 text items in `for-main.tsv`; `041` index pending).
  - `ja/en-purgatorio/` (`001`–`039`, Temple Classics *Purgatorio*): title page, Cantos I–XXXIII, and end matter translated, reviewed, checked, and committed (with 10 misprints/author errors in `ja/en-purgatorio/misprints.tsv`, 7 items in `for-main.tsv`, and 1 entry in `joins.tsv`; `040` index pending).
  - `ja/en-paradiso/` (`001`–`038`, Temple Classics *Paradiso*): title page, Cantos I–XXXIII, and end matter translated, reviewed, checked, and committed (with 6 misprints in `ja/en-paradiso/misprints.tsv` and 9 items in `for-main.tsv`; `039` index pending).
  - Proper-name audit & tables: generated `texts/en-{purgatorio,paradiso}/PROPER_NAMES.tsv` and `ja/en-{purgatorio,paradiso}/PROPER_NAMES.tsv` (363 / 379 poem-body entries), unified transliterations across all sections of all four English volumes, and updated `ja/PROPER_NAMES.{md,tsv}` (`de2c9aea`).
- **Next**:
  - Translate the plate/map/table index files (`en-oelsner/041`, `en-purgatorio/040`, `en-paradiso/039`).

## What is settled

### Scope and output

- **On this branch only `translations/` is touched** (with the explicit exception of the newly added `texts/en-{purgatorio,paradiso}/PROPER_NAMES.tsv` index tables). Everything of this work is there:
  the translations, the scripts (`translations/scripts/`), the records. Nothing outside it
  is changed on the branch, neither `ocr/` and `texts/` nor the files of the root (the
  README). What the work finds for them (a misprint, a line for the README) is recorded
  under "For `main`" and done on `main`, apart from this branch.
- **The source is `texts/`, not `ocr/`.** Its paragraphs are joined, its sections are files,
  its headings, arguments and footnotes are marked, its misprints are corrected, and the
  page markers `<!-- p. N (NNN) -->` still lead to `ocr/{dir}/NNN.png`. All six texts are
  checked ([ocr/PLAN.md](../ocr/PLAN.md)), so `texts/` changes from now on only by a
  misprint here and there; after a reconversion the diff of `texts/` shows which
  translations to look at.
- **What is translated**: the prefaces, essays, arguments and notes; for the English
  editions also the English prose translation of the poem, translated from the English (not
  from the Italian), to read the English with Japanese help, and the glosses under the
  verse (`1\. Bruno, brown, dark, obscure.`, 97 in `en`). The text of the poem (the
  Italian) and the verse translations of `la` and `grc` are not translated now.
- **The output** is `translations/ja/{dir}/`, one file per file of `texts/{dir}/` under the
  same name. A file with nothing to translate is not made; what is left out is listed in a
  README of `translations/` when there is something to list.
- **A file holds the Japanese only.** The headings, the page markers and the footnote IDs
  (`[^2-1]:`) are kept as in `texts/`; the footnote references (`[^2-1]`) stay in the
  Japanese paragraph, after the word they belong to. The original is not copied, nor the
  Italian verse. The files are to be converted into HTML together with `texts/` (later,
  not part of this plan yet), which pairs them by the page markers, the headings, the
  footnote IDs and the order of the paragraphs within a page, and shows the Japanese
  beside the English, not instead of it. A Markdown preview of a file alone may look
  broken (a footnote without its reference); that is accepted.
- **Figures** are not copied: a file refers to the images of `texts/{dir}/images/`.

### Paragraphs over a page

- **A paragraph that runs over a page** is split at the page marker in `texts/`
  (texts/PLAN.md, "Prose"); Japanese cannot be split there. It is translated whole and
  stands on the page where it begins; the marker of the next page stays where it is in
  `texts/`, with a comment on its own line after it:

  ```markdown
  …the whole paragraph that begins on p. v.

  <!-- p. vi (012) -->
  <!-- first paragraph joined to p. v (011) -->

  The first paragraph that begins on p. vi.
  ```

  A paragraph over several pages is followed by all their markers, each comment naming the
  page where it begins. The delegate is not told of this: `pages.py` joins the paragraphs
  in its input and adds the comments to its output. Footnotes split across pages are
  already joined in `texts/`.
- **A paragraph runs over a page** when prose follows the page marker and either it begins
  in lower case or the last prose of the page before does not end in punctuation
  (`. ! ? : ; ” ’ ) —`). The last prose of a page is looked for before its verse, glosses
  and footnotes; a footnote reference at its end is ignored. In the cantos a page often
  ends in a weak stop (`;`, `:`, `,`, an abbreviation such as `MSS.`) and the next begins
  in lower case. A weak stop followed by upper case is listed as doubtful, not joined;
  decided places are recorded in [`joins.tsv`](joins.tsv) (`file` as `{dir}/{file}`,
  `page`, `join` yes or no, `note`).
- **Verse vs. prose in `pages.py`**: `is_verse` treats a one-line verse block ending in
  its line number as verse (`LONE_VERSE`), and treats a block with `\` line breaks whose
  lines exceed 100 chars as prose. Because translated map captions, genealogical tables,
  and classification tables with trailing `\` often have short lines (`<= 100` chars),
  `pages.py check` reports `+V` on those blocks; verify that all `\` line breaks are kept.

### The delegate and the flow

- **The translator is a lightweight model**, as a delegate. Its rules stay basic, as for
  the read-through of `ocr/` (ocr/PLAN.md, "Read-through"); details are handled by scripts
  before and after, and by the review here, not by more rules.
- **Workflow with [`scripts/pages.py`](scripts/pages.py)**
  (`uv run python translations/scripts/pages.py …`, or `python3 translations/scripts/pages.py …`
  when `uv run` cannot see `../dante-corpus` in a sandbox):
  1. `prepare texts/{dir}/{file} -o tmp/translate/{dir}/in/{file}` writes the input with the
     paragraphs joined, and lists the joins and the doubtful places.
  2. Cold-start task prompts are written to `tmp/translate/{dir}/task-{NNN}.md` (following
     the rules of "Style"). The delegate writes `{stem}.md` (translation), `{stem}.tsv`
     (suspected misprints), and `{stem}.txt` (unclear points and work notes) to
     `tmp/translate/{dir}/out/`. `tmp/` is untracked working space.
  3. `check texts/{dir}/{file} tmp/translate/{dir}/out/{file}` compares the structure with the
     input (markers, headings, footnote IDs, paragraphs with their footnote references;
     the verse left out). Footnote references in another order within a paragraph, as
     Japanese word order may need, are reported apart, not as a difference.
  4. The translation is reviewed in batches against the English, paragraph by paragraph,
     and corrected in `tmp/translate/{dir}/out/{file}` before running `finish`.
     Common delegate errors to check:
     - Canto headings not in `# 第一歌`–`# 第三十四歌` format (`# 歌二十`, `# 第23歌`).
     - Dropped, shifted, or inconsistently translated marginal labels (`<!-- label: ... -->`).
     - `お前` / `おまえ`, `先生`, or polite forms (`です/ます/なさい/ください/でしょう`) in plain-form dialogue.
     - `」。` (period outside closing quote), unclosed or prematurely closed `」` across multi-paragraph speeches, or single quotes not rendered as `『...』`.
     - Cross-paragraph clause shifts or duplicated sentences across tercet boundaries.
     - Translated or katakana-ized citation references in `## Notes`, or missing trailing `\` in tables and diagrams.
  5. `finish texts/{dir}/{file} tmp/translate/{dir}/out/{file} -o translations/ja/{dir}/{file}`
     adds the comments of the joins; `check` is run on the result once more.
- **A canto file is handed over whole** and translated in one pass: the Argument, the
  English prose, the glosses/notes, and the Italian verse for reference only (not
  translated, left out of the output), so that the notes and the Italian help the reading
  of the prose, and the words agree between prose and notes.

### Style

- Plain written Japanese (である調), nothing added or left out. Keep literal translation
  as the principle while attending to readability (avoid Japanese em-dashes `——`), and
  do not restructure sentences or clause order unless specifically instructed. The prose
  of the poem word for word as far as natural Japanese allows, following the English
  where it differs from the Italian; in the past tense where the English is; the narrator
  is 私.
- **Speech**:
  - In `en`: plain form (常体), except Dante’s speeches to Virgil, which are in polite form (敬語 / です・ます調).
  - In the Temple Classics volumes (`en-oelsner`, `en-purgatorio`, `en-paradiso`): plain form (常体) for every speaker, as specified in their task prompts.
  - `thou` is あなた (never お前), `ye`/`you` plural is あなたがた. A `you` of respect to one person (Italian `voi`, as to Brunetto Latini) is あなた too.
- **Virgil and titles**: Virgil addressed as `"Master"` in speech is 師よ (`"My Master"`
  is 我が師よ; never 先生); `"Master"` in narration is 師 (`"my Master"` / `"My Master"`
  is 我が師); `"Guide"` is 導き手; `"Escort"` is 案内人; `"Leader"` is 先導者.
- **Quotation marks and footnotes**: Quotation marks as 「」, a quotation within one as
  『』; a speech continuing into the next paragraph (no closing `”` in English) has no
  closing 」 at the end of the paragraph. Footnote references (`[^N-M]`) stand immediately
  after the word they belong to, before `。`, `、`, and `」`.
- **Proper names and terms**: Proper names of persons and places in katakana (per-text
  decisions in `ja/PROPER_NAMES.md` and `ja/PROPER_NAMES.tsv`; filtered per canto with
  `scripts/proper_names.py`); titles of works in 『』 (e.g. *Comedy* = 『喜劇』).
- **Quotations and references**: Quotations in English are translated; words and quotations
  in Italian, Latin or Greek are kept as written, with a Japanese gloss in （） where the
  text does not give one; references (`Psalm xc. 10`, `Convito, Tr. iv. c. 23`, `verse 94`,
  `v. 42`, `Canto xii. 37-41`) and commentator/author names cited in parenthetical
  references (`Benv. da Imola`, `Ottimo Com.`, `Landino`, `Ovid, *Metam*.`) are kept as
  written (as sentence subjects, use katakana such as オッティモ注釈, ベンヴェヌート・ダ・イーモラ,
  オウィディウス). `Lit.:` is 直訳では; `"See X"` is `X を参照`; `"Compare X"` is `X と比較せよ`.
- **Temple Classics conventions** (`en-oelsner`, `en-purgatorio`, `en-paradiso`):
  - Marginal labels (`<!-- label: ... -->`) on translated English paragraphs are translated
    inside the comment, while Italian verse labels stay as-is.
  - Editorial revision square brackets `[...]` are omitted, treating their contents as
    plain prose.
  - Multiline map captions, diagrams, and genealogical/chronological tables preserve trailing
    `\` line breaks on every line.

### Misprints

- **A suspected misprint is recorded, not corrected.** The delegate translates by the
  reading it judges right and writes a row of its TSV (page, the phrase as written, the
  reason). The rows, and what the review here finds, go into `ja/{dir}/misprints.tsv`
  (columns `file`, `page`, `text`, `reason`). The places are looked into as in
  ocr/PLAN.md ("Decisions"): decided in the image, the decision a row of
  `ocr/{dir}/readcheck.tsv`, a misprint marked and listed in `misprints.tsv`, then the
  reconversion. The looking may be done here, since it changes nothing; the changes to
  `ocr/` and `texts/` are made on `main`, and reach this branch when the user brings them
  over.
- **An error of the author** (a wrong date) is not a misprint: it is translated as printed,
  and recorded in the same TSV with that reason.

## For `main`

Found by this work, to be done on `main` (not on this branch):

- [`for-main.tsv`](for-main.tsv) (columns `file`, `page`, `part`, `text`, `change`;
  `part` is `poem` for the text of the poem and its translations, which other branches
  use, or `notes` for the rest: notes, glosses, arguments, prefaces, essays): everything
  to be done or decided on `main`, one row each: an error of the transcription, and each
  editable-text misprint of `ja/{dir}/misprints.tsv` (to be marked as such or left as
  printed; see "Misprints"). A row is removed when the change has come over from `main`,
  or the decision is made. Misprints inside scan images (such as map labels in
  `images/NNN.jpg`) or author errors translated as printed have no row in `for-main.tsv`.

## Not settled

- **Plate/map/table indexes**: `en-oelsner/041-index-to-maps-plates-and-tables.md`,
  `en-purgatorio/040-index-to-plates-tables-etc.md`, and
  `en-paradiso/039-index-to-maps-diagrams-and-tables.md`.
- **Beyond the English editions**: the commentary of `la` (about 1300 scans), the Greek
  prologue, arguments and notes of `grc`, and how words in italics are handled there.

## Remaining steps

1. Translate the plate/map/table index files (`en-oelsner/041`, `en-purgatorio/040`,
   `en-paradiso/039`).
2. `la` and `grc`.
3. A README of `translations/`, and the conversion into HTML.

Commits when the user asks.
