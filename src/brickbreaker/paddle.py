from .utils.entity_base import EntityBase


class Paddle(EntityBase):
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        super().__init__(x, y, width, height)
