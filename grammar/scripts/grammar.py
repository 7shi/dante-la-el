"""
Write a grammar commentary on a canto, in English, covering every line: the
forms, the constructions, and the usage of the source text, and how the
existing line-by-line translation (<canticle>/<NN>.txt) renders them. The
content of the poem (story, allegory, background) is left out.

The canto is cut into sections of about --size lines that end where a
sentence ends. Each section is one call: the whole canto (every line followed
by its translation) is sent as its own message, followed by PROMPT for the
lines of that section. An answer is checked before it is kept: its heading
must name the section's lines, it must quote every line of the section once
and in order, and every quoted original and translation must match the
source and the .txt (up to a few characters), so that a translation the
model has rewritten is caught. An answer that fails is sent back with its
problems to be corrected (SECTION_REPAIR_PROMPT), up to --tries answers in
all. Its quote blocks are then rebuilt from the sources of truth
(as fix_quote_blocks.py does) and appended to <NN>.md, so an interrupted run
resumes after the last section saved. A last call adds the closing summary.
At the end of the run, the calls that had answers rejected are listed, each
with the first problem of every rejected answer, and the count of all.

Musurus's Greek with the Modern Greek translation of commentary/el-grc/
(-s grc -l el, grammar/el-grc/) is explained in the same way, with GRC_EL_PROMPT
and GRC_EL_SUMMARY_PROMPT: for English readers, what has changed from Ancient
to Modern Greek (constructions lost or replaced, the vocabulary), set against
the translation; the forms of the Greek alone are explained in grammar/grc/.

The model does not change the translation; where it finds the translation
wrong, it says so in a paragraph opening with `Translation note:`. With
--notes, these are listed from the saved commentaries without calling the
model.

A source printed with a prose translation of its own (en: the Italian
of Carlyle's Inferno and his English; en-oelsner, en-purgatorio,
en-paradiso: the Italian of the Temple Classics and the English printed
with it) is compared with that translation instead, block by block (lines
of the Italian and the part of the English that renders exactly them:
source.carlyle_blocks for en, cut by hand; source.oelsner_passages for the
Temple Classics, one spread each). Each block is one call
(BLOCK_PROMPT), with the block alone in <italian> and <english>: the model
writes a title, then goes through the lines a sentence or clause at a time,
each as a range `[a–b]` with the English that renders it, followed by
bullets on every place where the English departs from a word-for-word
rendering (word order, wording, words left out or supplied, changes of
construction). An answer is checked: the ranges must cover the block's
lines once and in order, their English joined must be the block's English
(word for word, up to punctuation and case), and every phrase in double
quotation marks must be found in the English of its range, and no bullet
may give the translation's own words as the word-for-word rendering. An
answer that fails is sent back with its problems to be corrected (REPAIR_PROMPT), up to
--tries answers in all. The quote blocks of the lines and the English (as
printed, cut where the ranges part) are then written by the script, under
the heading `## Lines a–b — title`. The general changes (a subject
supplied from the verb ending, the article before a possessive left out)
get no bullets of their own and are summed up in the summary, whose phrases
in double quotation marks must also be found in the English (a summary that
fails is sent back to be corrected too). These comparisons have no translation
notes: the translation is a printed text, not one to be corrected. The
commentary takes the name of the file of texts/ it explains: texts/en/
007-canto-01.md is explained in <out>/007-canto-01.md.
"""

import argparse
import re
import sys
from functools import partial
from pathlib import Path

from dante_corpus.api import CANTO_SPEC_HELP, check_canto_spec, select_cantos
from llm7shi import Client
from llm7shi.usage import append_usage, find_usage_file, print_today_totals

# The scripts shared with the commentaries
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "commentary" / "scripts"))

from fix_quote_blocks import ORIG_RE, TRANS_RE, rebuild_lines
from generate import CANTICLE_NAMES, LANGUAGES, same_line
from source import (OELSNER_DIRS, SOURCES, Line, Passage, carlyle_blocks, en_grc_lines,
                    grc_lines, oelsner_passages, source_lines, text_path)

# The blocks of a source printed with a prose translation: lines of the
# source and the part of the translation that renders exactly them (for
# the Temple Classics, a spread: the English faces the Italian tercet by tercet)
BLOCKS = {"en": carlyle_blocks,
          **{source: partial(oelsner_passages, source=source) for source in OELSNER_DIRS}}

# Per language of the source text: what the commentary should look at, on
# top of what every language has (forms, constructions, particles)
FOCUS = {
    "Italian": "the Old Italian and poetic forms that differ from modern Italian "
               "(verb endings, pronouns and clitics, articulated prepositions, "
               "elision and apocope, Latinisms)",
    "Ancient Greek": "the Attic, Homeric, and poetic forms and their spelling "
                     "(elision, prodelision, crasis, the augment, the dual, "
                     "the optative, the uses of the particles), and where the "
                     "translator's Greek follows the Italian construction "
                     "rather than Classical usage",
}

PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, each line followed by its translation into {lang} in parentheses. The translation is fixed: it is not to be changed.

Write, in English and in Markdown, a commentary on the grammar and usage of lines {start}–{end} of the {language} text.

