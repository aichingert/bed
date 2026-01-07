bool is_elf_bin(Buffer buf) {
    return buf.len > 4 && *((u32*)buf.mem) == 0x464c457f;
}

void app_elf_mode(Buffer buf) {
    init_tui();

    u32 byte_offset = 0;
    byte_offset = 1200;
    print_uint_as_hex(byte_offset);

    u8 sbuf[4096];
    memset(sbuf, 0, mob_static_array_len(sbuf));
    os_read(STD_IO_FD, sbuf, mob_static_array_len(sbuf));

    exit_tui();
}

