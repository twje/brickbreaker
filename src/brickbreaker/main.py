from .utils.game_base import GameBase
from .core.application import Application
from .game_screen import GameScreen
from .geom_testbed import GeomTestbed
from . import game_config


class BrickBreaker(GameBase):
    def __init__(self) -> None:
        super().__init__()

    def post_create(self):
        self.set_screen(GameScreen(self))


def main():
    app = Application(
        GeomTestbed(),
        game_config.WIDTH,
        game_config.HEIGHT,
        "BrickBreaker"
    )
    app.run()
