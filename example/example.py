import pyglet
import apheleia
import apheleia.manager
import apheleia.entity
import apheleia.state


# Replace with a metadata file in the resource manager?
apheleia.entity.Entity._prototyper.paths.append('/base/entities')
apheleia.projection.Component._prototyper.paths.append('/base/components')
apheleia.projection.Projection._prototyper.paths.append('/base/projections')


class Game(apheleia.state.Game):
    def setup(self):
        backend = apheleia.manager.DirectoryBackend('resources/')
        self.manager = apheleia.manager.Manager(backend)
        apheleia.common.prototypeable.defaultManager = self.manager
        self.window = pyglet.window.Window()
        self.setScene(TestScene())


class TestScene(apheleia.state.Scene):
    def setup(self):
        sprite = self.game.manager.load('/vehicles/skirmisher')
        fpsclock = self.game.manager.load('/vehicles/fpsclock')
        self.push(sprite)
        self.push(fpsclock)
        print(self.projections)


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.mainloop()