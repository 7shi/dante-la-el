# dante-la-el

Textualization of the translations of Dante's Divine Comedy in Latin, Greek, and other languages.

AI analysis and translation are also included.

## Source

Latin

* [Fratris Iohannis de Serravalle ... translatio et comentum totius libri - Dante Alighieri - Google Books](https://books.google.com/books?id=rt8_AQAAMAAJ)

Ancient Greek (a nineteenth-century literary translation closely modeled on Classical Greek)

* [Δάντου ο Αδής - Dante Alighieri - Google Books](https://books.google.gr/books?id=iMAFAAAAQAAJ)

English (Carlyle's literal prose translation, with the Italian text)

* [Dante's divine comedy : the inferno, a literal prose translation, with the text of the original collated from the best editions and explanatory notes - MacSphere](http://hdl.handle.net/11375/14640)
  (Carlyle's own edition: John A. Carlyle, fifth edition, London: George Bell & Sons, 1889)
* [The Inferno of Dante Alighieri : Dante Alighieri, 1265-1321; Oelsner, Hermann, 1871- ed; Carlyle, John Aitken, 1801-1879, tr : Internet Archive](https://archive.org/details/infernoofdanteal00dantrich)
  (edited by Oelsner: The Temple Classics, London: J. M. Dent & Co., 1903; the Carlyle text in [Inferno/](Inferno/) is taken from this edition; [ocr/en-oelsner/](ocr/en-oelsner/))
  * [The Inferno of Dante Alighieri (another copy of the same edition) : Internet Archive](https://archive.org/details/infernoofdanteal00dant)
    (the leaf with pp. 385–386, missing from the scan above, is taken from it)
  * [The Inferno of Dante Alighieri (Fifth Edition, 1904) : Internet Archive](https://archive.org/details/inferno00dant_3)
    (the two pages of plates, pp. 399–400, rewritten in this edition, and the images of the figures are taken from it)

English (the other two volumes of the Temple Classics, with the Italian text edited by Oelsner)

* [The Purgatorio of Dante Alighieri : Internet Archive](https://archive.org/details/purgatorioofdant00dant_0)
  (Thomas Okey's prose translation: London: J. M. Dent & Co., Fourth Edition, 1904; [ocr/en-purgatorio/](ocr/en-purgatorio/), converted into [texts/en-purgatorio/](texts/en-purgatorio/))
* [The Paradiso of Dante Alighieri : Internet Archive](https://archive.org/details/paradisoofdante00dant)
  (Philip H. Wicksteed's prose translation: London: J. M. Dent & Co., reprint of November 1910; [ocr/en-paradiso/](ocr/en-paradiso/), in progress)

## OCR

[ocr/](ocr/) contains the scanned page images of the Latin (`la/`), Ancient Greek (`grc/`), and English/Italian (`en/` for Carlyle's own edition, `en-oelsner/` for Oelsner's edition, `en-purgatorio/` and `en-paradiso/` for the *Purgatorio* and the *Paradiso* of the same series) sources, their OCR transcriptions (`.txt`), and the scripts used to produce them. See [ocr/README.md](ocr/README.md) for details.

## Dependency

Some of the checks read the Italian text of [dante-corpus](https://github.com/7shi/dante-corpus) through its API, as an editable path dependency (`../dante-corpus`), so both repositories must share one parent directory:

```bash
git clone https://github.com/7shi/dante-corpus.git
git clone https://github.com/7shi/dante-la-el.git
make -C dante-corpus
cd dante-la-el
uv sync
```

## References

* https://latindiscussion.org/threads/dante-divina-commedia-inferno-i.16133/
* https://italia.codigoro.discussioni.narkive.com/6tCRMXuo/daniele-storia

Italian

* [La Divina Commedia di Dante: Complete by Dante Alighieri | Project Gutenberg](https://www.gutenberg.org/ebooks/1000)
