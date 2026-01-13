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



def get_bytes_in_range(src_lbl, dst_lbl, source):
    assert len(src_lbl) > 0 and src_lbl[0] == '.', "error [bylib]: expected src as label"
    assert len(dst_lbl) > 0 and dst_lbl[0] == '.', "error [bylib]: expected dst as label"

    src_start = get_label(src_lbl, 0, source)
    assert src_start != -1, "error [bylib]: did not find src label"
    dst_start = get_label(dst_lbl, src_start, source)
    assert dst_start != -1, "error [bylib]: did not find dst label after src lbl"

    sum_of_bytes = 0

    pos = src_start
    while pos < dst_start and source[pos] != '\n':
        pos += 1

    while pos < dst_start:
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

def main():
    sys.argv.pop(0)

    if len(sys.argv) == 0:
        print("error [bylib]: expected flag")
        sys.exit(1)

    f = open("gbyl")
    source = f.read()
    f.close()

    match sys.argv[0]:
        case "-r" | "--range":
            assert len(sys.argv) > 2, "error [bylib]: range expects src and dst label"
            sum = get_bytes_in_range(sys.argv[1], sys.argv[2], source)
            print(f"bytes: {sum}")
        case "-b" | "--bytes":
            assert len(sys.argv) > 1, "error [bylib]: bytes expects mnemonic to search"
            sum = get_bytes_from_func(sys.argv[1], source)
            print(f"bytes: {sum}")
        case "-m" | "--multi":
            sum = 0
            for i in range(1, len(sys.argv)):
                sum += get_bytes_from_func(sys.argv[1], source)
            print(f"bytes: {sum}")


        case _:
            print("error [bylib]: unknown flag provided")

if __name__ == "__main__":
    main()
    
