import pyglet

import apheleia.common


@apheleia.common.prototypeable()
class Component:
    def __init__(self, projection, **attrs):
        self.projection = projection
        for attr in attrs:
            setattr(self, attr, attrs[attr])

    def initialize(self):
        """Override to initialize the component.

        This method is called when an instance of the projection is
        created from the datastore.

        """

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        attrs = kwargs.get('attributes', {})
        attrs['needs'] = kwargs.get('needs', [])
        return cls.register(
            kind,
            kwargs.get('fields', []),
            attrs
            )


class TextureComponent(Component):
    def initialize(self):
        self.texture = self.path.resource.texture

    def createGroup(self, parent=None):
        return pyglet.graphics.TextureGroup(self.texture, parent=parent)

    @property
    def texCoords(self):
        return self.texture.tex_coords


class PymunkComponent(Component):
    def initialize(self):
        self.position = self.projection.position
        self._subsystem = self._subsystem.resource
        self.body, self.shape = self._subsystem.createBody(
            self.shape, self.mass, self.shape_data)
        self.body.position = (self.position.x, self.position.y)

    def update_position(self, body, dt):
        body.update_position(body, dt)
        self.position = (body.position.x, body.position.y)


Component.registerImplementation("pymunk", PymunkComponent)
Component.registerImplementation("texture", TextureComponent)