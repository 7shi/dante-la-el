# The Temple Classics Paradiso (1910)

*The Paradiso of Dante Alighieri*, The Temple Classics (London: J. M. Dent & Co.; first issued December 1899, the reprint of November 1910): the Italian text edited by H. Oelsner, the English prose translation and the arguments by Philip H. Wicksteed, the notes by both. The companion of [`../en-oelsner/`](../en-oelsner/) (the *Inferno*) and [`../en-purgatorio/`](../en-purgatorio/), in the same layout: the Italian and the English face each other tercet by tercet; each canto has an argument, the editor's marginal labels, and notes, and some are followed by maps, diagrams or tables.

These files are generated from the checked page transcriptions in [`ocr/en-paradiso/`](../../ocr/en-paradiso/) by [`convert_en_oelsner.py`](../scripts/convert_en_oelsner.py) (`uv run texts/scripts/convert_en_oelsner.py paradiso`), the images by [`crop_en_oelsner_images.py`](../scripts/crop_en_oelsner_images.py) (`… paradiso`); see [`ocr/en-paradiso/README.md`](../../ocr/en-paradiso/README.md) for the source and [`../PLAN.md`](../PLAN.md) for the conventions. Do not edit them by hand: correct `ocr/en-paradiso/` and convert again.

## Reading the files

As in [`../en-purgatorio/README.md`](../en-purgatorio/README.md):

- **Pages**: every printed page starts with a comment such as `<!-- p. 3 (013) -->`: the printed page number and the scan, `ocr/en-paradiso/013.png`.
- **Spreads**: read band by band: the argument across the top of the first spread, then the Italian page, then the English page, then the notes across the bottom; a page that appears again in a later band gets its marker again with the band named (`<!-- p. 2 (012), text -->`, `<!-- p. 10 (020), notes -->`).
- **Headings**: `## Argument` and `## Notes` are added; the book prints no heading for them.
- **Verse**: tercets with the second and third lines indented; the first line of each tercet ends with its number, as printed (`… prende 4`). The canto's last line, printed alone, is translated in the last English paragraph.
- **English**: one paragraph per tercet, as printed.
- **Marginal labels**: comments at the end of the line or paragraph they stand beside: `<!-- label: Paradiso Terrestre -->`, `<!-- label: The glory of God -->`.
- **Notes**: keyed to verse numbers (`37-39. …`), as plain paragraphs. A note continued on the next page is joined to its start.
- **Maps and diagrams** printed below the notes of a page follow the notes of that page: the image, the labels line by line, the caption; the diagram of p. 12, printed between two notes, follows the note before it. The maps with pages of their own (pp. 115, 191, 207) are the image, then their labels. The caption names the canto a figure illustrates, which may be another than the canto of the file (`images/NNN.jpg`, NNN the scan).
- **Tables**: the Tables of Kings (pp. 240–243) and Dante's descent from Cacciaguida (p. 373), printed sideways, are text only, one person or couple per line; the persons named in Canto XIX are bold, as the thick letters of the print.
- **Misprints** are given corrected; the printed forms are listed in [`ocr/en-paradiso/misprints.tsv`](../../ocr/en-paradiso/misprints.tsv).
- **Not transcribed**: the covers, endpapers, blank pages, and the library's card.

## Contents

| File | Section | Pages |
|---|---|---|
| [001-title-page.md](001-title-page.md) | Series half-title, printings, frontispiece, title page, epigraph | [1] |

### The Paradiso

