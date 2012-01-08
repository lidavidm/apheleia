import pyglet
from pyglet import gl


class TransformGroup(pyglet.graphics.Group):
    def __init__(self, projection, parent=None):
        super().__init__(parent)
        self.projection = projection
        self.transforms = []

    def add(self, transform, **kwargs):
        self.transforms.append((transform, kwargs))
        return kwargs

    def set_state(self):
        for t, kwargs in self.transforms:
            t.apply(self.projection, kwargs)

    def unset_state(self):
        for t, kwargs in reversed(self.transforms):
            t.remove(self.projection, kwargs)


class transform:
    def __init__(self, func, inverse=lambda p, d, k: None, state={}):
        self.name = func.__name__
        self.func = func
        self.inv = inverse
        self.state = state

    def inverse(self, inverse):
        self.inverse = inverse
        return self

    def apply(self, projection, kwargs):
        self.func(projection, self.state, kwargs)

    def remove(self, projection, kwargs):
        self.inv(projection, self.state, kwargs)


@transform
def rotate(p, state, kwargs):
    x, y = p.x, p.y
    xp = x + (p.width / 2)
    yp = y + (p.height / 2)
    gl.glTranslatef(xp, yp, 0)
    gl.glRotatef(kwargs['angle'], 0.0, 0.0, 1.0)
    gl.glTranslatef(-xp, -yp, 0)


@transform
def clearModelview(p, state, kwargs):
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glPushMatrix()
    gl.glLoadIdentity()


@clearModelview.inverse
def clearModelview(p, state, kwargs):
    gl.glPopMatrix()
