from OpenGL.GL import *
import numpy as np


class IndexBuffer:
    def __init__(self, data) -> None:
        self.count = len(data)
        self.renderer_id = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.renderer_id)        
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER, 
            data.nbytes, 
            data, 
            GL_STATIC_DRAW
        )

    def bind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.renderer_id)

    def unbind(self) -> None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def delete(self):
        glDeleteBuffers(1, self.renderer_id)
