# Independent OCR of ocr/la with GLM-OCR, for checking the transcription.
# Usage (in this directory): make batch1, make batch2, ... (make -n batchN lists the pages)
# Each batch covers whole cantos, including the Summarium and the essay;
# the pages transcribed as [Blank page] in ocr/la and the pages already done are skipped.
# The output is shown while it runs. If it runs away (loops), Ctrl+C stops make;
# the unfinished page is kept for inspection: delete it before running the batch again.

OCR = ollama run glm-ocr --nowordwrap
BLANK := $(patsubst ../%.txt,%,$(shell grep -lx '\[Blank page\]' ../[01]*.txt))
pages = $(addsuffix .txt,$(filter-out $(BLANK),$(shell seq -f %04g $(1) $(2))))

.PHONY: help all batch1 batch2 batch3 batch4 batch5 batch6 batch7 batch8 batch9 batch10 batch11

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

all: $(call pages,1,1296) ## All pages
batch1: $(call pages,79,114) ## Inferno I-III (trial)
batch2: $(call pages,115,232) ## Inferno IV-XIII
batch3: $(call pages,233,348) ## Inferno XIV-XXIII
batch4: $(call pages,349,478) ## Inferno XXIV-XXXIV
batch5: $(call pages,479,608) ## Preambula in Purgatorium, Purgatorio I-XI
batch6: $(call pages,609,740) ## Purgatorio XII-XXII
batch7: $(call pages,741,870) ## Purgatorio XXIII-XXXIII
batch8: $(call pages,871,1010) ## PARADISUS half-title, Paradiso I-XI
batch9: $(call pages,1011,1140) ## Paradiso XII-XXII
batch10: $(call pages,1141,1270) ## Paradiso XXIII-XXXIII
batch11: $(call pages,7,78) $(call pages,1271,1290) ## Front matter (title pages to Preambula), appendix and index

.PRECIOUS: %.txt

%.txt: ../%.png
	$(OCR) "Text Recognition: $(abspath $<)" | tee $@
