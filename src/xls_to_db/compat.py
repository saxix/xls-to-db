# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

if sys.version_info >= (3, 0):
    NoneType = type(None)
    long = int
    unicode = str
    from io import BytesIO as StringIO
else:
    from types import NoneType
    from StringIO import StringIO
