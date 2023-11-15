import sys, math, re, unicodedata, Levenshtein

args = sys.argv[1:]

output_fn = ""
targets = []
while len(args) >= 2:
    if args[0] == "-o":
        output_fn = args[1]
        args = args[2:]
    elif args[0] == "-t":
        targets.append(args[1])
        args = args[2:]
    else:
        break

if not args:
    print(f"Usage: python {sys.argv[0]} [-o output] [-t target [-t ...]] file1 [file2 ...]")
    sys.exit(1)

texts = []
for arg in args:
    with open(arg, "r") as f:
        texts.append([l for line in f if (l := line.strip())])

def abbrev_name(name):
    if (m := re.match(r"[^-]+-(.*)\.[^.]+$", name)):
        name = m.group(1)
        if (m := re.match(r"([^-]+-.)", name)):
            name = m.group(1)
    return name

snames = [abbrev_name(arg) for arg in args]
snlen = max(len(arg) for arg in snames)
def spname(i):
    return f"{snames[i]:{snlen}}"

tlen = len(texts)
t0len = len(texts[0])
for i in range(1, tlen):
    if t0len != len(texts[i]):
        print("Error: files have different line lengths:", args[i])
        sys.exit(1)

def normalize(text):
    ret = ""
    for ch in text.lower():
        if ch != ch.upper():
            ret += ch
        elif ord(ch) < 128 and not ret.endswith(" "):
            ret += " "
    return ret.strip()

textsnorm = [[normalize(line) for line in text] for text in texts]

def dist(a, b):
    return Levenshtein.distance(a, b) / max(len(a), len(b))

print("# Mix")
print()
print("|", " | ".join([f"{i+1:{len(n)}}" for i, n in enumerate(snames)]), "|")
print("|", " | ".join(["-" * (len(n) - 1) + ":" for n in snames]), "|")
print("|", " | ".join(snames), "|")

sels  = [0 for _ in texts]
logs = []
for i in range(t0len):
    ds = []
    for j in range(tlen):
        tj = textsnorm[j][i]
        d = 0
        for k in range(tlen):
            if j == k:
                continue
            tk = textsnorm[k][i]
            d += dist(tj, tk) ** 2
        ds.append(math.sqrt(d / (tlen - 1)))
    mn = min(ds)
    ns = ""
    k = -1
    for j in range(len(texts)):
        if ds[j] - mn < 0.001:
            ns += str(j + 1)
            sels[j] += 1
            if k < 0:
                k = j
    logs.append((mn, ns, texts[k][i]))

mixed = [line for _, _, line in logs]
mlen = max(len(line) for line in mixed)
alen = max(len("Adopt"), tlen)
print()
print(f"| Line | Dist  | {'Adopt':{alen}} | {'Text':{mlen}} |")
print(f"| ---: | ----: | {'-' * alen} | {'-' * mlen} |")
for i, (mn, ns, line) in enumerate(logs):
    print(f"| {i+1:4} | {mn:.3f} | {ns:{alen}} | {line:{mlen}} |")

if output_fn:
    with open(output_fn, "w") as f:
        for line in mixed:
            print(line, file=f)

print()
print("## Ranking")
print()
print(f"| Rank | {'Name':{snlen}} | Adopt |")
print(f"| ---: | {'-' * snlen} | ----: |")
scores = list(enumerate(sels))
scores.sort(key=lambda x: x[1], reverse=True)
for r, (i, score) in enumerate(scores):
    print(f"| {r+1:4} | {spname(i)} | {score:5} |")

print()
print("# Distances")
print()

snames.append("MIX")
texts.append(mixed)
textsnorm.append([normalize(line) for line in mixed])
for target in targets:
    with open(target, "r") as f:
        lines = [l for line in f if (l := line.strip())]
        if t0len != len(lines):
            print(f"Error: `{target}` has different line length")
            sys.exit(1)
        snames.append(abbrev_name(target))
        texts.append(lines)
        textsnorm.append([normalize(line) for line in lines])

snlen = max(len(arg) for arg in snames)
tlen = len(texts)
spnames = []
for n in snames:
    length = max(5, len(n))
    spnames.append(f"{n:{length}}")
print("|", " " * snlen, "|", " | ".join(spnames[1:]), "|")
print("|", "-" * snlen, "|", " | ".join("-" * (len(spn) - 1) + ":" for spn in spnames[1:]), "|")
dists = [[0 for _ in range(tlen)] for _ in range(tlen)]
for i in range(tlen - 1):
    print("|", spname(i), end=" |")
    for j in range(1, tlen):
        sp = " " * (len(spnames[j]) + 1)
        if i < j:
            d = 0
            for k in range(t0len):
                d += dist(textsnorm[i][k], textsnorm[j][k]) ** 2
            d = math.sqrt(d / t0len)
            print(f"{d:{len(sp)}.3f}", end=" |")
            dists[i][j] = d
            dists[j][i] = d
        else:
            print(sp, end=" |")
    print()

for i in range(tlen):
    print()
    print("##", snames[i])
    print()
    print(f"| Rank | {'Name':{snlen}} | Dist  |")
    print(f"| ---: | {'-' * snlen} | ----: |")
    scores = [(j, d) for j, d in enumerate(dists[i]) if i != j]
    scores.sort(key=lambda x: x[1])
    for r, (j, score) in enumerate(scores):
        print(f"| {r+1:4} | {spname(j)} | {score:.3f} |")
