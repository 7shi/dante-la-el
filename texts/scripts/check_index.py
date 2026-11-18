"""Check Index of Proper Names (texts/en/041-index-of-proper-names.md) against texts/en/."""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TEXTS_EN = ROOT / "texts" / "en"
INDEX_FILE = TEXTS_EN / "041-index-of-proper-names.md"
DEFAULT_LOG = ROOT / "tmp" / "index_check.log"

ROMAN_RE = re.compile(
    r"\b(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv|xvi|xvii|xviii|xix|xx|"
    r"xxi|xxii|xxiii|xxiv|xxv|xxvi|xxvii|xxviii|xxix|xxx|xxxi|xxxii|xxxiii|xxxiv)\."
)
REF_SPLIT_RE = re.compile(
    r"(?=\b(?:i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv|xvi|xvii|xviii|xix|xx|"
    r"xxi|xxii|xxiii|xxiv|xxv|xxvi|xxvii|xxviii|xxix|xxx|xxxi|xxxii|xxxiii|xxxiv)\.)"
)
PAGE_RE = re.compile(r"^<!--\s*p\.\s*(\S+)\s*\((\d+)\)\s*-->$")
NOTE_RE = re.compile(r"^\[\^[^\]]+\]:")
GLOSS_RE = re.compile(r"^(\d+)\\\.")
VERSE_LINE_NUM_RE = re.compile(r"\s+(\d{1,3})\\?$")

ROMAN_MAP = {
    "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8,
    "ix": 9, "x": 10, "xi": 11, "xii": 12, "xiii": 13, "xiv": 14, "xv": 15, "xvi": 16,
    "xvii": 17, "xviii": 18, "xix": 19, "xx": 20, "xxi": 21, "xxii": 22, "xxiii": 23,
    "xxiv": 24, "xxv": 25, "xxvi": 26, "xxvii": 27, "xxviii": 28, "xxix": 29, "xxx": 30,
    "xxxi": 31, "xxxii": 32, "xxxiii": 33, "xxxiv": 34,
}

STOP_WORDS = {
    "and", "of", "the", "in", "on", "at", "to", "for", "from", "by",
    "da", "de", "del", "della", "delle", "degli", "dei", "di", "d",
    "st", "saint", "king", "pope", "friar", "master", "count", "marquis",
    "mount", "river", "lake", "fount", "city", "abbey", "fable", "valley",
    "evangelist", "baptist", "argonaut", "hebrew", "see", "dis",
}


def normalize(text: str) -> str:
    """Normalize ligatures, apostrophes, and combining accents for ASCII-friendly matching."""
    text = (
        text.replace("Æ", "Ae")
        .replace("æ", "ae")
        .replace("Œ", "Oe")
        .replace("œ", "oe")
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
    )
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


@dataclass
class Ref:
    canto: int
    canto_roman: str
    lines: list[int]
    etc: bool = False


@dataclass
class IndexEntry:
    line_no: int
    raw: str
    headword: str
    search_terms: list[str]
    refs: list[Ref]


@dataclass
class Segment:
    canto: int
    page: str
    kind: str  # "argument" | "prose" | "verse" | "gloss" | "note"
    line_start: int | None
    line_end: int | None
    text: str
    norm_text: str


def extract_search_terms(headword: str) -> list[str]:
    """Extract candidate search terms from an index headword."""
    cleaned = normalize(headword)
    # Remove trailing descriptors in parentheses into separate candidates
    parens = re.findall(r"\(([^)]+)\)", cleaned)
    base = re.sub(r"\([^)]*\)", "", cleaned)
    # Split on commas to inspect parts (e.g. "Ubaldini degli, Ottaviano", "Viso, mount")
    parts = [p.strip() for p in base.split(",") if p.strip()]

    candidates: list[str] = []
    # 1. Reordered full form if "Surname, Given"
    if len(parts) == 2 and parts[1].lower() not in STOP_WORDS:
        candidates.append(f"{parts[1]} {parts[0]}")
    if base.strip():
        candidates.append(base.strip())

    # 2. Significant individual tokens (length >= 3, not in STOP_WORDS)
    tokens: list[str] = []
    for chunk in parts + parens:
        for tok in re.findall(r"[A-Za-z][A-Za-z'-]*", chunk):
            # Strip trailing possessive 's or '
            tok_clean = re.sub(r"'s?$", "", tok)
            if len(tok_clean) >= 2 and tok_clean.lower() not in STOP_WORDS:
                tokens.append(tok_clean)

    # Prefer longer/more specific tokens first, deduplicated preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for t in tokens + candidates:
        t_norm = t.strip()
        key = t_norm.lower()
        if t_norm and key not in seen and key not in STOP_WORDS:
            seen.add(key)
            ordered.append(t_norm)
    return ordered


