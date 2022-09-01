from glfw import get_time


class Clock:
    def __init__(self) -> None:
        self.start_time = get_time()

    @property
    def delta(self):
        current_time = get_time()
        delta = get_time() - current_time
        self.start_time = current_time
        return delta * 1000
