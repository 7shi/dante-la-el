# English and Italian text

This directory contains page images and proofread OCR transcriptions of
*The Inferno of Dante Alighieri* in The Temple Classics (London: J. M. Dent &
Co., 1903), with the Italian text edited by H. Oelsner and the English prose
translation by John Aitken Carlyle. Publication details appear in
[008.txt](008.txt) and [011.txt](011.txt). By the General Editorial Note
([413.txt](413.txt)), the translation and the arguments are Carlyle's, reprinted
from his second edition (1867) with Oelsner's alterations in square brackets,
and the notes are Oelsner's.

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
* [The Inferno of Dante Alighieri (Fifth Edition, 1904) : Internet Archive](https://archive.org/details/inferno00dant_3)
  (only the two pages of plates, [411.png](411.png) and [412.png](412.png), and the pages
  of the other figures, [fifth/](fifth/))

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

The two pages of plates, printed pages 399–400 ([411.png](411.png) and
[412.png](412.png)), are taken from the third scan, the Fifth Edition (November
1904), which rewrote them: Fig. I (the plan of concentric spheres) and Fig. II
(a section of the eight revolving heavens, replacing the section of the
universe) with a long explanation that runs from the foot of page 399 onto page
400. The pages before and after them (398, 401) and the index of page 402 list
the same contents in both editions, so the rest stays the Fourth Edition
(1903). The two pages were transcribed by Claude Opus 5.5 from the images. The
Fifth Edition also prints the other figures without show-through: the pages
with them (`025`, `037`, `133`, `191`, `284`) are in [fifth/](fifth/), the same
file numbers, for the images of `texts/en-oelsner` only. All the Fifth Edition
pages were rendered from its PDF at 400 dpi.

## Credits

| Step | Model |
|---|---|
| OCR | Gemini 2.5 Flash (see [Makefile](../Makefile)) |
| Proofreading | GPT-6 Luna |
| Index ([INDEX.md](INDEX.md)) | Gemini 3.8 Flash |
| Final check | Claude Opus 5.5 |
| Check: retype and read-through ([SUMMARY.md](SUMMARY.md)) | Claude Opus 5.5 (retype, comparison with Tesseract and GLM-OCR, read-through, decisions in the images) |
