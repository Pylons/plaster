import pytest


class TestURL(object):
    def _callFUT(self, uri):
        from plaster.uri import parse_uri
        return parse_uri(uri)

    def test_relative_path(self):
        uri = self._callFUT('development.ini')
        assert uri.scheme == 'ini'
        assert uri.path == 'development.ini'
        assert uri.fragment is None

    def test_absolute_path(self):
        uri = self._callFUT('/path/to/development.ini')
        assert uri.scheme == 'ini'
        assert uri.path == '/path/to/development.ini'
        assert uri.fragment is None

    def test_absolute_path_with_fragment(self):
        uri = self._callFUT('/path/to/development.ini#main')
        assert uri.scheme == 'ini'
        assert uri.path == '/path/to/development.ini'
        assert uri.fragment == 'main'

    def test_url(self):
        uri = self._callFUT('redis://username@password:localhost/foo?a=b#main')
        assert uri.scheme == 'redis'
        assert uri.path == 'username@password:localhost/foo?a=b'
        assert uri.fragment == 'main'

    def test_url_for_file(self):
        uri = self._callFUT('ini+pastedeploy://development.ini')
        assert uri.scheme == 'ini+pastedeploy'
        assert uri.path == 'development.ini'
        assert uri.fragment is None

    def test_missing_scheme(self):
        from plaster.exceptions import InvalidURI
        with pytest.raises(InvalidURI):
            self._callFUT('foo')

    def test___str__(self):
        uri = self._callFUT('development.ini')
        assert str(uri) == 'ini://development.ini'

    def test___str___with_fragment(self):
        uri = self._callFUT('development.ini#main')
        assert str(uri) == 'ini://development.ini#main'

    def test_returns_same_instance(self):
        uri1 = self._callFUT('development.ini')
        uri2 = self._callFUT(uri1)
        assert uri1 is uri2

    def test_colon_prefix_scheme(self):
        uri = self._callFUT('egg:myapp#main')
        assert uri.scheme == 'egg'
        assert uri.path == 'myapp'
        assert uri.fragment == 'main'
