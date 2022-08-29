from OpenGL.GL import *
import numpy as np


class VertexBuffer:
    def __init__(self, data) -> None:
        self.renderer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer_id)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

    def set_data(self, data, size: int):           
        # Explicitly bind becuase VAO stores a VBO indirectly via attrib layouts
        self.bind()
        glBufferSubData(GL_ARRAY_BUFFER, 0, size, data)

    def bind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer_id)

    def unbind(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, [self.renderer_id])
