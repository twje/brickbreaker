from .screen import Screen
from .sprite_batch import SpriteBatch
from .shape_renderer import ShapeRenderer
from .orthographic_camera import OrthographicCamera
from .fit_viewport import FitViewport
from . import game_config


class GameScreen(Screen):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def show(self):
        self.batch = SpriteBatch()
        self.camera = OrthographicCamera()
        self.viewport = FitViewport(
            game_config.WORLD_WIDTH,
            game_config.WORLD_HEIGHT,
            self.camera
        )
        self.renderer = ShapeRenderer()

    def dispose(self):
        """Called when the Application is destroyed."""
        pass

    def pause(self):
        """Called when the Application is paused, usually when it's not active or visible on-screen."""
        pass

    def render(self, delta):
        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.draw_debug()
        self.renderer.end()

    def draw_debug(self):
        self.renderer.rect(-1.0, -1.0, 1, 1)

    def resize(self, width, height):
        self.viewport.update(width, height, True)

    def resume(self):
        """Called when the Application is resumed from a paused state, usually when it regains focus."""
        pass
