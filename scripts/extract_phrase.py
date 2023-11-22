import sys, re

from striplog import *

args = sys.argv[1:]

if len(args) < 2:
    print(f"Usage: python {sys.argv[0]} md src", file=sys.stderr)
    sys.exit(1)

data = {}
for arg in args:
    parse(arg, data)
nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}

lines = [l for line in readlines(args[1]) if (l := line.strip())]

print("| Line | Italian | English | Japanrse |")
print("|-----:|---------|---------|----------|")
for n in nums.keys():
    k = nums[n]
    e = n
    if m := re.match("\d+-(\d+)", k):
        e = int(m.group(1))
    table = data[k][0]
    rows = table[2:]
    src = lines[n - 1]
    output = True
    while rows:
        row = rows.pop(0)
        if not src and n < e:
            src = lines[n]
            n += 1
            output = True
        t = row[0]
        if (p := src.find(t)) >= 0:
            t = src[:p + len(t)]
            src = src[p + len(t):].strip()
        else:
            print(f"Error [{n}]: {t} | {src}", file=sys.stderr)
            src = ""
            break
        if output:
            print(f"| {n} | {t} | {row[1]} | {row[2]} |")
            output = False
        else:
            nsp = " " * len(str(n))
            print(f"| {nsp} | {t} | {row[1]} | {row[2]} |")
    if src:
        print(f"Left [{n}]: {src}", file=sys.stderr)
