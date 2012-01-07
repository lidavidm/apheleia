from pyglet import gl
import pymunk


import apheleia.common


@apheleia.common.prototypeable()
class Subsystem:

    class Update:
        FRAME = 'frame'
        INTERVAL = 'interval'


    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.initialize()

    def initialize(self):
        pass

    def begin(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        if 'update_type' not in kwargs:
            kwargs['update_type'] = Subsystem.Update.FRAME
        return cls.register(kind, kwargs['attributes'].keys(),
                            kwargs['attributes'])


class CameraSubsystem(Subsystem):
    def draw(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(-self.x, -self.y, 0)

    def update(self):
        pass


class PymunkSubsystem(Subsystem):
    INERTIAS = {
        "circle": lambda mass, kwargs:
        pymunk.moment_for_circle(mass, 0, kwargs['radius'])
    }

    SHAPES = {
        "circle": pymunk.Circle
    }

    def initialize(self):
        self.space = pymunk.Space()
        self.dt = 1 / 60.0
        self.shapes = []

    def begin(self):
        pass

    def draw(self):
        pass

    def update(self):
        for i in range(60):
            self.space.step(self.dt)

    def createBody(self, shape, mass, shape_data):
        inertia = PymunkSubsystem.inertiaFor(shape, mass, shape_data)
        body = pymunk.Body(mass, inertia)
        shape = PymunkSubsystem.shapeFor(shape, body, shape_data)
        self.space.add(body, shape)
        self.shapes.append(shape)
        return body, shape

    @classmethod
    def inertiaFor(cls, shape, mass, shape_data):
        return cls.INERTIAS[shape](mass, shape_data)

    @classmethod
    def shapeFor(cls, shape, body, shape_data):
        return cls.SHAPES[shape](body, **shape_data)


Subsystem.registerImplementation("camera", CameraSubsystem)
Subsystem.registerImplementation("pymunk", PymunkSubsystem)