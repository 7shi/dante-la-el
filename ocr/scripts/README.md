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
