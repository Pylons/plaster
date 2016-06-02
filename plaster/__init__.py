from .exceptions import NoSectionError

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
    config_uri, section = parse_uri(config_uri, section)
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
    config_uri, _ = parse_uri(config_uri)
    loader = get_loader(config_uri)
    return loader.setup_logging(defaults)

def parse_uri(config_uri, section=None):
    path, name = config_uri, None
    if '#' in config_uri:
        path, name = config_uri.split('#', 1)
    if section:
        name = section
    return path, name

def get_loader(config_uri):
    """
    Find a loader capable of handling ``config_uri``.

    """
