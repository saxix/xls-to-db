XLS-to-DB
=========

Load data from xls/xlsx to database.

Simple library and command line utility to load xls/xlsx into database.

Features
--------

- analyse xls/xlsx and creates (or dump the sql clause) related table
- handle multiple sheet, creating one table per sheet
- support mysql/postgres/sqlite
- append/overwrite/update data


How to use it
-------------

Install
~~~~~~~

Install command line with PostgreSQL and MySQL support

    $ pip install xls-to-db[cli,postgres,mysql]


Use
~~~

simply dump create clause::

    $ xls-to-db my_xls.xls sql
    CREATE TABLE sheet1 (
     date DATE,
     time TIME,
     datetime DATE,
     char_3 VARCHAR(4),
     int_4 BIGINT,
     field_0 BIGINT,
     float_6 FLOAT,
     currency FLOAT,
     percentage FLOAT,
     fraction FLOAT,
     cap BIGINT,
     empty VARCHAR(5),
     aeiou BIGINT,
     bool BIGINT,
     formula FLOAT);
    CREATE TABLE sheet2 (date DATE)


create table into database ::

    $  xls-to-db samples/xls.xls create --driver pg --user root -d xls

create and load data ::

    $  xls-to-db samples/xls.xls create --driver pg --user root -d xls load

Help
----

 ::

    Usage: xls-to-db [OPTIONS] FILEPATH COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

      xls-to-db utility to work with xls and database

    Options:
      --driver [postgres|mysql|sqlite3]
                                      SQL syntax to use
      --prefix TEXT                   prefix to prepend to each sheet name
      --rows NUM                      number of row to use to get the data type
      --sheet SHEET                   if provided only works on this sheet
      -h, --host HOST                 database hostname/ip
      -d, --database DATABASE         database name
      -u, --username USER
      -p, --password PASSWORD
      --version                       Show the version and exit.
      --help                          Show this message and exit.

    Commands:
      create
      load
      sql


Internal API
------------

::

    Parser.set_connection()
    Parser.analyze()
    Parser.get_clauses()

    Parser.truncate()
    Parser.drop()
    Parser.update()
    Parser.append()
    Parser.create_table()


Create

::

    from xls_to_db.parser import Parser

    p = Parser(target, driver="postgresql", prefix="test_")
    p.set_connection('HOST', 'DATABSE', 'USERNAME', 'PASSWORD')
    p.create_table()


is equivalent to::

    xls-to-db samples/xls.xls create --driver pg --user root -d xls


Create and load

::

    from xls_to_db.parser import Parser

    p = Parser(target, driver="postgresql", prefix="test_")
    p.set_connection('HOST', 'DATABSE', 'USERNAME', 'PASSWORD')
    p.create_table()
    p.load()


is equivalent to::

    xls-to-db samples/xls.xls create --driver pg --user root -d xls load

