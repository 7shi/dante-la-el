"""Convert ocr/la/NNNN.txt (Serravalle's translation and commentary, 1891) into texts/la/NNN-title.md.

The whole volume is converted (scans 0007–1290; see ocr/la/PLAN.md for the transcription). See texts/PLAN.md for the layout. Run from the repository root:

    uv run texts/scripts/convert_la.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "ocr" / "la"
DST = ROOT / "texts" / "la"

# Verses per canto (dante-corpus).
VERSES = {
    "inferno": [136, 142, 136, 151, 142, 115, 130, 130, 133, 136, 115, 139, 151, 142, 124, 136,
                136, 136, 133, 130, 139, 151, 148, 151, 151, 142, 136, 142, 139, 148, 145, 139,
                157, 139],
    "purgatorio": [136, 133, 145, 139, 136, 151, 136, 139, 145, 139, 142, 136, 154, 151, 145,
                   145, 139, 145, 145, 151, 136, 154, 133, 154, 139, 148, 142, 148, 154, 145,
                   145, 160, 145],
    "paradiso": [142, 148, 130, 142, 139, 142, 148, 148, 142, 148, 139, 145, 142, 139, 148, 154,
                 142, 136, 148, 148, 142, 154, 139, 154, 139, 142, 148, 139, 145, 148, 142, 151,
                 145],
}

# Cantos converted: (first scan, the scan of the essay, last scan), from INDEX.md.
CANTOS = {"inferno": [(79, 92, 92), (93, 102, 102), (103, 114, 114), (115, 127, 128),
                      (129, 139, 140), (141, 150, 150), (151, 161, 162), (163, 171, 172),
                      (173, 183, 184), (185, 196, 196), (197, 206, 206), (207, 220, 220),
                      (221, 232, 232), (233, 243, 244), (245, 255, 256), (257, 267, 268),
                      (269, 279, 280), (281, 291, 292), (293, 303, 304), (305, 314, 314),
                      (315, 324, 326), (327, 336, 336), (337, 347, 348), (349, 359, 360),
                      (361, 370, 370), (371, 382, 382), (383, 394, 394), (395, 407, 408),
                      (409, 418, 418), (419, 429, 430), (431, 440, 440), (441, 451, 452),
                      (453, 463, 464), (465, 475, 476)],
          "purgatorio": [(487, 497, 498), (499, 508, 508), (509, 519, 520), (521, 531, 532),
                         (533, 542, 542), (543, 553, 554), (555, 564, 564), (565, 574, 574),
                         (575, 586, 586), (587, 596, 596), (597, 607, 608), (609, 619, 620),
                         (621, 630, 630), (631, 643, 644), (645, 655, 656), (657, 668, 668),
                         (669, 679, 680), (681, 691, 692), (693, 703, 704), (705, 717, 718),
                         (719, 728, 728), (729, 739, 740), (741, 750, 750), (751, 761, 762),
                         (763, 773, 774), (775, 785, 786), (787, 797, 798), (799, 812, 812),
                         (813, 823, 824), (825, 834, 834), (835, 845, 846), (847, 858, 858),
                         (859, 869, 870)],
          "paradiso": [(873, 887, 888), (889, 901, 902), (903, 912, 912), (913, 924, 924),
                       (925, 934, 934), (935, 948, 948), (949, 959, 960), (961, 972, 972),
                       (973, 984, 984), (985, 996, 996), (997, 1008, 1010), (1011, 1023, 1024),
                       (1025, 1035, 1036), (1037, 1047, 1048), (1049, 1059, 1060),
                       (1061, 1072, 1072), (1073, 1083, 1084), (1085, 1095, 1096),
                       (1097, 1108, 1108), (1109, 1119, 1120), (1121, 1130, 1130), (1131, 1140, 1140),
                       (1141, 1149, 1150), (1151, 1161, 1162), (1163, 1172, 1172),
                       (1173, 1183, 1184), (1185, 1196, 1196), (1197, 1208, 1208),
                       (1209, 1220, 1220), (1221, 1231, 1232), (1233, 1243, 1244),
                       (1245, 1255, 1256), (1257, 1270, 1270)]}
# The first file of each cantica's cantos (001–007 are the front matter, not converted yet;
# 042 is the Purgatorio's preambula).
FIRST_FILE = {"inferno": 8, "purgatorio": 43, "paradiso": 76}
RUNNING_HEAD = {"inferno": "INFERNI", "purgatorio": "PURGATORII", "paradiso": "PARADISI"}
# The cantica's half-title that opens its first canto file, and the heading printed above
# the first canto's *Summarium*.
HALF_TITLE = {"inferno": 77, "paradiso": 871}
INCIPIT = {"paradiso": "INCIPIT PARADISUS"}
# Prose sections of one column: (file, first scan, last scan, the heading of the first page).
PROSE = [("042-purgatorio-preambula.md", 477, 486, "PREAMBULA")]
# Bartholomaeus a Colle's fragments: (file, first scan, last scan, running head), and the
# headings printed in capitals, as written here.
APPENDIX = ("109-appendix.md", 1271, 1287, "CANTICA PARADISI")
APPENDIX_HEADINGS = {
    "FRAGMENTA COMMENTARII SUPER COMOEDIAM DANTIS ALDIGHERII":
        "Fragmenta commentarii super Comoediam Dantis Aldigherii",
    "INCIPIT TERTIA CANTICA PARADISI ET CANTUS PRIMUS":
        "Incipit tertia cantica Paradisi et cantus primus",
    "CANTUS II PARADISI": "Cantus II Paradisi",
    "CANTUS TERTIUS": "Cantus tertius",
}
INDEX = ("110-index.md", 1289, 1290, "INDEX")
# The front matter: (file, scans, running head). Title pages (TITLE_PAGES) are kept line
# by line; a one-line half-title is a heading.
FRONT = [
    ("001-title-page.md", [7, 9, 10], None),
    ("002-dedication-to-leo-xiii.md", [11, 13, 14], None),
    ("003-notizie-preliminari.md", list(range(15, 43)), "NOTIZIE PRELIMINARI"),
    ("004-documenta.md", [43] + list(range(45, 55)), "DOCUMENTA"),
    ("005-dedicatio.md", [55, 57], None),
    ("006-epistola.md", [59, 60], "DEDICATIO"),
    ("007-preambula.md", list(range(61, 77)), "PREAMBULA"),
]
TITLE_PAGES = {7, 9, 10, 11, 43, 55, 57}
ROMAN_OFFSET = 6  # printed Roman page = scan - 6 (0011 = V)
FOOTNOTE = re.compile(r"\((\d)\) (.*)")
OFFSET = 54  # printed page = scan - 54

ORDINALS = ["PRIMUM", "SECUNDUM", "TERTIUM", "QUARTUM", "QUINTUM", "SEXTUM", "SEPTIMUM",
            "OCTAVUM", "NONUM", "DECIMUM", "UNDECIMUM", "DUODECIMUM", "TERTIUMDECIMUM",
            "QUARTUMDECIMUM", "QUINTUMDECIMUM", "SEXTUMDECIMUM", "DECIMUMSEPTIMUM",
            "DECIMUMOCTAVUM", "DECIMUMNONUM", "VICESIMUM", "VICESIMUMPRIMUM",
            "VICESIMUMSECUNDUM", "VICESIMUMTERTIUM", "VICESIMUMQUARTUM", "VICESIMUMQUINTUM",
            "VICESIMUMSEXTUM", "VICESIMUMSEPTIMUM", "VICESIMUMOCTAVUM", "VICESIMUMNONUM",
            "TRICESIMUM", "TRICESIMUMPRIMUM", "TRICESIMUMSECUNDUM", "TRICESIMUMTERTIUM",
            "TRICESIMUMQUARTUM"]
GENITIVES = ["PRIMI", "SECUNDI", "TERTII", "QUARTI", "QUINTI", "SEXTI", "SEPTIMI", "OCTAVI",
             "NONI", "DECIMI", "UNDECIMI", "DUODECIMI", "TERTIIDECIMI", "QUARTIDECIMI",
             "QUINTIDECIMI", "SEXTIDECIMI", "DECIMISEPTIMI", "DECIMIOCTAVI", "DECIMINONI",
             "VICESIMI", "VICESIMIPRIMI", "VICESIMISECUNDI", "VICESIMITERTII", "VICESIMIQUARTI",
             "VICESIMIQUINTI", "VICESIMISEXTI", "VICESIMISEPTIMI", "VICESIMIOCTAVI",
             "VICESIMINONI", "TRICESIMI", "TRICESIMIPRIMI", "TRICESIMISECUNDI", "TRICESIMITERTII",
             "TRICESIMIQUARTI"]

# The essays' titles as printed, in the case of INDEX.md (where it reads `angeli`, the print
# has `ANGIOLI`).
ESSAYS = {
    "LA DIVINA COMMEDIA": "La divina commedia",
    "ROMA NEL CONCETTO DI DANTE": "Roma nel concetto di Dante",
    "L'INFERNO E L'AMOR DIVINO": "L'inferno e l'amor divino",
    "LA FEDE DI DANTE": "La fede di Dante",
    "MINOSSE E LA REA COSCIENZA NELL' ETERNITÀ": "Minosse e la rea coscienza nell'eternità",
    "LA RISURREZIONE DEI CORPI": "La risurrezione dei corpi",
    "IL PECCATO DEGLI ANGIOLI": "Il peccato degli angioli",
    "IL SIMBOLISMO NELLE VISIONI": "Il simbolismo nelle visioni",
    "GLI ANGIOLI BUONI E CATTIVI": "Gli angioli buoni e cattivi",
    "LA SELVA IN CUI SI SMARRÌ L'ALIGHIERI": "La selva in cui si smarrì l'Alighieri",
    "L'ARTE DIVINA E L'ARTE UMANA": "L'arte divina e l'arte umana",
    "I PRODIGI NELLA MORTE DI CRISTO": "I prodigi nella morte di Cristo",
    "FEDERICO II.": "Federico II",
    "IL VALORE DELLE FAVOLE": "Il valore delle favole",
    "INTEGREZZA DEL SENTIMENTO MORALE IN DANTE": "Integrezza del sentimento morale in Dante",
    "IL CINGOLO DI DANTE": "Il cingolo di Dante",
    "LA FIERA DESCRITTA DAL POETA IN QUESTO CANTO": "La fiera descritta dal Poeta in questo canto",
    "SEGUITA L'ARGOMENTO DELLA FRODE": "Seguita l'argomento della frode",
    "VERI SENTIMENTI DELL'ALIGHIERI RISPETTO A' PONTEFICI VICARII DI GESÙ CRISTO":
        "Veri sentimenti dell'Alighieri rispetto a' pontefici vicarii di Gesù Cristo",
    "LO SPIRITISMO": "Lo spiritismo",
    "SE SIA POSSIBILE LA DIMINUZIONE PROGRESSIVA DELLE PENE ETERNE":
        "Se sia possibile la diminuzione progressiva delle pene eterne",
    "NATURA DEGLI SPIRITI INFERNALI": "Natura degli spiriti infernali",
    "L' IPOCRISIA": "L'ipocrisia",
    "LA VERA GLORIA DELL'UOMO": "La vera gloria dell'uomo",
    "UNA CONSIDERAZIONE SOPRA LE PRIME DUE TERZINE DI QUESTO CANTO":
        "Una considerazione sopra le prime due terzine di questo canto",
    "L'AMERICA": "L'America",
    "L'ACCENTRAMENTO DELLO SPIRITO IN SÈ STESSO NELL'INFERNO E FRATE GUIDO DA MONTEFELTRO":
        "L'accentramento dello spirito in sè stesso nell'Inferno e Frate Guido da Montefeltro",
    "L'UNITÀ DEL CATTOLICISMO E LA PUNIZIONE DELLE SCISSURE CHE LACERARONO LA CHIESA":
        "L'unità del cattolicismo e la punizione delle scissure che lacerarono la Chiesa",
    "L'ALCHIMIA": "L'alchimia",
    "I SOGNI": "I sogni",
    "I GIGANTI E LA CONFUSIONE DELLE LINGUE": "I giganti e la confusione delle lingue",
    "IL GHIACCIO IN FONDO ALL'INFERNO": "Il ghiaccio in fondo all'inferno",
    "I TRADITORI": "I traditori",
    "SATANA": "Satana",
    "IL PURGATORIO NEL CONCETTO DI DANTE": "Il purgatorio nel concetto di Dante",
    "L'EPISODIO DI CASELLA E STATO VERO DELLE ANIME NEL PURGATORIO":
        "L'episodio di Casella e stato vero delle anime nel Purgatorio",
    "LA NOSTRA SCIENZA E GESÙ CRISTO": "La nostra scienza e Gesù Cristo",
    "L'UNITÀ SOSTANZIALE DELL'ANIMA UMANA": "L'unità sostanziale dell'anima umana",
    "RELAZIONI CHE RESTANO TRA L'ANIMA E IL CORPO DOPO MORTE":
        "Relazioni che restano tra l'anima e il corpo dopo morte",
    "PERMANENZA DI AFFETTUOSE RELAZIONI FRA NOI E IL PURGATORIO":
        "Permanenza di affettuose relazioni fra noi e il Purgatorio",
    "LA GRAZIA": "La grazia",
    "L'AVE MARIA DELLA SERA E IL DE PROFUNDIS": "L'Ave Maria della sera e il De Profundis",
    "LA MISERICORDIA DIVINA SUPREMO PRINCIPIO DI SALUTE":
        "La misericordia divina supremo principio di salute",
    "CORRISPONDENZA TRA LA COLPA E L'ESPIAZIONE": "Corrispondenza tra la colpa e l'espiazione",
    "L'UMANA MESTIZIA E IL NOSTRO SOSPIRO ALL'INFINITO":
        "L'umana mestizia e il nostro sospiro all'Infinito",
    "L'UMILTÀ PRINCIPIO D'OGNI GRANDEZZA": "L'umiltà principio d'ogni grandezza",
    "DOLORE, PREGHIERA E AMORE NEL PURGATORIO": "Dolore, preghiera e amore nel Purgatorio",
    "I BENI TERRENI ED IL BENE ETERNO": "I beni terreni ed il bene eterno",
    "MISERABILE PUNIZIONE CHE IL POETA DÀ AL VIZIO DELL'IRA E PROFONDO INSEGNAMENTO CHE "
    "V'INCHIUSE": "Miserabile punizione che il Poeta dà al vizio dell'ira e profondo insegnamento"
                  " che v'inchiuse",
    "LA LIBERTÀ UMANA E LA SUPREMA SUA LEGGE": "La libertà umana e la suprema sua legge",  # 0668, a misprint mark
    "L'AMORE VITA DELL'UNIVERSO": "L'amore vita dell'universo",
    "IL CUORE RADICE DEL PENSIERO": "Il cuore radice del pensiero",
    "BASSEZZA DEL VIZIO DELL'ACCIDIA E SUBLIMITÀ DEL SUO CONTRAPPOSTO, LA FATICA E IL DOLORE":
        "Bassezza del vizio dell'accidia e sublimità del suo contrapposto, la fatica e il dolore",
    "LA SALITA DELLE ANIME AL CIELO": "La salita delle anime al cielo",
    "NESSO FRA L'ORDINE DI NATURA E IL SOPRANNATURALE":
        "Nesso fra l'ordine di natura e il soprannaturale",
    "LA VIRTÙ DELLA GIUSTIZIA": "La virtù della giustizia",
    "LA PIETÀ VERSO GLI ESTINTI, SPECIALMENTE NELLA VERA DONNA CRISTIANA":
        "La pietà verso gli estinti, specialmente nella vera donna cristiana",
    "PICCARDA DONATI E L'EROISMO DELLA VERGINITÀ": "Piccarda Donati e l'eroismo della verginità",
    "L'APPARIZIONE DEGLI SPIRITI": "L'apparizione degli spiriti",
    "LA PENA DEL FUOCO A PURGAZIONE DELLE COLPE DEL SENSO":
        "La pena del fuoco a purgazione delle colpe del senso",
    "L'EDEN IN CIMA ALLA MONTAGNA DANTESCA DEL PURGATORIO":
        "L'Eden in cima alla montagna dantesca del Purgatorio",
    "LA FONTANA DELL'EDEN": "La fontana dell'Eden",
    "IL CARRO IMMAGINATO DAL POETA IN QUESTO CANTO E LA CHIESA":
        "Il carro immaginato dal Poeta in questo canto e la Chiesa",
    "LA VISIONE DI BEATRICE": "La visione di Beatrice",
    "LA CONFESSIONE": "La confessione",
    "LA SCIENZA DEL BENE E DEL MALE": "La scienza del bene e del male",
    "IL TRIONFO FINALE DEL BENE": "Il trionfo finale del bene",
    "IL PARADISO": "Il Paradiso",
    "L'IDEA DIVINA NELL' UNIVERSO": "L'idea divina nell'universo",
    "IL FORMALE DEL GAUDIO ETERNO NELLA CARITÀ": "Il formale del gaudio eterno nella carità",
    "IL DUBBIO E LA CERTEZZA": "Il dubbio e la certezza",
    "IL VOTO E LA LIBERTÀ": "Il voto e la libertà",
    "GIUSTINIANO E LE LEGGI": "Giustiniano e le leggi",
    "LA CREAZIONE E LA REDENZIONE": "La creazione e la redenzione",
    "LA SOCIETÀ E GLI INDIVIDUI": "La società e gli individui",
    "IL PIANETA DI VENERE": "Il pianeta di venere",
    "L' UNITÀ DIVINA E L' UNITÀ DELLA SCIENZA": "L'unità divina e l'unità della scienza",
    "SAN FRANCESCO E SAN DOMENICO E LE LORO INSTITUZIONI":
        "San Francesco e San Domenico e le loro instituzioni",
    "LA SCIENZA E I DUE ORDINI DI SAN DOMENICO E DI SAN FRANCESCO":
        "La scienza e i due Ordini di San Domenico e di San Francesco",
    "LA GENERAZIONE ETERNA DEL VERBO E LA TEOLOGIA": "La generazione eterna del Verbo e la Teologia",
    "SE L'UOMO AVRÀ ACCRESCIMENTO DI GAUDIO PER LA RIASSUNZIONE DEL PROPRIO CORPO NEL DÌ NOVISSIMO":
        "Se l'uomo avrà accrescimento di gaudio per la riassunzione del proprio corpo nel dì"
        " novissimo",
    "LA DONNA NELLA SOCIETÀ CRISTIANA": "La donna nella società cristiana",
    "LE ANIME VERAMENTE GRANDI": "Le anime veramente grandi",
    "LA PRESCIENZA DIVINA E LA LIBERTÀ UMANA": "La prescienza divina e la libertà umana",
    "L'UMANA PERFETTIBILITÀ": "L'umana perfettibilità",
    "L'UNITÀ DI VOLERE NEL CUORE DE'GIUSTI": "L'unità di volere nel cuore de'giusti",
    "LA FEDE E L'IMPUTAZIONE": "La fede e l'imputazione",
    "IL RISO DE' BEATI IN CIELO": "Il riso de'beati in cielo",
    "SAN BENEDETTO": "San Benedetto",
    "LA VERGINE MADRE": "La Vergine Madre",
    "FEDE E RAGIONE": "Fede e ragione",
    "GENESI E NATURA DELLA SPERANZA": "Genesi e natura della speranza",
    "LA PAROLA NELL'UOMO": "La parola nell'uomo",
    "IL CANTO NEL CIELO E LA MUSICA": "Il canto nel cielo e la musica",
    "IL MOTO E LA QUIETE E L'IMMENSITÀ DIVINA": "Il moto e la quiete e l'immensità divina",
    "LA PREDICAZIONE": "La predicazione",
    "IL LUME DI GLORIA": "Il lume di gloria",
    "LA VISIONE IN CIELO": "La visione in cielo",
    "INNOCENZA, MERITO E PREMIO": "Innocenza, merito e premio",
    "LA PREGHIERA": "La preghiera",
}

# Tercet numbers misprinted (ocr/la/PLAN.md, Suspected misprints): (scan, column, tercet) -> printed.
MISNUMBERED = {(350, "it", 2): 3, (758, "it", 38): 37, (810, "la", 46): 45, (1182, "it", 47): 57}
# Running heads misprinted: scan -> printed.
MISPRINTED_HEAD = {710: "PURGATORI"}

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
NUMBER = re.compile(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+|\d+) ")  # a tercet number at the start of a verse line
# The scribe's verses at the end of a cantica, with their own gloss line: scan -> first words.
COLOPHON = {868: "Qui scripsit scribat", 1268: "Qui scripsit scribat"}
CLOSING = re.compile(r"(?:FINIT|EXPLICIT) [A-Z ]+\.$")
GLOSS = re.compile(r"\((?:[¹²³⁴⁵⁶⁷⁸⁹]+|\d{1,2})\)")  # `(1) costui. — (2) sarà.`


# A misprint mark `{{printed|fixed}}` (ocr/la/PLAN.md, "Misprint marks"), or a correction from the
# corrigenda, `{{printed|LIST|fixed}}` (ocr/PLAN.md, "Decisions"): the text keeps the fix.
MISPRINT = re.compile(r"\{\{([^{}|]*)\|(?:([0-9]+(?:&[0-9]+)*)\|)?([^{}|]*)\}\}")


def fixed(t):
    return MISPRINT.sub(r"\3", t)


def text_of(n):
    return fixed((SRC / f"{n:04d}.txt").read_text(encoding="utf-8")).replace("’", "'")


def marker(n, printed=True):
    p = n - OFFSET
    return f"<!-- p. {p if printed else f'[{p}]'} ({n:04d}) -->"


def blocks(lines):
    """The blank-separated blocks of lines."""
    out, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l.strip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def esc(line):
    """Keep a line from being read as Markdown list or heading syntax."""
    line = re.sub(r"^(\d+)\. ", r"\1\\. ", line)
    return re.sub(r"^([-+*#>]) ", r"\\\1 ", line)


# ---------------------------------------------------------------- hyphenation

WORD = r"[^\W\d_]+"
VOCAB = set()
for f in SRC.glob("[0-9][0-9][0-9][0-9].txt"):
    t = re.sub(r"(?<!\d)\*", "", fixed(f.read_text(encoding="utf-8"))).replace("’", "'")
    # the fragments of words hyphenated at a line end are not words
    t = re.sub(WORD + r"-\n\s*" + WORD, " ", t)
    VOCAB.update(w.lower() for w in re.findall(WORD + r"(?:-" + WORD + r")*", t))
UNDECIDED = []

# Line-end hyphens decided by hand: the word as it is to be written.
HYPHEN_FIXED = {}

# Words broken at a line end with no hyphen printed: the page, the last word of the line and
# the first of the next, joined without a space. Empty: the two such places (0639 `vir`,
# 1165 `pere`) are misprint marks now, whose fixed side has the hyphen.
HYPHEN_MISSING = set()


def join_hyphen(head, tail, where):
    m1 = re.search(r"(" + WORD + r")-$", head)
    m2 = re.match(r"\W*?(" + WORD + r")", tail)
    if not m1 or not m2:
        return head + tail
    a, b = m1.group(1), m2.group(1)
    key = f"{a}-{b}".lower()
    if key in HYPHEN_FIXED:
        sep = "-" if "-" in HYPHEN_FIXED[key] else ""
    elif (a + b).lower() in VOCAB:
        sep = ""  # the unbroken form wins: hyphens inside a line of unchecked pages are breaks
    elif key in VOCAB:
        sep = "-"
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}-{b}")
    else:
        sep = ""
        UNDECIDED.append(f"{where}: {a}-{b} -> {a}{b}")
    return head[:-1] + sep + tail


def join_lines(lines, where):
    """Join printed lines into one line. An italic pair closed at a line end and opened
    again on the next line is joined (`*dedit ven-*` / `*tum*:` -> `*dedit ventum*:`,
    `*a*` / `*b*` -> `*a b*`)."""
    text = lines[0]
    for l in lines[1:]:
        if text.endswith("*") and l.startswith("*"):
            text, l = text[:-1], l[1:]
        if re.search(WORD + "-$", text):
            text = join_hyphen(text, l, where)
        elif (where, text.rsplit(" ", 1)[-1], l.split(" ", 1)[0]) in HYPHEN_MISSING:
            text += l
        else:
            text += " " + l
    return text


# ---------------------------------------------------------------- pages

def read_page(n, errors):
    """(head, lines): the running head or heading removed, the signature mark at the foot
    removed. head is (printed page number or None, the heading/running head or None)."""
    lines = text_of(n).rstrip("\n").split("\n")
    for i, l in enumerate(lines, 1):
        if len(re.findall(r"(?<!\d)\*", l)) % 2:
            errors.append(f"{n:04d}:{i}: italic mark not closed")
    number = None
    if re.fullmatch(r"\d+", lines[0]):
        number = int(lines[0])
        if number != n - OFFSET:
            errors.append(f"{n:04d}: page number {number}")
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    title = None
    if lines and re.fullmatch(r"[A-ZÀ-Ý' .,]+", lines[0].strip()) and len(lines[0]) > 4:
        title = lines.pop(0).strip()
        # an essay title printed on two lines (0303, 0324)
        while lines and re.fullmatch(r"[A-ZÀ-Ý' .,]+", lines[0].strip()) and len(lines[0]) > 4:
            title += " " + lines.pop(0).strip()
    # signature mark: a number alone at the foot, after a blank line
    if len(lines) >= 2 and re.fullmatch(r"\d+", lines[-1].strip()) and not lines[-2].strip():
        lines = lines[:-2]
    return number, title, lines


def split_verse(n, bs, errors):
    """The verse at the top of a page: (italian, latin, glosses, closing lines, rest). A
    closing line is printed under a column at the cantica's end (0868 `FINIT FELICITER
    PURGATORIUM.`)."""
    it, la, gl, ends = [], [], [], []
    k = 0
    for part in ("it", "la"):
        if k < len(bs) and NUMBER.match(bs[k][0]):
            b = bs[k]  # a gloss line may follow the verse without a blank line
            e = len(b)
            while e > 1 and GLOSS.match(b[e - 1]):
                e -= 1
            (it if part == "it" else la).extend(b[:e])
            gl.extend(b[e:])
            k += 1
        while k < len(bs) and (GLOSS.match(bs[k][0]) or len(bs[k]) == 1 and CLOSING.match(bs[k][0])):
            (gl if GLOSS.match(bs[k][0]) else ends).extend(bs[k])
            k += 1
    if bool(it) != bool(la):
        errors.append(f"{n:04d}: one verse column only")
    return it, la, gl, ends, bs[k:]


def tercets(lines, n, where):
    """Group verse lines into tercets: [(printed number or None, [lines])]. A line opened by
    `[` is the end of the line above, set on a line of its own (`[togle.`)."""
    out = []
    for l in lines:
        if l.startswith("[") and sum(bool(re.search(WORD, w)) for w in GLOSS.sub("", l).split()) <= 3 and not l.endswith("]") and out:
            out[-1][1][-1] = join_lines([out[-1][1][-1], l[1:]], f"{n:04d}")
            RUNOVER.append(f"{n:04d} {where}: {out[-1][1][-1][-40:]}")
            continue
        m = NUMBER.match(l)
        b = re.match(r"\[(\d+) ", l)  # a tercet in printed brackets (0545: `[7 Vidi`)
        if m:
            out.append((int(m.group(1).translate(SUP)), [l[m.end():]]))
        elif b:
            out.append((int(b.group(1)), ["[" + l[b.end():]]))
        elif out and len(out[-1][1]) < 3:
            out[-1][1].append(l)
        else:
            out.append((None, [l]))  # an unnumbered tercet (the print omits the number)
    return out


RUNOVER = []


def bare(l):
    """A line without its italic marks (`*` not after a digit), for its length and its end."""
    return re.sub(r"(?<!\d)\*", "", l)


def column_width(lines):
    """The length of a full line: the 90th percentile, not swayed by a long gloss line."""
    ls = sorted(len(bare(l)) for l in lines)
    return ls[int(len(ls) * 0.9)] if ls else 60


def paragraphs(lines, width):
    """Split a block of commentary lines into printed paragraphs: a line that ends a
    sentence and falls short of the column width ends its paragraph."""
    out, cur = [], []
    for l in lines:
        cur.append(l)
        if re.search(r"[.?!:]$", bare(l)) and len(bare(l)) < width - 8:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def add_paragraphs(parts, ps, n, carry):
    """Append paragraphs (lists of printed lines); a word hyphenated across the page break
    (carry: the index of the paragraph open at the end of the previous page) is joined on the
    earlier page."""
    for pi, p in enumerate(ps):
        if carry is not None and pi == 0:
            head = parts[carry]
            if re.search(WORD + r"-\*?$", head):
                m = re.match(r"(\S+)\s*(.*)", p[0])
                first = m.group(1)
                if head.endswith("*") and first.startswith("*"):  # an italic pair, as join_lines
                    head, first = head[:-1], first[1:]
                parts[carry] = join_hyphen(head, first, f"{n:04d}")
                p = [m.group(2)] + p[1:] if m.group(2) else p[1:]
                if not p:
                    continue
        parts.append(esc(join_lines(p, f"{n:04d}")))


def add_prose(parts, bs, n):
    """An essay or a one-column prose page: paragraphs on one line each, verse quoted line by
    line, printed lines joined into paragraphs."""
    width = column_width([l for b in bs for l in b])
    for b in bs:
        if width > 120 and any(len(bare(l)) > 80 for l in b):
            # paragraphs on one line each; a paragraph broken at a column change
            # (no sentence end) is joined
            cur = []
            for l in b:
                cur.append(l)
                if re.search(r"[.?!:;»)]$", bare(l)):
                    parts.append(esc(join_lines(cur, f"{n:04d}")))
                    cur = []
            if cur:
                parts.append(esc(join_lines(cur, f"{n:04d}")))
        elif len(b) > 1 and all(len(bare(l)) < width * 0.75 and not bare(l).endswith("-") for l in b):
            parts.append("\\\n".join(esc(l) for l in b))  # verse quoted in the essay
        else:  # printed lines
            parts.extend(esc(join_lines(p, f"{n:04d}")) for p in paragraphs(b, width))


def convert_prose(first, last, heading, errors):
    """A prose section of one column (the Purgatorio's preambula): the cantica's half-title,
    then pages with the heading on the first and as the running head on the others."""
    parts = []
    carry = None
    for n in range(first, last + 1):
        if text_of(n).strip() == "[Blank page]":
            continue
        number, title, lines = read_page(n, errors)
        parts.append(marker(n, number is not None))
        if title and not lines:  # the half-title
            parts.append("# " + title.capitalize())
            continue
        if title != heading:
            errors.append(f"{n:04d}: heading {title!r}")
        if number is None:
            parts.append("# " + heading.capitalize())
        bs = blocks(lines)
        body = [l for b in bs for l in b]
        width = column_width(body)
        for bi, b in enumerate(bs):
            add_paragraphs(parts, paragraphs(b, width), n, carry if bi == 0 else None)
        carry = len(parts) - 1 if body and re.search(WORD + "-$", bare(body[-1])) else None
    return parts


def convert_appendix(errors):
    """The fragments: a half-title, then two columns of commentary under the running head,
    with notes at the page foot (`(1) …`, as footnotes `[^PAGE-1]`)."""
    name, first, last, head = APPENDIX
    parts = []
    carry = None
    for n in range(first, last + 1):
        if text_of(n).strip() == "[Blank page]":
            continue
        number, title, lines = read_page(n, errors)
        parts.append(marker(n, number is not None))
        if n == first:  # the half-title: the title, then the author's lines
            parts.append("# " + APPENDIX_HEADINGS[title])
            parts.append("\\\n".join(l for l in lines if l.strip()))
            continue
        if title in APPENDIX_HEADINGS:
            parts.append("## " + APPENDIX_HEADINGS[title])
            bs = blocks(lines)
            while bs and len(bs[0]) == 1 and bs[0][0].isupper():  # the subtitle lines
                parts.append(bs.pop(0)[0])
        else:
            if title != head or number is None:
                errors.append(f"{n:04d}: running head {title!r}")
            bs = blocks(lines)
        notes = []
        while bs and FOOTNOTE.match(bs[-1][0]):
            notes.insert(0, bs.pop())
        body = [l for b in bs for l in b]
        width = column_width(body)
        for bi, b in enumerate(bs):
            if len(b) == 1 and b[0] in APPENDIX_HEADINGS:  # a canto's heading in the column
                parts.append("## " + APPENDIX_HEADINGS[b[0]])
                continue
            add_paragraphs(parts, paragraphs(b, width), n, carry if bi == 0 else None)
        carry = len(parts) - 1 if body and re.search(WORD + "-$", bare(body[-1])) else None
        for b in notes:
            k, note = FOOTNOTE.match(join_lines(b, f"{n:04d}")).groups()
            ref = [i for i, p in enumerate(parts) if f"({k})" in p and not p.startswith("<!--")]
            if not ref:
                errors.append(f"{n:04d}: note ({k}) without its mark")
                continue
            parts[ref[-1]] = parts[ref[-1]].replace(f"({k})", f"[^{n:04d}-{k}]", 1)
            parts.append(f"[^{n:04d}-{k}]: {esc(note)}")
    return name, parts


def convert_index(errors):
    """The printed table of contents: each entry on a line, as printed (dot leaders and page
    references kept), an entry printed on two or three lines joined."""
    name, first, last, head = INDEX
    parts = []
    for n in range(first, last + 1):
        number, title, lines = read_page(n, errors)
        parts.append(marker(n, number is not None))
        if title != head:
            errors.append(f"{n:04d}: heading {title!r}")
        if number is None:
            parts.append("# Index")
        for b in blocks(lines):
            entries, cur = [], []
            for l in b:
                cur.append(l)
                if re.search(r"(?:Pag\.|») *[0-9IVXLCivxlc]+$", l) or l.isupper():
                    entries.append(esc(join_lines(cur, f"{n:04d}")))
                    cur = []
            if cur:
                errors.append(f"{n:04d}: index entry without a page {cur!r}")
                entries.append(esc(join_lines(cur, f"{n:04d}")))
            parts.append("\\\n".join(entries))
    return name, parts


def roman(k):
    out = ""
    for v, s in ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"),
                 (4, "IV"), (1, "I")):
        while k >= v:
            out += s
            k -= v
    return out


def add_notes(parts, notes, n, errors):
    """Notes at the page foot (`(1) …`, possibly several in a block) as footnotes `[^PAGE-1]`,
    their marks in the page's text replaced."""
    items = []
    for b in notes:
        for l in b:
            if FOOTNOTE.match(l):
                items.append([l])
            else:
                items[-1].append(l)
    for item in items:
        k, note = FOOTNOTE.match(join_lines(item, f"{n:04d}")).groups()
        ref = [i for i, p in enumerate(parts) if f"({k})" in p and not p.startswith(("<!--", "[^"))]
        if not ref:
            errors.append(f"{n:04d}: note ({k}) without its mark")
            continue
        parts[ref[-1]] = parts[ref[-1]].replace(f"({k})", f"[^{n:04d}-{k}]", 1)
        parts.append(f"[^{n:04d}-{k}]: {esc(note)}")


def convert_front(scans, head, errors):
    """A section of the front matter: Roman page numbers, prose with footnotes, documents with
    their headings (`Doc. 1.`), title pages line by line."""
    parts = []
    carry = None
    for n in scans:
        lines = text_of(n).rstrip("\n").split("\n")
        number = lines.pop(0) if re.fullmatch(r"[IVXLC]+|\d+", lines[0]) else None
        if number and number not in (roman(n - ROMAN_OFFSET), str(n - OFFSET)):
            errors.append(f"{n:04d}: page number {number}")
        p = n - OFFSET if n >= 55 else roman(n - ROMAN_OFFSET)
        parts.append(f"<!-- p. {number or f'[{p}]'} ({n:04d}) -->")
        bs = blocks(lines)
        if n in TITLE_PAGES:
            if len(bs) == 1 and len(bs[0]) == 1:
                parts.append("# " + bs[0][0].capitalize())
            else:
                parts.extend("\\\n".join(esc(l) for l in b) for b in bs)
            carry = None
            continue
        title = bs[0][0] if bs and len(bs[0]) == 1 and bs[0][0].isupper() else None
        if title and head is None:  # a salutation (0013)
            parts.append(bs.pop(0)[0])
        elif title:
            bs.pop(0)
            if title != head:
                errors.append(f"{n:04d}: heading {title!r}")
            if number is None:
                parts.append("# " + " ".join(w.capitalize() for w in title.split()))
        elif number is not None:
            errors.append(f"{n:04d}: no running head")
        if not bs:  # a half-title
            continue
        # the notes at the page foot: from the first block opened by `(1)` (a note may
        # quote verse after a blank line, 0022)
        first_note = next((i for i, b in enumerate(bs) if i and FOOTNOTE.match(b[0])), len(bs))
        bs, notes = bs[:first_note], bs[first_note:]
        body = [l for b in bs for l in b]
        width = column_width(body)
        for bi, b in enumerate(bs):
            if re.fullmatch(r"Doc\. \d+\.", b[0]):  # a document's number, then its date
                parts.append("## " + b[0])
                if len(b) > 1:
                    parts.append("\\\n".join(esc(l) for l in b[1:]))
            elif len(b) > 1 and all(len(bare(l)) < width * 0.75 and not bare(l).endswith("-") for l in b):
                parts.append("\\\n".join(esc(l) for l in b))  # signatures, addresses
            else:
                add_paragraphs(parts, paragraphs(b, width), n, carry if bi == 0 else None)
        carry = len(parts) - 1 if body and re.search(WORD + "-$", bare(body[-1])) else None
        add_notes(parts, notes, n, errors)
    return parts


def convert_canto(cantica, c, errors):
    first, essay, last = CANTOS[cantica][c - 1]
    head = RUNNING_HEAD[cantica]
    parts = []
    verse = {"it": [], "la": []}  # (page, printed number, lines)
    carry = None  # the commentary paragraph open at the end of the previous page
    if c == 1 and cantica in HALF_TITLE:
        n = HALF_TITLE[cantica]
        number, title, lines = read_page(n, errors)
        if number is not None or lines:
            errors.append(f"{n:04d}: not a half-title")
        parts += [marker(n, False), "# " + title.capitalize()]
    for n in range(first, last + 1):
        text = text_of(n)
        if text.strip() == "[Blank page]":
            continue
        number, title, lines = read_page(n, errors)
        parts.append(marker(n, number is not None))
        if n == first and title == INCIPIT.get(cantica):
            parts.append("# " + " ".join(w.capitalize() for w in title.split()))
            while lines and not lines[0].strip():
                lines.pop(0)
            title = lines.pop(0).strip() if lines else None
        if title:
            if n == first:
                want = f"CAPITULI {GENITIVES[c - 1]} SUMMARIUM"
            elif n >= essay:
                want = title if title in ESSAYS or number else None
            elif number is None:
                want = f"CAPITULUM {ORDINALS[c - 1]}"
            else:
                want = title  # the running head (also on an essay's second page)
            if want != title:
                errors.append(f"{n:04d}: heading {title!r}")
            if n >= essay and title != head:
                parts.append(f"# {ESSAYS.get(title, title)}")
            elif number is None:
                parts.append("# " + " ".join(w.capitalize() for w in title.split()))
            elif title not in (head, f"CAPITULUM {ORDINALS[c - 1]}", MISPRINTED_HEAD.get(n)):
                errors.append(f"{n:04d}: running head {title!r}")
        bs = blocks(lines)
        if n >= essay:
            add_prose(parts, bs, n)
            continue
        it, la, gl, ends, rest = split_verse(n, bs, errors)
        if it:
            ti, tl = tercets(it, n, "it"), tercets(la, n, "la")
            if [len(t[1]) for t in ti] != [len(t[1]) for t in tl]:
                errors.append(f"{n:04d}: the columns differ: {[len(t[1]) for t in ti]}"
                              f" / {[len(t[1]) for t in tl]}")
            for (ni, li), (nl, ll) in zip(ti, tl):
                if ni is None and len(li) == 1 and len(ll) == 1 and verse["it"]:
                    # the canto's last line, set alone after the last tercet
                    if parts[-1].startswith("<!--"):
                        errors.append(f"{n:04d}: the last line on a page of its own")
                    verse["it"][-1][2].extend(li)
                    verse["la"][-1][2].extend(ll)
                    parts[-2] += "\\\n&emsp;" + esc(li[0])
                    parts[-1] += "\\\n&emsp;" + esc(ll[0])
                    continue
                k = len(verse["it"]) + 1
                verse["it"].append((n, ni, li))
                verse["la"].append((n, nl, ll))
                for lines_ in (li, ll):
                    parts.append(f"{k} " + "\\\n&emsp;".join(esc(l) for l in lines_))
            parts += [esc(l) for l in ends]
            if gl:
                parts.append(esc(join_lines(gl, f"{n:04d}")))
        body = [l for b in rest for l in b]
        width = column_width(body)
        for bi, b in enumerate(rest):
            if b[0] == "[figure]":  # its printed labels, one per line (1245, 1247)
                parts.append("\\\n".join(esc(l) for l in b))
            elif b[0].startswith(COLOPHON.get(n, "\0")):  # verse, kept line by line
                parts.append("\\\n".join(esc(l) for l in b))
            elif GLOSS.match(b[0]) and bi and rest[bi - 1][0].startswith(COLOPHON.get(n, "\0")):
                parts.append(esc(join_lines(b, f"{n:04d}")))
            else:
                add_paragraphs(parts, paragraphs(b, width), n, carry if bi == 0 else None)
        last_line = body[-1] if body else ""
        carry = len(parts) - 1 if body and re.search(WORD + "-$", bare(last_line)) else None
    # tercet numbers: computed by counting, checked against the printed ones
    for lang in ("it", "la"):
        lines = sum(len(t[2]) for t in verse[lang])
        if lines != VERSES[cantica][c - 1]:
            errors.append(f"{cantica} {c} {lang}: {lines} lines,"
                          f" expected {VERSES[cantica][c - 1]}")
        for k, (n, num, _) in enumerate(verse[lang], 1):
            if num is not None and num != k and MISNUMBERED.get((n, lang, k)) != num:
                errors.append(f"{n:04d} {lang}: printed number {num} at tercet {k}")
            if num is None:
                MISSING_NUMBER.append(f"{n:04d} {lang}: tercet {k}")
    return parts


MISSING_NUMBER = []


def main():
    DST.mkdir(parents=True, exist_ok=True)
    errors = []
    for cantica, cantos in CANTOS.items():
        for c in range(1, len(cantos) + 1):
            parts = convert_canto(cantica, c, errors)
            path = DST / f"{FIRST_FILE[cantica] + c - 1:03d}-{cantica}-canto-{c:02d}.md"
            path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    for name, first, last, heading in PROSE:
        parts = convert_prose(first, last, heading, errors)
        (DST / name).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    for name, scans, head in FRONT:
        parts = convert_front(scans, head, errors)
        (DST / name).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    for convert in (convert_appendix, convert_index):
        name, parts = convert(errors)
        (DST / name).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    for e in errors:
        print("ERROR", e)
    for x in MISSING_NUMBER:
        print("NO NUMBER", x)
    for x in RUNOVER:
        print("RUNOVER", x)
    for u in dict.fromkeys(UNDECIDED):
        print("HYPHEN", u)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
