import scipy.io

ORIGINAL_BENCMARK_PATH = './examples/heat/heat/'
MAT_FILE = 'heat{:02}.mat'
#TODO: already implemented in fileOps!!! REUSE!
import os.path as osp


def get_abs_base_path(path):
    dir_name = osp.dirname(path)
    return osp.abspath(dir_name)


def construct_path(file_name, path):
    return osp.normpath(path + '/' + file_name)


def get_params(benchmark_id):
    mat_file_name = MAT_FILE.format(benchmark_id)
    mat_file_path = construct_path(mat_file_name, get_abs_base_path(ORIGINAL_BENCMARK_PATH))
    mat_dict = scipy.io.loadmat(mat_file_path)
    return mat_dict


def get_benchmark_inits(benchmark_id):
    mat_dict = get_params(benchmark_id)
    X0 = None
    Xf = None
    H0 = None
    NUM_ROOMS = None
    return X0, Xf, H0, NUM_ROOMS


def create_benchmark_specefic_controller_header(benchmark_id):
    pass
