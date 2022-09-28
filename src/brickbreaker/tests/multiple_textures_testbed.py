"""
Test different OpenGL methods for rendering multiple textures
Test:
    - MultiTextureTest
      - Any uniform sampler or image variable declared without a binding qualifier is initially bound to unit zero.
    - MultiTextureArrayTest
      - All each entry of uniform sampler array is bound to unit zero.
"""


from brickbreaker.core.texture_region import TextureRegion
from brickbreaker.core.application_listener import ApplicationListener
from brickbreaker.core.index_buffer import IndexBuffer
from brickbreaker.core.vertex_buffer import VertexBuffer
from brickbreaker.core.vertex_buffer_layout import VertexBufferLayout
from brickbreaker.core.shader import Shader
from brickbreaker.core.vertex_array import VertexArray
from brickbreaker.core.texture import Texture
from brickbreaker.core.color import Color
from brickbreaker.core.shape_type import ShapeType
from OpenGL.GL import *
import numpy as np
import pyrr

# todo
# test shape ImmediateModeRenderer
# test Renderer and revise check method
# add support for glDrawElements to reduce vertex count
# size for point and circle (particle system)
# check in code
# adapt to be used by sprite batch

__all__ = [
    "MultiTextureTest",
    "MultiTextureArrayTest",
    "ProgramaticShader",
    "TestImmediateModeRenderer"
]


class Geometry:
    def __init__(self) -> None:
        self.element_lookup = {}
        self.elements = []
        self.layout = VertexBufferLayout()
        self.index = 0
        self.has_data = False
        self.vertices = None

    @property
    def vertex_count(self):
        return self.index

    @property
    def size(self):
        return self.vertex_count * self.layout.stride

    def push_element(self, name: str, count: int, layout_id: str = None):
        self.element_lookup[name] = len(self.elements)
        self.elements.append((self.layout.count, layout_id))
        self.layout.push_float(count, layout_id)

    def finalize(self, max_vertices: int):
        self.vertices = np.zeros(
            max_vertices * self.layout.count,
            dtype=np.float32
        )

    def push_data(self, name: str, data: list):
        assert len(data) > 0

        if name not in self.element_lookup:
            return

        count, _ = self.elements[self.element_lookup[name]]
        for index, item in enumerate(data):
            offset = self.index * self.layout.count + count
            self.vertices[offset + index] = item

        self.has_data = True

    def next(self):
        self.index += 1

    def reset(self):
        self.index = 0
        self.has_data = False


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


class ShapeRenderer:
    ShapeType = ShapeType

    def __init__(self) -> None:
        self.shape_type = None
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, 0)

    def set_projection_matrix(self, matrix):
        self.projection = matrix

    def begin(self, shape_type):
        assert self.shape_type is None
        self.shape_type = shape_type
        self.renderer.begin(self.projection, self.shape_type)

    def end(self):
        assert self.shape_type is not None
        self.renderer.end()
        self.shape_type = None

    def check(self, preferred: ShapeType, other: ShapeType, new_vertices: int):
        assert self.shape_type is not None

        if self.shape_type != preferred and self.shape_type != other:
            self.end()
            self.begin(preferred)
        elif self.renderer.free_vertices_count() > new_vertices:
            shape_type = self.shape_type
            self.end()
            self.begin(shape_type)

    def rect(self, x: float, y: float, width: float, height: float):
        self.check(ShapeType.Line, ShapeType.Filled, 8)
        if self.shape_type == ShapeType.Line:
            # line 1
            self.add_vertex(x, y)
            self.add_vertex(x + width, y)

            # line 2
            self.add_vertex(x + width, y)
            self.add_vertex(x + width, y + height)

            # line 3
            self.add_vertex(x + width, y + height)
            self.add_vertex(x, y + height)

            # line 4
            self.add_vertex(x, y + height)
            self.add_vertex(x, y)
        else:
            # triangle 1
            self.add_vertex(x, y)
            self.add_vertex(x + width, y)
            self.add_vertex(x + width, y + height)

            # triangle 2
            self.add_vertex(x + width, y + height)
            self.add_vertex(x, y + height)
            self.add_vertex(x, y)

    def line(self, x1: float, y1: float, x2: float, y2: float):
        self.check(ShapeType.Line, None, 2)
        self.add_vertex(x1, y1)
        self.add_vertex(x2, y2)

    def polygon(self, vertices):
        # Polygons must contain at least 3 points.
        assert len(vertices) >= 6
        # Polygons must have an even number of vertices.
        assert len(vertices) % 2 == 0

        self.check(ShapeType.Line, None, len(vertices))

        first_x = vertices[0]
        first_y = vertices[1]
        for index in range(0, len(vertices), 2):
            x1 = vertices[index]
            y1 = vertices[index + 1]

            if index + 2 >= len(vertices):
                x2 = first_x
                y2 = first_y
            else:
                x2 = vertices[index + 2]
                y2 = vertices[index + 3]

            self.add_vertex(x1, y1)
            self.add_vertex(x2, y2)

    def add_vertex(self, x: float, y: float):
        self.renderer.position(x, y)
        self.renderer.color(self.color)
        self.renderer.new_vertex()

    def dispose(self):
        self.renderer.dispose()


