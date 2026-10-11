# Plan: reorganizing the OCR into `texts/`

The page-by-page transcriptions in `ocr/{dir}/NNN.txt` are reorganized into section files `texts/{dir}/{03d}-{title}.md`, where `{dir}` is the `ocr/` directory name (`en`, `en-oelsner`, `la`, `grc`).

## Status

| Directory | Status |
|---|---|
| `texts/en/` | Done: converted, verified against dante-corpus, footnote markers restored on every page. |
| `texts/en-oelsner/` | Done: `ocr/` normalized (labels, paragraph breaks) and converted; Italian verified against dante-corpus, English against `texts/en`. |
| `texts/la/` | Next: the missing Italian column must be retranscribed in `ocr/la/` first. |
| `texts/grc/` | Done: converted; verse counts, line numbers, and arguments checked by the script; misreadings found by a syllable count corrected in `ocr/`. |

## General policy

- **Follow the book.** Each file corresponds to a section of the printed book, in book order, and the content inside a file keeps the order in which it is printed. Nothing is moved into a different place for convenience (for example, all notes gathered at the end of a canto).
- **Linearize what Markdown cannot lay out.** Markdown has no columns or page areas, so the page is read top to bottom: prose → verse → verse notes → footnotes. The page remains the unit, and page boundaries are kept as markers.
- **Do not change the text.** Spellings, accents, and punctuation stay as transcribed in `ocr/`. Only layout-induced artifacts (words hyphenated across pages, footnotes split across pages) are resolved.
- **Traceability.** Every page starts with `<!-- p. N (NNN) -->`, giving the printed page number (`[N]` if unnumbered, Roman for front matter) and the scan number, so text can be checked against `ocr/{dir}/NNN.png`.
- **Physical-copy material is excluded**: covers, bookplates, flyleaves, tissue guards, blank pages, bound-in publisher's advertisements, library stamps, shelfmarks, loan slips, barcodes, and digitization inserts. A stamp transcribed on a page with printed text is removed from that page only.
- **Half-titles** belong to the section they introduce and open its file.
- **Headings** are the printed headings, in title case (`CANTO I.` → `# Canto I`). No heading is invented where the book prints none.
- **`ocr/` is left as it is.** Each directory keeps its own transcription conventions, and lines may stay broken where the print breaks them. The conversion script handles each directory's conventions: joining lines into paragraphs, removing line-end hyphenation, and dropping running heads and page numbers. Only misreadings (wrong or missing text) are corrected in `ocr/`, against the images.
- **Line-end hyphens** are ambiguous: `She-` / `wolf` keeps its hyphen, `de-` / `serted` does not. The script decides with a word list built from the same directory (a form that occurs unbroken elsewhere) and lists the undecided cases for review.
- **Slugs** are lowercase kebab-case English (`canto-01`, `index-of-proper-names`). File numbers are three digits, sequential in book order; the canto number is in the slug, not in the file number.

## `texts/en/` — Carlyle's edition (`ocr/en/`, 1889)

Done. Contents and reading notes: [`en/README.md`](en/README.md). Structure reference: [`ocr/en/INDEX.md`](../ocr/en/INDEX.md). Transcription conventions: [`ocr/en/README.md`](../ocr/en/README.md).

### Files

| File | Section (heading as printed) | Scans |
|---|---|---|
| `001-title-page.md` | Half-title, frontispiece, title page, imprint | `005`, `006`, `009`, `010` |
| `002-preface-first-edition.md` | PREFACE TO THE FIRST EDITION. | `011`–`018` |
| `003-preface-second-and-third-editions.md` | PREFACE TO THE SECOND EDITION. / PREFACE TO THE THIRD EDITION. | `019` |
| `004-manuscripts-and-editions.md` | MANUSCRIPTS AND EDITIONS. | `021`–`031` |
| `005-comments-and-translations.md` | COMMENTS AND TRANSLATIONS. | `032`–`046` |
| `006-the-inferno-of-dante.md` | THE INFERNO OF DANTE. | `047`–`054` |
| `007-canto-01.md` … `040-canto-34.md` | CANTO I. … CANTO XXXIV. (file number = canto + 6) | `055`–`476`, see INDEX.md |
| `041-index-of-proper-names.md` | INDEX OF PROPER NAMES. | `477`, `479`–`486` |

