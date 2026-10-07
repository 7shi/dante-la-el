CMD = uv run ocr.py -m gemini-2.5-flash -p
PROMPT = Please transcribe the text. The text is written in

.PHONY: check all en la grc

check:
	find . -type f -name "*.txt" -size 0

all: en la grc
en:
	$(CMD) "$(PROMPT) English and Italian." $@/*.png
la:
	$(CMD) "$(PROMPT) Latin." $@/*.png
grc:
	$(CMD) "$(PROMPT) Ancient Greek." $@/*.png
