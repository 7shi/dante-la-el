import sys

while (line := sys.stdin.readline()):
    sys.stdout.write(line
                    .replace("Cx", "Ĉ")
                    .replace("cx", "ĉ")
                    .replace("Gx", "Ĝ")
                    .replace("gx", "ĝ")
                    .replace("Hx", "Ĥ")
                    .replace("hx", "ĥ")
                    .replace("Jx", "Ĵ")
                    .replace("jx", "ĵ")
                    .replace("Sx", "Ŝ")
                    .replace("sx", "ŝ")
                    .replace("Ux", "Ŭ")
                    .replace("ux", "ŭ"));