def parse_refs(ref_str: str) -> list[Ref]:
    refs: list[Ref] = []
    # Strip trailing "See ..." and punctuation
    ref_str = re.sub(r"\bSee\b.*$", "", ref_str).strip().rstrip("\\.")
    for part in ref_str.split(";"):
        part = part.strip()
        if not part:
            continue
        m = ROMAN_RE.match(part)
        if not m:
            continue
        roman = m.group(1)
        canto = ROMAN_MAP[roman]
        rest = part[m.end():].strip()
        etc = "&c" in rest
        nums = [int(n) for n in re.findall(r"\b\d+\b", rest)]
        refs.append(Ref(canto=canto, canto_roman=roman, lines=nums, etc=etc))
    return refs


def parse_index(path: Path) -> list[IndexEntry]:
    entries: list[IndexEntry] = []
    prev_base = ""
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if (
            not line
            or line.startswith("#")
            or line.startswith("<!--")
            or line in ("THE END.",)
            or line.startswith("CHISWICK PRESS")
        ):
            continue
        line_clean = line.rstrip("\\").strip()
        m = REF_SPLIT_RE.search(line_clean)
        if not m:
            continue
        head_raw = line_clean[: m.start()].strip().rstrip(",").strip()
        ref_raw = line_clean[m.start():].strip()

        if head_raw.startswith("—"):
            sub = head_raw.lstrip("—").strip()
            resolved_head = f"{prev_base}, {sub}" if prev_base else sub
        else:
            resolved_head = head_raw
            # Base for following "—" lines is the first word/phrase before comma or space
            first_part = head_raw.split(",")[0].strip()
            prev_base = first_part.split()[0] if first_part else head_raw

        terms = extract_search_terms(resolved_head)
        refs = parse_refs(ref_raw)
        entries.append(
            IndexEntry(
                line_no=line_no,
                raw=line_clean,
                headword=resolved_head,
                search_terms=terms,
                refs=refs,
            )
        )
    return entries


def is_verse_block(block: str) -> bool:
    lines = block.strip("\n").splitlines()
    if any(len(l) > 100 for l in lines):
        return False
    return "\\\n" in block or block.rstrip().endswith("\\") or bool(
        re.match(r"^(&emsp;)?[^\[\n]{1,90} \d{1,3}$", block.strip())
    )


def parse_canto_file(path: Path, canto: int) -> list[Segment]:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", text.strip())
    segments: list[Segment] = []
    page = "0"
    in_argument = False
    verse_counter = 0

    # First pass: assign page + kind and exact verse line numbers
    raw_items: list[tuple[str, str, str, int | None, int | None]] = []
    for b in blocks:
        b_strip = b.strip()
        if not b_strip:
            continue
        pm = PAGE_RE.match(b_strip)
        if pm:
            page = pm.group(1)
            continue
        if b_strip.startswith("# "):
            continue
        if b_strip == "## Argument":
            in_argument = True
            continue
        if NOTE_RE.match(b_strip):
            raw_items.append((page, "note", b_strip, None, None))
            continue
        gm = GLOSS_RE.match(b_strip)
        if gm:
            ln = int(gm.group(1))
            raw_items.append((page, "gloss", b_strip, ln, ln))
            continue
        if is_verse_block(b_strip):
            in_argument = False
            vlines = b_strip.splitlines()
            start_ln = verse_counter + 1
            for vl in vlines:
                verse_counter += 1
                raw_items.append((page, "verse", vl, verse_counter, verse_counter))
            continue
        kind = "argument" if in_argument else "prose"
        if in_argument:
            in_argument = False
        raw_items.append((page, kind, b_strip, None, None))

    # Compute verse line range per page so prose & notes know their line span
    page_ranges: dict[str, tuple[int, int]] = {}
    for p, kind, _, s, e in raw_items:
        if kind == "verse" and s is not None:
            if p not in page_ranges:
                page_ranges[p] = (s, s)
            else:
                lo, hi = page_ranges[p]
                page_ranges[p] = (min(lo, s), max(hi, s))

    for p, kind, txt, s, e in raw_items:
        if s is None and kind in ("prose", "note") and p in page_ranges:
            s, e = page_ranges[p]
        segments.append(
            Segment(
                canto=canto,
                page=p,
                kind=kind,
                line_start=s,
                line_end=e,
                text=txt,
                norm_text=normalize(txt),
            )
        )
    return segments


