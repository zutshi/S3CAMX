#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
err.py
------
Provides templates for exceptions.
'''

import blessings

term = blessings.Terminal()


class Fatal(Exception):

    pass


class FileNotFound(Exception):

    pass


def error(msg):
    print 'ERROR: ' + msg
    exit(-1)


def warn(msg):
    print term.red('WARNING: ' + msg)


def warn_severe(msg):
    print term.red('WARNING: ' + msg)
    # forces the user to take heed!
    raw_input('please acknowledge by pressing enter')


def int_error(msg):
    print 'INTERNAL ERROR: ' + msg
    exit(-1)
