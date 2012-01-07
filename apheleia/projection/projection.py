import pyglet

import apheleia.common
from .component import Component


@apheleia.common.prototypeable()
class Projection:
    def __init__(self):
        for component in self.components:
            self.addComponent(component)
        self.initialize()

    def initialize(self):
        pass

    def draw(self):
        pass

    def addComponent(self, component, **attrs):
        cmpInstance = Component.getKind(component)(self, **attrs)
        setattr(self, component, cmpInstance)
        for need in cmpInstance.needs:
            if not self.hasComponent(need):
                self.addComponent(need)
        return cmpInstance

    def hasComponent(self, component):
        return hasattr(self, component)

    @classmethod
    def instance(cls, data):
        instance = cls()

        for component, attrs in data["attributes"]["components"].items():
            if not instance.hasComponent(component):
                instance.addComponent(component, **attrs)
            else:
                component = getattr(instance, component)
                for attr, val in attrs.items():
                    setattr(component, attr, val)

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
