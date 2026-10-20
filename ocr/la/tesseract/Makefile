# Tesseract's word boxes of ocr/la, for locating the marks of the markup method in the image
# (la_markprep.py, la_markresolve.py, la_lines.py, la_versecrop.py, la_view.py word).
# Usage (in this directory): make all, or make 0233.tsv; the pages already done are skipped.
# Tesseract (lat+ita) writes its TSV; only the words are kept, in the columns block_num,
# par_num, line_num, left, top, width, height, text (level, page_num, word_num and conf,
# and the rows of the blocks, paragraphs and lines, are not used).
# TESSERACT is the Windows build under WSL; relative paths, so that it can read and write them.

TESSERACT = /mnt/c/Program Files/Tesseract-OCR/tesseract.exe

.PHONY: all

all: $(patsubst ../%.png,%.tsv,$(wildcard ../[01]*.png))

%.tsv: ../%.png
	"$(TESSERACT)" $< $*.raw -l lat+ita tsv
	awk -F'\t' -v OFS='\t' \
	  'NR==1 {print "block_num","par_num","line_num","left","top","width","height","text"; next} \
	   $$1==5 && $$12~/[^ ]/ {print $$3,$$4,$$5,$$7,$$8,$$9,$$10,$$12}' $*.raw.tsv > $@
	rm $*.raw.tsv
