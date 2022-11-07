import os.path
import sys

import pytest


@pytest.fixture(scope="session")
def fake_packages():
    # we'd like to keep this scope more focused but it's proven really
    # difficult to fully monkeypatch importlib.metadata and so for now we just
    # install the packages for the duration of the test suite
    test_dir = os.path.dirname(__file__)

    for name in ("app1", "app2"):
        info_dir = os.path.join(test_dir, "fake_packages", name)
        sys.path.insert(0, info_dir)
