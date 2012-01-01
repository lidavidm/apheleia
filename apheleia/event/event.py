import apheleia.common


@apheleia.common.prototypeable()
class Event:
    def __init__(self):
        self._handlers = []

    def attach(self):
        pass

    def detach(self):
        pass

    def addHandler(self, handler):
        self._handlers.append(handler)

    def removeHandler(self, handler):
        self._handlers.remove(handler)

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        return cls.register(kind, [], {})
