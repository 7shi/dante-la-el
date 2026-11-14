# Tesseract's word boxes of ocr/en-purgatorio: a reading of the comparison and the boxes for
# ocr/scripts/wordcrop.py (ocr/en-purgatorio/PLAN.md, "The readings to compare").
# Usage (in this directory): make (all pages), make trial (pages 014-038), or make 014.tsv;
# the pages already done are skipped.
# Tesseract (eng+ita) writes its TSV; only the words are kept, in the columns block_num,
# par_num, line_num, left, top, width, height, text (level, page_num, word_num and conf,
# and the rows of the blocks, paragraphs and lines, are not used).
# TESSERACT is the Windows build under WSL; relative paths, so that it can read and write them.

TESSERACT = /mnt/c/Program Files/Tesseract-OCR/tesseract.exe
pages = $(addsuffix .tsv,$(shell seq -f %03g $(1) $(2)))

.PHONY: all trial

all: $(patsubst ../%.png,%.tsv,$(wildcard ../*.png))
trial: $(call pages,14,38)

%.tsv: ../%.png
	"$(TESSERACT)" $< $*.raw -l eng+ita tsv
	awk -F'\t' -v OFS='\t' \
	  'NR==1 {print "block_num","par_num","line_num","left","top","width","height","text"; next} \
	   $$1==5 && $$12~/[^ ]/ {print $$3,$$4,$$5,$$7,$$8,$$9,$$10,$$12}' $*.raw.tsv > $@
	rm $*.raw.tsv
