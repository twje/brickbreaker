from .shape_renderer import ShapeRenderer
from .orthographic_camera import OrthographicCamera
from .fit_viewport import FitViewport
from .sprite_batch import SpriteBatch
from .debug_camera_controller import DebugCameraController
from . import viewport_utils
from . import game_config
from .texture import Texture


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

        self.texture = Texture("textures/smiley.png")

    def resize(self, width: int, height: int):
        self.viewport.update(width, height, True)

    def render(self, delta: float):
        self.debug_camera_controller.handle_debug_input(delta)
        self.debug_camera_controller.apply_to(self.camera)

        viewport_utils.draw_grid(self.viewport, self.renderer)

        # batch
        self.batch.set_projection_matrix(self.camera.combined)
        self.batch.begin()
        self.batch.draw_texture(self.texture, 2, 2, 1, 1)
        self.batch.end()

        # debug
        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.renderer.rect(0.5, 0.5, 1, 1)
        self.renderer.end()

    def dispose(self):
        self.renderer.dispose()
