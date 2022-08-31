from .immediate_mode_renderer import ImmediateModeRenderer
from .shape_type import ShapeType
from .color import Color


class ShapeRenderer:
    ShapeType = ShapeType

    def __init__(self) -> None:
        self.shape_type = None
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, False)

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

    def check(self, preferred: ShapeType, other: ShapeType, new_vertices: int):
        assert self.shape_type is not None

        if self.shape_type != preferred and self.shape_type != other:
            self.end()
            self.begin(preferred)
        elif self.renderer.free_vertices_count() > new_vertices:
            shape_type = self.shape_type
            self.end()
            self.begin(shape_type)

    def rect(self, x: float, y: float, width: float, height: float):
        self.check(ShapeType.Line, ShapeType.Filled, 8)
        if self.shape_type == ShapeType.Line:
            # line 1
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y, 0)

            # line 2
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y + height, 0)

            # line 3
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y + height, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y + height, 0)

            # line 4
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y + height, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y, 0)
        else:
            # triangle 1
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y + height, 0)

            # triangle 2
            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x + width, y + height, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y + height, 0)

            with self.renderer.start_new_vertex():
                self.renderer.color(self.color)
                self.renderer.vertex(x, y, 0)

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self.check(ShapeType.Line, None, 2)

        with self.renderer.start_new_vertex():
            self.renderer.color(self.color)
            self.renderer.vertex(x1, y1, 0)

        with self.renderer.start_new_vertex():
            self.renderer.color(self.color)
            self.renderer.vertex(x2, y2, 0)

    def polygon(self, vertices):
        # Polygons must contain at least 3 points.
        assert len(vertices) >= 6
        # Polygons must have an even number of vertices.
        assert len(vertices) % 2 == 0

        self.check(ShapeType.Line, None, len(vertices))

        first_x = vertices[0]
        first_y = vertices[1]
        for index in range(0, len(vertices), 2):

            x1 = vertices[index]
            y1 = vertices[index + 1]

            if index + 2 >= len(vertices):
                x2 = first_x
                y2 = first_y
            else:
                x2 = vertices[index + 2]
                y2 = vertices[index + 3]

            with self.renderer.start_new_vertex():
                self.renderer.vertex(x1, y1, 0)
                self.renderer.color(self.color)

            with self.renderer.start_new_vertex():
                self.renderer.vertex(x2, y2, 0)
                self.renderer.color(self.color)

    def dispose(self):
        self.renderer.dispose()
