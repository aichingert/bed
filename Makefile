SRC_DIR = src
SRC = $(wildcard $(SRC_DIR)/*.c)

TARGET = tomb

CC 		= gcc
CFLAGS  = -Wall

.PHONY: build clean

build:
	@$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	@rm $(TARGET)
