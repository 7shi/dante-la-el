import sys

while (line := sys.stdin.readline()):
    sys.stdout.write(line
                    .replace("ä", "a")
                    .replace("ë", "e")
                    .replace("ï", "i")
                    .replace("ö", "o")
                    .replace("ü", "u"));
