# ocr

Scanned page images of the sources (see the root [README](../README.md)) and the scripts that transcribe them with Gemini or GLM-OCR.

## Contents

| Path | Description |
|---|---|
| `la/` | Latin pages (`0001.png`, `0001.txt`, ...; about 1,300 pages) |
| `grc/` | Ancient Greek pages (`001.png`, `001.txt`, ...; about 350 pages) |
| `en/` | English and Italian pages, Carlyle's own edition (5th ed., 1889; `001.png`, `001.txt`, ...; 514 pages) |
| `en-oelsner/` | English and Italian pages, Temple Classics edition revised by H. Oelsner (1903; `001.png`, `001.txt`, ...; 416 pages) |
| `Makefile` | Runs the OCR for each language directory |
| `ocr.py` | Transcribes images with Gemini and saves `<name>.txt` next to each image |
| `checkrep.py` | Detects repetitive output in `.txt` files and optionally deletes them |
| `pdf2png.py` | Converts a PDF to numbered PNG images |
| `split_pdf.py` | Splits a PDF into chunks of N pages |
| `rename_files.py` | Renames `page_12.png` to `012.png` in a directory |

Each `.png` has its transcription in the `.txt` with the same name.

## Usage

Run from this directory. The dependencies are managed by the project root `pyproject.toml`.

```sh
make la        # or: make en / make en-oelsner / make grc / make all
make check     # list empty .txt files
```

`ocr.py` skips images that already have a `.txt`, so an interrupted run can be resumed. To redo a page, delete its `.txt`.

```sh
uv run ocr.py -m gemini-2.5-flash -p "Please transcribe the text. The text is written in Latin." la/*.png
uv run ocr.py -m gemini-2.5-flash --dry la/*.png      # list the targets only
uv run checkrep.py la/*.txt                           # find repetitive output
```

## PDF preparation

For adding a new source, in this order:

```sh
uv run split_pdf.py book.pdf --chunk-size 100         # book-001-100.pdf, ...
uv run pdf2png.py book-001-100.pdf -o la -s 1         # la/001.png, ...
uv run rename_files.py la                             # page_12.png -> 012.png
```

`pdf2png.py` needs `poppler-utils` installed on the system.

## Notes

* A Gemini API key is required for `ocr.py`. It is read by `llm7shi`.
* `make en` uses GLM-OCR through Ollama instead of `ocr.py` (see [en/README.md](en/README.md)).
* The `.png` files are large (about 1 GB in total).
