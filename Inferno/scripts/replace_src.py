import sys, re
from striplog import *

args = sys.argv[1:]

if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} it")
    sys.exit(1)

it = [line for line in readlines(args[0]) if line]

while (line := sys.stdin.readline()):
    line = chop(line)
    if m := re.match(r"\|\ *(\d+)\ *\|.*?\|(.*?)\|", line):
        ln = int(m.group(1))
        en = m.group(2).strip()
        print(f"| {ln} | {it[ln-1]} | {en} |")
    else:
        print(line)
