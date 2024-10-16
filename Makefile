SRC_DIR = src
SRC = $(wildcard $(SRC_DIR)/*.c)

TARGET = toh
WAYLAND = /usr/share/wayland-protocols/stable

CC 		= gcc
CFLAGS  = -lwayland-client -lrt -Wall -Wextra -Wpedantic # -Werror

.PHONY: build clean

run: build
	./$(TARGET)
	@rm $(TARGET)

build:
	wayland-scanner private-code < $(WAYLAND)/xdg-shell/xdg-shell.xml > $(SRC_DIR)/xdg-shell-protocol.c
	wayland-scanner client-header < $(WAYLAND)/xdg-shell/xdg-shell.xml > $(SRC_DIR)/xdg-shell-client-protocol.h
	@$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	@rm $(TARGET)
