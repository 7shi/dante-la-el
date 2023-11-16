import sys, os, pyperclip
from striplog import chop

args = sys.argv[1:]

if len(args) == 0:
    print("Usage: python {sys.argv[0]} file")
    sys.exit(1)

file = args[0]

while True:
    print("waiting...")
    t = chop(pyperclip.waitForNewPaste().replace("\r\n", "\n")).split("\n")
    ex = os.path.exists(file)
    with open(file, "ab") as f:
        output = "\n" if ex else ""
        output += "\n".join(t)
        f.write(output.encode("utf_8"))
