from __future__ import print_function

import fileOps as f
import err

import logging

#EXAMPLE_LIST_FN = 'example_list'

example_list_str = \
    '''0_vanDerPol = ./examples/vanderpol_python/
    1_vanDerPol = ./examples/vanderpol_m_file/
    2_dc = ./examples/dc_controller_hand_coded/
    3_dci = ./examples/dc_controller_hand_coded_input/
    4_ex1a = ./examples/ex1a/
    5_ex1b = ./examples/ex1b/
    6_AbstractFuelControl = ./examples/abstractFuelControl/
    7_AbstractFuelControl = ./examples/abstractFuelControlCombined/
    8_fuzzy_invp = ./examples/fuzzy_invp/
    9_heater = ./examples/heater/
    10_GIF = ./examples/GI_fisher/'''

logger = logging.getLogger(__name__)


def get_example_list():
    return crawl_examples()


def crawl_examples():
    EXAMPLE_DICT = './examples/'
    TST_FILE_GLOB_PATTERN = '*.tst'

    example_list = []

    sub_dir_list = f.get_sub_dir_listing(EXAMPLE_DICT)
    for sub_dir in sub_dir_list:
        file_name_list = f.get_file_list_matching(TST_FILE_GLOB_PATTERN, sub_dir)
        if len(file_name_list) > 1:
            raise err.Fatal('More than one .tst file found!! {}'.format(file_name_list))
        if len(file_name_list) != 0:
            file_path = f.get_abs_base_path(file_name_list[0])
            system_name = f.get_file_name_from_path(file_name_list[0])

            d = {}
            d['filename'] = system_name
            d['path'] = file_path
            d['description'] = '{:-<50} {}'.format(system_name, file_path)
            example_list.append(d)

    return example_list

if __name__ == '__main__':
    for i in crawl_examples():
        print(i['description'])
