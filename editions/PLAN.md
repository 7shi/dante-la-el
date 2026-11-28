# Plan

What remains to be done on the reports of this directory; what is done is in [DONE.md](DONE.md).

## If texts/en/ or texts/en-oelsner/ change

The `el`, `commentary`, and `la` branches have been merged into `main` (see [DONE.md](DONE.md)), and work now continues on `main`, with no branch. If `texts/en/` or `texts/en-oelsner/` change further, check them again:

- Run `uv run scripts/compare_editions.py en` again and check the numbers of `judge-en.txt` against the new list (see [README.md](README.md#how-they-are-made)); judge any new difference.
- Render the tables of `en-carlyle-oelsner.md` again with `scripts/render_editions.py`, and update its counts.
- If `texts/en/` changes, run `compare_editions.py it` too and check `it-carlyle.md`; if the English of `texts/en/` changes, `uv run scripts/align_carlyle.py check` checks that every cut of `en-blocks.txt` is still found.

## After the merge into main

- Update the root README for this directory.
- Check against the page images the twelve unmarked one-word changes listed at the end of [en-carlyle-oelsner.md](en-carlyle-oelsner.md); corrections go into `ocr/en/` or `ocr/en-oelsner/`, and the comparison is then run again as above.
