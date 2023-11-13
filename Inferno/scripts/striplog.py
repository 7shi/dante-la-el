import sys, re

def chop(s):
    if s and s[-1] == "\n":
        s = s[:-1]
        if s and s[-1] == "\r":
            s = s[:-1]
    return s

def readlines(file):
    with open(file, "r") as f:
        return [chop(line) for line in f]

def replace(s):
    return s.replace("’", "'").replace("”", '"').replace("“", '"')

def isletter(s):
    return s.upper() != s.lower()

def islower(s):
    return isletter(s) and s.lower() == s

def strip_word(s):
    excepts = "'’)"
    while s and not (isletter(ch := s[0]) or ch in excepts):
        s = s[1:]
    while s and not (isletter(ch := s[-1]) or ch in excepts):
        s = s[:-1]
    return s

def read_table(lines, i):
    ret = []
    type = lines[i][0] == "|"
    while i < len(lines):
        line = lines[i]
        if not line or (type and line[0] != "|") or (not type and not "|" in line):
            break
        i += 1
        items = [c.strip() for c in line.split("|")]
        if line[0] == "|":
            if not items[0]:
                items.pop(0)
            if not items[-1]:
                items.pop()
        if len(ret) == 1:
            items = ["---"] * len(items)
        ret.append(items)
    if len(ret) < 3 or len(ret[1]) == 0 or len(ret[1][0]) < 2 or not ret[1][0].startswith("--"):
        print(f"{i}: table error", file=sys.stderr)
        print(ret, file=sys.stderr)
        sys.exit(1)
    return ret, i

def write_table(table):
    for items in table:
        print("|", " | ".join(items), "|")

def parse(file):
    ret = {}
    with open(file, "r") as f:
        log = [line.strip() for line in f]
    i = 0
    n = ""
    tables = []
    while i < len(log):
        line = log[i]
        i += 1
        if line.startswith("##"):
            if tables:
                ret[n] = tables
            n = line[2:].strip()
            tables = []
        elif line.startswith("|") or (t2 := "-|-" in line.replace(" ", "")):
            i -= 2 if t2 else 1
            table, i = read_table(log, i)
            tables.append(table)
    if tables:
        ret[n] = tables
    return ret

if __name__ == "__main__":
    args = sys.argv[1:]
    last = False
    if args and args[0] == "-l":
        last = True
        args = args[1:]

    if len(args) != 1:
        print(f"Usage: python {sys.argv[0]} [-l] log")
        sys.exit(1)

    data = parse(args[0])
    nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}
    first = True
    for n in sorted(nums.keys()):
        k = nums[n]
        tables = data[k]
        if tables:
            if first:
                first = False
            else:
                print()
            print(f"## {k}")
            for t in tables:
                print()
                write_table(t)
            if len(tables) != 2:
                print(f"[{k}] {len(tables)} tables", file=sys.stderr)
        else:
            print(f"[{k}] no tables", file=sys.stderr)
