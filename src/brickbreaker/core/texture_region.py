from .texture import Texture


class TextureRegion:
    def __init__(self, texture: Texture, name: str, x: int, y: int, width: int, height: int) -> None:
        self.texture = texture
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def uv(self):
        u1 = self.x/self.texture.width
        v1 = 1 - ((self.y + self.height)/self.texture.height)
        u2 = (self.x + self.width)/self.texture.width
        v2 = 1 - (self.y/self.texture.height)

        return u1, v1, u2, v2
