#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>

#include "list.h"

list_t* list_new() {
    list_t* list = malloc(sizeof(list_t));

    if (list == NULL) {
        exit(EXIT_FAILURE);
    }

    list->head = NULL;
    list->tail = NULL;
    return list;
}

node_t* node_new(void* data) {
    node_t* node = malloc(sizeof(node_t));

    if (node == NULL) {
        exit(EXIT_FAILURE);
    }

    node->data = data;
    node->next = NULL;
    node->prev = NULL;
    return node;
}

void list_push_front(list_t* self, void* data) {
    if (self->head == NULL) {
        self->head = node_new(data);
        self->tail = self->head;
        return;
    }

    node_t* head = node_new(data);

    head->next = self->head;
    self->head->prev = head;
    self->head = head;
}

void list_push_back(list_t* self, void* data) {
    if (self->tail == NULL) {
        self->tail = node_new(data);
        self->head = self->tail;
        return;
    }

    node_t* tail = node_new(data);
    tail->prev = self->tail;
    self->tail->next = tail;
    self->tail = tail;
}

void list_pop_front(list_t* self) {
    if (self->head == NULL) return;

    node_t* next = self->head->next;
    free(self->head);
    self->head = next;
}

void list_pop_back(list_t* self) {
    if (self->tail == NULL) return;

    node_t* last = self->tail->prev;
    last->next = NULL;
    free(self->tail);
    self->tail = last;
}

void list_free(list_t* self) {
    node_t* prev = NULL;

    for (node_t* cur = self->head; cur != NULL; cur = cur->next) {
        free(prev);
        prev = cur;
    }

    free(prev);
    free(self);
}
