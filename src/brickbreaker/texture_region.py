from .texture import Texture


class TextureRegion:
    def __init__(self, texture: Texture, name: str, x: int, y: int, width: int, height: int) -> None:
        self.texture = texture
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def uv1(self):
        pass

    @property
    def uv2(self):
        pass
