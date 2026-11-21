MODEL = gpt-6.2-astra
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
# Musurus's Greek explained against Oelsner's Italian/English + translations/en/grc/
GRC_EN = $(if $(filter grc,$(SOURCE)),$(filter en,$(LANG_CODE)))
BLOCK_MODE = $(or $(PROSE),$(GRC_EN))
# The translations quoted, in ../commentary/ (see its Makefile)
DIR = ../commentary/$(if $(filter it,$(SOURCE)),$(LANG_CODE),$(LANG_CODE)-$(SOURCE))
# The output: <lang>-<source>, or <source> for a block-mode source (prose or grc with LANG=en)
OUT = $(if $(BLOCK_MODE),$(SOURCE),$(LANG_CODE)-$(SOURCE))

.PHONY: help grammar grammar-notes fix-grammar-quotes

help:
	@echo "Usage: make grammar CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo "       make grammar-notes CANTICLE=<canticle> [CANTO=<spec>]"
	@echo "       make fix-grammar-quotes"
	@echo "       every target takes LANG=<el|eo|en> (default: el) and SOURCE=<it|grc> (default: it)"
	@echo "       with SOURCE=grc LANG=en, Musurus's Greek (and translations/en/grc/) is explained"
	@echo "       against Oelsner's Italian and English, in grc/"
	@echo "       every target also takes SOURCE=en (the Italian of Carlyle's Inferno) or"
	@echo "       SOURCE=en-oelsner, en-purgatorio, en-paradiso (that of the Temple Classics),"
	@echo "       explained against the English printed with it (without LANG), in <source>/"
	@echo ""
	@echo "  grammar      Write $(OUT)/<canticle>/NN.md (for en, the Temple Classics, and"
	@echo "               SOURCE=grc LANG=en, named as in ../texts/<source>/), a grammar"
	@echo "               commentary in English on every line of the $(SOURCE) source"
	@echo "  grammar-notes List the translation notes of the grammar commentaries, without calling the model"
	@echo "  fix-grammar-quotes Rebuild the quote blocks of the commentaries in $(OUT)/ from the source and $(DIR)/"
	@echo "               (for en, the Temple Classics, and SOURCE=grc LANG=en, from texts/ and translations/)"

grammar:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/grammar.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) $(if $(PROSE),,-l $(LANG_CODE)) $(if $(BLOCK_MODE),,-d $(DIR)) -s $(SOURCE) -o $(OUT)

grammar-notes:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/grammar.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -n $(if $(PROSE),,-l $(LANG_CODE)) -s $(SOURCE) -o $(OUT)

fix-grammar-quotes:
	uv run ../commentary/scripts/fix_quote_blocks.py -d $(OUT) -s $(SOURCE) $(if $(BLOCK_MODE),,-t $(DIR))
