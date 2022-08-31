from .entity_factory import EntityFactory
from .utils.screen_base import ScreenBase
from .game_world import GameWorld
from .game_renderer import GameRenderer
from .game_controller import GameController
from .paddle_input_controller import PaddleInputController


class GameScreen(ScreenBase):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def show(self):
        self.factory = EntityFactory()
        self.game_world = GameWorld(self.factory)
        self.renderer = GameRenderer(self.game_world)
        self.controller = GameController(self.game_world, self.renderer)
        self.paddle_input_controller = PaddleInputController(
            self.game_world.paddle,
            self.controller
        )

    def render(self, delta):
        game_over = self.game_world.is_game_over()

        if not game_over:
            self.paddle_input_controller.update(delta)

        self.controller.update(delta)
        self.renderer.render(delta)

        if game_over:
            pass
            # transition to menu screen

    def resize(self, width: int, height: int):
        self.renderer.resize(width, height)

    def hide(self):
        self.dispose()

    def dispose(self):
        self.renderer.dispose()
