from .core.gdx import Gdx
from .game_controller import GameController
import glfw


class PaddleInputController:
    def __init__(self, paddle, controller: GameController) -> None:
        self.paddle = paddle
        self.controller = controller

    def update(self, delta: float):
        if Gdx.input.is_key_held(glfw.KEY_LEFT):
            pass
        elif Gdx.input.is_key_held(glfw.KEY_RIGHT):
            pass