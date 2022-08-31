from brickbreaker.core.polygon import Polygon
from . import shape_utils


class EntityBase:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.bounds = Polygon()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0

    def post_init(self):
        self.bounds = Polygon()
        self.bounds.set_vertices(self.create_vertices())

    def update(self, delta: float):
        new_x = self.x + self.velocity_x * delta
        new_y = self.y + self.velocity_y * delta
        self.set_position(new_x, new_y)

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y
        self.update_bounds()

    def update_bounds(self):
        self.bounds.set_position(self.x, self.y)
        self.bounds.set_vertices(self.create_vertices())

    def create_vertices(self):
        return shape_utils.create_rect(self.x, self.y, self.width, self.height)
