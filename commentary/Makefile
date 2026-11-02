MODEL = gpt-6-astra
LANG_CODE = el
LANG_NAME = Modern Greek
DIR = $(LANG_CODE)

.PHONY: help generate fix-quotes

help:
	@echo "Usage: make generate CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo "       make fix-quotes"
	@echo ""
	@echo "  generate   Write $(DIR)/<canticle>/NN.md (commentary) and NN.txt (translation)"
	@echo "             in $(LANG_NAME) with $(MODEL); CANTO takes the SPEC syntax"
	@echo "             (e.g. 1, 1-3, 12-), all cantos if omitted"
	@echo "  fix-quotes Rebuild the quote blocks of every $(DIR)/*/NN.md from dante-corpus and NN.txt"

generate:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/generate.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) -l $(LANG_CODE) -L "$(LANG_NAME)" -d $(DIR)

fix-quotes:
	uv run scripts/fix_quote_blocks.py -d $(DIR)
