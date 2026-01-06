#include <stdio.h>

s32 main(s32 argc, char **argv, u8 **environ) {
    init_ctx(environ);
    init_tui();

    u8 buf[4096];
    memset(buf, 0, mob_static_array_len(buf));
    os_read(STD_IO_FD, buf, mob_static_array_len(buf));

    exit_tui();
    return 0;
}
