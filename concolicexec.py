#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
concolicexec.py [DEFUNCT]
--------------------------
Concolic engine to interface to process KLEE's outputs.
'''

import numpy as np
import kleewrap as k

import logging

import err

logger = logging.getLogger(__name__)


# Return the chosen concolic engine
# FOr now its only Klee

def concolic_engine_factory(*args, **kwargs):
    return Klee(*args, **kwargs)


class ConcolicEngine(object):

    pass


#    def __init__(self, dir_path, num_states, num_outputs, num_x, Type):
#        self.dir_path = dir_path
#        self.num_states = num_states
#        self.num_outputs = num_outputs
#        self.num_x = num_x
#        if Type == 'klee':
#            self.analyzer = k.Klee(var_type)
#            if dir_path != './':
#                raise err.Fatal('dir_path is not ./')
#        elif Type == 'z3':
#            pass
#        else:
#            raise NotImplementedError

# TODO: Platform dependant!!
# Expects PATH variable to be set for
#   llvm-gcc
#   klee

class Klee(ConcolicEngine):

    def __init__(
        self,
        var_type,
        num_dims,
        controller_str,
        ):

        # num_states, num_outputs, num_x is found from the generated test case!

        # The below part has been moved to the secam instead
#         var_type = {}
#         var_type['state_arr'] = 'int_arr'
#         var_type['x_arr'] = 'int_arr'
#         var_type['input_arr'] = 'int_arr'

        self.analyzer = k.KleeWrap(var_type, controller_str)
        self.num_dims = num_dims

    # Fire up Klee on a test case
    # read test case results
    # Return test cases in the format

    def get_test_cases(
        self,
        plant_state_ival_cons,
        controller_state_ival_cons,
        ci_ival_cons,
        ):

        # ##!!##logger.debug(plant_state_ival_cons)

        d = [plant_state_ival_cons.to_c_str_list('x_arr'),
             controller_state_ival_cons.to_c_str_list('state_arr'),
             ci_ival_cons.to_c_str_list('input_arr')]

        test_cases = self.analyzer.analyze(d)

        n = len(test_cases)
        s_array = np.empty((n, self.num_dims.s), dtype=float)
        x_array = np.empty((n, self.num_dims.x), dtype=float)
        ci_array = np.empty((n, self.num_dims.ci), dtype=float)

        idx = 0
        for test_case in test_cases:
            s = np.array(test_case['state_arr'])
            x = np.array(test_case['x_arr'])

            # print 'x:',x

            ci = np.array(test_case['input_arr'])

            # print 'lala:',type(s_array), s

            s_array[idx, :] = s.astype(float) 
            x_array[idx, :] = x.astype(float) 

            # print 'x_array:',x_array

            ci_array[idx, :] = ci.astype(float)
            idx += 1

        # finally tile c_state_array to the same size as number of test cases

        ret_test_cases = TestCases(s_array=s_array, x_array=x_array,
                                   ci_array=ci_array)

        # ##!!##logger.debug(ret_test_cases)

        return ret_test_cases

def call_z3(self, args):
    raise NotImplementedError


# Leave s' and u empty

class TestCases(object):

    def __init__(
        self,
        s_array=None,
        x_array=None,
        ci_array=None,
        ):
        self.n = len(x_array)

        # s: controller states

        self.s_array = s_array

        # x: plant states

        self.x_array = x_array

        # ci: controller disturbances/extraneous inputs

        self.ci_array = ci_array
        self.sanity_check()

    def sanity_check(self):
        if self.n != len(self.x_array) or self.n != len(self.s_array):
            raise err.Fatal('sanity check fails')
        return

    def __repr__(self):
        return '''test_case
s_array={}
x_array={}
ci_array={}'''.format(self.s_array,
                self.x_array, self.ci_array)


