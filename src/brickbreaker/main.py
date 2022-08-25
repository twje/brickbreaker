from .game_base import GameBase
from .application import Application
from .game_screen import GameScreen
from . import game_config


class BrickBreaker(GameBase):
    def __init__(self) -> None:
        super().__init__()

    def post_create(self):
        self.set_screen(GameScreen(self))


def main():
    app = Application(
        BrickBreaker(),
        game_config.WIDTH,
        game_config.HEIGHT,
        "BrickBreaker"
    )
    app.run()
