"""
Write a grammar commentary on a canto, in English, covering every line: the
forms, the constructions, and the usage of the source text, and how the
existing line-by-line translation (<canticle>/<NN>.txt) renders them. The
content of the poem (story, allegory, background) is left out.

The canto is cut into sections of about --size lines that end where a
sentence ends. Each section is one call: the whole canto (every line followed
by its translation) is sent as its own message, followed by PROMPT for the
lines of that section. An answer is checked before it is kept: its heading
must name the section's lines, it must quote every line of the section once
and in order, and every quoted original and translation must match the
source and the .txt (up to a few characters), so that a translation the
model has rewritten is caught. An answer that fails is asked again, up to
--tries times. Its quote blocks are then rebuilt from the sources of truth
(as fix_quote_blocks.py does) and appended to <NN>.md, so an interrupted run
resumes after the last section saved. A last call adds the closing summary.

A source printed with a prose translation of its own (carlyle: the Italian
of Carlyle's Inferno and his English) is explained against that translation
instead (PROSE_PROMPT): the canto is sent page by page, the lines of a page
followed by the English prose that renders them; the quotes give the
originals alone, and the model quotes Carlyle's words in its explanation in
double quotation marks, each of which must be found in his translation of
the canto (up to punctuation and case). No translation directory is needed.

The model does not change the translation; where it finds the translation
wrong, it says so in a paragraph opening with `Translation note:`. With
--notes, these are listed from the saved commentaries without calling the
model.
"""

import argparse
import re
import sys
from pathlib import Path

from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals

# The scripts shared with the commentaries
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "commentary" / "scripts"))

from fix_quote_blocks import ORIG_RE, TRANS_RE, rebuild_lines
from generate import CANTICLE_NAMES, LANGUAGES, same_line
from source import SOURCES, Line, Passage, carlyle_passages, source_lines

# The passages of a source printed with a prose translation
PASSAGES = {"carlyle": carlyle_passages}

# Per language of the source text: what the commentary should look at, on
# top of what every language has (forms, constructions, particles)
FOCUS = {
    "Italian": "the Old Italian and poetic forms that differ from modern Italian "
               "(verb endings, pronouns and clitics, articulated prepositions, "
               "elision and apocope, Latinisms)",
    "Ancient Greek": "the Attic, Homeric, and poetic forms and their spelling "
                     "(elision, prodelision, crasis, the augment, the dual, "
                     "the optative, the uses of the particles), and where the "
                     "translator's Greek follows the Italian construction "
                     "rather than Classical usage",
}

PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, each line followed by its translation into {lang} in parentheses. The translation is fixed: it is not to be changed.

Write, in English and in Markdown, a commentary on the grammar and usage of lines {start}–{end} of the {language} text.

- Begin with the heading `## Lines {start}–{end} — <a short title>`, the title naming what these lines say in a few words. Write no other heading.
- Go through the lines in order. Quote one sentence or clause at a time, one to four lines, and explain it right after the quote. Every line from {start} to {end} must be quoted exactly once.
- Quote each line as `> line-number original`, followed on the next line by `> (translation)`, copying both exactly from the attachment. Put consecutive lines in one quote block, separated by lines containing only `>`.
- Explain the grammar: the form of the words that need it (tense, mood, voice, person, case, number, the dictionary form), the syntax (what governs what, participles, infinitives, subordinate clauses, agreement, word order), the particles and conjunctions, and the usage of the text, especially {focus}.
- Say how the {lang} translation renders the constructions, where it renders them differently and why.
- Do not explain the content: no story, allegory, background, sources, or meter.
- Do not rewrite the translation. If it gets the grammar of a line wrong, add a paragraph opening with `Translation note:` that says what is wrong and what the line means.
""".strip()

PROSE_PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, with the {prose}, as printed page by page: each block gives the lines of a page, and then the English that renders them. The translation is fixed: it is not to be changed.

Write, in English and in Markdown, a commentary on the grammar and usage of lines {start}–{end} of the {language} text, as compared with this translation.

- Begin with the heading `## Lines {start}–{end} — <a short title>`, the title naming what these lines say in a few words. Write no other heading.
- Go through the lines in order. Quote one sentence or clause at a time, one to four lines, and explain it right after the quote. Every line from {start} to {end} must be quoted exactly once.
- Quote each line as `> line-number original`, copying it exactly from the attachment. Put consecutive lines in one quote block. Do not put the translation in the quote block.
- Explain the grammar: the form of the words that need it (tense, mood, voice, person, case, number, the dictionary form), the syntax (what governs what, participles, infinitives, subordinate clauses, agreement, word order), the particles and conjunctions, and the usage of the text, especially {focus}.
- Say how the translation renders the constructions, where it renders them differently and why. Quote its words in double quotation marks (“…”), copied exactly from the attachment; write the {language} words in italics, not in quotation marks.
- Do not explain the content: no story, allegory, background, sources, or meter.
- If the translation gets the grammar of a line wrong, add a paragraph opening with `Translation note:` that says what is wrong and what the line means.
""".strip()

