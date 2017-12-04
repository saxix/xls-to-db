# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import psycopg2
import pymysql
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from xls_to_db.parser import Parser

BASE = os.path.realpath(os.path.dirname(__file__))
DATABASE = 'xls'


def setup_module():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='')
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE))
    cur.execute("CREATE DATABASE {};".format(DATABASE))
    conn.commit()

    conn = psycopg2.connect("host='localhost' user='root' dbname='postgres'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE))
    cur.execute("CREATE DATABASE {};".format(DATABASE))
    conn.commit()


def teardown_module():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='')
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE))

    conn = psycopg2.connect("host='localhost' user='root' dbname='postgres'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS {};".format(DATABASE))

    if os.path.exists(DATABASE):
        os.unlink(DATABASE)


@pytest.mark.parametrize("driver", ["mysql", "sqlite3", "postgresql"])
def test_driver_xls(driver):
    target = os.path.join(BASE, 'xls.xls')
    p = Parser(target, driver=driver, prefix="test_")
    p.set_connection('localhost', 'xls', 'root', '')

    p.create_table(skip_if_exists=True)
    p.load()
    r = next(p.dump())
    assert r


@pytest.mark.parametrize("driver", ["mysql", "sqlite3", "postgresql"])
def test_driver_xlsx(driver):
    target = os.path.join(BASE, 'xls.xlsx')
    p = Parser(target, driver=driver, prefix="test_")
    p.set_connection('localhost', 'xls', 'root', '')

    p.create_table(skip_if_exists=True)
    p.load()
    r = next(p.dump())
    assert r


@pytest.mark.parametrize("driver", ["mysql", "sqlite3", "postgresql"])
def test_driver_csv(driver):
    target = os.path.join(BASE, 'xls.csv')
    p = Parser(target, driver=driver, prefix="test_")
    p.set_connection('localhost', 'xls', 'root', '')
    p.create_table(skip_if_exists=True)
    p.load()
    r = next(p.dump())
    assert r
