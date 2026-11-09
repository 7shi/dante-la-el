# Tesseract's word boxes of ocr/grc: the third reading of the comparison and the boxes for
# ocr/scripts/wordcrop.py (ocr/grc/PLAN.md).
# Usage (in this directory): make all, or make 021.tsv; the pages already done are skipped.
# Only the pages of texts/grc are read (the page markers `(021) -->` of its files).
# Tesseract writes its TSV with `-l grc`, and with `-l grc+lat+ita+fra` on the pages of notes
# (287-351), which quote Latin, Italian and French (the other languages misread the Greek of
# the verse: `Kaëaprnpiov` on 021). Only the words are kept, in the columns block_num,
# par_num, line_num, left, top, width, height, text (level, page_num, word_num and conf,
# and the rows of the blocks, paragraphs and lines, are not used).
# TESSERACT is the Windows build under WSL; relative paths, so that it can read and write them.

TESSERACT = /mnt/c/Program Files/Tesseract-OCR/tesseract.exe
PAGES := $(sort $(shell grep -oh '([0-9][0-9][0-9]) -->' ../../../texts/grc/*.md | tr -dc '0-9\n'))
NOTES := $(shell seq 287 351)

.PHONY: all

all: $(addsuffix .tsv,$(PAGES))

%.tsv: ../%.png
	"$(TESSERACT)" $< $*.raw -l $(if $(filter $*,$(NOTES)),grc+lat+ita+fra,grc) tsv
	awk -F'\t' -v OFS='\t' \
	  'NR==1 {print "block_num","par_num","line_num","left","top","width","height","text"; next} \
	   $$1==5 && $$12~/[^ ]/ {print $$3,$$4,$$5,$$7,$$8,$$9,$$10,$$12}' $*.raw.tsv > $@
	rm $*.raw.tsv