- Begin with the heading `## Lines {start}–{end} — <a short title>`, the title naming what these lines say in a few words. Write no other heading.
- Go through the lines in order. Quote one sentence or clause at a time, one to four lines, and explain it right after the quote. Every line from {start} to {end} must be quoted exactly once.
- Quote each line as `> line-number original`, followed on the next line by `> (translation)`, copying both exactly from the attachment. Put consecutive lines in one quote block, separated by lines containing only `>`.
- Explain the grammar: the form of the words that need it (tense, mood, voice, person, case, number, the dictionary form), the syntax (what governs what, participles, infinitives, subordinate clauses, agreement, word order), the particles and conjunctions, and the usage of the text, especially {focus}.
- Say how the {lang} translation renders the constructions, where it renders them differently and why.
- Do not explain the content: no story, allegory, background, sources, or meter.
- Do not rewrite the translation. If it gets the grammar of a line wrong, add a paragraph opening with `Translation note:` that says what is wrong and what the line means.
""".strip()

# For Musurus's Greek with the Modern Greek translation (-s grc -l el)
GRC_EL_PROMPT = """
Attached is the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, each line followed by its translation into Modern Greek in parentheses. The translation is fixed: it is not to be changed.

Write, in English and in Markdown, a commentary on lines {start}–{end} for English readers who want to see how Musurus's Ancient Greek differs from Modern Greek, line by line against the translation.

- Begin with the heading `## Lines {start}–{end} — <a short title>`, the title naming what these lines say in a few words. Write no other heading.
- Go through the lines in order. Quote one sentence or clause at a time, one to four lines, and explain it right after the quote. Every line from {start} to {end} must be quoted exactly once.
- Quote each line as `> line-number original`, followed on the next line by `> (translation)`, copying both exactly from the attachment. Put consecutive lines in one quote block, separated by lines containing only `>`. In both texts every line begins with a capital letter, as in the printed Greek: this does not mark a new sentence.
- Set the Ancient Greek against the Modern Greek: where Modern Greek has lost or replaced a form or construction, name both and say what took its place: the infinitive (*να* with the subjunctive, a noun, or a clause), the dative (*σε* with the accusative, the genitive), the participles (the gerund in *-οντας*, a relative or temporal clause), the optative, the synthetic future and perfect (*θα*, *έχω*), the middle voice, the particles (*μέν*, *δέ*, *γάρ*, *οὖν*, *ἄν*), and crasis, elision, and prodelision.
- Take up the vocabulary: Ancient words that Modern Greek has dropped, replaced, or given another meaning, with the Modern word that the translation uses instead; and Ancient words that the translation keeps, as learned Modern Greek may.
- Give the form of an Ancient word (tense, mood, voice, person, case, number, dictionary form) only where the comparison needs it, and pass over what is the same in both.
- The changes of spelling and sound (the monotonic accent, the breathings, iota subscript, the pronunciation) get no comment of their own: they are summed up at the end of the canto.
- Write Greek words in italics and your own English glosses in single quotation marks (‘…’). Use no bold.
- Do not explain the content: no story, allegory, background, sources, or meter.
- Do not rewrite the translation. If it misreads the Greek (its construction, or the meaning of a word), add a paragraph opening with `Translation note:` that says what is wrong and what the line means. Write no note on a nuance that the translation could only render more closely.
""".strip()

BLOCK_PROMPT = """
Attached are lines {start}–{end} of canto {number} of Dante's Divine Comedy, {canticle}: the {source} in <italian>, each line with its number, and in <english> the part of the {prose} that renders exactly these lines. The translation is fixed: it is not to be changed.

Write, in English and in Markdown, a comparison of the translation with the {language} text: where the translation departs from a word-for-word rendering, and how.

- On the first line, write a short title naming what these lines say, in a few words in Title Case, and nothing else.
- Then go through the lines in order, one sentence or clause at a time (one to four lines). For each, write a line `[a–b]` (or `[a]` for a single line) followed by the English that renders lines a to b, copied exactly from <english>. The ranges must cover every line from {start} to {end} once, in order; joined, their English must give the whole of <english>, in order, with no word left out, added, or changed.
- After each such line, list in Markdown bullets every place where the translation departs from a word-for-word rendering: a change of word order; another word or turn of phrase; a word left out or supplied; a change of construction, part of speech, tense, mood, or number. Write each as `- *{language} words* ‘word-for-word rendering’ → “the translation's words”: what has changed`, and, where it helps, why (what the {language} construction is, and what English needs instead). Where the translation follows another reading or interpretation of the {language}, say so in the same way. If the lines are rendered word for word, write only `- Literal.`
- Take up each {language} word or phrase in one bullet only: do not come back to the same words in a wider or narrower phrase.
- Write no bullet where the translation's words are the word-for-word rendering, and none on capitals, punctuation, or the spelling of names.
- Write no bullet only to say that a subject given by the ending of the verb is supplied, or that the article before a possessive is left out: these changes are general and are summed up at the end of the canto. Mention them only within a bullet on another change.
- Write {language} words in italics, your own renderings in single quotation marks (‘…’), and only words copied exactly from the English of that range in double quotation marks (“…”).
- Do not explain the content: no story, allegory, background, sources, or meter. Write no headings and no quote blocks.

For example, for lines 1–3 of canto 1 of the Inferno:

[1–3] In the middle of the journey of our life, I found myself in a dark wood; for the straight way was lost.
- *Mi ritrovai* ‘myself I found’ → “I found myself”: the subject, given only by the ending of *ritrovai*, is supplied, and the pronoun follows the verb.
- *per una selva oscura* ‘through a wood dark’ → “in a dark wood”: *per* (through, about) is rendered by a preposition of rest, and the adjective comes before the noun.
- *Chè* ‘because’ → “for”: the subordinating conjunction becomes the coordinating “for”.
""".strip()

# Sent after a rejected answer to a block, with the answer before it
REPAIR_PROMPT = """
Your answer has these problems:

