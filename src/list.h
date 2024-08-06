#ifndef LIST_H
#define LIST_H

typedef struct node_t node_t;

struct node_t {
    void* data;

    node_t* next;
    node_t* prev;
};

typedef struct {
    node_t* head;
    node_t* tail;
} list_t;

list_t* list_new();
node_t* node_new(void* data);

void list_push_front(list_t* self, void* data); 
void list_pop_front(list_t* self);

void list_push_back(list_t* self, void* data); 
void list_pop_back(list_t* self);

void list_free(list_t* self);

#endif /* LIST_H */
