import sys, re, pyperclip

args = sys.argv[1:]
i = 1
step = 3
seek = True

while len(args) >= 2:
    if args[0] == "-s": # 開始行を指定
        i = int(args[1])
        seek = False
        args = args[2:]
    elif args[0] == "-t": # stepを指定
        step = int(args[1])
        args = args[2:]
    else:
        break

if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} [-s start] [-t step] file")
    sys.exit(1)

if seek:
    with open(args[0], "r", encoding="utf_8") as f:
        for line in f:
            if m := re.match(r"## (\d+)", line):
                i = int(m.group(1)) + step

def chop(s):
    if s and s[-1] == "\n":
        s = s[:-1]
        if s and s[-1] == "\r":
            s = s[:-1]
    return s

file = args[0]
while True:
    print(f"## {i}-{i+2}", file=sys.stderr)
    p = chop(pyperclip.waitForNewPaste().replace("\r\n", "\n")).split("\n")
    print("log?")
    t = chop(pyperclip.waitForNewPaste().replace("\r\n", "\n")).split("\n")
    # fileに追記
    with open(file, "a", encoding="utf_8") as f:
        print(file=f)
        print(f"## {i}-{i+2}", file=f)
        print(file=f)
        for line in p:
            print("    " + line, file=f)
        print(file=f)
        for line in t:
            print(line, file=f)
    i += step
