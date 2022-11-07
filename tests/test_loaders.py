import pytest


@pytest.mark.usefixtures("fake_packages")
class Test_get_loader:
    def _callFUT(self, *args, **kwargs):
        from plaster.loaders import get_loader

        return get_loader(*args, **kwargs)

    def test_simple_uri(self):
        loader = self._callFUT("development.conf")
        assert loader.entry_point_key == "conf"

    def test_scheme_uri(self):
        loader = self._callFUT("conf://development.conf")
        assert loader.entry_point_key == "conf"

    def test_scheme_uri_for_pkg(self):
        loader = self._callFUT("app1+conf://")
        assert loader.entry_point_key == "conf"

    def test_path_with_extension(self):
        loader = self._callFUT("development.ini")
        assert loader.entry_point_key == "ini+wsgi"

    def test_path_with_extension_and_protocol(self):
        loader = self._callFUT("development.ini", protocols=["wsgi"])
        assert loader.entry_point_key == "ini+wsgi"

    def test_dup(self):
        from plaster.exceptions import MultipleLoadersFound

        with pytest.raises(MultipleLoadersFound):
            self._callFUT("dup://development.ini")

    def test_dedup_app1(self):
        loader = self._callFUT("app1+dup://development.ini")
        assert loader.entry_point_key == "app1+dup"

    def test_dedup_app2(self):
        loader = self._callFUT("app2+dup://development.ini")
        assert loader.entry_point_key == "app2+dup"

    def test_other_groups(self):
        from plaster.exceptions import LoaderNotFound

        with pytest.raises(LoaderNotFound):
            self._callFUT("other-scheme://development.ini")

    def test_bad(self):
        from app1.loaders import BadLoader

        loader = self._callFUT("bad:development")
        assert isinstance(loader, BadLoader)

    def test_it_broken(self):
        with pytest.raises(Exception):
            self._callFUT("development.broken")

    def test_it_notfound(self):
        from plaster.exceptions import LoaderNotFound

        with pytest.raises(LoaderNotFound):
            self._callFUT("development.notfound")

    def test_fallback_non_pkg_scheme(self):
        loader = self._callFUT("yaml+bar://development.yml")
        assert loader.entry_point_key == "yaml+bar"


@pytest.mark.usefixtures("fake_packages")
class Test_find_loaders:
    def _callFUT(self, *args, **kwargs):
        from plaster.loaders import find_loaders

        return find_loaders(*args, **kwargs)

    def test_simple_uri(self):
        loaders = self._callFUT("conf")
        assert len(loaders) == 1
        assert loaders[0].scheme == "app1+conf"
        loader = loaders[0].load("development.conf")
        assert loader.entry_point_key == "conf"

    def test_case_insensitive_scheme(self):
        loaders = self._callFUT("CONF")
        assert len(loaders) == 1
        assert loaders[0].scheme == "app1+conf"
        loader = loaders[0].load("development.conf")
        assert loader.entry_point_key == "conf"

    def test_scheme_specific_uri(self):
        loaders = self._callFUT("ini")
        assert len(loaders) == 1
        assert loaders[0].scheme == "app1+ini"
        loader = loaders[0].load("development.ini")
        assert loader.entry_point_key == "ini+wsgi"

    def test_multiple_yaml_loaders(self):
        loaders = self._callFUT("dup")
        assert len(loaders) == 2
        schemes = {loader.scheme for loader in loaders}
        assert "app1+dup" in schemes
        assert "app2+dup" in schemes

    def test_one_protocol(self):
        loaders = self._callFUT("ini", protocols=["wsgi"])
        assert len(loaders) == 1
        loader = loaders[0].load("development.ini")
        assert loader.entry_point_key == "ini+wsgi"

    def test_multiple_protocols(self):
        loaders = self._callFUT("ini", protocols=["wsgi", "dummy1"])
        assert len(loaders) == 1
        loader = loaders[0].load("development.ini")
        assert loader.entry_point_key == "ini+wsgi"

    def test_multiple_incompatible_protocols(self):
        loaders = self._callFUT("ini", protocols=["wsgi", "dummy2"])
        assert len(loaders) == 0

    def test_it_notfound(self):
        loaders = self._callFUT("notfound")
        assert len(loaders) == 0


@pytest.mark.usefixtures("fake_packages")
class Test_get_sections:
    def _callFUT(self, config_uri):
        from plaster.loaders import get_sections

        return get_sections(config_uri)

    def test_it(self):
        result = self._callFUT("development.ini")
        assert set(result) == {"a", "b"}

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT("development.bad")


@pytest.mark.usefixtures("fake_packages")
class Test_get_settings:
    def _callFUT(self, config_uri, section=None, defaults=None):
        from plaster.loaders import get_settings

        return get_settings(config_uri, section=section, defaults=defaults)

    def test_it_explicit_a(self):
        result = self._callFUT("development.ini", "a")
        assert result == {"foo": "bar"}

    def test_it_explicit_b(self):
        result = self._callFUT("development.ini", "b")
        assert result == {"baz": "xyz"}

    def test_it_fragment(self):
        result = self._callFUT("development.ini#a")
        assert result == {"foo": "bar"}

    def test_defaults(self):
        result = self._callFUT("development.ini", "a", {"baz": "foo"})
        assert result == {"foo": "bar", "baz": "foo"}

    def test_invalid_section(self):
        result = self._callFUT("development.ini", "c")
        assert result == {}

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT("development.bad")


@pytest.mark.usefixtures("fake_packages")
class Test_setup_logging:
    def _makeOne(self, config_uri):
        from plaster.loaders import get_loader

        return get_loader(config_uri)

    def _callFUT(self, config_uri, defaults=None):
        from plaster.loaders import setup_logging

        return setup_logging(config_uri, defaults=defaults)

    def test_it(self):
        loader = self._makeOne("development.ini#a")
        loader.setup_logging()
        assert loader.logging_setup
        assert loader.logging_defaults is None

    def test_it_top_level(self):
        self._callFUT("development.ini#a")

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT("bad://development.ini")
