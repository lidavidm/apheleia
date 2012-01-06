from pyglet import gl


import apheleia.common


@apheleia.common.prototypeable()
class Subsystem:

    class Update:
        FRAME = 'frame'
        INTERVAL = 'interval'


    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

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


Subsystem.registerImplementation("camera", CameraSubsystem)