from .rectangle import Rectangle


class Polygon:
    def __init__(self) -> None:
        self.local_vertices: list[float] = []
        self.world_vertices: list[float] = None
        self.x = 0
        self.y = 0
        self.bounds = None
        self.dirty = True

    def set_position(self, x: float, y: float):
        if x == self.x and y == self.y:
            return

        self.x = x
        self.y = y
        self.dirty = True

    def set_vertices(self, vertices: list[float]):
        # polygons must contain at least 3 points
        assert len(vertices) >= 6
        self.local_vertices = vertices
        self.dirty = True

    def get_transformed_vertices(self):
        if not self.dirty:
            return self.world_vertices

        self.world_vertices = []
        for index in range(0, len(self.local_vertices), 2):
            x = self.x + self.local_vertices[index]
            y = self.y + self.local_vertices[index + 1]
            self.world_vertices.append(x)
            self.world_vertices.append(y)

        self.dirty = False
        return self.world_vertices

    def get_bounding_rectangle(self) -> Rectangle:
        vertices = self.get_transformed_vertices()

        min_x = vertices[0]
        min_y = vertices[1]
        max_x = vertices[0]
        max_y = vertices[1]

        for i in range(2, len(vertices), 2):
            min_x = min(vertices[i], min_x)
            min_y = min(vertices[i + 1], min_y)
            max_x = max(vertices[i], max_x)
            max_y = max(vertices[i + 1], max_y)

        if self.bounds is None:
            self.bounds = Rectangle()

        self.bounds.x = min_x
        self.bounds.y = min_y
        self.bounds.width = max_x - min_x
        self.bounds.height = max_y - min_y

        return self.bounds
