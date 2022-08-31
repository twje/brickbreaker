from brickbreaker.core.screen import Screen


class ScreenBase(Screen):
    def get_input_processor(self):
        return None
