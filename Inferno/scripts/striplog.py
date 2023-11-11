import sys, re

def read_table(lines, i):
    ret = []
    type = lines[i][0] == "|"
    while i < len(lines):
        line = lines[i]
        if not line or (type and line[0] != "|") or (not type and not "|" in line):
            break
        i += 1
        rows = [c.strip() for c in line.split("|")]
        if line[0] == "|":
            rows = rows[1:-1]
        ret.append(rows)
    if len(ret) < 3 or len(ret[1]) == 0 or len(ret[1][0]) < 2 or not ret[1][0].startswith("--"):
        print(f"{i}: table error", file=sys.stderr)
        print(ret, file=sys.stderr)
        sys.exit(1)
    return ret, i

def write_table(table):
    for rows in table:
        print("|", " | ".join(rows), "|")

if __name__ == "__main__":
    args = sys.argv[1:]
    last = False
    if args and args[0] == "-l":
        last = True
        args = args[1:]

    if len(args) != 1:
        print(f"Usage: python {sys.argv[0]} [-l] log")
        sys.exit(1)

    with open(args[0], "r") as f:
        log = [line.strip() for line in f]

    i = 0
    n = 0
    tables = []
    while i < len(log):
        line = log[i]
        i += 1
        if line.startswith("##"):
            if n:
                if tables:
                    for table in tables[-1:] if last else tables:
                        print()
                        write_table(table)
                else:
                    print(f"{i}: [{n}] no tables", file=sys.stderr)
            if m := re.match(r"## (\d+)", line):
                n = int(m.group(1))
                if tables:
                    print()
                print(f"## {n}")
            else:
                n = 0
            words = []
            lines = []
        elif line.startswith("|") or (t2 := "-|-" in line.replace(" ", "")):
            i -= 2 if t2 else 1
            # bak = i + 1
            table, i = read_table(log, i)
            if n:
                tables.append(table)
