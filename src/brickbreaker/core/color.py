from dataclasses import dataclass


from dataclasses import dataclass


@dataclass
class Color:
    r: float = 1
    g: float = 1
    b: float = 1
    a: float = 1

    def __iter__(self) -> None:
        return iter([self.r, self.g, self.b, self.a])

    def copy(self):
        return Color(self.r, self.g, self.b, self.a)


WHITE = Color(1.0, 1.0, 1.0, 1.0)
RED = Color(1.0, 0.0, 0.0, 1.0)
GREEN = Color(0.0, 1.0, 0.0, 1.0)
BLUE = Color(0.0, 0.0, 1.0, 1.0)
PURPLE = Color(0.0, 1.0, 1.0, 1.0)