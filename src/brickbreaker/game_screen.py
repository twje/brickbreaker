from .entity_factory import EntityFactory
from .screen import Screen
from .game_world import GameWorld
from .game_renderer import GameRenderer
from .game_controller import GameController


class GameScreen(Screen):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def show(self):
        self.game_world = GameWorld(EntityFactory())
        self.renderer = GameRenderer(self.game_world)
        self.controller = GameController(self.game_world, self.renderer)

    def render(self, delta):
        self.controller.update(delta)
        self.renderer.render(delta)

    def resize(self, width: int, height: int):
        self.renderer.resize(width, height)

    def hide(self):
        self.dispose()

    def dispose(self):
        self.renderer.dispose()
