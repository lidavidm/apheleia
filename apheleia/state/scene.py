import weakref


class Layer:
    def __init__(self, z=0):
        self.z = z
        self.projections = []

    def push(self, projection):
        self.projections.append(projection)


class Scene:
    def __init__(self):
        self.game = None
        self.name = self.__class__.__name__
        self.layers = [Layer()]
        self.projections = {}

    def push(self, projection, layer=-1, name=None):
        self.layers[layer].push(projection)
        name = name or (projection.prototypeName +
                        str(len(self.projections)))
        self.projections[name] = weakref.ref(projection)

    def draw(self):
        for layer in self.layers:
            for projection in layer.projections:
                projection.draw()