import sys, re

from striplog import *

args = sys.argv[1:]
num = False
col = 1
while args:
    if args[0] == "-n":
        num = True
        args = args[1:]
    if args[0] == "-c" and len(args) >= 2:
        col = int(args[1])
        args = args[2:]
    else:
        break

if not args:
    print(f"Usage: python {sys.argv[0]} [-c column] [-n] md", file=sys.stderr)
    sys.exit(1)

data = {}
for arg in args:
    parse(arg, data)
nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}
for n in nums.keys():
    k = nums[n]
    for table in data[k]:
        for row in table[2:]:
            if re.match("\d+$", row[0]):
                if num:
                    print(row[0], row[col])
                else:
                    print(row[col])
