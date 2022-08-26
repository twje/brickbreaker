from brickbreaker.shader import Shader
from .vertex_buffer import VertexBuffer
from .vertex_buffer_layout import VertexBufferLayout
from .vertex_buffer_layout import VertexBufferElement
from OpenGL.GL import *


class VertexArray:
    def __init__(self) -> None:
        self.renderer_id = glGenVertexArrays(1)
        glBindVertexArray(self.renderer_id)

    def add_buffer(self, vertex_buffer: VertexBuffer, layout: VertexBufferLayout, shader: Shader) -> None:
        self.bind()
        vertex_buffer.bind()
        offset = 0
        for index, element in enumerate(layout.elements):
            attribute_loc = shader.get_attribute_location(element.name, index)
            glEnableVertexAttribArray(attribute_loc)
            glVertexAttribPointer(
                attribute_loc,
                element.count,
                element.type,
                element.normalized,
                layout.stride,
                ctypes.c_void_p(offset)
            )
            offset += element.count * \
                VertexBufferElement.get_size_of_type(element.type)

    def bind(self) -> None:
        glBindVertexArray(self.renderer_id)

    def unbind(self) -> None:
        glBindVertexArray(0)

    def delete(self):
        glDeleteVertexArrays(1, [self.renderer_id])
