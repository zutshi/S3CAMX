#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
#import matplotlib
# Force GTK3 backend. By default GTK2 gets loaded and conflicts with
# graph-tool
#matplotlib.use('GTK3Agg')
#global plt
import matplotlib.pyplot as plt

import logging
import numpy as np
#from optparse import OptionParser
import argparse
#import argcomplete
import time
import sys as SYS
import tqdm

import abstractioncomposable as AA
#import abstraction as AA
import sample
import fileOps as fp
import concolicexec as CE
import simulatesystem as simsys
import scattersimcomposable as SS
import err
import loadsystem
import loaddecomposedsystem
import traces
import list_examples as eg
import plothelper as ph
import plot_hack
import wmanager
import checkprop as chkp
import closestpair as CP
import utils as U
from utils import print

#matplotlib.use('GTK3Agg')

#precision=None, threshold=None, edgeitems=None, linewidth=None, suppress=True, nanstr=None, infstr=None, formatter=Nonu)
np.set_printoptions(suppress=True)

###############################
# terminal color printing compatibility for windows
# https://pypi.python.org/pypi/colorama/0.2.4

# from colorama import init
# init()

# use this when we add windows portability
###############################

# start logger

FORMAT = '[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
FORMAT2 = '%(levelname) -10s %(asctime)s %(module)s:\
           %(lineno)s %(funcName)s() %(message)s'

