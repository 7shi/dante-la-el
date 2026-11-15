"""The Italian verse of a converted Temple Classics volume against the standard text, word
by word: the near misses, to be decided in the image.

    uv run ocr/scripts/stdcmp.py paradiso [-o OUT] [--accents] [--ratio R] [--max N]

The verse of each canto of `texts/en-oelsner/` (inferno), `texts/en-purgatorio/` or
`texts/en-paradiso/` (the even pages up to `## Notes`, with the canto's last line) is
aligned line by line with dante-corpus (the counts must agree) and word by word within the
line. A word is listed when it was replaced by a standard word that it resembles (difflib
ratio at least R, default 0.75) and it occurs at most N times (default 2) in the Italian of
the three volumes: a rare form one or two letters from the standard one. Differences of
accents alone (the diaeresis, the grave) are left out unless --accents is given.

The standard text only points: almost every word listed is the edition's own reading
(`diliberarti`, `sospicar`); each is read in the image, and only what is clearly wrong is a
misprint (the rhyme, a form Italian does not have). The converted text gives the misprints
already marked in their fixed form, so a marked place is not listed again. Each row:
`CANTO:VERSE  SCAN:LINE  printed  standard  count  line`, SCAN:LINE the line in
`ocr/DIR/SCAN.txt` (`?` when not found).

Made for ocr/en-paradiso, step 7 (2026-11-15), and run on the other two volumes: it found
two misprints in the Paradiso and three in the Inferno that every reading and the
read-through had passed.
"""
import argparse
import difflib
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import dante_corpus as dc

ROOT = Path(__file__).resolve().parents[2]
VOLUMES = {"inferno": (0, "en-oelsner"), "purgatorio": (1, "en-purgatorio"),
           "paradiso": (2, "en-paradiso")}
WORD = re.compile(r"[A-Za-zÀ-ÿ]+")
MARKER = re.compile(r"<!-- p\. (\d+) \((\d+)\)(, \w+)? -->")


def words(s):
    return [w.lower() for w in WORD.findall(s)]


def plain(w):
    return "".join(c for c in unicodedata.normalize("NFD", w) if not unicodedata.combining(c))


def verses(path):
    """The verse lines of a canto file, each with the scan it is printed on."""
    out, on, scan, prev = [], False, None, ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Notes"):
            break
        m = MARKER.match(line)
        if m:
            on = m.group(3) in (None, ", text") and int(m.group(1)) % 2 == 0
            scan = m.group(2)
            continue
        if line.startswith("<!--"):
            on = False
            continue
        keep = on and (line.endswith("\\") or line.startswith("&emsp;")
                       or (line.strip() and prev.endswith("\\")))
        prev = line
        if keep:
            s = re.sub(r"<!--.*?-->", "", line).replace("&emsp;", "").rstrip("\\").rstrip()
            out.append((re.sub(r"\s\d+$", "", s), scan))
    return out


def canto_files(d):
    return sorted((ROOT / "texts" / d).glob("0*-canto-*.md"))


def find_line(d, scan, verse):
    """The line of ocr/DIR/SCAN.txt that holds the verse (marks read as printed)."""
    path = ROOT / "ocr" / d / f"{scan}.txt"
    if not path.exists():
        return "?"
    target = words(verse)
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = re.sub(r"\{\{[^|}]*\|([^}]*)\}\}", r"\1", line)  # the fixed side, as converted
        line = re.sub(r"\*\*[^*]+\*\*", "", line)  # a marginal label
        if words(line)[:len(target)] == target or (target and words(line) == target):
            return f"{scan}:{i}"
    return f"{scan}:?"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("volume", choices=VOLUMES)
    ap.add_argument("-o", "--out", type=Path, help="write the list here (default: stdout)")
    ap.add_argument("--accents", action="store_true", help="also list differences of accents alone")
    ap.add_argument("--ratio", type=float, default=0.75, help="least similarity (default 0.75)")
    ap.add_argument("--max", type=int, default=2,
                    help="most occurrences in the three volumes' Italian (default 2)")
    a = ap.parse_args()

    vocab = Counter()
    for _, d in VOLUMES.values():
        for f in canto_files(d):
            for v, _ in verses(f):
                vocab.update(words(v))

    index, d = VOLUMES[a.volume]
    canticle = list(dc.canticles())[index]
    rows, problems = [], 0
    for f in canto_files(d):
        n = int(f.stem.split("-")[-1])
        std = [getattr(l, "text", str(l)) for l in dc.canto(canticle, n).lines()]
        mine = verses(f)
        if len(mine) != len(std):
            print(f"{f.name}: {len(mine)} verse lines, the standard text {len(std)}; skipped",
                  file=sys.stderr)
            problems += 1
            continue
        for i, ((line, scan), ref) in enumerate(zip(mine, std), 1):
            ta, tb = words(line), words(ref)
            sm = difflib.SequenceMatcher(None, ta, tb)
            for op, a0, a1, b0, b1 in sm.get_opcodes():
                if op != "replace":
                    continue
                for x, y in zip(ta[a0:a1], tb[b0:b1]):
                    if vocab[x] > a.max or difflib.SequenceMatcher(None, x, y).ratio() < a.ratio:
                        continue
                    if not a.accents and plain(x) == plain(y):
                        continue
                    rows.append(f"{n}:{i}\t{find_line(d, scan, line)}\t{x}\t{y}\t{vocab[x]}\t{line}")
    text = "\n".join(rows) + ("\n" if rows else "")
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    print(f"{len(rows)} words listed; {problems} cantos skipped", file=sys.stderr)


if __name__ == "__main__":
    main()
