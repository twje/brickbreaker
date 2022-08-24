import math
from . import scaling
from OpenGL.GL import *


class FitViewport:
    def __init__(self, world_width: float, world_height: float, camera: "OrthographicCamera") -> None:
        self.world_width = world_width
        self.world_height = world_height
        self.screen_x = 0
        self.screen_y = 0
        self.screen_width = 0
        self.screen_height = 0
        self.camera = camera
        self.scaling = scaling.fit

    def update(self, screen_width: int, screen_height: int, center_camera: bool) -> None:
        """Configures this viewport's screen bounds using the specified screen size."""
        scale_x, scale_y = self.scaling(
            self.world_width,
            self.world_height,
            screen_width,
            screen_height
        )
        viewport_width = math.ceil(scale_x)
        viewport_height = math.ceil(scale_y)
        self.set_screen_bounds(
            int((screen_width - viewport_width)/2),
            int((screen_height - viewport_height)/2),
            viewport_width,
            viewport_height
        )
        self.apply(center_camera)

    def apply(self, center_camera: bool):
        """Applies the viewport to the camera and sets the glViewport."""
        glViewport(
            self.screen_x,
            self.screen_y,
            self.screen_width,
            self.screen_height
        )
        self.camera.viewport_width = self.world_width
        self.camera.viewport_height = self.world_height
        # if (centerCamera) camera.position.set(worldWidth / 2, worldHeight / 2, 0);
        self.camera.update()

    def set_screen_bounds(self, screen_x: int, screen_y: int, screen_width: int, screen_height: int):
        """Sets the viewport's bounds in screen coordinates."""
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_width = screen_width
        self.screen_height = screen_height
