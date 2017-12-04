# # -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    import MySQLdb as mysql
    from MySQLdb.cursors import DictCursor
except ImportError:
    import pymysql as mysql
    from pymysql.cursors import DictCursor

from .default import Driver as DefaultDriver


class Driver(DefaultDriver):
    def _connect(self):
        conn = mysql.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            connect_timeout=5,
            port=self.port or 3306,
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
