static const char **ENV = NULL;

s32 main(s32 argc, char **argv, const char **environ) {
    ENV = environ;

    getenv(S("PATH"));

    Window win = create_window(480, 640);

    return 0;

}
