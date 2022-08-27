from .screen import Screen
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import numpy as np

vertex_src = """
# version 330

layout(location = 0) in vec4 a_position;
layout(location = 1) in vec2 a_texture;

void main()
{
    gl_Position = a_position;
}
"""

fragment_src = """
# version 330

out vec4 out_color;

void main()
{    
    out_color = vec4(1.0, 1.0, 1.0, 1.0); 
}
"""


def load_texture(self, filepath):
    pass


class Test(Screen):
    def __init__(self) -> None:
        super().__init__()

    def show(self):
        vertices = np.array([
            -0.5, -0.5, 0, 0.0, 0.0,
            0.5, -0.5, 0, 1.0, 0.0,
            0.5,  0.5, 0, 1.0, 1.0,
            -0.5,  0.5, 0, 0.0, 1.0
        ], dtype=np.float32)

        self.indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

        # quad vao
        self.quad_VAO = glGenVertexArrays(1)
        glBindVertexArray(self.quad_VAO)

        # quad vbo
        quad_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, quad_VBO)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices.nbytes,
            vertices,
            GL_STATIC_DRAW
        )

        # quad ebo
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            GL_STATIC_DRAW
        )

        # quad attribs
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            vertices.itemsize * 5,
            ctypes.c_void_p(0)
        )

        # shader
        self.shader_program = compileProgram(
            compileShader(
                vertex_src,
                GL_VERTEX_SHADER
            ),
            compileShader(
                fragment_src,
                GL_FRAGMENT_SHADER
            ),
        )
        glUseProgram(self.shader_program)

        # toggle context state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, delta):
        glDrawElements(GL_TRIANGLES, len(
            self.indices), GL_UNSIGNED_INT, None)
