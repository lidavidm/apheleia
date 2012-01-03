import pyglet
import apheleia
import apheleia.manager
import apheleia.entity
import apheleia.state


# Replace with a metadata file in the resource manager?
apheleia.entity.Entity._prototyper.paths.append('/base/entities')
apheleia.projection.Component._prototyper.paths.append('/base/components')
apheleia.projection.Projection._prototyper.paths.append('/base/projections')
apheleia.event.Event._prototyper.paths.append('/events')


class Game(apheleia.state.Game):
    def setup(self):
        backend = apheleia.manager.DirectoryBackend('resources/')
        self.manager = apheleia.manager.Manager(backend)
        self.eventManager = apheleia.event.EventManager()
        apheleia.common.prototypeable.defaultManager = self.manager
        self.window = pyglet.window.Window()
        self.eventManager.provide("window", self.window)
        self.setScene(TestScene())


class TestScene(apheleia.state.Scene):
    def setup(self):
        self.game.eventManager.registerHandlers(self)
        self.game.eventManager.attachHandlers(self)
        sprite = self.game.manager.load('/vehicles/skirmisher')
        fpsclock = self.game.manager.load('/vehicles/fpsclock')
        self.push(sprite)
        self.push(fpsclock)

    @apheleia.event.reacts("move_up")
    def event_move_up(self, event, state, *args, **kwargs):
        pass

    @apheleia.event.reacts("click")
    def event_move_up(self, event, state, *args, **kwargs):
        print("Click", state)


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.mainloop()