logging.basicConfig(filename='log.secam', filemode='w', format=FORMAT2,
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Remove this re-structuring!! Use existing structures instead.
class SystemParams:

    def __init__(
            self,
            initial_state_set,
            final_state_set,
            is_final,
            plant_sim,
            controller_sim,
            ci,
            pi,
            sampler,
            final_cons,
            pi_ref,
            ci_ref
            ):

        self.initial_state_set = initial_state_set
        self.final_state_set = final_state_set
        self.is_final = is_final
        self.plant_sim = plant_sim
        self.controller_sim = controller_sim
        self.ci = ci
        self.pi = pi
        self.sampler = sampler
        self.final_cons = final_cons
        self.pi_ref = pi_ref
        self.ci_ref = ci_ref
        return


# TODO: make a module of its own once we add more general property using
# monitors...
def check_prop_violation(trace, prop):
    idx = prop.final_cons.contains(trace.x_array)
    return trace.x_array[idx], trace.t_array[idx]


def simulate(sys_list, prop_list, opts):
    num_samples = opts.num_sim_samples
    num_violations = 0

    if opts.decompose:
        err.warn_severe('ignoring decomposition rules!')
    sys = sys_list[0]
    prop = prop_list[0]

    concrete_states = sample.sample_init_UR(sys, prop, num_samples)
    trace_list = []

    sys_sim = simsys.get_system_simulator(sys)
    for i in tqdm.trange(num_samples):
        trace = simsys.simulate(sys_sim, concrete_states[i], prop.T)
        trace_list.append(trace)
        sat_x, sat_t = check_prop_violation(trace, prop)
        if sat_x.size != 0:
            num_violations += 1
            print('x0={} -> x={}, t={}...num_vio_counter={}'.format(
                trace.x_array[0, :],
                sat_x[0, :],    # the first violating state
                sat_t[0],       # corresponding time instant
                num_violations), file=SYS.stderr)

    print('number of violations: {}'.format(num_violations))
    return trace_list


def create_abstraction(sys, prop, opts):
    num_dims = sys.num_dims
    plant_config_dict = sys.plant_config_dict
    controller_path_dir_path = sys.controller_path_dir_path
    controller_object_str = sys.controller_object_str

    T = prop.T

    METHOD = opts.METHOD

    plant_abstraction_type = 'cell'
    if METHOD == 'concolic':
        controller_abstraction_type = 'concolic'

        # Initialize concolic engine

        var_type = {}

        # state_arr is not symbolic in concolic exec,
        # with concrete controller states

        var_type['state_arr'] = 'int_arr'
        var_type['x_arr'] = 'int_arr'
        var_type['input_arr'] = 'int_arr'
        concolic_engine = CE.concolic_engine_factory(
            var_type,
            num_dims,
            controller_object_str)

        # sampler = sample.Concolic(concolic_engine)

        sampler = sample.IntervalConcolic(concolic_engine)
    elif METHOD == 'concrete':
        sampler = sample.IntervalSampler()
        controller_abstraction_type = 'concrete'
        controller_sym_path_obj = None

        # TODO: manual contruction of paths!!!!
        # use OS independant APIs from fileOps
    elif METHOD == 'symbolic':
        sampler = None
        if opts.symbolic_analyzer == 'klee':
            controller_abstraction_type = 'symbolic_klee'
            if opts.cntrl_rep == 'smt2':
                controller_path_dir_path += '/klee/'
            else:
                raise err.Fatal('KLEE supports only smt2 files!')
        elif opts.symbolic_analyzer == 'pathcrawler':
            controller_abstraction_type = 'symbolic_pathcrawler'
            if opts.cntrl_rep == 'smt2':
                controller_path_dir_path += '/pathcrawler/'
            elif opts.cntrl_rep == 'trace':
                controller_path_dir_path += '/controller'
            else:
                raise err.Fatal('argparse should have caught this!')

            # TAG:PCH_IND
            # Parse PC Trace
            import CSymLoader as CSL
            controller_sym_path_obj = CSL.load_sym_obj((opts.cntrl_rep, opts.trace_struct), controller_path_dir_path)
        else:
            raise err.Fatal('unknown symbolic analyzer requested:{}'.format(opts.symbolic_analyzer))

    else:
        raise NotImplementedError

    # TODO: parameters like controller_sym_path_obj are absraction dependant
    # and should not be passed directly to abstraction_factory. Instead a
    # flexible structure should be created which can be filled by the
    # CAsymbolic abstraction module and supplied as a substructure. I guess the
    # idea is that an abstraction module should be 'pluggable'.
    current_abs = AA.abstraction_factory(
        plant_config_dict,
        T,
        num_dims,
        controller_sym_path_obj,
        sys.min_smt_sample_dist,
        plant_abstraction_type,
        controller_abstraction_type,
        )
    return current_abs, sampler


def falsify(sys_list, prop_list, opts):

    current_abs_sampler = [create_abstraction(sys, prop, opts)
                            for sys, prop in zip(sys_list, prop_list)]

    current_abs = [i[0] for i in current_abs_sampler]
    sampler = [i[1] for i in current_abs_sampler]

    # sys
    controller_sim = [sys.controller_sim for sys in sys_list]
    plant_sim = [sys.plant_sim for sys in sys_list]

    # prop
    init_cons_list = [prop.init_cons_list for prop in prop_list]
    init_cons = [prop.init_cons for prop in prop_list]
    final_cons = [prop.final_cons for prop in prop_list]
    ci = [prop.ci for prop in prop_list]
    pi = [prop.pi for prop in prop_list]
    initial_discrete_state = [tuple(prop.initial_discrete_state) for prop in prop_list]
    initial_controller_state = [np.array(prop.initial_controller_state)
                                for prop in prop_list]
    MAX_ITER = [prop.MAX_ITER for prop in prop_list]

    #TODO: hack to make random_test sample ci_cells when doing
    # ss-concrete. It is false if ss-symex (and anything else) is
    # asked for, because then ci_seq consists if concrete values. Can
    # also be activated for symex as an option, but to be done later.
    sample_ci = opts.METHOD == 'concrete'

    # options
    plot = opts.plot

    # make a copy of the original initial plant constraints

    original_plant_cons_list = init_cons_list

    pi_ref = [wmanager.WMap(pii, sys.pi_grid_eps) for sys, pii in zip(sys_list, pi)]
    ci_ref = [wmanager.WMap(cii, sys.ci_grid_eps)
              if sample_ci else None for sys, cii in zip(sys_list, ci)]

#            f1 = plt.figure()
##
##            plt.grid(True)
##
##            ax = f1.gca()
##           eps = current_abs.plant_abs.eps
##            #ax.set_xticks(np.arange(0, 2, eps[0]))
##            #ax.set_yticks(np.arange(0, 20, eps[1]))
##
##            f1.suptitle('abstraction')

    if opts.refine == 'init':
        if opts.decompose:
            print('Attempting compositional analyses...')
            refine_init_composable(
                current_abs,
                init_cons_list,
                final_cons,
                initial_discrete_state,
                initial_controller_state,
                plant_sim,
                controller_sim,
                ci,
                pi,
                sampler,
                plot,
                init_cons,
                original_plant_cons_list,
                MAX_ITER,
                sample_ci,
                pi_ref,
                ci_ref)
        else:
#             print(current_abs[0])
#             print(init_cons_list[0])
#             print(final_cons[0])
#             print(initial_discrete_state[0])
#             print(initial_controller_state[0])
#             print(plant_sim[0])
#             print(controller_sim[0])
#             print(ci[0])
#             print(pi[0])
#             print(sampler[0])
#             print(plot)
#             print(init_cons[0])
#             print(original_plant_cons_list[0])
#             print(MAX_ITER[0])
#             print(sample_ci)
#             print(pi_ref[0])
#             print(ci_ref[0])

            refine_init(
                current_abs[0],
                init_cons_list[0],
                final_cons[0],
                initial_discrete_state[0],
                initial_controller_state[0],
                plant_sim[0],
                controller_sim[0],
                ci[0],
                pi[0],
                sampler[0],
                plot,
                init_cons[0],
                original_plant_cons_list[0],
                MAX_ITER[0],
                sample_ci,
                pi_ref[0],
                ci_ref[0])
    # seed 4567432
    elif opts.refine == 'trace':
        refine_trace(
            current_abs,
            init_cons_list,
            final_cons,
            initial_discrete_state,
            initial_controller_state,
            plant_sim,
            controller_sim,
            ci,
            pi,
            sampler,
            plot,
            init_cons,
            original_plant_cons_list)
    else:
        raise err.Fatal('internal')

# def falsify(sys, prop, opts):

#     current_abs, sampler = create_abstraction(sys, prop, opts)

#     # sys
#     controller_sim = sys.controller_sim
#     plant_sim = sys.plant_sim

#     # prop
#     init_cons_list = prop.init_cons_list
#     init_cons = prop.init_cons
#     final_cons = prop.final_cons
#     ci = prop.ci
#     pi = prop.pi
#     initial_discrete_state = prop.initial_discrete_state
#     initial_controller_state = prop.initial_controller_state
#     MAX_ITER = prop.MAX_ITER

#     #TODO: hack to make random_test sample ci_cells when doing
#     # ss-concrete. It is false if ss-symex (and anything else) is
#     # asked for, because then ci_seq consists if concrete values. Can
#     # also be activated for symex as an option, but to be done later.
#     sample_ci = opts.METHOD == 'concrete'

#     # options
#     plot = opts.plot

#     initial_discrete_state = tuple(initial_discrete_state)
#     initial_controller_state = np.array(initial_controller_state)

#     # make a copy of the original initial plant constraints

#     original_plant_cons_list = init_cons_list

#     pi_ref = wmanager.WMap(pi, sys.pi_grid_eps)
#     ci_ref = wmanager.WMap(ci, sys.ci_grid_eps) if sample_ci else None

# #            f1 = plt.figure()
# ##
# ##            plt.grid(True)
# ##
# ##            ax = f1.gca()
# ##           eps = current_abs.plant_abs.eps
# ##            #ax.set_xticks(np.arange(0, 2, eps[0]))
# ##            #ax.set_yticks(np.arange(0, 20, eps[1]))
# ##
# ##            f1.suptitle('abstraction')

#     if opts.refine == 'init':
#         if opts.decompose:
#             print('Attempting compositional analyses...')
#             refine_init_composable(
#                 current_abs,
#                 init_cons_list,
#                 final_cons,
#                 initial_discrete_state,
#                 initial_controller_state,
#                 plant_sim,
#                 controller_sim,
#                 ci,
#                 pi,
#                 sampler,
#                 plot,
#                 init_cons,
#                 original_plant_cons_list,
#                 MAX_ITER,
#                 sample_ci,
#                 pi_ref,
#                 ci_ref)
#         else:
#             refine_init(
#                 current_abs,
#                 init_cons_list,
#                 final_cons,
#                 initial_discrete_state,
#                 initial_controller_state,
#                 plant_sim,
#                 controller_sim,
#                 ci,
#                 pi,
#                 sampler,
#                 plot,
#                 init_cons,
#                 original_plant_cons_list,
#                 MAX_ITER,
#                 sample_ci,
#                 pi_ref,
#                 ci_ref)
#     # seed 4567432
#     elif opts.refine == 'trace':
#         refine_trace(
#             current_abs,
#             init_cons_list,
#             final_cons,
#             initial_discrete_state,
#             initial_controller_state,
#             plant_sim,
#             controller_sim,
#             ci,
#             pi,
#             sampler,
#             plot,
#             init_cons,
#             original_plant_cons_list)
#     else:
#         raise err.Fatal('internal')


def refine_trace(
        current_abs,
        init_cons_list,
        final_cons,
        initial_discrete_state,
        initial_controller_state,
        plant_sim,
        controller_sim,
        ci,
        pi,
        sampler,
        plot,
        init_cons,
        original_plant_cons_list):

    (initial_state_set, final_state_set, is_final) = \
        SS.init(current_abs, init_cons_list, final_cons,
                initial_discrete_state, initial_controller_state)

    system_params = SystemParams(
        initial_state_set,
        final_state_set,
        is_final,
        plant_sim,
        controller_sim,
        ci,
        pi,
        sampler,
        final_cons,
        )

    SS.discover(current_abs, system_params)

    if plot:
        plt.autoscale()
        plt.show()

    while True:

        if not system_params.final_state_set:
            print('did not find any abstract counter example!', file=SYS.stderr)
            return True
        else:
            print('analyzing graph...')
        (promising_initial_states, ci_seq_list) = \
            current_abs.get_initial_states_from_error_paths(initial_state_set, final_state_set)

        # ##!!##logger.debug('promising initial states: {}'.format(promising_initial_states))

        print('begin random testing!')
        if plot:
            f2 = plt.figure()
            f2.suptitle('random testing')


        # TODO: ugly...should it be another function?
        # Read the TODO above the function definition for more details
        valid_promising_initial_state_list = SS.filter_invalid_abs_states(
                promising_initial_states,
                current_abs,
                init_cons)
        if valid_promising_initial_state_list == []:
            print('no valid sample found during random testing. STOP', file=SYS.stderr)
            return True

        done = SS.random_test(
            current_abs,
            system_params,
            valid_promising_initial_state_list,
            ci_seq_list,
            init_cons,
            initial_discrete_state,
            initial_controller_state,
            )
        if plot:
            plt.show()
        if done:
            print('Concretized', file=SYS.stderr)
            return True
        current_abs = SS.refine_trace_based(
                current_abs,
                current_abs.compute_error_paths(initial_state_set, final_state_set),
                system_params)
        #init_cons_list = [current_abs.plant_abs.get_ival_constraints(i) for i in valid_promising_initial_state_list]


# # returns a True when its done
# def refine_init_composable(
#         current_abs,
#         init_cons_list,
#         final_cons,
#         initial_discrete_state,
#         initial_controller_state,
#         plant_sim,
#         controller_sim,
#         ci,
#         pi,
#         sampler,
#         plot,
#         init_cons,
#         original_plant_cons_list,
#         MAX_ITER,
#         sample_ci,
#         pi_ref,
#         ci_ref,
#         num_systems):

#     i = 1
#     while i <= MAX_ITER:
#         print('iteration:', i)
#         # TODO: temp function ss.init()

#         sys_init = [SS.init(current_abs[k],
#                             init_cons_list[k],
#                             final_cons[k],
#                             initial_discrete_state[k],
#                             initial_controller_state[k]) for k in range(num_systems)]

#         system_params_list = [SystemParams(
#             sys_init[k][0], # initial_state_set,
#             sys_init[k][1], # final_state_set,
#             sys_init[k][2], # is_final,
#             plant_sim,
#             controller_sim,
#             ci,
#             pi,
#             sampler,
#             final_cons,
#             pi_ref,
#             ci_ref
#             ) for k in range(num_systems)]


#         for k in range(num_systems):
#             SS.discover(current_abs[k], system_params_list[k])

#         if plot:
#             #plt.autoscale()
#             #ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
#             #plot_hack.LINE_LIST = []
#             plt.show()

#         for k in range(num_systems):
#             if not system_params_list[k].final_state_set:
#                 print('did not find any abstract counter example!', file=SYS.stderr)
#                 return False

#         print('analyzing graphs...')
#         for k in range(num_systems):
#             pi_ref[k].cleanup()
#             if ci_ref[k] is not None:
#                 ci_ref[k].cleanup()
#             # creates a new pi_ref, ci_ref
#             (promising_initial_states, ci_seq_list, pi_seq_list)\
#                 = current_abs.get_initial_states_from_error_paths(
#                         initial_state_set,
#                         final_state_set,
#                         pi_ref,
#                         ci_ref,
#                         pi,
#                         ci)

#         print('begin random testing!')
#         if plot:
#             f2 = plt.figure()
#             f2.suptitle('random testing')

#         print(len(promising_initial_states), len(ci_seq_list), len(pi_seq_list))
#         #U.pause()
#         # TODO: ugly...should it be another function?
#         # Read the TODO above the function definition for more details
#         (valid_promising_initial_state_list,
#             pi_seq_list, ci_seq_list) = SS.filter_invalid_abs_states(
#                         promising_initial_states,
#                         pi_seq_list,
#                         ci_seq_list,
#                         current_abs,
#                         init_cons)
#         print(len(valid_promising_initial_state_list), len(ci_seq_list), len(pi_seq_list))
#         #U.pause()
#         if valid_promising_initial_state_list == []:
#             print('no valid sample found during random testing. STOP', file=SYS.stderr)
#             return False
#         done = SS.random_test(
#             current_abs,
#             system_params,
#             valid_promising_initial_state_list,
#             ci_seq_list,
#             pi_seq_list,
#             init_cons,
#             initial_discrete_state,
#             initial_controller_state,
#             sample_ci
#             )
#         if plot:
#             #ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
#             plt.show()
#         if done:
#             print('Concretized', file=SYS.stderr)
#             return True

#         (current_abs, init_cons_list) = SS.refine_init_based(
#                 current_abs,
#                 promising_initial_states, # should it not be valid_promising_initial_state_list?
#                 original_plant_cons_list)#, pi_ref, ci_ref)
#         pi_ref.refine()
#         if ci_ref is not None:
#             ci_ref.refine()
#         i += 1
#     print('Failed: MAX iterations {} exceeded'.format(MAX_ITER), file=SYS.stderr)
#     # raise an exception maybe?


def discover(current_abs, init_cons_list, final_cons,
          initial_discrete_state, initial_controller_state, plant_sim,
          controller_sim, ci, pi, sampler, pi_ref, ci_ref, plot):
    # TODO: temp function ss.init()

    (initial_state_set, final_state_set, is_final) = \
        SS.init(current_abs, init_cons_list, final_cons,
                initial_discrete_state, initial_controller_state)

    system_params = SystemParams(
        initial_state_set,
        final_state_set,
        is_final,
        plant_sim,
        controller_sim,
        ci,
        pi,
        sampler,
        final_cons,
        pi_ref,
        ci_ref
        )
    SS.discover(current_abs, system_params)
    if plot: plt.show()
    return system_params


def get_init_states(pi_ref, ci_ref, current_abs, pi, ci, initial_state_set, final_state_set, init_cons, plot):

    pi_ref.cleanup()
    if ci_ref is not None:
        ci_ref.cleanup()
    # creates a new pi_ref, ci_ref
    (promising_initial_states,
        ci_seq_list,
        pi_seq_list) = current_abs.get_initial_states_from_error_paths(initial_state_set,
                                                                       final_state_set,
                                                                       pi_ref,
                                                                       ci_ref,
                                                                       pi,
                                                                       ci)

    # ##!!##logger.debug('promising initial states: {}'.format(promising_initial_states))

    print('begin random testing!')
    #if plot:
    #    f2 = plt.figure()
    #    f2.suptitle('random testing')

    print(len(promising_initial_states), len(ci_seq_list), len(pi_seq_list))
    #U.pause()
    # TODO: ugly...should it be another function?
    # Read the TODO above the function definition for more details
    (valid_promising_initial_state_list,
        pi_seq_list, ci_seq_list) = SS.filter_invalid_abs_states(
                    promising_initial_states,
                    pi_seq_list,
                    ci_seq_list,
                    current_abs,
                    init_cons)
    print(len(valid_promising_initial_state_list), len(ci_seq_list), len(pi_seq_list))
    return (promising_initial_states, valid_promising_initial_state_list, ci_seq_list, pi_seq_list)


def refinement_step(current_abs, promising_initial_states, original_plant_cons_list, ci_ref, pi_ref):

    (current_abs, init_cons_list) = SS.refine_init_based(
            current_abs,
            promising_initial_states, # should it not be valid_promising_initial_state_list?
            original_plant_cons_list)#, pi_ref, ci_ref)
    pi_ref.refine()
    if ci_ref is not None:
        ci_ref.refine()
    return current_abs, init_cons_list


# returns a True when its done
def refine_init_composable(
        current_abs,
        init_cons_list,
        final_cons,
        initial_discrete_state,
        initial_controller_state,
        plant_sim,
        controller_sim,
        ci,
        pi,
        sampler,
        plot,
        init_cons,
        original_plant_cons_list,
        MAX_ITER,
        sample_ci,
        pi_ref,
        ci_ref):

    num_sys = len(current_abs)

    i = 1
    while i <= MAX_ITER:
        print('iteration:', i)

#         print(current_abs)
#         print(init_cons_list[0][0])
#         print(final_cons[0])
#         print(initial_discrete_state,initial_controller_state,plant_sim)
#         print(controller_sim,ci,pi,sampler)
#         print(pi_ref,ci_ref)
        l_system_params = []
        for j in range(num_sys):
            args = (current_abs[j], init_cons_list[j], final_cons[j],
                    initial_discrete_state[j],
                    initial_controller_state[j], plant_sim[j],
                    controller_sim[j], ci[j], pi[j], sampler[j],
                    pi_ref[j], ci_ref[j], plot)
            l_system_params.append(discover(*args))

        # get the graph from every system and process it to search for
        # final states
        l_closest_nodes = chkp.search_final_abs_states(current_abs)
        if not l_closest_nodes:
            print('did not find any abstract counter example!', file=SYS.stderr)
            return False
        else:
            # assign final states
            for closest_nodes, system_params in zip(l_closest_nodes, l_system_params):
                system_params.final_state_set = set(closest_nodes)

        print('analyzing graph...')
        ret_vals = [get_init_states(pi_ref[j], ci_ref[j],
                                    current_abs[j], pi[j], ci[j],
                                    l_system_params[j].initial_state_set,
                                    l_system_params[j].final_state_set,
                    init_cons[j], plot) for j in range(num_sys)]

        promising_S0, valid_promising_S0, ci_seq_list, pi_seq_list = zip(*ret_vals)
        #for promising_S0, valid_promising_S0, ci_seq_list, pi_seq_list in ret_vals:
        err.warn('assumes all systems should return a violation. Could also be any!')
        for j in range(num_sys):
            if valid_promising_S0[j] == []:
                print('no valid sample found during random testing. STOP', file=SYS.stderr)
                return False

        l_traces = [SS.random_test_composable(current_abs[j],
                                              l_system_params[j],
                                              valid_promising_S0[j],
                                              ci_seq_list[j],
                                              pi_seq_list[j],
                                              init_cons[j],
                                              initial_discrete_state[j],
                                              initial_controller_state[j],
                                              sample_ci)
                    for j in range(num_sys)]

        violating_trace_pairs = chkp.search_final_concrete_states(l_traces)
        if violating_trace_pairs:
            print('Concretized', file=SYS.stderr)
            if plot:
                #for vio_pairs in violating_trace_pairs:
                    #traces.plot_trace_list(vio_pairs, plt)
                tl1, tl2 = zip(*violating_trace_pairs)
                traces.plot_trace_list(tl1+tl2, plt)
            return True
        err.warn_severe('Falied to concretize, refining')

        for j in range(num_sys):
            (current_abs[j], init_cons_list[j])\
                = refinement_step(current_abs[j], promising_S0[j],
                                  original_plant_cons_list[j], ci_ref[j], pi_ref[j])
        i += 1
    print('Failed: MAX iterations {} exceeded'.format(MAX_ITER), file=SYS.stderr)
    # raise an exception maybe?


# returns a True when its done
def refine_init(
        current_abs,
        init_cons_list,
        final_cons,
        initial_discrete_state,
        initial_controller_state,
        plant_sim,
        controller_sim,
        ci,
        pi,
        sampler,
        plot,
        init_cons,
        original_plant_cons_list,
        MAX_ITER,
        sample_ci,
        pi_ref,
        ci_ref):

    i = 1
    while i <= MAX_ITER:
        print('iteration:', i)
        # TODO: temp function ss.init()

        (initial_state_set, final_state_set, is_final) = \
            SS.init(current_abs, init_cons_list, final_cons,
                    initial_discrete_state, initial_controller_state)

        system_params = SystemParams(
            initial_state_set,
            final_state_set,
            is_final,
            plant_sim,
            controller_sim,
            ci,
            pi,
            sampler,
            final_cons,
            pi_ref,
            ci_ref
            )
        SS.discover(current_abs, system_params)

        if plot:
            #plt.autoscale()
            #ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
            #plot_hack.LINE_LIST = []
            plt.show()

        if not system_params.final_state_set:
            print('did not find any abstract counter example!', file=SYS.stderr)
            return False

        print('analyzing graph...')
        pi_ref.cleanup()
        if ci_ref is not None:
            ci_ref.cleanup()
        # creates a new pi_ref, ci_ref
        (promising_initial_states,
            ci_seq_list,
            pi_seq_list) = current_abs.get_initial_states_from_error_paths(initial_state_set,
                                                                           final_state_set,
                                                                           pi_ref,
                                                                           ci_ref,
                                                                           pi,
                                                                           ci)

        # ##!!##logger.debug('promising initial states: {}'.format(promising_initial_states))

        print('begin random testing!')
        if plot:
            f2 = plt.figure()
            f2.suptitle('random testing')

        print(len(promising_initial_states), len(ci_seq_list), len(pi_seq_list))
        #U.pause()
        # TODO: ugly...should it be another function?
        # Read the TODO above the function definition for more details
        (valid_promising_initial_state_list,
            pi_seq_list, ci_seq_list) = SS.filter_invalid_abs_states(
                        promising_initial_states,
                        pi_seq_list,
                        ci_seq_list,
                        current_abs,
                        init_cons)
        print(len(valid_promising_initial_state_list), len(ci_seq_list), len(pi_seq_list))
        #U.pause()
        if valid_promising_initial_state_list == []:
            print('no valid sample found during random testing. STOP', file=SYS.stderr)
            return False
        done = SS.random_test(
            current_abs,
            system_params,
            valid_promising_initial_state_list,
            ci_seq_list,
            pi_seq_list,
            init_cons,
            initial_discrete_state,
            initial_controller_state,
            sample_ci
            )
        if plot:
            #ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
            plt.show()
        if done:
            print('Concretized', file=SYS.stderr)
            return True

        (current_abs, init_cons_list) = SS.refine_init_based(
                current_abs,
                promising_initial_states, # should it not be valid_promising_initial_state_list?
                original_plant_cons_list)#, pi_ref, ci_ref)
        pi_ref.refine()
        if ci_ref is not None:
            ci_ref.refine()
        i += 1
    print('Failed: MAX iterations {} exceeded'.format(MAX_ITER), file=SYS.stderr)
    # raise an exception maybe?


def dump_trace(trace_list):
    print('dumping trace[0]')
    trace_list[0].dump_matlab()


def run_secam(sys_list, prop_list, opts):
    MODE = opts.MODE
    plot = opts.plot

    if MODE == 'simulate':
        start_time = time.time()
        trace_list = simulate(sys_list, prop_list, opts)
        if plot:
            if opts.dump_trace:
                dump_trace(trace_list)
            traces.plot_trace_list(trace_list, plt)
    elif MODE == 'falsify':
        # ignore time taken to create_abstraction: mainly to ignore parsing
        # time
        start_time = time.time()
        falsify(sys_list, prop_list, opts)
    else:
        raise err.Fatal('bad MODE supplied: {}'.format(MODE))

    stop_time = time.time()
    print('*'*20)
    print('time spent(s) = {}'.format(stop_time - start_time), file=SYS.stderr)
    return


def main():
    logger.info('execution begins')
    LIST_OF_SYEMX_ENGINES = ['klee', 'pathcrawler']
    LIST_OF_CONTROLLER_REPRS = ['smt2', 'trace']
    LIST_OF_TRACE_STRUCTS = ['list', 'tree']
    LIST_OF_REFINEMENTS = ['init', 'trace']

    usage = '%(prog)s <filename>'
    parser = argparse.ArgumentParser(description='S3CAM', usage=usage)
    parser.add_argument('-f', '--filename', default=None, metavar='file_path.tst')

    #parser.add_argument('--run-benchmarks', action="store_true", default=False,
    #                    help='run pacakged benchmarks')

    parser.add_argument('-s', '--simulate', type=int, metavar='num-sims',
                        help='simulate')
    parser.add_argument('-c', '--ss-concrete', action="store_true",
                        help='scatter & simulate')
    parser.add_argument('--ss-concolic', action="store_true",
                        help='scatter & simulate with concolic execution using KLEE')
    parser.add_argument('-x', '--ss-symex', type=str,
                        metavar='engine', choices=LIST_OF_SYEMX_ENGINES,
                        help='SS + SymEx with static paths')

    parser.add_argument('-r', '--cntrl-rep', type=str, metavar='repr',
                        choices=LIST_OF_CONTROLLER_REPRS,
                        help='Controller Representation')

    parser.add_argument('-p', '--plot', action='store_true',
                        help='enable plotting')

    parser.add_argument('--dump', action='store_true',
                        help='dump trace in mat file')

    parser.add_argument('--seed', type=int, metavar='seed_value',
                        default=None, help='seed for the random generator')

    # TAG:MSH
    parser.add_argument('--meng', type=str, metavar='engine_name',
                        default=None, help='Shared Matlab Engine name')

    parser.add_argument('-t', '--trace-struct', type=str, metavar='struct', default='tree',
                        choices=LIST_OF_TRACE_STRUCTS, help='structure for cntrl-rep')

    parser.add_argument('--refine', type=str, metavar='method', default='init',
                        choices=LIST_OF_REFINEMENTS, help='Refinement method')

    parser.add_argument('--decompose', action='store_true', help='Refinement method')

#    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    #print(args)

    if args.filename is None:
        print('No file to test. Please use --help')
        exit()
        print('No arguments passed. Loading list of packaged benchmarks!')
        example_list = eg.get_example_list()
        print('select from a list of examples')
        for (idx, example) in enumerate(example_list):
            print('({}) {}'.format(idx, example_list[idx]['description']))

        i = int(raw_input())
        filename = example_list[i]['filename']
        path = example_list[i]['path']
        filepath = fp.construct_path(filename, path)
    else:
        filepath = args.filename

    if args.seed is not None:
        np.random.seed(args.seed)

    # TODO:
    # dynamicall generate an opt class to mimic the same defined in
    # loadsystem.py
    # switch this to a reg class later.
    Options = type('Options', (), {})
    opts = Options()
    if args.simulate is not None:
        opts.MODE = 'simulate'
        opts.num_sim_samples = args.simulate
    elif args.ss_concrete:
        opts.MODE = 'falsify'
        opts.METHOD = 'concrete'
    elif args.ss_concolic:
        opts.MODE = 'falsify'
        opts.METHOD = 'concolic'
        print('removed concolic (KLEE)')
        exit(0)
    elif args.ss_symex is not None:
        opts.MODE = 'falsify'
        opts.METHOD = 'symbolic'
        opts.symbolic_analyzer = args.ss_symex
        #if opts.symbolic_analyzer not in LIST_OF_SYEMX_ENGINES:
        #    raise err.Fatal('unknown symbolic analyses engine requested.')
        if args.cntrl_rep is None:
            raise err.Fatal('controller representation must be provided')
        else:
            opts.cntrl_rep = args.cntrl_rep
            opts.trace_struct = args.trace_struct
    else:
        raise err.Fatal('no options passed. Check usage.')
    opts.plot = args.plot
    opts.dump_trace = args.dump
    opts.refine = args.refine
    opts.decompose = args.decompose

    sys, prop = loadsystem.parse(filepath)

    assert(not(sys.comp_scheme is None and args.ss_symex is not None))
    # opts.decompose => sys.comp_scheme is not None
    assert(not opts.decompose or sys.comp_scheme is not None)

    # TAG:MSH
    matlab_engine = args.meng

    if opts.decompose:
        sys_list, prop_list = loaddecomposedsystem.decompose(sys, prop)
        print('system:', sys_list)
        print()
        print('property:', prop_list)

        # Matlab SIM() is unsopported for compositional analyses
        # Should work in theory but have to work out the details
        assert(matlab_engine is None)
        for idx, sys_i in enumerate(sys_list):
            sys_i.init_sims(plt, psim_args=idx)
        # opts.decompose => sys/prop is actually sys_list/prop_list
    else:
        sys.init_sims(plt, psim_args=matlab_engine)
        sys_list = [sys]
        prop_list = [prop]

    if opts.plot:
        pass
        #import matplotlib

        # Force GTK3 backend. By default GTK2 gets loaded and conflicts with
        # graph-tool

        #matplotlib.use('GTK3Agg')
        #global plt
        #import matplotlib.pyplot as plt

    #sanity_check_input(sys, prop, opts)
    run_secam(sys_list, prop_list, opts)
    # ##!!##logger.debug('execution ends')

if __name__ == '__main__':
    main()
