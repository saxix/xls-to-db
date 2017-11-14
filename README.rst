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

simply dump create clause::

    $ xls-to-db my_xls.xls
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

    $  xls-to-db samples/xls.xls --driver pg --user root -d xls --apply

create and load data ::

    $  xls-to-db samples/xls.xls --driver pg --user root -d xls --apply --load
