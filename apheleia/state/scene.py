import weakref
import pyglet


class Layer:
    def __init__(self, z=0):
        self.z = z
        self.projections = []
        self.group = pyglet.graphics.OrderedGroup(z)

    def push(self, projection):
        self.projections.append(projection)


class Scene:
    def __init__(self):
        self.game = None
        self.name = self.__class__.__name__
        self.layers = [Layer()]
        self.projections = {}
        self.batch = pyglet.graphics.Batch()

    def push(self, projection, layer=-1, name=None):
        projection.initialize(self.batch, self.layers[layer].group)
        self.layers[layer].push(projection)
        name = name or (projection.prototypeName +
                        str(len(self.projections)))
        self.projections[name] = weakref.ref(projection)

    def draw(self):
        self.batch.draw()
        for projection in self.layers[-1].projections:
            if projection.MANUAL_DRAW:
                projection.draw()
