# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class ParserException(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(ParserException, self).__init__(*args)


class UnsupportedFileError(ParserException):
    pass


class InsertError(ParserException):
    pass


class LineParseError(ParserException):
    pass


class ValidationError(ParserException):
    pass


class InvalidFieldNameError(ParserException):
    def __init__(self, field_name, column=None, *args, **kwargs):
        self.field_name = field_name
        self.column = column
        super(InvalidFieldNameError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Invalid field name '%s' on column #%s" % (self.field_name, chr(ord('A') + self.column))

# class UknkownCellException(ParserException):
#     def __init__(self, row, col, value=None, *args):
#         self.row = row
#         self.col = col
#         self.value = value
#
#     def __str__(self):
#         return "Unable to parse value of column {0.col} on row {0.row}. ({0.value})".format(self)
