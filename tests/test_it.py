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
        yield ws
    except:
        sys.path.remove(os.path.dirname(info_dir))
        raise

class Test_get_loader(object):
    @pytest.fixture(autouse=True)
    def working_set(self, fake_loaders):
        self.working_set = fake_loaders

    def _callFUT(self, config_uri):
        from plaster.loaders import get_loader
        return get_loader(config_uri, _working_set=self.working_set)

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
