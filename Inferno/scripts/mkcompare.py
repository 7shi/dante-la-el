import sys

type = 0
args = sys.argv[1:]
if len(args) > 0 and args[0] == "-1":
    type = 1
    args = args[1:]

larg = len(args)
narg = larg // 2
if narg < 1 or larg % 2 != 0:
    print(f"Usage: python {sys.argv[0]} [-1] name file [name file ...]")
    sys.exit(1)

names = []
texts = []
for i, arg in enumerate(args):
    if i % 2 == 0:
        names.append(arg)
    else:
        with open(arg, "r") as f:
            texts.append([l for line in f if (l := line.strip())])

print("<table>")
i = 1
ln3 = 0
length = len(texts[0])
while i <= length:
    step = 3 if type == 0 else (4 if i == 37 else 2 if i == 44 else 3)
    for j, text in enumerate(texts):
        if len(text) != length:
            continue
        e = min(i + step, length + 1)
        lns = "<br>".join(str(ln) for ln in range(i, e))
        print(f'<tr><td>{names[j]}</td><td align="right">{lns}</td><td>')
        for ln in range(i, e):
            t = text[ln - 1]
            if ln < e - 1:
                t += "<br>"
            print(t)
        print("</td></tr>")
    for j, text in enumerate(texts):
        if len(text) == length:
            continue
        if ln3 < len(text):
            print(f'<tr><td>{names[j]}</td><td></td><td>')
            print(text[ln3])
            print("</td></tr>")
    i += step
    ln3 += 1
print("</table>")
