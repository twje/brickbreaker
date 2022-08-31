from brickbreaker.core.rectangle import Rectangle


class ParallaxLayer:
    def __init__(self, start_x, start_y, width, height) -> None:
        self.first_region_bounds = Rectangle(start_x, start_y, width, height)
        self.second_region_bounds = Rectangle(
            start_x,
            start_y + height,
            width,
            height
        )