class SpriteBatch:
    def __init__(self) -> None:
        self.projection = None
        self.color = Color()
        self.renderer = ImmediateModeRenderer(5000, True, 1)
        self.drawing = False
        self.last_texture = None

    def set_projection_matrix(self, matrix):
        self.projection = matrix

    def begin(self):
        assert not self.drawing
        self.renderer.begin(self.projection, ShapeType.Filled)
        self.drawing = True

    def end(self):
        assert self.drawing
        self.flush()
        self.last_texture = None
        self.drawing = False

    def switch_texture(self, texture: Texture):
        self.flush()
        self.last_texture = texture

    def flush(self):
        if self.renderer.has_gemeotry_data():
            self.last_texture.bind()
            self.renderer.end()

    def check(self, texture: Texture, new_vertices: int):
        if texture is not self.last_texture:
            self.switch_texture(texture)
        elif new_vertices > self.renderer.free_vertices_count():
            self.flush()

    def draw_texture(self, texture: Texture, x: float, y: float, width: float, height: float):
        self.draw_texture_uv(
            texture,
            x,
            y,
            width,
            height,
            0,
            0,
            1,
            1
        )

    def draw_texture_region(self, texture_region: TextureRegion, x: float, y: float, width: float, height: float):
        u1, v1, u2, v2 = texture_region.uv()
        self.draw_texture_uv(
            texture_region.texture,
            x,
            y,
            width,
            height,
            u1,
            v1,
            u2,
            v2
        )

    def draw_texture_uv(self, texture: Texture, x: float, y: float, width: float, height: float, u1: float, v1: float, u2: float, v2: float):
        self.check(texture, 6)

        # triangle 1
        self.add_vertex(x, y, u1, v1)
        self.add_vertex(x + width, y, u2, v1)
        self.add_vertex(x + width, y + height, u2, v2)

        # triangle 2
        self.add_vertex(x + width, y + height, u2, v2)
        self.add_vertex(x, y + height, u1, v2)
        self.add_vertex(x, y, u1, v1)

    def add_vertex(self, x: float, y: float, u: float, v: float):
        self.renderer.color(self.color)
        self.renderer.position(x, y)
        self.renderer.texture_coordinate(0, u, v)
        self.renderer.new_vertex()

    def dispose(self):
        self.renderer.dispose()

from brickbreaker.core.texture_atlas import TextureAtlas

class TestImmediateModeRenderer(ApplicationListener):
    def create(self):
        # shader uniforms
        self.proj_model_view = pyrr.matrix44.create_orthogonal_projection(
            -1,
            1,
            -1,
            1,
            0,
            100
        )
        self.shape_renderer = SpriteBatch()
        self.texture_atlas = TextureAtlas ("assets/gameplay/gameplay.atlas")

    def render(self, delta):
        self.shape_renderer.set_projection_matrix(self.proj_model_view)
        self.shape_renderer.begin()
        self.shape_renderer.draw_texture_region(self.texture_atlas.find_region("ball"), 0, 0, 0.5, 0.5)
        self.shape_renderer.end()

    def create_octagon(self, origin_x: float, origin_y: float, radius: float, vertex_count: float):
        import math
        vertices = []
        for index in range(0, vertex_count):
            x = origin_x + radius * \
                math.cos(math.radians(360 * index/vertex_count))
            y = origin_y + radius * \
                math.sin(math.radians(360 * index/vertex_count))
            vertices.extend([x, y])

        return vertices


