import sys

def is_ident_start(char):
    return char.isalpha() or char == '_'

found = {
    "write_u8": 1,
    "write_bits_8": 1,
    "write_u16": 2,
    "write_u32": 4,
    "write_u64": 8,
}

def get_bytes_from_func(fn, source):
    if fn in found:
        return found[fn]

    bts = 0
    pos = 0
    fln = len(fn)

    while pos + fln < len(source):
        # bad but this is python so anyway
        if source[pos:pos + fln] != fn:
            pos += 1
            continue

        pos += fln
        while pos < len(source) and source[pos] == ' ':
            pos += 1

        # have to do this since my neovim idents 
        # wrong if i don't close the braces :/
        if pos < len(source) and source[pos] != "()"[0]:
            continue

        while pos < len(source) and source[pos] != "{}"[0]:
            pos += 1

        brc = 1
        pos += 1
        while pos < len(source) and brc > 0:
            if source[pos] == "{}"[0]:
                brc += 1
            if source[pos] == "{}"[1]:
                brc -= 1

            if is_ident_start(source[pos]):
                beg = pos
                while pos < len(source) and source[pos].isalnum() or source[pos] == '_':
                    pos += 1

                if source[beg:pos] == "write_zeroes":
                    while pos < len(source) and source[pos] == ' ':
                        pos += 1
                    num = 0
                    while pos < len(source) and source[pos].isdigit():
                        num *= 10 + int(source[pos])
                        pos += 1
                    bts += num
                else:
                    bts += get_bytes_from_func(source[beg:pos], source)
            pos += 1

    found[fn] = bts
    return bts

def get_label(lbl, offset, source):
    lbl_start = -1
    pos = offset

    while pos < len(source) and lbl_start == -1:
        if source[pos] == '.':
            beg = pos
            pos += 1
            while pos < len(source) and (source[pos].isalpha() or source[pos] == '_'):
                pos += 1
            
            if lbl == source[beg:pos]:
                lbl_start = pos
            else:
                pos += 1
        else:
            pos += 1
    return lbl_start

def get_bytes_in_range(src, dst, source):
    sum_of_bytes = 0
    pos = src

    while pos < dst and source[pos] != '\n':
        pos += 1

    while pos < dst:
        if source[pos] == '#':
            while pos < len(source) and source[pos] != '\n':
                pos += 1

        if is_ident_start(source[pos]):
            beg = pos
            while source[pos].isalnum() or source[pos] == '_':
                pos += 1

            if beg != pos:
                sum_of_bytes += get_bytes_from_func(source[beg:pos],  source)
        pos += 1
    return sum_of_bytes

def get_twos_compliment(number):
    binary = "{:08b}".format(number)
    binarr = [1] * 32

    # one's complement
    for i in range(len(binary)):
        binarr[len(binarr) - 8 + i] = 1 - int(binary[i])
    
    # two's complement
    binarr[len(binarr) - 1] += 1

    for i in range(len(binarr) - 1, -1, -1):
        if binarr[i] < 2:
            break
        binarr[i] = 0

        if i > 0:
            binarr[i - 1] += 1

    binstr = "".join(str(x) for x in binarr)
    newnum = ""

    for i in range(4):
        bin_as_hex = "{:02x}".format(int(binstr[i * 8 : (i + 1) * 8], 2))
        newnum += ' ' + bin_as_hex

    return newnum

