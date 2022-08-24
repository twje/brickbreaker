class ApplicationListener:
    """
    Application lifecycle modeled on LibGDX Application lifecycle
    """

    def create(self):
        """Called when the Application is first created."""
        pass

    def dispose(self):
        """Called when the Application is destroyed."""
        pass

    def pause(self):
        """Called when the Application is paused, usually when it's not active or visible on-screen."""
        pass

    def render(self, delta):
        """Called when the Application should render itself."""
        pass

    def resize(self, width, height):
        """Called when the Application is resized."""
        pass

    def resume(self):
        """Called when the Application is resumed from a paused state, usually when it regains focus."""
        pass
