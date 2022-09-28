from .immediate_mode_renderer import ImmediateModeRenderer
from .shape_type import ShapeType
from .color import Color
from .texture import Texture
from .texture_region import TextureRegion


class SpriteBatch:
    def __init__(self) -> None:
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, 1)
        self.drawing = False
        self.last_texture = None

    def set_projection_matrix(self, matrix):
        self.projection = matrix

    def begin(self):
        assert not self.drawing
        self.renderer.begin(self.projection, ShapeType.Filled)
        self.drawing = True

    def end(self):
        assert self.drawing
        self.flush()
        self.last_texture = None
        self.drawing = False

    def switch_texture(self, texture: Texture):
        self.flush()
        self.last_texture = texture

    def flush(self):
        if self.renderer.has_gemeotry_data():
            self.last_texture.bind()
            self.renderer.end()

    def check(self, texture: Texture, new_vertices: int):
        if texture is not self.last_texture:
            self.switch_texture(texture)
        elif new_vertices > self.renderer.free_vertices_count():
            self.flush()

    def draw_texture(self, texture: Texture, x: float, y: float, width: float, height: float):
        self.draw_texture_uv(
            texture,
            x,
            y,
            width,
            height,
            0,
            0,
            1,
            1
        )

    def draw_texture_region(self, texture_region: TextureRegion, x: float, y: float, width: float, height: float):
        u1, v1, u2, v2 = texture_region.uv()
        self.draw_texture_uv(
            texture_region.texture,
            x,
            y,
            width,
            height,
            u1,
            v1,
            u2,
            v2
        )

    def draw_texture_uv(self, texture: Texture, x: float, y: float, width: float, height: float, u1: float, v1: float, u2: float, v2: float):
        self.check(texture, 6)

        # triangle 1
        self.add_vertex(x, y, u1, v1)
        self.add_vertex(x + width, y, u2, v1)
        self.add_vertex(x + width, y + height, u2, v2)

        # triangle 2
        self.add_vertex(x + width, y + height, u2, v2)
        self.add_vertex(x, y + height, u1, v2)
        self.add_vertex(x, y, u1, v1)

    def add_vertex(self, x: float, y: float, u: float, v: float):
        self.renderer.color(self.color)
        self.renderer.position(x, y)
        self.renderer.texture_coordinate(0, u, v)
        self.renderer.new_vertex()

    def dispose(self):
        self.renderer.dispose()
