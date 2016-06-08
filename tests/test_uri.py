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