{problems}

Correct them, and give the whole answer again, changing nothing else. A phrase in double quotation marks must be copied exactly from the translation (in a block, from the English of its range); if it is your own rendering, put it in single quotation marks instead.
""".strip()

# Sent after a rejected answer to a section, with the answer before it
SECTION_REPAIR_PROMPT = """
Your answer has these problems:

{problems}

Correct them, and give the whole answer again, changing nothing else. Quote every line and its translation exactly as they are attached, each line once and in order.
""".strip()

SUMMARY_PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, {layout}, and a commentary on its grammar and usage.

Write, in English and in Markdown, the closing section of that commentary: the heading `## Summary — <a short title>`, followed by a few paragraphs that sum up the forms, constructions, and usages that recur in this canto, and how the translation deals with them. Quote no lines and do not explain the content (story, allegory, background, meter). Output only this section.
""".strip()

GRC_EL_SUMMARY_PROMPT = """
Attached is the {source} of canto {number} of Dante's Divine Comedy, {canticle}, line by line, each line followed by its translation into Modern Greek in parentheses, and a commentary on how the Ancient Greek differs from the Modern Greek.

Write, in English and in Markdown, the closing section of that commentary: the heading `## Summary — <a short title>`, followed by a few paragraphs that sum up the differences between Musurus's Ancient Greek and the Modern Greek translation that recur in this canto (the forms and constructions lost or replaced, the particles, the vocabulary dropped, replaced, or kept), with a few examples, and the changes of spelling and sound that the commentary leaves out (the monotonic accent, the breathings, iota subscript, the pronunciation). Quote no lines and do not explain the content (story, allegory, background, meter). Write Greek words in italics and English glosses in single quotation marks (‘…’), and use no bold. Output only this section.
""".strip()

PROSE_SUMMARY_PROMPT = """
Attached are the {source} of canto {number} of Dante's Divine Comedy, {canticle}, block by block (in <italian> the lines, each with its number, and in <english> the part of the {prose} that renders them), and a comparison of the translation with the {language} text.

Write, in English and in Markdown, the closing section of that comparison: the heading `## Summary — <a short title>`, followed by a few paragraphs that sum up how the translation departs from a word-for-word rendering in this canto: the kinds of departure that recur (word order, choice of words, words left out or supplied, changes of construction), with a few examples, and where it keeps close to the {language}. Sum up here also the general changes that the comparison leaves out: subjects given by the ending of the verb supplied, and articles before possessives left out. Quote no lines and do not explain the content (story, allegory, background, meter). Write {language} words in italics, your own renderings in single quotation marks (‘…’), and only words copied exactly from the {prose} in double quotation marks (“…”). Output only this section.
""".strip()

GRC_BLOCK_PROMPT = """
Attached are lines {start}–{end} of canto {number} of Dante's Divine Comedy, {canticle}: in <italian> the {italian_source}, each line with its number; in <english> the part of the {prose} that renders exactly these Italian lines; and in <greek> the {source}, each line with its number and followed in parentheses by its line-by-line English translation. The texts and translations are fixed: they are not to be changed.

Write, in English and in Markdown, a commentary on the Greek translation and its grammar and usage against the Italian: how Musurus translated the Italian into Ancient Greek, and the forms and constructions of his Greek.

- On the first line, write a short title naming what these lines say, in a few words in Title Case, and nothing else.
- Then go through the lines in order, one sentence or clause at a time (one to four lines). For each, write a line `[a–b]` (or `[a]` for a single line) followed by the English that renders lines a to b, copied exactly from <english>. The ranges must cover every line from {start} to {end} once, in order; joined, their English must give the whole of <english>, in order, with no word left out, added, or changed.
- After each such line, explain the Greek translation of lines a to b against the Italian in flat Markdown bullets (`- ...`, no nested bullets): cover how the Greek renders the Italian (word order, choice of words, words supplied or left out, changes of construction, part of speech, tense, mood, voice, or case, and where the Greek follows another reading or interpretation of the Italian), and the grammar and usage of the Greek words that need it (the form — tense, mood, voice, person, case, number, and dictionary form — the syntax, participles, infinitives, subordinate clauses, agreement, particles and conjunctions, and {focus}).
- Write Greek and Italian words in italics, your own literal glosses in single quotation marks (‘…’), and quotations of the English translations in double quotation marks (“…”).
- Do not explain the content: no story, allegory, background, sources, or meter. Write no headings and no quote blocks (the script writes the Italian and Greek quote blocks from `[a–b]`).

For example, for lines 1–3 of canto 1 of the Inferno:

[1–3] In the middle of the journey of our life I [came to] myself in a dark wood [where] the straight way was lost.
- *τοῦ βίου τούτου* ‘of this life’ renders *di nostra vita* ‘of our life’: Musurus replaces the possessive with the demonstrative *τούτου* (gen. sg. masc. of *οὗτος*), in the normal Greek post-nominal position after the articular noun.
- *Εὑρέθην ἐν σκοτεινῷ τινι δρυμῶνι* ‘I was found in a certain dark forest’ renders *mi ritrovai per una selva oscura*: the Italian reflexive becomes the aorist passive *εὑρέθην* (1st sg. aor. pass. ind. of *εὑρίσκω*), *per* becomes static *ἐν* + dative, and the indefinite article *una* is rendered by the enclitic indefinite *τινι* (dat. sg. masc. of *τις*).
- *Τῆς γὰρ εὐθείας ὁδοῦ παρεξετράπην* ‘for I turned aside from the straight road’ renders *che la diritta via era smarrita*: Musurus reads *che* as causal (*γάρ*, postpositive) and recasts the passive clause with the 1st sg. aor. pass. ind. *παρεξετράπην* (from *παρεκτρέπομαι*) governing the genitive of separation *τῆς εὐθείας ὁδοῦ*.
""".strip()

