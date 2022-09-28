from .vertex_array import VertexArray
from .vertex_buffer import VertexBuffer
from .shader import Shader
from .color import Color
from .geometry import Geometry
from OpenGL.GL import *


class ImmediateModeRenderer:
    # vertex element ids

    # layout
    POSITION_ATTRIB = "a_position"
    COLOR_ATTRIB = "a_color"
    TEXCOORD_ATTRIB = "a_tex_coord"

    # uniforms
    PROJECTION_UNIFORM = "u_projTrans"
    U_SAMPLER_UNIFORM = "u_sampler"

    # varyings
    COLOR_VARY = "v_color"
    TEXCOORD_VARY = "v_tex_coord"

    def __init__(self, max_vertices: int, has_colors: bool, num_text_coords: int) -> None:
        # data
        self.max_vertices = max_vertices
        self.geometry: Geometry = self.create_gemoetry(
            max_vertices,
            has_colors,
            num_text_coords
        )

        # shader
        self.shader = Shader(
            self.create_vertex_shader(has_colors, num_text_coords),
            self.create_fragment_shader(has_colors, num_text_coords)
        )

        # vbo
        self.vbo = VertexBuffer(self.geometry.vertices)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(self.vbo, self.geometry.layout, self.shader)

    @classmethod
    def create_gemoetry(cls, max_vertices: int, has_colors: bool, num_text_coords: int):
        gemoetry = Geometry()

        # position
        gemoetry.push_element("position", 2, cls.POSITION_ATTRIB)

        # color (optional)
        if has_colors:
            gemoetry.push_element("color", 4, cls.COLOR_ATTRIB)

        # texture coordinates (optional)
        for index in range(num_text_coords):
            gemoetry.push_element(
                f"texture{index}",
                2,
                f"{cls.TEXCOORD_ATTRIB}{index}"
            )

        gemoetry.finalize(max_vertices)
        return gemoetry

    @classmethod
    def create_vertex_shader(cls, has_colors, num_tex_coords):
        """
        Procedurally generate a Vertex Shader with support for optional colors
        and textures.
        """

        # version
        shader = "# version 330 core\n"

        # layout
        shader += f"in vec4 {cls.POSITION_ATTRIB};\n"
        if has_colors:
            shader += f"in vec4 {cls.COLOR_ATTRIB};\n"
        for index in range(num_tex_coords):
            shader += f"in vec2 {cls.TEXCOORD_ATTRIB}{index};\n"

        # uniforms
        shader += f"uniform mat4 {cls.PROJECTION_UNIFORM};\n"

        # varyings
        if has_colors:
            shader += f"out vec4 {cls.COLOR_VARY};\n"
        for index in range(num_tex_coords):
            shader += f"out vec2 {cls.TEXCOORD_VARY}{index};\n"

        # body
        shader += "void main(){\n"
        shader += f"gl_Position = {cls.PROJECTION_UNIFORM} * {cls.POSITION_ATTRIB};\n"
        if has_colors:
            shader += f"{cls.COLOR_VARY} = {cls.COLOR_ATTRIB};\n"
        for index in range(num_tex_coords):
            shader += f"{cls.TEXCOORD_VARY}{index} = {cls.TEXCOORD_ATTRIB}{index};\n"
        shader += "gl_PointSize = 1.0;\n"
        shader += "}"

        return shader

    @classmethod
    def create_fragment_shader(cls, has_colors, num_tex_coords):
        """
        Procedurally generate a Fragment Shader with support for optional colors
        and textures.
        """

        # version
        shader = "# version 330 core\n"

        # layout
        shader += "out vec4 out_color;\n"

        # uniform
        for index in range(num_tex_coords):
            shader += f"uniform sampler2D {cls.U_SAMPLER_UNIFORM}{index};\n"

        # varyings
        if has_colors:
            shader += f"in vec4 {cls.COLOR_VARY};"
        for index in range(num_tex_coords):
            shader += f"in vec2 {cls.TEXCOORD_VARY}{index};\n"

        # body
        shader += "void main(){\n"
        if has_colors:
            shader += f"out_color = {cls.COLOR_VARY}"
        else:
            shader += f"out_color = vec4(1, 1, 1, 1)"

        if num_tex_coords > 0:
            shader += " * "
        for index in range(num_tex_coords):
            if index == num_tex_coords - 1:
                shader += f"texture({cls.U_SAMPLER_UNIFORM}{index}, {cls.TEXCOORD_VARY}{index})"
            else:
                shader += f"texture({cls.U_SAMPLER_UNIFORM}{index}, {cls.TEXCOORD_VARY}{index}) * "

        shader += ";}\n"

        return shader

    # ----------
    # Client API
    # ----------
    def has_gemeotry_data(self):
        return self.geometry.has_data

    def free_vertices_count(self):
        return self.max_vertices - self.geometry.vertex_count

    def begin(self, proj_model_view, primitive_type):
        self.proj_model_view = proj_model_view
        self.primitive_type = primitive_type
        self.shader.bind()

    def end(self):
        self.flush()

    def flush(self):
        if not self.geometry.has_data:
            return

        self.vao.bind()
        self.vbo.set_data(
            self.geometry.vertices,
            self.geometry.size
        )

        self.shader.set_uniform_mat4f("u_projTrans", self.proj_model_view)
        glDrawArrays(self.primitive_type, 0, self.geometry.vertex_count)
        self.geometry.reset()

    def color(self, color: Color):
        self.geometry.push_data("color", [color.r, color.g, color.b, color.a])

    def position(self, x: float, y: float):
        self.geometry.push_data("position", [x, y])

    def texture_coordinate(self, index: int, u: float, v: float):
        self.geometry.push_data(f"texture{index}", [u, v])

    def new_vertex(self):
        self.geometry.next()

    def dispose(self):
        self.vao.delete()
        self.vbo.delete()
        self.shader.delete()
