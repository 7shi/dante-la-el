import sys, re

from striplog import *

args = sys.argv[1:]

if not args:
    print(f"Usage: python {sys.argv[0]} md", file=sys.stderr)
    sys.exit(1)

data = {}
for arg in args:
    parse(arg, data)
nums = {int(m.group(1)): k for k in data.keys() if (m := re.match("(\d+)", k))}
for i, n in enumerate(nums.keys()):
    k = nums[n]
    for table in data[k]:
        for row in table[2:]:
            if re.match("\d+$", row[0]):
                print(row[0], row[2])
