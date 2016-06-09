import unittest

from tests.fixture import *
import defaultapp.loaders as loaders

import plaster

class TestGetLoader(unittest.TestCase):

    def test_simple_uri(self):
        config_uri = 'development.ini'
        loader = plaster.get_loader(config_uri)

        self.assertEqual(loader.entry_point_key, 'ini')

    def test_scheme_uri(self):
        config_uri = 'ini://development.ini'
        loader = plaster.get_loader(config_uri)

        self.assertEqual(loader.entry_point_key, 'ini')

    def test_scheme_other_uri(self):
        config_uri = 'ini+other://development.ini'
        loader = plaster.get_loader(config_uri)

        self.assertEqual(loader.entry_point_key, 'ini+other')

    def test_uri_loader(self):
        config_uri = 'yaml://development.ini'
        loader = plaster.get_loader(config_uri)

        self.assertIsInstance(loader.uri, plaster.PlasterURL)

    def test_other_groups(self):
        config_uri = 'other-scheme://development.ini'

        self.assertRaises(plaster.NoLoaderFound, plaster.get_loader, config_uri)
