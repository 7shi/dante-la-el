# Independent OCR of ocr/en-paradiso with GLM-OCR, a reading that votes in the comparison
# (ocr/en-paradiso/PLAN.md, "The readings to compare"), through llm7shi
# (ocr/scripts/glmocr.py: the same output as `ollama run glm-ocr`).
# Usage (in this directory): make (all pages), or make NNN.txt; the pages already done
# are skipped.
# A page that runs away (loops) is stopped, written as it stood and listed at the end.
# Blank pages run away: empty their NNN.txt. Ctrl+C leaves no partial file.

OCR = uv run ../../scripts/glmocr.py -o .

.PHONY: all

all:
	$(OCR) $(sort $(wildcard ../*.png))

%.txt: ../%.png
	$(OCR) $<
