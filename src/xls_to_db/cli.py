# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

import click
from click import Choice
from pygments import formatters, highlight, lexers

from .parser import Parser

_global_options = [
    click.option('--driver', default="sqlite3",
                 type=Choice(["postgres", "mysql", "sqlite3"]),
                 help="SQL syntax to use"),
    click.option('--prefix', default="",
                 help="prefix to prepend to each sheet name"),
    click.option('--rows', default=100,
                 metavar="NUM",
                 help="number of row to use to get the data type"),
    click.option('--sheet', default=None, type=int,
                 metavar="SHEET",
                 help="if provided only works on this sheet"),
]

_db_options = [
    click.option('-h', '--host', default='localhost',
                 metavar="HOST", help="database hostname/ip"),
    click.option('-d', '--database', default=":memory:",
                 metavar="DATABASE",
                 help="database name"),
    click.option('-u', '--username', metavar="USER", ),
    click.option('-p', '--password', metavar="PASSWORD", )
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


def db_options(func):
    for option in reversed(_db_options):
        func = option(func)
    return func


def get_version():
    try:
        import pkg_resources  # part of setuptools
        return pkg_resources.require("xls-to-db")[0].version
    except:
        return "UNKNOWN"


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


@click.group(chain=True)
@global_options
@db_options
@click.argument('xls', type=click.File('rb'), metavar="FILEPATH")
@click.version_option(version=get_version())
@click.pass_context
def cli(ctx, xls, driver, **kwargs):
    """xls-to-db utility to work with xls and database"""
    ctx.obj = {"xls": xls}


@cli.command()
@global_options
@click.option('--plain', is_flag=True, default=False,
              help="do not highlight text")
@click.option('-l', '--single-line', is_flag=True, default=False,
              help="dump sql in a signle line")
@click.pass_context
def sql(ctx, plain, single_line, driver, rows, prefix, sheet):
    xls = ctx.obj["xls"]
    try:
        p = Parser(xls.name, driver, analyze_rows=rows, prefix=prefix)
        ctx.obj["p"] = p

        if sheet:
            p.selection = range(sheet, sheet + 1)

        sql = p.get_sql()
        if not single_line:
            sql = sql.replace(',', ',\n').replace('(', '(\n ', 1).replace(';', ';\n')
        echo(sql, plain)

    except Exception as e:
        click.echo(click.style(str(e), fg='red'), err=True)


@cli.command()
@global_options
@db_options
@click.pass_context
def create(ctx, driver, rows, prefix, sheet,
          host, database, username, password):
    try:
        xls = ctx.obj["xls"]
        if "p" not in ctx.obj:
            p = Parser(xls.name, driver, analyze_rows=rows, prefix=prefix)
            ctx.obj["p"] = p

        ctx.obj['database'] = database
        ctx.obj["p"].set_connection(host, database, username, password)
        ctx.obj["p"].create_table()

    except Exception as e:
        click.echo(click.style(str(e), fg='red'), err=True)


@cli.command()
@global_options
@db_options
@click.pass_context
def load(ctx, driver, rows, prefix, sheet,
         host, username, password, database):
    try:
        xls = ctx.obj["xls"]
        if "p" not in ctx.obj:
            p = Parser(xls.name, driver, analyze_rows=rows, prefix=prefix)
            ctx.obj["p"] = p
        if "database" in ctx.obj:
            database = ctx.obj["database"]

        ctx.obj["p"].set_connection(host, database, username, password)
        ctx.obj["p"].load()
    except Exception as e:
        click.echo(click.style(str(e), fg='red'), err=True)
