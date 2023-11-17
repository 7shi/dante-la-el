import sys

args = sys.argv[1:]

trema = False
if args and args[0] == '-t':
    trema = True
    args = args[1:]

if args:
    print(f"Usage: python3 {sys.argv[0]} [-t]", file=sys.stderr)
    sys.exit()

n = 1
while (line := sys.stdin.readline()):
    line = line.strip()
    if line:
        if trema:
            line = line.replace('ä', 'a').replace('ë', 'e').replace('ï', 'i').replace('ö', 'o').replace('ü', 'u')
        print(n, line)
        if n % 3 == 0:
            print()
        n = n + 1
