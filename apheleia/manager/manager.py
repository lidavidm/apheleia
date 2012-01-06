import os.path
import collections
import json
import pyglet

import apheleia.projection.component


class Backend:
    class Promise:
        def __init__(self):
            pass

        def open(self, mode):
            pass

    def __init__(self, path):
        self._path = path
        self._cache = {}

    def load(self, key):
        pass

    def cache(self, key, data):
        self._cache[key] = data

    def preload(self):
        pass

    def contents(self, path):
        pass

    @staticmethod
    def parseKey(key):
        result = []
        key = os.path.normpath(key)
        head, tail = os.path.split(key)
        while tail:
            result.append(tail)
            head, tail = os.path.split(head)
            if not tail and head:
                result.append('/')
        result.reverse()
        return result

    @staticmethod
    def unparseKey(key):
        if key[0] == '/':
            return '/' + '/'.join(key[1:])
        return '/'.join(key[1:])

    @staticmethod
    def relativeTo(base, key):
        return Backend.unparseKey(Backend.parseKey(os.path.join(base, key)))


class DirectoryBackend(Backend):
    class Promise(Backend.Promise):
        def __init__(self, path):
            self._path = path

        def open(self, mode):
            if 'a' in mode or 'w' in mode:
                raise ValueError("Mode must be read-only")
            return open(self._path, mode)

        def __repr__(self):
            return '<DirectoryBackend promise for {}>'.format(self._path)

    def preload(self, extensions):
        self._preload = {}
        self._root = os.path.basename(self._path.rstrip('/\\'))
        explore = [(self._preload, os.path.abspath(self._path))]
        while explore:
            parent, path = explore.pop()
            name = os.path.basename(path.rstrip('/\\'))
            parent[name] = {}
            for fname in os.listdir(path):
                fullpath = os.path.join(path, fname)
                if os.path.isfile(fullpath):
                    key, extension = os.path.splitext(fname)
                    if extension in extensions:
                        parent[name][key] = (extension, fullpath)
                elif os.path.isdir(fullpath):
                    explore.append((parent[name], fullpath))

    def load(self, key):
        key = self.parseKey(key)
        assert key and key[0] == '/', "Key must be absolute path"
        current = self._preload[self._root]
        for component in key[1:]:
            if component not in current:
                raise BackendKeyError
            current = current[component]
        return current[0], DirectoryBackend.Promise(current[1])

    def contents(self, path):
        key = self.parseKey(path)
        assert key and key[0] == '/', "Key must be absolute path"
        current = self._preload[self._root]
        for component in key[1:]:
            if component not in current:
                raise BackendKeyError
            current = current[component]

        res = []
        for key, item in current.items():
            if isinstance(item, tuple):
                res.append(key)
            else:
                res.append(key + '/')  # it's a directory
        return res


class BackendKeyError(KeyError):
    pass

# Instead of tags, use "collections", which are another data type (lists of
# references, essentially)


class Path:
    def __init__(self, path, contents):
        self.path = path
        self.contents = contents

    def __contains__(self, key):
        return key in self.contents


class Reference(collections.namedtuple('Reference', 'manager path resource')):
    def __repr__(self):
        return "<Reference {} {}>".format(self.path, repr(self.resource)[:50])


