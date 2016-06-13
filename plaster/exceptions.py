class NoSectionError(ValueError):
    """
    Raised by a :class:`plaster.ILoader` which cannot find a section.

    :ivar section: The name of the section that does not exist.

    """
    def __init__(self, section, message=None):
        if message is None:
            message = 'Could not find requested section "{0}".'.format(section)
        Exception.__init__(self, message)
        self.message = message
        self.section = section


class InvalidURI(ValueError):
    """
    Raised by :func:`plaster.parse_uri` when failing to parse a ``config_uri``.

    :ivar uri: The user-supplied ``config_uri`` string.

    """
    def __init__(self, uri, message=None):
        if message is None:
            message = 'Unable to parse config_uri "{0}".'.format(uri)
        Exception.__init__(self, message)
        self.message = message
        self.uri = uri


class LoaderNotFound(ValueError):
    """
    Raised by :func:`plaster.get_loader` when no loaders match the requested
    ``scheme``.

    :ivar scheme: The scheme being matched.

    """
    def __init__(self, scheme, message=None):
        if message is None:
            message = (
                'Could not find a matching loader for the scheme "{0}".'
                .format(scheme))
        Exception.__init__(self, message)
        self.message = message
        self.scheme = scheme


class MultipleLoadersFound(ValueError):
    """
    Raised by :func:`plaster.get_loader` when more than one loader matches the
    requested ``scheme``.

    :ivar scheme: The scheme being matched.
    :ivar loaders: A list of :class:`plaster.LoaderInfo` objects.

    """
    def __init__(self, scheme, loaders, message=None):
        if message is None:
            message = (
                'Multiple plaster loaders were found for scheme="{0}". '
                'Please specify a more specific config_uri. '
                'Matched loaders: {1}'
            ).format(scheme, ', '.join(loader.scheme
                                       for loader in sorted(
                                           loaders, key=lambda v: v.scheme)))
        Exception.__init__(self, message)
        self.message = message
        self.scheme = scheme
        self.loaders = loaders
