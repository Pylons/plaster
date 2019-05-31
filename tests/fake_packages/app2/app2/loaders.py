import plaster

_SECTIONS = {"a": {"foo": "bar"}, "b": {"baz": "xyz"}}


class LoaderBase(plaster.ILoader):
    entry_point_key = None

    def __init__(self, uri):
        self.uri = uri

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
            pass
        return result

    def setup_logging(self, defaults=None):
        self.logging_setup = True
        self.logging_defaults = defaults


class YAMLBarLoader(LoaderBase):
    entry_point_key = "yaml+bar"


class DuplicateLoader(LoaderBase):
    entry_point_key = "app2+dup"
