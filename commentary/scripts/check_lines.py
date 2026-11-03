"""
Check with an LLM that each translation (<canticle>/<NN>.txt) follows the
original line by line.

The translation must hold, on each line, what the original holds on that
line and nothing from its neighbours, even at the cost of a forced word
order. Whether a phrase has crossed a line break is a matter of meaning, so
the model reads the whole canto - each original line followed by its
translation - and reports the groups of lines that break this.

Each answer is saved as <out>/<canticle>/<NN>.json together with the
translation it was given. A canto whose saved translation still matches its
.txt is not sent again, so a run can be interrupted and resumed, and only the
cantos edited since are asked anew. Every saved answer is reported at the
end.

Only the .txt files are read; the commentaries are synced from them
afterwards with fix_quote_blocks.py.
"""

import argparse
import json
import sys
from pathlib import Path

from dante_corpus import ref
from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals
from pydantic import BaseModel, Field

CANTICLES = ["inferno", "purgatorio", "paradiso"]

CANTICLE_NAMES = {
    "inferno": "Inferno",
    "purgatorio": "Purgatorio",
    "paradiso": "Paradiso",
}

PROMPT = """
Attached are the Italian text of canto {number} of Dante's Divine Comedy, {canticle}, and its translation into {lang}. Each line number is followed by the original line and, on the next line, its translation.

The translation must follow the original line by line: each translated line must render what its own original line says, and nothing from another line, even if the word order becomes forced. Find every place where this does not hold:

- a word or phrase of one original line rendered on another line (carried over the line break, in either direction)
- part of a line's content missing from its translation, or a translation adding content that belongs to no line
- a translation that renders a different line altogether (lines shifted)

Do not report word choice, style, or accuracy within a line, nor the order of words inside a line. Report each problem once, listing every line involved; if there is none, return an empty list.
""".strip()


class Issue(BaseModel):
    lines: list[int] = Field(description="Numbers of all the lines involved, e.g. [133, 134]")
    problem: str = Field(description="What has moved or is missing, quoting the words concerned in the original and in the translation")


class Result(BaseModel):
    issues: list[Issue]


# Set the path only when usage should be recorded
USAGE_PATH = None


def paired_text(lines, translations: list[str]) -> str:
    return "\n".join(
        f"{line.no} {line.text}\n{line.no} {trans}"
        for line, trans in zip(lines, translations)
    )


def check(client: Client, canticle: str, canto: int, args: argparse.Namespace):
    txt_path = args.dir / canticle / f"{canto:02d}.txt"
    if not txt_path.exists():
        return
    translations = txt_path.read_text().splitlines()
    out_path = args.out / canticle / f"{canto:02d}.json"
    if out_path.exists():
        saved = json.loads(out_path.read_text())
        if saved["translations"] == translations:
            return
    lines = ref(f"{canticle} {canto}")
    prompt = PROMPT.format(
        canticle=CANTICLE_NAMES[canticle], number=canto, lang=args.lang_name
    )
    print(f"\n=== {canticle} {canto} ===")
    response = client([paired_text(lines, translations), prompt], Result)
    result = Result.model_validate_json(response.text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(
        {"translations": translations,
         "issues": [issue.model_dump() for issue in result.issues]},
        ensure_ascii=False, indent=1,
    ) + "\n")


def report(canticle: str, canto: int, args: argparse.Namespace) -> int:
    """Print the saved issues of one canto; return how many there are."""
    txt_path = args.dir / canticle / f"{canto:02d}.txt"
    out_path = args.out / canticle / f"{canto:02d}.json"
    if not out_path.exists():
        return 0
    saved = json.loads(out_path.read_text())
    stale = txt_path.exists() and saved["translations"] != txt_path.read_text().splitlines()
    for issue in saved["issues"]:
        nums = sorted(issue["lines"])
        span = f"{nums[0]}" if len(nums) == 1 else f"{nums[0]}-{nums[-1]}"
        print(f"{txt_path}: {span}{' (stale)' if stale else ''}: {issue['problem']}")
    return len(saved["issues"])


def main():
    global USAGE_PATH
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("canticles", nargs="*", metavar="canticle", choices=CANTICLES,
                        help="Canticles to check (default: all)")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    parser.add_argument("-m", "--model",
                        help="Model name with optional vendor prefix (e.g. gpt-6-astra); "
                             "required unless --report")
    parser.add_argument("-L", "--lang-name",
                        help="Name of the target language, as written into the prompt "
                             "(e.g. 'Modern Greek'); required unless --report")
    parser.add_argument("-d", "--dir", type=Path, required=True,
                        help="Directory holding <canticle>/<NN>.txt (e.g. el)")
    parser.add_argument("-o", "--out", type=Path, required=True,
                        help="Directory for the saved answers, <out>/<canticle>/<NN>.json")
    parser.add_argument("-r", "--report", action="store_true",
                        help="Only report the saved answers, without calling the model")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking output (include_thoughts=False)")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name")
    args = parser.parse_args()
    canticles = args.canticles or CANTICLES
    if err := check_canto_spec(canticles, args.canto):
        parser.error(err)
    if not args.report and not (args.model and args.lang_name):
        parser.error("-m/--model and -L/--lang-name are required unless --report")

    cantos = [(canticle, canto) for canticle in canticles
              for canto in select_cantos(canticle, args.canto)]

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