def update_addresses(source):
    lbl = {}
    que = []
    pos = get_label(".begin", 0, source)
    bts = 0
    adr = 0

    while pos < len(source) and source[pos] != '\n':
        pos += 1

    while pos < len(source):
        if source[pos] == '#':
            while pos < len(source) and source[pos] != '\n':
                if source[pos] == '.':
                    pos += 1
                    beg = pos
                    while pos < len(source) and (source[pos].isalpha() or source[pos] == '_'):
                        pos += 1
                    lbl[source[beg:pos]] = bts
                pos += 1

        if not is_ident_start(source[pos]):
            pos += 1
            continue

        beg = pos
        while pos < len(source) and (source[pos].isalnum() or source[pos] == '_'):
            pos += 1

        iden = source[beg:pos]
        bts += get_bytes_from_func(iden, source)
        skip = 0

        if iden == "call_imm32" or iden == "jmp_imm32" or iden.startswith("jcc_"):
            arg = pos
            while pos < len(source) and source[pos] != '>':
                pos += 1
            pos += 1

            beg = pos
            while pos < len(source) and (source[pos].isalpha() or source[pos] == '_'):
                pos += 1
            
            func = source[beg:pos]

            if iden == "jmp_imm32" or iden.startswith("jcc_"):
                que.append([iden, bts, func, arg])
                continue
            else:
                assert func in lbl, "error [glib]: calling non existend function `" + func + "`"

            offset = bts - lbl[func]
            newoff = get_twos_compliment(offset)
            
            adr += 1
            source = source[:arg] + newoff + source[arg + len(newoff):]
        elif iden.endswith("imm8"):
            skip = 1
        elif iden.endswith("imm16"):
            skip = 2
        elif iden.endswith("imm32"):
            skip = 4
        elif iden.endswith("imm64"):
            skip = 8
        for i in range(skip):
            pos += 3
        pos += 1

    for entry in que:
        [eiden, ebytes, elbl, efile] = entry
        assert elbl in lbl, "error [glib]: label not found"

        offset = lbl[elbl] - ebytes
        newoff = ""

        if offset < 0:
            newoff = get_twos_compliment(abs(offset))
        else:
            binstr = "{:032b}".format(offset)
            for i in range(4):
                bin_as_hex = "{:02x}".format(int(binstr[i * 8 : (i + 1) * 8], 2))
                newoff += ' ' + bin_as_hex
        adr += 1

        if eiden.endswith("imm8"):
            newoff = newoff[9:]
        elif eiden.endswith("imm16"):
            newoff = newoff[6:]
        elif eiden.endswith("imm32"):
            newoff = newoff
        elif eiden.endswith("imm64"):
            assert False, "error [glib]: 64 bit jumps are not yet implemented"
        else:
            assert False, "error [glib]: unknown jump size {}".format(eiden)

        source = source[:efile] + newoff + source[efile + len(newoff):]

    return source, adr

def main():
    sys.argv.pop(0)

    if len(sys.argv) == 0:
        print("error [glib]: expected flag")
        sys.exit(1)

    f = open("gbyl", "r+")
    source = f.read()

    match sys.argv[0]:
        case "-r" | "--range":
            assert len(sys.argv) > 2, "error [glib]: range expects src and dst label"
            s = sys.argv[1]
            d = sys.argv[2]
            assert len(s) > 0 and s[0] == '.', "error [glib]: expected src as label"
            assert len(d) > 0 and d[0] == '.', "error [glib]: expected dst as label"

            src_start = get_label(s, 0, source)
            assert src_start != -1, "error [glib]: did not find src label"
            dst_start = get_label(d, src_start, source)
            assert dst_start != -1, "error [glib]: did not find dst label after src lbl"
            sum = get_bytes_in_range(src_start, dst_start, source)
            print(f"bytes: {sum} | {sum:02X}")
        case "-b" | "--bytes":
            assert len(sys.argv) > 1, "error [glib]: bytes expects mnemonic to search"
            sum = get_bytes_from_func(sys.argv[1], source)
            print(f"bytes: {sum} | {sum:02X}")
        case "-c" | "--fix-calls":
            source, adr = update_addresses(source)

            f = open("gbyl", "w")
            if adr > 1:
                print(f"glib: updated {adr} addresses")
            else:
                print(f"glib: updated {adr} addresses")

            f.write(source)
            f.truncate()
        case "-m" | "--multi":
            sum = 0
            for i in range(1, len(sys.argv)):
                sum += get_bytes_from_func(sys.argv[1], source)
            print(f"bytes: {sum} | {sum:02X}")
        case "-t" | "--two-complement":
            assert len(sys.argv) > 1, "error [glib]: need number for two's compliment"
            print(get_twos_compliment(int(sys.argv[1])))
        case _:
            print("error [glib]: unknown flag provided")
    f.close()

if __name__ == "__main__":
    main()
    
