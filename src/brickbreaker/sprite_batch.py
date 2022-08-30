from .immediate_mode_renderer import ImmediateModeRenderer
from .shape_type import ShapeType
from .color import Color
from .texture import Texture
from .texture_region import TextureRegion


class SpriteBatch:
    def __init__(self) -> None:
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, True)
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
        if self.renderer.contains_vertices():
            self.last_texture.bind()
            self.renderer.end()

    def check(self, texture: Texture, new_vertices: int):
        if texture is not self.last_texture:
            self.switch_texture(texture)
        elif new_vertices > self.renderer.free_vertices_count():
            self.flush()

    def draw_texture(self, texture: Texture, x: float, y: float, width: float, height: float):
        self.check(texture, 6)

        # triangle 1
        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(0.0, 0.0)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(1.0, 0.0)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(1.0, 1.0)

        # triangle 2
        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(1.0, 1.0)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(0.0, 1.0)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(0.0, 0.0)

    def draw_texture_region(self, texture_region: TextureRegion, x: float, y: float, width: float, height: float):
        self.check(texture_region.texture, 6)

        u1, v1, u2, v2 = texture_region.uv()

        # triangle 1
        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u1, v1)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u2, v1)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u2, v2)

        # triangle 2
        with self.renderer.start_new_vertex():
            self.renderer.vertex(x + width, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u2, v2)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y + height, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u1, v2)

        with self.renderer.start_new_vertex():
            self.renderer.vertex(x, y, 0)
            self.renderer.color(self.color)
            self.renderer.texture(u1, v1)

    def dispose(self):
        self.renderer.dispose()
