class DebugCameraInfo:
    DEFAULT_MOVE_SPEED = 20.0
    DEFAULT_ZOOM_SPEED = 2.0
    DEFAULT_MAX_ZOOM_IN = 0.25
    DEFAULT_MAX_ZOOM_OUT = 30

    def __init__(self) -> None:
        self.setup_defaults()

    def setup_defaults(self):
        self.move_speed = self.DEFAULT_MOVE_SPEED
        self.zoom_speed = self.DEFAULT_ZOOM_SPEED
        self.max_zoom_in = self.DEFAULT_MAX_ZOOM_IN
        self.max_zoom_out = self.DEFAULT_MAX_ZOOM_OUT

    def is_left_pressed(self):
        return False

    def is_right_pressed(self):
        return False

    def is_up_pressed(self):
        return False

    def is_down_pressed(self):
        return False

    def is_zoom_in_pressed(self):
        return False

    def is_zoom_out_pressed(self):
        return False

    def is_reset_pressed(self):
        return False

    def is_log_pressed(self):
        return False
