# Plan: Japanese translations in `translations/ja/`

What the editions print around the poem (prefaces, essays, arguments, notes), and for `en`
the English prose translation of the poem, is translated into Japanese from the section
files of [`texts/`](../texts/), into `translations/ja/{dir}/`, where `{dir}` is the
directory name of `ocr/` and `texts/`. The work is done on the branch `translations`.

## State (2026-11-15)

The trial is done ("Trial"): the flow below is tried on three files of `en`
(`002-preface-first-edition.md`, `007-canto-01.md`, `008-canto-02.md`), which are in
`ja/en/`. The prefaces and essays of `en` (`003`–`006`) followed, by the same flow. Next:
the cantos from III (`009`). The delegate is gpt-6-luna (Codex).

## What is settled

### Scope and output

- **On this branch only `translations/` is touched.** Everything of this work is there:
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
- **What is translated**: the prefaces, essays, arguments and notes; for `en` also the
  English prose translation of the poem, translated from the English (not from the
  Italian), to read the English with Japanese help, and the glosses under the verse
  (`1\. Bruno, brown, dark, obscure.`, 97 in `en`). The text of the poem (the Italian) and
  the verse translations of `la` and `grc` are not translated now.
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
  (`. ! ? : ; ” ’ ) —`; `xii (018)` of the preface goes on with "Original"). The last
  prose of a page is looked for before its verse, glosses and footnotes; a footnote
  reference at its end is ignored. In the cantos a page often ends in a weak stop (`;`,
  `:`, `,`, an abbreviation such as `MSS.`) and the next begins in lower case. A weak stop
  followed by upper case is listed as doubtful, not joined (five in `en`: pp. 40, 45, 54,
  153, 268), to be decided in the image when their cantos are done.

### The delegate and the flow

- **The translator is a lightweight model**, as a delegate. Its rules stay basic, as for
  the read-through of `ocr/` (ocr/PLAN.md, "Read-through"); details are handled by scripts
  before and after, and by the review here, not by more rules.
- **A batch is one file.** The flow, with [`scripts/pages.py`](scripts/pages.py)
  (`uv run python translations/scripts/pages.py …`):
  1. `prepare texts/{dir}/{file} -o tmp/translate/in/{file}` writes the input with the
     paragraphs joined, and lists the joins and the doubtful places.
  2. The task is written to `tmp/translate/task-{NNN}.md`, after the last one (the rules
     of "Style"), and the delegate is told to read it and carry it out. It writes
     `tmp/translate/out/{file}` and a TSV of suspected misprints beside it, and nothing
     else (seen by `git status`). `tmp/` is not tracked; it is working space, and nothing
     that must last is kept there.
  3. `check texts/{dir}/{file} tmp/translate/out/{file}` compares the structure with the
     input (markers, headings, footnote IDs, paragraphs with their footnote references;
     the verse left out). Footnote references in another order within a paragraph, as
     Japanese word order may need, are reported apart, not as a difference.
  4. The translation is read against the English, paragraph by paragraph, and corrected
     here, not sent back; the corrected copy is `tmp/translate/fixed-{NNN}.md`.
  5. `finish texts/{dir}/{file} tmp/translate/fixed-{NNN}.md -o translations/ja/{dir}/{file}`
     adds the comments of the joins; `check` is run on the result once more.
- **A canto file is handed over whole** and translated in one pass: the Argument, the
  English prose, the glosses, the footnotes, and the Italian verse for reference only (not
  translated, left out of the output), so that the notes and the Italian help the reading
  of the prose, and the words agree between prose and notes. No Argument runs over a page
  in `en`.

### Style

- Plain written Japanese (である調), nothing added or left out. The prose of the poem
  word for word as far as natural Japanese allows, following the English where it differs
  from the Italian; in the past tense where the English is; the narrator is 私.
- **Speech** is in plain form (常体) for every speaker; `thou` is あなた, `ye`/`you`
  あなたがた, as the English uses `thou` to everyone. Quotation marks as 「」, a quotation
  within one as 『』.
- Proper names of persons and places in katakana; titles of works in 『』.
- Quotations in English are translated; words and quotations in Italian, Latin or Greek
  are kept as written, with a Japanese gloss in （） where the text does not give one;
  references (`Psalm xc. 10`, `Convito, Tr. iv. c. 23`) are kept as written.
- Glosses keep the line number and the Italian word: `12\. Alto：高い、深い、あるいは困難な。`

### Misprints

