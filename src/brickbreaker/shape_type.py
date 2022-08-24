from enum import IntEnum
from OpenGL.GL import *


class ShapeType(IntEnum):
    Line = GL_LINES
    Filled = GL_TRIANGLES
