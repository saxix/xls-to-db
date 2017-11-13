# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
# import unittest

import pytest
import time

logger = logging.getLogger(__name__)


class Abstract(object):
    _driver = None
    PARAMS = None
    DATABASE = 'xls'
    _DROP_DB = "DROP DATABASE IF EXISTS {};".format(DATABASE)
    _CREATE_DB = "CREATE DATABASE {};".format(DATABASE)

    @classmethod
    def setUpClass(cls):
        cls._driver.set_params(cls.PARAMS[0], '', cls.PARAMS[2], cls.PARAMS[3])
        cls._driver.execute(cls._CREATE_DB)

    @classmethod
    def tearDownClass(cls):
        cls._driver.set_params(cls.PARAMS[0], '', cls.PARAMS[2], cls.PARAMS[3])
        cls._driver.execute(cls._DROP_DB)
        time.sleep(1)

    # def setUp(self):
    #     self._driver.set_params(*self.PARAMS)
    #     self._driver.execute("CREATE TABLE test;")
    #
    def tearDown(self):
        self._driver.set_params(*self.PARAMS)
        try:
            self._driver.execute("DROP TABLE test;")
        except:
            pass

    @property
    def driver(self):
        self._driver.set_params(*self.PARAMS)
        return self._driver

    def test_connect(self):
        self.driver.get_connection()

        self.driver.set_params(self.PARAMS[0], '', self.PARAMS[2], self.PARAMS[3])
        self.driver.get_connection()

    def test_db_type(self):
        assert self.driver.db_type(["n", int, None, "", 0, 0, 0], {}) == "BIGINT"
        assert self.driver.db_type(["n", str, None, "", 0, 0, 2], {}) == "VARCHAR(2)"

    def test_execute(self):
        self.driver.execute('CREATE TABLE test (id INT)'.format(self.DATABASE))
        assert True

    def _create(self):
        sql = self.driver.get_create('test', ['id INT'])
        self.driver.execute(sql)

    def test_execute_and_fetch(self):
        self._create()
        self.driver.execute('INSERT INTO test VALUES (%s)', [1])
        ret = self.driver.execute('SELECT * FROM test', fetch=True)
        assert ret == [{"id": 1}]

    def test_exists(self):
        self._create()
        assert self.driver.exists('test')
        assert not self.driver.exists('test_2')

        d = self.driver
        d.set_params(self.PARAMS[0], '', self.PARAMS[2], self.PARAMS[3])
        with pytest.raises(Exception):
            assert d.exists('test')

    def test_truncate(self):
        self._create()
        self.driver.execute('INSERT INTO test VALUES (%s)', [1])

        self.driver.truncate('test')
        ret = self.driver.execute('SELECT * FROM test', fetch=True)
        assert not ret

    def test_select(self):
        self._create()
        self.driver.execute('INSERT INTO test VALUES (%s)', [1])
        ret = self.driver.execute('SELECT * FROM test', fetch=True)
        assert ret == [{'id': 1}]

    def test_update(self):
        self.driver.execute('CREATE TABLE test (id INT, a INT, b INT)')
        self.driver.execute('INSERT INTO test VALUES (%s, %s, %s)', [1, 11, 12])
        self.driver.execute('INSERT INTO test VALUES (%s, %s, %s)', [2, 41, 42])

        self.driver.update('test', [('a', 3), ('b', 5)], [("id", 2)])
        ret = self.driver.execute('SELECT * FROM test', fetch=True)
        assert ret == [{u'a': 11, u'b': 12, u'id': 1},
                       {u'a': 3, u'b': 5, u'id': 2}]

    def test_update_all(self):
        self.driver.execute('CREATE TABLE test (id INT, a INT, b INT)')
        self.driver.execute('INSERT INTO test VALUES (%s, %s, %s)', [1, 11, 12])
        self.driver.execute('INSERT INTO test VALUES (%s, %s, %s)', [2, 41, 42])

        self.driver.update('test', [('a', 0), ('b', 0)])
        ret = self.driver.execute('SELECT * FROM test', fetch=True)
        assert ret == [{u'a': 0, u'b': 0, u'id': 1},
                       {u'a': 0, u'b': 0, u'id': 2}]
