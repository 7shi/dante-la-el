"""Decide the marks left by la_markprep.py and resolve them into the pages.

    la_markresolve.py WORK -t TESSDIR [--write]

Reads WORK/post/ and WORK/locate.tsv (la_markprep.py), WORK/decide.tsv (la_markdecide.py,
if present), and the hand-made WORK/mine.tsv and WORK/fixes.tsv (if present). Each mark
gets a route:

- rule:  `:` against `;` only, decided by a context rule (a naive Bayes on the neighbouring
         words, trained on the proofread pages 0104-0194; right about 70% of the time: the
         edition uses `:` also as a stop stronger than `;`, and the choice matters little);
- text:  `.` against `,` only, decided by hand from the context (a dot inside a running
         sentence is a comma);
- image: text on one side only, marks not located, GLM-OCR's dropped passages, and the
         model's answers that are not taken: decided by hand in the image;
- model: the model's verdict, taken for a letter mark only when Tesseract's word at the
         place is the same side exactly, for other marks unless the chosen side adds an
         accent.

A decision that changes ocr/la (`right`) taken from the model is `check` until confirmed in
WORK/mine.tsv: the model reads common forms for misprints, and Tesseract shares GLM-OCR's
c/e errors.

WORK/mine.tsv (page, line, k, decision, note) holds the decisions made by hand and
overrides the others: `left`, `right`, or `text:` followed by the printed text (`⏎` for a
line break). WORK/fixes.tsv (page, old, new, note) holds replacements made after the marks
are resolved (`⏎` for a line break), for what the marks do not cover; each `old` must occur
exactly once.

Writes WORK/route.tsv (every mark), WORK/review.tsv (the marks still to decide by hand,
with the reason and the crop), and WORK/out/PAGE.txt for each page whose marks are all
decided; with --write also ocr/la/PAGE.txt."""

import argparse
import collections
import difflib
import math
import re
import shutil
from pathlib import Path

import la_markup as M
from la_markprep import klass, letters, passage_mark, tess_words

ACCENTED = re.compile(r"[àèéìíòóùúâêîôûÀÈÉÌÒÙ]")
TRAIN = [f"{p:04}" for p in range(104, 195) if p not in (115, 128, 140, 141, 162, 172)]


# ---- the context rule for `:` against `;` ----

def flat(t): return re.sub(r"\s+", " ", re.sub(r"(?<=\w)-\n", "", t))


def features(before, after):
    pw = re.findall(r"\S+", before)[-1:] or [""]
    nws = re.findall(r"\S+", after)[:2]
    nw = nws[0] if nws else ""
    clause = re.findall(r"[^.;:?!]+$", before)
    return [f"n:{re.sub(r'\W', '', nw).lower()}", f"cap:{nw[:1].isupper()}",
            f"p:{re.sub(r'\W', '', pw[0]).lower()}",
            f"n2:{re.sub(r'\W', '', nws[1]).lower() if len(nws) > 1 else ''}",
            f"len:{min(len(clause[0].split()) // 5, 6) if clause else 0}"]


class ColonRule:
    def __init__(self, pages=TRAIN):
        self.cnt = {":": collections.Counter(), ";": collections.Counter()}
        self.n = collections.Counter()
        for p in pages:
            t = flat((M.ROOT / f"{p}.txt").read_text(encoding="utf-8"))
            for m in re.finditer(r"(?<=\S)[:;](?= )", t):
                c = m.group(); self.n[c] += 1
                self.cnt[c].update(features(t[max(0, m.start() - 300):m.start()], t[m.end():m.end() + 60]))

    def predict(self, before, after):
        """`:` or `;` for the stop between the text before and after, and the confidence."""
        f = features(flat(before), flat(after))
        s = {c: math.log(self.n[c]) + sum(math.log((self.cnt[c][x] + 0.5) / (self.n[c] + 1)) for x in f)
             for c in ":;"}
        return (":" if s[":"] > s[";"] else ";"), abs(s[":"] - s[";"])