| File | Canto | Pages | First line | After the notes |
|---|---|---|---|---|
| [002-canto-01.md](002-canto-01.md) | I | 2–13 | La gloria di colui che tutto move | Diagram of the four circles and three crosses, in the notes |
| [003-canto-02.md](003-canto-02.md) | II | 14–25 | O voi, che siete in piccioletta barca, |  |
| [004-canto-03.md](004-canto-03.md) | III | 26–35 | Quel sol, che pria d'amor mi scaldò il petto, |  |
| [005-canto-04.md](005-canto-04.md) | IV | 36–47 | Intra due cibi, distanti e moventi |  |
| [006-canto-05.md](006-canto-05.md) | V | 48–59 | “S' io ti fiammeggio nel caldo d' amore | Diagram of the three mirrors (to Canto II) |
| [007-canto-06.md](007-canto-06.md) | VI | 60–75 | “Poscia che Costantin l' aquila volse |  |
| [008-canto-07.md](008-canto-07.md) | VII | 76–89 | “*Osanna sanctus Deus Sabaoth,* | Maps of Provence and of Naples and Sicily (to Canto VIII) |
| [009-canto-08.md](009-canto-08.md) | VIII | 90–101 | Solea creder lo mondo in suo periclo | Maps of Hungary, Rascia, etc. (to Cantos VIII and XIX) and of the Mediterranean (to Canto IX) |
| [010-canto-09.md](010-canto-09.md) | IX | 102–115 | Da poi che Carlo tuo, bella Clemenza, | Map of the district about Romano |
| [011-canto-10.md](011-canto-10.md) | X | 116–129 | Guardando nel suo figlio con l' amore |  |
| [012-canto-11.md](012-canto-11.md) | XI | 130–141 | O insensata cura dei mortali, | Map shewing the position of Assisi |
| [013-canto-12.md](013-canto-12.md) | XII | 142–155 | Sì tosto come l' ultima parola |  |
| [014-canto-13.md](014-canto-13.md) | XIII | 156–167 | Imagini chi bene intender cupe |  |
| [015-canto-14.md](015-canto-14.md) | XIV | 168–179 | Dal centro al cerchio, e sì dal cerchio al centro, |  |
| [016-canto-15.md](016-canto-15.md) | XV | 180–191 | Benigna volontade, in cui si liqua | Map of the district about Florence |
| [017-canto-16.md](017-canto-16.md) | XVI | 192–207 | O poca nostra nobiltà di sangue! | Map of Cacciaguida's Florence |
| [018-canto-17.md](018-canto-17.md) | XVII | 208–217 | Qual venne a Climenè, per accertarsi |  |
| [019-canto-18.md](019-canto-18.md) | XVIII | 218–227 | Già si godeva solo del suo verbo |  |
| [020-canto-19.md](020-canto-19.md) | XIX | 228–243 | Parea dinanzi a me con l' ali aperte | Tables of Kings I–IV |
| [021-canto-20.md](021-canto-20.md) | XX | 244–255 | Quando colui che tutto il mondo alluma |  |
| [022-canto-21.md](022-canto-21.md) | XXI | 256–267 | Già eran gli occhi miei rifissi al volto |  |
| [023-canto-22.md](023-canto-22.md) | XXII | 268–279 | Oppresso di stupore alla mia guida |  |
| [024-canto-23.md](024-canto-23.md) | XXIII | 280–289 | Come l' augello, intra l' amate fronde, |  |
| [025-canto-24.md](025-canto-24.md) | XXIV | 290–301 | “O sodalizio eletto alla gran cena |  |
| [026-canto-25.md](026-canto-25.md) | XXV | 302–313 | Se mai continga che il poema sacro, |  |
| [027-canto-26.md](027-canto-26.md) | XXVI | 314–325 | Mentr' io dubbiava per lo viso spento, |  |
| [028-canto-27.md](028-canto-27.md) | XXVII | 326–337 | “Al Padre, al Figlio, allo Spirito Santo” |  |
| [029-canto-28.md](029-canto-28.md) | XXVIII | 338–349 | Poscia che contro alla vita presente |  |
| [030-canto-29.md](030-canto-29.md) | XXIX | 350–361 | Quando ambo e due i figli di Latona, |  |
| [031-canto-30.md](031-canto-30.md) | XXX | 362–373 | Forse sei mila miglia di lontano | Table: Dante's descent from Cacciaguida (to Canto XV) |
| [032-canto-31.md](032-canto-31.md) | XXXI | 374–385 | In forma dunque di candida rosa |  |
| [033-canto-32.md](033-canto-32.md) | XXXII | 386–397 | Affetto al suo piacer, quel contemplante | Maps of the world west and east of Jerusalem (to Cantos XXVII and XXII) |
| [034-canto-33.md](034-canto-33.md) | XXXIII | 398–409 | “Vergine madre, figlia del tuo figlio, |  |

### End matter

| File | Section | Pages |
|---|---|---|
| [035-note-on-dantes-paradise.md](035-note-on-dantes-paradise.md) | Note on Dante’s Paradise (Wicksteed), with the scheme of the heavens | 410–413 |
| [036-epigraph.md](036-epigraph.md) | Epigraph (Bernard) | 414 |
| [037-general-editorial-note.md](037-general-editorial-note.md) | General editorial note (I. G.; no heading printed) | 415 |
| [038-editorial-note.md](038-editorial-note.md) | Editorial Note (H. O., P. H. W.) | 416–418 |
| [039-index-to-maps-diagrams-and-tables.md](039-index-to-maps-diagrams-and-tables.md) | Index to Maps, Diagrams and Tables, and the printer’s imprint | 419–420 |
