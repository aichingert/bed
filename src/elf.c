// https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html

// currently reading:
// https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.sheader.html

bool is_elf_bin(Buffer buf) {
    return buf.len > 4 && *((u32*)buf.mem) == 0x464c457f;
}

typedef u8  elf64_byte;
typedef u16 elf64_half;

typedef u32 elf64_word;
typedef s32 elf64_sword;

typedef u64 elf64_xword;
typedef u64 elf64_addr;
typedef u64 elf64_off;
typedef s64 elf64_sxword;

static const String ELF_TYPE_LIST[5] = {
    [0] = S("NONE"),
    [1] = S("REL"),
    [2] = S("EXEC"),
    [3] = S("DYN"),
    [4] = S("CORE"),
};

struct ElfIden {
    // magic number
    elf64_byte file_ident[4];
    // 32/64 bit 
    elf64_byte class;
    // encoding
    elf64_byte data;

    // used to verify validness
    elf64_byte version;
    elf64_byte os_abi;
    elf64_byte abi_version;

    // padding
    elf64_byte pad[6];
    // struct size
    elf64_byte nident;
};

struct ElfHeader {
    ElfIden     iden;
    elf64_half  bin_type;
    elf64_half  machine;
    elf64_addr  entry;
    elf64_off   phoff;
    elf64_off   shoff;
    elf64_word  flags;
    elf64_half  ehsize;
    elf64_half  phentsize;
    elf64_half  phnum;
    elf64_half  shentsize;
    elf64_half  shnum;
    elf64_half  shstrndx;
};

ElfHeader read_elf(u64 *byte_off, Buffer buf) {
    assert(buf.len >= sizeof(ElfHeader), S("invalid elf file too short"));
    ElfHeader ehead = {0};

    // TODO: read elf iden properly
    *byte_off += sizeof(ElfIden);

    ehead.bin_type  = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.machine   = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.entry     = mem_read_u64(buf.mem + *byte_off, byte_off);
    ehead.phoff     = mem_read_u64(buf.mem + *byte_off, byte_off);
    ehead.shoff     = mem_read_u64(buf.mem + *byte_off, byte_off);
    ehead.flags     = mem_read_u32(buf.mem + *byte_off, byte_off);
    ehead.ehsize    = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.phentsize = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.phnum     = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.shentsize = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.shnum     = mem_read_u16(buf.mem + *byte_off, byte_off);
    ehead.shstrndx  = mem_read_u16(buf.mem + *byte_off, byte_off);
    return ehead;
}

void print_elf_header(u64 byte_off, ElfHeader ehead) {
}

void app_elf_mode(Buffer buf) {
    init_tui();

    u64 byte_off = 0;
    ElfHeader ehead = read_elf(&byte_off, buf);

    print_elf_header(byte_off, ehead);

    print_uint_as_hex(byte_off);

    u8 sbuf[4096];
    memset(sbuf, 0, mob_static_array_len(sbuf));
    os_read(STD_IO_FD, sbuf, mob_static_array_len(sbuf));

    exit_tui();
}

