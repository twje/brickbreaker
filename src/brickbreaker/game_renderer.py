from brickbreaker.core.texture_region import TextureRegion
from .core.shape_renderer import ShapeRenderer
from .core.orthographic_camera import OrthographicCamera
from .core.fit_viewport import FitViewport
from .core.sprite_batch import SpriteBatch
from .core.texture_atlas import TextureAtlas
from .core import color
from .core import viewport_utils
from .utils.debug_camera_controller import DebugCameraController
from .utils import shape_render_utils
from .utils.entity_base import EntityBase
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
        viewport_utils.debug_pixels_per_unit(self.viewport)

    def render(self, delta: float):
        self.debug_camera_controller.handle_debug_input(delta)
        self.debug_camera_controller.apply_to(self.camera)

        self.render_game_play()
        self.render_debug()

    def render_game_play(self):
        if not self.game_world.draw_world:
            return

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
        self.draw_entity(self.paddle_region, paddle)

        # bricks
        for brick in self.game_world.bricks:
            self.draw_entity(self.brick_region, brick)

        # ball
        ball = self.game_world.ball
        self.draw_entity(self.ball_region, ball)

    def render_debug(self):
        self.viewport.apply(False)

        if self.game_world.draw_grid:
            viewport_utils.draw_grid(self.viewport, self.renderer, True)

        if self.game_world.draw_debug:
            self.renderer.set_projection_matrix(self.camera.combined)
            self.renderer.begin(ShapeRenderer.ShapeType.Line)
            self.draw_debug()
            self.renderer.end()

    def draw_debug(self):
        old_color = self.renderer.color.copy()
        self.renderer.color = color.RED

        # background
        background = self.game_world.background
        shape_render_utils.rectangle(
            self.renderer, background.first_region_bounds)
        shape_render_utils.rectangle(
            self.renderer, background.second_region_bounds)

        # paddle
        paddle = self.game_world.paddle
        shape_render_utils.polygon(self.renderer, paddle.bounds)

        # bricks
        for brick in self.game_world.bricks:
            shape_render_utils.polygon(self.renderer, brick.bounds)

        # ball
        ball = self.game_world.ball
        shape_render_utils.polygon(self.renderer, ball.bounds)

        self.renderer.color = old_color

    def draw_entity(self, region: TextureRegion, entity: EntityBase):
        self.batch.draw_texture_region(
            region,
            entity.x,
            entity.y,
            entity.width,
            entity.height
        )

    def dispose(self):
        self.renderer.dispose()
