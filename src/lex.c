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
            size_t len = s - line - off + 1;
            char* buf = malloc(sizeof(char) * len);
            memcpy(buf, line + off, len);
            buf[len - 1] = '\0';

            item_t* item = item = hash_get(self->table, buf);

            if (item != NULL) {
                item->value += 1;
            } else {
                hash_insert(self->table, item_new(buf, 1));
            }

            word_t* word = malloc(sizeof(word_t));
            word->buf = buf;
            word->line_len = s - line;

            list_push_back(self->words, word);
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

    /*
    for (size_t i = 0; i < UINT8_MAX; i++) {
        if (self->table->items[i] == NULL) continue;

        for (node_t* node = self->table->items[i]->head; node != NULL; node = node->next) {
            item_t* item = (item_t*)node->data;
            printf("%s - %d\n", item->key, item->value);
        }
    }
    */
}

lex_t* lex_file(FILE* file) {
    lex_t* lexer = malloc(sizeof(lex_t));

    if (lexer == NULL) {
        exit(EXIT_FAILURE);
    }

    lexer->words = list_new();
    lexer->table = hash_new();
    lex_consume_file(lexer, file);

    return lexer;
}


