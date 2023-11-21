In this directory you will find scripts to process the logs.

### Warning

After generating files from the logs, AI errors must be corrected manually.
Therefore, just running the script through will not match the file placed here.

# Main Process

The processes is not yet systematic, and these scripts were created haphazardly as needed.
Therefore, the main process is tentative at this time.

| No. | Script | Process |
|----:|--------|---------|
|1|(manually)|AI chat to get the information we need. Results are output in tabular format whenever possible, as this is useful for formatting later.|
|2|[copy_log.py](https://github.com/7shi/dante-la-el/blob/main/scripts/copy_log.py)|This is a script that automatically records the chat logs as we manually copy them. If we could ask questions via the API, there would be no need for such a thing, but due to billing reasons, we provide one like this.|
|3|[striplog.py](https://github.com/7shi/dante-la-el/blob/main/scripts/striplog.py)|Extract tables from chat logs. Manual modifications are made to the extracted tables.<br>This script can be referenced as a library. If detailed post-processing is required, this can be referenced to create a custom script.|
|4|[replace_tr.py](https://github.com/7shi/dante-la-el/blob/main/scripts/replace_tr.py)|When the AI quotes the original text, punctuation and other characters may change slightly. This script will replace the sentences in the table.|
|5|[conv_log_s.py](https://github.com/7shi/dante-la-el/blob/main/scripts/conv_log_s.py)|Generate translations and word tables from tables. A simple error check is performed, which is then used as a reference for manual correction.|

Here is an example of a file output from this process. The main purpose is to facilitate learning.

* translation: [01-en.txt](https://github.com/7shi/dante-la-el/blob/main/Inferno/ChatGPT/en/01-en.txt)
* word table: [01-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/ChatGPT/en/01-en.md)

# Aggregation

Scripts for comparing results. The main purpose is to examine ways to generate stable translations.

| Script | Example | Description |
|--------|---------|-------------|
|[make_compare.py](https://github.com/7shi/dante-la-el/blob/main/scripts/make_compare.py)|[compare-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/compare-en.md)|Juxtapose multiple translations.|
|[make_score.py](https://github.com/7shi/dante-la-el/blob/main/scripts/make_score.py)|[01-score-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/MT/01-en-score.md)<br>[01-en-mix.txt](https://github.com/7shi/dante-la-el/blob/main/Inferno/MT/en/01-en-mix.txt)|Calculate scores and generate a mixed translation.|

The score is calculated based on the edit distance between multiple translations. It is not a direct indication of the quality of a translation, but it does give an indication of how average a translation is in the population. The most average lines are adopted to generate a mixed translation.

# Assistance

Scripts to assist with manual tasks that are difficult to automate.

| Script | Description |
|--------|-------------|
|[copy_adjnl.py](https://github.com/7shi/dante-la-el/blob/main/scripts/copy_adjnl.py)|Insert spaces for line breaks in quoted text to accommodate differences in Markdown specifications. Monitor the clipboard and automatically modify copied text.|
|[copy_append.py](https://github.com/7shi/dante-la-el/blob/main/scripts/copy_append.py)|Monitor the clipboard to automatically retrieve copied text.|
|[make_31.py](https://github.com/7shi/dante-la-el/blob/main/scripts/make_31.py)|The prose of the source text and the translation, which is split into three lines, are lined up to instruct the AI to split the latter. Used in [Norton](https://github.com/7shi/dante-la-el/tree/main/Inferno/Bard/en-norton).|
|[splitrans.py](https://github.com/7shi/dante-la-el/blob/main/scripts/splitrans.py)|Split sentences to be translated by machine translation with character limit. Copying the translation will automatically proceed to the next step.|

# Others

| Script | Description |
|--------|-------------|
|[extract_line.py](https://github.com/7shi/dante-la-el/blob/main/scripts/extract_line.py)|Extract lines from a table.|
|[extract_phrase.py](https://github.com/7shi/dante-la-el/blob/main/scripts/extract_phrase.py)|Extract phrases from the table. Check if the original text has not been changed.|
|[fix_eo.py](https://github.com/7shi/dante-la-el/blob/main/scripts/fix_eo.py)|Convert x-convention to circumflex (^).|
|[fix_grc.py](https://github.com/7shi/dante-la-el/blob/main/scripts/fix_grc.py)|Ancient Greek quotation marks at the beginning of lines are also applied to the translation.|
|[fix_num.py](https://github.com/7shi/dante-la-el/blob/main/scripts/fixnum.py)|Corrected auto-numbered log section numbers.|
|[greco_roman.py](https://github.com/7shi/dante-la-el/blob/main/scripts/greco_roman.py)|Transliteration of Ancient Greek into Latin characters using [greektrans](https://github.com/7shi/greektrans).|
|[number.py](https://github.com/7shi/dante-la-el/blob/main/scripts/number.py)|Add line numbers to the text.|
|[rm_trema.py](https://github.com/7shi/dante-la-el/blob/main/scripts/rm_trema.py)|Remove trema (¨) from the text.|
