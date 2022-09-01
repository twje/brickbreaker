from .application_listener import ApplicationListener
from .window import Window
from .input_manager import InputManager
from .clock import Clock
from .gdx import Gdx, Graphics


__all__ = ["DesktopApplication"]


class Application:
    def __init__(self, listener: ApplicationListener, width: int, height: int, title: str) -> None:
        super().__init__()
        self.listener = listener
        self.window = Window(self, width, height, title)
        self.clock = Clock()
        self.input = InputManager()
        self.fps = 1/60
        self.delta = 0

        # global
        Gdx.graphics = Graphics(self.window)
        Gdx.input = self.input

    def run(self):
        self.create()
        while not self.window.is_done():
            self.delta += self.clock.delta
            if self.delta >= self.fps:
                self.render()
                self.delta = 0

            self.window.update()
            self.input.update()
        self.destroy()

    def render(self):
        self.window.begin_render()
        self.listener.render(self.fps)
        self.window.end_render()

    def create(self):
        self.listener.create()
        self.listener.resize(self.window.width, self.window.height)

    def destroy(self):
        self.listener.pause()
        self.listener.dispose()
        self.window.destroy()

    # ----------------
    # Callback Methods
    # ----------------
    def window_maximize_callback(self):
        self.listener.resize(self.window.width, self.window.height)

    def window_restore_maximize_callback(self):
        self.listener.resize(self.window.width, self.window.height)

    def window_iconified_callback(self):
        self.listener.resize(self.window.width, self.window.height)
        self.listener.pause()

    def window_restore_iconified_callback(self):
        self.listener.resize(self.window.width, self.window.height)
        self.listener.resume()

    def window_resize(self, width, height):
        self.listener.resize(width, height)

    def key_pressed_callback(self, key):
        self.input.set_key_pressed(key)

    def key_released_callback(self, key):
        self.input.set_key_released(key)
