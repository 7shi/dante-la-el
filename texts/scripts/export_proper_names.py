"""Export proper-name occurrences to texts/en/PROPER_NAMES.tsv and collect Japanese renderings."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_index as ci

ROOT = ci.ROOT
TEXTS_EN = ci.TEXTS_EN
JA_EN = ROOT / "translations" / "ja" / "en"
OUT_EN_TSV = TEXTS_EN / "PROPER_NAMES.tsv"
OUT_JA_TSV = JA_EN / "PROPER_NAMES.tsv"

sys.path.insert(0, str(ROOT / "translations" / "scripts"))
import pages as pg  # noqa: E402

EXTRA_STOP = ci.STOP_WORDS | {
    "counts", "count", "alluded", "city", "empire", "duke", "marquis",
    "brother", "father", "son", "daughter", "wife", "mother", "old",
    "great", "little", "new", "holy", "roman", "tuscan",
}

SPECIAL_PATTERNS: dict[str, list[str]] = {
    "Adam, Master": [r"Master Adam"],
    "Alberto, degli Alberti": [r"Alberto", r"Alberti"],
    "Alessandro, degli Alberti": [r"Alessandro", r"Alberti"],
    "Anselmuccio": [r"Anselm(?:uccio)?"],
    "Apuglia": [r"Apuglia", r"Apulia\w*"],
    "Caccianemico": [r"Caccian[ei]mico"],
    "Diomede": [r"Diomed\w*"],
    "Erinnys": [r"Er[iy]nn[iy]s"],
    "Frieselanders": [r"Frie[sz]e?landers?"],
    "Latinus, King": [r"Latian king", r"Latinus"],
    "Latium": [r"Latian", r"Latium"],
    "Mantuans": [r"Mantuan\w*"],
    "Mascheroni, Sassolo": [r"Sassol\w*", r"Mascheroni"],
    "Matthew, Apostle": [r"Matthew", r"Matthias"],
    "Ptolomæus, Claudius": [r"Ptol[eo]m[ae]+us"],
    "Sardinians": [r"Sardini\w*"],
    "Tisiphone": [r"T[ei]siphone"],
    "Tuscan": [r"Tuscan\w*"],
    "Buondelmonti": [r"Buondelmont[ei]"],
    "Brutus, Lucius Junius": [r"Lucius Junius", r"Brutus"],
    "Brutus, Marcus Junius": [r"Marcus Junius", r"Brutus"],
    "John, Evangelist": [r"Evangelist", r"St\. John"],
    "John, Baptist": [r"Baptist", r"St\. John"],
    "Jason, Argonaut": [r"Jason"],
    "Jason, Hebrew": [r"Jason"],
    "Guidi, Counts": [r"Guidi"],
    "Viso, mount": [r"\bViso\b"],
}

KATA_TOKEN_RE = re.compile(r"[ァ-ヴー]+(?:・[ァ-ヴー]+)*(?:人|派|川|山|湖|泉)?")

KATA_TABLE = {
    "キャ": "kya", "キュ": "kyu", "キョ": "kyo",
    "シャ": "sha", "シュ": "shu", "ショ": "sho",
    "チャ": "cha", "チュ": "chu", "チョ": "cho",
    "ニャ": "nya", "ニュ": "nyu", "ニョ": "nyo",
    "ヒャ": "hya", "ヒュ": "hyu", "ヒョ": "hyo",
    "ミャ": "mya", "ミュ": "myu", "ミョ": "myo",
    "リャ": "rya", "リュ": "ryu", "リョ": "ryo",
    "ギャ": "gya", "ギュ": "gyu", "ギョ": "gyo",
    "ジャ": "ja", "ジュ": "ju", "ジョ": "jo",
    "ビャ": "bya", "ビュ": "byu", "ビョ": "byo",
    "ピャ": "pya", "ピュ": "pyu", "ピョ": "pyo",
    "ヴァ": "va", "ヴィ": "vi", "ヴ": "vu", "ヴェ": "ve", "ヴォ": "vo",
    "ファ": "fa", "フィ": "fi", "フェ": "fe", "フォ": "fo",
    "ティ": "ti", "ディ": "di", "トゥ": "tu", "ドゥ": "du", "テュ": "tyu", "デュ": "dyu",
    "ウィ": "wi", "ウェ": "we", "ウォ": "wo",
    "シェ": "she", "ジェ": "je", "チェ": "che",
    "ツァ": "tsa", "ツィ": "tsi", "ツェ": "tse", "ツォ": "tso",
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    "サ": "sa", "シ": "si", "ス": "su", "セ": "se", "ソ": "so",
    "タ": "ta", "チ": "ti", "ツ": "tu", "テ": "te", "ト": "to",
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
    "ハ": "ha", "ヒ": "hi", "フ": "fu", "ヘ": "he", "ホ": "ho",
    "マ": "ma", "ミ": "mi", "ム": "mu", "メ": "me", "モ": "mo",
    "ヤ": "ya", "ユ": "yu", "ヨ": "yo",
    "ラ": "ra", "リ": "ri", "ル": "ru", "レ": "re", "ロ": "ro",
    "ワ": "wa", "ヲ": "wo", "ン": "n",
    "ガ": "ga", "ギ": "gi", "グ": "gu", "ゲ": "ge", "ゴ": "go",
    "ザ": "za", "ジ": "ji", "ズ": "zu", "ゼ": "ze", "ゾ": "zo",
    "ダ": "da", "ヂ": "di", "ヅ": "du", "デ": "de", "ド": "do",
    "バ": "ba", "ビ": "bi", "ブ": "bu", "ベ": "be", "ボ": "bo",
    "パ": "pa", "ピ": "pi", "プ": "pu", "ペ": "pe", "ポ": "po",
    "ァ": "a", "ィ": "i", "ゥ": "u", "ェ": "e", "ォ": "o",
    "ャ": "ya", "ュ": "yu", "ョ": "yo",
    "ー": "", "・": "", "ッ": "",
}


def kata_to_romaji(s: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(s):
        if i + 1 < len(s) and s[i : i + 2] in KATA_TABLE:
            out.append(KATA_TABLE[s[i : i + 2]])
            i += 2
        else:
            out.append(KATA_TABLE.get(s[i], ""))
            i += 1
    return "".join(out)


def phonetic_skel(s: str) -> str:
    """Reduce English/romaji string to a consonant-like phonetic skeleton."""
    s = ci.normalize(s).lower()
    s = re.sub(r"[^a-z]", "", s)
    # Normalize common English/Italian <-> Katakana equivalences
    s = re.sub(r"c([eiy])", r"s\1", s)
    s = s.replace("gh", "g").replace("ph", "f").replace("th", "t")
    s = s.replace("ch", "k").replace("qu", "k").replace("sh", "s").replace("zh", "j")
    s = s.replace("v", "b").replace("l", "r").replace("c", "k").replace("j", "g")
    s = s.replace("z", "s").replace("w", "u")
    s = re.sub(r"(.)\1+", r"\1", s)
    if not s:
        return ""
    return s[0] + re.sub(r"[aeiouy]", "", s[1:])


def edit_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for ca in a:
        curr = [prev[0] + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def build_patterns(headword: str) -> list[re.Pattern[str]]:
    if headword in SPECIAL_PATTERNS:
        return [
            re.compile(rf"\b{p}\b" if not p.startswith(r"\b") else p, re.IGNORECASE)
            for p in SPECIAL_PATTERNS[headword]
        ]

    norm = ci.normalize(headword)
    parens = re.findall(r"\(([^)]+)\)", norm)
    base = re.sub(r"\([^)]*\)", "", norm)
    parts = [p.strip() for p in base.split(",") if p.strip()]

    tokens: list[str] = []
    if len(parts) >= 2:
        second_tokens = [
            re.sub(r"'s?$", "", t)
            for t in re.findall(r"[A-Za-z][A-Za-z'-]*", parts[1])
            if t.lower() not in EXTRA_STOP and len(t) >= 2
        ]
        first_tokens = [
            re.sub(r"'s?$", "", t)
            for t in re.findall(r"[A-Za-z][A-Za-z'-]*", parts[0])
            if t.lower() not in EXTRA_STOP and len(t) >= 2
        ]
        tokens.extend(second_tokens or first_tokens)
    else:
        for t in re.findall(r"[A-Za-z][A-Za-z'-]*", base):
            tc = re.sub(r"'s?$", "", t)
            if tc.lower() not in EXTRA_STOP and len(tc) >= 2:
                tokens.append(tc)

    for p in parens:
        for t in re.findall(r"[A-Za-z][A-Za-z'-]*", p):
            tc = re.sub(r"'s?$", "", t)
            if tc.lower() not in EXTRA_STOP and len(tc) >= 2:
                tokens.append(tc)

    seen: set[str] = set()
    pats: list[re.Pattern[str]] = []
    for t in tokens:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            pats.append(re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE))
    return pats


def split_by_page(blocks: list[str]) -> list[tuple[str, list[str]]]:
    pages: list[tuple[str, list[str]]] = []
    cur_page = "0"
    cur_blocks: list[str] = []
    for b in blocks:
        lines = [
            ln for ln in b.strip().splitlines()
            if not ln.startswith("<!-- first paragraph joined")
        ]
        if not lines:
            continue
        pm = ci.PAGE_RE.match(lines[0].strip())
        if pm:
            if cur_blocks or cur_page != "0":
                pages.append((cur_page, cur_blocks))
            cur_page = pm.group(1)
            cur_blocks = ["\n".join(lines[1:])] if len(lines) > 1 else []
        else:
            cur_blocks.append("\n".join(lines))
    if cur_blocks or cur_page != "0":
        pages.append((cur_page, cur_blocks))
    return pages


def load_aligned_pairs() -> list[tuple[int, int, str, str]]:
    """Return (canto, line_start, en_block, ja_block) aligned via pages.py."""
    pairs: list[tuple[int, int, str, str]] = []
    canto_files = sorted(TEXTS_EN.glob("0[0-4][0-9]-canto-*.md"))
    for canto_idx, en_path in enumerate(canto_files, 1):
        ja_path = JA_EN / en_path.name
        if not ja_path.exists():
            continue
        en_prep, _ = pg.prepare(en_path)
        en_blocks = [
            b for b in pg.blocks(en_prep)
            if not pg.is_verse(b) and not b.startswith("#")
        ]
        ja_blocks = [
            b for b in pg.blocks(ja_path.read_text(encoding="utf-8"))
            if not b.startswith("<!-- first paragraph joined") and not b.startswith("#")
        ]
        segs = ci.parse_canto_file(en_path, canto_idx)
        page_line: dict[str, int] = {}
        for s in segs:
            if s.line_start is not None and s.page not in page_line:
                page_line[s.page] = s.line_start

        en_pages = split_by_page(en_blocks)
        ja_pages = split_by_page(ja_blocks)
        ja_map = dict(ja_pages)
        for p, ebs in en_pages:
            jbs = ja_map.get(p, [])
            ln_default = page_line.get(p, 0)
            if len(ebs) == len(jbs):
                for eb, jb in zip(ebs, jbs):
                    gm = ci.GLOSS_RE.match(eb.strip())
                    ln = int(gm.group(1)) if gm else ln_default
                    pairs.append((canto_idx, ln, ci.normalize(eb), jb))
            elif jbs:
                pairs.append(
                    (canto_idx, ln_default, ci.normalize("\n\n".join(ebs)), "\n\n".join(jbs))
                )
    return pairs


def best_ja_match(headword: str, ja_text: str) -> str | None:
    """Find the best matching katakana token in ja_text for headword."""
    norm = ci.normalize(headword)
    base = re.sub(r"\([^)]*\)", "", norm)
    # Strip trailing "da <Place>" / "of <Place>" / "de' <Family>" when extracting primary name
    primary = re.split(r"\b(?:da|de'|degli|del|della|delle|di|of)\b", base, maxsplit=1)[0]
    en_words = [
        w for w in re.findall(r"[A-Za-z]+", primary)
        if w.lower() not in EXTRA_STOP and len(w) >= 2
    ]
    if not en_words:
        en_words = [
            w for w in re.findall(r"[A-Za-z]+", base)
            if w.lower() not in EXTRA_STOP and len(w) >= 2
        ]
    if not en_words:
        return None
    en_skels = [phonetic_skel(w) for w in en_words]
    full_en_skel = phonetic_skel(" ".join(en_words))

    best_tok: str | None = None
    best_score = 999.0
    for tok in KATA_TOKEN_RE.findall(ja_text):
        rom = kata_to_romaji(tok)
        jsk = phonetic_skel(rom)
        if not jsk:
            continue
        candidates = [
            edit_distance(jsk, esk) / max(len(jsk), len(esk), 1)
            for esk in en_skels + [full_en_skel]
        ]
        if "・" in tok:
            for sub in tok.split("・"):
                ssk = phonetic_skel(kata_to_romaji(sub))
                if ssk:
                    for esk in en_skels:
                        candidates.append(edit_distance(ssk, esk) / max(len(ssk), len(esk), 1))
        score = min(candidates)
        if score < best_score:
            best_score = score
            best_tok = tok
    if best_tok is not None and best_score <= 0.45:
        return best_tok
    return None


def main() -> None:
    entries = ci.parse_index(ci.INDEX_FILE)
    canto_files = sorted(TEXTS_EN.glob("0[0-4][0-9]-canto-*.md"))
    by_canto = {idx: ci.parse_canto_file(cf, idx) for idx, cf in enumerate(canto_files, 1)}
    en_segs = [
        seg
        for idx in sorted(by_canto)
        for seg in by_canto[idx]
        if seg.kind != "verse"
    ]

    en_rows: list[str] = []
    for entry in entries:
        pats = build_patterns(entry.headword)
        locs: list[tuple[int, int]] = []
        seen_loc: set[tuple[int, int]] = set()
        for seg in en_segs:
            if any(p.search(seg.norm_text) for p in pats):
                ln = seg.line_start if seg.line_start is not None else 0
                key = (seg.canto, ln)
                if key not in seen_loc:
                    seen_loc.add(key)
                    locs.append(key)
        locs.sort()
        loc_str = ",".join(f"{c}:{l}" for c, l in locs)
        en_rows.append(f"{entry.headword}\t{loc_str}")

    OUT_EN_TSV.write_text("\n".join(en_rows) + "\n", encoding="utf-8")
    empty_en = sum(1 for r in en_rows if r.endswith("\t"))
    print(f"Wrote {len(en_rows)} rows to {OUT_EN_TSV} (empty locs: {empty_en})")

    # Collect Japanese renderings from aligned blocks
    aligned = load_aligned_pairs()
    print(f"Aligned {len(aligned)} prose/note/gloss blocks across cantos")

    ja_rows: list[str] = []
    multi_count = 0
    empty_ja = 0
    for entry in entries:
        pats = build_patterns(entry.headword)
        counts: Counter[str] = Counter()
        for _, _, eb, jb in aligned:
            if any(p.search(eb) for p in pats):
                m = best_ja_match(entry.headword, jb)
                if m:
                    counts[m] += 1
        if not counts:
            empty_ja += 1
            ja_rows.append(entry.headword)
        else:
            if len(counts) > 1:
                multi_count += 1
            forms = [f for f, _ in counts.most_common()]
            ja_rows.append("\t".join([entry.headword] + forms))

    OUT_JA_TSV.write_text("\n".join(ja_rows) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(ja_rows)} rows to {OUT_JA_TSV} "
        f"(multiple ja forms: {multi_count}, empty ja: {empty_ja})"
    )


if __name__ == "__main__":
    main()
