// NOTE: https://gaultier.github.io/blog/wayland_from_scratch.html
// NOTE: only supporting wayland

#include <stdio.h>

typedef struct Window {
    u16 width;
    u16 height;
} Window;

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

void read_wayland_env(
        String xdg_runtime_dir_name, 
        String *xdg_runtime_dir, 
        String wayland_display_name, 
        String *wayland_display
) {
    const char **env_ptr = ENV;

    while (*env_ptr != NULL && (xdg_runtime_dir->len == 0 || wayland_display->len == 0)) {
        if          (c_string_begins_with(*env_ptr, xdg_runtime_dir_name)) {
            *xdg_runtime_dir = from_c_string(*env_ptr + xdg_runtime_dir_name.len + 1);
        } else if   (c_string_begins_with(*env_ptr, wayland_display_name)) {
            *wayland_display = from_c_string(*env_ptr + wayland_display_name.len + 1);
        }

        env_ptr += 1;
    }

    xdg_runtime_dir->val = NULL;
}

s32 wayland_display_connect() {
    String xdg_runtime_dir = {0};
    String wayland_display = {0};
    read_wayland_env(S("XDG_RUNTIME_DIR"), &xdg_runtime_dir, S("WAYLAND_DISPLAY"), &wayland_display);

    if (xdg_runtime_dir.val == NULL) {
        printf("ERROR: no xdg runtime dir set\n");
        // TODO: sketchy assert
        char a = *xdg_runtime_dir.val;
        (void)a;
    }
    if (wayland_display.val == NULL) {
        wayland_display = S("wayland-0");
    }

    printf("%s - %s\n", xdg_runtime_dir.val, wayland_display.val);

    return 0;
}

Window create_window(u16 width, u16 height) {
    wayland_display_connect();

    return (Window){
        .width = width,
        .height = height,
    };
}
