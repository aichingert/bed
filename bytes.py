import sys

if len(sys.argv) <= 1:
    sys.exit(0)

f = open("gbyl")
source = f.read() ; f.close()

pos = 0
ans = 0
needle = sys.argv[1]

while pos + len(needle) < len(source):
    found = True 

    for i in range(len(needle)):
        if source[pos + i] != needle[i]:
            found = False
            break
    if not found:
        pos += 1
        continue

    pos += len(needle)
    while pos < len(source) and source[pos] == ' ':
        pos += 1

    if pos >= len(source) or source[pos] != '(':
        pos += 1
        continue

    while pos < len(source) and source[pos] != '{':
        pos += 1
    pos += 1
    brcs = 1
    wri = "write_"
    while pos + len(wri) < len(source) and brcs > 0:
        if source[pos] == '{':
            brcs += 1
        elif source[pos] == '}':
            brcs -= 1

        wrf = True
        for i in range(len(wri)):
            if source[pos + i] != wri[i]:
                wrf = False
                break

        if not wrf:
            pos += 1
            continue

        pos += len(wri)
        if source[pos] == "z":
            print("zero", source[pos:])
            sys.exit(1)
            while pos < len(source) and source[pos] != ' ':
                pos += 1
            pos += 1
            while pos < len(source) and source[pos].isdigit():
                pos += 1
                ans += 1
            pos += 1
        elif pos + 1 < len(source):
            if source[pos + 1] == '8' or source[pos + 1] == 'i':
                ans += 1
            elif source[pos + 1] == '1':
                ans += 2
            elif source[pos + 1] == '3':
                ans += 4
            elif source[pos + 1] == '6':
                ans += 8
        pos += 1

print(ans)
