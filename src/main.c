#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "lex.h"
#include "encode.h"

const char* help = 
    "info: Usage: tomb [OPTION] [FILE]\n"
    "\n"
    "Options:\n"
    "  -e --encode to compress the file\n"
    "  -d --decode to restore the previous state\n"
    "  --help lists this information\n";

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("%s", help);
        return 1;
    }

    FILE* file = fopen(argv[2], "r");

    if (file == NULL) {
        printf("File cannot be opened\n");
        return 1;
    }

    lex_t* lexer = lex_file(file);

    if (strcmp(argv[1], "-e") == 0 || strcmp(argv[1], "--encode") == 0) {
        encode_file(lexer, "out.tb");
    } else if (strcmp(argv[1], "-d") == 0 || strcmp(argv[1], "--decode") == 0) {
        printf("DECODING\n");
    } else {
        printf("no such option: \033[0;31m%s\n\033[0mtry --help\n", argv[1]);
        return 1;
    }

    return 0;
}
