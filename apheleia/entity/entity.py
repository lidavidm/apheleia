import apheleia.common

@apheleia.common.prototypeable()
class Entity:
    def __init__(self, **fields):
        self.projection = None
        for field, value in fields.items():
            setattr(self, field, value)

    @classmethod
    def entity_register(cls, kind, kwargs):
        return cls.register(kind, [], kwargs['attributes'])
