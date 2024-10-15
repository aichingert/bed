SRC_DIR = src
SRC = $(wildcard $(SRC_DIR)/*.c)

TARGET = toh

CC 		= gcc
CFLAGS  = -Wall -Wextra -Wpedantic # -Werror

.PHONY: build clean

run: build
	./$(TARGET)
	@rm $(TARGET)

build:
	@$(CC) $(CFLAGS) $(SRC) -o $(TARGET) -lwayland-client

clean:
	@rm $(TARGET)
