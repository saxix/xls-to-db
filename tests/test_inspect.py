# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import pytest

from xls_to_db.parser import Parser

BASE = os.path.realpath(os.path.dirname(__file__))
DATABASE = 'xls'


@pytest.mark.parametrize("c", [True, False])
@pytest.mark.parametrize("f", ['xls.xls', 'xls.xlsx'])
def test_mysql(f, c):
    target = os.path.join(BASE, f)
    if c:
        p = Parser(target, file_content=open(target).read(), driver="mysql", prefix="test_")
    else:
        p = Parser(target, driver="mysql", prefix="test_")

    assert p.field_defs == [
        ['date DATETIME', 'time TIME', 'datetime DATETIME', 'char_3 VARCHAR(4)', 'int_4 BIGINT', 'field_0 BIGINT',
         'float_6 FLOAT', 'currency FLOAT', 'percentage FLOAT', 'fraction FLOAT', 'cap BIGINT', 'empty VARCHAR(5)',
         'aeiou BIGINT', 'bool BIGINT', 'formula FLOAT'],
        ['date DATETIME']]


@pytest.mark.parametrize("f", ['xls.xls', 'xls.xlsx'])
def test_sqlite(f):
    target = os.path.join(BASE, f)
    p = Parser(target, driver="sqlite3", prefix="test_")

    assert p.field_defs == [
        ['date DATE', 'time TIME', 'datetime DATE', 'char_3 VARCHAR(4)', 'int_4 BIGINT', 'field_0 BIGINT',
         'float_6 FLOAT', 'currency FLOAT', 'percentage FLOAT', 'fraction FLOAT', 'cap BIGINT',
         'empty VARCHAR(5)', 'aeiou BIGINT', 'bool BIGINT', 'formula FLOAT'], ['date DATE']]


@pytest.mark.parametrize("f", ['xls.xls', 'xls.xlsx'])
def test_pg(f):
    target = os.path.join(BASE, f)
    p = Parser(target, driver="postgresql", prefix="test_")

    assert p.field_defs == [
        ['date DATE', 'time TIME', 'datetime DATE', 'char_3 VARCHAR(4)', 'int_4 BIGINT', 'field_0 BIGINT',
         'float_6 FLOAT', 'currency FLOAT', 'percentage DOUBLE PRECISION', 'fraction DOUBLE PRECISION',
         'cap BIGINT', 'empty VARCHAR(5)', 'aeiou BIGINT', 'bool BIGINT', 'formula FLOAT'], ['date DATE']]
