from .screen import Screen
from OpenGL.GL.shaders import compileProgram, compileShader
from .shader import Shader
from OpenGL.GL import *
from PIL import Image
import numpy as np


vertex_src = """
#version 330 core
in vec4 a_position;
in vec4 a_color;
in vec2 a_texture;

out vec4 v_color;
out vec2 v_texture;

void main()
{
	gl_Position = a_position;
	v_color = a_color;
	v_texture = a_texture;
}
"""

fragment_src = """
#version 330 core
out vec4 out_color;

in vec4 v_color;
in vec2 v_texture;

uniform sampler2D s_texture;

void main()
{	
    out_color = v_color * texture(s_texture, v_texture);
};
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
            -0.5, -0.5, 0, 1.0, 1.0, 1.0, 1.0, 0, 0,
            0.5, -0.5, 0, 1.0, 1.0, 1.0, 1.0, 1, 0,
            0.5,  0.5, 0, 1.0, 1.0, 1.0, 1.0, 1, 1,
            -0.5,  0.5, 0, 1.0, 1.0, 1.0, 1.0, 0, 1
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

        # shader
        self.shader = Shader(vertex_src, fragment_src, [
                             "a_color", "a_texture", "a_position"])

        # self.shader_program = compileProgram(
        #     compileShader(
        #         vertex_src,
        #         GL_VERTEX_SHADER
        #     ),
        #     compileShader(
        #         fragment_src,
        #         GL_FRAGMENT_SHADER
        #     ),
        # )
        # glUseProgram(self.shader_program)

        # texture
        self.texture = glGenTextures(1)

        # glActiveTexture(GL_TEXTURE0)
        load_texture("textures/smiley.png", self.texture)

        loc1 = glGetAttribLocation(self.shader.renderer_id, "a_position")
        loc2 = glGetAttribLocation(self.shader.renderer_id, "a_color")
        loc3 = glGetAttribLocation(self.shader.renderer_id, "a_texture")

        print(loc1, loc2, loc3)

        # loc1 = glGetAttribLocation(self.shader_program, "a_position")
        # loc2 = glGetAttribLocation(self.shader_program, "a_color")
        # loc3 = glGetAttribLocation(self.shader_program, "a_texture")
        # print(loc1)
        # print(loc2)
        # print(loc3)

        # glActiveTexture(GL_TEXTURE1)
        # quad attribs
        glEnableVertexAttribArray(loc1)
        glVertexAttribPointer(
            loc1,
            3,
            GL_FLOAT,
            GL_FALSE,
            vertices.itemsize * 9,
            ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(loc2)
        glVertexAttribPointer(
            loc2,
            4,
            GL_FLOAT,
            GL_FALSE,
            vertices.itemsize * 9,
            ctypes.c_void_p(12)
        )
        glEnableVertexAttribArray(loc3)
        glVertexAttribPointer(
            loc3,
            2,
            GL_FLOAT,
            GL_FALSE,
            vertices.itemsize * 9,
            ctypes.c_void_p(28)
        )

        # toggle context state
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render(self, delta):
        glBindVertexArray(self.vao)
        glDrawElements(
            GL_TRIANGLES,
            len(self.indices),
            GL_UNSIGNED_INT,
            None
        )
