# byl

syntax (might change or is already changed check tests)

```odin
// PRIMARY goals of this syntax are to be as easy to parse as possible
// since it is kind of a pain...

// PRIMITIVES
//      s8, s16, s32, s64
//      might poke some more around the 
//      data section to include static strings

// NOTE: there is no global variable support
*s8 variable = 0;

[10]s64 s_array = [0,1,2,3,4,5,6,7,8,9];

Data {
    s32 a;
}

// the Data struct has to be provided before using it
// might improve this later on if I see this as necessary
Other {
    Data d;
    s64 some_field;
}

inc_a (*s32 a) {
    ^a = ^a + 1; // NOTE: not sure about this one
}

inc_data (*Data d) {
    ^d.a = ^d.a - 1; // NOTE: like I said not really sure about this one
}

// NOTE: has to be provided as entry point
main (s32 argc, **s8 argv) {
    // ...

    // NOTE: provided by the compiler to invoke systemcalls
    // first argument is the systemcall number and after it
    // the values get filled by the abi specification
    // rdi: 1st, rsi: 2nd, ...
    #syscall(60, 0);  
}
```

