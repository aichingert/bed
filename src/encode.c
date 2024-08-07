#include <string.h>
#include <stdio.h>

#include "encode.h"

void encode_file(lex_t* lexer, const char* out) {
    size_t prev = 0;

    for (node_t* cur = lexer->words->head; cur != NULL; cur = cur->next) {
        word_t* word = cur->data;

        printf("%ld\n", word->line_len);
        if (word->line_len - strlen(word->buf) < prev || word->line_len == 0) {
            printf("\n");
        }

        printf("%s ", word->buf);
        prev = word->line_len;
    }
}
