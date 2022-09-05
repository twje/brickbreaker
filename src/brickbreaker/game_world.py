from .core.intersector import Intersector
from .core.circle import Circle
from .entity_factory import EntityFactory
from .brick import Brick
from .utils import rectangle_utils
from . import game_config
from pyrr import Vector3


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
        for brick in list(self.bricks):
            brick_polygon = brick.bounds
            if not Intersector.overlap_convex_polygons(self.ball.bounds, brick_polygon):
                continue

            # stage brick bounds
            brick_bounds = brick_polygon.get_bounding_rectangle()
            bottom_left = rectangle_utils.get_bottom_left(brick_bounds)
            bottom_right = rectangle_utils.get_bottom_right(brick_bounds)
            top_left = rectangle_utils.get_top_left(brick_bounds)
            top_right = rectangle_utils.get_top_right(brick_bounds)

            # stage ball bounds
            radius = self.ball.width/2
            ball_bounds = Circle(
                self.ball.x + radius,
                self.ball.y + radius,
                radius
            )

            # hit detection
            center = Vector3([ball_bounds.x, ball_bounds.y, 0])
            radius_squared = ball_bounds.radius * ball_bounds.radius

            bottom_hit = Intersector.intersect_segment_circle(
                bottom_left,
                bottom_right,
                center,
                radius_squared
            )
            top_hit = Intersector.intersect_segment_circle(
                top_left,
                top_right,
                center,
                radius_squared
            )
            left_hit = Intersector.intersect_segment_circle(
                bottom_left,
                top_left,
                center,
                radius_squared
            )
            right_hit = Intersector.intersect_segment_circle(
                bottom_right,
                top_right,
                center,
                radius_squared
            )

            # left - right
            if self.ball.velocity_x > 0 and left_hit:
                self.ball.velocity_x *= -1
            elif self.ball.velocity_x < 0 and right_hit:
                self.ball.velocity_x *= -1

            # bottom - top
            if self.ball.velocity_y > 0 and bottom_hit:
                self.ball.velocity_y *= -1
            elif top_hit:
                self.ball.velocity_y *= -1

            self.bricks.remove(brick)

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
