#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "lex.h"
#include "hash.h"
#include "list.h"

const char* help = 
    "info: Usage: tomb [OPTION] [FILE]\n"
    "\n"
    "Options:\n"
    "  -e --encode to compress the file\n"
    "  -d --decode to restore the previous state\n"
    "  --help lists this information\n";

typedef struct {
    int a;
    int b;
} data_t;

int main(int argc, char* argv[]) {
    printf("TESTING ----------\n");

    item_t* item1 = item_new("hello", 10);

    hash_table_t* hash = hash_new();
    hash_insert(hash, item1);
    hash_remove(hash, item1->key);

    printf("%d\n", hash_get(hash, item1->key) == NULL);
    printf("%d\n", hash_get(hash, "lol") == NULL);

    printf("TESTING DONE------\n");

    if (argc < 2) {
        printf("%s", help);
        return 1;
    }

    if (strcmp(argv[1], "-e") == 0 || strcmp(argv[1], "--encode") == 0) {
        printf("ENCODING\n");
    } else if (strcmp(argv[1], "-d") == 0 || strcmp(argv[1], "--decode") == 0) {
        printf("DECODING\n");
    } else if (strcmp(argv[1], "--help") == 0) {
        printf("%s", help);
    } else {
        printf("no such option: \033[0;31m%s\n\033[0mtry --help\n", argv[1]);
        return 1;
    }

    return 0;
}
