from brickbreaker.core.application_listener import ApplicationListener


class GameBase(ApplicationListener):
    def __init__(self) -> None:
        super().__init__()
        self.current_screen = None

    def set_screen(self, screen):
        if self.current_screen is screen:
            return

        if self.current_screen is not None:
            self.current_screen.hide()

        self.current_screen = screen
        self.current_screen.show()

    def create(self):
        self.post_create()

    def dispose(self):
        if self.current_screen is not None:
            self.current_screen.dispose()

    def pause(self):
        if self.current_screen is not None:
            self.current_screen.pause()

    def render(self, delta):
        if self.current_screen is not None:
            self.current_screen.render(delta)

    def resize(self, width, height):
        if self.current_screen is not None:
            self.current_screen.resize(width, height)

    def resume(self):
        if self.current_screen is not None:
            self.current_screen.resume()

    def post_create(self):
        pass
