import mock
import os.path
import pkg_resources
import pytest
import sys

@pytest.fixture
def fake_packages():
    test_dir = os.path.dirname(__file__)
    ws = pkg_resources.WorkingSet()
    paths = []
    for name in ('app1', 'app2'):
        info_dir = os.path.join(test_dir, 'fake_packages', name)
        ws.add_entry(info_dir)
        paths.append(info_dir)
    sys.path.extend(paths)
    try:
        with mock.patch.multiple(
            'pkg_resources',
            working_set=ws,
            iter_entry_points=ws.iter_entry_points,
        ):
            yield ws
    finally:
        for path in paths:
            sys.path.remove(path)
