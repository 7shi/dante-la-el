import sys

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} A B")
    sys.exit(1)

texts = []
for arg in sys.argv[1:]:
    with open(arg, "r") as f:
        texts.append([ln for line in f if (ln := line.strip())])

for i in range(0, len(texts[0]), 3):
    print()
    e = min(i + 3, len(texts[0]))
    # if i + 1 == e:
    #     print(f"# {e}")
    # else:
    #     print(f"# {i+1}-{e}")
    print("[A]")
    for j in range(i, e):
        print(texts[0][j])
    print("[B]")
    print(texts[1][i // 3])
