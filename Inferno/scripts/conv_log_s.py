import os, sys, re
from striplog import *

args = sys.argv[1:]

first = 1
step = 1
col = 2
cja = -1
while len(args) >= 2:
    if args[0] == "-s":
        step = int(args[1])
        args = args[2:]
    elif args[0] == "-c":
        col = int(args[1])
        args = args[2:]
    elif args[0] == "-f":
        first = int(args[1])
        args = args[2:]
    elif args[0] == "-j":
        cja = int(args[1])
        args = args[2:]
    else:
        break

if not (1 <= len(args) <= 2):
    print(f"Usage: python {sys.argv[0]} [-s step] [-c column] [-f first] [-j column] log-s [src]")
    sys.exit(1)

data = parse(args.pop(0))
nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}
if args:
    src = [replace(line) for line in readlines(args[0]) if line]
else:
    src = None

# The first header should be modified manually.
min_key = nums[min(nums.keys())]
names = [h + ":" for h in data[min_key][0][0]]
if first:
    names[0], names[first] = names[first], names[0]

def fix(s, t):
    last = s[-1]
    if not isletter(last) and isletter(t[-1]):
        t += last
        print(f'[{n+i}] add "{last}": {t}', file=sys.stderr)
    itlt = isletter(s[0])
    enlt = isletter(t[0])
    if itlt != enlt:
        print(f'{n+i} it="{s[0]}", en="{t[0]}"', file=sys.stderr)
    if t[:2] != "I " and enlt and (itlw := islower(s[0])) != islower(t[0]):
        e1 = t[0]
        t = (e1.lower() if itlw else e1.upper()) + t[1:]
        print(f'[{n+i}] case change: {e1} -> {t}', file=sys.stderr)
    return t

def strip_word2(w, col):
    if col + 1 != cja:
        w = strip_word(w)
    w = re.sub(r"[(（].*[）)]", "", w)
    return re.sub(r"[,、].*", "", w).strip()

# step 1: extract English lines (The correction should be completed here.)
# step 2: make juxtaposition
for n in range(1, max(nums) + 1, 3):
    if n not in nums:
        print(f"[{n}] no table", file=sys.stderr)
        continue
    title = nums[n]
    tables = data[title]
    if tables and len(tables) == 2 and len(tables[1][0]) >= 3:
        table = tables[1][2:]
        if step == 1:
            for i, items in enumerate(table):
                if col == cja:
                    print(items[col])
                else:
                    print(fix(items[1], items[col]))
        elif step == 2:
            words = tables[0][2:]
            if not words:
                print(f"[{n}] no words", file=sys.stderr)
            for i, items in enumerate(table):
                ln = n + i
                if ln > 1:
                    print()
                for j in range(1, len(items)):
                    t = src[ln - 1] if src and j == col else items[j]
                    spc = "  " if j < len(items) - 1 else ""
                    print(f"{ln} {t}{spc}")
                s = items[1]
                print()
                print("<table><tr><td><b>", "<br>".join(names), "</b></td>", sep="")
                while words:
                    ws = [strip_word2(w, iw) for iw, w in enumerate(words[0])]
                    if w := ws[0]:
                        if (p := s.find(w)) < 0:
                            break
                        s = s[p + len(w):]
                        if first:
                            ws[0], ws[first] = ws[first], w
                        print("<td>", "<br>".join(ws), "</td>", sep="")
                    else:
                        # print(f"{ln} no letter: {ws}", file=sys.stderr)
                        pass
                    words.pop(0)
                print("</tr></table>")
            if words:
                print(f"[{n}] left:", *[w[0] for w in words], file=sys.stderr)
    else:
        print(f"[{title}] no tables", file=sys.stderr)