def compile_term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term)
    return re.compile(rf"\b{escaped}\b", re.IGNORECASE)


def find_matches(
    terms: list[str], segments: list[Segment]
) -> list[tuple[Segment, str]]:
    patterns = [(t, compile_term_pattern(t)) for t in terms]
    hits: list[tuple[Segment, str]] = []
    for seg in segments:
        for term, pat in patterns:
            if pat.search(seg.norm_text):
                hits.append((seg, term))
                break
    return hits


def ref_matches_segment(ref: Ref, seg: Segment, margin: int = 3) -> bool:
    if seg.canto != ref.canto:
        return False
    if not ref.lines:
        return True
    if seg.line_start is None or seg.line_end is None:
        return False
    for ln in ref.lines:
        if seg.line_start - margin <= ln <= seg.line_end + margin:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--log", type=Path, default=DEFAULT_LOG, help="Output log file path"
    )
    args = parser.parse_args()

    entries = parse_index(INDEX_FILE)
    all_segments: list[Segment] = []
    by_canto: dict[int, list[Segment]] = {}

    canto_files = sorted(TEXTS_EN.glob("0[0-4][0-9]-canto-*.md"))
    for idx, cf in enumerate(canto_files, 1):
        segs = parse_canto_file(cf, idx)
        all_segments.extend(segs)
        by_canto[idx] = segs

    args.log.parent.mkdir(parents=True, exist_ok=True)

    total_refs = 0
    matched_refs = 0
    unmatched_entries: list[str] = []
    log_lines: list[str] = []

    for entry in entries:
        hits = find_matches(entry.search_terms, all_segments)
        log_lines.append(f"=== L{entry.line_no}: {entry.raw}")
        log_lines.append(f"    headword={entry.headword!r} terms={entry.search_terms}")
        for ref in entry.refs:
            total_refs += 1
            ref_hits = [
                (seg, t) for seg, t in hits if ref_matches_segment(ref, seg)
            ]
            canto_hits = [(seg, t) for seg, t in hits if seg.canto == ref.canto]
            lines_str = ",".join(str(x) for x in ref.lines) if ref.lines else "(canto)"
            if ref_hits:
                matched_refs += 1
                sample_seg, sample_term = ref_hits[0]
                span = (
                    f"{sample_seg.line_start}-{sample_seg.line_end}"
                    if sample_seg.line_start != sample_seg.line_end
                    else f"{sample_seg.line_start}"
                )
                log_lines.append(
                    f"    [OK] {ref.canto_roman}. {lines_str} -> "
                    f"canto {sample_seg.canto} p.{sample_seg.page} {sample_seg.kind} "
                    f"L{span} (matched {sample_term!r}, {len(ref_hits)} hit(s))"
                )
            elif canto_hits:
                sample_seg, sample_term = canto_hits[0]
                log_lines.append(
                    f"    [CANTO_ONLY] {ref.canto_roman}. {lines_str} -> "
                    f"found in canto {sample_seg.canto} p.{sample_seg.page} "
                    f"{sample_seg.kind} L{sample_seg.line_start}-{sample_seg.line_end} "
                    f"(matched {sample_term!r})"
                )
                unmatched_entries.append(
                    f"L{entry.line_no} {entry.headword} ({ref.canto_roman}. {lines_str}) [CANTO_ONLY]"
                )
            else:
                log_lines.append(
                    f"    [MISS] {ref.canto_roman}. {lines_str} -> "
                    f"no match in canto {ref.canto} (global hits={len(hits)})"
                )
                unmatched_entries.append(
                    f"L{entry.line_no} {entry.headword} ({ref.canto_roman}. {lines_str}) [MISS]"
                )

    summary = [
        f"Index entries parsed: {len(entries)}",
        f"Total refs checked: {total_refs}",
        f"Matched at ref (margin +/-3): {matched_refs} ({matched_refs / total_refs * 100:.1f}%)",
        f"Unmatched (CANTO_ONLY or MISS): {len(unmatched_entries)}",
    ]
    args.log.write_text("\n".join(summary + [""] + log_lines) + "\n", encoding="utf-8")

    print("\n".join(summary))
    print("\nFirst 30 unmatched refs:")
    for u in unmatched_entries[:30]:
        print(" ", u)
    print(f"\nFull log written to: {args.log}")


if __name__ == "__main__":
    main()
