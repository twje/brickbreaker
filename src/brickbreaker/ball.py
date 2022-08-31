from .utils.entity_base import EntityBase
from .utils import shape_utils


class Ball(EntityBase):
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        super().__init__(x, y, width, height)

    def create_vertices(self):
        return shape_utils.create_octagon(
            self.width/2,
            self.height/2,
            self.width/2,
            8
        )
