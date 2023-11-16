In this directory you will find scripts to process the logs.

### Warning

After generating files from the logs, AI errors must be corrected manually.
Therefore, just running the script through will not match the file placed here.

# Process

The work is not yet systematic, and these scripts were created haphazardly as needed.
Therefore, the process is tentative at this time.

| No. | Script | Process |
|----:|--------|---------|
|1|(manually)|AI chat to get the information we need. Results are output in tabular format whenever possible, as this is useful for formatting later.|
|2|[logcopy.py](https://github.com/7shi/dante-la-el/blob/main/scripts/logcopy.py)|This is a script that automatically records the chat logs as we manually copy them. If we could ask questions via the API, there would be no need for such a thing, but due to billing reasons, we provide one like this.|
|3|[striplog.py](https://github.com/7shi/dante-la-el/blob/main/scripts/striplog.py)|Extract tables from chat logs. Manual modifications are made to the extracted tables.<br>This script can be referenced as a library. If detailed post-processing is required, this can be referenced to create a custom script.|
|4|[replace_tr.py](https://github.com/7shi/dante-la-el/blob/main/scripts/replace_tr.py)|When the AI quotes the original text, punctuation and other characters may change slightly. This script will replace the sentences in the table.|
|5|[conv_log_s.py](https://github.com/7shi/dante-la-el/blob/main/scripts/conv_log_s.py)|Generate translations and word tables from tables. A simple error check is performed, which is then used as a reference for manual correction.|

Here is an example of a file output from this process. The main purpose is to facilitate learning.

* translation: [01-en.txt](https://github.com/7shi/dante-la-el/blob/main/Inferno/ChatGPT/en/01-en.txt)
* word table: [01-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/ChatGPT/en/01-en.md)

## Aggregation

Scripts for comparing results. The main purpose is to examine ways to generate stable translations.

| Script | Example | Description |
|--------|---------|-------------|
|[mkcompare.py](https://github.com/7shi/dante-la-el/blob/main/scripts/mkcompare.py)|[compare-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/compare-en.md)|Multiple translation results are juxtaposed.|
|[score.py](https://github.com/7shi/dante-la-el/blob/main/scripts/score.py)|[01-score-en.md](https://github.com/7shi/dante-la-el/blob/main/Inferno/MT/01-score-en.md)<br>[01-en-mix.txt](https://github.com/7shi/dante-la-el/blob/main/Inferno/MT/01-en-mix.txt)|It calculates a score based on the edit distance between multiple translations and generates a translation that mixes the most average lines. It is not a direct measure of translation excellence, but it does provide an indication of how average a translation is in the population.|
