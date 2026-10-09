# Latin text

This directory contains page images and proofread OCR transcriptions of
Giovanni da Serravalle's Latin translation and commentary on Dante's *Divine
Comedy*, *Translatio et Comentum totius libri Dantis Aldigherii*, edited by
Marcellino da Civezza and Teofilo Domenichelli (Prato: Marcello Vestri, 1891).
The title page is [0009.txt](0009.txt).

Each `.png` has its transcription in the `.txt` with the same name
(`0001.png`, `0001.txt`, ... `1296.txt`).

## Index

See [INDEX.md](INDEX.md) for the structure of the book and the mapping from
the front matter, cantos, essays, and appendix to page files.

## Layout

The book contains the whole *Comedy* (Inferno, Purgatorio, Paradiso). Each
canto has Serravalle's Latin summary (*Summarium*), the Italian text with his
line-by-line Latin translation, his Latin commentary (*Comentum*), and a modern
Italian essay by the editors.

The front matter is numbered in Roman numerals from V to XLVIII; the file
number is the printed page number plus 6. The main body is numbered from 1 to
1236; the file number is the printed page number plus 54. No pages are
missing or duplicated. Blank pages are transcribed as
`[Blank page]`.

## Credits

| Step | Model |
|---|---|
| OCR | Gemini 2.5 Flash (see [Makefile](../Makefile)) |
| Proofreading | GPT-6 Luna |
| Index ([INDEX.md](INDEX.md)) | Gemini 3.8 Flash |
| Final check | Claude Opus 5.5 |

In the final check, [0106.txt](0106.txt), [0314.txt](0314.txt), and
[0553.txt](0553.txt) were retranscribed from the images by Claude Opus 5.5.
[0379.txt](0379.txt), [0574.txt](0574.txt), [0671.txt](0671.txt), and
[1249.txt](1249.txt) were OCRed again with Gemini 2.5 Flash and proofread by
Gemini 3.8 Flash.
