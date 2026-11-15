This directory contains the page images and the checked transcriptions of *The
Purgatorio of Dante Alighieri* in The Temple Classics (London: J. M. Dent & Co.; first
edition November 1901, the scan below the fourth, November 1904), the companion volume of
[../en-oelsner/](../en-oelsner/) (the *Inferno*), in the same layout: the Italian and the
English face each other tercet by tercet. Each `NNN.png` (NNN the leaf) has its
transcription in `NNN.txt`; the readings compared with it are in `tesseract/`, `glm-ocr/`
and `ia-ocr/`. The converted text is [../../texts/en-purgatorio/](../../texts/en-purgatorio/).

By the closing note of the series editor (I. G., Israel Gollancz, October 1901):

- the Italian text and the notes are by H. Oelsner;
- the English prose translation is by Thomas Okey (Carlyle translated only the
  *Inferno*);
- the arguments are by Philip H. Wicksteed.

See [SUMMARY.md](SUMMARY.md) for an account of the transcription and the check,
[PLAN.md](PLAN.md) for the plan and the settled readings, [DONE.md](DONE.md) for the record
step by step, and [INDEX.md](INDEX.md) for the structure of the book and the mapping from
cantos, plates and end matter to the leaves.

## Source

* [The Purgatorio of Dante Alighieri : Internet Archive](https://archive.org/details/purgatorioofdant00dant_0)
  (Getty Research Institute; Fourth Edition, November 1904)

## Choice of the scan

Chosen 2026-11-15 by the steps of [../GUIDE.md](../GUIDE.md) ("Choosing the scan"),
from the OCR that Internet Archive provides for each scan
([../scripts/iascan.py](../scripts/iascan.py): `leaves`, `heads`, `diff`, `image`).

| Scan | Printing | Leaves | Printed page = leaf − | Images |
|---|---|---|---|---|
| **purgatorioofdant00dant_0** (chosen) | Fourth Edition, November 1904 | 462 | 12, constant | clean |
| [purgatorio00aliguoft](https://archive.org/details/purgatorio00aliguoft) | Third Edition, September 1903 | 458 | 10, constant | strong show-through; the left margin cut into the line starts (p. 101) |

- No missing or repeated leaf in either.
- The two printings have the same text: their word diff leaves only OCR noise. The
  Index to Plates, Tables, etc. lists the same plates on the same pages (12, 13, 34–35,
  47, 59, 86–91, 103, 241, 376–377); the Fourth Edition sets it in mixed case.
- The other copies listed are later Dent reprints (1924, 1926, 1941, 1964) or other
  translations.

## Layout

The printed page is the leaf − 12 throughout, from printed page 2 (`014`) to 443 (`455`);
the leaves before `013` (the epigraph, p. [1]) are unnumbered, and none is missing or
repeated.

- **The cantos** (`014`–`443`) are printed on facing pages: the Italian on the even pages,
  with the tercet numbers at the right and the editor's marginal labels at the left
  (`Anti-purgatorio`, `Girone I`); the English, one paragraph per tercet, on the odd
  pages, with labels at the right (`Proem`, `The proud`). The argument (Wicksteed's) runs
  across the top of the first spread, whose heads are `*PURGATORIO*` and `*CANTO N*`
  without page numbers; the page number then stands at the foot. The notes begin at the
  foot of a spread and run on over the following pages.
- **The diagrams** of pp. 12, 13, 34, 35, 47 and 103 are printed below the notes of their
  page, with their labels and an italic caption (none on p. 35); the plate of the Zodiac
  (p. 59) has a page of its own; the family tables (pp. 86–91, 241) are full pages of text;
  the map of Upper and Central Italy runs across pp. 376–377.
- **The end matter** (`444`–`455`): Wicksteed's note on Dante's Purgatory and the
  chronology, the general editorial note (no heading), the translator's note, the
  editorial note, the Index to Plates, Tables, etc., and the printer's imprint.
- **The signature marks** (`B`, `2 A`) stand at the foot of the first page of each sheet
  of 16 pages; on p. 241 (`253`) the `Q` stands above the page number.

## Transcription

The conventions of [../en-oelsner/](../en-oelsner/): lines as printed, line-end hyphens,
running heads, page numbers, signature marks and tercet numbers kept; a blank line between
paragraphs and before the foot line; the marginal labels as `**Label**` at the start of
their line; italics `*…*`; curly quotes `“ ”` and `’` in the English, `'` for the Italian
elision; the labels of the diagrams and the map line by line, name by name. Misprints are
kept as printed and marked `{{printed|fixed}}` ([misprints.tsv](misprints.tsv)); every
decision of the check is a row of [readcheck.tsv](readcheck.tsv). The settled readings of
the edition are in PLAN.md.

## Credits

| Step | By |
|---|---|
| The base (`NNN.txt`) | la-el-agy in its Orchestrator mode: Gemini 4 Argon directing Gemini 4 Hydrogen workers |
| Tesseract (`tesseract/`), GLM-OCR (`glm-ocr/`) | run by the user |
| Internet Archive's OCR (`ia-ocr/`) | the library's own OCR, fetched by Claude (`iascan.py pages`) |
| The check: comparison, read-through, mechanical checks, decisions in the images ([SUMMARY.md](SUMMARY.md)) | Claude Opus 5.5 |
| Index ([INDEX.md](INDEX.md)), the conversion and the figures | Claude Opus 5.5 |
