#ifndef HASH_H
#define HASH_H

#include "list.h"

typedef struct {
    char *key;
    int value;
} item_t;

typedef struct {
    list_t* items[UINT8_MAX];
} hash_table_t;

hash_table_t* hash_new();
item_t* item_new();

uint8_t hash_insert(hash_table_t* hash_table, item_t* item);
uint8_t hash_remove(hash_table_t* hash_table, char* key);

item_t* hash_get(hash_table_t* hash, char* key);

#endif /* HASH_H */
