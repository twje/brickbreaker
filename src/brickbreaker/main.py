from .application_listener import ApplicationListener
from .application import Application
from .sprite_batch import SpriteBatch
from .shape_renderer import ShapeRenderer
from .orthographic_camera import OrthographicCamera
from .fit_viewport import FitViewport
from . import game_config


class BrickBreaker(ApplicationListener):
    def create(self):
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
        # self.batch.set_projection_matrix(self.camera.combined)
        # self.batch.begin()
        # self.batch.draw(None)
        # self.batch.end()

        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.draw_debug()
        self.renderer.end()

    def draw_debug(self):
        self.renderer.rect(-0.5, -0.5, 1, 1)

    def resize(self, width, height):
        self.viewport.update(width, height, True)

    def resume(self):
        """Called when the Application is resumed from a paused state, usually when it regains focus."""
        pass


def main():
    app = Application(
        BrickBreaker(),
        game_config.WIDTH,
        game_config.HEIGHT,
        "BrickBreaker"
    )
    app.run()
