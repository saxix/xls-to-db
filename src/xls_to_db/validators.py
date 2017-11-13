from __future__ import unicode_literals

import re

EMPTY_VALUES = (None, '', [], (), {})


def is_integer(v):
    return re.match(r'\d{1,}', v)
