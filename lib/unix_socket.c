#define UNIX_PATH_MAX 108

#define AF_UNIX 1

#define SOCK_STREAM 2

struct SocketAddress {
    u16 socket_family;
    s8  socket_data[14];
};

struct UnixSocketAddress {
    u16 socket_family;
    s8  socket_path[UNIX_PATH_MAX];
};
