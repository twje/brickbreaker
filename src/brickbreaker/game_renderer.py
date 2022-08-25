from .shape_renderer import ShapeRenderer
from .orthographic_camera import OrthographicCamera
from .fit_viewport import FitViewport
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

    def resize(self, width: int, height: int):
        self.viewport.update(width, height, True)

    def render(self, delta: float):
        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.draw_debug()
        self.renderer.end()

    def draw_debug(self):
        self.renderer.rect(-1.0, -1.0, 1, 1)

    def dispose(self):  # implement
        pass
