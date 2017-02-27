# coding: utf-8
__author__ = 'flyingpang'
"""Create at 2017.02.27"""
import hashlib


def make_sign(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest().upper()
