import sys

args = sys.argv[1:]

defstep = 3
steps = {}
while args:
    if args[0] == "-s" and len(args) >= 3:
        steps[int(args[1])] = int(args[2])
        args = args[3:]
    elif args[0] == "-d" and len(args) >= 2:
        defstep = int(args[1])
        args = args[2:]
    else:
        break

larg = len(args)
narg = larg // 2
if narg < 1 or larg % 2 != 0:
    print(f"Usage: python {sys.argv[0]} [-s line_number step] [-d default_step] name file [name file ...]")
    sys.exit(1)

names = []
texts = []
for i, arg in enumerate(args):
    if i % 2 == 0:
        names.append(arg)
    else:
        with open(arg, "r") as f:
            texts.append([l for line in f if (l := line.strip())])

all_same = True
t0len = len(texts[0])
for text in texts[1:]:
    if t0len != len(text):
        all_same = False
        break
if defstep == 1 and not all_same:
    print("Error: `-d 1` is not compatible with files of different lengths.")
    sys.exit(1)

print("<table>")
i = 1
lnx = 0
length = len(texts[0])
while i <= length:
    if i > 1 and all_same:
        print("<tr><td></td><td></td><td></td></tr>")
    step = steps[i] if i in steps else defstep
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
        if lnx < len(text):
            print(f'<tr><td>{names[j]}</td><td></td><td>')
            print(text[lnx])
            print("</td></tr>")
    i += step
    lnx += 1
print("</table>")
