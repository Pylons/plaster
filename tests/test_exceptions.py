class TestNoSectionError(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import NoSectionError
        return NoSectionError(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.section == 'foo'
        assert exc.message == 'Could not find requested section "foo".'

    def test_it_overrides_message(self):
        exc = self._makeOne('foo', 'bar')
        assert isinstance(exc, ValueError)
        assert exc.section == 'foo'
        assert exc.message == 'bar'


class TestInvalidURI(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import InvalidURI
        return InvalidURI(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'Unable to parse config_uri "foo".'
        assert exc.uri == 'foo'

    def test_it_overrides_message(self):
        exc = self._makeOne('foo', 'bar')
        assert isinstance(exc, ValueError)
        assert exc.message == 'bar'
        assert exc.uri == 'foo'


class TestLoaderNotFound(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import LoaderNotFound
        return LoaderNotFound(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.scheme == 'foo'
        assert exc.message == (
            'Could not find a matching loader for the scheme "foo".')

    def test_it_overrides_message(self):
        exc = self._makeOne('foo', 'bar')
        assert isinstance(exc, ValueError)
        assert exc.scheme == 'foo'
        assert exc.message == 'bar'


class TestMultipleLoadersFound(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import MultipleLoadersFound
        return MultipleLoadersFound(*args, **kwargs)

    def test_it(self):
        dummy1 = DummyLoader('dummy1')
        dummy2 = DummyLoader('dummy2')
        exc = self._makeOne('https', [dummy1, dummy2])
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Multiple plaster loaders were found for scheme="https". '
            'Please specify a more specific config_uri. Matched loaders: '
            'dummy1, dummy2')
        assert exc.scheme == 'https'
        assert exc.loaders == [dummy1, dummy2]

    def test_it_overrides_message(self):
        dummy = object()
        exc = self._makeOne('https', [dummy], 'foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'foo'
        assert exc.scheme == 'https'
        assert exc.loaders == [dummy]


class DummyLoader(object):
    def __init__(self, scheme):
        self.scheme = scheme
