#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path as osp
import logging
import err
import glob
import stat

logger = logging.getLogger(__name__)


def split_filename_ext(file_path):
    filename, ext = os.path.splitext(file_path)
    if ext[0] == '.':
        pass
    else:
        raise err.Fatal('unexpected: something wrong?')
    return filename, ext[1:]


def make_exec(file_path):
    old_fp = stat.S_IMODE(os.stat(file_path).st_mode)
    new_fp = old_fp | stat.S_IXUSR
    os.chmod(file_path, new_fp)


def get_file_name_from_path(path_str):
    return os.path.basename(path_str)


def get_sub_dir_listing(path_str):
    abs_path_str = get_abs_base_path(path_str)
    listing_with_path = [construct_path(i, abs_path_str) for i in os.listdir(abs_path_str)]
    return [i for i in listing_with_path if os.path.isdir(i)]


def validate_file_names(file_name_list):
    return all([osp.exists(fn) for fn in file_name_list])


def file_exists(file_name):
    return osp.exists(file_name)


def get_file_list_matching(pattern_str, file_path='./'):
    fpp = construct_path(pattern_str, file_path)
    return glob.glob(fpp)


def is_dir_empty(dir_path):
    return os.listdir(dir_path) == []


def make_dir(dir_path):
    os.makedirs(dir_path)


def make_n_change_dir(dir_path):
    os.makedirs(dir_path)
    os.chdir(dir_path)


def get_abs_base_path(path):
    dir_name = osp.dirname(path)
    return osp.abspath(dir_name)


def construct_path(file_name, path):
    return osp.normpath(path + '/' + file_name)


def get_data(filename):
    logger.info('reading file: {}'.format(filename))
    try:
        with open(filename, 'r') as f:
            data = f.read()
            return data
    except (OSError, IOError), e:
        raise err.FileNotFound(e)


def append_data(filename, data):
    logger.info('writing file: {}'.format(filename))
    with open(filename, 'a') as f:
        f.write(data)
        return


def write_data(filename, data):
    logger.info('writing file: {}'.format(filename))
    with open(filename, 'w') as f:
        f.write(data)
        return


def get_non_blank_lines(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        non_blank_lines = [line for line in lines if line]
        return non_blank_lines
