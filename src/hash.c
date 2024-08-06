#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "hash.h"

#define SEED 0x23ab8

// cyrb53 (c) 2018 bryc (github.com/bryc). License: Public domain. Attribution appreciated.
// A fast and simple 64-bit (or 53-bit) string hash function with decent collision resistance.
// Largely inspired by MurmurHash2/3, but with a focus on speed/simplicity.
uint8_t cybr64(char* key) {
    uint64_t h1 = 0xdeadbeef ^ SEED, h2 = 0x41c6ce57 ^ SEED;

    for(char* c = key; *c != '\0'; c++) {
        uint64_t cur = (uint64_t) *c;

        h1 = h1 ^ cur * 2654435761;
        h2 = h2 ^ cur * 1597334677;
    }

    h1  = h1 ^ (h1 >> 16) * 2246822507;
    h1 ^= h2 ^ (h2 >> 13) * 3266489909;
    h2  = h2 ^ (h2 >> 16) * 2246822507;
    h2 ^= h1 ^ (h1 >> 13) * 3266489909;

    return (uint8_t)((4294967296 * (2097151 & h2) + (h1 >> 0)) % UINT8_MAX);
}

hash_table_t* hash_new() {
    hash_table_t* hash = malloc(sizeof(hash_table_t));
    memset(hash, 0, sizeof *hash);

    if (hash == NULL) {
        exit(EXIT_FAILURE);
    }

    return hash;
}

item_t* item_new(char* key, int value) {
    item_t* item = malloc(sizeof(item_t));

    item->key = key;
    item->value = value;
    return item;
}

uint8_t hash_insert(hash_table_t* hash_table, item_t* item) {
    uint8_t position = cybr64(item->key);

    if (hash_table->items[position] == NULL) {
        list_t* list = list_new();
        list_push_front(list, (void*) item);
        hash_table->items[position] = list;
        return 1;
    }

    for (node_t* node = hash_table->items[position]->head; node != NULL; node = node->next) {
        item_t* cur = (item_t*)node->data;

        if (strcmp(cur->key, item->key) == 0) {
            cur->value += item->value;
            return 0;
        }
    }

    list_push_back(hash_table->items[position], (void*) item);
    return 1;
}

uint8_t hash_remove(hash_table_t* hash_table, char* key) {
    uint8_t position = cybr64(key);

    if (hash_table->items[position] == NULL) return 0;

    for (node_t* node = hash_table->items[position]->head; node != NULL; node = node->next) {
        item_t* cur = (item_t*)node->data;

        if (strcmp(cur->key, key) == 0) {
            if (node->prev == NULL) {
                hash_table->items[position]->head = node->next;

                if (node->next) {
                    node->prev = NULL;
                }
            } else {
                node_t* last = node->prev;
                last->next = node->next;

                if (node->next) {
                    node->next->prev = last;
                }
            }

            free(node);
            return 1;
        }
    }

    return 0;

}

item_t* hash_get(hash_table_t* hash_table, char* key) {
    uint8_t position = cybr64(key);

    if (hash_table->items[position] == NULL) {
        return NULL;
    }

    for (node_t* node = hash_table->items[position]->head; node != NULL; node = node->next) {
        item_t* item = (item_t*)node->data;

        if (strcmp(item->key, key) == 0) {
            return item;
        }
    }

    return NULL;
}
