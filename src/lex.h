#ifndef LEX_H
#define LEX_H

#include "hash.h"

typedef struct {
    char* buf;
    size_t line_len;
} word_t;

typedef struct {
    FILE* file;
    list_t* words;
    hash_table_t* table;
} lex_t;

lex_t* lex_file(FILE* file);

#endif /* LEX_H */
