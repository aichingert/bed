import sys

def is_ident_start(char):
    return char.isalpha() or char == '_'

def is_ident(char):
    return char.isalnum() or char == '_'

def skip_to_next_line(pos, source):
    while pos < len(source) and source[pos] != '\n':
        pos += 1
    pos += 1
    return pos

def get_register(pos, source):
    while pos < len(source) and source[pos] != '$' and source[pos] != '\n': pos += 1
    if pos < len(source) and source[pos] == '$':
        pos += 1
        beg = pos
        while pos < len(source) and is_ident(source[pos]): pos += 1
        return pos, source[beg:pos]
    return pos, None

def format_binary_string_to_hex_with_spaces(binstr):
    formated_hex_str = ""
    for i in range(len(binstr) // 8):
        bin_as_hex = "{:02x}".format(int(binstr[i * 8 : (i + 1) * 8], 2))
        formated_hex_str += ' ' + bin_as_hex
    return formated_hex_str

known_func_sizes = {
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

def get_bytes_from_func(func_ident, source):
    if func_ident in known_func_sizes:
        return known_func_sizes[func_ident]

    pos = 0
    size = 0

    while pos < len(source):
        if not is_ident_start(source[pos]):
            pos += 1
            continue

        func_it = 0
        found_ident = True

        while pos < len(source) and is_ident(source[pos]):
            pos += 1

            if not found_ident or func_it >= len(func_ident) or source[pos - 1] != func_ident[func_it]:
                found_ident = False
                continue
            func_it += 1

        if not found_ident or func_it < len(func_ident):
            pos += 1
            continue

        while pos < len(source) and source[pos] == ' ': pos += 1
        if pos + 1 >= len(source) or source[pos] + source[pos + 1] != "()": continue
        while pos < len(source) and source[pos] != "{}"[0]: pos += 1

        # NOTE: function position found
        break

    # NOTE: skipping opening brace
    pos += 1

    while pos < len(source) and source[pos] != '}':
        if not is_ident_start(source[pos]):
            pos += 1
            continue

        beg = pos
        while pos < len(source) and is_ident(source[pos]): pos += 1
        instr = source[beg:pos]

        match instr:
            case "write_zeroes": 
                while pos < len(source) and not source[pos].isdigit(): pos += 1
                beg = pos
                while pos < len(source) and source[pos].isdigit(): pos += 1
                size += int(source[beg:pos])
            case _:
                size += get_bytes_from_func(instr, source)
                pos = skip_to_next_line(pos, source)

    known_func_sizes[func_ident] = size
    return size

def get_label(label, offset, source):
    pos = offset

    while pos < len(source):
        if not source[pos] == '#':
            pos = skip_to_next_line(pos, source)
            continue

        while pos < len(source) and source[pos] != '.' and source[pos] != '\n':
            pos += 1
        if pos == '\n': continue

        beg = pos
        pos += 1
        while pos < len(source) and is_ident(source[pos]): pos += 1
        if label == source[beg:pos]:
            return pos
    return -1

def get_bytes_in_range(src, dst, source):
    sum_of_bytes = 0
    pos = skip_to_next_line(src, source)

    while pos < dst:
        if source[pos] == '#':
            pos = skip_to_next_line(pos, source)
            continue
        if not is_ident_start(source[pos]):
            pos += 1
            continue
        
        beg = pos
        while pos < len(source) and is_ident(source[pos]):
            pos += 1
        sum_of_bytes += get_bytes_from_func(source[beg:pos], source)
        pos = skip_to_next_line(pos, source)
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
    return binstr

def update_jumps(source):
    pos = get_label(".begin", 0, source)
    assert pos > 0, "error [glib]: expected begin label at the start of the instructions"
    pos = skip_to_next_line(pos, source)

    end = get_label(".shell_script_write_final_output", pos, source)
    assert end > 0, "error [glib]: expected end label at the end of the instructions"
    sum_of_bytes = 0

    jumps_to_update = []
    labels_encounter = {}

    while pos < end:
        if source[pos] == '#':
            pos += 1
            while pos < end and source[pos] == ' ' and source[pos] != '\n': 
                pos += 1
            if source[pos] != '.':
                pos = skip_to_next_line(pos, source)
                continue
            pos += 1
            beg = pos
            while pos < end and is_ident(source[pos]): pos += 1

            label = source[beg:pos]
            labels_encounter[label] = sum_of_bytes
            pos = skip_to_next_line(pos, source)
            continue

        if not is_ident_start(source[pos]):
            pos += 1
            continue
    
        beg = pos
        while pos < end and is_ident(source[pos]): 
            pos += 1

        instr = source[beg:pos]
        jmp_imm_val_start = pos
        prv = sum_of_bytes
        sum_of_bytes += get_bytes_from_func(instr, source)

        # TODO: fix this when using _u16_ registers
        if "_u32" in instr:
            # NOTE: adjusting write_u8 41
            # since it is conditionaly if 
            # one of the r8-r15 registers
            # is being used by the instr
            tmp = pos
            while tmp < len(source) and source[tmp] != '\n':
                tmp += 1

            off, reg = get_register(pos, source)
            new, rem = get_register(off, source)

            if reg[0] != 'r' and (rem == None or rem[0] != 'r'):
                sum_of_bytes -= 1

        while pos < end and source[pos] != '#' and source[pos] != '\n': pos += 1
        if pos < end and source[pos] == '\n': continue
        pos += 1
        while pos < end and source[pos] == ' ' and source[pos] != '\n': pos += 1
        if pos < end and source[pos] != '>': continue
        pos += 1

        beg = pos
        while pos < end and is_ident(source[pos]):
            pos += 1

        label = source[beg:pos]
        jumps_to_update.append((instr, label, sum_of_bytes, jmp_imm_val_start))
        pos = skip_to_next_line(pos, source)

    for it in jumps_to_update:
        ident, label, previous_bytes, file_insert_offset = it

        byts = get_byte_size_from_str_end(ident)
        bits = byts * 8
        diff = labels_encounter[label] - previous_bytes
        bins = ""
        trim = ""

        if diff < 0: 
            bins = get_twos_compliment(abs(diff))
            trim = '1'
        else:        
            bins = "{:032b}".format(diff)
            trim = '0'

        unused = bins[:32 - bits]
        assert len(unused.lstrip(trim)) == 0, "error [glib]: {0} instruction is trimming jump address".format(ident)

        source = source[:file_insert_offset] +\
            format_binary_string_to_hex_with_spaces(bins[32 - bits:]) +\
            source[file_insert_offset + 3 * byts:]
    return len(jumps_to_update), source

def main():
    sys.argv.pop(0)
    file = "bylc"

    if len(sys.argv) == 0:
        print("error [glib]: expected flag")
        sys.exit(1)

    f = open(file, "r+")
    source = f.read()

    # TODO: if this script gets slow one can compute the size of all
    # functions before running a command therfore only one pass has 
    # to be made on the function size parsing

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
        case "-u" | "--update_calls":
            updated, source = update_jumps(source)

            f = open(file, "w")
            if updated > 1: print(f"glib: updated {updated} addresses")
            else:           print(f"glib: updated {updated} addresses")
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
    
