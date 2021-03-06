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

    def fire(self, state, *args, **kwargs):
        for handler in self._handlers:
            handler(self, state, *args, **kwargs)

    @classmethod
    def _prototype_define(cls, kind, kwargs):
        return cls.register(
            kind, [],
            {
                "source": {
                    k: None for k in kwargs["attributes"].get("sources", [])}
            })


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
        for source in event.source:
            event.source[source] = self._sources[source]
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
            print(event)
            event.attach()
