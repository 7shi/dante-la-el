MODEL = gpt-6.2-astra
CHECK_MODEL = $(MODEL)
# The target language is given as LANG on the command line (make LANG=eo).
# LANG from the environment is the locale and is ignored; when LANG is given,
# it is not passed on to the scripts, so they do not get it as a locale.
ifeq ($(origin LANG),command line)
LANG_CODE := $(LANG)
unexport LANG
endif
LANG_CODE ?= el
# The source text: it (Italian, default) or grc (Musurus's Greek Inferno);
# a translation from another source than the Italian goes to <lang>-<source>
SOURCE ?= it
DIR = $(if $(filter it,$(SOURCE)),$(LANG_CODE),$(LANG_CODE)-$(SOURCE))
CHECK_DIR = check/$(DIR)

.PHONY: help generate fix-quotes check-quotes check-lines report-lines apply-lines

help:
	@echo "Usage: make generate CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo "       make fix-quotes"
	@echo "       make check-quotes"
	@echo "       make check-lines [CANTICLE=<canticle>] [CANTO=<spec>] [CHECK_MODEL=<model>]"
	@echo "       make report-lines [CANTICLE=<canticle>] [CANTO=<spec>] [KIND=\"<kind> ...\"]"
	@echo "       make apply-lines KIND=\"<kind> ...\" [CANTICLE=<canticle>] [CANTO=<spec>]"
	@echo "       every target takes LANG=<el|eo|en> (default: el)"
	@echo "       every target takes SOURCE=grc for the translation of Musurus's Greek Inferno in $(LANG_CODE)-grc/"
	@echo ""
	@echo "  generate   Write $(DIR)/<canticle>/NN.md (commentary) and NN.txt (translation)"
	@echo "             in $(LANG_CODE) with $(MODEL); CANTO takes the SPEC syntax"
	@echo "             (e.g. 1, 1-3, 12-), all cantos if omitted"
	@echo "  fix-quotes Rebuild the quote blocks of every $(DIR)/*/NN.md from dante-corpus and NN.txt"
	@echo "  check-quotes Check that the quote marks of every $(DIR)/*/NN.txt follow the original"
	@echo "  check-lines  Ask $(CHECK_MODEL) whether every $(DIR)/*/NN.txt follows the original line by line;"
	@echo "               answers are saved in $(CHECK_DIR)/ and only cantos changed since are asked again"
	@echo "  report-lines Report the answers saved by check-lines, with their fixes, without calling the model"
	@echo "  apply-lines  Apply the saved fixes of the given kinds (moved, function, missing, added) to NN.txt"

generate:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/generate.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) -l $(LANG_CODE) -s $(SOURCE) -d $(DIR)

fix-quotes:
	uv run scripts/fix_quote_blocks.py -d $(DIR)

check-quotes:
	uv run scripts/check_quotes.py -l $(LANG_CODE) -s $(SOURCE) -d $(DIR)

check-lines:
	uv run scripts/check_lines.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(CHECK_MODEL) -l $(LANG_CODE) -s $(SOURCE) -d $(DIR) -o $(CHECK_DIR)

report-lines:
	uv run scripts/check_lines.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -r $(foreach k,$(KIND),-k $(k)) -s $(SOURCE) -d $(DIR) -o $(CHECK_DIR)

apply-lines:
ifndef KIND
	$(error KIND is required: one or more of moved, function, missing, added)
endif
	uv run scripts/check_lines.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -a $(foreach k,$(KIND),-k $(k)) -l $(LANG_CODE) -s $(SOURCE) -d $(DIR) -o $(CHECK_DIR)
