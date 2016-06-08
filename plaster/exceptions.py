class NoSectionError(Exception):

    def __init__(self, message=None):
        if message is None:
            message = 'A section name is required.'
        Exception.__init__(self, message)
        self.message = message


class NoLoaderFound(RuntimeError, KeyError):

    def __init__(self, message=None):
        if message is None:
            message = 'A section name is required.'
        Exception.__init__(self, message)
        self.message = message


class SchemeNotFound(RuntimeError, ValueError):

    def __init__(self, message=None):
        if message is None:
            message = 'Scheme could not be determined from the config_uri'
        Exception.__init__(self, message)
        self.message = message


class InvalidURI(RuntimeError, ValueError):

    def __init__(self, message=None):
        if message is None:
            message = 'The URI is invalid'
        Exception.__init__(self, message)
        self.message = message
