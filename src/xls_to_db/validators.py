# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import time

from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal
import locale

locales = ('en_AU.utf-8', 'en_BW.utf-8', 'en_CA.utf8',
           'en_DK.utf-8', 'en_GB.utf8', 'en_HK.utf-8', 'en_IE.utf-8', 'en_IN', 'en_NG',
           'en_PH.utf-8', 'en_US.utf-8', 'en_ZA.utf-8',
           'en_ZW.utf-8', 'ja_JP.utf-8')

SYMBOLS = []
CODES = []
for l in locales:
    try:
        locale.setlocale(locale.LC_ALL, l)
    except:
        pass
    else:
        conv = locale.localeconv()
        CODES.append(conv['int_curr_symbol'].strip())
        SYMBOLS.append(conv['currency_symbol'].decode('utf8').replace('$', r'\$'))


EMPTY_VALUES = (None, '', [], (), {})


def is_integer(v):
    return re.match(r'\d{1,}', v)


def parse_bool(v):
    if v in ('true', 'TRUE', 'True', 'Yes', 'yes', 'YES'):
        return True
    elif v in ('false', 'FALSE', 'False', 'No', 'no', 'NO'):
        return False
    raise ValueError


def parse_date(v):
    """
    >>> parse_date("Monday, 7 Mar 2013 8:00")
    datetime.datetime(2013, 3, 7, 8, 0)

    >>> parse_date("7 Mar 2013 8:00")
    datetime.datetime(2013, 3, 7, 8, 0)

    >>> parse_date("7 Mar 2013")
    datetime.date(2013, 3, 7)
    """
    if len(v) > 5:
        parsed = parse(v)
        if ':' not in v:
            return parsed.date()
        return parsed
    raise ValueError


M = u"|".join(CODES+SYMBOLS)
rex = re.compile(r'(%s) *([+-]*\d.*)' % M)


def parse_currency(v):
    """
    >>> parse_currency('1.0')
    Traceback (most recent call last):
      ...
    ValueError

    >>> parse_currency('$1.0')
    Decimal('1.0')

    >>> parse_currency('$-1.0')
    Decimal('-1.0')

    >>> parse_currency('USD 1.0')
    Decimal('1.0')

    """
    m = rex.findall(v)
    if m:
        try:
            return Decimal(m[0][1])
        except:
            pass
    raise ValueError


def parse_number(v):
    """
    >>> parse_number("1.0")
    Decimal('1.0')
    >>> parse_number("1")
    1
    >>> parse_number("-1")
    -1
    """
    try:
        if "." in str(v):
            try:
                return Decimal(v)
            except:
                pass
        try:
            return int(v)
        except:
            raise ValueError
    except:
        raise ValueError


def parse_time(v):
    """
    >>> parse_time(u'17:00:00')
    time.struct_time(tm_year=1900, tm_mon=1, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=1, tm_wday=0, tm_yday=1, tm_isdst=-1)
    """
    if re.search(r'^\d\d:\d\d:{0,1}', v):
        parts = v.split(':')
        sec = int(parts[0]) * 3600 + int(parts[1]) * 60
        if len(parts) == 3:
            sec += int(parts[2])
        return datetime.fromtimestamp(time.gmtime(sec)).time()
        # return time.gmtime(sec)

    raise ValueError
