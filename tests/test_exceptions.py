class TestNoSectionError(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import NoSectionError
        return NoSectionError(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne()
        assert isinstance(exc, ValueError)
        assert exc.message == 'Could not find requested section.'

    def test_it_overrides_message(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'foo'


class TestInvalidURI(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import InvalidURI
        return InvalidURI(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne()
        assert isinstance(exc, ValueError)
        assert exc.message == 'Unable to parse "config_uri".'

    def test_it_overrides_message(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'foo'


class TestLoaderNotFound(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import LoaderNotFound
        return LoaderNotFound(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne()
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Could not find a matching loader for the "config_uri".')

    def test_it_overrides_message(self):
        exc = self._makeOne('foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'foo'


class TestMultipleLoadersFound(object):
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import MultipleLoadersFound
        return MultipleLoadersFound(*args, **kwargs)

    def test_it(self):
        dummy = object()
        exc = self._makeOne('https', [dummy])
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Multiple plaster loaders were found for scheme="https". '
            'Please specify a more specific "config_uri".')
        assert exc.scheme == 'https'
        assert exc.loaders == [dummy]

    def test_it_overrides_message(self):
        dummy = object()
        exc = self._makeOne('https', [dummy], 'foo')
        assert isinstance(exc, ValueError)
        assert exc.message == 'foo'
        assert exc.scheme == 'https'
        assert exc.loaders == [dummy]
