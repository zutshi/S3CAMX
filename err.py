#!/usr/bin/python
# -*- coding: utf-8 -*-


import blessed

term = blessed.Terminal()


class Fatal(Exception):

    pass


class FileNotFound(Exception):

    pass


def error(msg):
    print 'ERROR: ' + msg
    exit(-1)


def warn(msg):
    print term.red_on_white('WARNING: ' + msg)


def warn_severe(msg):
    print term.red_on_white('WARNING: ' + msg)
    # forces the user to take heed!
    raw_input('please acknowledge by pressing enter')


def int_error(msg):
    print 'INTERNAL ERROR: ' + msg
    exit(-1)
