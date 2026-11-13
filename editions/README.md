# editions

Reports on the texts behind the `carlyle` source of [grammar.py](../grammar/README.md#scriptsgrammarpy): the Italian printed in John A. Carlyle's Inferno (fifth edition, 1889; [`texts/en/`](../texts/en/)), the Italian of [dante-corpus](https://github.com/7shi/dante-corpus), and Oelsner's edition of the Temple Classics (1903; [`texts/en-oelsner/`](../texts/en-oelsner/)), with its own Italian text and its revision of Carlyle's English.

## Reports

| File | Compares |
|---|---|
| [it-carlyle.md](it-carlyle.md) | the Italian of dante-corpus and of Carlyle's edition, line by line, with Oelsner's Italian beside them |
| [en-carlyle-oelsner.md](en-carlyle-oelsner.md) | Carlyle's English and Oelsner's revision of it, word by word over each canto |

Neither lists every difference. The differences of spelling, punctuation, and the forms of words are described by their features with examples; the differences of words are listed in full.

## How they are made

1. [`scripts/compare_editions.py`](scripts/compare_editions.py) collects the differences and sorts out what can be told mechanically (orthography, forms of the same word, punctuation, case), and lists the rest:

   ```bash
   uv run scripts/compare_editions.py it -o it.txt
   uv run scripts/compare_editions.py en -o en.txt
   ```

2. The listed differences in words were read and sorted into categories by hand. The judgments are kept here:

   | File | Items | Categories |
   |---|---|---|
   | [judge-it.txt](judge-it.txt) | lines, as `canto:line` | `content`, `function`, `order`, `inflection` |
   | [judge-en.txt](judge-en.txt) | differences, by their number in the output of `compare_editions.py en` (from 1); for `F`, `number:line` gives the Italian line the revision follows | `F` (follows Oelsner's Italian), `W` (other change of words, also every difference not listed), `O` (word order), `N` (proper name), `M` (ending), `A` (article or conjunction), `S` (spelling) |

   The numbers of `judge-en.txt` hold only as long as the texts and the script give the same list: after a change to `texts/en/`, `texts/en-oelsner/`, or the comparison, the judgments have to be checked against the new list.

3. [`scripts/render_editions.py`](scripts/render_editions.py) renders the tables of the reports from the judgments (run from this directory):

   ```bash
   uv run scripts/render_editions.py it judge-it.txt content      # function, order, inflection
   uv run scripts/render_editions.py en judge-en.txt F --italian  # W, O, N, M, A
   ```

   The tables are pasted into the reports; the rest of the reports (the counts, the descriptions and examples of the features, the table of spellings in `en-carlyle-oelsner.md`, and the list of changes to check against the page images) is written by hand.

## Notes

- Carlyle's edition prints the English prose page by page above the Italian verse it renders; Oelsner's prints the English one paragraph per tercet facing the Italian, though a paragraph may render two tercets (XXVI 25–30). So the English is compared over the whole canto, and each difference is located by the page of Carlyle's edition where it falls.
- The scan of Oelsner's edition lacks the leaf with pp. 385–386 (canto XXXIV: the English of lines 19–51 and the Italian of lines 52–84); these are left out.
- The unmarked changes of a single word listed at the end of `en-carlyle-oelsner.md` may be errors of transcription and are to be checked against the page images; corrections belong in `ocr/en/` or `ocr/en-oelsner/`, not here.

## scripts/compare_editions.py

```bash
uv run scripts/compare_editions.py it [-o OUT]
uv run scripts/compare_editions.py en [-o OUT]
```

Collects the differences between the editions of the Inferno, as material for the reports in this directory. The model is not called; the output (to standard output, or to `-o`) is read by hand, and the reports describe the differences by their features and list in full only the changes of words.

- `it` compares the Italian of dante-corpus with the Italian of Carlyle's edition line by line, with Oelsner's Italian beside them. Each line is sorted by its first kind of difference: identical; orthography only (the same letters once accents, apostrophes, case, punctuation, and word division are left aside); word forms only (every differing segment close in spelling, such as *luogo* / *loco*, or an elided form of the other, such as *il* / *'l*); or other words. It prints the counts, the counts of the orthographic features, the pairs of word forms by frequency, and every segment of other words with the three lines.
- `en` compares Carlyle's English with Oelsner's word by word over each canto, places each difference on the page of Carlyle's edition where it falls, and sorts it: punctuation, case, spelling (close in spelling), and substituted, inserted, or deleted words, each also counted as marked by Oelsner's square brackets or not. It prints the counts, then every difference in words with its context and the Italian lines of that page where the two editions differ in words. The English of the leaf missing from Oelsner's edition (canto XXXIV) is left out.

The judgments made by hand on its output, and the tables rendered from them by `scripts/render_editions.py`, are described under [How they are made](#how-they-are-made).

`../commentary/scripts/source.py` reads the editions printed with an English translation passage by passage: Carlyle's edition one page at a time (the verse of the page and the English prose above it, which renders exactly that verse), Oelsner's one spread at a time (the Italian of an even page and the English of the odd page facing it, which renders the tercets that begin on the even page).
