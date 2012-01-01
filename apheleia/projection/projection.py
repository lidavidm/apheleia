import pyglet

import apheleia.common
from .component import Component


@apheleia.common.prototypeable()
class Projection:
    def __init__(self):
        for component in self.components:
            setattr(self, component, Component.getKind(component)())
        self.initialize()

    def initialize(self):
        pass

    def draw(self):
        pass

    @classmethod
    def instance(cls, data):
        instance = cls()
        for component, attrs in data["attributes"]["components"].items():
            component = getattr(instance, component)
            for attr, value in attrs.items():
                setattr(component, attr, value)
        return instance

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        return cls.register(
            kind,
            kwargs['attributes']['components'],
            {'components': kwargs['attributes']['components']})


class SpriteProjection(Projection):
    def draw(self):
        self.texture.path.resource.blit(self.position.x, self.position.y)


class FPSProjection(Projection):
    def initialize(self):
        self.clock = pyglet.clock.ClockDisplay()

    def draw(self):
        self.clock.draw()

Projection.registerImplementation("sprite", SpriteProjection)
Projection.registerImplementation("fpsclock", FPSProjection)
