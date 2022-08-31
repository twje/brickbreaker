from collections import defaultdict


class InputManager:
    def __init__(self) -> None:
        self.cnt_press = defaultdict(bool)
        self.prv_press = defaultdict(bool)

    # ----------
    # Client API
    # ----------
    def is_key_pressed(self, key):
        return self.cnt_press[key] == True and self.prv_press[key] == False

    def is_key_released(self, key):
        return self.cnt_press[key] == False and self.prv_press[key] == True

    def is_key_held(self, key):
        return self.cnt_press[key] == True and self.prv_press[key] == True

    # -------------
    # Framework API
    # -------------
    def set_key_pressed(self, key):
        self.cnt_press[key] = True

    def set_key_released(self, key):
        self.cnt_press[key] = False

    def update(self):
        for key, value in self.cnt_press.items():
            self.prv_press[key] = value
