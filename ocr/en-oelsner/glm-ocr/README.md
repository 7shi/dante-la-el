# GLM-OCR reading of `ocr/en-oelsner`

An independent OCR of the Temple Classics Inferno (1903) with GLM-OCR, run locally with
ollama. It is the fourth reading of the check ([../PLAN.md](../PLAN.md), "The readings to
compare"), beside the base, Claude's retype and Tesseract. `cmpread.py -g` uses it as a
vote; its reading alone decides nothing, the image does.

## Pages

- One file per page, `PAGE.txt`, for the 404 pages of `texts/en-oelsner` (`007`–`412`
  without `009` and `012`); the covers, library leaves and blank leaves are not read.
- Run by the user with the [Makefile](Makefile) (`make batch1` … `make batch5`, in page
  order), 2026-11-13. The prompt is `Text Recognition:` with the page image.
- All 404 pages are present.

## The form of the output

- The lines of a paragraph are joined, so the printed line breaks and line-end hyphens
  are lost. The running heads and page numbers are mostly dropped. `cmpread.py`
  compares words, not lines.
- Italics and labels are not marked; a marginal label is set in the text, often away
  from the line where it is printed.

## Habits

These were seen in the trial and the first retypes:

- **Normalized forms**: `Aeneas` for `Æneas`, `Eneid`, accents dropped from the Italian
  (`sicurta`, `si`).
- **Words run together** (`surgewherewith`), and words or periods dropped or added.
- **Run-aways**: a page, a paragraph or a whole table is repeated.
- **Maps**: names dropped or misread, and given in an order of their own.

## Pages outside the length check

`cmpread.py` leaves out a page whose length is not within 1.3 times the base's, and
says so on stderr. After the run, nine pages were outside this range:

- **Run again by the user until within the range**: `248`, `309`, `320` (notes; a
  page or a paragraph repeated), `249`, `321`, `345` (the genealogical tables;
  repeated two or three times). They are now within 0.96–1.0 of the base, with no
  repeated lines.
- **Left out**:
  - `412`, the index to the maps, plates and tables. On every run the reading stops
    after the first entry and its leader dots (0.16 of the base). It is checked with
    Tesseract and the image.
  - `025` and `037`, the maps (0.69 and 1.44 of the base). Their names are dropped,
    misread or repeated in the caption. Running them again would not help: the names of
    a map are read in the image one by one ([../PLAN.md](../PLAN.md), "Settled
    readings").
