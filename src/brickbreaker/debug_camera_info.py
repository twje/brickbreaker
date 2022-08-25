class DebugCameraInfo:
    DEFAULT_MOVE_SPEED = 20.0

    def __init__(self) -> None:
        self.setup_defaults()

    def setup_defaults(self):
        self.move_speed = self.DEFAULT_MOVE_SPEED

    def is_left_pressed(self):
        return False

    def is_right_pressed(self):
        return False

    def is_up_pressed(self):
        return False

    def is_down_pressed(self):
        return False

    