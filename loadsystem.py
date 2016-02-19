###############################################################################
# File name: loadsystem.py
# Author: Aditya
# Python Version: 2.7
#
#                       #### Description ####
# Provides a parse function and structures to load a parsed system.
# Reads the system description from the provided .tst file,
# and populates respective structures and returns them.
###############################################################################

from __future__ import print_function

import numpy as np
import sys as SYS
import imp

from numdims import NumDims
import constraints as cns
import utils as U
from utils import print
import fileOps as fp
import system as S
import prop as P
import err


class MissingSystemDefError(Exception):
    def __init__(self, args):
        missing_attr = args[0].replace(''''module' object has no attribute ''', '')
        error_msg = 'Missing definition in the .tst file: {}'.format(missing_attr)
        self.args = (error_msg,)
        return


# No longer being used
# Instead, all options are now passed using the commandline
class Options(object):
    def __init__(self, plot, MODE, num_sim_samples, METHOD, symbolic_analyzer):
        self.plot = plot
        self.MODE = MODE
        self.num_sim_samples = num_sim_samples
        self.METHOD = METHOD
        self.symbolic_analyzer = symbolic_analyzer

        self.sanity_check = U.assert_no_Nones

        return


def parse(file_path):
    test_des_file = file_path
    path = fp.get_abs_base_path(file_path)

    test_dir = fp.get_abs_base_path(test_des_file)
    SYS.path.append(test_dir)

    sut = imp.load_source('test_des', test_des_file)

    try:
        assert(len(sut.initial_set) == 2)
        assert(len(sut.error_set) == 2)
        assert(len(sut.ci) == 2)
        assert(len(sut.pi) == 2)

        assert(len(sut.ci[0]) == len(sut.ci[1]))
        assert(len(sut.pi[0]) == len(sut.pi[1]))

        assert(len(sut.initial_set[0]) == len(sut.initial_set[1]))
        assert(len(sut.error_set[0]) == len(sut.error_set[1]))

        assert(len(sut.initial_set[0]) == len(sut.error_set[0]))

        assert(len(sut.initial_set[0]) == len(sut.grid_eps))

        #if sut.initial_pvt_states:
        #    err.error('pvt states not implementd!')

        num_dims = NumDims(
            si=len(sut.initial_controller_integer_state),
            sf=len(sut.initial_controller_float_state),
            s=len(sut.initial_controller_integer_state)+len(sut.initial_controller_float_state),
            x=len(sut.initial_set[0]),
            u=sut.num_control_inputs,
            ci=len(sut.ci[0]),
            pi=len(sut.pi[0]),
            d=len(sut.initial_discrete_state),
            pvt=0,
            )

        # check for optional attributes
        if not hasattr(sut, 'ci_grid_eps') or len(sut.ci_grid_eps) == 0:
            sut.ci_grid_eps = []

        if not hasattr(sut, 'pi_grid_eps') or len(sut.pi_grid_eps) == 0:
            sut.pi_grid_eps = []

        if hasattr(sut, 'plant_composition'):
            # composition analyses
            comp_scheme = sut.plant_composition
        else:
            comp_scheme = None

        if num_dims.ci == 0:
            ci = None
        else:
            ci = cns.IntervalCons(np.array(sut.ci[0]), np.array(sut.ci[1]))

        if num_dims.pi == 0:
            pi = None
        else:
            pi = cns.IntervalCons(np.array(sut.pi[0]), np.array(sut.pi[1]))

        assert((pi is None and sut.pi_grid_eps == []) or
               (pi is not None and sut.pi_grid_eps != []))
        assert((ci is None and sut.ci_grid_eps == []) or
               (ci is not None and sut.ci_grid_eps != []))

        if pi is not None:
            assert(len(sut.pi[0]) == len(sut.pi_grid_eps))

        if ci is not None:
            assert(len(sut.ci[0]) == len(sut.ci_grid_eps))

        ci_grid_eps = np.array(sut.ci_grid_eps, dtype=float)
        pi_grid_eps = np.array(sut.pi_grid_eps, dtype=float)

        plant_config_dict = {'plant_description': sut.plant_description,
                             'plant_path': sut.plant_path,
                             'eps': np.array(sut.grid_eps, dtype=float),
                             'num_samples': int(sut.num_samples),
                             'delta_t': float(sut.delta_t),
                             'type': 'value',
                             }

        # TODO: fix the list hack, once the controller ifc matures

        init_cons = cns.IntervalCons(np.array(sut.initial_set[0]),
                                     np.array(sut.initial_set[1]))

        init_cons_list = [init_cons]

        final_cons = cns.IntervalCons(np.array(sut.error_set[0]),
                                      np.array(sut.error_set[1]))
        T = sut.T
        delta_t = sut.delta_t

        if sut.controller_path is not None:
            controller_object_str = fp.split_filename_ext(sut.controller_path)[0]
            controller_path_dir_path = fp.construct_path(sut.controller_path_dir_path, path)
        else:
            controller_object_str = None
            controller_path_dir_path = None

        initial_discrete_state = sut.initial_discrete_state
        initial_controller_state = (sut.initial_controller_integer_state +
                                    sut.initial_controller_float_state)
        MAX_ITER = sut.MAX_ITER

        num_segments = int(np.ceil(T / delta_t))

        controller_path = sut.controller_path
        plant_pvt_init_data = sut.plant_pvt_init_data

        sys = S.System(controller_path, num_dims, plant_config_dict,
                       delta_t, controller_path_dir_path,
                       controller_object_str, path, plant_pvt_init_data,
                       sut.min_smt_sample_dist, ci_grid_eps,
                       pi_grid_eps, comp_scheme)
        prop = P.Property(T, init_cons_list, init_cons, final_cons, ci,
                          pi, initial_discrete_state, initial_controller_state,
                          MAX_ITER, num_segments)

        #num_sim_samples = sut.num_sim_samples
        #METHOD = sut.METHOD
        #symbolic_analyzer = sut.symbolic_analyzer
        #plot = sut.plot
        #MODE = sut.MODE
        #opts = Options(plot, MODE, num_sim_samples, METHOD, symbolic_analyzer)
    except AttributeError as e:
        raise MissingSystemDefError(e)
    print('system loaded...')
    return sys, prop
