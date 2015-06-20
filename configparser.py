#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


def parse_config(description_str):
    output_dict = {}

    # ##!!##logger.debug('parsing abstraction parameters')

    # split the description into lines by breaking at "\n"

    description_arr = description_str.splitlines()

    for l in description_arr:

        # assume it as a comment and move on

        if l[0] == '#':
            continue

        # split each line on "="

        parameter_def = l.split('=')

        # strip leading and trailing whitespaces

        parameter_name = parameter_def[0].strip()
        parameter_val = parameter_def[1].strip()
        output_dict[parameter_name] = parameter_val

    # store the RHS type of the output dict, i.e., all RHS are strings

    output_dict['type'] = 'string'
    return output_dict
