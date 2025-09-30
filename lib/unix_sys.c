#define SYS_CALL_SOCKET     41
#define SYS_CALL_CONNECT    42
#define SYS_CALL_EXIT       60

void assert(bool condition, char *msg) {
    #ifndef DEBUG

    if (!condition) {
        printf("ERROR: %s\n", msg);
        sys_exit(1);
    }

    #endif
}

s32 sys_socket(s32 domain, s32 type, s32 protocol) {
    u64 result = 0;

    __asm__ volatile (
            "   movq %[sys_call_n], %%rax\n"
            "   movq %[asm_domain], %%rdi\n"
            "   movq %[asm_type],   %%rsi\n"
            "   movq %[asm_prot],   %%rdx\n"
            "   syscall\n"
            : "=r" (result)
            :   [sys_call_n] "r" ((u64)SYS_CALL_SOCKET), 
                [asm_domain] "r" ((u64)domain),
                [asm_type]   "r" ((u64)type),
                [asm_prot]   "r" ((u64)protocol)
            : "%rdi", "%rsi", "%rdx"
    );

    return (s32)result;
}

s32 sys_connect(
        s32 socket_fd, 
        const SocketAddress *socket_addr, 
        u32 socket_len
) {
    u64 result = 0;

    __asm__ volatile (
            "   movq %[sys_call_n],     %%rax\n"
            "   movq %[asm_socket_fd],  %%rdi\n"
            "   movq %[asm_socket_addr],%%rsi\n"
            "   movq %[asm_socket_len], %%rdx\n"
            "   syscall\n"
            : "=r" (result)
            :   [sys_call_n]        "r" ((u64)SYS_CALL_CONNECT),
                [asm_socket_fd]     "r" ((u64)socket_fd),
                [asm_socket_addr]   "r" ((u64)socket_addr),
                [asm_socket_len]    "r" ((u64)socket_len)
            : "%rdi", "%rsi", "%rdx"
    );
    
    return (s32)result;
}

void sys_exit(u16 exit_code) {
    __asm__ volatile (
            "   movq %[sys_call_n],     %%rax\n"
            "   movq %[asm_exit_code],  %%rdi\n"
            "   syscall\n"
            : /* NO OUTPUT */
            :   [sys_call_n]    "r" ((u64)SYS_CALL_EXIT),
                [asm_exit_code] "r" ((u64)exit_code)
            : "%rdi"
    );
}


