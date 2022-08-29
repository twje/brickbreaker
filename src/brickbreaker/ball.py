import math
from .polygon import Polygon


class Ball:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounds = self.create_octagon(
            x,
            y,
            self.width/2,
            self.height/2,
            self.width/2,
            8
        )

    def create_octagon(self, pos_x: float, pos_y: float, origin_x: float, origin_y: float, radius: float, vertex_count: float):
        vertices = []
        for index in range(0, vertex_count):
            x = origin_x + radius * \
                math.cos(math.radians(360 * index/vertex_count))
            y = origin_y + radius * \
                math.sin(math.radians(360 * index/vertex_count))
            vertices.extend([x, y])

        polygon = Polygon()
        polygon.set_position(pos_x, pos_y)
        polygon.set_vertices(vertices)
        return polygon
