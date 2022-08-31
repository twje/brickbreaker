from .input_manager import InputManager


class Graphics:
    def __init__(self, window) -> None:
        self.window = window

    @property
    def width(self):
        return self.window.width

    @property
    def height(self):
        return self.window.height


class Gdx:
    graphics: Graphics = None
    input: InputManager = None