GRC_SUMMARY_PROMPT = """
Attached are the {italian_source} (with the {prose}) and the {source} (with its line-by-line English translation) of canto {number} of Dante's Divine Comedy, {canticle}, block by block, and a commentary on the Greek translation against the Italian.

Write, in English and in Markdown, the closing section of that commentary: the heading `## Summary — <a short title>`, followed by a few paragraphs that sum up how Musurus translates the Italian into Ancient Greek in this canto (the forms, constructions, particles, and turns of phrase that recur, where he departs from a literal rendering or follows the Italian syntax, and any notable readings), with a few examples. Quote no lines and do not explain the content (story, allegory, background, meter). Write Greek and Italian words in italics and literal glosses in single quotation marks (‘…’). Output only this section.
""".strip()

# The layout of the attachment, in SUMMARY_PROMPT
LAYOUT = "each line followed by its translation into {lang} in parentheses"

SECTION_RE = re.compile(r"^## Lines (\d+)\s*[–-]\s*(\d+)\b")
SUMMARY_HEADING = "## Summary"
NOTE_RE = re.compile(r"^Translation note:")
# A sentence ends at the end of a line with one of these, before any closing
# quote marks; the Greek ; is a question mark
SENTENCE_END = {
    "Italian": re.compile(r"[.!?][»”’\"]*$"),
    "Ancient Greek": re.compile(r"[.!?;][»”’“\"]*$"),
}
# A clause ends at the end of a line with one of these
CLAUSE_END = re.compile(r"[.!?;:·][»”’“\"]*$")

# Set the path only when usage should be recorded
USAGE_PATH = None
# Every call of ask() in this run: (what was asked, the first problem of
# every rejected answer, passed)
ASKED: list[tuple[str, list[str], bool]] = []


