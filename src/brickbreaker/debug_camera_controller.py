from pyrr import Vector3
from .debug_camera_info import DebugCameraInfo


class DebugCameraController:
    def __init__(self) -> None:
        self.info = DebugCameraInfo()
        self.position = Vector3()
        self.start_position = Vector3()
        self.zoom = 1.0

    def handle_debug_input(self, delta: float):
        move_speed = self.info.move_speed * delta
        zoom_speed = self.info.zoom_speed * delta

        if self.info.is_left_pressed():
            self.move_left(move_speed)

        if self.info.is_right_pressed():
            self.move_right(move_speed)

        if self.info.is_up_pressed():
            self.move_up(move_speed)

        if self.info.is_down_pressed():
            self.move_down(move_speed)

        if self.info.is_zoom_in_pressed():
            self.zoom_in(zoom_speed)

        if self.info.is_zoom_out_pressed():
            self.zoom_out(zoom_speed)

        if self.info.is_reset_pressed():
            self.reset()

        if self.info.is_log_pressed():
            self.log_debug()

    def apply_to(self, camera) -> None:
        camera.set_position(self.position.x, self.position.y)
        camera.zoom = self.zoom
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

    def zoom_in(self, speed):
        self.set_zoom(self.zoom - speed)

    def zoom_out(self, speed):
        self.set_zoom(self.zoom + speed)

    def set_zoom(self, value: float):
        self.zoom = max(min(value, self.info.max_zoom_out),
                        self.info.max_zoom_in)

    def set_start_position(self, x, y):
        self.start_position.x = x
        self.start_position.y = y
        self.position.x = x
        self.position.y = y

    def reset(self):
        self.position.x = self.start_position.x
        self.position.y = self.start_position.y
        self.zoom = 1.0

    def log_debug(self):
        print(f"position={self.position}, zoom={self.zoom}")
