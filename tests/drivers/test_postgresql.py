# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

import xls_to_db.drivers.postgresql
from .ab import Abstract


class TestPostgresql(Abstract, unittest.TestCase):
    _driver = xls_to_db.drivers.postgresql.driver
    PARAMS = ('localhost', 'xls', 'postgres', '',)
