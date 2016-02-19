###############################################################################
# File name: loadsystem.py
# Author: Aditya
# Python Version: 2.7
#
#                       #### Description ####
# decomposes a provided system into its constituents according to the
# supplied composition_ scheme
###############################################################################

from __future__ import print_function

import constraints as cns
import system as S
import prop as P
from numdims import NumDims
import err


class Offset(object):
    def __init__(self):
        self.x = 0
        self.ci = 0
        self.pi = 0
        self.d = 0
        self.pvt = 0

    def incr(self, nx, nci, npi, nd, npvt):
        self.x += nx
        self.ci += nci
        self.pi += npi
        self.d += nd
        self.pvt += npvt


def decompose(sys, prop):
    sys_list = []
    prop_list = []
    # pre-fixed indices
    xk = 0
    dk = 1
    pvtk = 2
    cik = 3
    pik = 4

    offset = Offset()

    for sys_part in sys.comp_scheme:

        num_dims = NumDims(
            si=0,
            sf=0,
            s=0,
            x=sys_part[xk],
            u=0,
            ci=sys_part[cik],
            pi=sys_part[pik],
            d=sys_part[dk],
            pvt=sys_part[pvtk],
            )

        plant_config_dict = {k: d for k, d in sys.plant_config_dict.iteritems()}
        plant_config_dict['eps'] = plant_config_dict['eps'][offset.x:offset.x + sys_part[xk]]

        ci_grid_eps = sys.ci_grid_eps[offset.ci:offset.ci + sys_part[cik]]
        pi_grid_eps = sys.pi_grid_eps[offset.pi:offset.pi + sys_part[pik]]

        system_i = S.System(sys.controller_path, num_dims,
                            plant_config_dict, sys.delta_t,
                            sys.controller_path_dir_path,
                            sys.controller_object_str, sys.path,
                            sys.plant_pvt_init_data, sys.min_smt_sample_dist,
                            ci_grid_eps, pi_grid_eps, sys.comp_scheme)

        init_cons = cns.IntervalCons(prop.init_cons.l[offset.x:offset.x + sys_part[xk]],
                                     prop.init_cons.h[offset.x:offset.x + sys_part[xk]])
        init_cons_list = [init_cons]
        final_cons = cns.IntervalCons(prop.final_cons.l[offset.x:offset.x + sys_part[xk]],
                                      prop.final_cons.h[offset.x:offset.x + sys_part[xk]])

        ci = None if prop.ci is None else (
                cns.IntervalCons(
                    prop.ci.l[offset.ci:offset.ci + sys_part[cik]],
                    prop.ci.h[offset.ci:offset.ci + sys_part[cik]]))

        pi = None if prop.pi is None else (
                cns.IntervalCons(
                    prop.pi.l[offset.pi:offset.pi + sys_part[pik]],
                    prop.pi.h[offset.pi:offset.pi + sys_part[pik]]))

        initial_discrete_state = prop.initial_discrete_state[offset.d:offset.d + sys_part[dk]]

        prop_i = P.Property(prop.T, init_cons_list, init_cons,
                            final_cons, ci, pi, initial_discrete_state,
                            prop.initial_controller_state, prop.MAX_ITER,
                            prop.num_segments)

        offset.incr(sys_part[xk], sys_part[cik], sys_part[pik], sys_part[dk], sys_part[pvtk])
        prop_list.append(prop_i)
        sys_list.append(system_i)

    # The grid_eps accross systems must be equal
    # This means, the systems are copies of each other
    # Required to keep the porperty check simple.
    # TODO: Can this be removed? and the property check generelized?
    assert(len(set(tuple(sys.plant_config_dict['eps']) for sys in sys_list)) == 1)
    return sys_list, prop_list
