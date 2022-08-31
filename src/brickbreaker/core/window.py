from OpenGL.GL import *
import glfw

__all__ = ["GLFWWindow"]


class Window:
    """
    Handle windowing, input handling and OpenGL context creation
    """

    def __init__(self, application: "Application", width: int, height: int, title: str) -> None:
        self.application = application
        self.quit = False

        if not glfw.init():
            raise Exception("glfw can not be initialized")

        self.window = glfw.create_window(
            width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        center_x, center_y = self.get_window_center_pixel_coords_on_primary_monitor()
        glfw.set_window_pos(self.window, center_x, center_y)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        self.register_window_callbacks()
        glClearColor(0, 0.1, 0.1, 1)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    @property
    def width(self):
        width, _ = glfw.get_window_size(self.window)
        return width

    @property
    def height(self):
        _, height = glfw.get_window_size(self.window)
        return height

    def get_window_center_pixel_coords_on_primary_monitor(self):
        monitor = glfw.get_primary_monitor()
        position = glfw.get_monitor_pos(monitor)
        size = glfw.get_window_size(self.window)
        mode = glfw.get_video_mode(monitor)

        return (
            int(position[0] + (mode.size.width - size[0]) / 2),
            int(position[1] + (mode.size.height - size[1]) / 2)
        )

    def register_window_callbacks(self):
        glfw.set_window_maximize_callback(
            self.window,
            self.window_maximize_callback
        )
        glfw.set_window_iconify_callback(
            self.window,
            self.window_iconify_callback
        )
        glfw.set_window_size_callback(
            self.window,
            self.window_size_callback
        )
        glfw.set_key_callback(
            self.window,
            self.key_callback_callback
        )

    def is_done(self):
        return self.quit or glfw.window_should_close(self.window)

    def destroy(self):
        glfw.terminate()

    def update(self):
        glfw.poll_events()

    def begin_render(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def end_render(self):
        glfw.swap_buffers(self.window)

    # ----------------
    # Callback Methods
    # ----------------
    def window_maximize_callback(self, window, maximized: int):
        if maximized == 1:
            self.application.window_maximize_callback()
        else:
            self.application.window_restore_maximize_callback()

    def window_iconify_callback(self, window, iconified: int):
        if iconified == 1:
            self.application.window_iconified_callback()
        else:
            self.application.window_restore_iconified_callback()

    def window_size_callback(self, window, width, height):
        self.application.window_resize(self.width, self.height)

    def key_callback_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.application.key_pressed_callback(key)
        elif action == glfw.RELEASE:
            self.application.key_released_callback(key)
