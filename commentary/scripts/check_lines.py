"""
Check with an LLM that each translation (<canticle>/<NN>.txt) follows the
original line by line, and apply the fixes it proposes.

The translation must hold, on each line, what the original holds on that
line and nothing from its neighbours, even at the cost of a forced word
order. Whether a phrase has crossed a line break is a matter of meaning, so
the model reads the whole canto - each original line followed by its
translation - and reports every group of lines that breaks this, with its
kind and a rewritten translation of the lines involved:

- moved: a content word or phrase rendered on another line
- function: a function word, auxiliary, clitic, or degree word on another
  line; often forced by the grammar of the target language
- missing: part of a line's content not rendered
- added: content in the translation that belongs to no line

The fix is left empty when the lines cannot follow the original without
breaking the grammar; the problem then says why. Nothing is excluded at
report time: whether to apply a fix is decided afterwards, by kind and by
reading it against the original.

Each answer is saved as <out>/<canticle>/<NN>.json together with the
translation it was given. A canto whose saved translation still matches its
.txt is not sent again, so a run can be interrupted and resumed, and only the
cantos edited since are asked anew. Every saved answer is reported at the
end, with its fix.

--apply writes the fixes of the saved, up-to-date answers into the .txt
files, limited to the kinds given by --kind. A fix is applied only if it
rewrites nothing but the lines of its issue, every rewritten line has a
letter of the target language, the quote marks still follow the original
(as check_quotes.py checks them), and no fix applied before it in the same
canto has touched its lines; the others are reported and left out. The
cantos changed are then stale and asked anew on the next run.

Only the .txt files are read; the commentaries are synced from them
afterwards with fix_quote_blocks.py.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Literal

from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals
from pydantic import BaseModel, Field

from check_quotes import runs
from generate import CANTICLE_NAMES, LANGUAGES
from source import SOURCES, TRANSLATED_SOURCES, source_lines

CANTICLES = list(CANTICLE_NAMES)
KINDS = ["moved", "function", "missing", "added"]

PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, and its translation into {lang}. Each line number is followed by the original line and, on the next line, its translation.

The translation must follow the original line by line: each translated line must render what its own original line says, and nothing from another line, even if the word order becomes forced. Find every place where this does not hold, and classify it:

- moved: a content word or phrase of one original line rendered on another line (carried over the line break, in either direction)
- function: a function word, auxiliary verb, clitic pronoun, or degree word{degree} rendered on another line; report these too, even where the grammar of {lang} seems to force it
- missing: part of a line's content not rendered in its translation
- added: content in a translation that belongs to no line of the original

Do not report word choice, style, or accuracy within a line, nor the order of words inside a line. Report each problem once, listing every line involved; if there is none, return an empty list.

For each problem, give a fix: the rewritten translation of every line involved, so that each holds what its own original line holds. Change only what the problem requires, keeping the wording and style of the existing translation otherwise; keep quotation marks on the same lines as the original.{note} If the lines cannot follow the original without breaking the grammar of {lang}, leave the fix empty and say why in the problem.
""".strip()


class LineFix(BaseModel):
    line: int = Field(description="Line number")
    translation: str = Field(description="The rewritten translation of that line")


class Issue(BaseModel):
    lines: list[int] = Field(description="Numbers of all the lines involved, e.g. [133, 134]")
    kind: Literal["moved", "function", "missing", "added"]
    problem: str = Field(description="What has moved or is missing, quoting the words concerned in the original and in the translation; if no fix is given, why")
    fix: list[LineFix] = Field(description="Rewritten translation of each line involved; empty if the lines cannot follow the original without breaking the grammar")


class Result(BaseModel):
    issues: list[Issue]


# Examples of degree words in the prompt, per source
DEGREE_WORDS = {
    "it": ' (such as "sì", "tanto")',
    "grc": ' (such as "οὕτως", "τοσοῦτον")',
    "la-la": ' (such as "sic", "tantum")',
    "la-it": ' (such as "sì", "tanto")',
}

# Set the path only when usage should be recorded
USAGE_PATH = None


