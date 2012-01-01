import apheleia.common

@apheleia.common.prototypeable()
class Component:
    @classmethod
    def _prototype_define(cls, kind, kwargs):
        return cls.register(
            kind,
            kwargs.get('fields', []),
            kwargs.get('attributes', {}))
