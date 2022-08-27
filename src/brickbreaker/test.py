from .screen import Screen
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
from PIL import Image
import numpy as np

vertex_src = """
# version 330

layout(location = 0) in vec4 a_position;
layout(location = 1) in vec2 a_texture;

out vec2 v_texture;

void main()
{
    gl_Position = a_position;
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{    
    out_color = texture(s_texture, v_texture);
    // out_color = vec4(1.0, 1.0, 1.0, 1.0); 
}
"""


def load_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        image.width,
        image.height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data
    )
    return texture


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
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # quad vbo
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
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

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            2,
            GL_FLOAT,
            GL_FALSE,
            vertices.itemsize * 5,
            ctypes.c_void_p(12)
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

        # texture
        self.texture = glGenTextures(1)
        load_texture("textures/smiley.png", self.texture)

        # toggle context state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, delta):
        glBindVertexArray(self.vao)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glDrawElements(
            GL_TRIANGLES,
            len(self.indices),
            GL_UNSIGNED_INT,
            None
        )
