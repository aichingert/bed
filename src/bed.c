#include <stdio.h>

s32 main(s32 argc, char **argv, char **environ) {
    init_ctx((u8**)environ);

    Window win = create_window(480, 640);

    return 0;

}
