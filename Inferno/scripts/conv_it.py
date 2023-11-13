import os, sys, re
from striplog import *

args = sys.argv[1:]

mode = 1
if len(args) >= 2 and args[0] == "-m":
    mode = int(args[1])
    args = args[2:]

if len(args) != 3:
    print(f"Usage: python {sys.argv[0]} [-m mode] log-s it en-1")
    sys.exit(1)

sit = [line for line in readlines(args[1]) if line]
sen = [replace(line) for line in readlines(args[2]) if line]

data = parse(args[0])
nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}

# mode 1: extract English lines
# mode 2: make juxtaposition
for n in range(1, len(sit) + 1, 3):
    if n not in nums:
        print(f"[{n}] no table", file=sys.stderr)
        continue
    title = nums[n]
    tables = data[title]
    if tables and len(tables) == 2 and len(tables[1][0]) == 3:
        if mode == 1:
            for i, rows in enumerate(tables[1][2:]):
                it = sit[n + i - 1]
                en = rows[2]
                last = it[-1]
                if not isletter(last) and isletter(en[-1]):
                    en += last
                    print(f'[{n+i}] add "{last}": {en}', file=sys.stderr)
                itlt = isletter(it[0])
                enlt = isletter(en[0])
                if itlt != enlt:
                    print(f'{n+i} it="{it[0]}", en="{en[0]}"', file=sys.stderr)
                if en[:2] != "I " and enlt and (itlw := islower(it[0])) != islower(en[0]):
                    e1 = en[0]
                    en = (e1.lower() if itlw else e1.upper()) + en[1:]
                    print(f'[{n+i}] case change: {e1} -> {en}', file=sys.stderr)
                print(en)
        elif mode == 2:
            words = tables[0][2:]
            if not words:
                print(f"[{n}] no words", file=sys.stderr)
            for i in range(n, min(n + 3, len(sit) + 1)):
                if i > 1:
                    print()
                it = sit[i - 1]
                print(f"{i} {it}  ")
                print(f"{i} {sen[i-1]}")
                print()
                print("<table><tr><td>Lemma:<br>Italian:<br>English:</td>")
                while words:
                    w = words[0][0]
                    if (p := it.find(w)) < 0:
                        break
                    wit, lemma, wen = words.pop(0)
                    if isletter(wit):
                        print(f"<td>{lemma}<br>{wit}<br>{wen}</td>")
                        it = it[p + len(w):]
                    else:
                        print(f"{i} not letter: {wit}", file=sys.stderr)
                print("</tr></table>")
            if words:
                print(f"[{n}] left:", *[w[0] for w in words], file=sys.stderr)
    else:
        print(f"[{title}] no tables", file=sys.stderr)
