import plaster
from plaster.protocols import IWSGIProtocol

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


class ConfLoader(LoaderBase):
    entry_point_key = "conf"


class INILoader(LoaderBase):
    entry_point_key = "ini"


class INIWSGILoader(IWSGIProtocol, LoaderBase):
    entry_point_key = "ini+wsgi"

    def get_wsgi_app(self, name=None, defaults=None):
        return "wsgi app"

    def get_wsgi_app_settings(self, name=None, defaults=None):
        return {"a": "b"}

    def get_wsgi_filter(self, name=None, defaults=None):
        return "wsgi filter"

    def get_wsgi_server(self, name=None, defaults=None):
        return "wsgi server"


class YAMLLoader(LoaderBase):
    entry_point_key = "yaml"


class YAMLFooLoader(LoaderBase):
    entry_point_key = "yaml+foo"


class DuplicateLoader(LoaderBase):
    entry_point_key = "app1+dup"


class BadLoader:
    def __init__(self, uri):
        self.uri = uri


class WontBeLoaded(LoaderBase):
    entry_point_key = "ini"
