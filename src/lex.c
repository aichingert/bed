#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include "lex.h"

void lex_consume_line(lex_t* self, char* line) {
    size_t off = 0;
    size_t cnt = 0;

    for (char* s = line ;; s++) {
        cnt++;
        if (*s == ' ' || *s == '\n') {
            char cur = *s;
            *s = '\0';

            char* buf = malloc(sizeof(char) * (s - line));
            memcpy(buf, line + off, (s - line));

            item_t* item = item_new(buf, 1);
            hash_insert(self->table, item);

            *s = cur;
            off = cnt;
        }

        if (*s == '\n') break;
    }
}

void lex_consume_file(lex_t* self, FILE* file) {
    char* line = NULL;
    size_t len = 0;
    size_t read;

    while ((read = getline(&line, &len, file)) != -1) {
        lex_consume_line(self, line);
    }

    for (size_t i = 0; i < UINT8_MAX; i++) {
        if (self->table->items[i] == NULL) continue;

        for (node_t* node = self->table->items[i]->head; node != NULL; node = node->next) {
            item_t* item = (item_t*)node->data;
            printf("%s - %d\n", item->key, item->value);
        }
    }
}

lex_t* lex_file(FILE* file) {
    lex_t* lexer = malloc(sizeof(lex_t));

    if (lexer == NULL) {
        exit(EXIT_FAILURE);
    }

    lexer->table = hash_new();
    lex_consume_file(lexer, file);

    return lexer;
}