class Manager:
    formats = {}
    types = {}

    class Cache:
        OBJECT = 0  # cache the resulting object
        DATA = 1  # cache just the data
        NOTHING = 2  # don't cache anything

    def __init__(self, backend=None):
        self._backend = backend
        self._cache = {}
        backend.preload(Manager.formats.keys())

    def provide(self, path, resource):
        """Provide an external asset (windows, etc.)"""
        pass

    def reference(self, path, force=False):
        """
        Create a reference to an asset, prototype, or instance.

        :param force: If ``True``, always create a reference.

        """
        item = self.load(path)
        if (not force or (
                not isinstance(item, Prototype) and
                not isinstance(item, Instance))):
            return Reference(self, path, item)
        return item

    def path(self, path):
        return Path(path, self._backend.contents(path))

    def load(self, key):
        if key in self._cache:
            return self._cache[key]
        try:
            extension, promise = self._backend.load(key)
            type_, data = Manager.formats[extension](key, promise, self)
            cache, obj = Manager.types[type_](key, data, self)
            # if references to other objects are made, the type_loader can
            # use Manager.parseKey to get a relative key
            if cache == Manager.Cache.OBJECT:
                self._cache[key] = obj
            elif cache == Manager.Cache.DATA:
                self._backend.cache(key, data)
            return obj
        except BackendKeyError:
            raise KeyError("Key {} not found".format(key))
        except KeyError:
            raise KeyError("Could not load key {}".format(key))
        except ValueError:
            raise

    def parseKey(self, key):
        return self._backend.parseKey(key)

    def relativeTo(self, base, key):
        if isinstance(base, Path):
            base = base.path
        return self._backend.relativeTo(base, key)

    @classmethod
    def type_loader(cls, type_):
        """
        Decorator for functions that load data types (resource, event...)
        """
        def format_loader_decorator(func):
            Manager.types[type_] = func
            return func
        return format_loader_decorator

    @classmethod
    def format_loader(cls, *formats):
        """Decorator for functions that load data formats (JSON, Sexp...)"""
        def format_loader_decorator(func):
            for format_ in formats:
                Manager.formats[format_] = func
            return func
        return format_loader_decorator


class Prototype:
    prototypeable = {}

    def __init__(self, type_, kind, kwargs):
        self.type = Prototype.prototype(type_, kind, kwargs)
        self.kind = kind
        self.kwargs = kwargs

    def create(self):
        return self.type()

    def __repr__(self):
        return "<Prototype {} for {} (data {})>".format(
            self.kind, self.type, self.kwargs)

    @classmethod
    def define(cls, type_, klass):
        cls.prototypeable[type_] = klass

    @classmethod
    def prototype(cls, type_, kind, kwargs):
        return cls.prototypeable[type_]._prototype_define(kind, kwargs)

    @classmethod
    def get(cls, type_, kind):
        return cls.prototypeable[type_].getKind(kind)


def jsonRefHook(manager):
    def hook(dct):
        if "__ref__" in dct:
            return manager.reference(dct["__ref__"], force=False)
        return dct
    return hook


@Manager.format_loader('.json')
def json_loader(key, promise, manager):
    data = json.load(promise.open('r'), object_hook=jsonRefHook(manager))
    if "type" not in data and "data" not in data:
        raise ValueError("JSON in {} not well formed".format(key))
    return data["type"], data["data"]


@Manager.format_loader('.placeholder_asset')
def placeholder_asset_loader(key, promise, manager):
    data = promise.open('rb').read()
    return "placeholder_asset", data


@Manager.format_loader('.png')
def png_loader(key, promise, manager):
    image = pyglet.image.load('.png', file=promise.open('rb'))
    return "image", image


@Manager.type_loader('prototype')
def prototype_loader(key, data, manager):
    type_ = data["type"]
    kind = data["kind"]
    del data["type"]
    del data["kind"]
    return Manager.Cache.OBJECT, Prototype(type_, kind, data)


@Manager.type_loader('instance')
def instance_loader(key, data, manager):
    prototype = data["type"]
    kind = data["kind"]
    del data["type"], data["kind"]
    return Manager.Cache.DATA, Prototype.get(prototype, kind).instance(data)


@Manager.type_loader('image')
def image_type_loader(key, data, manager):
    return Manager.Cache.OBJECT, data


@Manager.type_loader("placeholder_asset")
def placeholder_asset_type_loader(key, data, manager):
    return Manager.Cache.NOTHING, data


def test():
    backend = DirectoryBackend('/home/david/Code/apheleia/apheleia')
    backend.preload({'.py'})
    print(backend._preload)
    return backend
