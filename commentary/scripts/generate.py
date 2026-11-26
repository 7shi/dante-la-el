"""
Explain a canto of the Divina Commedia in a target language, and translate
every line of it into that language.
The source (the Italian of dante_corpus, or another source of source.py, sent
line by line with line numbers so the model can cite them) is sent as its own
message, followed by the instructions in PROMPT. The translations quoted in
the commentary seed the line-by-line translation, and TRANSLATE_PROMPT fills
in the rest. For a source other than the Italian, only the translation is made
(TRANSLATE_PROMPT fills in every line); its commentary is not written yet.
"""

import argparse
import re
import sys
from pathlib import Path
from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals

from source import SOURCES, TRANSLATED_SOURCES, source_lines

CANTICLE_NAMES = {
    "inferno": "Inferno",
    "purgatorio": "Purgatorio",
    "paradiso": "Paradiso",
}

# Per target language (keyed by language code):
# - name: the name of the language, as written into the prompts
# - letters: a translation must contain at least one of these, or it is
#   taken as a copy of the original
# - reject: (optional) a regex for characters a translation must not contain;
#   such a line is taken as a copy of the original (polytonic Greek in el)
# - closing: the word that opens the heading of the closing section
# - note: an extra instruction appended to both prompts
# - quotes: the opening and closing quote marks of translations, counted by
#   check_quotes.py
# - apostrophe: (optional) a regex for a mark that is an apostrophe, not a
#   quote; such marks are dropped before counting
LANGUAGES = {
    "el": {
        "name": "Modern Greek",
        "letters": r"[\u0370-\u03ff\u1f00-\u1fff]",
        "closing": "Επίλογος",
        "note": "Use the monotonic orthography.",
        # Catches a copy of the polytonic source grc
        "reject": r"[\u1f00-\u1fff]",
        # ’ is the apostrophe of elision (γι’, απ’), so ‘’ do not count
        "quotes": ("«“", "»”"),
    },
    "eo": {
        "name": "Esperanto",
        # Shares its script with Italian, so this rejects only lines without
        # letters; a verbatim copy is still caught by comparing with the original
        "letters": r"[A-Za-zĈĜĤĴŜŬĉĝĥĵŝŭ]",
        "closing": "Epilogo",
        "note": "Write ĉ, ĝ, ĥ, ĵ, ŝ, ŭ with their diacritics, not in the x- or h-system.",
        # Nests ‘’ inside «» like the original; ’ is an apostrophe only in
        # Italian names (d’Este, de’ Pazzi)
        "quotes": ("«“‘", "»”’"),
        "apostrophe": r"(?<=\w)’(?=\w)|\bde’",
    },
    "en": {
        "name": "English",
        # Shares its script with Italian, as Esperanto does
        "letters": r"[A-Za-z]",
        "closing": "Epilogue",
        "note": "Write quotation marks as “” and ‘’, not as straight quotes; "
                "write the apostrophe as the straight ' (don't, souls', de' Pazzi), not as ’.",
        # The apostrophe is the straight ', so every ’ closes a ‘
        "quotes": ("“‘", "”’"),
    },
}

PROMPT = """
Read the attached Italian text of canto {number} of Dante's Divine Comedy, {canticle}, and write an article in Markdown, in {lang}, that explains its allegory and background.

- Give a heading to each scene or theme, and under each heading quote the lines that form the core of that passage. Aim for about ten headings.
- Quote each line as `> line-number original`, followed on the next line by `> (translation in {lang})`.
- Translate each quoted line on its own, keeping to what that line says even if the word order becomes forced; do not carry words or quotation marks over from a neighbouring line.
- Put consecutive lines together in a single quote block, separated by lines containing only `>`. Do not open a separate block for each line.
- After each quote, explain the allegory and background of those lines in prose.
- Quote only the lines you actually discuss. There is no need to quote every line.
- Even under one heading, alternate quotes and prose for each point you discuss. Do not quote the whole range of a heading first and then discuss it.
- End with a section headed `## {closing} — <a title summing up the content>`, briefly summing up what the canto as a whole means.
- Write the whole article in {lang}.{note}
""".strip()

