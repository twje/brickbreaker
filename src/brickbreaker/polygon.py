from tkinter.messagebox import RETRY


class Polygon:
    def __init__(self) -> None:
        self.local_vertices: list[float] = []
        self.world_vertices: list[float] = None
        self.x = 0
        self.y = 0
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
            x = self.local_vertices[index] + self.x
            y = self.local_vertices[index + 1] + self.y
            self.world_vertices.append(x)
            self.world_vertices.append(y)

        return self.world_vertices