def paired_text(lines, translations: list[str]) -> str:
    return "\n".join(
        f"{line.no} {line.text}\n{line.no} {trans}"
        for line, trans in zip(lines, translations)
    )


def paths(canticle: str, canto: int, args: argparse.Namespace) -> tuple[Path, Path]:
    return (args.dir / canticle / f"{canto:02d}.txt",
            args.out / canticle / f"{canto:02d}.json")


def load(canticle: str, canto: int, args: argparse.Namespace):
    """(translations, saved answer or None, whether the answer is stale)."""
    txt_path, out_path = paths(canticle, canto, args)
    if not txt_path.exists():
        return None, None, False
    translations = txt_path.read_text().splitlines()
    if not out_path.exists():
        return translations, None, False
    saved = json.loads(out_path.read_text())
    return translations, saved, saved["translations"] != translations


def check(client: Client, canticle: str, canto: int, args: argparse.Namespace):
    translations, saved, stale = load(canticle, canto, args)
    if translations is None or (saved is not None and not stale):
        return
    lines = source_lines(args.source, canticle, canto)
    language = LANGUAGES[args.lang_code]
    note = f" {language['note']}" if language.get("note") else ""
    prompt = PROMPT.format(
        canticle=CANTICLE_NAMES[canticle], number=canto, lang=language["name"], note=note,
        source=SOURCES[args.source]["name"], degree=DEGREE_WORDS[args.source],
    )
    print(f"\n=== {canticle} {canto} ===")
    response = client([paired_text(lines, translations), prompt], Result)
    result = Result.model_validate_json(response.text)
    _, out_path = paths(canticle, canto, args)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(
        {"model": args.model,
         "translations": translations,
         "issues": [issue.model_dump() for issue in result.issues]},
        ensure_ascii=False, indent=1,
    ) + "\n")


def span(nums: list[int]) -> str:
    nums = sorted(nums)
    return f"{nums[0]}" if len(nums) == 1 else f"{nums[0]}-{nums[-1]}"


def report(canticle: str, canto: int, args: argparse.Namespace) -> int:
    """Print the saved issues of one canto; return how many were printed."""
    translations, saved, stale = load(canticle, canto, args)
    if saved is None:
        return 0
    txt_path, _ = paths(canticle, canto, args)
    printed = 0
    for issue in saved["issues"]:
        if args.kind and issue["kind"] not in args.kind:
            continue
        print(f"{txt_path}: {span(issue['lines'])} [{issue['kind']}]"
              f"{' (stale)' if stale else ''}: {issue['problem']}")
        for fix in issue["fix"]:
            no = fix["line"]
            old = translations[no - 1] if 1 <= no <= len(translations) else "?"
            print(f"    {no} - {old}\n    {no} + {fix['translation']}")
        printed += 1
    return printed


def apply(canticle: str, canto: int, args: argparse.Namespace) -> tuple[int, int]:
    """Apply the fixes of one canto's up-to-date answer; return (applied, rejected)."""
    translations, saved, stale = load(canticle, canto, args)
    if saved is None or stale:
        return 0, 0
    txt_path, _ = paths(canticle, canto, args)
    language = LANGUAGES[args.lang_code]
    letters = re.compile(language["letters"])
    current = list(translations)
    touched: set[int] = set()
    applied = rejected = 0
    for issue in saved["issues"]:
        if args.kind and issue["kind"] not in args.kind:
            continue
        where = f"{txt_path}: {span(issue['lines'])} [{issue['kind']}]"
        fixes = {fix["line"]: fix["translation"].strip() for fix in issue["fix"]}
        reason = None
        if not fixes:
            reason = "no fix given"
        elif not set(fixes) <= set(issue["lines"]):
            reason = f"fix rewrites lines outside the issue: {sorted(set(fixes) - set(issue['lines']))}"
        elif not all(1 <= no <= len(current) for no in fixes):
            reason = "line number out of range"
        elif set(fixes) & touched:
            reason = "lines already changed by an earlier fix"
        elif not all(letters.search(text) for text in fixes.values()):
            reason = "a rewritten line has no letter of the target language"
        else:
            candidate = list(current)
            for no, text in fixes.items():
                candidate[no - 1] = text
            before = {no for first, last in runs(canticle, canto, current, language, args.source)
                      for no in range(first, last + 1)}
            after = {no for first, last in runs(canticle, canto, candidate, language, args.source)
                     for no in range(first, last + 1)}
            if after - before:
                reason = f"quote marks no longer follow the original at {span(sorted(after - before))}"
        if reason:
            print(f"{where}: skipped, {reason}")
            rejected += 1
            continue
        for no, text in sorted(fixes.items()):
            print(f"{where}: {no} - {current[no - 1]}")
            print(f"{where}: {no} + {text}")
            current[no - 1] = text
        touched |= set(fixes)
        applied += 1
    if current != translations:
        txt_path.write_text("\n".join(current) + "\n")
    return applied, rejected


