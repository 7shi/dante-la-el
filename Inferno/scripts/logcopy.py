import sys, os, re, pyperclip

args = sys.argv[1:]
i = 1
step = 3
seek = True
threshold = 1

while len(args) >= 2:
    if args[0] == "-s": # Start
        i = int(args[1])
        seek = False
        args = args[2:]
    elif args[0] == "-t": # sTep
        step = int(args[1])
        args = args[2:]
    elif args[0] == "-h": # each 2 times
        threshold = int(args[1])
        args = args[2:]
    else:
        break

if len(args) != 1:
    print(f"Usage: python {sys.argv[0]} [-s start] [-t step] [-h threshold] file")
    sys.exit(1)

if seek and os.path.exists(args[0]):
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

thr = 0
def writeline(f, showThr=False):
    if step == 1:
        s = f"## {i}"
    else:
        s = f"## {i}-{i+step-1}"
    if showThr and threshold > 1:
        s += f" ({thr+1}/{threshold})"
    print(s, file=f)

file = args[0]
while True:
    writeline(sys.stderr, True)
    p = chop(pyperclip.waitForNewPaste().replace("\r\n", "\n")).split("\n")
    print("log?")
    t = chop(pyperclip.waitForNewPaste().replace("\r\n", "\n")).split("\n")
    ex = os.path.exists(file)
    with open(file, "a", encoding="utf_8") as f:
        if thr == 0:
            if ex:
                print(file=f)
            writeline(f)
        print(file=f)
        for line in p:
            print("    " + line, file=f)
        print(file=f)
        for line in t:
            print(line, file=f)
    thr += 1
    if thr == threshold:
        i += step
        thr = 0
