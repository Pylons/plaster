class NoSectionError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = 'A section name is required.'
        Exception.__init__(self, message)
        self.message = message

class InvalidLoaderURI(Exception):
    def __init__(self, message=None):
        if message is None:
            message = 'Unable to parse supplied "config_uri".'
        Exception.__init__(self, message)
        self.message = message
