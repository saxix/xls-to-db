# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import re
import sqlite3
from contextlib import contextmanager

import pytest
from click.testing import CliRunner

from xls_to_db.compat import StringIO
from xls_to_db.cli import cli, echo


ansi_escape = re.compile(r'\x1b[^m]*m')


@contextmanager
def temp_environ(**kwargs):
    _environ = dict(os.environ)
    for k, v in kwargs.items():
        os.environ[k] = v
    yield
    os.environ.clear()
    os.environ.update(_environ)


@pytest.fixture()
def runner(monkeypatch):
    runner = CliRunner(echo_stdin=True)
    monkeypatch.setattr('click.confirm', lambda *k : 'y')
    monkeypatch.setattr('click.prompt', lambda prompt, default: default or "<value>")
    monkeypatch.setattr('click.core.Option.prompt_for_value', lambda *k: '')
    return runner


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert result.output.find("Usage") == 0


def test_display(runner, target1):
    result = runner.invoke(cli, [target1, 'sql', '--plain', '-l'], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert result.output == "CREATE TABLE sheet1 (date DATE, time TIME, datetime DATE, " \
                            "char_3 VARCHAR(4), int_4 BIGINT, field_0 BIGINT, float_6 FLOAT, " \
                            "currency FLOAT, percentage FLOAT, fraction FLOAT, cap BIGINT, " \
                            "empty VARCHAR(5), aeiou BIGINT, bool BIGINT, formula FLOAT);" \
                            "CREATE TABLE sheet2 (date DATE)\n"


def test_apply(runner, target1, database):
    result = runner.invoke(cli, [target1, 'sql', '--plain', 'create',
                                 '-d', database], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sheet1")
    assert len(cur.fetchall()) == 0


def test_load(runner, target1, database):

    result = runner.invoke(cli, [target1, 'create', '-d', database, 'load'],
                           catch_exceptions=False)

    assert result.exit_code == 0, result.output
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sheet1")
    assert cur.fetchone() == (u'1966-07-19', u'17:00:00', u'1900-04-09', u'char', 10, -10, 10.0, 10.0, 0.1, 0.25, 144, u'', 10, 1, 6.0)


def test_single_sheet(runner, target1, database):
    result = runner.invoke(cli, [target1, 'sql', '--plain', '-l', '--sheet', 1],
                           catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert result.output == "CREATE TABLE sheet2 (date DATE)\n"


def test_highlight(runner, target1, monkeypatch):
    result = runner.invoke(cli, [target1, 'sql', '--sheet', 1], catch_exceptions=False)

    assert result.exit_code == 0, result.output
    assert ansi_escape.sub('', result.output) == "CREATE TABLE sheet2 (\n date DATE)\n\n"


# def test_aliases(runner, ):
#     result = runner.invoke(cli, [__file__, '--driver', 'pg'])
#     assert result.output == "File type 'py' is not supported for read.\n"
#
#     result = runner.invoke(cli, [__file__, '--driver', 'sqlite'])
#     assert result.output == "File type 'py' is not supported for read.\n"


def test_echo(monkeypatch):
    buffer = StringIO()
    monkeypatch.setattr("sys.stdout", buffer)
    echo("SELECT FROM DUAL")
    echo("SELECT FROM DUAL", lexer='mysql')
    echo("SELECT FROM DUAL", lexer='postgresql')
    echo("SELECT FROM DUAL", lexer='sqlite3')
    echo("SELECT FROM DUAL", lexer='invalid')
    echo("SELECT FROM DUAL", lexer='invalid', raw=True)
