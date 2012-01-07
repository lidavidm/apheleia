import pyglet
import math
import apheleia
import apheleia.manager
import apheleia.entity
import apheleia.state


# Replace with a metadata file in the resource manager?
apheleia.entity.Entity._prototyper.paths.append('/base/entities')
apheleia.projection.Component._prototyper.paths.append('/base/components')
apheleia.projection.Projection._prototyper.paths.append('/base/projections')
apheleia.event.Event._prototyper.paths.append('/events')
apheleia.state.Subsystem._prototyper.paths.append('/base/subsystems')


class Game(apheleia.state.Game):
    def setup(self):
        backend = apheleia.manager.DirectoryBackend('resources/')
        self.manager = apheleia.manager.Manager(backend)
        apheleia.common.prototypeable.defaultManager = self.manager

        self.eventManager = apheleia.event.EventManager()

        self.window = pyglet.window.Window()
        self.eventManager.provide("window", self.window)

        self.pymunk = apheleia.state.Subsystem.getKind('pymunk')()
        self.manager.provide('/runtime/subsystems/pymunk', self.pymunk)

        self.camera = apheleia.state.Subsystem.getKind('camera')()
        self.camera.x = -20
        self.camera.y = -20
        self.manager.provide("/runtime/subsystems/camera", self.camera)

        self.addSubsystem(self.camera)
        self.addSubsystem(self.pymunk)

        self.setScene(TestScene())


class TestScene(apheleia.state.Scene):
    def setup(self):
        self.game.eventManager.registerHandlers(self)
        self.game.eventManager.attachHandlers(self)
        sprite = self.game.manager.load('/vehicles/skirmisher')
        fpsclock = self.game.manager.load('/vehicles/fpsclock')
        self.push(sprite)
        self.push(fpsclock)
        self.sprite = sprite

    @apheleia.event.reacts("move_up")
    def event_move_up(self, event, state, *args, **kwargs):
        pass

    @apheleia.event.reacts("click")
    def event_click(self, event, state, x, y, button, modifiers):
        x0, y0 = self.sprite.position.x, self.sprite.position.y
        angle = math.atan2(x - x0, y - y0)
        self.sprite.pymunk.body.angle = (math.pi / 2) - angle
        print("Click", state, math.degrees(angle))


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.mainloop()