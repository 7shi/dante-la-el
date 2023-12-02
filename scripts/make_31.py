import sys

args = sys.argv[1:]

type = 1
if len(args) >= 2 and args[0] == "-t":
    type = int(args[1])
    args = args[2:]

if len(args) != 2:
    print(f"Usage: python {sys.argv[0]} [-t type] A B")
    sys.exit(1)

texts = []
for arg in args:
    with open(arg, "r") as f:
        texts.append([ln for line in f if (ln := line.strip())])

i = 0
while i < len(texts[0]):
    if i:
        print()
    if type == 1:
        print(texts[0][i])
        s = i * 3
        e = min(s + 3, len(texts[1]))
        for j in range(s, e):
            print(texts[1][j])
        i += 1
    else:
        print("[A]")
        e = min(i + 3, len(texts[0]))
        for j in range(i, e):
            print(texts[0][j])
        print("[B]")
        print(texts[1][i // 3])
        i += 3
