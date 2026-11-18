"""Extract proper-name translations for a given Inferno canto.

Uses `texts/en/PROPER_NAMES.tsv` (canto:line index) and
`translations/ja/PROPER_NAMES.tsv` (Japanese renderings) to list the proper
names appearing in a target canto for inclusion in translation prompts.

    python3 translations/scripts/proper_names.py 1
    python3 translations/scripts/proper_names.py texts/en-oelsner/002-canto-01.md
    python3 translations/scripts/proper_names.py 1 --tsv
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EN = ROOT / "texts/en/PROPER_NAMES.tsv"
DEFAULT_JA = ROOT / "translations/ja/PROPER_NAMES.tsv"


def parse_canto(target: str) -> int:
    """Parse a canto number from an integer string or a filename like 002-canto-01.md."""
    if target.isdigit():
        canto = int(target)
    else:
        m = re.search(r"canto-(\d+)", Path(target).stem)
        if not m:
            raise ValueError(f"cannot determine canto number from {target!r}")
        canto = int(m.group(1))
    if not 1 <= canto <= 34:
        raise ValueError(f"canto number out of range (1-34): {canto}")
    return canto


def load_ja(path: Path) -> dict[str, list[str]]:
    """Load name -> list of Japanese forms from PROPER_NAMES.tsv."""
    mapping: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        name = parts[0]
        forms = [p for p in parts[1:] if p]
        mapping[name] = forms
    return mapping


def canto_names(en_path: Path, ja_path: Path, canto: int) -> list[tuple[str, list[str]]]:
    """Return (name, ja_forms) pairs whose references include `canto`."""
    ja_map = load_ja(ja_path)
    results: list[tuple[str, list[str]]] = []
    for line in en_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        name, _, refs_str = line.partition("\t")
        cantos = {int(ref.split(":", 1)[0]) for ref in refs_str.split(",") if ":" in ref}
        if canto in cantos:
            results.append((name, ja_map.get(name, [])))
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("target", help="canto number (1-34) or canto filename (e.g. 002-canto-01.md)")
    ap.add_argument("--en", type=Path, default=DEFAULT_EN, help="path to texts/en/PROPER_NAMES.tsv")
    ap.add_argument("--ja", type=Path, default=DEFAULT_JA, help="path to translations/ja/PROPER_NAMES.tsv")
    ap.add_argument("--tsv", action="store_true", help="output as TSV instead of prompt list")
    a = ap.parse_args()

    try:
        canto = parse_canto(a.target)
    except ValueError as e:
        sys.exit(f"error: {e}")

    entries = canto_names(a.en, a.ja, canto)
    for name, forms in entries:
        if a.tsv:
            print("\t".join([name, *forms]))
        else:
            rendered = " / ".join(forms) if forms else "(未登録)"
            print(f"- {name}: {rendered}")


if __name__ == "__main__":
    main()
