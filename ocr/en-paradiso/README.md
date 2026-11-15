# English and Italian text: Paradiso

This directory contains the page images and the checked transcriptions of *The
Paradiso of Dante Alighieri* in The Temple Classics (London: J. M. Dent & Co.; first
issued December 1899, the scan below the reprint of November 1910), the first volume of
the three, which
[../en-oelsner/](../en-oelsner/) (the *Inferno*) and
[../en-purgatorio/](../en-purgatorio/) follow in the same layout: the Italian
and the English face each other tercet by tercet.

By its Editorial Note (signed P. H. W. and H. O.):

- the Italian text is edited by H. Oelsner, based on the editions of Witte, Moore
  and Casini;
- the English prose translation and the arguments are by Philip H. Wicksteed;
- the notes are by both.

The check is finished ([SUMMARY.md](SUMMARY.md)): the base compared with three OCRs
and read through, every place decided in the image; the text is converted into
[../../texts/en-paradiso/](../../texts/en-paradiso/), with the maps and diagrams cut from
the scan. See [PLAN.md](PLAN.md) for the plan and the settled readings (the standard
flow of [../GUIDE.md](../GUIDE.md), as [../en-purgatorio/](../en-purgatorio/) ran it, with
the tools made there) and [DONE.md](DONE.md) for each step.

## Credits

| Step | By |
|---|---|
| The base (`NNN.txt`) | la-el-agy in its Orchestrator mode, its subagents called through `invoke_subagent` on Gemini 4 Hydrogen |
| Tesseract (`tesseract/`), GLM-OCR (`glm-ocr/`, through [../scripts/glmocr.py](../scripts/glmocr.py)) | run by the user |
| Internet Archive's OCR (`ia-ocr/`) | the library's own OCR, fetched by Claude (`iascan.py pages`) |
| The check: comparison, read-through, mechanical checks, decisions in the images ([SUMMARY.md](SUMMARY.md)) | Claude Opus 5.5; the doubtful places left to the user decided by the user |
| Index ([INDEX.md](INDEX.md)), the conversion and the figures | Claude Opus 5.5 |

## Layout

The printed page is the leaf − 10 throughout, from printed page 2 (`012`) to 420 (`430`);
the leaves before `011` (the epigraph, p. [1]) are unnumbered, and none is missing or
repeated. The structure page by page is in [INDEX.md](INDEX.md).

- **The cantos** (`012`–`419`) are printed on facing pages, as in the *Purgatorio*: the
  Italian on the even pages, with the tercet numbers at the right and the editor's
  marginal labels at the left (`Paradiso Terrestre`, `Luna`, `Marte`); the English, one
  paragraph per tercet, on the odd pages, with labels at the right (`The glory of God`).
  The argument runs across the top of the first spread, whose heads are `*PARADISO*` and
  `*CANTO N*` without page numbers. The notes begin at the foot of a spread and run on
  over the following pages.
- **The maps and diagrams**: most are printed below the notes of a page, with their
  labels and an italic caption naming the canto they illustrate, which may be another
  than the canto of the page (the three mirrors of Canto II on p. 59, in Canto V; the
  two retrospects of Cantos XXII and XXVII on pp. 396–397, in Canto XXXII); the maps of
  the district about Romano (p. 115), the district about Florence (p. 191) and
  Cacciaguida's Florence (p. 207) have pages of their own.
- **The tables**: the Tables of Kings I–IV (pp. 240–243) and Dante's descent from
  Cacciaguida (p. 373) are full pages of text printed sideways.
- **The end matter** (`420`–`430`): Wicksteed's note on Dante's Paradise (with a scheme
  of the heavens in type), an epigraph from Bernard, the general editorial note (no
  heading), the Editorial Note, the Index to Maps, Diagrams and Tables, and the printer's
  imprint.

## Transcription

The conventions of [../en-purgatorio/](../en-purgatorio/) (its README.md,
"Transcription"), taken over whole: lines as printed, line-end hyphens, running heads,
page numbers, signature marks and tercet numbers kept; a blank line between paragraphs
and before the foot line; the marginal labels as `**Label**` at the start of their line;
italics `*…*`; curly quotes `“ ”` and `’` in the English, `'` for the Italian elision;
the labels of the maps and diagrams line by line, name by name; the tables as text.
Misprints are kept as printed and marked `{{printed|fixed}}`
([misprints.tsv](misprints.tsv)); every decision of the check is a row of
[readcheck.tsv](readcheck.tsv). The settled readings of the edition are in PLAN.md.

## Source

* [The Paradiso of Dante Alighieri : Internet Archive](https://archive.org/details/paradisoofdante00dant)
  (PIMS, University of Toronto; the reprint of November 1910)

## Choice of the scan

Chosen 2026-11-15 by the steps of [../GUIDE.md](../GUIDE.md) ("Choosing the scan"),
from the OCR that Internet Archive provides for each scan
([../scripts/iascan.py](../scripts/iascan.py): `leaves`, `heads`, `diff`, `image`).

| Scan | Printing | Leaves | Printed page = leaf − | Images |
|---|---|---|---|---|
| **paradisoofdante00dant** (chosen) | reprint, November 1910 | 436 | 10, constant | the cleanest |
| [paradisoofdantea00dant](https://archive.org/details/paradisoofdantea00dant) (Getty; dated 1899 in the catalogue) | reprint, November 1910 | 434 | 10, constant | more show-through |
| [paradisodanteal00oelsgoog](https://archive.org/details/paradisodanteal00oelsgoog) (Google, Harvard) | Sixth Edition, February 1908 | 441 | 15 | binarized |
| [paradisoofdantea00dantrich](https://archive.org/details/paradisoofdantea00dantrich) | Fifth Edition, March 1904 | 438 | 12, but 14 for pp. 388–405 | strong show-through |
| [paradisoofdantea00dantuoft](https://archive.org/details/paradisoofdantea00dantuoft) | 1900 (no list of editions) | 430 | 6, constant | show-through |

- **The 1904 scan is defective**: pp. 388–389 are scanned twice, and pp. 406–407, the end
  of Canto XXXIII, are missing.
- **The 1910 reprint revised notes**, though its title verso lists it only as a reprint
  ("First issue of this Edition, December 1899; Reprinted August 1900, May 1901,
  February 1903, March 1904, February 1908, November 1910"). The word diff against
  1904 shows, among others: the note on the three mirrors (Canto II) rewritten; the
  note on V 124-126 extended ("… of a blessed spirit, as discerned by Dante, in any of
  the revolving spheres", checked in the images, where 1900, 1904 and 1908 end at
  "Dante"); Rabanus Maurus replaced by Isidore of Seville as the source of an
  arrangement; a note quoting Benvenuto. 1908 still has the old text.
- The two 1910 copies have the same text; the Getty copy is the spare.
- The 1900 printing has no Index to Maps, Diagrams and Tables at the end.
- The other copies listed are later Dent reprints (1921, 1941, 1954, 1958, 1965) or other
  translations.
