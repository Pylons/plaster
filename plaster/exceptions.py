class NoSectionError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Could not find requested section.'
        Exception.__init__(self, message)
        self.message = message


class InvalidURI(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Unable to parse "config_uri".'
        Exception.__init__(self, message)
        self.message = message


class LoaderNotFound(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Could not find a matching loader for the "config_uri".'
        Exception.__init__(self, message)
        self.message = message


class MultipleLoadersFound(ValueError):
    def __init__(self, scheme, loaders, message=None):
        self.scheme = scheme
        self.loaders = loaders
        if message is None:
            message = (
                'Multiple plaster loaders were found for scheme="{0}". '
                'Please specify a more specific "config_uri".'
            ).format(self.scheme)
        Exception.__init__(self, message)
        self.message = message
