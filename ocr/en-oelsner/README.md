# English and Italian text

This directory contains page images and proofread OCR transcriptions of
*The Inferno of Dante Alighieri* in The Temple Classics (London: J. M. Dent &
Co., 1903), with the Italian text edited by H. Oelsner and the English prose
translation by John Aitken Carlyle. Publication details appear in
[008.txt](008.txt) and [011.txt](011.txt).

This is a later edition revised by Oelsner, so its layout and text differ from
Carlyle's own edition in [../en/](../en/).

This edition was originally chosen because its English translation is aligned
with the Italian tercet by tercet, which makes it a good basis for re-editing
into a line-by-line correspondence. Carlyle's own edition prints the
translation as running paragraphs above the Italian text.

Each `.png` has its transcription in the `.txt` with the same name
(`001.png`, `001.txt`, ... `418.txt`).

## Source

* [The Inferno of Dante Alighieri : Dante Alighieri, 1265-1321; Oelsner, Hermann, 1871- ed; Carlyle, John Aitken, 1801-1879, tr : Internet Archive](https://archive.org/details/infernoofdanteal00dantrich)
* [The Inferno of Dante Alighieri (another copy of the same edition) : Internet Archive](https://archive.org/details/infernoofdanteal00dant)
  (only the leaf missing from the first scan, [397.png](397.png) and [398.png](398.png))

The Carlyle text in [../../Inferno/](../../Inferno/) (e.g. `compare-en.md`) is
taken from this edition.

## Index

See [INDEX.md](INDEX.md) for the structure of the book and the mapping from
cantos, appendices, and plates to page files.

## Layout

The main text is printed on facing pages: the Italian text on even printed
pages and the English translation on odd printed pages. Each canto begins with
an argument (summary) and ends with notes.

The file number is the printed page number plus 12 (printed pages 2–402,
`014`–`414`). The leaf with printed pages 385–386 in Canto XXXIV is missing
from the first scan; [397.png](397.png) and [398.png](398.png) are taken from
the second scan (its pages 393–394), whose pages 384 and 387 match the first
scan line for line. They were transcribed by Claude Opus 5.5 from the images
and compared with Carlyle's own edition ([../../texts/en/](../../texts/en/))
and dante-corpus.

## Credits

| Step | Model |
|---|---|
| OCR | Gemini 2.5 Flash (see [Makefile](../Makefile)) |
| Proofreading | GPT-6 Luna |
| Index ([INDEX.md](INDEX.md)) | Gemini 3.8 Flash |
| Final check | Claude Opus 5.5 |
| Check: retype and read-through ([SUMMARY.md](SUMMARY.md)) | Claude Opus 5.5 (retype, comparison with Tesseract and GLM-OCR, read-through, decisions in the images) |
