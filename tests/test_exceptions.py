class TestInvalidURI:
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import InvalidURI

        return InvalidURI(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne("foo")
        assert isinstance(exc, ValueError)
        assert exc.message == 'Unable to parse config_uri "foo".'
        assert exc.uri == "foo"

    def test_it_overrides_message(self):
        exc = self._makeOne("foo", message="bar")
        assert isinstance(exc, ValueError)
        assert exc.message == "bar"
        assert exc.uri == "foo"


class TestLoaderNotFound:
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import LoaderNotFound

        return LoaderNotFound(*args, **kwargs)

    def test_it(self):
        exc = self._makeOne("foo")
        assert isinstance(exc, ValueError)
        assert exc.scheme == "foo"
        assert exc.protocols is None
        assert exc.message == ('Could not find a matching loader for the scheme "foo".')

    def test_it_with_protocol(self):
        exc = self._makeOne("foo", ["wsgi"])
        assert isinstance(exc, ValueError)
        assert exc.scheme == "foo"
        assert exc.protocols == ["wsgi"]
        assert exc.message == (
            'Could not find a matching loader for the scheme "foo", ' 'protocol "wsgi".'
        )

    def test_it_with_multiple_protocols(self):
        exc = self._makeOne("foo", ["wsgi", "qt"])
        assert isinstance(exc, ValueError)
        assert exc.scheme == "foo"
        assert exc.protocols == ["wsgi", "qt"]
        assert exc.message == (
            'Could not find a matching loader for the scheme "foo", '
            'protocol "wsgi, qt".'
        )

    def test_it_overrides_message(self):
        exc = self._makeOne("foo", message="bar")
        assert isinstance(exc, ValueError)
        assert exc.scheme == "foo"
        assert exc.protocols is None
        assert exc.message == "bar"


class TestMultipleLoadersFound:
    def _makeOne(self, *args, **kwargs):
        from plaster.exceptions import MultipleLoadersFound

        return MultipleLoadersFound(*args, **kwargs)

    def test_it(self):
        dummy1 = DummyLoaderInfo("dummy1")
        dummy2 = DummyLoaderInfo("dummy2")
        exc = self._makeOne("https", [dummy1, dummy2])
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Multiple plaster loaders were found for scheme "https". '
            "Please specify a more specific config_uri. Matched loaders: "
            "dummy1, dummy2"
        )
        assert exc.scheme == "https"
        assert exc.protocols is None
        assert exc.loaders == [dummy1, dummy2]

    def test_it_with_protocol(self):
        dummy1 = DummyLoaderInfo("dummy1")
        dummy2 = DummyLoaderInfo("dummy2")
        exc = self._makeOne("https", [dummy1, dummy2], protocols=["wsgi"])
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Multiple plaster loaders were found for scheme "https", '
            'protocol "wsgi". Please specify a more specific config_uri. '
            "Matched loaders: dummy1, dummy2"
        )
        assert exc.scheme == "https"
        assert exc.protocols == ["wsgi"]
        assert exc.loaders == [dummy1, dummy2]

    def test_it_with_multiple_protocols(self):
        dummy1 = DummyLoaderInfo("dummy1")
        dummy2 = DummyLoaderInfo("dummy2")
        exc = self._makeOne("https", [dummy1, dummy2], protocols=["wsgi", "qt"])
        assert isinstance(exc, ValueError)
        assert exc.message == (
            'Multiple plaster loaders were found for scheme "https", '
            'protocol "wsgi, qt". Please specify a more specific '
            "config_uri. Matched loaders: dummy1, dummy2"
        )
        assert exc.scheme == "https"
        assert exc.protocols == ["wsgi", "qt"]
        assert exc.loaders == [dummy1, dummy2]

    def test_it_overrides_message(self):
        dummy = object()
        exc = self._makeOne("https", [dummy], message="foo")
        assert isinstance(exc, ValueError)
        assert exc.message == "foo"
        assert exc.scheme == "https"
        assert exc.protocols is None
        assert exc.loaders == [dummy]


class DummyLoaderInfo:
    def __init__(self, scheme):
        self.scheme = scheme
