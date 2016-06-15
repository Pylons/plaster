import pkg_resources

from .exceptions import (
    LoaderNotFound,
    MultipleLoadersFound,
)
from .interfaces import ILoaderInfo
from .uri import parse_uri


def get_sections(config_uri):
    """
    Load the list of named sections.

    .. code-block:: python

        sections = plaster.get_sections('development.ini')
        full_config = {
            section: plaster.get_settings('development.ini', section)
            for section in sections
        }

    """
    loader = get_loader(config_uri)
    return loader.get_sections()


def get_settings(config_uri, section=None, defaults=None):
    """
    Load the settings from a named section.

    .. code-block:: python

        settings = plaster.get_settings(...)
        print(settings['foo'])

    If ``name`` is not ``None`` then it will be used. Otherwise, the ``name``
    will be populated by the fragment defined in the ``config_uri#name``
    syntax. If ``name`` is still ``None`` then a
    :class:`plaster.NoSectionError` error will be raised.

    Any values in ``defaults`` may be overridden by the loader prior to
    returning the final configuration dictionary.

    """
    loader = get_loader(config_uri)
    return loader.get_settings(section, defaults)


def setup_logging(config_uri, defaults=None):
    """
    Execute the logging configuration defined in the config file.

    This function should, at least, configure the Python standard logging
    module. However, it may also be used to configure any other logging
    subsystems that serve a similar purpose.

    """
    loader = get_loader(config_uri)
    return loader.setup_logging(defaults)


def get_loader(config_uri):
    """
    Find a :class:`plaster.ILoader` object capable of handling ``config_uri``.

    ``config_uri`` may be anything that can be parsed by
    :func:`plaster.parse_uri`.

    """
    config_uri = parse_uri(config_uri)
    requested_scheme = config_uri.scheme

    matched_loaders = find_loaders(config_uri)

    if len(matched_loaders) < 1:
        raise LoaderNotFound(requested_scheme)

    if len(matched_loaders) > 1:
        raise MultipleLoadersFound(requested_scheme, matched_loaders)

    loader_info = matched_loaders[0]
    loader = loader_info.load()
    return loader


def find_loaders(config_uri):
    """
    Find all loaders which satisfy the ``config_uri`` scheme.

    Returns a list containing zero or more :class:`plaster.ILoaderInfo`
    objects.

    """
    config_uri = parse_uri(config_uri)
    requested_scheme = config_uri.scheme

    matched_loaders = []
    for loader in pkg_resources.iter_entry_points(group='plaster.loader'):
        if requested_scheme == loader.name:
            matched_loaders.append(loader)

        elif '+' in loader.name:
            ext, _ = loader.name.split('+', 1)
            if ext == requested_scheme:
                matched_loaders.append(loader)

    return [
        EntryPointLoaderInfo(ep, config_uri)
        for ep in matched_loaders
    ]


class EntryPointLoaderInfo(ILoaderInfo):
    def __init__(self, ep, config_uri):
        self.scheme = ep.name
        self.entrypoint = ep
        self.config_uri = config_uri

    def load(self):
        factory = self.entrypoint.load()
        return factory(self.config_uri)