# ---- Tesseract's vote ----

def tess_vote(ws, box, l, r, frac):
    """Tesseract's words at the mark (a run of 1..n+1 words near the box) and the side they
    equal exactly (letters only): `left`, `right` or `none`."""
    x0, y0, x1, y1 = box
    lh = y1 - y0 if y1 - y0 < 60 else 40
    near = {i for i, w in enumerate(ws) if x0 - 5 <= w["box"][0] and w["box"][2] <= x1 + 5
            and y0 - lh - 5 <= w["box"][1] and w["box"][3] <= y1 + lh + 5}
    lw, rw = letters(l), letters(r)
    n = max(len(l.split()), len(r.split()), 1)
    best, bs = None, -9
    for a in sorted(near):
        for b in range(a, min(a + n + 1, len(ws))):
            if b not in near: break
            t = letters("".join(ws[i]["text"] for i in range(a, b + 1)))
            s = max(difflib.SequenceMatcher(None, t, lw).ratio(), difflib.SequenceMatcher(None, t, rw).ratio())
            bx = ws[b]["box"]
            if frac is not None: s -= abs((bx[2] - x0) / max(1, x1 - x0) - frac)
            if bx[1] < y0 - 5 or bx[3] > y1 + 5: s -= 0.3
            if s > bs: best, bs = (a, b), s
    if best is None: return "none", ""
    found = " ".join(ws[i]["text"] for i in range(best[0], best[1] + 1))
    t = letters(found)
    return ("left" if t == lw != rw else "right" if t == rw != lw else "none"), found


# ---- routing ----

def table(path):
    if not path.exists(): return []
    rows = path.read_text(encoding="utf-8").splitlines()
    head = rows[0].split("\t")
    return [dict(zip(head, r.split("\t"))) for r in rows[1:] if r.strip()]


