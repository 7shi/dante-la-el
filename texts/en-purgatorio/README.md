# The Temple Classics Purgatorio (1904)

*The Purgatorio of Dante Alighieri*, The Temple Classics (London: J. M. Dent & Co., Fourth Edition, 1904; first November 1901): the Italian text and the notes edited by H. Oelsner, the English prose translation by Thomas Okey, the arguments by Philip H. Wicksteed. The companion of [`../en-oelsner/`](../en-oelsner/) (the *Inferno*), in the same layout: the Italian and the English face each other tercet by tercet; each canto has an argument, the editor's marginal labels, and notes, and some are followed by diagrams, a plate, family tables or a map.

These files are generated from the checked page transcriptions in [`ocr/en-purgatorio/`](../../ocr/en-purgatorio/) by [`convert_en_oelsner.py`](../scripts/convert_en_oelsner.py) (`uv run texts/scripts/convert_en_oelsner.py purgatorio`), the images by [`crop_en_oelsner_images.py`](../scripts/crop_en_oelsner_images.py) (`… purgatorio`); see [`ocr/en-purgatorio/README.md`](../../ocr/en-purgatorio/README.md) for the source and [`../PLAN.md`](../PLAN.md) for the conventions. Do not edit them by hand: correct `ocr/en-purgatorio/` and convert again.

## Reading the files

As in [`../en-oelsner/README.md`](../en-oelsner/README.md):

- **Pages**: every printed page starts with a comment such as `<!-- p. 3 (015) -->`: the printed page number and the scan, `ocr/en-purgatorio/015.png`.
- **Spreads**: read band by band: the argument across the top of the first spread, then the Italian page, then the English page, then the notes across the bottom; a page that appears again in a later band gets its marker again with the band named (`<!-- p. 2 (014), text -->`, `<!-- p. 10 (022), notes -->`).
- **Headings**: `## Argument` and `## Notes` are added; the book prints no heading for them.
- **Verse**: tercets with the second and third lines indented; the first line of each tercet ends with its number, as printed (`… regno, 4`). The canto's last line, printed alone, is translated in the last English paragraph.
- **English**: one paragraph per tercet, as printed.
- **Marginal labels**: comments at the end of the line or paragraph they stand beside: `<!-- label: Anti-purgatorio -->`, `<!-- label: The proud -->`.
- **Notes**: keyed to verse numbers (`73-75. …`), as plain paragraphs. A note continued on the next page is joined to its start.
- **Diagrams** printed below the notes of a page (pp. 12, 13, 34, 35, 47, 103) follow the notes of that page: the image, the labels line by line, the caption. The plate of the Zodiac (p. 59) and the map (pp. 376–377, one image for each page) are shown as images above their labels; the family tables are text only, line by line (`images/NNN.jpg`, NNN the scan).
- **Signatures**: the notes and the end matter keep their signatures as paragraphs (`H. O.`, `T. O.`).
- **Not transcribed**: the covers, endpapers, blank pages and the library label.

## Contents

| File | Section | Pages |
|---|---|---|
| [001-title-page.md](001-title-page.md) | Series half-title, editions, frontispiece, title page, epigraph | — |

### The Purgatorio

