class NoSectionError(Exception):
    def __init__(self, message=None):
        if message is None:
            message = 'A section name is required.'
        Exception.__init__(self, message)
        self.message = message

class InvalidURI(Exception):
    def __init__(self, message=None):
        if message is None:
            message = 'Unable to parse "config_uri".'
        Exception.__init__(self, message)
        self.message = message
