import pkg_resources
import warnings

from .exceptions import (
    NoLoaderFound,
    NoSectionError,
)
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
    config_uri = parse_uri(config_uri)
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
    :class:`plaster.exceptions.NoSectionError` error will be raised.

    Any values in ``defaults`` may be overridden by the loader prior to
    returning the final configuration dictionary.

    """
    config_uri = parse_uri(config_uri)
    if section is None:
        section = config_uri.fragment
    if not section:
        raise NoSectionError
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
    Find a :class:`plaster.interfaces.Loader` object capable of handling
    ``config_uri``.

    ``config_uri`` may be anything that can be parsed by
    :func:`plaster.parse_uri`.

    """
    config_uri = parse_uri(config_uri)

    scheme_prefix, scheme_suffix = _split_scheme(config_uri.scheme)

    prefix_loaders = []
    suffix_loaders = []

    for loader in pkg_resources.iter_entry_points(group='plaster.loader'):
        prefix, suffix = _split_scheme(loader.name)

        if scheme_prefix != prefix:
            continue
        elif scheme_suffix is None and suffix is None:
            prefix_loaders.append(loader)
        elif suffix is not None:
            suffix_loaders.append(loader)

    source = None

    if prefix_loaders and scheme_suffix is None:
        source = prefix_loaders

    elif suffix_loaders and scheme_suffix is not None:
        source = suffix_loaders

    elif not (prefix_loaders and not suffix_loaders) or source is None:
        raise NoLoaderFound

    if len(source) > 1:
        warnings.warn(
            'Multiple loaders found supporting this scheme. Using the '
            'first.')

    loader_factory = source[0].load()
    loader = loader_factory(config_uri)
    return loader


def _split_scheme(scheme):
    if '+' in scheme:
        prefix, suffix = scheme.split('+', 1)

    else:
        prefix = scheme
        suffix = None

    return prefix, suffix
