class LoaderBase(object):
    entry_point_key = None

    def __init__(self, uri):
        self.uri = uri

    def get_settings(self, *args, **kwargs):

        return self.__class__.entry_point_key

    def setup_logging(self):

        return self.__class__.entry_point_key

class INILoader(LoaderBase):
    entry_point_key = 'ini'

class INIOtherLoader(LoaderBase):
    entry_point_key = 'ini+other'
    STRING_CONFIG = True

class YAMLLoader(LoaderBase):
    entry_point_key = 'yaml'

class YAMLOtherLoader(LoaderBase):
    entry_point_key = 'yaml+other'
    STRING_CONFIG = True

class BadLoader(object):

    def __init__(self, uri):
        self.uri = uri


class WontBeLoaded(LoaderBase):
    entry_point_key = 'ini'