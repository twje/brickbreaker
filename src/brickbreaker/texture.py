from OpenGL.GL import *
from PIL import Image


class Texture:
    def __init__(self, filepath) -> None:
        self.renderer_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.renderer_id)

        # set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        # set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # load image data
        self.image = Image.open(filepath)
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = self.image.convert("RGBA").tobytes()
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            self.image.width,
            self.image.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data
        )

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.renderer_id)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def delete(self):
        glDeleteTextures(1, [self.renderer_id])
