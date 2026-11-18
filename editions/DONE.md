# Done

The items of [PLAN.md](PLAN.md) that are done.

## After the rebase onto main (903e1f18)

The rebase added the leaf of Oelsner's Inferno with pp. 385–386 (canto XXXIV: the English of lines 19–51 and the Italian of lines 52–84), and corrected three misprints of Oelsner's Italian.

- `compare_editions.py en` was run again. The leaf brings three differences in words, 349–351 (XXXIV 39–51: "up to" / "at", "begins his valley" / "descends", ", whereby" / ". Thereby"), all `W`, as the two Italian texts agree there. The output was otherwise unchanged, so the numbers of `judge-en.txt` from 349 on were shifted by three (`F` 352:93, 353:93; `O` 357, 358).
- `en-carlyle-oelsner.md`: the three rows were added to the table of other changes, and the tables of every category were rendered again and found to match. The counts were updated: differences of punctuation 596 → 603, of case 374 → 377, in words 355 → 358 (marked 210 → 212, `W` 165 → 168), *;* → *:* 94 → 96, *:* → *;* 68 → 71.
- The handling of the missing page was dropped from `compare_editions.py` and `commentary/scripts/source.py`, with the output unchanged, and the notes on the missing leaf were removed from the reports.
- `compare_editions.py it` and the tables of `it-carlyle.md` were unchanged: the three misprints are on lines that are not in its tables.
