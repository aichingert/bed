# byl

syntax (might change or is already changed check tests)

```odin
// PRIMARY goals of this syntax are to be as easy to parse as possible
// since it is kind of a pain...

// PRIMITIVES
//      s8, s16, s32, s64
//      might poke some more around the 
//      data section to include static strings

*s8 variable = 0;

[10]s64 s_array = [0,1,2,3,4,5,6,7,8,9];

struct Data {
    s32 a;
}

// the Data struct has to be provided before using it
// might improve this later on if I see this as necessary
struct Other {
    Data d;
    s64 some_field;
}

inc_a (*s32 a) {
    ^a += 1; // NOTE: not sure about this one
}

inc_data (*Data d) {
    ^d.a += 1; // NOTE: like I said not really sure about this one
}

// NOTE: has to be provided as entry point
main (s32 argc, **s8 argv) s8 {
    // ...
    return 0;
}
```

