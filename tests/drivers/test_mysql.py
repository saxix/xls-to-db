# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

import xls_to_db.drivers.mysql

# PARAMS = ('localhost', 'xls', 'root', '',)
# DATABASE = 'xls'

from .ab import Abstract


class TestMySql(Abstract, unittest.TestCase):
    _driver = xls_to_db.drivers.mysql.driver
    PARAMS = ('localhost', 'xls', 'root', '',)
