MODEL = gpt-6-astra
# The language of the translations quoted is given as LANG on the command line
# (make LANG=eo). LANG from the environment is the locale and is ignored; when
# LANG is given, it is not passed on to the scripts, so they do not get it as a
# locale.
ifeq ($(origin LANG),command line)
LANG_CODE := $(LANG)
unexport LANG
endif
LANG_CODE ?= el
# The source text: it (Italian, default), grc (Musurus's Greek Inferno), en
# (the Italian of Carlyle's Inferno in texts/en/), or en-oelsner, en-purgatorio,
# en-paradiso (the Italian of the Temple Classics in texts/<source>/); these
# are compared by grammar with the English printed with them, so they take no LANG
SOURCE ?= it
PROSE_SOURCES = en en-oelsner en-purgatorio en-paradiso
PROSE = $(filter $(PROSE_SOURCES),$(SOURCE))
# The translations quoted, in ../commentary/ (see its Makefile)
DIR = ../commentary/$(if $(filter it,$(SOURCE)),$(LANG_CODE),$(LANG_CODE)-$(SOURCE))
# The output: <lang>-<source>, or <source> for a source printed with its own translation
OUT = $(if $(PROSE),$(SOURCE),$(LANG_CODE)-$(SOURCE))

.PHONY: help grammar grammar-notes fix-grammar-quotes

help:
	@echo "Usage: make grammar CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo "       make grammar-notes CANTICLE=<canticle> [CANTO=<spec>]"
	@echo "       make fix-grammar-quotes"
	@echo "       every target takes LANG=<el|eo|en> (default: el) and SOURCE=<it|grc> (default: it)"
	@echo "       every target also takes SOURCE=en (the Italian of Carlyle's Inferno) or"
	@echo "       SOURCE=en-oelsner, en-purgatorio, en-paradiso (that of the Temple Classics),"
	@echo "       explained against the English printed with it (without LANG), in <source>/"
	@echo ""
	@echo "  grammar      Write $(OUT)/<canticle>/NN.md (for en and the Temple Classics, named"
	@echo "               as in ../texts/<source>/), a grammar commentary in English on"
	@echo "               every line of the $(SOURCE) source, quoting the translations of $(DIR)/"
	@echo "               (for en and the Temple Classics, a comparison with the English, block by block)"
	@echo "  grammar-notes List the translation notes of the grammar commentaries, without calling the model"
	@echo "  fix-grammar-quotes Rebuild the quote blocks of the commentaries in $(OUT)/ from the source and $(DIR)/"
	@echo "               (for en and the Temple Classics, from the source alone)"

grammar:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/grammar.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) $(if $(PROSE),,-l $(LANG_CODE) -d $(DIR)) -s $(SOURCE) -o $(OUT)

grammar-notes:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/grammar.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -n -s $(SOURCE) -o $(OUT)

fix-grammar-quotes:
	uv run ../commentary/scripts/fix_quote_blocks.py -d $(OUT) -s $(SOURCE) $(if $(PROSE),,-t $(DIR))
