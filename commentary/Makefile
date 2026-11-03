MODEL = gpt-6-astra
LANG_CODE = el
LANG_NAME = Modern Greek
DIR = $(LANG_CODE)
CHECK_DIR = check/$(LANG_CODE)

.PHONY: help generate fix-quotes check-quotes check-lines report-lines

help:
	@echo "Usage: make generate CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo "       make fix-quotes"
	@echo "       make check-quotes"
	@echo "       make check-lines [CANTICLE=<canticle>] [CANTO=<spec>]"
	@echo "       make report-lines [CANTICLE=<canticle>] [CANTO=<spec>]"
	@echo ""
	@echo "  generate   Write $(DIR)/<canticle>/NN.md (commentary) and NN.txt (translation)"
	@echo "             in $(LANG_NAME) with $(MODEL); CANTO takes the SPEC syntax"
	@echo "             (e.g. 1, 1-3, 12-), all cantos if omitted"
	@echo "  fix-quotes Rebuild the quote blocks of every $(DIR)/*/NN.md from dante-corpus and NN.txt"
	@echo "  check-quotes Check that the quote marks of every $(DIR)/*/NN.txt follow the original"
	@echo "  check-lines  Ask $(MODEL) whether every $(DIR)/*/NN.txt follows the original line by line;"
	@echo "               answers are saved in $(CHECK_DIR)/ and only cantos changed since are asked again"
	@echo "  report-lines Report the answers saved by check-lines, without calling the model"

generate:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/generate.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) -l $(LANG_CODE) -L "$(LANG_NAME)" -d $(DIR)

fix-quotes:
	uv run scripts/fix_quote_blocks.py -d $(DIR)

check-quotes:
	uv run scripts/check_quotes.py -d $(DIR)

check-lines:
	uv run scripts/check_lines.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) -L "$(LANG_NAME)" -d $(DIR) -o $(CHECK_DIR)

report-lines:
	uv run scripts/check_lines.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -r -d $(DIR) -o $(CHECK_DIR)
