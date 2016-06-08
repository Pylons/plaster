from .exceptions import (
    NoSectionError,
    NoLoaderFound,
    SchemeNotFound,
    InvalidURI,
)
from .compat import parse
import os
import pkg_resources
import warnings

DEFAULT_SCHEME = 'ini+pastedeploy'
LOADER_ENTRY_POINT_GROUP = 'plaster.loader'


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
    config_uri = parse_uri(config_uri, section)
    if section is None:
        raise NoSectionError
    loader = get_loader(config_uri)
    return loader.get_settings(section, defaults)


def setup_logging(config_uri, name=None, defaults=None):
    """
    Execute the logging configuration defined in the config file.

    This function should, at least, configure the Python standard logging
    module. However, it may also be used to configure any other logging
    subsystems that serve a similar purpose.

    """
    config_uri = parse_uri(config_uri, section=name)
    loader = get_loader(config_uri)
    return loader.setup_logging(defaults)


def get_loader(config_uri):
    """
    Find a loader capable of handling ``config_uri``.

    """

    parsed_uri = parse_uri(config_uri)

    scheme_prefix, scheme_suffix = _split_scheme(parsed_uri.scheme)

    all_loaders = []
    prefix_loaders = []
    suffix_loaders = []

    for loader in pkg_resources.iter_entry_points(
            group=LOADER_ENTRY_POINT_GROUP):
        all_loaders.append(loader)

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
        raise NoLoaderFound()

    if len(source) > 1:
        warnings.warn(
            'Multiple loaders found supporting this scheme. Using the '
            'first')

    loader_obj = source[0].load()

    loader_uses_str = getattr(loader_obj, 'STRING_CONFIG', False)

    if loader_uses_str:
        parsed_uri = parsed_uri.geturl()

    loader_instance = loader_obj(parsed_uri)

    return loader_instance


def parse_uri(uri, scheme=None, section=None):
    parse_result = parse.urlparse(uri)._asdict()

    if parse_result['path'] == '' and parse_result['netloc'] != '':
        parse_result['path'] = parse_result['netloc']

    elif parse_result['netloc'] == '' and parse_result['path'] == '':
        raise InvalidURI('neiter the netloc nor path portion of the '
                         'uri could be parsed.')

    # Set scheme
    if scheme is None and parse_result['scheme'] == '':
        parse_result['scheme'] = _get_scheme_from_uri(parse_result)
    elif scheme is not None:
        parse_result['scheme'] = scheme
    elif parse_result['scheme'] == '':
        parse_result['scheme'] = DEFAULT_SCHEME

    # Set fragment
    if section is not None:
        parse_result['fragment'] = section

    return parse.ParseResult(**parse_result)


def _get_scheme_from_uri(parse_result):
    if parse_result['path'] == '':
        raise SchemeNotFound('Scheme could not be found from the '
                             'uri {}.'.format(parse_result))
    else:
        path = parse_result['path']
        if path == '':
            path = parse_result['netloc']

        if path == '':
            raise SchemeNotFound(
                'Scheme could not be found from the '
                'uri {}.'.format(parse_result))

    filename, extension = os.path.splitext(path)

    if extension == '':
        # warnings.warn(str(path))
        extension = DEFAULT_SCHEME
    else:
        extension = extension[1:]

    return extension


def _split_scheme(scheme):
    if '+' in scheme:
        prefix, suffix = scheme.split('+', 1)

    else:
        prefix = scheme
        suffix = None

    return prefix, suffix
