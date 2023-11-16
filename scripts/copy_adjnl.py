import pyperclip

while True:
    print("waiting...")
    t1 = pyperclip.waitForNewPaste()
    t2 = t1.replace("\r\n", "\n")
    lines = t2.split("\n")
    for i in range(len(lines) - 1):
        if lines[i] and not lines[i].endswith("  ") and lines[i + 1]:
            lines[i] += "  "
    if t1 == t2:
        print("LF")
        pyperclip.copy("\n".join(lines))
    else:
        print("CRLF")
        pyperclip.copy("\r\n".join(lines))
