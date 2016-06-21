#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import err

logger = logging.getLogger(__name__)


class Constraints(object):

    def __init__(self):
        pass


class IntervalCons(Constraints):

    def __init__(self, l, h):
        if type(h) != np.ndarray or type(l) != np.ndarray:
            raise err.Fatal('interval constraints should be expressed as np.ndarray expected'
                            )
        self.h = h
        self.l = l
        self.dim = len(self.l)
        self.sanity_check()

    # sanity check

    def sanity_check(self):
        for (i, j) in zip(self.l, self.h):
            if i > j:

                # # ##!!##logger.debug('IntervalCons sanity check failure!: l > h')
                # # ##!!##logger.debug('l = {}, h = {}'.format(self.l, self.h))

                raise err.Fatal('malformed interval!')
        if len(self.l) != len(self.h):
            raise err.Fatal('dimension mismatch between bounds!')

    def dim(self):
        return len(self.h)

    def scaleNround(self, CONVERSION_FACTOR):
        raise err.Fatal('#$%^$&#%#&%$^$%^$^#!@$')

        # do not do inplace conversion, instead return a copy!
        # self.h = (self.h * CONVERSION_FACTOR).astype(int)
        # self.l = (self.l * CONVERSION_FACTOR).astype(int)

        h = np.round(self.h * CONVERSION_FACTOR).astype(int)
        l = np.round(self.l * CONVERSION_FACTOR).astype(int)
        return IntervalCons(l, h)

    # Returns the more traditional format for expressing constraints
    # [[x1_l, x1_h],
    #  [x2_l, x2_h],
    #  [x3_l, x3_h]]
    def to_numpy_array(self):
        return np.concatenate(([self.l], [self.h]), axis=0).T

    # Get the constraints as C program statements!
    # [(1,10), (2,12)]
    # will become
    # [
    #   'x[0] >= 1',
    #   'x[0] <= 2'.
    #   'x[1] >= 10'
    #   'x[1] <= 12
    # ]

    def to_c_str_list(self, var_name):

        # template string

        ts_ge = '{0}[{1}] >= {2}'
        ts_le = '{0}[{1}] <= {2}'
        s = []
        for (idx, l, h) in zip(range(len(self.l)), self.l, self.h):
            s.append(ts_ge.format(var_name, idx, l))
            s.append(ts_le.format(var_name, idx, h))
        return s

    def __str__(self):
        s = self.to_c_str_list('x')
        return ' and '.join(s)

    def any_sat(self, x_array):
        return np.logical_and.reduce(self.sat(x_array), 0)

    def sat(self, x_array):
        res_l = x_array >= self.l
        res_h = x_array <= self.h

        # Columnwise reduction

        return np.logical_and.reduce(np.logical_and(res_l, res_h), 1)

    def __and__(self, ic):

        # check dimensions

        if self.dim != ic.dim:
            raise err.Fatal('intersection of interval constraints: must be of same dimensions!'
                            )

#       use max/min instead of case check!

        l = np.maximum(self.l, ic.l)
        h = np.minimum(self.h, ic.h)
        try:
            return IntervalCons(l, h)
        except err.Fatal:
            return None

    # must return True or False
    # Use contains() for vectorized function

    def __contains__(self, x):

        if x.ndim != 1:
            raise err.Fatal('dim(x) must be 1, instead dim(x) = {}'.format(x.ndim))

        # print x.shape, x

        res_l = x >= self.l
        res_h = x <= self.h

        # print np.logical_and.reduce(np.logical_and(res_l, res_h), 0)

        ret_val = np.logical_and.reduce(np.logical_and(res_l, res_h), 0)
        return ret_val

    # vecotirzed version of __contains__()

    def contains(self, x_array):

        # print x.shape, x

        res_l = x_array >= self.l
        res_h = x_array <= self.h

        # The axis used is different from __contains__()

        return np.logical_and.reduce(np.logical_and(res_l, res_h), 1)

    def __repr__(self):
        return '{},{}'.format(str(self.l), str(self.h))


#        s = '[' + str(self.l) + ',' + str(self.h) + ']'
#        return s

class Z3Constraints(Constraints):

    def __init__(self, C):
        self.C = C

    def substitute(
        self,
        C,
        v,
        v_,
        ):
        self.z3.substitute(self.C, [(v, v_)])


# returns a function which needs to be instantiated by passing in the z3.array
# befor using as a constraint

#def ic2smt(z3, ic):
#
#    def get_cons(x):
#        cons_list = []
#        int_size = 4  # bytes
#        for i in range(ic.dim):
#            c_upper_bound = z3.Concat(x[int_size * i + 3], x[int_size * i
#                                      + 2], x[int_size * i + 1], x[int_size
#                                      * i + 0]) <= ic.h[i]
#            c_lower_bound = z3.Concat(x[int_size * i + 3], x[int_size * i
#                                      + 2], x[int_size * i + 1], x[int_size
#                                      * i + 0]) >= ic.l[i]
#            cons_list.append(c_upper_bound)
#            cons_list.append(c_lower_bound)
#        return z3.And(cons_list)
#
#    return get_cons


