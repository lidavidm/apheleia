import pyglet


class Game:
    def __init__(self):
        self.manager = None
        self.scene = None
        self.window = None

    def setup(self):
        pass

    def mainloop(self):
        self.window.on_draw = self.draw
        pyglet.app.run()

    def draw(self):
        self.window.clear()
        self.scene.draw()

    def teardown(self):
        pass

    def setScene(self, scene):
        if self.scene:
            self.scene.teardown()
        self.scene = scene
        scene.game = self
        scene.setup()