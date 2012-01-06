import types


class prototypeable:
    defaultManager = None

    def __init__(self, *paths, manager=None):
        self.paths = list(paths)
        self._manager = manager
        self.cls = None

    def __call__(self, cls):
        if self.cls:
            raise RuntimeError(
                "Prototyper can only manage one class at a time")

        def __repr__(self):
            return "<{} {}>".format(
                self.__class__.__name__,
                " ".join(
                    ":".join([field, str(getattr(self, field))])
                    for field in self.fields))
        cls._kinds = {}
        cls._implementations = {}
        cls.register = classmethod(self.register)
        cls.registerImplementation = classmethod(self.implementation)
        cls.getKind = classmethod(self.getKind)
        cls.__repr__ = __repr__
        cls._prototyper = self
        cls.prototypeName = property(self.prototypeName)
        self.cls = cls
        return cls

    def register(self, cls, name, fields, defaultFields):
        if name in cls._kinds:
            raise ValueError(
                "{} {} already registered".format(cls.__name__, name))
        fields = {f: None for f in fields}
        fields.update(defaultFields)
        fields['fields'] = list(fields.keys())
        superclass = cls._implementations.get(name, cls)
        cls._kinds[name] = type(name.capitalize() + cls.__name__,
                               (superclass,),
                               fields)
        return cls._kinds[name]

    def implementation(self, cls, name, impl):
        if name in cls._implementations:
            raise ValueError("{} implementation {} already registered".format(
                    cls.__name__, name))
        cls._implementations[name] = impl

    def getKind(self, cls, kind, manager=None):
        manager = manager or self.manager
        if kind in cls._kinds:
            return cls._kinds[kind]
        else:
            for path in self.paths:
                if kind in manager.path(path):
                    proto = manager.load(manager.relativeTo(path, kind))
                    return proto.type
            raise KeyError(cls.__name__, kind)

    def listKinds(self, manager=None):
        manager = manager or self.manager
        return sum((manager.path(p).contents for p in self.paths),
                   list(self.cls._kinds.keys()))

    @property
    def manager(self):
        return self._manager or prototypeable.defaultManager

    def prototypeName(self, instance):
        return instance.__class__.__name__
