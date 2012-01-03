from .event import Event, EventManager
from . import baseevents

def reacts(event):
    def _handler(func):
        if not hasattr(func, '_apheleia_events'):
            func._apheleia_events = []
        func._apheleia_events.append(event)
        return func
    return _handler