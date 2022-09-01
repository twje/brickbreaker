from turtle import back
from .utils.parrallax_layer import ParallaxLayer
from .brick import Brick
from .paddle import Paddle
from .ball import Ball
from . import game_config


class EntityFactory:
    def create_bricks(self):
        bricks = []

        start_x = game_config.LEFT_PAD
        start_y = game_config.WORLD_HEIGHT - \
            (game_config.TOP_PAD + game_config.BRICK_HEIGHT)

        for row in range(game_config.ROW_COUNT):
            brick_y = start_y - row * \
                (game_config.ROW_SPACING + game_config.BRICK_HEIGHT)

            for column in range(game_config.COLUMN_COUNT):
                brick_x = start_x + column * \
                    (game_config.BRICK_WIDTH + game_config.COLUMN_SPACING)

                bricks.append(self.create_brick(brick_x, brick_y))

        return bricks

    def create_brick(self, x: float, y: float):
        return Brick(x, y, game_config.BRICK_WIDTH, game_config.BRICK_HEIGHT)

    def create_paddle(self):
        paddle = Paddle(
            game_config.PADDLE_START_X,
            game_config.PADDLE_START_Y,
            game_config.PADDLE_START_WIDTH,
            game_config.PADDLE_HEIGHT
        )
        paddle.post_init()
        return paddle

    def create_background(self):
        return ParallaxLayer(0, 0, game_config.WORLD_WIDTH, game_config.WORLD_HEIGHT)

    def create_ball(self):
        ball = Ball(
            game_config.BALL_START_X,
            game_config.BALL_START_Y,
            game_config.BALL_SIZE,
            game_config.BALL_SIZE
        )
        ball.post_init()
        return Ball(game_config.BALL_START_X, game_config.BALL_START_Y, game_config.BALL_SIZE, game_config.BALL_SIZE)
