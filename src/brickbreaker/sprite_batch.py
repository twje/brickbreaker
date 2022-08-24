from .vertex_buffer_layout import VertexBufferLayout
from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .index_buffer import IndexBuffer
from .shader import Shader
import numpy as np
from OpenGL.GL import *

vertex_src = """
#version 330 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;

out vec4 v_Color;

uniform mat4 u_projTrans;

void main()
{
   gl_Position = u_projTrans * position;
   v_Color = color;
};
"""

fragment_src = """
#version 330 core

layout(location = 0) out vec4 color;

in vec4 v_Color;

void main()
{	
	color = v_Color;
};
"""


class SpriteBatch:
    def __init__(self) -> None:
        # data
        positions = np.array([
            -1.0, -1.0, 0.18, 0.6, 0.96, 1.0,
            1.0, -1.0, 0.18, 0.6, 0.96, 1.0,
            1.0,  1.0, 0.18, 0.6, 0.96, 1.0,
            -1.0,  1.0, 0.18, 0.6, 0.0, 1.0,
        ], dtype=np.float32)

        indicies = np.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=np.uint32)

        # vbo
        vbo = VertexBuffer(positions)
        vbo_layout = VertexBufferLayout()
        vbo_layout.push_float(2)
        vbo_layout.push_float(4)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(vbo, vbo_layout)

        # ibo
        self.ibo = IndexBuffer(indicies)

        # shader
        self.shader = Shader(vertex_src, fragment_src)

    def set_projection_matrix(self, matrix):
        self.shader.set_uniform_mat4f("u_projTrans", matrix)

    def begin(self):
        pass

    def end(self):
        pass

    def draw(self, texture):
        self.shader.bind()
        self.vao.bind()
        self.ibo.bind()
        glDrawElements(GL_TRIANGLES, self.ibo.count, GL_UNSIGNED_INT, None)
