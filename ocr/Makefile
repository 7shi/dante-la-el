CMD = uv run ocr.py -m gemini-2.5-flash -p
PROMPT = Please transcribe the text. The text is written in

.PHONY: check all en en-oelsner la grc

check:
	find . -type f -name "*.txt" -size 0

all: en en-oelsner la grc
en: $(patsubst %.png,%.txt,$(wildcard en/*.png))
en/%.txt: en/%.png
	ollama run glm-ocr --nowordwrap "Text Recognition: ./$<" | tee $@
en-oelsner:
	$(CMD) "$(PROMPT) English and Italian." $@/*.png
la:
	$(CMD) "$(PROMPT) Latin." $@/*.png
grc:
	$(CMD) "$(PROMPT) Ancient Greek." $@/*.png