TRANSLATE_PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, and its translation into {lang}, on alternating lines. Fill in the translation for the lines whose translation is {placeholder}.

- Translate only the lines marked {placeholder}, one per line, in the form `line-number translation`.
{style}
- Keep each translation to what its own line says, even if the word order becomes forced; do not carry words over to or from a neighbouring line. Open and close quotation marks on the same lines as the original.
- Output only the lines you filled in.
- Write the translation itself on each line. Do not include {placeholder} in the output.{note}
""".strip()

# The style of the translation in TRANSLATE_PROMPT: a readable one from the
# Italian, a literal one from any other source
STYLE = "- Follow the style of the existing translations, so that the text reads on smoothly from its context."
LITERAL_STYLE = "- Translate as literally as possible, even where it reads stiffly: render every word, and keep the word order, the constructions (a participle as a participle, unless that changes who does what), and the tenses of the original, as far as the line stays correct {lang} that reads as the original means. Do not paraphrase, and add nothing to explain the text."


PLACEHOLDER = "**NEED TRANSLATE**"

# Lines Dante made meaningless on purpose, keyed by (canticle, canto):
# a verbatim copy of these is a valid rendering, not a missed translation
VERBATIM_LINES = {
    ("inferno", 7): {1},  # Plutus: «Pape Satàn, pape Satàn aleppe!»
    ("inferno", 31): {67},  # Nimrod: «Raphèl maì amècche zabì almi»
}

# Set the path only when usage should be recorded
USAGE_PATH = None

QUOTE_RE = re.compile(r"^>\s*(\d+)\s+(.*?)\s*$")
# Quote marks and apostrophes the model may restyle in a quoted original
QUOTE_MARKS = str.maketrans({"«": '"', "»": '"', "“": '"', "”": '"', "’": "'", "‘": "'"})
# Other characters a quoted original may differ by (a dropped diaeresis, a
# changed punctuation mark). Lines up to ten apart in a canto differ by at
# least 6 (Paradiso 4.4 and 4.6), so even an exact quote of a neighbouring
# line under the wrong number is still rejected.
MAX_QUOTE_DIFF = 3


def edit_distance(a: str, b: str, limit: int) -> int:
    """Levenshtein distance, or limit + 1 once it is sure to exceed limit."""
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > limit:
            return limit + 1
        prev = cur
    return prev[-1]


def same_line(quoted: str, original: str) -> bool:
    """A quoted line matches its original up to the style of its quote marks
    and a few other characters."""
    return edit_distance(
        quoted.translate(QUOTE_MARKS), original.translate(QUOTE_MARKS), MAX_QUOTE_DIFF
    ) <= MAX_QUOTE_DIFF

TRANS_RE = re.compile(r"^>\s*\((.*)\)\s*$")
FILLED_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")
MARKER_RE = re.compile(rf"^\**\s*{re.escape(PLACEHOLDER.strip('*'))}\s*\**\s*")


def clean_translation(text: str) -> str:
    """Drop the placeholder, which the model sometimes echoes ahead of the
    translation instead of replacing it, with or without its emphasis marks."""
    return MARKER_RE.sub("", text.strip())


def is_translated(
    trans: str, original: str, letters: re.Pattern, verbatim: bool = False,
    reject: re.Pattern | None = None,
) -> bool:
    """The model sometimes copies the original line instead of translating it.

    With verbatim, the line may be left as it is in the original. A line with
    a character matching reject is taken as a copy too.
    """
    return (
        bool(trans)
        and (verbatim or trans != original)
        and bool(letters.search(trans))
        and not (reject and reject.search(trans))
    )


def canto_text(lines) -> str:
    return "\n".join(f"{line.no} {line.text}" for line in lines)


def extract_translations(commentary: str, lines) -> dict[int, str]:
    """Collect `> N original` / `> (translation)` pairs from a commentary.

    Pairs whose quoted original does not match the corpus line (quote marks
    and a few other characters aside) are dropped, so that a partial or misquoted line is left
    untranslated instead of wrong.
    """
    originals = {line.no: line.text for line in lines}
    md_lines = commentary.splitlines()
    translations: dict[int, str] = {}
    for i, md_line in enumerate(md_lines[:-1]):
        if not (quote := QUOTE_RE.match(md_line)):
            continue
        if not (trans := TRANS_RE.match(md_lines[i + 1])):
            continue
        no = int(quote.group(1))
        if not same_line(quote.group(2), originals.get(no, "")):
            print(f"skip line {no}: quoted text does not match", file=sys.stderr)
            continue
        translations[no] = trans.group(1)
    return translations


def interleaved_text(lines, translations: dict[int, str], placeholder: str) -> str:
    """Original and translation on alternating lines, sent to the model.

    Untranslated lines carry a placeholder, since the model overlooks blank lines easily.
    """
    return "\n".join(
        f"{line.no} {line.text}\n{translations.get(line.no, placeholder)}"
        for line in lines
    )


def translations_only_text(lines, translations: dict[int, str]) -> str:
    """Translations only, one per source line, blank where untranslated."""
    return "\n".join(translations.get(line.no, "") for line in lines)


def parse_translations_only(
    saved: str, lines, letters: re.Pattern, verbatim: set[int],
    reject: re.Pattern | None = None,
) -> dict[int, str]:
    """Read back a saved translations-only file, keeping the lines already translated."""
    translations: dict[int, str] = {}
    for line, text_line in zip(lines, saved.splitlines()):
        trans = clean_translation(text_line)
        if is_translated(trans, line.text, letters, line.no in verbatim, reject):
            translations[line.no] = trans
    return translations


def parse_filled(
    filled: str, missing: set[int], lines, letters: re.Pattern, verbatim: set[int],
    reject: re.Pattern | None = None,
) -> dict[int, str]:
    """Collect `N translation` lines, keeping only the requested line numbers."""
    originals = {line.no: line.text for line in lines}
    translations: dict[int, str] = {}
    for text_line in filled.splitlines():
        if match := FILLED_RE.match(text_line):
            no, trans = int(match.group(1)), clean_translation(match.group(2))
            if no in missing and is_translated(
                trans, originals.get(no, ""), letters, no in verbatim, reject
            ):
                translations[no] = trans
    return translations


def generate(client: Client, canticle: str, canto: int, args: argparse.Namespace):
    lines = source_lines(args.source, canticle, canto)
    text = canto_text(lines)
    language = LANGUAGES[args.lang_code]
    letters = re.compile(language["letters"])
    reject = re.compile(language["reject"]) if language.get("reject") else None
    italian = args.source == "it"
    # Lines left meaningless on purpose are known only for the Italian
    verbatim = VERBATIM_LINES.get((canticle, canto), set()) if italian else set()
    note = f" {language['note']}" if language.get("note") else ""
    names = dict(
        canticle=CANTICLE_NAMES[canticle], number=canto,
        lang=language["name"], note=note,
    )
    style = STYLE if italian else LITERAL_STYLE.format(lang=language["name"])

    out_dir = args.dir / canticle
    out_path = out_dir / f"{canto:02d}.md"
    trans_path = out_dir / f"{canto:02d}.txt"

    if trans_path.exists():
        # Resume: the saved file already holds every translation extracted so far.
        print(f"Resuming from {trans_path}")
        translations = parse_translations_only(
            trans_path.read_text(), lines, letters, verbatim, reject
        )
    elif not italian:
        translations = {}  # translation only: every line is filled in below
    else:
        if out_path.exists():
            print(f"Skipped (already exists): {out_path}")
            commentary = out_path.read_text()
        else:
            prompt = PROMPT.format(**names, closing=language["closing"])
            response = client([text, prompt])
            commentary = response.text
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(commentary)
            print(f"\nSaved to {out_path}")
        translations = extract_translations(commentary, lines)

    saved = trans_path.read_text() if trans_path.exists() else ""

    def save():
        # Saved every round, so an interrupted run can resume where it left off.
        nonlocal saved
        content = translations_only_text(lines, translations) + "\n"
        if content != saved:
            out_dir.mkdir(parents=True, exist_ok=True)
            trans_path.write_text(content)
            saved = content
            print(f"\nSaved to {trans_path}")

    prompt = TRANSLATE_PROMPT.format(
        **names, source=SOURCES[args.source]["name"], style=style,
        placeholder=PLACEHOLDER,
    )
    for round_no in range(1, args.rounds + 1):
        missing = {line.no for line in lines if line.no not in translations}
        if not missing:
            break
        print(f"\n--- round {round_no}: {len(missing)} lines left ---")
        response = client(
            [interleaved_text(lines, translations, PLACEHOLDER), prompt]
        )
        if not (added := parse_filled(
            response.text, missing, lines, letters, verbatim, reject
        )):
            print("\nno progress, giving up", file=sys.stderr)
            break
        translations |= added
        save()
    save()  # in case the loop ended before any round wrote the file
    if remaining := sorted(line.no for line in lines if line.no not in translations):
        print(f"\nstill untranslated: {remaining}", file=sys.stderr)


def main():
    global USAGE_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "canticle",
        choices=list(CANTICLE_NAMES),
        help="Canticle name: inferno, purgatorio, or paradiso",
    )
    parser.add_argument(
        "-c", "--canto",
        help=CANTO_SPEC_HELP,
    )
    parser.add_argument(
        "-m", "--model",
        required=True,
        help="Model name with optional vendor prefix (e.g. gpt-6-astra)",
    )
    parser.add_argument(
        "-l", "--lang-code",
        required=True,
        choices=list(LANGUAGES),
        help="Language code of the target language (e.g. el)",
    )
    parser.add_argument(
        "-s", "--source",
        choices=TRANSLATED_SOURCES,
        default="it",
        help="Source text to explain and translate (default: it, the Italian; "
             "grc: Musurus's Greek Inferno; la-la, la-it: Serravalle's Latin and "
             "the Italian printed with it; translation only)",
    )
    parser.add_argument(
        "-r", "--rounds",
        type=int,
        default=5,
        help="Max translation passes to fill remaining lines (default: 5)",
    )
    parser.add_argument(
        "--no-think",
        action="store_true",
        help="Disable thinking output (include_thoughts=False)",
    )
    parser.add_argument(
        "-d", "--dir",
        type=Path,
        required=True,
        help="Output directory holding <canticle>/<NN>.md",
    )
    parser.add_argument(
        "--save-usage",
        action="store_true",
        help="Record usage regardless of model name",
    )
    args = parser.parse_args()

    if err := check_canto_spec([args.canticle], args.canto):
        parser.error(err)
    if args.canticle not in SOURCES[args.source]["canticles"]:
        parser.error(f"source {args.source} has no {args.canticle}")

    if args.model.startswith(("openai:", "gpt-")) or args.save_usage:
        USAGE_PATH = find_usage_file()

    client = Client(
        model=args.model,
        include_thoughts=not args.no_think,
        show_params=False,
        keep_history=False,
        show_usage=True,
    )

    try:
        for canto in select_cantos(args.canticle, args.canto):
            generate(client, args.canticle, canto, args)
    finally:
        # Record silently so an interrupted run still logs what it consumed;
        # the report below is printed only on normal completion
        if client.usages and USAGE_PATH is not None:
            append_usage(sum(client.usages), args.model, USAGE_PATH)

    if client.usages:
        print(f"\n--- Total Usage ---\n{sum(client.usages)}")
        if USAGE_PATH is not None:
            print()
            print_today_totals(USAGE_PATH, models=[args.model])


if __name__ == "__main__":
    main()
