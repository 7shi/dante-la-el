import sys, math, re, Levenshtein
from striplog import write_table

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
    if (m := re.match(r"(.*?)/(\w+)(.*)", name)):
        name = f"{m.group(2)}-{m.group(1)}{m.group(3)}"
    if (m := re.match(r"[^-]+-(.*)\.[^.]+$", name)):
        name = m.group(1)
        if (m := re.match(r"([^-]+-.)", name)):
            name = m.group(1)
    return name

anames = [abbrev_name(arg) for arg in args]

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

print("# MIX")
print()
write_table([anames, [], [i + 1 for i in range(len(anames))]],
            fit=True, right=list(range(len(anames))))
print()
sels  = [0 for _ in texts]
logs = []
dists1 = [0 for _ in range(tlen)]
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
        d /= tlen - 1
        dists1[j] += d
        ds.append(math.sqrt(d))
    mn = min(ds)
    ns = ""
    k = -1
    for j in range(len(texts)):
        if ds[j] - mn < 0.001:
            ns += str(j + 1)
            sels[j] += 1
            if k < 0:
                k = j
    logs.append([i + 1, f"{mn:.3f}", ns, texts[k][i]])
write_table([["Line", "Dist", "Adopt", "Text"], []] + logs,
            fit=True, right=[0, 1])

mixed = [log[3] for log in logs]
if output_fn:
    with open(output_fn, "w") as f:
        for line in mixed:
            print(line, file=f)

print()
print("## Number of Adopted")
print()
scores = list(enumerate(sels))
scores.sort(key=lambda x: x[1], reverse=True)
write_table([["Rank", "Name", "Adopt"], []] +
            [[r + 1, anames[i], score] for r, (i, score) in enumerate(scores)],
            fit=True, right=[0, 2])

print()
print("## Distance from Others")
print()
scores = list(enumerate([math.sqrt(d / t0len) for d in dists1]))
scores.sort(key=lambda x: x[1])
write_table([["Rank", "Name", "Dist"], []] +
            [[r + 1, anames[i], f"{score:.3f}"] for r, (i, score) in enumerate(scores)],
            fit=True, right=[0, 2])

print()
print("# Distances")
print()
anames.append("MIX")
texts.append(mixed)
textsnorm.append([normalize(line) for line in mixed])
for target in targets:
    with open(target, "r") as f:
        lines = [l for line in f if (l := line.strip())]
        if t0len != len(lines):
            print(f"Error: `{target}` has different line length")
            sys.exit(1)
        anames.append(abbrev_name(target))
        texts.append(lines)
        textsnorm.append([normalize(line) for line in lines])
tlen = len(texts)
dists2 = [[0] * tlen for _ in range(tlen)]
for i in range(tlen - 1):
    for j in range(1, tlen):
        if i < j:
            d = 0
            for k in range(t0len):
                d += dist(textsnorm[i][k], textsnorm[j][k]) ** 2
            d = math.sqrt(d / t0len)
            dists2[i][j] = d
            dists2[j][i] = d
write_table([[""] + anames[1:], []] +
            [[anames[i]] + [f"{dists2[i][j]:.3f}" if i < j else "" for j in range(1, tlen)]
                            for i in range(0, tlen - 1)],
            fit=True, right=list(range(1, tlen + 1)))

for i in range(tlen):
    print()
    print("##", anames[i])
    print()
    scores = [(j, d) for j, d in enumerate(dists2[i]) if i != j]
    scores.sort(key=lambda x: x[1])
    write_table([["Rank", "Name", "Dist"], []] +
                [[r + 1, anames[j], f"{d:.3f}"] for r, (j, d) in enumerate(scores)],
                fit=True, right=[0, 2])
