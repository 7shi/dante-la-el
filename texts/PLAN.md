# Plan: reorganizing the OCR into `texts/`

The page-by-page transcriptions in `ocr/{dir}/NNN.txt` are reorganized into section files `texts/{dir}/{03d}-{title}.md`, where `{dir}` is the `ocr/` directory name (`en`, `en-oelsner`, `la`, `grc`).

## Status

| Directory | Status |
|---|---|
| `texts/en/` | Done: converted, verified against dante-corpus, footnote markers restored on every page. |
| `texts/en-oelsner/` | Not started. |
| `texts/la/` | Not started; the missing Italian column must be retranscribed in `ocr/la/` first. |
| `texts/grc/` | Not started. |

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
- **Verse**: the print sets each tercet with the 2nd and 3rd lines indented and no blank line between tercets (see `062.png`). This is reproduced with `&emsp;` indentation and hard line breaks (`\`) inside one block per page. The printed verse numbers (every 5th line, omitted in `ocr/`) are computed by counting lines from the start of the canto and added as `<!-- 5 -->` comments, which also checks that no verse is missing.
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
4. **Footnote markers**: restored on every page with notes, checked by the script (each note referenced once on its page) and by spot checks against the images. Three notes have no printed marker and are added by the script (pp. 78, 179, 375).


## `texts/en-oelsner/` — Temple Classics edition (`ocr/en-oelsner/`, 1903)

Structure reference: [`ocr/en-oelsner/INDEX.md`](../ocr/en-oelsner/INDEX.md). The leaf with pp. 385–386 (Canto XXXIV) is missing from the scan.

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

- **Facing pages**: Italian on even pages, English on odd pages, aligned tercet by tercet. Pages stay in order (Italian page, then English page), so each spread reads as Italian followed by its English.
- **Argument**: printed across the tops of the first spread (p. 2 and p. 3). It is kept as one `## Argument` at the head of the file with the `p. 3` marker inside it, and the Italian of p. 2 follows. This is the one place where print order is relaxed, because splitting the summary around 21 verses would break it.
- **Verse**: tercets with lines 2–3 indented, as in `texts/en`. The printed tercet numbers (`(7)`, `(10)`, …, at the first line of each tercet) are kept as `<!-- 7 -->` comments.
- **English**: one paragraph per tercet, as printed.
- **Marginal labels** (`Proemio`, `Selva oscura`, `Dante`, `The Leopard`) are printed text and are kept, as a bold label at the start of the line or paragraph they stand beside (`**Il Colle** Ma poi ch' io fui …`).
- **Notes** are endnotes keyed to verse numbers (`73-75. …`), printed after the canto. They stay as plain paragraphs under the printed `NOTES` heading (`## Notes`); no footnote syntax.
- **Maps, plates, tables** are kept where they are printed, with their transcribed text.
- **Missing leaf**: `<!-- pp. 385–386 missing from the scan -->` between `396` and `397`.

### Conversion notes for `ocr/en-oelsner/`

- Lines are broken as printed, with line-end hyphenation (`de-` / `serted`, `014`); the script joins them.
- Running heads and page numbers are transcribed (`CANTO I` on `015`, page number `2` at the end of `014`); the script removes them. Some are misread (`CANTO I II` on `023`, `206 INFERNO` for 266 on `278`), so they are recognized by position (first and last line of the page), not by an exact pattern.
- Marginal labels are marked `**…**` on the Italian pages but run into the line on the English pages (`I [came Dante` / `to] myself` on `015`; `017`). The English ones are misreadings for the script's purpose and are corrected in `ocr/` to the Italian pages' form.
- The `NOTES` heading is often merged with the page number (`12 NOTES` on `024`), and only 28 of the 34 cantos have it in the transcription; the investigation names `047`, `091`, `101`, `111`, `201`, `392` as pages where the notes begin without it. Check these against the images.
- Unlike `ocr/en`, italics are transcribed as `*…*` (146 files). They are kept as they are.

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

The canto ranges come from INDEX.md. The script takes them from there; the blank-page lists in the investigation report contradict INDEX.md and are not used. Blank pages (62, all `[Blank page]`) and `0001`–`0006`, `1291`–`1296` are excluded. Slugs use the English cantica names, as the policy requires. Section titles of the front matter are left in the original language where there is no plain English equivalent (`notizie-preliminari`, `documenta`).

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

Structure reference: [`ocr/grc/INDEX.md`](../ocr/grc/INDEX.md).

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
- **Verse**: twelve-syllable lines, not set in tercets and not indented (`022.png`). They stay one per line with hard line breaks. The printed line numbers (every 5th line, transcribed at the start of the line) move to `<!-- 5 -->` comments at the line end.
- **Notes**: one file, as printed: a continuous back section in which a canto's notes can start in the middle of a page (`292`, `293`, `299`). Per-canto headings (`Εἰς ᾨδὴν Α΄.`) become `##`. Notes are paragraphs keyed to line numbers. The few asterisk footnotes inside the notes (`289`, `343`) use `[^{page}-{n}]` labels.

### Conversion notes for `ocr/grc/`

- Running heads with page numbers are transcribed (`2 ΩΔΗ Α΄` on `022`); the script removes them.
- Prose (argument, prologue, notes) is broken as printed, with line-end hyphenation (`τριακονταπενταε-` / `τῆς`, `289`); the script joins it. Verse lines are kept as they are.
- The script drops the library stamps on `001` and `351`.

## Order of work

1. `texts/en`: write the conversion script and generate the files. **Done.**
2. Extend the script for `en-oelsner` and `grc` (line joining, hyphenation, running heads), correcting the misreadings listed above in `ocr/`, one directory at a time.
3. `la`: retranscribe the missing Italian column in `ocr/la/`, then convert.
