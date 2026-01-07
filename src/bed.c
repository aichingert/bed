#include <stdio.h>

s32 main(s32 argc, char **argv, u8 **environ) {
    init_ctx(environ);
    init_tui();

    String color = TUI_SET_COLOR(255, 255, 0);
    //printf("%s\n", color.val);
    os_write(STD_IO_FD, color.val, color.len); 

    String hex_value = S("0xbaa112 ");
    String mnemonic  = S("mov ");
    String registerv = S("rax");
    String comma     = S(", ");
    String literal   = S("60\n");

    os_write(STD_IO_FD, hex_value.val, hex_value.len);
    os_write(STD_IO_FD, mnemonic.val, mnemonic.len);
    os_write(STD_IO_FD, registerv.val, registerv.len);
    os_write(STD_IO_FD, comma.val, comma.len);
    os_write(STD_IO_FD, literal.val, literal.len);
    os_write(STD_IO_FD, TUI_RESET_COLOR.val, TUI_RESET_COLOR.len); 

    u8 buf[4096];
    memset(buf, 0, mob_static_array_len(buf));
    os_read(STD_IO_FD, buf, mob_static_array_len(buf));

    exit_tui();
    return 0;
}
