# Independent OCR of ocr/en-oelsner with GLM-OCR, a third reading for the comparison
# (ocr/en-oelsner/PLAN.md, "The readings to compare").
# Usage (in this directory): make batch1, make batch2, ... (make -n batchN lists the pages)
# Only the pages of texts/en-oelsner are read (the page markers `(014) -->` of its files);
# the pages already done are skipped.
# The output is shown while it runs. If it runs away (loops), Ctrl+C stops make;
# the unfinished page is kept for inspection: delete it before running the batch again.

OCR = ollama run glm-ocr --nowordwrap
PAGES := $(sort $(shell grep -oh '([0-9][0-9][0-9]) -->' ../../../texts/en-oelsner/*.md | tr -dc '0-9\n'))
pages = $(addsuffix .txt,$(filter $(PAGES),$(shell seq -f %03g $(1) $(2))))

.PHONY: help all batch1 batch2 batch3 batch4 batch5

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

all: $(addsuffix .txt,$(PAGES)) ## All pages (404)
batch1: $(call pages,1,111) ## Front matter, Cantos I-IX
batch2: $(call pages,112,213) ## Cantos X-XVIII
batch3: $(call pages,214,309) ## Cantos XIX-XXVI
batch4: $(call pages,310,402) ## Cantos XXVII-XXXIV
batch5: $(call pages,403,416) ## End matter (essays, plates, editorial note, index)

.PRECIOUS: %.txt

%.txt: ../%.png
	$(OCR) "Text Recognition: $(abspath $<)" | tee $@
