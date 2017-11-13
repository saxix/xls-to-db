# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

import click
from pygments import formatters, highlight, lexers

from .parser import Parser


def echo(sql, raw=False, lexer='sql'):
    if lexer == 'mysql':
        lexer = lexers.MySqlLexer()
    elif lexer == 'sqlite3':
        lexer = lexers.SqliteConsoleLexer()
    elif lexer == 'postgresql':
        lexer = lexers.PostgresConsoleLexer()
    else:
        lexer = lexers.SqlLexer()

    if not raw:
        sql = highlight(sql, lexer,
                        formatters.TerminalFormatter())
    sys.stdout.write(sql)
    sys.stdout.write("\n")
    sys.stdout.flush()


@click.command()
@click.argument('xls', type=click.File('rb'))
@click.option('--driver', default="sqlite3", )
@click.option('--prefix', default="")
@click.option('--plain', is_flag=True, default=False)
@click.option('--drop', is_flag=True, default=False)
@click.option('--sheet', default=None, type=int)
@click.option('-l', '--single-line', is_flag=True, default=False)
@click.option('--apply', is_flag=True, default=False)
@click.option('--load', is_flag=True, default=False)
@click.option('--rows', default=100)
@click.option('-h', '--host', default='localhost')
@click.option('-d', '--database', default=":memory:")
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.pass_context
def cli(ctx, xls, driver, plain, single_line, rows, prefix,
        sheet,
        drop, apply, load,
        host, database, username, password):
    try:
        if driver in ["pg", "postgres"]:
            driver = "postgresql"
        elif driver in ["sqlite", ]:
            driver = "sqlite3"
        p = Parser(xls.name, driver, analyze_rows=rows, prefix=prefix)
        p.set_connection(host, database, username, password)
        if sheet:
            p.selection = range(sheet, sheet + 1)

        sql = p.get_sql()
        if not single_line:
            sql = sql.replace(',', ',\n').replace('(', '(\n ', 1).replace(';', ';\n')
        echo(sql, plain)

        if apply:
            p.create_table()

        if load:
            p.load()
    except Exception as e:
        click.echo(click.style(str(e), fg='red'), err=True)
