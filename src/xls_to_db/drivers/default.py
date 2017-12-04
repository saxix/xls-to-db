# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import date, datetime, time
from decimal import Decimal
from time import struct_time
from types import NoneType

import sys


class Driver(object):
    TYPE_NUM = (int, long, float, Decimal)
    TYPE_STR = (str, unicode)
    TYPE_DATES = (datetime,)
    ORDER = (None, NoneType, int, long, float, Decimal,
             str, unicode, date, time, datetime)

    RESERVED = ("char", "varchar", "int", "float")

    MAPPING = {datetime: 'DATETIME',
               date: 'DATE',
               time: 'TIME',
               struct_time: 'TIME',
               str: 'VARCHAR',
               unicode: 'VARCHAR',
               int: 'BIGINT',
               float: 'FLOAT',
               Decimal: 'FLOAT',
               long: 'BIGINT',
               NoneType: 'VARCHAR',
               bool: 'BOOLEAN'
               }

    def __init__(self):
        self.host = None
        self.dbname = None
        self.username = None
        self.password = None

    def set_params(self, host, dbname, username, password):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password

    def get_create(self, table, field_defs, sep=", "):
        return "CREATE TABLE {table} ({fields})".format(table=table,
                                                        fields=sep.join(field_defs))

    def _connect(self):
        raise NotImplementedError

    def exists(self, table):
        raise NotImplementedError

    def get_connection(self):
        self._conn = self._connect()
        return self._conn

    def execute(self, sql, params=None, silent=False, fetch=False):
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, params or [])
            conn.commit()
            if fetch:
                return cur.fetchall()
        except Exception as e:
            raise
            # a,b,c = sys.exc_info()
            # raise a, """Error executing query:
# Sql:{}
# Params: {}
# Error: {}
#             """.format(sql, params, e), c
        finally:
            conn.close()

    def truncate(self, table):
        stm = r"TRUNCATE {table};".format(table=table)
        self.execute(stm)

    def update(self, table, values, where=None):
        template = "UPDATE {table} SET {values} {where}"
        assignment = ",".join(["{}=%s".format(a, b) for a, b in values])
        values = [b for a, b in values]
        if where:
            values.extend([b for a, b in where])
            where = "WHERE " + " AND ".join(["{}=%s".format(a, b) for a, b in where])
        else:
            where = ""

        sql = template.format(table=table, values=assignment, where=where)
        self.execute(sql, values)

    def db_type(self, col_defs, config):
        (name, typ, cast, fmt, min_value, max_value, max_length) = col_defs
        t = self.MAPPING[typ]
        if t == 'VARCHAR':
            t = 'VARCHAR(%s)' % max(max_length, config.get('varchar_min', 0))
        return t
