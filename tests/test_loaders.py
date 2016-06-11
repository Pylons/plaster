import mock
import os.path
import pkg_resources
import pytest
import sys

@pytest.yield_fixture(scope='session')
def fake_loaders():
    test_dir = os.path.dirname(__file__)
    info_dir = os.path.join(
        test_dir, 'fake_packages', 'defaultapp', 'DefaultApp.egg-info')
    ws = pkg_resources.WorkingSet()
    ws.add_entry(os.path.dirname(info_dir))
    sys.path.append(os.path.dirname(info_dir))
    try:
        with mock.patch(
            'pkg_resources.iter_entry_points', ws.iter_entry_points,
        ):
            yield ws
    finally:
        sys.path.remove(os.path.dirname(info_dir))

class Test_get_loader(object):
    @pytest.fixture(autouse=True)
    def working_set(self, fake_loaders):
        self.working_set = fake_loaders

    def _callFUT(self, config_uri):
        from plaster.loaders import get_loader
        return get_loader(config_uri)

    def test_simple_uri(self):
        loader = self._callFUT('development.conf')
        assert loader.entry_point_key == 'conf'

    def test_scheme_uri(self):
        loader = self._callFUT('conf://development.conf')
        assert loader.entry_point_key == 'conf'

    def test_scheme_specific_uri(self):
        loader = self._callFUT('ini+foo://development.ini')
        assert loader.entry_point_key == 'ini+foo'

    def test_compound_uri_with_extension(self):
        loader = self._callFUT('development.ini')
        assert loader.entry_point_key == 'ini+foo'

    def test_yaml_loader_fails(self):
        from plaster.exceptions import MultipleLoadersFound
        with pytest.raises(MultipleLoadersFound):
            self._callFUT('development.yaml')

    def test_other_groups(self):
        from plaster.exceptions import LoaderNotFound
        with pytest.raises(LoaderNotFound):
            self._callFUT('other-scheme://development.ini')

    def test_bad(self):
        from defaultapp.loaders import BadLoader
        loader = self._callFUT('development.bad')
        assert isinstance(loader, BadLoader)

    def test_it_broken(self):
        with pytest.raises(Exception):
            self._callFUT('development.broken')

class Test_get_sections(object):
    @pytest.fixture(autouse=True)
    def working_set(self, fake_loaders):
        self.working_set = fake_loaders

    def _callFUT(self, config_uri):
        from plaster.loaders import get_sections
        return get_sections(config_uri)

    def test_it(self):
        result = self._callFUT('development.ini')
        assert set(result) == set(['a', 'b'])

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT('development.bad')

class Test_get_settings(object):
    @pytest.fixture(autouse=True)
    def working_set(self, fake_loaders):
        self.working_set = fake_loaders

    def _callFUT(self, config_uri, section=None, defaults=None):
        from plaster.loaders import get_settings
        return get_settings(config_uri, section=section, defaults=defaults)

    def test_it_explicit_a(self):
        result = self._callFUT('development.ini', 'a')
        assert result == {'foo': 'bar'}

    def test_it_explicit_b(self):
        result = self._callFUT('development.ini', 'b')
        assert result == {'baz': 'xyz'}

    def test_it_fragment(self):
        result = self._callFUT('development.ini#a')
        assert result == {'foo': 'bar'}

    def test_defaults(self):
        result = self._callFUT('development.ini', 'a', {'baz': 'foo'})
        assert result == {'foo': 'bar', 'baz': 'foo'}

    def test_invalid_section(self):
        from plaster.exceptions import NoSectionError
        with pytest.raises(NoSectionError):
            self._callFUT('development.ini', 'c')

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT('development.bad')

class Test_setup_logging(object):
    @pytest.fixture(autouse=True)
    def working_set(self, fake_loaders):
        self.working_set = fake_loaders

    def _makeOne(self, config_uri):
        from plaster.loaders import get_loader
        return get_loader(config_uri)

    def _callFUT(self, config_uri, defaults=None):
        from plaster.loaders import setup_logging
        return setup_logging(config_uri, defaults=defaults)

    def test_it(self):
        loader = self._makeOne('development.ini#a')
        loader.setup_logging()
        assert loader.logging_setup
        assert loader.logging_defaults is None

    def test_it_top_level(self):
        self._callFUT('development.ini#a')

    def test_it_bad(self):
        with pytest.raises(Exception):
            self._callFUT('bad://development.ini')
