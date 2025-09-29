#include <stdio.h>

static char **ENV = NULL;

s32 main(s32 argc, char **argv, char **environ) {
    ENV = environ;

    Window win = create_window(480, 640);

    return 0;

}
