
struct String {
    char *val;
    u64 len;
};

#define S(value) ((String){                             \
        .val = value,                                   \
        .len = (sizeof(value) / sizeof(value[0]) - 1)   \
        })                                              \


