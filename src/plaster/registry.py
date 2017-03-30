from collections import defaultdict

from .interfaces import ILoaderInfo
from .uri import parse_uri

class LoaderRegistry(object):
    def __init__(self, search_entry_points=True):
        # scheme -> protocol -> factory
        self._factories = defaultdict(defaultdict(set))

        self.search_entry_points = search_entry_points

    def add_loader(self, factory, scheme, protocols=None):
        for protocol in {None} | set(protocols or []):
            self._factories[scheme][protocol].add(factory)

    def find_loaders(self, scheme, protocols=None):
        infos = []
        found_factories = self._factories[scheme][None]
        if not protocols:
            protocols = []

        # a factory must satisfy every requested protocol so we intersect
        # the sets
        for protocol in protocols:
            found_factories &= self._factories[scheme][protocol]

        for factory in found_factories:
            infos.append(BasicLoaderInfo(factory, scheme, protocols))

        if self.search_entry_points:
            pass

        return infos

    def get_loader(self, config_uri, protocols=None):
        config_uri = parse_uri(config_uri)
        loaders = self.find_loaders(config_uri.scheme, protocols)

        if len(loaders) < 1:
            raise LoaderNotFound

        elif len(loaders) > 1:
            raise MultipleLoadersFound

        loader_info = loaders[0]
        return loader_info.load(config_uri)


class BasicLoaderInfo(ILoaderInfo):
    def __init__(self, factory, scheme, protocols):
        self.factory = factory
        self.scheme = scheme
        self.protocols = protocols

    def load(self, uri):
        uri = parse_uri(uri)
        return self.factory(uri)


class EntryPointLoaderInfo(ILoaderInfo):
    def __init__(self, ep, protocols=None):
        self.entry_point = ep
        self.scheme = '{0}+{1}'.format(ep.name, ep.dist.project_name)
        self.protocols = protocols

        self._factory = None

    @property
    def factory(self):
        if self._factory is None:
            self._factory = self.entry_point.load()
        return self._factory

    def load(self, config_uri):
        config_uri = parse_uri(config_uri)
        return self.factory(config_uri)
