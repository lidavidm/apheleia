import pyglet


class Game:
    def __init__(self):
        self.manager = None
        self.scene = None
        self.window = None
        self.subsystems = []

    def setup(self):
        pass

    def mainloop(self):
        self.window.on_draw = self.draw

        for subsystem in self.subsystems:
            subsystem.begin()

        pyglet.app.run()

    def draw(self):
        self.window.clear()

        for subsystem in self.subsystems:
            if subsystem.update_type == subsystem.Update.FRAME:
                subsystem.update()
            subsystem.draw()

        self.scene.draw()

    def teardown(self):
        pass

    def setScene(self, scene):
        if self.scene:
            self.scene.teardown()
        self.scene = scene
        scene.game = self
        scene.setup()

    def addSubsystem(self, subsystem):
        self.subsystems.append(subsystem)

        if subsystem.update_type == subsystem.Update.INTERVAL:
            pyglet.clock.schedule_interval(
                subsystem.update,
                subsystem.update_interval)

    def removeSubsystem(self, subsystem):
        self.subsystems.remove(subsystem)
        pyglet.clock.unschedule(subsystem.update)