| File | Canto | Pages | First line | After the notes |
|---|---|---|---|---|
| [002-canto-01.md](002-canto-01.md) | I | 2–13 | Per correr miglior acqua alza le vele | Diagrams (a), (b) in the notes |
| [003-canto-02.md](003-canto-02.md) | II | 14–23 | Già era il sole all' orizzonte giunto, |  |
| [004-canto-03.md](004-canto-03.md) | III | 24–35 | Avvegna che la subitana fuga | Diagrams of synchronisms in the notes |
| [005-canto-04.md](005-canto-04.md) | IV | 36–47 | Quando per dilettanze ovver per doglie, | Diagram (c) in the notes |
| [006-canto-05.md](006-canto-05.md) | V | 48–59 | Io era già da quell' ombre partito, | Plate: the signs of the Zodiac |
| [007-canto-06.md](007-canto-06.md) | VI | 60–73 | Quando si parte il giuoco della zara, |  |
| [008-canto-07.md](008-canto-07.md) | VII | 74–91 | Poscia che l' accoglienze oneste e liete | Family tables I–VI |
| [009-canto-08.md](009-canto-08.md) | VIII | 92–103 | Era già l' ora che volge il disio | Diagram (d) in the notes |
| [010-canto-09.md](010-canto-09.md) | IX | 104–115 | La concubina di Titone antico |  |
| [011-canto-10.md](011-canto-10.md) | X | 116–125 | Poi fummo dentro al soglio della porta, |  |
| [012-canto-11.md](012-canto-11.md) | XI | 126–137 | “O Padre nostro, che nei cieli stai, |  |
| [013-canto-12.md](013-canto-12.md) | XII | 138–149 | Di pari, come buoi che vanno a giogo, |  |
| [014-canto-13.md](014-canto-13.md) | XIII | 150–163 | Noi eravamo al sommo della scala, |  |
| [015-canto-14.md](015-canto-14.md) | XIV | 164–177 | “Chi è costui che il nostro monte cerchia, |  |
| [016-canto-15.md](016-canto-15.md) | XV | 178–189 | Quanto tra l' ultimar dell' ora terza |  |
| [017-canto-16.md](017-canto-16.md) | XVI | 190–201 | Buio d' inferno e di notte privata |  |
| [018-canto-17.md](018-canto-17.md) | XVII | 202–213 | Ricorditi, lettor, se mai nell' alpe |  |
| [019-canto-18.md](019-canto-18.md) | XVIII | 214–227 | Posto avea fine al suo ragionamento |  |
| [020-canto-19.md](020-canto-19.md) | XIX | 228–241 | Nell' ora che non può il calor diurno | Table: the Malaspina family |
| [021-canto-20.md](021-canto-20.md) | XX | 242–257 | Contra miglior voler voler mal pugna: |  |
| [022-canto-21.md](022-canto-21.md) | XXI | 258–269 | La sete natural che mai non sazia, |  |
| [023-canto-22.md](023-canto-22.md) | XXII | 270–283 | Già era l' angel retro a noi rimaso, |  |
| [024-canto-23.md](024-canto-23.md) | XXIII | 284–295 | Mentre che gli occhi per la fronda verde |  |
| [025-canto-24.md](025-canto-24.md) | XXIV | 296–309 | Nè il dir l' andar, nè l' andar lui più lento |  |
| [026-canto-25.md](026-canto-25.md) | XXV | 310–321 | Ora era onde il salir non volea storpio, |  |
| [027-canto-26.md](027-canto-26.md) | XXVI | 322–333 | Mentre che sì per l' orlo, uno innanzi altro, |  |
| [028-canto-27.md](028-canto-27.md) | XXVII | 334–347 | Sì come quando i primi raggi vibra |  |
| [029-canto-28.md](029-canto-28.md) | XXVIII | 348–361 | Vago già di cercar dentro e dintorno |  |
| [030-canto-29.md](030-canto-29.md) | XXIX | 362–377 | Cantando come donna innamorata, | Map of Upper and Central Italy |
| [031-canto-30.md](031-canto-30.md) | XXX | 378–391 | Quando il settentrion del primo cielo, |  |
| [032-canto-31.md](032-canto-31.md) | XXXI | 392–403 | “O tu, che sei di là dal fiume sacro,” |  |
| [033-canto-32.md](033-canto-32.md) | XXXII | 404–417 | Tanto eran gli occhi miei fissi ed attenti |  |
| [034-canto-33.md](034-canto-33.md) | XXXIII | 418–431 | “*Deus, venerunt gentes*” alternando, |  |

### End matter

| File | Section | Pages |
|---|---|---|
| [035-note-on-dantes-purgatory.md](035-note-on-dantes-purgatory.md) | Note on Dante’s Purgatory (Wicksteed) | 432–434 |
| [036-the-chronology-of-the-purgatorio.md](036-the-chronology-of-the-purgatorio.md) | The Chronology of the “Purgatorio” | 435–437 |
| [037-general-editorial-note.md](037-general-editorial-note.md) | General editorial note (I. G.; no heading printed) | 439 |
| [038-translators-note.md](038-translators-note.md) | Translator’s Note (T. O.) | 440 |
| [039-editorial-note.md](039-editorial-note.md) | Editorial Note (H. O.) | 441 |
| [040-index-to-plates-tables-etc.md](040-index-to-plates-tables-etc.md) | Index to Plates, Tables, etc., and the printer’s imprint | 442–443 |
