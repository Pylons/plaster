import plaster

_SECTIONS = {
    'a': {
        'foo': 'bar',
    },
    'b': {
        'baz': 'xyz',
    },
}


class LoaderBase(plaster.Loader):
    entry_point_key = None

    def get_sections(self):
        return list(_SECTIONS.keys())

    def get_settings(self, section=None, defaults=None):
        if section is None:
            section = self.uri.fragment
        if defaults is not None:
            result = defaults.copy()
        else:
            result = {}
        try:
            result.update(_SECTIONS[section])
        except KeyError:
            raise plaster.NoSectionError
        return result

    def setup_logging(self, defaults=None):
        self.logging_setup = True
        self.logging_defaults = defaults


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
