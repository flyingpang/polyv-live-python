# coding: utf-8
__author__ = 'flyingpang'
"""Create at 2017.02.27"""


class PolyvException(Exception):
    """Base polyv Exception."""


class MissingParameterException(PolyvException):
    """Parameter is missing."""


class RequestException(PolyvException):
    """Request api error."""
