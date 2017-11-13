# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import importlib


def import_by_name(name):
    """dynamically load a class from a string

    eg:
        klass = import_by_name('my_package.my_module.my_class')
        some_object = klass()

    :param name:
    :return:

    >>> import_by_name("wfp_commonlib.path.Path")
    Traceback (most recent call last):
    ...
    ImportError: No module named path

    >>> import_by_name("wfp_commonlib.python.structure.RexList")
    <class 'wfp_commonlib.python.structure.RexList'>

    >>> import_by_name("wfp_commonlib.python.RexList")
    <class 'wfp_commonlib.python.structure.RexList'>

    """
    class_data = name.split('.')
    module_path = '.'.join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    return getattr(module, class_str)
