from . import game_config
from .entity_factory import EntityFactory
from .brick import Brick


class GameWorld:
    def __init__(self, factory: EntityFactory) -> None:
        self.factory = factory
        self.background = factory.create_background()
        self.paddle = factory.create_paddle()
        self.ball = factory.create_ball()
        self.bricks: list[Brick] = []
        self.draw_grid = False
        self.draw_debug = False
        self.draw_world = True
        self.start_level()

    def start_level(self):
        self.restart()
        self.bricks = self.factory.create_bricks()

    def restart(self):
        self.paddle.set_position(
            game_config.PADDLE_START_X,
            game_config.PADDLE_START_Y
        )
        self.ball.set_position(
            game_config.BALL_START_X,
            game_config.BALL_START_Y
        )
        self.ball.stop()

    def is_game_over(self):
        return False

    def update(self, delta: float):
        self.background.update(delta)

        if self.ball.is_not_active():
            return

        self.paddle.update(delta)

        self.block_paddle_from_leaving_world()

        self.ball.update(delta)

        self.block_ball_from_leaving_world()

        self.check_collision()

    def block_paddle_from_leaving_world(self):
        if self.paddle.x <= 0:
            self.paddle.x = 0

        paddle_right_x = self.paddle.x + self.paddle.width

        if paddle_right_x >= game_config.WORLD_WIDTH:
            self.paddle.x = game_config.WORLD_WIDTH - self.paddle.width

    def block_ball_from_leaving_world(self):
        # bottom
        if self.ball.y <= 0:
            self.restart()

        # 0top
        ball_top = self.ball.y + self.ball.width
        if ball_top >= game_config.WORLD_HEIGHT:
            self.y = game_config.WORLD_HEIGHT - self.ball.height
            self.ball.velocity_y *= -1

        # left
        if self.ball.x <= 0:
            self.ball.x = 0
            self.ball.velocity_x *= -1

        # right
        ball_right = self.ball.x + self.ball.width
        if ball_right >= game_config.WORLD_WIDTH:
            self.ball.x = game_config.WORLD_WIDTH - self.ball.width
            self.ball.velocity_x *= -1

    def check_collision(self):
        self.check_ball_with_paddle_collision()
        self.check_ball_with_brick_collision()

    def check_ball_with_paddle_collision(self):
        pass

    def check_ball_with_brick_collision(self):
        pass

    def activate_ball(self):
        self.ball.set_velocity_by_angled(
            game_config.BALL_START_ANGLE,
            game_config.BALL_START_SPEED
        )

    def is_game_over(self):
        return False

    def toggle_draw_grid(self):
        self.draw_grid = not self.draw_grid

    def toggle_debug(self):
        self.draw_debug = not self.draw_debug

    def toggle_draw_world(self):
        self.draw_world = not self.draw_world
