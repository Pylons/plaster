import os.path

import pytest


class TestURL:
    def _callFUT(self, uri):
        from plaster.uri import parse_uri

        return parse_uri(uri)

    def test_relative_path(self):
        uri = self._callFUT("development.ini")
        assert uri.scheme == "file+ini"
        assert uri.path == "development.ini"
        assert uri.options == {}
        assert uri.fragment == ""

    def test_absolute_path(self):
        path = os.path.abspath("/path/to/development.ini")
        uri = self._callFUT(path)
        assert uri.scheme == "file+ini"
        assert uri.path == path
        assert uri.options == {}
        assert uri.fragment == ""

    def test_absolute_path_with_fragment(self):
        path = os.path.abspath("/path/to/development.ini")
        uri = self._callFUT(path + "?a=b&c=d#main")
        assert uri.scheme == "file+ini"
        assert uri.path == path
        assert uri.options == {"a": "b", "c": "d"}
        assert uri.fragment == "main"

    def test_url(self):
        uri = self._callFUT("redis://username@password:localhost/foo?a=b#main")
        assert uri.scheme == "redis"
        assert uri.path == "username@password:localhost/foo"
        assert uri.options == {"a": "b"}
        assert uri.fragment == "main"

    def test_url_for_file(self):
        uri = self._callFUT("pastedeploy+ini://development.ini")
        assert uri.scheme == "pastedeploy+ini"
        assert uri.path == "development.ini"
        assert uri.options == {}
        assert uri.fragment == ""

    def test_missing_scheme(self):
        from plaster.exceptions import InvalidURI

        with pytest.raises(InvalidURI):
            self._callFUT("foo")

    def test___str__(self):
        uri = self._callFUT("development.ini")
        assert str(uri) == "file+ini://development.ini"

    def test___str___with_options(self):
        uri = self._callFUT("development.ini?a=b&c=d")
        assert str(uri) == "file+ini://development.ini?a=b&c=d"

    def test___str___with_fragment(self):
        uri = self._callFUT("development.ini#main")
        assert str(uri) == "file+ini://development.ini#main"

    def test___repr___(self):
        uri = self._callFUT("development.ini#main")
        assert repr(uri) == "PlasterURL('file+ini://development.ini#main')"

    def test_returns_same_instance(self):
        uri1 = self._callFUT("development.ini")
        uri2 = self._callFUT(uri1)
        assert uri1 is uri2

    def test_colon_prefix_scheme(self):
        uri = self._callFUT("egg:myapp#main")
        assert uri.scheme == "egg"
        assert uri.path == "myapp"
        assert uri.fragment == "main"

    def test_only_scheme(self):
        uri = self._callFUT("egg:")
        assert uri.scheme == "egg"
        assert uri.path == ""
        assert uri.options == {}
        assert uri.fragment == ""


def test_default_url_values():
    from plaster.uri import PlasterURL

    url = PlasterURL("foo")
    assert url.scheme == "foo"
    assert url.path == ""
    assert url.options == {}
    assert url.fragment == ""
