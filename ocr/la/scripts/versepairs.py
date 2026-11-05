"""The verse of the cantos in texts/la, the Italian and the Latin line side by side.

For the text-only comparison of the verse check (ocr/la/PLAN.md, "Verse check", step 0):
each Latin line beside the Italian line it translates, so that a reader can list the
places where the two clearly part in sense. One TSV per canto (or one file with -o):

    canto  page  tercet  line  italian  latin

`page` is the scan page (ocr/la/PAGE.txt) of the Latin tercet. A tercet whose two columns
differ in line count, or that has one column only, is written with the missing lines
empty; these are listed on stderr too.
"""
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXTS = ROOT / "texts" / "la"
PAGE = re.compile(r"<!-- p\. .*\((\d+)\) -->")
HEAD = re.compile(r"^(\d+) (.*)$")


def clean(s):
    s = s.rstrip()
    if s.endswith("\\"):
        s = s[:-1]
    return s.replace("&emsp;", "").strip()


def blocks(path):
    """(scan page, tercet number, lines) for every verse block of a canto file."""
    page, cur, out = None, None, []
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = PAGE.match(line)
        if m:
            page = m.group(1)
            continue
        if cur is not None:
            if line.startswith("&emsp;"):
                cur[2].append(clean(line))
                continue
            out.append(tuple(cur))
            cur = None
        m = HEAD.match(line)
        if m and line.rstrip().endswith("\\"):
            cur = [page, int(m.group(1)), [clean(m.group(2))]]
    if cur is not None:
        out.append(tuple(cur))
    return out


def pairs(path):
    """Rows (page, tercet, line, italian, latin) and the problems found."""
    bs = blocks(path)
    rows, problems = [], []
    i = 0
    while i < len(bs):
        page, n, it = bs[i]
        if i + 1 < len(bs) and bs[i + 1][1] == n:
            lpage, _, la = bs[i + 1]
            i += 2
        else:
            lpage, la = page, []
            problems.append(f"{path.name}: tercet {n}: one column only")
            i += 1
        if la and len(it) != len(la):
            problems.append(f"{path.name}: tercet {n}: {len(it)} Italian, {len(la)} Latin lines")
        for k in range(max(len(it), len(la))):
            rows.append((lpage, n, k + 1, it[k] if k < len(it) else "",
                         la[k] if k < len(la) else ""))
    return rows, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", help="texts/la canto files (default: all cantos)")
    ap.add_argument("-d", "--outdir", help="one CANTO.tsv per canto in this directory")
    ap.add_argument("-o", "--output", help="all cantos in one file")
    a = ap.parse_args()
    files = [Path(f) for f in a.files] or sorted(TEXTS.glob("*-canto-*.md"))
    out = open(a.output, "w", encoding="utf-8") if a.output else None
    if a.outdir:
        Path(a.outdir).mkdir(parents=True, exist_ok=True)
    total = 0
    for f in files:
        canto = f.stem
        rows, problems = pairs(f)
        for p in problems:
            print(p, file=sys.stderr)
        lines = ["canto\tpage\ttercet\tline\titalian\tlatin"] if a.outdir else []
        lines += ["\t".join([canto, *map(str, r)]) for r in rows]
        if a.outdir:
            (Path(a.outdir) / f"{canto}.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        elif out:
            out.write("\n".join(lines) + "\n")
        else:
            sys.stdout.write("\n".join(lines) + "\n")
        total += len(rows)
    print(f"{len(files)} cantos, {total} lines", file=sys.stderr)


if __name__ == "__main__":
    main()