- **A suspected misprint is recorded, not corrected.** The delegate translates by the
  reading it judges right and writes a row of its TSV (page, the phrase as written, the
  reason). The rows, and what the review here finds, go into `ja/{dir}/misprints.tsv`
  (columns `file`, `page`, `text`, `reason`). The places are looked into as in
  ocr/PLAN.md ("Decisions"): decided in the image, the decision a row of
  `ocr/{dir}/readcheck.tsv`, a misprint marked and listed in `misprints.tsv`, then the
  reconversion. The looking may be done here, since it changes nothing; the changes to
  `ocr/` and `texts/` are made on `main`, and reach this branch when the user brings them
  over. The record is a by-product, not a check: in the trial the delegate recorded
  nothing, and smoothed over what it met (see "Trial").
- **An error of the author** (a wrong date) is not a misprint: it is translated as printed, and recorded in the same
  TSV with that reason.

## Not settled

- **Style, the rest**: the words in italics (other texts).
- **The scope beyond `en`**: the notes of the three Temple Classics volumes, which repeat
  much of Carlyle's; the commentary of `la`, which is most of that book (about 1300 scans);
  the Greek prologue, arguments and notes of `grc`; the indexes.
- **The order of the texts** after `en`.

## Trial

Three files of `en`, all returned with the structure unchanged and the TSVs of misprints
empty. The Japanese reads well and follows the English closely; the review here found a
few errors in each file, of the same kinds throughout: a word or a clause left out ("See"
of a reference, "our own", "all", "good"), something added (古形 in a gloss, あなたが直面し),
a sense shifted ("deserted" as 荒れ果てた, "though it was late" as 遅すぎた, "So Milton"
as "therefore"), and once a closing quotation mark misplaced, which gave Beatrice's words
to Lucia. These are what the review looks for.

- `002-preface-first-edition.md`: seven joins, one paragraph over pp. viii–x. One
  mistranslation ("saying, Peace, peace; when there is no peace?") and one shifted
  sentence ("All anger and indignation…") corrected.
- `007-canto-01.md`, in two passes: first the Argument and the 24 footnotes, with the
  prose and the verse taken out (five places corrected); then the prose, with the
  Japanese of the notes given to copy, which came back identical. One paragraph was split
  in two (p. 5), joined here. The delegate split a verse quotation into its lines, as
  printed, without recording that the transcription has it on one line (`for-main.tsv`).
- `008-canto-02.md`, in one pass (the flow above): Argument, prose, 9 glosses and 21
  footnotes. Eight places corrected. The speech came back in mixed registers (です in one
  speech, あなた and お前 in another), which led to the rule of plain speech; Cantos I
  and II were brought in line with it. Two misprints were found in the review, not by the
  delegate (`ja/en/misprints.tsv`).

The prefaces and essays (`003`–`006`) came back with the structure unchanged, but for
three references of `004` set apart from the verse they belong to (removed here). The
review found errors of the same kinds as in the trial, and two more: Italian and Latin
put into katakana or translated where they are kept as written (titles such as *Ottimo
Comento*, *Libri titulus est*), and references turned into Japanese (`Inf. x. 85` as
『地獄篇』x. 85). The names of editions are kept the same across the essays (ニドベアティーナ版,
コミーノ版, ジュンタ版). The delegate recorded two suspected misprints, neither a misprint;
one was an error of the author, which it had corrected in the translation.

## For `main`

Found by this work, to be done on `main` (not on this branch):

- [`for-main.tsv`](for-main.tsv) (columns `file`, `page`, `part`, `text`, `change`;
  `part` is `poem` for the text of the poem and its translations, which other branches
  use, or `notes` for the rest: notes, glosses, arguments, prefaces, essays): everything
  to be done or decided on `main`, one row each: an error of the transcription, and each
  misprint of `ja/{dir}/misprints.tsv` (to be marked as such or left as printed; see
  "Misprints"). A row is removed when the change has come over from `main`, or the
  decision is made. A row of `misprints.tsv` whose reason says it is not a misprint (an
  error of the author, translated as printed) needs nothing on `main` and has no row here.

## Steps

1. Done: `pages.py` (prepare, check, finish).
2. Done: the trial; the points decided are written above.
3. `en`, one file at a time, the prefaces and essays first; the suspected misprints looked
   into after each file or at the end, as the user decides, and corrected on `main`.
4. The other texts, in the order and scope then decided.
5. A README of `translations/`, and the conversion into HTML.

Commits when the user asks.
