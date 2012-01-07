import pyglet

import apheleia.common
from .component import Component


@apheleia.common.prototypeable()
class Projection:
    MANUAL_DRAW = False

    def __init__(self):
        for component in self.components:
            self.addComponent(component, _init=False)

    def initialize(self):
        """Override to initialize the projection.

        This method is called when the projection is added to a scene,
        after all components have been added.

        """
        pass

    def draw(self):
        pass

    def addComponent(self, component, _init=False, **attrs):
        cmpInstance = Component.getKind(component)(self, **attrs)
        setattr(self, component, cmpInstance)
        for need in cmpInstance.needs:
            if not self.hasComponent(need):
                self.addComponent(need)

        if _init:
            cmpInstance.initialize()

        return cmpInstance

    def hasComponent(self, component):
        return hasattr(self, component)

    @classmethod
    def instance(cls, data):
        instance = cls()

        for component, attrs in data["attributes"]["components"].items():
            if not instance.hasComponent(component):
                instance.addComponent(component, _init=True, **attrs)
            else:
                component = getattr(instance, component)
                for attr, val in attrs.items():
                    setattr(component, attr, val)
                component.initialize()

        return instance

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        return cls.register(
            kind,
            kwargs['attributes']['components'],
            {'components': kwargs['attributes']['components']})


class SpriteProjection(Projection):
    def initialize(self, batch, group):
        x, y = self.position.x, self.position.y
        width, height = self.texture.width, self.texture.height
        group = self.texture.createGroup(group)
        self.vlist = batch.add(
            4, pyglet.gl.GL_QUADS, group,
            ('v2f', [x, y,
                     x + width, y,
                     x + width, y + height,
                     x, y + height]),
            ('t3f', self.texture.texCoords)
        )


class FPSProjection(Projection):
    MANUAL_DRAW = True

    def initialize(self, batch, group):
        self.clock = pyglet.clock.ClockDisplay()

    def draw(self):
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glPushMatrix()
        pyglet.gl.glLoadIdentity()
        self.clock.draw()
        pyglet.gl.glPopMatrix()

Projection.registerImplementation("sprite", SpriteProjection)
Projection.registerImplementation("fpsclock", FPSProjection)
