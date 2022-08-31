from . import game_config
from .core.gdx import Gdx
import glfw


class PaddleInputController:
    """
    Mobile touch gestures has been removed as it is only a Desktop only port
    """

    def __init__(self, paddle) -> None:
        self.paddle = paddle

    def update(self, delta: float):
        velocity_x = 0
        if Gdx.input.is_key_held(glfw.KEY_LEFT):
            velocity_x = -game_config.PADDLE_VELOCITY_X
        elif Gdx.input.is_key_held(glfw.KEY_RIGHT):
            velocity_x = game_config.PADDLE_VELOCITY_X

        self.paddle.velocity_x = velocity_x
