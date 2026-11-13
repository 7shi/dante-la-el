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
| `scripts/` | The scripts that prepare and transcribe the pages ([scripts/README.md](scripts/README.md)) |
| `PLAN.md` | The plan of the checks against the images, and their state |
| `GUIDE.md` | General lessons of the checks: the shortest path for checking an OCR transcription in a new project |

Each `.png` has its transcription in the `.txt` with the same name.

## Usage

Run from this directory. The dependencies are managed by the project root `pyproject.toml`.

```sh
make la        # or: make en / make en-oelsner / make grc / make all
make check     # list empty .txt files
```

The scripts themselves, the PDF preparation for a new source and the commands behind the
Makefile are in [scripts/README.md](scripts/README.md).

## Notes

* `make en` uses GLM-OCR through Ollama instead of `scripts/ocr.py` (see [en/README.md](en/README.md)).
* The `.png` files are large (about 1 GB in total).
