# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys
import tempfile
import shutil
import pytest

here = os.path.realpath(os.path.dirname(__file__))
src = os.path.join(here, os.pardir, "src")
sys.path.insert(0, src)

BASE = os.path.realpath(os.path.dirname(__file__))
DB = os.path.join(BASE, 'test.sqlite3')


@pytest.fixture
def target1():
    return os.path.join(BASE, 'xls.xls')


@pytest.fixture
def target2():
    return os.path.join(BASE, 'multiple.xls')


@pytest.fixture
def update1():
    return os.path.join(BASE, 'update1.xls')


@pytest.fixture
def update2():
    return os.path.join(BASE, 'update2.xls')


@pytest.fixture
def database():
    yield DB
    if os.path.exists(DB):
        os.unlink(DB)


@pytest.fixture
def tmpdir():
    curdir = os.curdir
    dir = tempfile.mkdtemp(suffix = 'tmp', prefix = 'xls_to_tb')
    os.chdir(dir)
    yield os.path.realpath(os.path.abspath(dir))
    os.chdir(curdir)
    shutil.rmtree(dir)
