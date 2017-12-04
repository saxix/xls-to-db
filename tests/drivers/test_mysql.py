# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest
import pytest
import xls_to_db.drivers.mysql
from .ab import Abstract



class TestMySql(Abstract, unittest.TestCase):
    pytestmark = pytest.mark.mysql
    _driver = xls_to_db.drivers.mysql.driver
    PARAMS = ('localhost', 'xls', 'root', '',)
    _CREATE_DB = "CREATE DATABASE IF NOT EXISTS {};".format(Abstract.DATABASE)
