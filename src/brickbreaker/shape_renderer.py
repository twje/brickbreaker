from http import server
from .immediate_mode_renderer import ImmediateModeRenderer
from .shape_type import ShapeType
from .gdx import Gdx
import pyrr


class ShapeRenderer:
    ShapeType = ShapeType

    def __init__(self) -> None:
        self.shape_type = None
        self.renderer = ImmediateModeRenderer(5000, False, True, 0)
        self.projection = pyrr.matrix44.create_orthogonal_projection(
            0,
            Gdx.graphics.width,
            0,
            Gdx.graphics.height,
            0,
            1
        )

    def set_projection_matrix(self, matrix):
        self.projection = matrix

    def begin(self, shape_type):
        assert self.shape_type is None
        self.shape_type = shape_type
        self.renderer.begin(self.projection, self.shape_type)

    def end(self):
        assert self.shape_type is not None
        self.renderer.end()
        self.shape_type = None

    def rect(self, x: float, y: float, width: float, height: float):
        if self.shape_type == ShapeType.Line:
            # line 1
            self.renderer.vertex(x, y, 0)
            self.renderer.vertex(x + width, y, 0)

            # line 2
            self.renderer.vertex(x + width, y, 0)
            self.renderer.vertex(x + width, y + height, 0)

            # line 3
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.vertex(x, y + height, 0)

            # line 4
            self.renderer.vertex(x, y + height, 0)
            self.renderer.vertex(x, y, 0)
        else:
            # triangle 1
            self.renderer.vertex(x, y, 0)
            self.renderer.vertex(x + width, y, 0)
            self.renderer.vertex(x + width, y + height, 0)

            # triangle 2
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.vertex(x, y + height, 0)
            self.renderer.vertex(x, y, 0)