def sections(lines: list[Line], language: str, size: int) -> list[tuple[int, int]]:
    """Cut a canto into (start, end) line ranges of about size lines, each
    ending where a sentence ends (or a clause, if no sentence ends near
    enough), the last one at the end of the canto."""
    sentence = SENTENCE_END[language]
    result: list[tuple[int, int]] = []
    start = 1
    last = len(lines)
    while start <= last:
        if last - start + 1 <= size * 3 // 2:
            result.append((start, last))
            break
        window = range(start + size // 2, min(start + size * 3 // 2, last))
        end = None
        for pattern in (sentence, CLAUSE_END):
            ends = [no for no in window if pattern.search(lines[no - 1].text.strip())]
            if ends:
                end = min(ends, key=lambda no: abs(no - (start + size - 1)))
                break
        if end is None:
            end = start + size - 1
        result.append((start, end))
        start = end + 1
    return result


def canto_text(lines: list[Line], translations: list[str]) -> str:
    return "\n".join(
        f"{line.no} {line.text}\n({trans})" for line, trans in zip(lines, translations)
    )


def block_text(block: Passage, greek: dict[int, tuple[str, str]] | None = None) -> str:
    """A block as attached: its lines, then the English that renders them
    (and, with greek, the Greek lines and their English translation)."""
    lines = "\n".join(f"{line.no} {line.text}" for line in block.lines)
    text = f"<italian>\n{lines}\n</italian>\n<english>\n{block.english}\n</english>"
    if greek is not None:
        grc = "\n".join(f"{line.no} {greek[line.no][0]}\n({greek[line.no][1]})"
                        for line in block.lines)
        text += f"\n<greek>\n{grc}\n</greek>"
    return text


WORD_RE = re.compile(r"\w+")
# A quotation of the translation in the comparison
ENGLISH_QUOTE_RE = re.compile(r"“([^“”]+)”")
# A range of lines and the English that renders it, `[1–3] In the middle …`
RANGE_RE = re.compile(r"^\[(\d+)(?:\s*[–-]\s*(\d+))?\]\s*(.*)$")
# A bullet's word-for-word rendering and the translation's words,
# `‘…’ → “…”` (a rendering may hold an apostrophe, ‘Peter’s’)
RENDERING_RE = re.compile(r"‘(.+?)’\s*→\s*“([^“”]+)”")


def words(text: str) -> list[str]:
    """The words of a text, without punctuation and case."""
    return WORD_RE.findall(text.replace("’", "'").lower())


def contains(text: str, quote: str) -> bool:
    """Whether the words of quote (piece by piece, if cut with an ellipsis)
    occur in text, up to punctuation and case."""
    found = f" {' '.join(words(text))} "
    return all(f" {' '.join(piece)} " in found
               for part in re.split(r"…|\.\.\.", quote) if (piece := words(part)))


def parse_block(text: str) -> tuple[str, list[tuple[int, int, str, list[str]]], list[str]]:
    """(title, ranges, problems) of an answer to BLOCK_PROMPT; a range is
    (first line, last line, English, bullets)."""
    rows = text.strip().splitlines()
    title = rows[0].strip().strip("#*_ ") if rows else ""
    problems = []
    if not title or RANGE_RE.match(title) or title.startswith(("-", ">")):
        problems.append("the first line is not a title")
    ranges: list[tuple[int, int, str, list[str]]] = []
    for row in rows[1:]:
        if not row.strip():
            continue
        if m := RANGE_RE.match(row.strip()):
            first = int(m.group(1))
            ranges.append((first, int(m.group(2) or first), m.group(3).strip(), []))
        elif ranges and row.startswith("- "):
            ranges[-1][3].append(row.strip())
        elif ranges and ranges[-1][3] and row.startswith(" "):
            ranges[-1][3][-1] += " " + row.strip()  # a bullet continued
        else:
            problems.append(f"a line that is neither a range `[a–b] English` nor a bullet: {row.strip()[:60]}")
    return title, ranges, problems


def check_block(text: str, block: Passage, check_quotes: bool = True) -> list[str]:
    """The problems of one answer to BLOCK_PROMPT (or GRC_BLOCK_PROMPT, with
    check_quotes=False); [] if it can be kept."""
    title, ranges, problems = parse_block(text)
    if not ranges:
        return problems + ["no ranges `[a–b] English`"]
    expected = block.start
    for first, last, _, _ in ranges:
        if first != expected or last < first:
            problems.append(f"the ranges are {[f'{a}-{b}' for a, b, _, _ in ranges]}, "
                            f"not lines {block.start}–{block.end} once each in order")
            break
        expected = last + 1
    else:
        if expected != block.end + 1:
            problems.append(f"the ranges end at line {expected - 1}, not {block.end}")
    joined = words(" ".join(english for _, _, english, _ in ranges))
    given = words(block.english)
    if joined != given:
        i = next((i for i, (a, b) in enumerate(zip(joined, given)) if a != b),
                 min(len(joined), len(given)))
        problems.append("the English of the ranges, joined, is not the English given: "
                        f"after “{' '.join(given[max(0, i - 5):i])}” it has "
                        f"“{' '.join(joined[i:i + 5])}”, not “{' '.join(given[i:i + 5])}”")
    for first, last, english, bullets in ranges:
        where = f"[{first}–{last}]" if last > first else f"[{first}]"
        if not bullets:
            problems.append(f"{where}: no bullets")
        if not check_quotes:
            continue
        for bullet in bullets:
            if (m := RENDERING_RE.search(bullet)) and words(m.group(1)) == words(m.group(2)):
                problems.append(f"{where}: the word-for-word rendering is the translation's "
                                f"own words, “{m.group(2)}”: leave out a bullet where "
                                f"nothing departs; for a change of word order, take "
                                f"a phrase wide enough to show it (*Alle quai poi* "
                                f"‘to which then’ → “Then to these”)")
            for quote in ENGLISH_QUOTE_RE.findall(bullet):
                if not contains(english, quote):
                    problems.append(f"{where}: not in the English of this range: “{quote}”")
    return problems


def split_english(english: str, counts: list[int]) -> list[str]:
    """english cut into pieces of counts[i] words (as words() counts them),
    each piece keeping the rest of its last word (Peter’s, sixty-six, which
    words() splits) and the punctuation after it, up to a space or a dash."""
    ends = [m.end() for m in WORD_RE.finditer(english.replace("’", "'"))]
    pieces, start, total = [], 0, 0
    for count in counts:
        total += count
        cut = ends[total - 1] if total else 0
        while cut < len(english) and not english[cut].isspace() \
                and english[cut - 1] != "—":
            cut += 1
        pieces.append(english[start:cut].strip())
        start = cut
    pieces[-1] = (pieces[-1] + english[start:]).strip()
    return pieces


def render_block(text: str, block: Passage,
                 greek: dict[int, tuple[str, str]] | None = None) -> str:
    """The section of a checked answer: the heading, then for every range the
    lines, the English as printed, (with greek, the Greek lines and their
    English translation,) and the bullets."""
    title, ranges, _ = parse_block(text)
    pieces = split_english(block.english,
                           [len(words(english)) for _, _, english, _ in ranges])
    lines = {line.no: line.text for line in block.lines}
    rows = [f"## Lines {block.start}–{block.end} — {title}"]
    for (first, last, _, bullets), piece in zip(ranges, pieces):
        rows += [""] + [f"> {no} {lines[no]}  " for no in range(first, last + 1)]
        rows += ["", piece]
        if greek is not None:
            pairs = [f"> {no} {greek[no][0]}  \n> ({greek[no][1]})"
                     for no in range(first, last + 1)]
            rows += ["", "\n>\n".join(pairs)]
        rows += [""] + bullets
    return "\n".join(rows)


def quoted_pairs(text: str) -> list[tuple[int, str, str | None]]:
    """(line number, original, translation or None) of every quoted line."""
    md = text.splitlines()
    pairs = []
    for i, row in enumerate(md):
        if orig := ORIG_RE.match(row):
            trans = TRANS_RE.match(md[i + 1]) if i + 1 < len(md) else None
            pairs.append((int(orig.group(1)), orig.group(2),
                          trans.group(1) if trans else None))
    return pairs


def check_section(text: str, start: int, end: int, lines: list[Line],
                  translations: list[str]) -> list[str]:
    """The problems of one answer; [] if it can be kept."""
    problems = []
    headings = [row for row in text.splitlines() if row.startswith("#")]
    if not headings or not (m := SECTION_RE.match(headings[0])) \
            or (int(m.group(1)), int(m.group(2))) != (start, end):
        problems.append(f"the heading is not `## Lines {start}–{end} — ...`")
    if len(headings) > 1:
        problems.append(f"{len(headings)} headings")
    pairs = quoted_pairs(text)
    numbers = [no for no, _, _ in pairs]
    if numbers != list(range(start, end + 1)):
        problems.append(f"quoted lines {numbers}, not {start}–{end} once each in order")
    for no, orig, trans in pairs:
        if not start <= no <= end:
            continue
        if not same_line(orig, lines[no - 1].text):
            problems.append(f"line {no}: the quoted original does not match")
        if trans is None:
            problems.append(f"line {no}: no translation after the quote")
        elif not same_line(trans, translations[no - 1]):
            problems.append(f"line {no}: the quoted translation does not match")
    return problems


def ask(client: Client, messages: list[str], check, tries: int, label: str,
        repair: bool = False, repair_prompt: str = REPAIR_PROMPT) -> str | None:
    """The first answer with no problems, or None after tries answers. With
    repair, a rejected answer is sent back with its problems to be
    corrected (repair_prompt); otherwise the question is asked again. The
    call is recorded in ASKED under label."""
    text, problems, rejected = None, [], []
    for attempt in range(1, tries + 1):
        if repair and text is not None:
            history = client.history
            client.history = [{"role": "user", "content": m} for m in messages] \
                + [{"role": "assistant", "content": text}]
            try:
                listed = "\n".join(f"- {problem}" for problem in problems)
                text = client(repair_prompt.format(problems=listed)).text.strip()
            finally:
                client.history = history
        else:
            text = client(messages).text.strip()
        if not (problems := check(text)):
            ASKED.append((label, rejected, True))
            return text
        print(f"\nanswer {attempt} rejected:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        more = f" (and {len(problems) - 1} more)" if len(problems) > 1 else ""
        rejected.append(problems[0] + more)
    ASKED.append((label, rejected, False))
    return None


def print_rejections():
    """List the calls that had answers rejected, each with the first problem
    of every rejected answer, and the count of all."""
    print("\n--- Rejections ---")
    for label, rejected, passed in ASKED:
        if rejected:
            result = f"passed on answer {len(rejected) + 1}" if passed else "none passed"
            print(f"{label}: {len(rejected)} ({result})")
            for attempt, problem in enumerate(rejected, 1):
                print(f"  answer {attempt}: {problem}")
    count = sum(len(rejected) for _, rejected, _ in ASKED)
    print(f"{count} rejected answer(s) in {len(ASKED)} call(s)")


def open_commentary(path: Path, canticle: str, canto: int) -> str | None:
    """The commentary saved so far (or its title, if none), or None if it is
    complete."""
    if path.exists():
        saved = path.read_text()
        if any(row.startswith(SUMMARY_HEADING) for row in saved.splitlines()):
            print(f"Skipped (already complete): {path}")
            return None
        print(f"Resuming from {path}")
        return saved
    return f"# {CANTICLE_NAMES[canticle]} {canto}\n"


def save(path: Path, saved: str, part: str) -> str:
    """saved with part appended, written to path."""
    saved = saved.rstrip("\n") + "\n\n" + part.strip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(saved)
    print(f"\nSaved to {path}")
    return saved


def done_sections(saved: str) -> set[int]:
    """The last lines of the sections saved."""
    return {int(m.group(2)) for row in saved.splitlines() if (m := SECTION_RE.match(row))}


def summarize(client: Client, messages: list[str], tries: int, canto: int,
              english: str | None = None, repair: bool | None = None,
              repair_prompt: str = REPAIR_PROMPT) -> str | None:
    """The closing summary; with english (a prose translation), every phrase
    in double quotation marks must be found in it, and a rejected summary
    is sent back to be corrected."""
    def check(answer: str) -> list[str]:
        problems = [] if answer.startswith(f"{SUMMARY_HEADING} — ") \
            else [f"does not open with `{SUMMARY_HEADING} — ...`"]
        if english is not None:
            problems += [f"not in the English: “{quote}”"
                         for quote in ENGLISH_QUOTE_RE.findall(answer)
                         if not contains(english, quote)]
        return problems
    return ask(client, messages, check, tries, f"canto {canto}, summary",
               repair=(english is not None) if repair is None else repair,
               repair_prompt=repair_prompt)


def is_grc_en(source: str, lang_code: str | None) -> bool:
    """Whether source is grc explained against Oelsner's Italian and English
    with translations/en/grc/ (Step 3: grammar/grc/)."""
    return source == "grc" and lang_code == "en"


def is_grc_el(source: str, lang_code: str | None) -> bool:
    """Whether source is grc explained against the Modern Greek translation
    of commentary/el-grc/ (Step 4: grammar/el-grc/)."""
    return source == "grc" and lang_code == "el"


def commentary_path(out: Path, source: str, canticle: str, canto: int,
                    lang_code: str | None = None) -> Path:
    """The commentary on a canto: <out>/<canticle>/<NN>.md, or, for a source
    printed with a prose translation (or grc with en), <out>/ and the name of
    its file of texts/ (as <out>/007-canto-01.md)."""
    if "prose" in SOURCES[source] or is_grc_en(source, lang_code):
        return out / text_path(source, canto).name
    return out / canticle / f"{canto:02d}.md"


def explain(client: Client, canticle: str, canto: int, args: argparse.Namespace) -> bool:
    """Write or continue <out>/<canticle>/<NN>.md; False if a section failed."""
    source = SOURCES[args.source]
    if "prose" in source:
        return compare(client, canticle, canto, args)
    if is_grc_en(args.source, args.lang_code):
        return compare_grc(client, canticle, canto, args)
    lines = source_lines(args.source, canticle, canto)
    names = dict(
        source=source["name"], language=source["language"],
        canticle=CANTICLE_NAMES[canticle], number=canto,
        lang=LANGUAGES[args.lang_code]["name"],
    )
    trans_path = args.dir / canticle / f"{canto:02d}.txt"
    translations = trans_path.read_text().splitlines()
    if len(translations) != len(lines) or not all(translations):
        print(f"{trans_path}: not one translation per line of the source, skipped",
              file=sys.stderr)
        return False
    text = canto_text(lines, translations)
    originals = {line.no: line.text for line in lines}
    grc_el = is_grc_el(args.source, args.lang_code)

    out_path = commentary_path(args.out, args.source, canticle, canto, args.lang_code)
    if (saved := open_commentary(out_path, canticle, canto)) is None:
        return True
    done = done_sections(saved)

    def append(part: str):
        nonlocal saved
        rows = rebuild_lines(out_path, part.splitlines(), originals, translations)
        saved = save(out_path, saved, "\n".join(rows))

    for start, end in sections(lines, source["language"], args.size):
        if end in done:
            continue
        print(f"\n--- canto {canto}, lines {start}-{end} ---")
        if grc_el:
            prompt = GRC_EL_PROMPT.format(**names, start=start, end=end)
        else:
            prompt = PROMPT.format(**names, start=start, end=end,
                                   focus=FOCUS[source["language"]])
        answer = ask(
            client, [text, prompt],
            lambda answer: check_section(answer, start, end, lines, translations),
            args.tries, f"canto {canto}, lines {start}-{end}",
            repair=True, repair_prompt=SECTION_REPAIR_PROMPT,
        )
        if answer is None:
            print(f"\ncanto {canto}, lines {start}-{end}: no answer passed, "
                  f"canto left unfinished", file=sys.stderr)
            return False
        append(answer)

    print(f"\n--- canto {canto}, summary ---")
    if grc_el:
        prompt = GRC_EL_SUMMARY_PROMPT.format(**names)
    else:
        prompt = SUMMARY_PROMPT.format(**names, layout=LAYOUT.format(lang=names["lang"]))
    if (answer := summarize(client, [text, saved, prompt], args.tries, canto,
                            repair=True, repair_prompt=SECTION_REPAIR_PROMPT)) is None:
        print(f"\ncanto {canto}: no summary passed", file=sys.stderr)
        return False
    append(answer)
    return True


def compare_grc(client: Client, canticle: str, canto: int, args: argparse.Namespace) -> bool:
    """Write or continue the commentary on Musurus's Greek (grammar/grc/)
    against Oelsner's Italian and English, spread by spread; False if a block
    failed."""
    source = SOURCES["grc"]
    oelsner = SOURCES["en-oelsner"]
    blocks = oelsner_passages(canto)
    greek = {g.no: (g.text, e.text)
             for g, e in zip(grc_lines(canto), en_grc_lines(canto))}
    names = dict(
        source=source["name"], italian_source=oelsner["name"], prose=oelsner["prose"],
        canticle=CANTICLE_NAMES[canticle], number=canto,
        focus=FOCUS[source["language"]],
    )
    out_path = commentary_path(args.out, args.source, canticle, canto, args.lang_code)
    if (saved := open_commentary(out_path, canticle, canto)) is None:
        return True
    done = done_sections(saved)

    for block in blocks:
        if block.end in done:
            continue
        print(f"\n--- canto {canto}, lines {block.start}-{block.end} ---")
        prompt = GRC_BLOCK_PROMPT.format(**names, start=block.start, end=block.end)
        answer = ask(client, [block_text(block, greek), prompt],
                     lambda answer: check_block(answer, block, check_quotes=False),
                     args.tries, f"canto {canto}, lines {block.start}-{block.end}",
                     repair=True)
        if answer is None:
            print(f"\ncanto {canto}, lines {block.start}-{block.end}: no answer passed, "
                  f"canto left unfinished", file=sys.stderr)
            return False
        saved = save(out_path, saved, render_block(answer, block, greek))

    print(f"\n--- canto {canto}, summary ---")
    text = "\n\n".join(block_text(block, greek) for block in blocks)
    prompt = GRC_SUMMARY_PROMPT.format(**names)
    if (answer := summarize(client, [text, saved, prompt], args.tries, canto,
                            repair=True)) is None:
        print(f"\ncanto {canto}: no summary passed", file=sys.stderr)
        return False
    saved = save(out_path, saved, answer)
    return True


def compare(client: Client, canticle: str, canto: int, args: argparse.Namespace) -> bool:
    """Write or continue the commentary (commentary_path) on a source printed
    with a prose translation, block by block; False if a block failed."""
    source = SOURCES[args.source]
    blocks = BLOCKS[args.source](canto)
    names = dict(
        source=source["name"], language=source["language"], prose=source["prose"],
        canticle=CANTICLE_NAMES[canticle], number=canto,
    )
    out_path = commentary_path(args.out, args.source, canticle, canto)
    if (saved := open_commentary(out_path, canticle, canto)) is None:
        return True
    done = done_sections(saved)

    for block in blocks:
        if block.end in done:
            continue
        print(f"\n--- canto {canto}, lines {block.start}-{block.end} ---")
        prompt = BLOCK_PROMPT.format(**names, start=block.start, end=block.end)
        answer = ask(client, [block_text(block), prompt],
                     lambda answer: check_block(answer, block), args.tries,
                     f"canto {canto}, lines {block.start}-{block.end}", repair=True)
        if answer is None:
            print(f"\ncanto {canto}, lines {block.start}-{block.end}: no answer passed, "
                  f"canto left unfinished", file=sys.stderr)
            return False
        saved = save(out_path, saved, render_block(answer, block))

    print(f"\n--- canto {canto}, summary ---")
    text = "\n\n".join(block_text(block) for block in blocks)
    prompt = PROSE_SUMMARY_PROMPT.format(**names)
    english = " ".join(block.english for block in blocks)
    if (answer := summarize(client, [text, saved, prompt], args.tries, canto,
                            english)) is None:
        print(f"\ncanto {canto}: no summary passed", file=sys.stderr)
        return False
    saved = save(out_path, saved, answer)
    return True


def list_notes(canticle: str, cantos, out: Path, source: str,
               lang_code: str | None = None):
    """Print every `Translation note:` paragraph with the lines quoted last
    before it."""
    count = 0
    for canto in cantos:
        path = commentary_path(out, source, canticle, canto, lang_code)
        if not path.exists():
            continue
        quoted: list[int] = []
        last_quote = True
        for row in path.read_text().splitlines():
            if orig := ORIG_RE.match(row):
                if not last_quote:
                    quoted = []
                quoted.append(int(orig.group(1)))
                last_quote = True
            elif row.startswith(">"):
                pass
            else:
                if row.strip():
                    last_quote = False
                if NOTE_RE.match(row):
                    where = f"{quoted[0]}-{quoted[-1]}" if quoted else "?"
                    print(f"{path}:{where}: {row}\n")
                    count += 1
    print(f"{count} translation note(s)")


def main():
    global USAGE_PATH
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("canticle", choices=list(CANTICLE_NAMES),
                        help="Canticle name: inferno, purgatorio, or paradiso")
    parser.add_argument("-c", "--canto", help=CANTO_SPEC_HELP)
    parser.add_argument("-m", "--model",
                        help="Model name with optional vendor prefix (e.g. gpt-6-astra); "
                             "required unless --notes")
    parser.add_argument("-l", "--lang-code", choices=list(LANGUAGES),
                        help="Language code of the translation (e.g. el); "
                             "required unless --notes or the source has its own prose translation")
    parser.add_argument("-s", "--source", choices=list(SOURCES), default="it",
                        help="Source text to explain (default: it)")
    parser.add_argument("-d", "--dir", type=Path,
                        help="Directory holding the translations <canticle>/<NN>.txt; "
                             "required unless --notes or the source has its own prose translation")
    parser.add_argument("-o", "--out", type=Path, required=True,
                        help="Output directory for <canticle>/<NN>.md, or for the "
                             "files named as in texts/ for a source with its own "
                             "prose translation")
    parser.add_argument("--size", type=int, default=30,
                        help="Lines per section, roughly (default: 30)")
    parser.add_argument("-t", "--tries", type=int, default=3,
                        help="Answers asked for one section before giving up (default: 3)")
    parser.add_argument("-n", "--notes", action="store_true",
                        help="Only list the translation notes of the saved commentaries")
    parser.add_argument("--no-think", action="store_true",
                        help="Disable thinking output (include_thoughts=False)")
    parser.add_argument("--save-usage", action="store_true",
                        help="Record usage regardless of model name")
    args = parser.parse_args()

    if err := check_canto_spec([args.canticle], args.canto):
        parser.error(err)
    if args.canticle not in SOURCES[args.source]["canticles"]:
        parser.error(f"source {args.source} has no {args.canticle}")
    cantos = select_cantos(args.canticle, args.canto)
    if args.notes:
        list_notes(args.canticle, cantos, args.out, args.source, args.lang_code)
        return
    if "prose" in SOURCES[args.source] or is_grc_en(args.source, args.lang_code):
        required = ["model"]
    else:
        required = ["model", "lang_code", "dir"]
    for name in required:
        if getattr(args, name) is None:
            parser.error(f"--{name.replace('_', '-')} is required")

    if args.model.startswith(("openai:", "gpt-")) or args.save_usage:
        USAGE_PATH = find_usage_file()

    client = Client(
        model=args.model,
        include_thoughts=not args.no_think,
        show_params=False,
        keep_history=False,
        show_usage=True,
    )

    failed = []
    try:
        for canto in cantos:
            if not explain(client, args.canticle, canto, args):
                failed.append(canto)
    finally:
        if client.usages and USAGE_PATH is not None:
            append_usage(sum(client.usages), args.model, USAGE_PATH)

    if ASKED:
        print_rejections()
    if client.usages:
        print(f"\n--- Total Usage ---\n{sum(client.usages)}")
        if USAGE_PATH is not None:
            print()
            print_today_totals(USAGE_PATH, models=[args.model])
    if failed:
        print(f"\nunfinished cantos: {failed}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
