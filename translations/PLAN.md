# Plan: Japanese translations in `translations/ja/`

What the editions print around the poem (prefaces, essays, arguments, notes) is translated
into Japanese from the section files of [`texts/`](../texts/), into
`translations/ja/{dir}/`, where `{dir}` is the directory name of `ocr/` and `texts/`. The
work is done on the branch `translations`.

## State (2026-11-15)

Planned with the user; nothing translated and no script written yet. The work itself is done
in a new session, and this file is its handoff. The details not settled below are settled by
a trial ("Trial"), not beforehand.

## What is settled

- **On this branch only `translations/` is touched.** Everything of this work is there:
  the translations, the scripts (`translations/scripts/`), the records. Nothing outside it
  is changed on the branch, neither `ocr/` and `texts/` nor the files of the root (the
  README). What the work finds for them (a misprint, a line for the README) is recorded
  here and done on `main`, apart from this branch.
- **The source is `texts/`, not `ocr/`.** Its paragraphs are joined, its sections are files,
  its headings, arguments and footnotes are marked, its misprints are corrected, and the
  page markers `<!-- p. N (NNN) -->` still lead to `ocr/{dir}/NNN.png`. All six texts are
  checked ([ocr/PLAN.md](../ocr/PLAN.md)), so `texts/` changes from now on only by a
  misprint here and there; after a reconversion the diff of `texts/` shows which
  translations to look at.
- **The output** is `translations/ja/{dir}/`, one file per file of `texts/{dir}/` under the
  same name. A file with nothing to translate is not made; what is left out is listed in a
  README of `translations/` when there is something to list.
- **A file holds the Japanese only.** The headings, the page markers and the footnote IDs
  (`[^2-1]:`) are kept as in `texts/`; the original is not copied. The files are to be
  converted into HTML together with `texts/` (later, not part of this plan yet), which
  pairs them by the page markers, the headings, the footnote IDs and the order of the
  paragraphs within a page. A Markdown preview of a file alone may therefore look broken (a
  footnote without its reference); that is accepted.
- **What is translated**: the prefaces, essays, arguments and notes. The text of the poem
  and its translation (the English, Latin or Greek of the edition) is not translated now.
  For `en`, the aim is to read the English translation with Japanese help: if its text is
  translated later, the Japanese paragraphs go into the same file at the same place and are
  shown beside the English, not instead of it.
- **Figures** are not copied: a file refers to the images of `texts/{dir}/images/`.
- **The translator is a lightweight model**, as a delegate. Its rules stay basic, as for
  the read-through of `ocr/` (ocr/PLAN.md, "Read-through"); details are handled by scripts
  before and after, not by more rules.
- **The task of the delegate is a file in `tmp/`** at the root of the project: the prompt
  is written there, and the outside agent is told to read it and carry it out. `tmp/` is
  not tracked, so this is no change outside `translations/`; it is working space, and
  nothing that must last is kept there.
- **A suspected misprint is recorded, not corrected.** The delegate translates by the
  reading it judges right and writes a row of a TSV (page, the phrase as written, the
  reason), as the reader of the read-through did. It writes only the translation files and
  the TSV, never `texts/` or `ocr/` (seen by `git status`). The TSVs are kept in
  `translations/`. The places are looked into afterwards as in ocr/PLAN.md ("Decisions"):
  decided in the image, the decision a row of `ocr/{dir}/readcheck.tsv`, a misprint marked
  and listed in `misprints.tsv`, then the reconversion. The looking may be done here, since
  it changes nothing; the changes to `ocr/` and `texts/` are made on `main`, and reach this
  branch when the user brings them over. The record is a by-product, not a check: a model that translates smooths
  errors over without a word, and flags spellings of the edition; the settled readings of
  `ocr/{dir}/PLAN.md` answer the latter.
- **A paragraph that runs over a page** is split at the page marker in `texts/`
  (texts/PLAN.md, "Prose"); Japanese cannot be split there. It is translated whole and
  stands on the page where it begins; the marker of the next page follows it, with a
  comment on its own line (the wording to be fixed in the trial):

  ```markdown
  …the whole paragraph that begins on p. v.

  <!-- p. vi (012) -->
  <!-- first paragraph joined to p. v (011) -->

  The first paragraph that begins on p. vi.
  ```

  The delegate is not told of this. A script joins such paragraphs in the input it is
  given, and the same script, which knows what it joined, puts the markers and the comments
  back into what it returns. Footnotes split across pages are already joined in `texts/`.

## Not settled

- **Which paragraphs run over a page**: `texts/` does not mark them. To be judged from the
  text (the last paragraph of a page not ending in a sentence's punctuation, the next page
  beginning in lower case) and listed for review on the first text.
- **The input given to the delegate** for a canto file: the whole file, or only the parts
  to translate (argument, notes) with the rest taken out by the script.
- **Style**: plain or polite Japanese; proper names; the quotations in the notes (Italian,
  Latin, Greek) and the words in italics.
- **The delegate and its model** (the user sets them), the size of a batch, and the
  place and the names of the TSVs of suspected misprints inside `translations/`.
- **The scope beyond `en`**: the notes of the three Temple Classics volumes, which repeat
  much of Carlyle's; the commentary of `la`, which is most of that book (about 1300 scans);
  the Greek prologue, arguments and notes of `grc`; the indexes.
- **The order of the texts** after `en`.

## Trial

On `en`, the smallest text in one language, two files:

- [`texts/en/002-preface-first-edition.md`](../texts/en/002-preface-first-edition.md):
  prose over eight pages, with paragraphs running over the pages;
- [`texts/en/007-canto-01.md`](../texts/en/007-canto-01.md): an argument and footnotes,
  with the text of the poem left out.

It is to show:

1. the input: the joining of the paragraphs, and what of a canto file is handed over;
2. whether the delegate returns the headings, page markers and footnote IDs unchanged,
   checked by a script (the same numbers and order as in `texts/`, a page that begins with
   a continuation one paragraph short);
3. the quality and the style of the Japanese, and with them the few rules worth giving;
4. the record of suspected misprints: what it misses and what it flags falsely.

## Steps

1. The script that writes the delegate's input and takes its output back (joins, markers,
   comments), and the check of the structure against `texts/`, in `translations/scripts/`.
2. The trial; the points of "Not settled" decided with the user and written here.
3. `en` in batches; the suspected misprints looked into after each batch or at the end, as
   the user decides, and corrected on `main`.
4. The other texts, in the order and scope then decided.
5. A README of `translations/`, and the conversion into HTML.

Commits when the user asks.
