from .core.shape_renderer import ShapeRenderer
from .core.orthographic_camera import OrthographicCamera
from .core.fit_viewport import FitViewport
from .core.sprite_batch import SpriteBatch
from .core.texture_atlas import TextureAtlas
from .core import color
from .core import viewport_utils
from .utils.debug_camera_controller import DebugCameraController
from . import game_config


class GameRenderer:
    def __init__(self, game_world) -> None:
        self.game_world = game_world
        self.camera = OrthographicCamera()
        self.viewport = FitViewport(
            game_config.WORLD_WIDTH,
            game_config.WORLD_HEIGHT,
            self.camera
        )
        self.renderer = ShapeRenderer()
        self.batch = SpriteBatch()
        self.debug_camera_controller = DebugCameraController()
        self.debug_camera_controller.set_start_position(
            game_config.WORLD_CENTER_X,
            game_config.WORLD_CENTER_Y
        )

        # refactor out
        self.texture_atlas = TextureAtlas("textures/gameplay/gameplay.atlas")
        self.background_region = self.texture_atlas.find_region("background")
        self.paddle_region = self.texture_atlas.find_region("paddle")
        self.brick_region = self.texture_atlas.find_region("brick")
        self.ball_region = self.texture_atlas.find_region("ball")

    def resize(self, width: int, height: int):
        self.viewport.update(width, height, True)

    def render(self, delta: float):
        self.debug_camera_controller.handle_debug_input(delta)
        self.debug_camera_controller.apply_to(self.camera)

        self.render_game_play()
        self.render_debug()

    def render_game_play(self):
        self.batch.set_projection_matrix(self.camera.combined)
        self.batch.begin()
        self.draw_game_play()
        self.batch.end()

    def draw_game_play(self):
        # background
        background = self.game_world.background
        self.batch.draw_texture_region(
            self.background_region,
            background.first_region_bounds.x,
            background.first_region_bounds.y,
            background.first_region_bounds.width,
            background.first_region_bounds.height
        )
        self.batch.draw_texture_region(
            self.background_region,
            background.second_region_bounds.x,
            background.second_region_bounds.y,
            background.second_region_bounds.width,
            background.second_region_bounds.height
        )

        # paddle
        paddle = self.game_world.paddle
        self.batch.draw_texture_region(
            self.paddle_region,
            paddle.x,
            paddle.y,
            paddle.width,
            paddle.height
        )

        # bricks
        for brick in self.game_world.bricks:
            self.batch.draw_texture_region(
                self.brick_region,
                brick.x,
                brick.y,
                brick.width,
                brick.height
            )

        # ball
        ball = self.game_world.ball
        self.batch.draw_texture_region(
            self.ball_region,
            ball.x,
            ball.y,
            ball.width,
            ball.height
        )

    def render_debug(self):
        self.viewport.apply(False)

        print(self.game_world.draw_grid)

        viewport_utils.draw_grid(self.viewport, self.renderer)
        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.draw_debug()
        self.renderer.end()

    def draw_debug(self):
        old_color = self.renderer.color.copy()
        self.renderer.color = color.RED

        # background
        background = self.game_world.background
        self.renderer.rect(
            background.first_region_bounds.x,
            background.first_region_bounds.y,
            background.first_region_bounds.width,
            background.first_region_bounds.height
        )
        self.renderer.rect(
            background.second_region_bounds.x,
            background.second_region_bounds.y,
            background.second_region_bounds.width,
            background.second_region_bounds.height
        )

        # paddle
        paddle = self.game_world.paddle
        self.renderer.rect(paddle.x, paddle.y, paddle.width, paddle.height)

        # bricks
        for brick in self.game_world.bricks:
            self.renderer.rect(brick.x, brick.y, brick.width, brick.height)

        # ball
        ball = self.game_world.ball
        self.renderer.polygon(ball.bounds.get_transformed_vertices())

        self.renderer.color = old_color

    def dispose(self):
        self.renderer.dispose()
