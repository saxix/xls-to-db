# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sqlite3
from datetime import datetime, date, time
import pytest

from xls_to_db.exceptions import InvalidFieldNameError
from xls_to_db.parser import Parser, inspect_column


@pytest.fixture
def cursor(target2, database):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [4]
    p.create_table()
    p.load()

    conn = sqlite3.connect(database)
    return conn.cursor()


@pytest.fixture
def cursor_update(update1, database):
    p = Parser(update1, driver='sqlite3', prefix='test_')
    p.set_connection('', database, '', '')
    p.create_table()
    p.load()

    conn = sqlite3.connect(database)
    return conn.cursor()


def test_selection(target1):
    p = Parser(target1, driver="postgresql", prefix="test_")
    p.selection = [1]
    p.analyze()
    s = p.get_sql()
    assert p.field_defs == [['date DATE']]
    assert s == "CREATE TABLE test_sheet2 (date DATE)"
    with pytest.raises(ValueError):
        p.selection = [4]


def test_parser(target1):
    p = Parser(target1,
               file_content=open(target1).read(),
               driver="postgresql", prefix="test_")
    p.selection = [1]
    p.analyze()
    s = p.get_sql()
    assert p.field_defs == [['date DATE']]
    assert s == "CREATE TABLE test_sheet2 (date DATE)"


def test_invalid_field(target2):
    p = Parser(target2)
    p.selection = [0]
    with pytest.raises(InvalidFieldNameError):
        p.field_defs

    p = Parser(target2)
    p.selection = [1]
    assert p.field_defs


def test_reserved_name(target2):
    p = Parser(target2)
    p.selection = [1]
    ret = p.get_sql()
    assert ret == 'CREATE TABLE reserved (varchar_0 BIGINT)'


def test_empty_sheet(target2):
    p = Parser(target2)
    p.selection = [2]
    ret = p.get_clauses()
    assert ret == []


def test_empty_col(target2):
    p = Parser(target2)
    p.selection = [3]
    ret = p.get_clauses()
    assert ret == [u'CREATE TABLE empty_col (aa BIGINT, bb VARCHAR(2), field_3 VARCHAR(0), dd VARCHAR(2))']


def test_create_table(target2, database):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [3]
    p.create_table()
    with pytest.raises(Exception):
        p.create_table()

    p.create_table(skip_if_exists=True)


def test_drop(target2, database, cursor):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [4]
    # p.create_table()
    p.drop()
    p.drop()  # do not raise error


def test_load(target2, database, cursor):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [4]
    p.load()

    cursor.execute('SELECT * FROM {}'.format(p._names[4]))
    assert cursor.fetchall() == [(1, 11, u'c1'),
                                 (2, 12, u'c2'),
                                 (3, 13, u'c3'),
                                 (1, 11, u'c1'),
                                 (2, 12, u'c2'),
                                 (3, 13, u'c3'),
                                 ]


def test_truncate(target2, database, cursor):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [4]
    p.truncate()


def test_update(update2, database, cursor_update):
    p = Parser(update2, driver='sqlite3', prefix="test_")
    p.set_connection('', database, '', '')

    # sanity check
    cursor_update.execute('SELECT * FROM {}'.format(p.table_names[0]))
    assert cursor_update.fetchall() == [(1, u'a1', u'b1'),
                                        (2, u'a2', u'b2'),
                                        (3, u'a3', u'b3')]

    p.update(0)
    cursor_update.execute('SELECT * FROM {}'.format(p._names[0]))
    assert cursor_update.fetchall() == [(1, u'a1', u'B100'),
                                        (2, u'a200', u'b2'),
                                        (3, u'a3', u'b3')]


def test_dump(target2, database, cursor):
    p = Parser(target2, driver='sqlite3')
    p.set_connection('', database, '', '')
    p.selection = [4]
    result = list(p.dump())
    assert result == [[{'a': 1, 'c': u'c1', 'b': 11},
                       {'a': 2, 'c': u'c2', 'b': 12},
                       {'a': 3, 'c': u'c3', 'b': 13}]]


def test_inspect_column():
    ret = inspect_column([datetime.today().date()], {})
    assert ret[0] == date

    ret = inspect_column([datetime.today().time()], {})
    assert ret[0] == time

    ret = inspect_column([datetime(2000, 1, 1)], {})
    assert ret[0] == datetime

    ret = inspect_column([1, "a"], {})
    assert ret[0] == unicode

    ret = inspect_column(["a", datetime.today(), 1], {})
    assert ret[0] == unicode

    ret = inspect_column([], {})
    assert ret[0] == str
