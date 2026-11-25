"""
Rebuild the block-quote pairs in a commentary (e.g. el/inferno/01.md) from
the sources of truth, instead of trusting whatever text already sits in the
quote block:

    > 1 Nel mezzo del cammin di nostra vita
    > (Στη μέση του δρόμου της ζωής μας)

The original comes from dante_corpus (or another source of source.py, with
-s), the translation from the sibling <canticle>/<NN>.txt file (same line
numbering, one verse per physical line), or from <canticle>/<NN>.txt under
the directory given with -t (for the grammar commentaries of grammar.py,
which are kept apart from the translations). A file whose .txt is missing is
skipped entirely and reported once. A source printed with a prose
translation of its own (en, en-oelsner, en-purgatorio, en-paradiso) has no
.txt: its commentaries, named as its files in texts/ (as 007-canto-01.md),
quote the originals alone, `> N original` with the two-space hard break, and
only these are rebuilt.

For each quote block (a maximal run of lines starting with ">") in a file
that has a sibling .txt:

1. Flatten the block to a string.
2. If it opens with `> <line-number> ...`, find the lowest and highest
   quoted line numbers.
3. Rebuild every numbered pair from the source and the .txt file, in the
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

from source import SOURCES, en_grc_lines, oelsner_lines, source_lines

CANTICLES = ["inferno", "purgatorio", "paradiso"]

ORIG_RE = re.compile(r"^>\s*(\d+)[.:)]?\s+(.*?)\s*$")
# Punctuation after the closing paren: the model sometimes moves a trailing
# comma of the original outside, as in `> («...»),`
TRANS_RE = re.compile(r"^>\s*\((.*)\)[,.;:!?·»”’]*\s*$")
PATH_RE = re.compile(r"(?:^|/)(inferno|purgatorio|paradiso)/(\d+)\.md$")
# A commentary on a source printed with a prose translation, named as in texts/
TEXT_NAME_RE = re.compile(r"-canto-(\d+)\.md$")

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


def rebuild_block(path: Path, originals: dict[int, str],
                  translations: list[str] | None, block: list[str]) -> list[str] | None:
    """Rebuild one quote block from the source lines + the .txt lines (or
    the source lines alone, if translations is None).

    Returns None if the block doesn't open with a numbered original line."""
    if not ORIG_RE.match(block[0]):
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
        if translations is None:
            if n not in originals:
                print(f"{path}: line {n} out of range for the source text, "
                      f"left as-is", file=sys.stderr)
                out.append(block[i])
            else:
                out.append(f"> {n} {originals[n]}  ")
            i += 1
            continue
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


def rebuild_lines(path: Path, lines: list[str], originals: dict[int, str],
                  translations: list[str] | None) -> list[str]:
    """Every quote block of a commentary (its lines) rebuilt."""
    out = list(lines)
    # Back to front: a rebuilt block can be longer than the original (a
    # missing separator is inserted), which would shift every later block's
    # position in out and overwrite the prose between them.
    for start, end in reversed(find_blocks(lines)):
        block = lines[start:end]
        rebuilt = rebuild_block(path, originals, translations, block)
        if rebuilt is not None:
            out[start:end] = rebuilt
    return out


def normalize_file(path: Path, source: str, trans_dir: Path | None,
                   dry_run: bool) -> bool:
    """Rewrite the quote blocks of one commentary from the source + its .txt.
    True if changed; False (with a warning) if the file has no .txt or its
    canticle/canto can't be resolved from its path."""
    grc_en = source == "grc" and trans_dir is None and bool(TEXT_NAME_RE.search(path.name))
    if "prose" in SOURCES[source] or grc_en:
        m = TEXT_NAME_RE.search(path.name)
        canticle = SOURCES[source]["canticles"][0]
        number = int(m.group(1)) if m else 0
    elif m := PATH_RE.search(path.as_posix()):
        canticle, number = m.group(1), int(m.group(2))
    if not m:
        print(f"{path}: can't resolve canticle/canto from path, file left as-is",
              file=sys.stderr)
        return False

    if grc_en:
        try:
            it_originals = {line.no: line.text for line in oelsner_lines(number)}
            grc_originals = {line.no: line.text
                             for line in source_lines("grc", canticle, number)}
            grc_translations = [line.text for line in en_grc_lines(number)]
        except ValueError as e:
            print(f"{path}: {e}, file left as-is", file=sys.stderr)
            return False
        lines = path.read_text().splitlines()
        out = list(lines)
        for start, end in reversed(find_blocks(lines)):
            block = lines[start:end]
            if not ORIG_RE.match(block[0]):
                continue
            has_trans = len(block) > 1 and bool(TRANS_RE.match(block[1]))
            rebuilt = rebuild_block(
                path,
                grc_originals if has_trans else it_originals,
                grc_translations if has_trans else None,
                block,
            )
            if rebuilt is not None:
                out[start:end] = rebuilt
        if out == lines:
            return False
        if not dry_run:
            path.write_text("\n".join(out) + "\n")
        return True

    if "prose" in SOURCES[source]:
        translations = None
    else:
        if trans_dir is None:
            txt_path = path.with_suffix(".txt")
        else:
            txt_path = trans_dir / canticle / f"{number:02d}.txt"
        if not txt_path.exists():
            print(f"{path}: no {txt_path}, file left as-is", file=sys.stderr)
            return False
        translations = txt_path.read_text(encoding="utf-8").splitlines()
    try:
        originals = {line.no: line.text
                     for line in source_lines(source, canticle, number)}
    except ValueError as e:
        print(f"{path}: {e}, file left as-is", file=sys.stderr)
        return False

    lines = path.read_text().splitlines()
    out = rebuild_lines(path, lines, originals, translations)
    if out == lines:
        return False
    if not dry_run:
        path.write_text("\n".join(out) + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("-d", "--dir", dest="dirs", action="append", type=Path,
                        required=True, metavar="DIR",
                        help="Directory holding <canticle>/<NN>.md files (e.g. el), "
                             "or the files named as in texts/ for a source with "
                             "its own prose translation; repeatable")
    parser.add_argument("-s", "--source", choices=list(SOURCES), default="it",
                        help="Source text of the quoted originals (default: it)")
    parser.add_argument("-t", "--translations", type=Path, metavar="DIR",
                        help="Directory holding <canticle>/<NN>.txt "
                             "(default: next to each <NN>.md)")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Report the changes without writing them back")
    args = parser.parse_args()

    if "prose" in SOURCES[args.source] or (args.source == "grc" and args.translations is None):
        paths = [path for dir in args.dirs for path in sorted(dir.glob("*-canto-*.md"))]
    else:
        paths = [
            path
            for dir in args.dirs
            for canticle in CANTICLES
            for path in sorted((dir / canticle).glob("*.md"))
        ]
    if not paths:
        parser.error("no commentaries found under the given directories")

    rewritten = 0
    for path in paths:
        if normalize_file(path, args.source, args.translations, args.dry_run):
            print(f"{'Would rewrite' if args.dry_run else 'Rewrote'} {path}")
            rewritten += 1
    print(f"\n{rewritten} file(s) "
          + ("would change" if args.dry_run else "rewritten")
          + f" out of {len(paths)}")


if __name__ == "__main__":
    main()
