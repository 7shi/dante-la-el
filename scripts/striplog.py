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

def write_table(table, fit=False, right=[], file=sys.stdout):
    widths = []
    cols = len(table[0])
    if fit:
        widths = [max(3, *[len(str(row[i])) for j, row in enumerate(table) if j != 1])
                  for i in range(cols)]
    for row, items in enumerate(table):
        if row == 1:
            seps = []
            for col in range(cols):
                if fit:
                    if col in right:
                        seps.append("-" * (widths[col] + 1) + ":")
                    else:
                        seps.append("-" * (widths[col] + 2))
                else:
                    seps.append(items[col] + ":" if col in right else items[col])
            print("|", "|".join(seps), "|", sep="", file=file)
        else:
            items2 = []
            for col in range(cols):
                if fit:
                    if col in right:
                        items2.append(str(items[col]).rjust(widths[col]))
                    else:
                        items2.append(str(items[col]).ljust(widths[col]))
                else:
                    items2.append(str(items[col]))
            print("|", " | ".join(items2), "|", file=file)

def parse(file, ret=None):
    if ret is None:
        ret = {}
    with open(file, "r") as f:
        log = [line.rstrip() for line in f]
    i = 0
    n = ""
    tables = []
    while i < len(log):
        line = log[i]
        i += 1
        if line.startswith("##"):
            if tables:
                if n not in ret:
                    ret[n] = []
                ret[n] += tables
            n = line[2:].strip()
            tables = []
        elif line.startswith("|") or (not line.startswith(" ") and (t2 := re.search(r"-:? *\| *:?-", line))):
            i -= 2 if t2 else 1
            try:
                table, i = read_table(log, i)
            except:
                print(f"{i}: {line}", file=sys.stderr)
                raise
            tables.append(table)
    if tables:
        if n not in ret:
            ret[n] = []
        ret[n] += tables
    return ret

def write_tables(data, keys, *checks):
    first = True
    for k in keys:
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
            if checks:
                ok = False
                for chk in checks:
                    if chk == len(tables):
                        ok = True
                        break
                if not ok:
                    print(f"[{k}] {len(tables)} table(s)", file=sys.stderr)
        else:
            print(f"[{k}] no tables", file=sys.stderr)

if __name__ == "__main__":
    args = sys.argv[1:]

    check = 2
    while len(args) >= 2:
        if args[0] == "-c":
            check = int(args[1])
            args = args[2:]
        else:
            break

    if len(args) == 0:
        print(f"Usage: python {sys.argv[0]} [-c check] log1 [log2 ...]", file=sys.stderr)
        sys.exit(1)

    data = {}
    for arg in args:
        parse(arg, data)
    nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}
    write_tables(data, [nums[n] for n in sorted(nums.keys())], check)
