import collections

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


class EventManager:
    def __init__(self):
        self._sources = {}
        self._handlers = collections.defaultdict(list)
        self._events = {}

    def provide(self, source, obj):
        self._sources[source] = obj

    def remove(self, source):
        del self._sources[source]

    def getEvent(self, kind):
        event = Event.getKind(kind)()
        self._events[kind] = event
        return event

    def registerHandlers(self, scene):
        for attr in dir(scene):
            attr = getattr(scene, attr)
            if hasattr(attr, '_apheleia_events'):
                for event in attr._apheleia_events:
                    self.getEvent(event).addHandler(attr)
                    self._handlers[event].append(attr)

    def attachHandlers(self, scene):
        for event in self._events.values():
            event.attach()
