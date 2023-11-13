import sys, os, re

from striplog import chop

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "greektrans"))
import greektrans

args = sys.argv[1:]
if args:
    print(f"Usage: python {sys.argv[0]}")
    sys.exit(1)

line = sys.stdin.readline()
while line:
    line = chop(line)
    if m := re.match(r"(\d+ )(.*)", line):
        print(line)
        t = greektrans.romanize(m.group(2))
        print(f"{m.group(1)}{t}")
        while (line := sys.stdin.readline()) and re.match(r"\d+ ", line):
            print(chop(line))
    elif m := re.match(r"<table><tr><td>(.*)</td>", line):
        items = m.group(1).split("<br>")
        items.insert(2, "Transliteration:")
        print("<table><tr><td>", "<br>".join(items), "</td>", sep="")
        while (line := sys.stdin.readline()) and (m := re.match(r"<td>(.*)</td>", line)):
            items = m.group(1).split("<br>")
            items.insert(2, greektrans.romanize(items[1]))
            print("<td>", "<br>".join(items), "</td>", sep="")
    else:
        print(line)
        line = sys.stdin.readline()
