# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import date, datetime, time
from decimal import Decimal
from types import NoneType

import psycopg2
import psycopg2.extras
from psycopg2._psycopg import ProgrammingError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .default import Driver as DefaultDriver


class Driver(DefaultDriver):
    RESERVED = ("char", "varchar", "int", "float")

    MAPPING = {datetime: 'DATE',
               date: 'DATE',
               time: 'TIME',
               str: 'VARCHAR',
               unicode: 'VARCHAR',
               # text: 'TEXT',
               int: 'BIGINT',
               Decimal: 'FLOAT',
               float: 'DOUBLE PRECISION',
               long: 'BIGINT',
               NoneType: 'VARCHAR',
               bool: 'BOOLEAN'
               }

    def exists(self, table):
        try:
            self.execute('SELECT 1 FROM {}'.format(table))
            return True
        except ProgrammingError:
            return False

    def _connect(self):
        conn = psycopg2.connect(host=self.host,
                                dbname=self.dbname,
                                user=self.username,
                                password=self.password,
                                cursor_factory=psycopg2.extras.RealDictCursor)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        return conn


driver = Driver()
