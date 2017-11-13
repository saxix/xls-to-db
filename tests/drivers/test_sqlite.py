# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

import xls_to_db.drivers.sqlite3

from .ab import Abstract


class TestSqlite(Abstract, unittest.TestCase):
    _driver = xls_to_db.drivers.sqlite3.driver
    PARAMS = ('', 'xls.sqlite', 'root', '',)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
