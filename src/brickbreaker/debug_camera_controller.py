from pyrr import Vector3
from .debug_camera_info import DebugCameraInfo


class DebugCameraController:
    def __init__(self) -> None:
        self.info = DebugCameraInfo()
        self.position = Vector3()

    def handle_debug_input(self, delta: float):
        move_speed = self.info.move_speed * delta
        if self.info.is_left_pressed():
            self.move_left(move_speed)

        if self.info.is_right_pressed():
            self.move_right(move_speed)

        if self.info.is_up_pressed():
            self.move_up(move_speed)

        if self.info.is_down_pressed():
            self.move_down(move_speed)

    def apply_to(self, camera) -> None:
        camera.set_position(self.position.x, self.position.y)
        camera.update()

    def move_left(self, speed: float):
        self.move_camera(-speed, 0)

    def move_right(self, speed: float):
        self.move_camera(speed, 0)

    def move_up(self, speed: float):
        self.move_camera(0, speed)

    def move_down(self, speed: float):
        self.move_camera(0, -speed)

    def move_camera(self, x_speed: float, y_speed: float):
        self.position.x += x_speed
        self.position.y += y_speed
