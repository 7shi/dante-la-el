# English and Italian text

This directory contains page images and OCR transcriptions (not yet
proofread) of John A. Carlyle's *Dante's Divine Comedy: The Inferno. A Literal
Prose Translation, with the Text of the Original Collated from the Best
Editions, and Explanatory Notes*, fifth edition (London: George Bell & Sons,
1889; printed at the Chiswick Press). The title page is [009.png](009.png).

This is Carlyle's own text: the prefaces to the first (1848), second (1867),
and third editions are reprinted in [011.txt](011.txt)–[019.txt](019.txt).
The later edition revised by H. Oelsner is in [../en-oelsner/](../en-oelsner/).

The scanned copy carries the bookplate of Bertrand and Alys Russell
([002.png](002.png)).

Each `.png` has its transcription in the `.txt` with the same name
(`001.png`, `001.txt`, ... `514.txt`).

## Source

* [Dante's divine comedy : the inferno, a literal prose translation, with the text of the original collated from the best editions and explanatory notes - MacSphere](http://hdl.handle.net/11375/14640)
  (McMaster University Library; also `https://doi.org/10.71548/2741`)

The repository metadata gives only Dante as author and 1889 as the date; the
translator, edition, and publisher above are taken from the title page.

## Notes on the transcriptions

The `.txt` files are the raw output of GLM-OCR. Pages without text (blank
pages, plates) may contain only an empty Markdown code block, and pages with
little text may be misread.

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

Later versions of Ollama loop on this model, so v0.23.4 was used.
