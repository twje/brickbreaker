from .game_world import GameWorld
from .game_renderer import GameRenderer


class GameController:
    def __init__(self, game_world, renderer) -> None:
        self.game_world: GameWorld = game_world
        self.renderer: GameRenderer = renderer

    def update(self, delta: float):
        self.handle_debug_input()

    def handle_debug_input(self):
        self.game_world.toggle_draw_grid()