def route(p, t, locs, model, tw, rule):
    """(route, decision, model, tess, note) for each mark of the page t."""
    out = []
    marks = list(M.MARK.finditer(t))
    assert len(marks) == len(locs), p
    for k, (m, f) in enumerate(zip(marks, locs)):
        l, r = m.groups()
        c = klass(l, r); decision = mv = tv = note = ""
        located = f["status"] not in ("unlocated", "ambiguous")
        if c == "colon":
            before = M.MARK.sub(lambda x: x.group(1), t[:m.start()])
            after = M.MARK.sub(lambda x: x.group(1), t[m.end():])
            i = max(l.rfind(":"), l.rfind(";"))
            g, conf = rule.predict(before + l[:i], l[i + 1:] + after)
            rt, decision, note = "rule", ("left" if l[i] == g else "right"), f"rule {g} conf {conf:.1f}"
        elif c == "comma":
            rt, note = "text", "comma: from the context"
        elif c == "onesided" or not located or passage_mark(l, r):
            rt, note = "image", f["status"] if not located else ("passage" if passage_mark(l, r) else "one side only")
        elif k not in model:
            rt, note = "image", "no model answer"
        else:
            v, reading = model[k]; mv = f"{v} {reading!r}"
            rt = "model"
            if v not in ("left", "right"):
                rt, note = "image", f"model {v}"
            elif c == "letters":
                ls = t.rfind("\n", 0, m.start()) + 1
                le = t.find("\n", m.end()); le = len(t) if le < 0 else le
                plain = M.MARK.sub(lambda x: x.group(1), t[ls:m.end()])
                rest = M.MARK.sub(lambda x: x.group(1), t[m.end():le])
                frac = len(plain) / max(1, len(plain) + len(rest)) if len(plain) + len(rest) < 100 else None
                side, found = tess_vote(tw, tuple(map(int, f["box"].split(","))), l, r, frac)
                tv = f"{side} {found!r}"
                if side == v: decision = v
                else: rt, note = "image", "model and Tesseract differ"
            elif len(ACCENTED.findall(l if v == "left" else r)) > len(ACCENTED.findall(r if v == "left" else l)):
                rt, note = "image", "accent added"
            else:
                decision = v
        out.append((rt, decision, mv, tv, note))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("work", type=Path, help="the work directory of la_markprep.py")
    ap.add_argument("-t", "--tessdir", required=True, type=Path, help="Tesseract's PAGE.tsv files")
    ap.add_argument("--write", action="store_true", help="also write the finished pages to ocr/la")
    a = ap.parse_args()
    w = a.work
    (w / "out").mkdir(exist_ok=True)
    locs = collections.defaultdict(list)
    for f in table(w / "locate.tsv"): locs[f["page"]].append(f)
    model = collections.defaultdict(dict)
    for f in table(w / "decide.tsv"): model[f["page"]][int(f["k"])] = (f["verdict"], f["reading"])
    mine = {(f["page"], int(f["k"])): f["decision"] for f in table(w / "mine.tsv")}
    fixes = collections.defaultdict(list)
    for f in table(w / "fixes.tsv"):
        fixes[f["page"]].append((f["old"].replace("⏎", "\n"), f["new"].replace("⏎", "\n")))
    rule = ColonRule()
    rows = ["page\tline\tk\tclass\tleft\tright\troute\tdecision\tmodel\ttess\tnote"]
    review = ["page\tline\tk\tclass\tleft\tright\treason\tmodel\ttess\tcrop"]
    log, count = [], collections.Counter()
    for p in sorted(locs):
        t = (w / "post" / f"{p}.txt").read_text(encoding="utf-8")
        marks = list(M.MARK.finditer(t))
        tw = tess_words(a.tessdir / f"{p}.tsv")
        text, pos, todo = "", 0, 0
        for k, (m, f, (rt, decision, mv, tv, note)) in enumerate(
                zip(marks, locs[p], route(p, t, locs[p], model[p], tw, rule))):
            l, r = m.groups(); line = t[:m.start()].count("\n") + 1
            cells = [p, str(line), str(k), klass(l, r), l.replace("\n", "⏎"), r.replace("\n", "⏎")]
            if rt == "model" and decision == "right": rt, note = "check", "changes ocr/la"
            rows.append("\t".join(cells + [rt, decision, mv, tv, note]))
            final = mine.get((p, k), decision if rt in ("rule", "model") else "")
            count[(rt, "decided" if final else "open")] += 1
            text += t[pos:m.start()]; pos = m.end()
            if final == "left": text += l
            elif final == "right": text += r
            elif final.startswith("text:"): text += final[5:].replace("⏎", "\n")
            else:
                text += m.group(0); todo += 1
                review.append("\t".join(cells + [note, mv, tv, f["crop"]]))
        text += t[pos:]
        problems = []
        for old, new in fixes[p]:
            if text.count(old) == 1: text = text.replace(old, new)
            else: problems.append(f"fix {old!r} found {text.count(old)} times")
        if todo or problems or "{{" in text:
            log.append(f"{p}: {todo} marks to decide" + "".join(f"; {x}" for x in problems))
            (w / "out" / f"{p}.txt").unlink(missing_ok=True)
            continue
        (w / "out" / f"{p}.txt").write_text(text, encoding="utf-8")
        changed = text != (M.ROOT / f"{p}.txt").read_text(encoding="utf-8")
        if a.write and changed: shutil.copyfile(w / "out" / f"{p}.txt", M.ROOT / f"{p}.txt")
        log.append(f"{p}: done, {len(marks)} marks, {len(fixes[p])} fixes"
                   + (", written to ocr/la" if a.write and changed else "" if changed else ", no change"))
    (w / "route.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (w / "review.tsv").write_text("\n".join(review) + "\n", encoding="utf-8")
    print(", ".join(f"{rt} {st}: {n}" for (rt, st), n in sorted(count.items())))
    print("\n".join(log))


if __name__ == "__main__":
    main()
