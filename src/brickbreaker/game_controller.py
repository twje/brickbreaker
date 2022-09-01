from .game_world import GameWorld
from .game_renderer import GameRenderer
from .core.gdx import Gdx
import glfw


class GameController:
    def __init__(self, game_world, renderer) -> None:
        self.game_world: GameWorld = game_world
        self.renderer: GameRenderer = renderer

    def update(self, delta: float):
        self.handle_debug_input()

        if self.game_world.is_game_over():
            return

        ball = self.game_world.ball

        if ball.is_not_active() and Gdx.input.is_key_pressed(glfw.KEY_SPACE):
            self.game_world.activate_ball()

        self.game_world.update(delta)

    def handle_debug_input(self):
        if Gdx.input.is_key_pressed(glfw.KEY_F5):
            self.game_world.toggle_draw_grid()

        if Gdx.input.is_key_pressed(glfw.KEY_F6):
            self.game_world.toggle_debug()

        if Gdx.input.is_key_pressed(glfw.KEY_F7):
            self.game_world.toggle_draw_world()
