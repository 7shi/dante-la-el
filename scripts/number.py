import sys

if len(sys.argv) < 2:
    print('Usage: python3 number.py FILE', FILE=sys.stderr)
    sys.exit()

with open(sys.argv[1]) as f:
    n = 1
    for line in f:
        line = line.strip()
        if line:
            print(n, line)
            if n % 3 == 0:
                print()
            n = n + 1
