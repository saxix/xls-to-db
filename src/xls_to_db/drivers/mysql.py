# # -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pymysql
from pymysql.cursors import DictCursor

from .default import Driver as DefaultDriver


class Driver(DefaultDriver):
    def _connect(self):
        conn = pymysql.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            connect_timeout=5,
            cursorclass=DictCursor,
            use_unicode=True,
            charset="utf8")
        if self.dbname:
            conn.select_db(self.dbname)
        return conn

    def exists(self, table):
        try:
            self.execute('SELECT 1 FROM {}'.format(table))
            return True
        except Exception as e:
            if e.args[0] == 1146:
                return False
            raise


driver = Driver()
