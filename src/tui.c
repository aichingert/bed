#define STD_IO_FD               1

#define TUI_SET_COLOR(r,g,b)    S("\e[38;2;" #r ";" #g ";" #b "m")
#define TUI_SET_POSITION(x, y)  S("\e[" #y ";" #x "H")

const String TUI_OPEN_BUF       = S("\e[?1049h");
const String TUI_CLOSE_BUF      = S("\e[?1049l");
const String TUI_CLEAR          = S("\e[2j");
const String TUI_RESET_COLOR    = S("\e[0m");
const String TUI_LEFT_TOP       = TUI_SET_POSITION(1, 1);

const String TUI_COLOR_NAVY     = TUI_SET_COLOR(45, 60, 89);
const String TUI_COLOR_SAGE     = TUI_SET_COLOR(148, 163, 120);
const String TUI_COLOR_YELLOW   = TUI_SET_COLOR(229, 186, 65);
const String TUI_COLOR_ORANGE   = TUI_SET_COLOR(209, 133, 92);

const String TUI_FG             = S("\e[48;2;197;200;198m");
const String TUI_BG             = S("\e[48;2;29;31;33m");

void init_tui() {
    os_write(STD_IO_FD, TUI_OPEN_BUF.val, TUI_OPEN_BUF.len);
    os_write(STD_IO_FD, TUI_CLEAR.val, TUI_CLEAR.len);
    os_write(STD_IO_FD, TUI_LEFT_TOP.val, TUI_LEFT_TOP.len);
}

void exit_tui() {
    os_write(STD_IO_FD, TUI_CLOSE_BUF.val, TUI_CLOSE_BUF.len);
}
