# English and Italian text

This directory contains page images and proofread OCR transcriptions of
John A. Carlyle's *Dante's Divine Comedy: The Inferno. A Literal Prose
Translation, with the Text of the Original Collated from the Best
Editions, and Explanatory Notes*, fifth edition (London: George Bell & Sons,
1889; printed at the Chiswick Press). The title page is [009.png](009.png).

This is Carlyle's own text: the prefaces to the first (1848), second (1867),
and third editions are reprinted in [011.txt](011.txt)–[019.txt](019.txt).
The later edition revised by H. Oelsner is in [../en-oelsner/](../en-oelsner/).

The scanned copy carries the bookplate of Bertrand and Alys Russell
([002.png](002.png)).

Each `.png` has its transcription in the `.txt` with the same name
(`001.png`, `001.txt`, ... `514.txt`).

## Index

See [INDEX.md](INDEX.md) for the structure of the book and the mapping from
the front matter, cantos, and back matter to page files.

## Source

* [Dante's divine comedy : the inferno, a literal prose translation, with the text of the original collated from the best editions and explanatory notes - MacSphere](http://hdl.handle.net/11375/14640)
  (McMaster University Library; also `https://doi.org/10.71548/2741`)

The repository metadata gives only Dante as author and 1889 as the date; the
translator, edition, and publisher above are taken from the title page.

## Notes on the transcriptions

The GLM-OCR output was proofread against the page images. The transcriptions
follow these conventions:

* The print is followed as is, including spellings and accents that differ
  from modern editions of Dante; only damaged type is written as the intended
  letter.
* Prose is one paragraph per line, and Italian verse is one line per verse,
  without blank lines between tercets. Blocks (prose, verse, verse notes,
  footnotes) are separated by blank lines.
* Running heads, page numbers, and verse numbers are omitted. Footnote
  reference marks in the body are written as superscript digits where they
  are printed (`wood;²`). Footnotes are written as `1 text...` at the end of
  the page; a footnote continued from the previous page comes first, without a
  number.
* Small capitals in running text are written in uppercase; the first word of a
  canto is written in normal case.
* Quotation marks and apostrophes are curly (`“ ” ‘ ’`), as printed. They are
  not balanced artificially: a quotation running over several paragraphs opens
  each paragraph and closes only at the end, and quotations that continue
  across pages are left open on the page.
* Blank pages are marked `[Blank page]`, and the covers `[Cover]`.

## Plan

The English translation is printed as running paragraphs above the Italian
text. It is planned to be rearranged into a line-by-line alignment with the
Italian, using these as references:

* [../en-oelsner/](../en-oelsner/): the Temple Classics edition, whose English
  is aligned with the Italian tercet by tercet. Its wording differs in places
  (e.g. "the firm foot" here vs. "the right foot" there), so its text cannot be
  reused as is.
* [Inferno/01-en-carlyle.txt](../../Inferno/01-en-carlyle.txt) and
  [Inferno/02-en-carlyle.txt](../../Inferno/02-en-carlyle.txt): Cantos I–II
  already rearranged by hand, one tercet per line, from the Oelsner text.

## Credits

| Step | Model |
|---|---|
| OCR | GLM-OCR via Ollama v0.23.4 (see [Makefile](../Makefile)) |
| Proofreading | Gemini 3.8 Flash |
| Index ([INDEX.md](INDEX.md)) | Gemini 3.8 Flash |
| Final check | Claude Opus 5.5 |

Later versions of Ollama loop on this model, so v0.23.4 was used.