def main():
    global USAGE_PATH
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("canticles", nargs="*", metavar="canticle", choices=CANTICLES,
                        help="Canticles to check (default: all)")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    parser.add_argument("-m", "--model",
                        help="Model name with optional vendor prefix (e.g. gpt-6.2-astra); "
                             "required to ask the model")
    parser.add_argument("-l", "--lang-code", choices=list(LANGUAGES),
                        help="Language code of the target language (e.g. el); "
                             "required to ask the model or to apply")
    parser.add_argument("-s", "--source", choices=TRANSLATED_SOURCES, default="it",
                        help="Source text the translations follow (default: it)")
    parser.add_argument("-d", "--dir", type=Path, required=True,
                        help="Directory holding <canticle>/<NN>.txt (e.g. el)")
    parser.add_argument("-o", "--out", type=Path, required=True,
                        help="Directory for the saved answers, <out>/<canticle>/<NN>.json")
    parser.add_argument("-r", "--report", action="store_true",
                        help="Only report the saved answers, without calling the model")
    parser.add_argument("-a", "--apply", action="store_true",
                        help="Apply the fixes of the saved, up-to-date answers to the .txt "
                             "files, without calling the model")
    parser.add_argument("-k", "--kind", action="append", choices=KINDS,
                        help="Report or apply only issues of this kind (repeatable; "
                             "default: all to report, required to apply)")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking output (include_thoughts=False)")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name")
    args = parser.parse_args()
    canticles = args.canticles or SOURCES[args.source]["canticles"]
    if err := check_canto_spec(canticles, args.canto):
        parser.error(err)
    if missing := set(canticles) - set(SOURCES[args.source]["canticles"]):
        parser.error(f"source {args.source} has no {', '.join(sorted(missing))}")
    if args.report and args.apply:
        parser.error("--report and --apply cannot be combined")
    if args.apply and not (args.lang_code and args.kind):
        parser.error("--apply requires -l/--lang-code and -k/--kind")
    if not args.report and not args.apply and not (args.model and args.lang_code):
        parser.error("-m/--model and -l/--lang-code are required "
                     "unless --report or --apply")

    cantos = [(canticle, canto) for canticle in canticles
              for canto in select_cantos(canticle, args.canto)]

    if args.apply:
        applied = rejected = 0
        for canticle, canto in cantos:
            a, r = apply(canticle, canto, args)
            applied += a
            rejected += r
        print(f"\n{applied} fix(es) applied, {rejected} skipped")
        return

    client = None
    if not args.report:
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
            for canticle, canto in cantos:
                check(client, canticle, canto, args)
        finally:
            if client.usages and USAGE_PATH is not None:
                append_usage(sum(client.usages), args.model, USAGE_PATH)
        print()

    issues = sum(report(canticle, canto, args) for canticle, canto in cantos)
    print(f"\n{issues} issue(s)")

    if client is not None and client.usages:
        print(f"\n--- Total Usage ---\n{sum(client.usages)}")
        if USAGE_PATH is not None:
            print()
            print_today_totals(USAGE_PATH, models=[args.model])


if __name__ == "__main__":
    main()
