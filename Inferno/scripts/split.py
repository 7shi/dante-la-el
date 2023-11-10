import sys, re

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} md out1 [out2 ...]", file=sys.stderr)
    sys.exit(1)

def chop(s):
    if s and s[-1] == "\n":
        s = s[:-1]
        if s and s[-1] == "\r":
            s = s[:-1]
    return s

texts = []
lines = []

with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.strip()
        if m := re.match(r"\d+ (.*)", line):
            lines.append(m.group(1))
        elif lines:
            texts.append(lines)
            lines = []

outs = sys.argv[2:]
for i in range(len(outs)):
    with open(outs[i], "w") as f:
        for j, ts in enumerate(texts):
            if j and j % 3 == 0:
                print(file=f)
            if i + 1 < len(ts):
                print(ts[i + 1], file=f)
