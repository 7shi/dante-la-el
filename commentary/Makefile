MODEL = gpt-6-astra
LANG_CODE = el
LANG_NAME = Modern Greek
DIR = $(LANG_CODE)

.PHONY: help generate

help:
	@echo "Usage: make generate CANTICLE=<inferno|purgatorio|paradiso> [CANTO=<spec>]"
	@echo ""
	@echo "  generate   Write $(DIR)/<canticle>/NN.md (commentary) and NN.txt (translation)"
	@echo "             in $(LANG_NAME) with $(MODEL); CANTO takes the SPEC syntax"
	@echo "             (e.g. 1, 1-3, 12-), all cantos if omitted"

generate:
ifndef CANTICLE
	$(error CANTICLE is required: inferno, purgatorio, or paradiso)
endif
	uv run scripts/generate.py $(CANTICLE) $(if $(CANTO),-c $(CANTO)) -m $(MODEL) -l $(LANG_CODE) -L "$(LANG_NAME)" -d $(DIR)
