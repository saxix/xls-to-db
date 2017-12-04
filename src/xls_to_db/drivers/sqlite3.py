# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlite3
from datetime import date, datetime, time
from decimal import Decimal
from time import struct_time
from types import NoneType

from .default import Driver as DefaultDriver


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Driver(DefaultDriver):
    RESERVED = ("char", "varchar", "int", "float")

    MAPPING = {datetime: 'DATE',
               date: 'DATE',
               time: 'TIME',
               struct_time: 'TIME',
               str: 'VARCHAR',
               unicode: 'VARCHAR',
               int: 'BIGINT',
               Decimal: 'FLOAT',
               float: 'FLOAT',
               long: 'BIGINT',
               NoneType: 'VARCHAR',
               bool: 'BOOLEAN'
               }

    def _connect(self):
        self._conn = sqlite3.connect(self.dbname)
        self._conn.row_factory = dict_factory
        return self._conn

    def exists(self, table):
        try:
            self.execute('SELECT 1 FROM {}'.format(table), silent=True)
            return True
        except sqlite3.OperationalError:
            return False

    def execute(self, sql, params=None, silent=False, fetch=False):
        sql = sql.replace("%s", "?")
        return super(Driver, self).execute(sql, map(str, params or []),
                                           silent, fetch)

    def truncate(self, table):
        stm = r"DELETE FROM {table};".format(table=table)
        self.execute(stm)


driver = Driver()
