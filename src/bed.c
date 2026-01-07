#include <stdio.h>

static u8 *lookup = u8"0123456789abcdef";

#define BYTE_TO_HEX(byte)                               \
    do {                                                \
        os_write(STD_IO_FD, &lookup[(byte) >>   4], 1);   \
        os_write(STD_IO_FD, &lookup[(byte) & 0x0f], 1);   \
    } while(0)                                          

void print_uint_as_hex(u32 uint) {
    os_write(STD_IO_FD, u8"0x", 2);
    BYTE_TO_HEX((uint >> 24) & 0xFF);
    BYTE_TO_HEX((uint >> 16) & 0xFF);
    BYTE_TO_HEX((uint >> 8 ) & 0xFF);
    BYTE_TO_HEX((uint      ) & 0xFF);
}

void print_byte_as_hex(u8 byte) {
    os_write(STD_IO_FD, u8"0x", 2);
    BYTE_TO_HEX(byte);
}

void error_log(String error_msg) {
    String error_red = S("error: ");
    os_write(STD_IO_FD, TUI_ERROR_COLOR.val, TUI_ERROR_COLOR.len); 
    os_write(STD_IO_FD, error_red.val, error_red.len); 
    os_write(STD_IO_FD, TUI_RESET_COLOR.val, TUI_RESET_COLOR.len); 
    os_write(STD_IO_FD, error_msg.val, error_msg.len); 
    os_exit(1);
}

s32 main(s32 argc, char **argv, u8 **environ) {
    if (argc < 2) {
        error_log(S("no binary provided\n"));
    }

    init_ctx(environ);

    // NOTE: load in a seperate thread
    String name = from_c_string(argv[1]);
    String temp = file_read_as_string_alloc(&ctx.allocator, name);

    // NOTE: there should be a better way lol
    Buffer data = *(Buffer*)((void*)&temp);

    if (is_elf_bin(data)) {
        app_elf_mode(data);
    } else {
        error_log(S("unknown format provided\n"));
    }

    return 0;
}
