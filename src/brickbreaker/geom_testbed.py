from .core.application_listener import ApplicationListener
from .core.shape_renderer import ShapeRenderer
from .core.orthographic_camera import OrthographicCamera
from .core.fit_viewport import FitViewport
from .core import color
from .core import primitive
from .core.intersector import Intersector
from .core import viewport_utils
from .utils.debug_camera_controller import DebugCameraController
from .utils import shape_render_utils

from .core.gdx import Gdx


class GeomTestbed(ApplicationListener):
    def create(self):
        self.camera = OrthographicCamera()
        self.viewport = FitViewport(
            Gdx.graphics.width,
            Gdx.graphics.height,
            self.camera
        )
        self.debug_camera_controller = DebugCameraController()
        self.debug_camera_controller.set_start_position(
            0,
            0,
        )
        self.renderer = ShapeRenderer()

    def dispose(self):
        self.renderer.dispose()

    def update_debug_camera(self, delta: float):
        self.debug_camera_controller.handle_debug_input(delta)
        self.debug_camera_controller.apply_to(self.camera)

    def resize(self, width, height):
        self.viewport.update(width, height, True)
        viewport_utils.debug_pixels_per_unit(self.viewport)

    def render(self, delta: float):
        self.update_debug_camera(delta)

        self.viewport.apply(False)
        viewport_utils.draw_grid(self.viewport, self.renderer)

        self.renderer.set_projection_matrix(self.camera.combined)
        self.renderer.begin(ShapeRenderer.ShapeType.Line)
        self.draw_debug()
        self.renderer.end()

    def draw_debug(self):
        # line = primitive.Line((0, 0), (-20, 20))
        # shape_render_utils.line(self.renderer, line)

        # segment = primitive.Segment((50, 50), (100, 50))
        # shape_render_utils.segment(self.renderer, segment)

        # circle = primitive.Circle((50, 50), 50)
        # shape_render_utils.circle(self.renderer, circle)

        # rect = primitive.Rectangle((10, 10), (50, 50))
        # shape_render_utils.rectangle(self.renderer, rect)

        o_rect = primitive.OrientedRectangle((100, 100), (50, 100), 90)
        shape_render_utils.oriented_rectangle(self.renderer, o_rect)
