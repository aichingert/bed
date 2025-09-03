#ifdef _WIN64
// TODO: windows
#elif __unix__

// NOTE: https://gaultier.github.io/blog/wayland_from_scratch.html


static const u32 wayland_display_object_id = 1;
static const u16 wayland_wl_registry_event_global = 0;
static const u16 wayland_shm_pool_event_format = 0;
static const u16 wayland_wl_buffer_event_release = 0;
static const u16 wayland_xdg_wm_base_event_ping = 0;
static const u16 wayland_xdg_toplevel_event_configure = 0;
static const u16 wayland_xdg_toplevel_event_close = 1;
static const u16 wayland_xdg_surface_event_configure = 0;
static const u16 wayland_wl_display_get_registry_opcode = 1;
static const u16 wayland_wl_registry_bind_opcode = 0;
static const u16 wayland_wl_compositor_create_surface_opcode = 0;
static const u16 wayland_xdg_wm_base_pong_opcode = 3;
static const u16 wayland_xdg_surface_ack_configure_opcode = 4;
static const u16 wayland_wl_shm_create_pool_opcode = 0;
static const u16 wayland_xdg_wm_base_get_xdg_surface_opcode = 2;
static const u16 wayland_wl_shm_pool_create_buffer_opcode = 0;
static const u16 wayland_wl_surface_attach_opcode = 1;
static const u16 wayland_xdg_surface_get_toplevel_opcode = 1;
static const u16 wayland_wl_surface_commit_opcode = 6;
static const u16 wayland_wl_display_error_event = 0;
static const u32 wayland_format_xrgb8888 = 1;
static const u32 wayland_header_size = 8;
static const u32 color_channels = 4;

// NOTE: only supporting wayland
typedef struct Window {
    u16 width;
    u16 height;
} Window;

#endif 

Window create_window(u16 width, u16 height) {
    return (Window){
        .width = width,
        .height = height,
    };
}