class ProgramaticShader(ApplicationListener):
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

    def create(self):
        glEnable(GL_PROGRAM_POINT_SIZE)

        has_colors = True
        num_text_coords = 1

        positions = np.array([
            # position only
            # -0.5, -0.5,
            # 0.5, -0.5,
            # 0.5,  0.5,
            # -0.5,  0.5,

            # no color, 1 tex
            # -0.5, -0.5, 0, 0,
            # 0.5, -0.5, 1, 0,
            # 0.5,  0.5, 1, 1,
            # -0.5,  0.5, 0, 1,

            # no color, 2 tex
            # -0.5, -0.5, 0, 0, 0, 0,
            # 0.5, -0.5, 1, 0, 1, 0,
            # 0.5,  0.5, 1, 1, 1, 1,
            # -0.5,  0.5, 0, 1, 0, 1,

            # color
            # -0.5, -0.5, 1.0, 1.0, 1.0, 1.0,
            # 0.5, -0.5,  1.0, 1.0, 1.0, 1.0,
            # 0.5,  0.5,  1.0, 1.0, 1.0, 1.0,
            # -0.5,  0.5,  1.0, 1.0, 1.0, 1.0,

            # color, 1 tex
            -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            0.5, -0.5,  1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            0.5,  0.5,  1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            -0.5,  0.5,  1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ], dtype=np.float32)

        indicies = np.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=np.uint32)

        # shader
        self.shader = Shader(
            self.create_vertex_shader(has_colors, num_text_coords),
            self.create_fragment_shader(has_colors, num_text_coords),
        )

        # vbo
        vbo = VertexBuffer(positions)

        # vbo layout
        vbo_layout = VertexBufferLayout()
        vbo_layout.push_float(2, self.POSITION_ATTRIB)
        if has_colors:
            vbo_layout.push_float(4, self.COLOR_ATTRIB)
        for index in range(num_text_coords):
            vbo_layout.push_float(2, f"{self.TEXCOORD_ATTRIB}{index}")

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(vbo, vbo_layout, self.shader)

        # ibo
        self.ibo = IndexBuffer(indicies)

        # shader uniforms
        proj_model_view = pyrr.matrix44.create_orthogonal_projection(
            -1,
            1,
            -1,
            1,
            0,
            100
        )
        self.shader.set_uniform_mat4f("u_projTrans", proj_model_view)

        if has_colors:
            vbo_layout.push_float(4, self.COLOR_ATTRIB)

        for index in range(num_text_coords):
            self.shader.set_uniform_i(
                f"{self.U_SAMPLER_UNIFORM}{index}",
                index
            )

        # textures
        self.texture1 = Texture("assets/yellow.png")
        # self.texture2 = Texture("assets/red.png")

        self.texture1.bind(0)
        # self.texture2.bind(1)

    def render(self, delta):
        self.shader.bind()
        self.vao.bind()
        self.ibo.bind()
        glDrawElements(GL_POINTS, self.ibo.count, GL_UNSIGNED_INT, None)

    @ classmethod
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


class MultiTextureTest(ApplicationListener):
    def create(self):
        vertex_src = """
            # version 330 core

            layout(location = 0) in vec3 a_position;
            layout(location = 1) in vec2 texCoord;

            out vec2 v_TexCoord;

            void main()
            {
                gl_Position = vec4(a_position, 1.0);
                v_TexCoord = texCoord;
            }
        """

        fragment_src = """
            # version 330 core

            layout(location = 0) out vec4 color;

            in vec2 v_TexCoord;
            uniform sampler2D u_Texture1;
            uniform sampler2D u_Texture2;

            void main()
            {
                vec4 textColor = texture(u_Texture2, v_TexCoord);
	            color = textColor;
            }
        """

        positions = np.array([
            -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, 1.0, 0.0,
            0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5, 0.0, 1.0
        ], dtype=np.float32)

        indicies = np.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=np.uint32)

        # shader
        self.shader = Shader(vertex_src, fragment_src)

        # vbo
        vbo = VertexBuffer(positions)

        # vbo layout
        vbo_layout = VertexBufferLayout()
        vbo_layout.push_float(2)
        vbo_layout.push_float(2)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(vbo, vbo_layout, self.shader)

        # ibo
        self.ibo = IndexBuffer(indicies)

        # textures
        self.texture1 = Texture("assets/yellow.png")
        self.texture2 = Texture("assets/red.png")

    def render(self, delta):
        self.shader.bind()
        self.vao.bind()
        self.ibo.bind()
        glDrawElements(GL_TRIANGLES, self.ibo.count, GL_UNSIGNED_INT, None)


class MultiTextureArrayTest(ApplicationListener):
    def create(self):
        vertex_src = """
            # version 330 core

            layout(location = 0) in vec3 a_position;
            layout(location = 1) in vec2 texCoord;

            out vec2 v_TexCoord;

            void main()
            {
                gl_Position = vec4(a_position, 1.0);
                v_TexCoord = texCoord;
            }
        """

        fragment_src = """
            # version 330 core

            layout(location = 0) out vec4 color;

            in vec2 v_TexCoord;
            uniform sampler2D u_Textures[2];

            void main()
            {
                vec4 textColor = texture(u_Textures[1], v_TexCoord);
	            color = textColor;
            }
        """

        positions = np.array([
            -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, 1.0, 0.0,
            0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5, 0.0, 1.0
        ], dtype=np.float32)

        indicies = np.array([
            0, 1, 2,
            2, 3, 0,
        ], dtype=np.uint32)

        # shader
        self.shader = Shader(vertex_src, fragment_src)

        # vbo
        vbo = VertexBuffer(positions)

        # vbo layout
        vbo_layout = VertexBufferLayout()
        vbo_layout.push_float(2)
        vbo_layout.push_float(2)

        # vao
        self.vao = VertexArray()
        self.vao.add_buffer(vbo, vbo_layout, self.shader)

        # ibo
        self.ibo = IndexBuffer(indicies)

        # textures
        self.texture1 = Texture("assets/yellow.png")
        self.texture2 = Texture("assets/red.png")

        # set sampler values - default is 0
        samplers = [1, 0]
        self.shader.set_uniform_iv("u_Textures", samplers)

        self.texture1.bind(0)
        self.texture2.bind(1)

    def render(self, delta):
        self.shader.bind()
        self.vao.bind()
        self.ibo.bind()
        glDrawElements(GL_TRIANGLES, self.ibo.count, GL_UNSIGNED_INT, None)
