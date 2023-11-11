import sys, re

start = 0
step = 3

args = sys.argv[1:]
if len(args) >= 2 and args[0] == "-s":
    start = int(args[1])
    args = args[2:]

if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} [-s start] file", file=sys.stderr)
    sys.exit(1)

def chop(s):
    if s and s[-1] == "\n":
        s = s[:-1]
        if s and s[-1] == "\r":
            s = s[:-1]
    return s

with open(args[0], "r") as f:
    for line in f:
        line = chop(line)
        if m := re.match(r"## (\d+)-(\d+)", line):
            i = int(m.group(1))
            j = int(m.group(2))
            if i >= start:
                i += step
                j += step
            print(f"## {i}-{j}")
        elif m := re.match(r"## (\d+)", line):
            i = int(m.group(1))
            if i >= start:
                i += step
            print(f"## {i}")
        else:
            print(line)
