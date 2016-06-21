# -*- coding: utf-8 -*-
###############################################################################
# File name: matpy.py
# Author: Aditya
# Python Version: 2.7
#
#                       #### Description ####
# Provides an interface between Python and their counterpart Matlab functions.
# The primary reason for such a layer is the lack of Matlab R2015a support for
# passing double array of more than 1 dim. This layer takes care of
# serialization and de-serialization. This is done with its matlab counterpart
# simulate_system_external.m
###############################################################################

import array
import numpy as np

import err
import external_interface as exifc


# Reachabillity Property structure translated to matlab
class MatProp(object):
    def __init__(self, T, init_cons, final_cons, ci, num_segments, delta_t):
        self.T = T
        self.init_cons = init_cons
        self.final_cons = final_cons
        self.w = ci
        # self.pi = pi
        self.num_segments = num_segments
        self.delta_t = delta_t


# TODO: init_cons_list is not handled!
def load_system(file_path):
    one_shot_sim, prop = exifc.load_system(file_path)
    #T = prop.T
    init_cons = serialize_array(prop.init_cons.to_numpy_array())
    final_cons = serialize_array(prop.final_cons.to_numpy_array())
    ci = serialize_array(prop.ci.to_numpy_array())
    print init_cons, final_cons, ci
    #num_segments = prop.num_segments
    mat_prop = MatProp(prop.T,
                       init_cons,
                       final_cons,
                       ci,
                       prop.num_segments,
                       prop.delta_t)

    def mat_one_shot_sim(x, t0, tf, w):
        x = deserialize_array(x)
        w = deserialize_array(w)
        #print '#'*20
        #print x
        #print w
        trace = one_shot_sim(x, t0, tf, w)
        #print trace

        T_ser = serialize_array(trace.t_array)
        X_ser = serialize_array(trace.x_array)
        #print trace.x_array

        return (T_ser, X_ser)

    return mat_one_shot_sim, mat_prop


# S should be a tuple representing matrix size
# This is not trivially generizable to N-dim arrays.More work needs to be dont
# to serialize/un-serialize matlab N-dim arrays
# At present, use it for matrices only!

# [shape data]
def serialize_array(x):
    if x.ndim > 2:
        raise err.Fatal('Interface can only be used for matrices, dim <= 2')
    flat_x = x.flatten()
    if x.ndim == 1:
        s = (1, x.shape[0])
    else:
        s = x.shape
    tmp_x = np.append(s, flat_x)
    x_ser = array.array(tmp_x.dtype.char, tmp_x)
    return x_ser


def deserialize_array(x_ser):
    s = x_ser[0:2]
    flat_x = x_ser[2:]
    # if num rows is 1, interpret it as 1-dim array
    if s[0] == 1:
        x = np.array(flat_x)
    else:
        #s.reverse()
        s = map(int, s)
        #x = np.reshape(flat_x, s).T
        x = np.reshape(flat_x, s)
    #print x
    return x

## [ndim shape data]
#def serialize_array(x):
#    if x.ndim > 2:
#        raise err.Fatal('Interface can only be used for matrices, dim <= 2')
#    flat_x = x.flatten()
#    tmp_x = np.append(x.shape, flat_x)
#    tmp_x = np.append(x.ndim, tmp_x)
#    x_ser = array.array(tmp_x.dtype.char, tmp_x)
#    return x_ser

#def deserialize_array(x_ser):
#    dim = int(x_ser[0])
#    s = x_ser[1:1+dim]
#    flat_x = x_ser[1+dim:]
#    s.reverse()
#    s = map(int, s)
#    x = np.reshape(flat_x, s).T
#    print x
#    return x