SUMMARY_PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, {layout}, and a commentary on its grammar and usage.

Write, in English and in Markdown, the closing section of that commentary: the heading `## Summary — <a short title>`, followed by a few paragraphs that sum up the forms, constructions, and usages that recur in this canto, and how the translation deals with them. Quote no lines and do not explain the content (story, allegory, background, meter). Output only this section.
""".strip()

# The layout of the attachment, in SUMMARY_PROMPT
LAYOUT = "each line followed by its translation into {lang} in parentheses"
PROSE_LAYOUT = "with the {prose}, as printed page by page"

SECTION_RE = re.compile(r"^## Lines (\d+)\s*[–-]\s*(\d+)\b")
SUMMARY_HEADING = "## Summary"
NOTE_RE = re.compile(r"^Translation note:")
# A sentence ends at the end of a line with one of these, before any closing
# quote marks; the Greek ; is a question mark
SENTENCE_END = {
    "Italian": re.compile(r"[.!?][»”’\"]*$"),
    "Ancient Greek": re.compile(r"[.!?;][»”’“\"]*$"),
}
# A clause ends at the end of a line with one of these
CLAUSE_END = re.compile(r"[.!?;:·][»”’“\"]*$")

# Set the path only when usage should be recorded
USAGE_PATH = None


def sections(lines: list[Line], language: str, size: int) -> list[tuple[int, int]]:
    """Cut a canto into (start, end) line ranges of about size lines, each
    ending where a sentence ends (or a clause, if no sentence ends near
    enough), the last one at the end of the canto."""
    sentence = SENTENCE_END[language]
    result: list[tuple[int, int]] = []
    start = 1
    last = len(lines)
    while start <= last:
        if last - start + 1 <= size * 3 // 2:
            result.append((start, last))
            break
        window = range(start + size // 2, min(start + size * 3 // 2, last))
        end = None
        for pattern in (sentence, CLAUSE_END):
            ends = [no for no in window if pattern.search(lines[no - 1].text.strip())]
            if ends:
                end = min(ends, key=lambda no: abs(no - (start + size - 1)))
                break
        if end is None:
            end = start + size - 1
        result.append((start, end))
        start = end + 1
    return result


def canto_text(lines: list[Line], translations: list[str]) -> str:
    return "\n".join(
        f"{line.no} {line.text}\n({trans})" for line, trans in zip(lines, translations)
    )


def prose_text(passages: list[Passage]) -> str:
    """Page by page: the lines of a page, then its English."""
    return "\n\n".join(
        "\n".join(f"{line.no} {line.text}" for line in passage.lines)
        + f"\n\nEnglish: {passage.english}"
        for passage in passages
    )


# A quotation of the translation in the explanation
ENGLISH_QUOTE_RE = re.compile(r"“([^“”]+)”")
WORD_RE = re.compile(r"\w+")


def words(text: str) -> str:
    return " ".join(WORD_RE.findall(text.replace("’", "'").lower()))


def english_quotes(text: str, english: str) -> list[str]:
    """The quotations of two words or more in the explanations (outside the
    quote blocks) that are not in english, up to punctuation and case; a
    quotation cut with an ellipsis is checked piece by piece."""
    found = words(english)
    missing = []
    for row in text.splitlines():
        if row.startswith(">"):
            continue
        for quote in ENGLISH_QUOTE_RE.findall(row):
            for piece in re.split(r"…|\.\.\.", quote):
                if len(piece := words(piece)) and " " in piece \
                        and f" {piece} " not in f" {found} ":
                    missing.append(quote)
                    break
    return missing


def quoted_pairs(text: str) -> list[tuple[int, str, str | None]]:
    """(line number, original, translation or None) of every quoted line."""
    md = text.splitlines()
    pairs = []
    for i, row in enumerate(md):
        if orig := ORIG_RE.match(row):
            trans = TRANS_RE.match(md[i + 1]) if i + 1 < len(md) else None
            pairs.append((int(orig.group(1)), orig.group(2),
                          trans.group(1) if trans else None))
    return pairs


def check_section(text: str, start: int, end: int, lines: list[Line],
                  translations: list[str] | None, english: str = "") -> list[str]:
    """The problems of one answer; [] if it can be kept. Without
    translations, the quotes must give the originals alone, and the
    quotations of the translation must be found in english."""
    problems = []
    headings = [row for row in text.splitlines() if row.startswith("#")]
    if not headings or not (m := SECTION_RE.match(headings[0])) \
            or (int(m.group(1)), int(m.group(2))) != (start, end):
        problems.append(f"the heading is not `## Lines {start}–{end} — ...`")
    if len(headings) > 1:
        problems.append(f"{len(headings)} headings")
    pairs = quoted_pairs(text)
    numbers = [no for no, _, _ in pairs]
    if numbers != list(range(start, end + 1)):
        problems.append(f"quoted lines {numbers}, not {start}–{end} once each in order")
    for no, orig, trans in pairs:
        if not start <= no <= end:
            continue
        if not same_line(orig, lines[no - 1].text):
            problems.append(f"line {no}: the quoted original does not match")
        if translations is None:
            if trans is not None:
                problems.append(f"line {no}: a translation in the quote")
        elif trans is None:
            problems.append(f"line {no}: no translation after the quote")
        elif not same_line(trans, translations[no - 1]):
            problems.append(f"line {no}: the quoted translation does not match")
    if translations is None:
        for quote in english_quotes(text, english):
            problems.append(f"not in the translation: “{quote}”")
    return problems


def ask(client: Client, messages: list[str], check, tries: int) -> str | None:
    """The first answer with no problems, or None after tries answers."""
    for attempt in range(1, tries + 1):
        text = client(messages).text.strip()
        if not (problems := check(text)):
            return text
        print(f"\nanswer {attempt} rejected:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
    return None


def explain(client: Client, canticle: str, canto: int, args: argparse.Namespace) -> bool:
    """Write or continue <out>/<canticle>/<NN>.md; False if a section failed."""
    source = SOURCES[args.source]
    lines = source_lines(args.source, canticle, canto)
    names = dict(
        source=source["name"], language=source["language"],
        canticle=CANTICLE_NAMES[canticle], number=canto,
    )
    if "prose" in source:
        passages = PASSAGES[args.source](canto)
        translations = None
        english = " ".join(passage.english for passage in passages)
        text = prose_text(passages)
        names["prose"] = source["prose"]
        prompt_template = PROSE_PROMPT
        layout = PROSE_LAYOUT.format(prose=source["prose"])
    else:
        trans_path = args.dir / canticle / f"{canto:02d}.txt"
        translations = trans_path.read_text().splitlines()
        if len(translations) != len(lines) or not all(translations):
            print(f"{trans_path}: not one translation per line of the source, skipped",
                  file=sys.stderr)
            return False
        english = ""
        text = canto_text(lines, translations)
        names["lang"] = LANGUAGES[args.lang_code]["name"]
        prompt_template = PROMPT
        layout = LAYOUT.format(lang=names["lang"])
    originals = {line.no: line.text for line in lines}

    out_path = args.out / canticle / f"{canto:02d}.md"
    if out_path.exists():
        saved = out_path.read_text()
        if any(row.startswith(SUMMARY_HEADING) for row in saved.splitlines()):
            print(f"Skipped (already complete): {out_path}")
            return True
        print(f"Resuming from {out_path}")
    else:
        saved = f"# {CANTICLE_NAMES[canticle]} {canto}\n"
    done = {int(m.group(2)) for row in saved.splitlines() if (m := SECTION_RE.match(row))}

    def append(part: str):
        nonlocal saved
        rows = rebuild_lines(out_path, part.splitlines(), originals, translations)
        saved = saved.rstrip("\n") + "\n\n" + "\n".join(rows) + "\n"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(saved)
        print(f"\nSaved to {out_path}")

    for start, end in sections(lines, source["language"], args.size):
        if end in done:
            continue
        print(f"\n--- canto {canto}, lines {start}-{end} ---")
        prompt = prompt_template.format(**names, start=start, end=end,
                                        focus=FOCUS[source["language"]])
        answer = ask(
            client, [text, prompt],
            lambda answer: check_section(answer, start, end, lines, translations,
                                         english),
            args.tries,
        )
        if answer is None:
            print(f"\ncanto {canto}, lines {start}-{end}: no answer passed, "
                  f"canto left unfinished", file=sys.stderr)
            return False
        append(answer)

    print(f"\n--- canto {canto}, summary ---")
    prompt = SUMMARY_PROMPT.format(**names, layout=layout)
    answer = ask(
        client, [text, saved, prompt],
        lambda answer: [] if answer.startswith(f"{SUMMARY_HEADING} — ")
        else [f"does not open with `{SUMMARY_HEADING} — ...`"],
        args.tries,
    )
    if answer is None:
        print(f"\ncanto {canto}: no summary passed", file=sys.stderr)
        return False
    append(answer)
    return True


def list_notes(canticle: str, cantos, out: Path):
    """Print every `Translation note:` paragraph with the lines quoted last
    before it."""
    count = 0
    for canto in cantos:
        path = out / canticle / f"{canto:02d}.md"
        if not path.exists():
            continue
        quoted: list[int] = []
        last_quote = True
        for row in path.read_text().splitlines():
            if orig := ORIG_RE.match(row):
                if not last_quote:
                    quoted = []
                quoted.append(int(orig.group(1)))
                last_quote = True
            elif row.startswith(">"):
                pass
            else:
                if row.strip():
                    last_quote = False
                if NOTE_RE.match(row):
                    where = f"{quoted[0]}-{quoted[-1]}" if quoted else "?"
                    print(f"{path}:{where}: {row}\n")
                    count += 1
    print(f"{count} translation note(s)")


def main():
    global USAGE_PATH
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("canticle", choices=list(CANTICLE_NAMES),
                        help="Canticle name: inferno, purgatorio, or paradiso")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    parser.add_argument("-m", "--model",
                        help="Model name with optional vendor prefix (e.g. gpt-6-astra); "
                             "required unless --notes")
    parser.add_argument("-l", "--lang-code", choices=list(LANGUAGES),
                        help="Language code of the translation (e.g. el); "
                             "required unless --notes or the source has its own prose translation")
    parser.add_argument("-s", "--source", choices=list(SOURCES), default="it",
                        help="Source text to explain (default: it)")
    parser.add_argument("-d", "--dir", type=Path,
                        help="Directory holding the translations <canticle>/<NN>.txt; "
                             "required unless --notes or the source has its own prose translation")
    parser.add_argument("-o", "--out", type=Path, required=True,
                        help="Output directory for <canticle>/<NN>.md")
    parser.add_argument("--size", type=int, default=30,
                        help="Lines per section, roughly (default: 30)")
    parser.add_argument("-t", "--tries", type=int, default=3,
                        help="Answers asked for one section before giving up (default: 3)")
    parser.add_argument("-n", "--notes", action="store_true",
                        help="Only list the translation notes of the saved commentaries")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking output (include_thoughts=False)")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name")
    args = parser.parse_args()

    if err := check_canto_spec([args.canticle], args.canto):
        parser.error(err)
    if args.canticle not in SOURCES[args.source]["canticles"]:
        parser.error(f"source {args.source} has no {args.canticle}")
    cantos = select_cantos(args.canticle, args.canto)
    if args.notes:
        list_notes(args.canticle, cantos, args.out)
        return
    required = ["model"] if "prose" in SOURCES[args.source] else ["model", "lang_code", "dir"]
    for name in required:
        if getattr(args, name) is None:
            parser.error(f"--{name.replace('_', '-')} is required")

    if args.model.startswith(("openai:", "gpt-")) or args.save_usage:
        USAGE_PATH = find_usage_file()

    client = Client(
        model=args.model,
        include_thoughts=not args.no_think,
        show_params=False,
        keep_history=False,
        show_usage=True,
    )

    failed = []
    try:
        for canto in cantos:
            if not explain(client, args.canticle, canto, args):
                failed.append(canto)
    finally:
        if client.usages and USAGE_PATH is not None:
            append_usage(sum(client.usages), args.model, USAGE_PATH)

    if client.usages:
        print(f"\n--- Total Usage ---\n{sum(client.usages)}")
        if USAGE_PATH is not None:
            print()
            print_today_totals(USAGE_PATH, models=[args.model])
    if failed:
        print(f"\nunfinished cantos: {failed}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
