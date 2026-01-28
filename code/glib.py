import sys

def is_ident_start(char):
    return char.isalpha() or char == '_'

found = {
    "write_bits_8": 1,
    "write_u8": 1,
    "write_u16": 2,
    "write_u32": 4,
    "write_u64": 8,
}

def get_byte_size_from_str_end(s):
    i = len(s) - 1
    while i >= 0 and s[i].isdigit():
        i -= 1
    i += 1

    match s[i:]:
        case "8":   return 1
        case "16":  return 2 
        case "32":  return 4
        case "64":  return 8
        case _: return 0


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

        # check if this is a function definition or a call
        if pos < len(source) and source[pos] != "()"[0]:
            continue
        # advance until the function body starts
        while pos < len(source) and source[pos] != "{}"[0]:
            pos += 1
        break

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
            iden = source[beg:pos]

            if iden == "write_zeroes":
                while pos < len(source) and source[pos] == ' ':
                    pos += 1
                num = 0
                while pos < len(source) and source[pos].isdigit():
                    num *= 10 + int(source[pos])
                    pos += 1
                bts += num
            else:
                bts += get_bytes_from_func(iden, source)
                pos += get_byte_size_from_str_end(iden) * 3
        else:
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
            while pos < len(source) and (source[pos].isalnum() or source[pos] == '_'):
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
    binary = "{:032b}".format(number)
    binarr = [0] * 32
    assert len(binary) == 32, "error [glib]: 2's compliment impl only supports 32 bit"

    # one's complement
    for i in range(len(binary)):
        binarr[len(binarr) - i - 1] = 1 - int(binary[i])

    # two's complement
    binarr[0] += 1

    for i in range(len(binarr)):
        if binarr[i] < 2:
            break
        binarr[i] = 0
        if i + 1 < len(binarr):
            binarr[i + 1] += 1

    binstr = "".join(str(x) for x in reversed(binarr))
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
                    while pos < len(source) and (source[pos].isalnum() or source[pos] == '_'):
                        pos += 1
                    lbl[source[beg:pos]] = bts
                else:
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
            while pos < len(source) and source[pos] != '>' and source[pos] != '\n':
                pos += 1
            if pos < len(source) and source[pos] == '\n':
                pos += 1
                continue
            pos += 1

            beg = pos
            while pos < len(source) and (source[pos].isalnum() or source[pos] == '_'):
                pos += 1
            
            func = source[beg:pos]

            if iden == "call_imm32":
                assert func in lbl, "error [glib]: calling non existend function `" + func + "`"
            else:
                que.append([iden, bts, func, arg])
                continue

            offset = bts - lbl[func]
            newoff = get_twos_compliment(offset)
            
            adr += 1
            source = source[:arg] + newoff + source[arg + len(newoff):]
        pos += 1

    for entry in que:
        [eiden, ebytes, elbl, efile] = entry
        assert elbl in lbl, "error [glib]: label `{}` not found".format(elbl)

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
    file = "bylc"

    if len(sys.argv) == 0:
        print("error [glib]: expected flag")
        sys.exit(1)

    f = open(file, "r+")
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
            sum = 0
            for i in range(1, len(sys.argv)):
                sum += get_bytes_from_func(sys.argv[i], source)
            print(f"bytes: {sum} | {sum:02X}")
        case "-c" | "--fix-calls":
            source, adr = update_addresses(source)

            f = open(file, "w")
            if adr > 1:
                print(f"glib: updated {adr} addresses")
            else:
                print(f"glib: updated {adr} addresses")

            f.write(source)
            f.truncate()
        case "-t" | "--two-complement":
            assert len(sys.argv) > 1, "error [glib]: need number for two's compliment"
            print(get_twos_compliment(int(sys.argv[1])))
        case _:
            print("error [glib]: unknown flag provided")
    f.close()

if __name__ == "__main__":
    main()
    
