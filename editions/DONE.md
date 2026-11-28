# Done

The items of [PLAN.md](PLAN.md) that are done.

## After the rebase onto main (903e1f18)

The rebase added the leaf of Oelsner's Inferno with pp. 385–386 (canto XXXIV: the English of lines 19–51 and the Italian of lines 52–84), and corrected three misprints of Oelsner's Italian.

- `compare_editions.py en` was run again. The leaf brings three differences in words, 349–351 (XXXIV 39–51: "up to" / "at", "begins his valley" / "descends", ", whereby" / ". Thereby"), all `W`, as the two Italian texts agree there. The output was otherwise unchanged, so the numbers of `judge-en.txt` from 349 on were shifted by three (`F` 352:93, 353:93; `O` 357, 358).
- `en-carlyle-oelsner.md`: the three rows were added to the table of other changes, and the tables of every category were rendered again and found to match. The counts were updated: differences of punctuation 596 → 603, of case 374 → 377, in words 355 → 358 (marked 210 → 212, `W` 165 → 168), *;* → *:* 94 → 96, *:* → *;* 68 → 71.
- The handling of the missing page was dropped from `compare_editions.py` and `commentary/scripts/source.py`, with the output unchanged, and the notes on the missing leaf were removed from the reports.
- `compare_editions.py it` and the tables of `it-carlyle.md` were unchanged: the three misprints are on lines that are not in its tables.

## After the merge into main (c3119649)

`el` was merged into `main`, and the `translations/for-main.tsv` fixes in `texts/en/` (`c3119649`: three missing quotation marks in Carlyle's English, plus footnote and Argument fixes) were checked (`8498fc85`):

- `uv run scripts/align_carlyle.py check` passed (`377 blocks`).
- `uv run scripts/compare_editions.py en` was run again: `punctuation only` changed from `603` to `602`; all other counts and word differences were unchanged.
- `en-carlyle-oelsner.md` was updated (`603` → `602`).
- `uv run scripts/compare_editions.py it` was unchanged.

## After the merge into main (71c2b827)

`commentary` was merged into `main` (`b565e9da`), and the `translations/for-main.tsv` fixes in `texts/en-oelsner/` (`71c2b827`: a missing quotation mark in canto VII's English, a missing quotation mark in canto IX line 131's Italian, and an Argument name fix in canto XXII) were checked:

- `uv run scripts/compare_editions.py en` was run again: all counts (`punctuation 602`, `case 377`, `words 358`, `marked 212`) and tables in `en-carlyle-oelsner.md` were unchanged.
- `uv run scripts/compare_editions.py it` was unchanged (`160 / 1874 / 2367 / 194 / 125`), and the affected lines are not in the tables of `it-carlyle.md`.

## Unmarked changes checked against the page images

The twelve unmarked changes of a single word listed at the end of [en-carlyle-oelsner.md](en-carlyle-oelsner.md) were checked against the page images of both books (2026-11-28; `ocr/en/` 066, 073, 129, 130, 192, 245, 257, 307, 377, 434, 443, 449; `ocr/en-oelsner/` 023, 031, 087, 089, 141, 187, 201, 245, 313, 365, 373, 377). Every one is printed as transcribed, so none is an error of transcription, and `ocr/` and the comparison are unchanged. Two take up Carlyle's own footnotes (XII *wild*, XXI *nick it for him*); the section of the report was renamed and says so.
