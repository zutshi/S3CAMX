#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
c_info.py
---------
Defines machine's C types.
'''

import ctypes


def sizeof_double():
    return ctypes.sizeof(ctypes.c_double)


def sizeof_int():
    return ctypes.sizeof(ctypes.c_int)


def sizeof_char():
    return ctypes.sizeof(ctypes.c_char)
