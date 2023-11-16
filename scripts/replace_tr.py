import sys, re
from striplog import *

args = sys.argv[1:]

col = 1
if len(args) >= 2 and args[0] == "-c":
    col = int(args[1])
    args = args[2:]

if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} [-c column] src")
    sys.exit(1)

src = [line for line in readlines(args[0]) if line]

while (line := sys.stdin.readline()):
    line = chop(line)
    if re.match(r"\| *\d+ *\|", line):
        items = line.split("|")
        if items[0] or items[-1]:
            print(f"Invalid line: {line}", file=sys.stderr)
            continue
        items = items[1:-1]
        items[col] = " " + src[int(items[0]) - 1] + " "
        print("|", "|".join(items), "|", sep="")
    else:
        print(line)
