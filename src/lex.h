#ifndef LEX_H
#define LEX_H

#include "hash.h"

typedef struct {
    FILE* file;
    hash_table_t* table;
} lex_t;

lex_t* lex_file(FILE* file);

#endif /* LEX_H */
