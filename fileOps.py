#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
fileOps.py
----------
Provides os independant file manipulation functionality.
'''


import os
import os.path as osp
import logging
import glob
import stat
import hashlib


class FileError(Exception):
    pass

logger = logging.getLogger(__name__)

DIR_MASK = 0b10
FILE_MASK = 0b01


def size(file_path):
    return os.path.getsize(file_path)

def delete(file_path):
        os.remove(file_path)

def enumerate_dir(root_dir, mask=0b11, filter_fun=lambda x: True, recurse=False):
    if recurse:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            path_list = []
            if mask & DIR_MASK:
                dirnames = filter(filter_fun, dirnames)
                path_list = [os.path.join(dirpath, i) for i in dirnames]
            if mask & FILE_MASK:
                filenames = filter(filter_fun, filenames)
                path_list = [os.path.join(dirpath, i) for i in filenames]
            for i in path_list:
                yield i
    else:
        for e in (i for i in os.listdir(root_dir) if filter_fun(i)):
            yield e


def sanitize_path(path):
    return osp.normpath(path)


def ext_filter(file_extension):
    def f(file_path):
        _, file_ext = split_filename_ext(file_path)
        return file_ext == file_extension
    return f


def split_filename_ext(file_path):
    filename, ext = os.path.splitext(file_path)
    if ext != '':
        assert(ext[0] == '.')
        return filename, ext[1:]
    else:
        return filename, ext


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


def get_abs_path(file_name):
    return osp.abspath(file_name)


def get_abs_base_path(path):
    dir_name = osp.dirname(path)
    return osp.abspath(dir_name)


def construct_path(file_name, path):
    return osp.normpath(path + '/' + file_name)


def get_data(filename, mode='r'):
    logger.info('reading file: {}'.format(filename))
    try:
        with open(filename, mode) as f:
            data = f.read()
            return data
    except (OSError, IOError), e:
        raise FileError(e)


def append_data(filename, data):
    write_data(filename, data, mode='a')
    return


def write_data(filename, data, mode='w'):
    logger.info('writing file: {}'.format(filename))
    with open(filename, mode) as f:
        f.write(data)
    return


def get_non_blank_lines(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        non_blank_lines = [line for line in lines if line]
        return non_blank_lines


# just a wrapper
def open_file(file_path, mode):
    return open(file_path, mode)


def compute_hash(file_path):
    data = get_data(file_path, 'rb')
    m = hashlib.md5(data)
    md5sum = m.hexdigest()
    return md5sum
