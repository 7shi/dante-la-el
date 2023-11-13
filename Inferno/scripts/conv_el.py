import sys, re

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} md it")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    md = [line.strip() for line in f]

with open(sys.argv[2], "r") as f:
    it = [l for line in f if (l := line.strip())]

i = 0
def read_table():
    global i
    ret = []
    while i < len(md):
        line = md[i]
        i += 1
        if not "|" in line:
            i -= 1
            break
        rows = [c.strip() for c in line.split("|")]
        if line[0] == "|":
            rows = rows[1:-1]
        ret.append(rows)
    if len(ret) < 3 or len(ret[1]) == 0 or len(ret[1][0]) < 2 or not ret[1][0].startswith("--"):
        print(f"{i}: table error", file=sys.stderr)
        print(ret, file=sys.stderr)
        sys.exit(1)
    return ret

n = 0
words = []
lines = []
while i < len(md):
    line = md[i]
    i += 1
    if m := re.match(r"## (\d+)", line):
        if n and not lines:
            print(f"{i}: [{n}] no lines", file=sys.stderr)
        n = int(m.group(1))
        words = []
        lines = []
    elif line.startswith("|") or (t2 := "-|-" in line.replace(" ", "")):
        i -= 2 if t2 else 1
        # bak = i + 1
        if not words:
            words = read_table()
            # print(bak, n, words)
        elif not lines:
            lines = read_table()
            # print(bak, n, lines)
            w = 2
            nn = n
            for ln in range(2, len(lines)):
                if n > 1:
                    print()
                it1 = it[n - 1].replace("’", "'")
                it2 = lines[ln][0].replace("’", "'")
                print(f"{n} {it1}  ")
                if it1[:len(it2)] != it2:
                    print(f"{n} {it1} != {it2}", file=sys.stderr)
                    # pass
                length = len(lines[ln])
                for j in range(1, length):
                    t = lines[ln][j]
                    if j < length - 1:
                        t += "  "
                    print(f"{n} {t}")
                tds = []
                wd = ""
                while w < len(words):
                    wd = words[w][0].replace("’", "'")
                    p = it1.find(wd)
                    if p < 0:
                        break
                    tds.append("<td>" + "<br>".join(words[w]) + "</td>")
                    it1 = it1[p + len(wd):]
                    w += 1
                if not tds:
                    if wd:
                        wd = ": " + wd
                    print(f"{n} no match" + wd, "|", it1, file=sys.stderr)
                else:
                    print()
                    print("<table><tr><td><b>Italian:<br>English:<br>Modern Greek:</td>")
                    for td in tds:
                        print(td)
                    print("</tr></table>")
                n += 1
            if w < len(words):
                print(f"[{nn}]remain:", words[w:], file=sys.stderr)
