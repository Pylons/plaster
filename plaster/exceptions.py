class NoSectionError(ValueError):
    def __init__(self, section, message=None):
        if message is None:
            message = 'Could not find requested section "{0}".'.format(section)
        Exception.__init__(self, message)
        self.message = message
        self.section = section


class InvalidURI(ValueError):
    def __init__(self, uri, message=None):
        if message is None:
            message = 'Unable to parse config_uri "{0}".'.format(uri)
        Exception.__init__(self, message)
        self.message = message
        self.uri = uri


class LoaderNotFound(ValueError):
    def __init__(self, scheme, message=None):
        if message is None:
            message = (
                'Could not find a matching loader for the scheme "{0}".'
                .format(scheme))
        Exception.__init__(self, message)
        self.message = message
        self.scheme = scheme


class MultipleLoadersFound(ValueError):
    def __init__(self, scheme, loaders, message=None):
        if message is None:
            message = (
                'Multiple plaster loaders were found for scheme="{0}". '
                'Please specify a more specific config_uri. '
                'Matched loaders: {1}'
            ).format(scheme, ', '.join(loader.name
                                       for loader in sorted(
                                           loaders, key=lambda v: v.name)))
        Exception.__init__(self, message)
        self.message = message
        self.scheme = scheme
        self.loaders = loaders