Excluded: `001`–`004`, `007`, `008`, `020` (blank), the 9 blank versos inside the cantos (`146`, `184`, `210`, `284`, `298`, `312`, `398`, `412`, `426`), `478`, `487`–`510` (Bohn's catalogue), `511`–`514`.

Closing lines are part of the text and are kept: `END OF THE INFERNO.` (end of canto 34) and `THE END.` with the Chiswick Press colophon (end of the index).

### Canto file layout

```markdown
# Canto I

<!-- p. [1] (055) -->

## Argument

Dante finds himself astray in a dark Wood, …

<!-- p. 2 (056) -->

In the middle[^2-1] of the journey of our life, I found myself in a dark wood;[^2-2] for the straight way was lost. …

Nel mezzo del cammin di nostra vita\
&emsp;Mi ritrovai per una selva oscura,\
&emsp;Chè la diritta via era smarrita.\
Ahi quanto a dir qual era è cosa dura\
&emsp;Questa selva selvaggia ed aspra e forte,\
&emsp;Che nel pensier rinnova la paura! <!-- 5 -->\
…

[^2-1]: The action of the poem begins on Good Friday of the year 1300, …

[^2-2]: In “the erroneous wood of this life” …

<!-- p. 3 (057) -->
…
```

- **Headings**: `# Canto I` (from `CANTO I.`), `## Argument` (from `ARGUMENT.`). Other files use the printed section title as `#`, in title case.
- **Prose**: one paragraph per line, as in `ocr/`. A paragraph that runs over a page is left split at the page marker, as in print; a word hyphenated across the page break is joined on the earlier page (`Grey-` / `hound` → `Greyhound` on `063`).
- **Verse**: the print sets each tercet with the 2nd and 3rd lines indented and no blank line between tercets (see `062.png`). This is reproduced with `&emsp;` indentation and hard line breaks (`\`) inside one block per page. The printed verse numbers (every 5th line, omitted in `ocr/`) are computed by counting lines from the start of the canto and printed at the line end as in the book (`… muova, 5`), which also checks that no verse is missing; the text has no numbers that they could be confused with.
- **Verse notes** (`1. Bruno, brown, …`, printed below the verse) are kept as a paragraph after the verse block, unchanged.
- **Footnotes** keep the book's per-page numbering. Labels are `[^{page}-{n}]` (`[^8-2]` = note 2 on p. 8), so they don't collide and still identify the printed note. Definitions follow their page's verse, as at the foot of the page. A note continued on the next page (the unnumbered block at the top of that page's notes) is appended to its definition on the starting page, joining any hyphenated word (`promi-` / `nent`, `084`→`085`).
- **Footnote markers** in the prose were omitted in `ocr/`. They are restored in `ocr/` as superscript digits at the printed position (`author.²` on p. 8, as already on `148`), which the script turns into references (`[^8-2]`). A marker missing in the print itself (note 2 on p. 78, `132`; note 1 on p. 179, `233`; note 1 on p. 375, `429`) is added by the script (`ADDED_MARKERS`), not in `ocr/`. The script lists pages whose notes are not referenced yet.
- **Italics** in the print (titles, Latin and Italian quotations in notes) are not transcribed in `ocr/` and are not added in this pass.

### Other files

Front matter and the index use the same page markers and footnote labels. Roman page numbers are written as printed (`<!-- p. xiii (019) -->`). The index keeps one entry per line, with each entry ending in a hard line break.

### Procedure

1. **Script**: [`convert_en.py`](convert_en.py) (`uv run texts/convert_en.py`). It classifies the blocks on each page (prose, verse, verse notes `^\d+\. `, footnotes `^\d+ `, unnumbered continuation), telling Italian verse from short English lines by common function words, and writes the files with page markers, verse indentation and numbers, footnote labels, and merged continuations. It checks the verse count of each canto against the standard text, the footnote numbering of each page, and that every note is referenced once from its page, and lists the hyphen joins it could not decide from the vocabulary (8 cases, all checked).
2. **Irregularities found during the investigation**, all handled by the script:
   - Tercets are sometimes separated by blank lines against the `ocr/en` convention (`062`, `069`, `070`, `080`, `081`, …). The script does not depend on blank lines inside the verse.
   - Notes containing blank lines (multi-paragraph notes, quoted verse such as Milton in `060`, `061`, `282`) must not be split into separate notes: a block without a leading number belongs to the preceding note.
   - Pages without footnotes (`078`, `087`, `088`, `200`, `331`, `452`, `457`) and pages with only a continued note (`454`, `456`).
   - Hyphenated words across pages, in prose (about 26 cases) and in notes (`084`→`085`, `233`→`234`, `281`→`282`).
   - Lines starting with a number followed by a period inside footnotes, which must not be taken as verse notes.
3. **Verify**: the verse lines of each canto are compared line by line with the Italian text of [dante-corpus](https://github.com/7shi/dante-corpus) (`src/inferno/NN.txt`, one verse per line). For `texts/en` all 4,720 lines align; the five lines below 0.75 similarity (letters only, accents removed) are readings of this edition (e.g. XXIII 63 *in Cologna* / *in Clugnì*), not misplaced lines. Every footnote of `ocr/` appears once.
4. **Footnote markers**: restored on every page with notes, checked by the script (each note referenced once on its page), by confirming that removing the superscript digits from `ocr/en/` gives back the previous text (nothing else changed), and by spot checks against the images. Three notes have no printed marker and are added by the script (pp. 78, 179, 375).


## `texts/en-oelsner/` — Temple Classics edition (`ocr/en-oelsner/`, 1903)

Done. Contents and reading notes: [`en-oelsner/README.md`](en-oelsner/README.md). Structure reference: [`ocr/en-oelsner/INDEX.md`](../ocr/en-oelsner/INDEX.md). The leaf with pp. 385–386 (Canto XXXIV) is missing from the scan.

### Files

| File | Section | Scans |
|---|---|---|
| `001-title-page.md` | Series half-title, publishing history, frontispiece, title page, epigraph | `007`, `008`, `010`, `011`, `013` |
| `002-canto-01.md` … `035-canto-34.md` | CANTO I … CANTO XXXIV (file number = canto + 1), each with its notes and the maps, plates, or tables printed after it | `014`–`402`, see INDEX.md |
| `036-note-on-dantes-hell.md` | NOTE ON DANTE’S HELL | `403`–`405` |
| `037-the-chronology-of-the-inferno.md` | THE CHRONOLOGY OF THE “INFERNO” | `406`–`408` |
| `038-plan-of-concentric-spheres.md` | Plate | `409` |
| `039-section-of-the-universe.md` | Plate | `410` |
| `040-editorial-note.md` | EDITORIAL NOTE | `411` |
| `041-index-to-maps-plates-and-tables.md` | INDEX TO MAPS, PLATES AND TABLES | `412` |

Excluded: `001`–`006`, `009`, `012`, `413`–`416`.

### Layout

- **Spreads**: Italian on even pages, English on odd pages, aligned tercet by tercet; each English page translates exactly the tercets of the facing Italian page. Markdown cannot set the two pages side by side, so a spread is read band by band: what is printed across the top of both pages, then the Italian page, then the English page, then what is printed across the bottom of both pages. A page that appears in a second band gets its marker again with the band named (`<!-- p. 2 (014), text -->`, `<!-- p. 10 (022), notes -->`).
- **Argument**: printed across the top of the first spread (p. 2 and p. 3). It comes first, under `## Argument` (not printed; the book has no heading), with both page markers, followed by the text band of the same spread.
- **Verse**: tercets with lines 2–3 indented, as in `texts/en`. The printed tercet numbers (`4`, `7`, … at the first line of each tercet) are transcribed inconsistently in `ocr/` (at the line end, as `(7)`, as superscripts, as a column after the verse, sometimes misplaced or misread), so the script removes them and computes them by counting lines from the start of the canto, and prints them as plain numbers at the line end (`… fianco 4`), as in the book; the text has no numbers that they could be confused with. The canto's last line, set alone, is translated in the last English tercet paragraph.
- **English**: one paragraph per tercet, as printed.
- **Marginal labels** are the editor's sidenotes, not part of the text: on the Italian pages the place in Hell (`Proemio`, `Vestibolo`, `Cerchio VIII. Bolgia 3`, repeated at the top of each page) and occasional scenes (`Selva oscura`, `Il Colle`); on the English pages the subject or speaker (`Dante and Virgil`, `The Leopard`, `Charon`). They are kept out of the text as machine-readable comments at the end of the verse line or English paragraph they stand beside (`… giunto, 13 <!-- label: Il Colle -->`), one comment per label, including the repetitions at the top of each page. Their rendering can be changed later by processing these comments.
- **Notes** are keyed to verse numbers (`73-75. …`) and begin right after the canto's last verse, running across the bottoms of the remaining pages and over whole pages. The book prints no heading for them (`NOTES` is only the running head of the pages of notes); `## Notes` is added at their start, after the text band of the spread where they begin. They stay plain paragraphs, no footnote syntax. A paragraph running over a page is joined on the earlier page.
- **Maps, plates, tables** are kept where they are printed, with their transcribed text line by line. The *Section of Malebolge* diagram on p. 272 (`284`) has no text.
- **Missing leaf**: `<!-- pp. 385–386 missing from the scan -->` between `396` (p. 384, Italian vv. 19–51 of Canto XXXIV) and `397` (p. 387, English vv. 52–84).

### Conversion notes for `ocr/en-oelsner/`

- Script: [`convert_en_oelsner.py`](convert_en_oelsner.py) (`uv run texts/convert_en_oelsner.py`). It is separate from `convert_en.py`: the two books share little beyond hyphen handling and title case.
- Lines are broken as printed, with line-end hyphenation (`de-` / `serted`, `014`); the script joins them, deciding with a word list from `ocr/en-oelsner` and `ocr/en` (the same translation), from which the fragments of hyphenated words are excluded, and lists the undecided cases. The cases decided by hand against the images and `ocr/en` are in `HYPHEN_FIXED` (`re-erected`, `father-in-law`, `praiseworthy`, …); an undecided case that looks like no word (`ap-` / `have`) is a misreading to correct in `ocr/`.
- Running heads and page numbers are transcribed (`CANTO I` on `015`, `8` / `INFERNO` on two lines on `020`, page number `2` at the end of `014`), and so are the printer's signature marks at the foot of some pages (`B` on `029`, `2 C` on `411`); the script removes them. Some heads are misread (`CANTO I II` on `023`, `206 INFERNO` for 266 on `278`, `V. NOTES` on `284`), so they are recognized by position (first lines and last line of the page), not by an exact pattern.
- `ocr/` is normalized so that the script can tell the layers apart (all against the images; delegated, then checked):
  - Marginal labels: written once, whole, as `**Label**` at the start of the line where the label begins. In the transcription they had run into the line ends on the English pages (`I [came Dante` / `to] myself` on `015`), stood unmarked at the line start or on lines of their own on most Italian pages (`Cerchio` / `VIII.` / `Bolgia 3`), or were set bold only in places.
  - Other bold (drop capitals, first words, running heads) is removed.
  - English paragraph breaks (Argument, tercets, notes) are blank lines; they were missing on most pages, which made the tercets impossible to tell apart.
  - Transcriber's notes that are not printed (`Line numbers on the right:`, `*Side notes*:` with a list of the labels, `*Map 1: …*`, `*Caption below maps:*`, marker asterisks in the genealogical tables) are deleted; `[Blank page]` stays, as the pages it marks are not converted.
- Checks: the words of each normalized page are compared with the previous version (only `**`, label moves, and blank lines may differ); the Italian lines are compared with dante-corpus (labels left in the line or misread lines show up as mismatches); the English is compared with `texts/en` (Carlyle's own edition of the same translation), where every difference must be an Oelsner revision (`[came to]`) or a variant, not a stray label; the number of English paragraphs on each page is compared with the number of tercets that begin on the facing Italian page (one fewer on a canto's last page). The script reports as errors a canto whose verse count is wrong, a numbered note among the English tercets, and a note running over from an Italian page whose continuation is not found on the English page; on a canto's last page a missing paragraph break otherwise lets the next note fill the last tercet's place unnoticed. It lists note paragraphs that start after an unfinished sentence and English pages whose notes start without a verse number (normally a continued note). The first note paragraph of a page after a finished sentence is a new paragraph unless the page is in `NOTE_CONTINUED` (flush left in the image, `189`, `356`); the pages checked as new paragraphs are in `NOTE_NEW`.
- Unlike `ocr/en`, italics are transcribed, mostly as `*…*` and on some pages as `_…_`. They are kept as they are, except on `411`, which is printed in italics with the names in roman; the transcription marked a few sentences at random, so the marks were removed there.

## `texts/la/` — Serravalle's translation and commentary (`ocr/la/`, 1891)

Structure reference: [`ocr/la/INDEX.md`](../ocr/la/INDEX.md). The volume covers the whole *Comedy*.

### Files

| File | Section | Scans |
|---|---|---|
| `001-title-page.md` | Half-title, title page, imprimatur | `0007`, `0009`, `0010` |
| `002-dedication-to-leo-xiii.md` | A SUA SANTITÀ PAPA LEONE XIII | `0011`, `0013`, `0014` |
| `003-notizie-preliminari.md` | NOTIZIE PRELIMINARI | `0015`–`0042` |
| `004-documenta.md` | DOCUMENTA (half-title and documents I–XI) | `0043`, `0045`–`0054` |
| `005-dedicatio.md` | Comentum half-title; dedication to the English bishops | `0055`, `0057` |
| `006-epistola.md` | Epistle to Cardinal Amideus | `0059`, `0060` |
| `007-preambula.md` | Preambula to the whole work | `0061`–`0077` |
| `008-inferno-canto-01.md` … `041-inferno-canto-34.md` | Inferno I–XXXIV | `0079`–`0477` |
| `042-purgatorio-preambula.md` | Preambula to Purgatorio | `0479`–`0486` |
| `043-purgatorio-canto-01.md` … `075-purgatorio-canto-33.md` | Purgatorio I–XXXIII | `0487`–`0869` |
| `076-paradiso-canto-01.md` … `108-paradiso-canto-33.md` | Paradiso I–XXXIII (the PARADISUS half-title `0871` opens canto 1) | `0871`–`1270` |
| `109-appendix.md` | Appendix: Bartholomaeus a Colle | `1271`, `1273`–`1287` |
| `110-index.md` | INDEX (the printed table of contents) | `1289`, `1290` |

The canto ranges and blank pages come from INDEX.md; lists of blank versos compiled elsewhere contradicted it and are not used. Blank pages (62, all `[Blank page]`) and `0001`–`0006`, `1291`–`1296` are excluded. Slugs use the English cantica names, as the policy requires. Section titles of the front matter are left in the original language where there is no plain English equivalent (`notizie-preliminari`, `documenta`).

### Layout

Each canto has the Latin *Summarium*, then pages with the verse in two columns at the top and the Latin *Comentum* in two columns below, and at the end a modern Italian essay by the editors.

- **Verse**: the Italian (left column) and Serravalle's Latin (right column) are aligned tercet by tercet with the same tercet number. They are interleaved per tercet: the Italian tercet, then the Latin tercet, each starting with its printed number (`¹`). This keeps the visible correspondence that two columns give.
- **Commentary**: the left column, then the right column, one paragraph per line. The separators between glosses (short rules) become `---`.
- **Essay**: kept at the end of the canto file under its printed title (`## La divina commedia`).
- **Footnotes** occur in the Italian front matter and essays (`(1) …`) and use the `[^{page}-{n}]` labels.

### Conversion notes for `ocr/la/`

- **The Italian verse column is missing from many pages.** Of the canto pages with numbered tercets, 255 contain both columns and 199 only the Latin (`0083` has only the Latin; the image shows both). The missing column is missing text, so it is transcribed again in `ocr/` before conversion. Pages without numbered tercets (738) need a check of how their verse is numbered (`0099` has line numbers instead).
- Lines are broken as printed, with line-end hyphenation (`dividi-` / `tur`, `0081`); the script joins them.
- `CAPITULUM PRIMUM` at the top of most pages is the running head (with the page number on `0083.png`); on a canto's first text page (`0081`) it may be the printed heading. Check against the images.

## `texts/grc/` — Musurus's Greek translation (`ocr/grc/`, 1882)

Done. Contents and reading notes: [`grc/README.md`](grc/README.md). Structure reference: [`ocr/grc/INDEX.md`](../ocr/grc/INDEX.md).

### Files

| File | Section | Scans |
|---|---|---|
| `001-title-page.md` | English title page, imprint, Greek title page | `001`–`003` |
| `002-prologos.md` | ΠΡΟΛΟΓΟΣ | `005`–`007` |
| `003-table-of-contents.md` | ΠΙΝΑΞ ΤΩΝ ΕΝ ΕΚΑΣΤΗι ΩΔΗι ΠΕΡΙΕΧΟΜΕΝΩΝ | `009`–`013` |
| `004-corrigenda.md` | ΠΑΡΟΡΑΜΑΤΩΝ ΔΙΟΡΘΩΣΙΣ | `014` |
| `005-corrigenda-extended.md` | Διορθώσεις παροραμάτων … (separately paginated 1–4) | `015`–`018` |
| `006-canto-01.md` … `039-canto-34.md` | ΩΔΗ Α΄ … ΩΔΗ ΛΔ΄; the half-title `019` opens canto 1 | `019`, `021`–`285` |
| `040-notes.md` | ΣΗΜΕΙΩΣΕΙΣ, with half-title | `287`, `289`–`351` |

Excluded: `004`, `008`, `020`, `286`, `288`, and the library stamps transcribed on `001` and `351`.

### Layout

- **Canto**: heading `# ᾨδὴ Α΄` (as printed, `ΩΔΗ Α΄.`), then the printed argument as a plain paragraph (no `## Argument`, since the book prints none), then the verse.
- **Verse**: twelve-syllable lines, not set in tercets and not indented (`022.png`). They stay one per line with hard line breaks. The translation is line for line: Greek line *n* renders Italian verse *n*, so every canto has exactly the verse count of the Italian (136, 142, …). The printed line numbers (every 5th line, at the start of the line) are transcribed there, but some are misplaced or misread (`35` before `30` on `038`); as in `texts/en` and `texts/en-oelsner`, the script removes them, computes the numbers by counting lines, and prints every 5th at the line end (`… στυγήρης, 5`). The removed numbers are kept for checking.
- **Notes**: one file, as printed: a continuous back section in which a canto's notes can start in the middle of a page (`292`, `293`, `299`). Per-canto headings (`Εἰς ᾨδὴν Α΄.`) become `##`. Notes are paragraphs keyed to line numbers. The few asterisk footnotes inside the notes (`289`, `343`) use `[^{page}-{n}]` labels.

### Conversion notes for `ocr/grc/`

- Running heads with page numbers are transcribed in several forms: `2 ΩΔΗ Α΄` (`022`), `ΩΔΗ Α΄.` / `3` on two lines (`023`), `ΩΔΗ Γ΄. 19` (`039`); on the notes pages the head names the canto whose notes the page carries (`272` / `Εἰς ᾨδὴν Α΄.` on `292`, `Εἰς ᾨδὴν Β΄. 273` on `293`), which looks like the per-canto heading `Εἰς ᾨδὴν Β΄.` printed in the middle of `292`. Heads are recognized by position (the first lines of the page), as in `en-oelsner`. Printer's signature marks at the foot of some pages (`Β΄ 2` on `023`) are removed too.
- The argument is not always separated from the verse by a blank line (`075`). The printed table of contents (`009`–`013`) repeats every argument, so the script can find where the argument ends by comparing with it, and report a canto whose argument differs.
- Prose (argument, prologue, notes) is broken as printed, with line-end hyphenation (`τριακονταπενταε-` / `τῆς`, `289`); the script joins it, with a word list from `ocr/grc` and a list of undecided cases, as for `en-oelsner`. Verse lines are kept as they are; the quotation marks that open continued speech at the line start (`„ Ἔλαχον`, `038`) are printed and stay.
- Notes: each note starts with its line number and an indented first line (`105. Δηλαδὴ …`, `292.png`). The transcription separates them by blank lines on some pages (`289`) and not on others (`292`), so the script starts a note at a line beginning with a line number and a period; lines inside a note that begin with a number (`15)· ἁρπαγεὶς …`, `292`) must not match, and unnumbered paragraphs inside a note are reported for checking against the images. A note continued on the next page is joined to its start.
- The script drops the library stamps: `ΠΑΝΕΠΙΣΤΗΜΙΟ ΚΡΗΤΗΣ` (last line of `001`) and `ΒΙΒΛΙΟΘΗΚΗ` / `ΙΩΑΝΝΟΥ` / `ΚΑΛΙΤΣΟΥΝΑΚΗ` (between `ΤΕΛΟΣ ΤΩΝ ΣΗΜΕΙΩΣΕΩΝ.` and the printer's line on `351`).
- Script: [`convert_grc.py`](convert_grc.py) (`uv run texts/convert_grc.py`). Findings from the conversion:
  - The numeral sign is transcribed in several forms (`΄`, `´`, `ʹ`, `’`, …); heads written with `ʹ` (`ΩΔΗ Δʹ.` on `048`) had been counted as verse in the rough count. The ornamental rules around the arguments (`245.png`) are dropped.
  - A long line whose end does not fit is set on the next line, indented (`ῥίπτεις ; ”` on `069`): a short line starting in lowercase is joined to the line before it (11 cases, listed by the script). With the heads and these runovers handled, all 34 cantos have the Italian verse count and every printed line number stands at its line, so no line is missing or doubled.
  - Arguments that differ from the table of contents are listed; the three that remain are printed so (`ARG_CHECKED`: `αἱρετικοί—` / `αἱρετικοί.—`, `μετὰ` / `κατὰ`, `ἔννατον` / `ἕνατον`). The other differences were misreadings of the table (`Σίμων` for `Σίνων`, `ἀλχημισταί` for `ἀλχυμισταί`, …).
  - The checks do not catch misreadings inside a line, and the transcription tends to replace rare forms with common ones (`λυπηρὸς` for `λυπρὸς`, `βραχέως` for `βραγχῶς`, `πρόνοος` for `πρόνους`, `Ἅδου` for the printed `ᾍδου` throughout; the upper dot also appeared as `˙` and `•`, now `·`). Counting syllables (a vowel group with the diphthongs counted once) finds those that change the metre: of the 4720 lines, 40 did not have twelve; 33 were misreadings and are corrected in `ocr/`, and the 7 left are printed so, some listed in the corrigenda (`ΚΔ΄` 128 and 133, `Λ΄` 137, `ΛΓ΄` 52). Misreadings that keep twelve syllables may remain.
  - Notes pages: the page number is removed from the head; the label is the running head unless it names the next canto, then it is the heading of that canto's notes printed at the top of the page (`303`, `318`, `326`, `347`). Misprinted heads are in `HEAD_MISPRINTED`. A note starts with a number that is higher than the last note and within the canto's verse count; `1300.` at a line start on `318` is a year inside a note (`NUMBER_CHECKED`).
  - Quotations in verse set off inside the notes are listed by their first words in `NOTE_VERSE`; the unnumbered paragraphs checked against the images are in `NOTE_UNNUMBERED`.
  - Line-end hyphens: Greek words are always joined (the print hyphenates Greek by syllables); the others are decided by hand in `HYPHEN_FIXED`.
- Decisions to review if the conventions change (all checked against the images; only the first departs from the print):
  - `ΛΒ΄` 86 (`265`): the `Ε` of `Εἶπον` did not print. `ocr/` has the printed `ἶπον`; the script writes `Εἶπον` (`MISSING_TYPE`), with the capital that starts every line; without it the line would start with a lowercase `ἶ`.
  - `ΙΖ΄` 92 (`147`): `(ἀλλ οὐ,` without an apostrophe, as printed; `ocr/` and the output keep it.
  - Line-end hyphens outside Greek (`HYPHEN_FIXED`): `veuil-je` and `ci-dessus` keep the hyphen (as `ferois-je`, `fait-elle`); `porce-` / `que` is joined as `porceque` (as `porque` in the same sentence), though Old French also writes `por ce que`.
  - Quotations in verse inside the notes (`NOTE_VERSE`, 11) keep their printed lines with hard breaks, also inside a numbered note (`301`, `309`, `332`); a verse quotation set after a blank line is part of the note it is quoted in.
  - The running heads `Ε΄` on `298` and `299` are misprints for `ΣΤ΄` (`HEAD_MISPRINTED`); `Ἀσδέντης` on `324` is an indented paragraph of note 118 without a number.

### Procedure for `grc`

All steps are done; the findings are in the conversion notes above.

1. **Script** `convert_grc.py`: page reading (heads, signature marks, stamps), the canto files (argument, verse, computed line numbers), the notes file (per-canto headings, notes split by number, page joins, the asterisk footnotes), and the front matter (prologue, table of contents and corrigenda line by line).
2. **Verse checks**, reported by the script as errors: the line count of each canto against the Italian verse count; each printed line number against the position of its line, which locates an extra or missing line between two numbers (a rough count shows differences in 22 of the 34 cantos, mostly of one or two lines, partly caused by the rough counting itself); each argument against the table of contents.
3. **Corrections in `ocr/grc/`**, against the images: missing or doubled verse lines, misplaced or misread line numbers (only where they hide a misplaced line; the numbers themselves are not used), argument/verse separation, misreadings found by the checks. If the cantos with errors are many, delegate them in batches (see Delegated work) with the error list as input; verify the result with the script's checks and the whole-page comparison.
4. **Notes checks**: every canto has its `Εἰς ᾨδὴν …` heading in order; the note numbers inside each canto increase and do not exceed its verse count; the list of unnumbered note paragraphs is checked against the images.
5. Generate the files, write `texts/grc/README.md` like the other books, update `texts/README.md` and the Status here. Commit `ocr/grc` and `texts` separately.

## Delegated work

Investigation and page-by-page corrections in `ocr/` may be delegated to another agent, but its reports are not reliable: earlier reports contained wrong lists (blank pages of `la`), invented examples (Greek text in the `grc` report), and markup not in `ocr/` (italics). Check every claim against the files, verify edits mechanically where possible (e.g. that only the intended characters were inserted), and open the images only for doubtful places. In the `en-oelsner` normalization the delegate also changed what it was told to leave alone (it deleted blank lines between the Argument, the verse, and the notes on the Italian pages, and moved labels to the wrong line), so compare the whole page, blank lines included, not only the intended kind of edit.

How the delegation is run (via herdr, to the agent `la-el-codex`; replies go to `la-el-claude`):

- Write the task to a file and send one short prompt naming it. Do not poll; the reply arrives as a prompt. Hold corrections for the next task file instead of sending them while the agent works.
- Every task file says: write only the listed files and the report (`tmp/herdr-report-<task>.md`); no commit, push, delete, or rename; stay inside the repository; **no subagents** (their tool calls need manual approval, and herdr drops the agent's name when they run); no git commands that change the repository or use the network (`git diff` / `git status` are fine); questions go back as a prompt, then stop; reply once when done.
- Batches of about ten cantos, after a trial batch of three. Each batch repeats the lessons of the previous ones with page examples.
- Report format: one line per page with the result (labels, paragraph counts, inserted text), then the unusual findings. Tell the agent explicitly not to correct the print and not to fix misreadings it notices, only to list them; then follow every listed item up.
- If herdr shows no name for an agent, list again; the name can drop without the session changing. Restore it with `herdr agent rename <pane> <name>`.

## Order of work

1. `texts/en`: write the conversion script and generate the files. **Done.**
2. `texts/en-oelsner`: normalize `ocr/`, write the conversion script, and generate the files. **Done.**
3. `texts/grc`: see *Procedure for `grc`* above. **Done.**
4. `la`: retranscribe the missing Italian column in `ocr/la/`, then convert. **Next.**
