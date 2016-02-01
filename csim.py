#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
csim.py
--------
Controller Simulator.
Provides the low level functionality to call the controller shared
object using ctypes.
'''

import ctypes as ct

# Can also use os along with platform?
# import os

import platform

import numpy as np

# TODO: Better way to use ndpointer, but lets do that later
# from numpy.ctypeslib import ndpointer

import logging

import err
import controlifc as cifc
import collections

logger = logging.getLogger(__name__)


# ###################################################
# Low level INTERFACE to C controller
# ###################################################
# TODO:
# Make proper meta class interface
def InputValCT_meta(num_dims):#num_inputs, num_states, num_x):
    # TODO: above classes ar eonw being dynamically created to circumvent the
    # error: _Attributeerror _fields_ is final
    # Make sure we udnerstand if this is OK, and clean up.

    InputValCT = type('InputValCT', (ct.Structure,), {})
    InputValCT._fields_ = [('input_arr', ct.POINTER(ct.c_double * num_dims.ci)),
                           ('int_state_arr', ct.POINTER(ct.c_int * num_dims.si)),
                           ('float_state_arr', ct.POINTER(ct.c_double * num_dims.sf)),
                           ('x_arr', ct.POINTER(ct.c_double * num_dims.x))]

    def split_controller_state(state_array, num_dims):
        return state_array[0:num_dims.si], state_array[num_dims.si:]

    def init(self, to_controller_data):

        int_state_array, float_state_array = \
            split_controller_state(to_controller_data.state_array, num_dims)

        c_input_array = get_double_array_from_double_list(to_controller_data.input_array)
        int_state_array = map(int, int_state_array)
        c_int_state_array = get_int_array_from_int_list(int_state_array)
        c_float_state_array = get_double_array_from_double_list(float_state_array)
        c_x_array = get_double_array_from_double_list(to_controller_data.x_array)

        p_c_input_array = ct.pointer(c_input_array)
        p_c_int_state_array = ct.pointer(c_int_state_array)
        p_c_float_state_array = ct.pointer(c_float_state_array)
        p_c_x_array = ct.pointer(c_x_array)
        super(InputValCT, self).__init__(
            p_c_input_array,
            p_c_int_state_array,
            p_c_float_state_array,
            p_c_x_array)
        return

    InputValCT.__init__ = init
    return InputValCT


def RetValCT_meta(num_dims):#num_states, num_outputs):

    RetValCT = type('RetValCT', (ct.Structure,), {})
    RetValCT._fields_ = [('int_state_arr', ct.POINTER(ct.c_int * num_dims.si)),
                         ('float_state_arr', ct.POINTER(ct.c_double * num_dims.sf)),
                         ('output_arr', ct.POINTER(ct.c_double * num_dims.u))]

    def combine_controller_state(int_state_array, float_state_array):
        return int_state_array + float_state_array

    def init(self):
        c_int_state_array = get_int_array_from_int_list([0] * num_dims.si)
        c_float_state_array = get_double_array_from_double_list([0] * num_dims.sf)
        c_output_array = get_double_array_from_double_list([0] * num_dims.u)

        p_c_int_state_array = ct.pointer(c_int_state_array)
        p_c_float_state_array = ct.pointer(c_float_state_array)
        p_c_output_array = ct.pointer(c_output_array)
        super(RetValCT, self).__init__(
            p_c_int_state_array,
            p_c_float_state_array,
            p_c_output_array)
        return

    @property
    def from_controller(self):
        int_state_array = [i for i in self.int_state_arr.contents]
        float_state_array = [i for i in self.float_state_arr.contents]
        state_array = combine_controller_state(int_state_array, float_state_array)
        output_array = [i for i in self.output_arr.contents]
        return cifc.FromController(state_array, output_array)

    RetValCT.__init__ = init
    RetValCT.from_controller = from_controller
    return RetValCT


def wrap_controller_scaleNround(controller_call_fun, cf):

    def wraped_call(tcd):
        err.warn('wraped_call being used!')
        tcd.input_array = np.array([int(round(i * cf)) for i in
                                   tcd.input_array])
        tcd.state_array = np.array([int(round(i * cf)) for i in
                                   tcd.state_array])
        tcd.x_array = np.array([int(round(i * cf)) for i in tcd.x_array])

#        tcd.state_array = (tcd.state_array * cf).astype(int)
#        tcd.x_array = (tcd.x_array * cf).astype(int)

        fcd = controller_call_fun(tcd)

        # WHY ROUND here???
        # fcd.state_array = list((np.round(fcd.state_array / cf).astype(float)))
        # fcd.output_array = list((np.round(fcd.output_array / cf).astype(float)))

        fcd.state_array = list(fcd.state_array.astype(float) / cf)
        fcd.output_array = list(fcd.output_array.astype(float) / cf)
        return fcd

    return wraped_call


class Controller(object):

    def __init__(self):
        pass

    def call(self, to_controller_data):
        raise NotImplementedError


class DummyController(Controller):

    # def __init__(self, state_array, output_array):

    def __init__(self, num_dims):
        dummy_state_array = list(np.zeros(num_dims.s))
        dummy_output_array = list(np.zeros(num_dims.u))
        self.state_array = dummy_state_array
        self.output_array = dummy_output_array

    def call(self, to_controller_data):
        return cifc.FromController(self.state_array, self.output_array)


# Interface class which provides functions to call the C controller

class ControllerSO(Controller):

    def __init__(self, lib_path, num_dims):
        self.num_states = num_dims.s
        self.num_outputs = num_dims.u
        self.num_x = num_dims.x
        self.num_inputs = num_dims.ci

        # TODO: Can also use os along with platform?

        platform_str = platform.system()
        if platform_str == 'Linux':
            logger.info('Linux detected')
        elif platform_str == 'Windows':
            logger.info('Windows detected')
        else:
            raise err.Fatal('unknown platfor {}'.format(platform_str))
        ct.cdll.LoadLibrary(lib_path)
        self.lib = ct.CDLL(lib_path)

        self.RetValCT = RetValCT_meta(num_dims)#self.num_states, self.num_outputs)
        self.InputValCT = InputValCT_meta(num_dims)#self.num_inputs, self.num_states, self.num_x)

        # Set arguement types

        self.lib.controller.argtypes = [ct.POINTER(self.InputValCT),
                ct.POINTER(self.RetValCT)]

        # Set return type

        self.lib.controller.restype = ct.c_void_p

        # Initialize the library
        # TODO: The controller initialization routine is hard coded but should
        # ideally be supplied as a string

        self.lib.controller_init()


    #TODO: can be called on multiple s0, just like the plant sim
    def call_array(self, controller_args):
        raise NotImplementedError

    # Returns a list!
    # Ideally should be returning a numpy array

    def call(self, to_controller_data):
        input_val = self.InputValCT(to_controller_data)
        ret_val = self.RetValCT()

        # call the controller function

        ignore_void_p = self.lib.controller(ct.byref(input_val), ct.byref(ret_val))
        return ret_val.from_controller

    # UPDATE: no longer used
    # Low level call

    def call_(self, args):
        return self.lib.controller(*args)

def get_double_array_from_double_list(array):
    return (ct.c_double * len(array))(*array)

def get_int_array_from_int_list(array):
    return (ct.c_int * len(array))(*array)


################################
# Test Functions
################################

def test_call(
    c,
    input_array,
    x_array,
    state_array,
    ):

    args = cifc.ToController(np.array(input_array), np.array(state_array),
                             np.array(x_array))

    # ToController -> FromController

    ret_val = c.call(args)

    next_state_array = ret_val.state_array
    output_array = ret_val.output_array
    return (next_state_array, output_array)


def main():
    lib_path = './csim_test_controller.so'
    x_array = [10, 11, 12, 13, 14]
    int_state_array = [1, 2, 3]
    float_state_array = [1, 2, 3, 4]
    state_array = int_state_array + float_state_array
    input_array = [23]
    num_outputs = 2
    num_inputs = len(input_array)
    num_states = len(state_array)
    num_int_states = len(int_state_array)
    num_float_states = len(float_state_array)
    num_x = len(x_array)

    # TODO: export NumDims to some common file?

    NumDims = collections.namedtuple('NumDims', ['s', 'si', 'sf', 'x', 'u', 'ci', 'pi'],
                                     verbose=False)
    num_dims = NumDims(s=num_states,
                       si=num_int_states,
                       sf=num_float_states,
                       x=num_x,
                       u=num_outputs,
                       ci=num_inputs,
                       pi=0)
    c = ControllerSO(lib_path, num_dims)

    # Test call()

    print '=' * 60
    print 'Testing call, the high level call function'
    (next_state_array, output_array) = test_call(c, input_array, x_array,
            state_array)

    print '''{0} || OUTPUTS || {0}'''.format('=' * 15)
    print 'state:',
    for i in next_state_array:
        print '{}'.format(i),
    print
    print 'output:',
    print output_array


if __name__ == '__main__':
    main()

# c_bool  _Bool   bool (1)
# c_char  char    1-character string
# c_wchar wchar_t 1-character unicode string
# c_byte  char    int/long
# c_ubyte unsigned char   int/long
# c_short short   int/long
# c_ushort        unsigned short  int/long
# c_int   int     int/long
# c_uint  unsigned int    int/long
# c_long  long    int/long
# c_ulong unsigned long   int/long
# c_longlong      __int64 or long long    int/long
# c_ulonglong     unsigned __int64 or unsigned long long  int/long
# c_float float   float
# c_double        double  float
# c_longdouble    long double     float
# c_char_p        char * (NUL terminated) string or None
# c_wchar_p       wchar_t * (NUL terminated)      unicode or None
# c_void_p        void *  int/long or None

# Accessing arrays:
    # Using numpy
#        self.lib.controller.restype\
#            = ndpointer(dtype=ct.c_int, shape=(NUM_STATES))
    # using Python
#        self.lib.controller.restype\
#            = ct.POINTER(ct.c_int * NUM_STATES)
