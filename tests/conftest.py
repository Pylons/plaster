import os.path
import pkg_resources
import pytest

@pytest.fixture
def fake_packages(monkeypatch):
    test_dir = os.path.dirname(__file__)
    ws = pkg_resources.WorkingSet()
    for name in ('app1', 'app2'):
        info_dir = os.path.join(test_dir, 'fake_packages', name)
        ws.add_entry(info_dir)
        monkeypatch.syspath_prepend(info_dir)
    monkeypatch.setattr('pkg_resources.working_set', ws)
    monkeypatch.setattr('pkg_resources.iter_entry_points', ws.iter_entry_points)
    yield ws
