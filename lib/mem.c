u8* memcpy(u8 *dst, u8 *src, u64 size) {
    for (u64 i = 0; i < size; i++) {
        dst[i] = src[i];
    }

    return dst;
}
