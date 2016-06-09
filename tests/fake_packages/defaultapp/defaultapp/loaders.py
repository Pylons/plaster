class LoaderBase(object):
    entry_point_key = None

    def __init__(self, uri):
        self.uri = uri

    def get_sections(self):
        return ['a', 'b']

    def get_settings(self, *args, **kwargs):
        return self.entry_point_key

    def setup_logging(self):
        return self.entry_point_key


class ConfLoader(LoaderBase):
    entry_point_key = 'conf'


class INILoader(LoaderBase):
    entry_point_key = 'ini+foo'


class YAMLFooLoader(LoaderBase):
    entry_point_key = 'yaml+foo'


class YAMLBarLoader(LoaderBase):
    entry_point_key = 'yaml+bar'


class BadLoader(object):
    def __init__(self, uri):
        self.uri = uri


class WontBeLoaded(LoaderBase):
    entry_point_key = 'ini'
