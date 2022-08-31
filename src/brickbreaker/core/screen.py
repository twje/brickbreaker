class Screen:
    def show(self):
        """Called when this screen becomes the current screen for a Game."""

    def render(self, delta: float):
        """Called when the screen should render itself."""

    def resize(self, width: int, height: int):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def hide(self):
        """Called when this screen is no longer the current screen for a Game."""

    def dispose(self):
        """Called when this screen should release all resources."""
