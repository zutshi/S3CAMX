#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
controlifc.py
----------------
Defines the low level interface to the C controller's shared object.
'''

import ctypes as ct
import numpy as np

import err


# Interface definition
class ControllerIfcVarNames(object):
    def __init__(self, num_dims):
        x_name_str_list = ['iv_x{}'.format(i) for i in self.num_dims.x]
        s_name_str_list = ['iv_s{}'.format(i) for i in self.num_dims.s]
        ci_name_str_list = ['iv_ci{}'.format(i) for i in self.num_dims.ci]

        self.args = ControllerArgs(ci_name_str_list, s_name_str_list, x_name_str_list)

        s_name_str_list = ['rv_s{}'.format(i) for i in self.num_dims.s]
        u_name_str_list = ['rv_u{}'.format(i) for i in self.num_dims.u]

        self.ret_val = ControllerRetVals(s_name_str_list, u_name_str_list)

        return



####################################################
# High level INTERFACE for python to controller
####################################################

# TODO: Add sanity checks
class ControllerRetVals(object):

    def __init__(self, state_array, output_array):

        self.state_array = state_array
        self.output_array = output_array


class ControllerArgs(object):

    def __init__(
        self,
        input_array,
        state_array,
        x_array,
        ):

        self.input_array = input_array
        self.state_array = state_array
        self.x_array = x_array

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!! DEPRECATED in favor of !!!!!!
# ControllerArgs and ControllerRetVals !!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
####################################################
# High level INTERFACE for python to controller
####################################################

# Both the interfaces need to be modified if the communication protocol ever
# changes
# Current Protocol:
#
# Output from C controller:
# &struct,
# where struct = {&state_array[num_controller_states],
#                 &output_array[num_controller_outputs]}
#
# Input to C controller:
# &struct,
# where struct = {&state_array[num_controller_states],
#                 &x_array[num_plant_states]}

class FromController(object):

    # TODO: force sending numpy arrays

    def __init__(self, state_array, output_array):

#        self._state_array = self.state_array(state_array)
#        self._output_array = self.output_array(output_array)

        self.state_array = state_array
        self.output_array = output_array

    @property
    def state_array(self):
        return self._state_array

    @state_array.setter
    def state_array(self, val):
        if type(val) != list:
            raise err.Fatal('state_array is not a list: type = {}'.format(type(val)))
        self._state_array = np.array(val)

    @property
    def output_array(self):
        return self._output_array

    @output_array.setter
    def output_array(self, val):
        if type(val) != list:
            raise err.Fatal('output_array is not a list: type = {}'.format(type(val)))
        self._output_array = np.array(val)


class ToController(object):

    # TODO: force sending numpy arrays

    def __init__(
        self,
        input_array,
        state_array,
        x_array,
        ):

#       self._state_array = self.state_array(state_array)
#       self._x_array = self.x_array(x_array)

        self.input_array = input_array
        self.state_array = state_array
        self.x_array = x_array

# TODO: Looks like a better way to deal with the interface. But requirs
# num_dims. There should either be a metaclass or some kind of initialization
# in secam() which supplies it the interface, numdims etc.
#    @property
#    def int_state_array(self):
#        return list(self._state_array[])
#
#    @property
#    def float_state_array(self):
#        return list(self._state_array[])

    @property
    def input_array(self):
        return list(self._input_array)

    @input_array.setter
    def input_array(self, val):
        if type(val) != np.ndarray:
            raise err.Fatal('input_array is not a numpy array: type = {}'.format(type(val)))
        if val.ndim != 1:
            raise err.Fatal('input_array: more than one state vector provided?: ci = {}, ndim = {}'.format(val, val.ndim))
        self._input_array = val

    @property
    def state_array(self):
        return list(self._state_array)

    @state_array.setter
    def state_array(self, val):
        if type(val) != np.ndarray:
            raise err.Fatal('state_array is not a numpy array: type = {}'.format(type(val)))
        if val.ndim != 1:
            raise err.Fatal('state_array: more than one state vector provided?: s = {}, ndim = {}'.format(val, val.ndim))
        self._state_array = val

    @property
    def x_array(self):
        return list(self._x_array)

    @x_array.setter
    def x_array(self, val):
        if type(val) != np.ndarray:
            raise err.Fatal('x_array is not a numpy array: type = {}'.format(type(val)))
        if val.ndim != 1:
            raise err.Fatal('x_array: more than one x vector provided?: x = {}, ndim = {}'.format(val, val.ndim))
        self._x_array = val
