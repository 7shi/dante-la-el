# Scripts for `ocr/`

The scripts shared by all the sources: preparing the page images and transcribing them.
The commands below are run from `ocr/` (one level up); the dependencies are managed by
the project root `pyproject.toml`. The scripts of one source are in its own directory
([`la/scripts/`](../la/scripts/README.md)).

| Script | Description |
|---|---|
| `ocr.py` | Transcribes images with Gemini and saves `<name>.txt` next to each image |
| `checkrep.py` | Detects repetitive output in `.txt` files and optionally deletes them |
| `check_outlier.py` | Lists `.txt` files whose length is an outlier (runaway output) |
| `pdf2png.py` | Converts a PDF to numbered PNG images |
| `split_pdf.py` | Splits a PDF into chunks of N pages |
| `rename_files.py` | Renames `page_12.png` to `012.png` in a directory |

## The read-through

The tools of the last reading of each text for sense ([ocr/PLAN.md](../PLAN.md), "Read-through"), run
from the repository root. A reader gets whole pages of the converted text and lists the
places that look wrong; each place is found in the page file, decided in the image, and a
misreading is corrected.

| Script | Description |
|---|---|
| `pages.py TEXTDIR FIRST LAST [-o OUT]` | The pages of scans FIRST–LAST of `texts/…`, cut at the page markers (`<!-- p. 26 (0080) -->`), for the reader |
| `findline.py DIR FLAGS [-o OUT] [--min R]` | The lines of `DIR/PAGE.txt` where the reader's flagged phrases are (`page phrase reason`): compared word by word without case, punctuation, italic marks and brackets, across hyphenated line breaks and page breaks; otherwise the most similar run of words (`~`) |
| `wordcrop.py DIR OUT SPEC... [-t TESS]` | Bands of `DIR/PAGE.png` around words (`PAGE:TEXT[:N]`, the Nth word of Tesseract's `TESS/PAGE.tsv` containing TEXT), stacked into one PNG under labels with the match count, for deciding a flagged place in the image |
| `txtfix.py DIR FIXES [-n]` | Applies the fixes, `PAGE:LINE old new` (`old` once in the line); writes nothing if a row fails |
| `cmpread.py DIR RETYPE [-t TESS] [-g GLM] [-i IA] [-o OUT] [PAGE...]` | The comparison before the read-through ([ocr/PLAN.md](../PLAN.md), step 2): `DIR/PAGE.txt` (the printed side of the marks), a retype `RETYPE/PAGE.txt` and Tesseract's words aligned word by word (quotes, dashes, spacing and note markers normalized); every place the base differs from the retype, classed A (Tesseract agrees with the retype), B (the retype alone), C (a run one lacks); with `-g` GLM-OCR as a fourth reading (class D), with `-i` Internet Archive's OCR as a column that does not vote |
| `misprints.py DIR [--fix-lines]` | Checks the misprint marks `{{printed\|fixed}}` of `DIR`'s pages against `DIR/misprints.tsv` (every applied row one mark, every mark a row); with `--fix-lines` writes the new line of a mark that has moved |

## Choosing the scan

Before a new source is added, its scans on Internet Archive are compared
([../GUIDE.md](../GUIDE.md), "Choosing the scan"), run from the repository root:

| Script | Description |
|---|---|
| `iascan.py fetch -d DIR ID...` | Downloads the OCR files that Internet Archive provides (`_djvu.txt`, `_djvu.xml`, `_page_numbers.json`) into `DIR/ID/` |
| `iascan.py image -d DIR ID LEAF...` | Downloads leaf images (`ID-nLEAF.jpg`), to compare the same page across scans |
| `iascan.py leaves ID_djvu.xml` | The printed page number of each leaf minus the leaf number: the runs of a constant offset, the leaves off it, and repeated leaves |
| `iascan.py heads ID_djvu.xml FIRST LAST` | The first and last line of some leaves, to look at a place `leaves` marked |
| `iascan.py diff A_djvu.txt B_djvu.txt [--min 5]` | A word diff of two printings, only the blocks of MIN words or more: the revisions above the OCR noise |
| `iascan.py pages ID_djvu.xml -d DIR [--first L] [--last L] [--shift K]` | The chosen scan's OCR as page files `DIR/PAGE.txt` (leaf + K), for `cmpread.py -i` |
| `iapdf.py URL -o OUT [-d DIR] [--dpi 300] [--first P] [--last P]` | The chosen scan's PDF (named by its URL `archive.org/details/ID`, or by ID) downloaded into `DIR/ID/ID.pdf` (default `tmp`; an interrupted download resumes) and rendered as `OUT/NNN.png`, NNN the PDF page = the leaf of the OCR (pages already rendered skipped); the page count checked against `DIR/ID/ID_djvu.xml` if fetched. Needs `poppler-utils` |
| `glmocr.py IMAGE... -o OUT [-m ollama:glm-ocr]` | GLM-OCR on page images through llm7shi (Ollama): `OUT/NNN.txt` for `NNN.png`, the same output as `ollama run glm-ocr "Text Recognition: FILE"`; a page that runs away is stopped, written as it stood and listed at the end (blank pages run away: empty their files); pages done are skipped, no partial files |

## PDF preparation

For adding a new source, in this order:

```sh
uv run scripts/split_pdf.py book.pdf --chunk-size 100         # book-001-100.pdf, ...
uv run scripts/pdf2png.py book-001-100.pdf -o la -s 1         # la/001.png, ...
uv run scripts/rename_files.py la                             # page_12.png -> 012.png
```

`pdf2png.py` needs `poppler-utils` installed on the system.

## Transcription

`make la` (and the other targets of the [Makefile](../Makefile)) runs `ocr.py`.
`ocr.py` skips images that already have a `.txt`, so an interrupted run can be resumed. To
redo a page, delete its `.txt`.

```sh
uv run scripts/ocr.py -m gemini-2.5-flash -p "Please transcribe the text. The text is written in Latin." la/*.png
uv run scripts/ocr.py -m gemini-2.5-flash --dry la/*.png      # list the targets only
uv run scripts/checkrep.py la/*.txt                           # find repetitive output
uv run scripts/check_outlier.py la/*.txt                      # find runaway pages
```

A Gemini API key is required for `ocr.py`. It is read by `llm7shi`.
