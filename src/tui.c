#define STD_IO_FD   1

#define TUI_OPEN_BUF    S("\e[?1049h")
#define TUI_CLOSE_BUF   S("\e[?1049l")
#define TUI_CLEAR       S("\e[2j")

void init_tui() {
    os_write(STD_IO_FD, TUI_OPEN_BUF.val, TUI_OPEN_BUF.len);
    os_write(STD_IO_FD, TUI_CLEAR.val, TUI_CLEAR.len);
}

void exit_tui() {
    os_write(STD_IO_FD, TUI_CLOSE_BUF.val, TUI_CLOSE_BUF.len);
}
