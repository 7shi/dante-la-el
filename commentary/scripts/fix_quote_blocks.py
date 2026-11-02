"""
Rebuild the block-quote pairs in a commentary (e.g. el/inferno/01.md) from
the sources of truth, instead of trusting whatever text already sits in the
quote block:

    > 1 Nel mezzo del cammin di nostra vita
    > (Στη μέση του δρόμου της ζωής μας)

The original comes from dante_corpus, the translation from the sibling
<canticle>/<NN>.txt file (same line numbering, one verse per physical line).
A file whose sibling .txt is missing is skipped entirely and reported once.

For each quote block (a maximal run of lines starting with ">") in a file
that has a sibling .txt:

1. Flatten the block to a string.
2. If it opens with `> <line-number> ...`, find the lowest and highest
   quoted line numbers.
3. Rebuild every numbered pair from dante_corpus and the .txt file, in the
   canonical layout (original line ends with a two-space hard break,
   translation follows with no trailing spaces). Anything else in the
   block — separators, gaps where lines are skipped, unnumbered lines — is
   left untouched.
4. Compare the rebuilt block against the original string; rewrite the file
   only if something differs.
5. Report, per file, whether it was rewritten.

A pair whose translation line is missing, or a line number out of range for
the source text, is left as-is and reported as a warning.
"""

import argparse
import re
import sys
from pathlib import Path

from dante_corpus.api import canto

CANTICLES = ["inferno", "purgatorio", "paradiso"]

ORIG_RE = re.compile(r"^>\s*(\d+)[.:)]?\s+(.*?)\s*$")
TRANS_RE = re.compile(r"^>\s*\((.*)\)\s*$")
PATH_RE = re.compile(r"(?:^|/)(inferno|purgatorio|paradiso)/(\d+)\.md$")

SEPARATOR = ">"


def find_blocks(lines: list[str]) -> list[tuple[int, int]]:
    """[start, end) index ranges of maximal runs of lines starting with '>'."""
    blocks = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith(">"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                j += 1
            blocks.append((i, j))
            i = j
        else:
            i += 1
    return blocks


def rebuild_block(path: Path, canticle: str, number: int,
                   translations: list[str], block: list[str]) -> list[str] | None:
    """Rebuild one quote block from dante_corpus + the sibling .txt.

    Returns None if the block doesn't open with a numbered original line."""
    if not ORIG_RE.match(block[0]):
        return None

    numbers = [int(mm.group(1)) for line in block if (mm := ORIG_RE.match(line))]
    start, end = min(numbers), max(numbers)
    try:
        originals = {line.no: line.text for line in canto(canticle, number).lines(start, end)}
    except ValueError as e:
        print(f"{path}: {e}, block left as-is", file=sys.stderr)
        return None

    out: list[str] = []
    i = 0
    while i < len(block):
        orig = ORIG_RE.match(block[i])
        if not orig:
            out.append(block[i])
            i += 1
            continue
        n = int(orig.group(1))
        trans = TRANS_RE.match(block[i + 1]) if i + 1 < len(block) else None
        if not trans:
            print(f"{path}: line {n} has no translation on the next line, "
                  f"left as-is", file=sys.stderr)
            out.append(block[i])
            i += 1
            continue
        if n not in originals or not (1 <= n <= len(translations)):
            print(f"{path}: line {n} out of range for the source text, "
                  f"left as-is", file=sys.stderr)
            out.append(block[i])
            out.append(block[i + 1])
            i += 2
            continue
        out.append(f"> {n} {originals[n]}  ")
        out.append(f"> ({translations[n - 1]})")
        i += 2
        # Insert exactly one blank quote line between this pair and the next
        # one when the source had none; an existing separator (or a gap that
        # runs into prose) is preserved as-is by the pass-through branch above.
        if i < len(block) and ORIG_RE.match(block[i]):
            out.append(SEPARATOR)
    return out


def normalize_file(path: Path, dry_run: bool) -> bool:
    """Rewrite the quote blocks of one commentary from dante_corpus + its
    sibling .txt. True if changed; False (with a warning) if the file has no
    sibling .txt or its canticle/canto can't be resolved from its path."""
    m = PATH_RE.search(path.as_posix())
    if not m:
        print(f"{path}: can't resolve canticle/canto from path, file left as-is",
              file=sys.stderr)
        return False
    canticle, number = m.group(1), int(m.group(2))

    txt_path = path.with_suffix(".txt")
    if not txt_path.exists():
        print(f"{path}: no sibling {txt_path.name}, file left as-is", file=sys.stderr)
        return False
    translations = txt_path.read_text(encoding="utf-8").splitlines()

    lines = path.read_text().splitlines()
    out = list(lines)
    changed = False
    # Back to front: a rebuilt block can be longer than the original (a
    # missing separator is inserted), which would shift every later block's
    # position in out and overwrite the prose between them.
    for start, end in reversed(find_blocks(lines)):
        block = lines[start:end]
        rebuilt = rebuild_block(path, canticle, number, translations, block)
        if rebuilt is not None and rebuilt != block:
            out[start:end] = rebuilt
            changed = True

    if not changed:
        return False
    if not dry_run:
        path.write_text("\n".join(out) + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("-d", "--dir", dest="dirs", action="append", type=Path,
                        required=True, metavar="DIR",
                        help="Directory holding <canticle>/<NN>.md files (e.g. el); "
                             "repeatable")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Report the changes without writing them back")
    args = parser.parse_args()

    paths = [
        path
        for dir in args.dirs
        for canticle in CANTICLES
        for path in sorted((dir / canticle).glob("*.md"))
    ]
    if not paths:
        parser.error("no <canticle>/*.md files found under the given directories")

    rewritten = 0
    for path in paths:
        if normalize_file(path, args.dry_run):
            print(f"{'Would rewrite' if args.dry_run else 'Rewrote'} {path}")
            rewritten += 1
    print(f"\n{rewritten} file(s) "
          + ("would change" if args.dry_run else "rewritten")
          + f" out of {len(paths)}")


if __name__ == "__main__":
    main()
