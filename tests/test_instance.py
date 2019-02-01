# -*- coding: utf-8 -*-
import unittest
from .fixtures import fixture_data, Chain, SharedInstance


class Testcases(unittest.TestCase):
    def setUp(self):
        fixture_data()

    def test_shared_instance(self):
        self.assertFalse(SharedInstance.instance)
        c = Chain()
        c.set_shared_instance()
        self.assertEqual(id(c), id(SharedInstance.instance))
        c2 = Chain()
        c2.set_shared_instance()
        self.assertEqual(id(c2), id(SharedInstance.instance))

    def test_shared_config(self):
        self.assertFalse(SharedInstance.config)
        c = Chain()
        c.set_shared_config(dict(nobroadcast=True))
        self.assertTrue(SharedInstance.config.get("nobroadcast", False))

        c.set_shared_instance()
        c.set_shared_config(dict(nobroadcast=False))
        self.assertFalse(SharedInstance.config.get("nobroadcast", True))
