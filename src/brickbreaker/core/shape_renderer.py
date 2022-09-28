from .immediate_mode_renderer import ImmediateModeRenderer
from .shape_type import ShapeType
from .color import Color


class ShapeRenderer:
    ShapeType = ShapeType

    def __init__(self) -> None:
        self.shape_type = None
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, 0)

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
            self.add_vertex(x, y)
            self.add_vertex(x + width, y)

            # line 2
            self.add_vertex(x + width, y)
            self.add_vertex(x + width, y + height)

            # line 3
            self.add_vertex(x + width, y + height)
            self.add_vertex(x, y + height)

            # line 4
            self.add_vertex(x, y + height)
            self.add_vertex(x, y)
        else:
            # triangle 1
            self.add_vertex(x, y)
            self.add_vertex(x + width, y)
            self.add_vertex(x + width, y + height)

            # triangle 2
            self.add_vertex(x + width, y + height)
            self.add_vertex(x, y + height)
            self.add_vertex(x, y)

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self.check(ShapeType.Line, None, 2)
        self.add_vertex(x1, y1)
        self.add_vertex(x2, y2)

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

            self.add_vertex(x1, y1)
            self.add_vertex(x2, y2)

    def add_vertex(self, x: float, y: float):
        self.renderer.position(x, y)
        self.renderer.color(self.color)
        self.renderer.new_vertex()

    def dispose(self):
        self.renderer.dispose()
