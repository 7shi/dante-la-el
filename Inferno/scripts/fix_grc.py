import sys, re
from striplog import chop

args = sys.argv[1:]

if len(args) != 0:
    print(f"Usage: python {sys.argv[0]}")
    sys.exit(1)

while (line := sys.stdin.readline()):
    line = chop(line)
    if m := re.match(r'\| (\d+) \| („ .*?) \| "?([^„].*?) \|$', line):
        n, g, e = m.group(1, 2, 3)
        print(f"| {n} | {g} | „ {e} |")
    else:
        print(line)
