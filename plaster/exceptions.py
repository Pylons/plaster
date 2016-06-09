class NoSectionError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'A section name is required.'
        Exception.__init__(self, message)
        self.message = message


class InvalidURI(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Unable to parse "config_uri".'
        Exception.__init__(self, message)
        self.message = message


class NoLoaderFound(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = 'Could not find a matching loader for the "config_uri".'
        Exception.__init__(self, message)
        self.message = message
