from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *


class Shader:
    def __init__(self, vertex_src, fragment_src) -> None:
        self.uniform_location_cache = dict()
        self.renderer_id = compileProgram(
            compileShader(
                vertex_src,
                GL_VERTEX_SHADER
            ),
            compileShader(
                fragment_src,
                GL_FRAGMENT_SHADER
            ),
        )
        glUseProgram(self.renderer_id)

    def bind(self):
        glUseProgram(self.renderer_id)

    def unbind(self):
        glUseProgram(0)

    def delete(self):
        glDeleteProgram(self.renderer_id)

    def set_uniform_mat4f(self, name: str, matrix):
        glUniformMatrix4fv(self.get_uniform_location(name),
                           1, GL_FALSE, matrix)

    def get_uniform_location(self, name: str) -> int:
        if name in self.uniform_location_cache:
            return self.uniform_location_cache[name]

        location = glGetUniformLocation(self.renderer_id, name)
        if location == -1:
            print(f"Warning: uniform {name} doesn't exist")

        self.uniform_location_cache[name] = location
        return location
