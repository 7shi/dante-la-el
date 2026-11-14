# Independent OCR of ocr/en-paradiso with GLM-OCR, a reading that votes in the comparison
# (ocr/en-paradiso/PLAN.md, "The readings to compare").
# Usage (in this directory): make (all pages), or make NNN.txt; the pages already done
# are skipped.
# The output is shown while it runs. If it runs away (loops), Ctrl+C stops make;
# the unfinished page is kept for inspection: delete it before running again.

OCR = ollama run glm-ocr --nowordwrap

.PHONY: all

all: $(patsubst ../%.png,%.txt,$(wildcard ../*.png))

.PRECIOUS: %.txt

%.txt: ../%.png
	$(OCR) "Text Recognition: $(abspath $<)" | tee $@
