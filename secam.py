#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import matplotlib
# Force GTK3 backend. By default GTK2 gets loaded and conflicts with
# graph-tool
matplotlib.use('GTK3Agg')
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

import abstraction
import sample
import fileOps as fp
import concolicexec as CE
import simulatesystem as simsys
import scattersim as SS
import err
import loadsystem
import traces
import example_list as egl
import plothelper as ph
import plot_hack

#precision=None, threshold=None, edgeitems=None, linewidth=None, suppress=True, nanstr=None, infstr=None, formatter=Nonu)
np.set_printoptions(suppress=True)

###############################
## terminal color printing compatibility for windows
## https://pypi.python.org/pypi/colorama/0.2.4

## from colorama import init
## init()

## use this when we add windows portability
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
        return



def sanity_check_input(sys, prop, opts):
    return


# TODO: make a module of its own once we add more general property using
# monitors...
def check_prop_violation(trace, prop):
    idx = prop.final_cons.contains(trace.x_array)
    return trace.x_array[idx], trace.t_array[idx]


def simulate(sys, prop, opts):
    num_samples = opts.num_sim_samples
    num_violations = 0

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
    current_abs = abstraction.abstraction_factory(
        plant_config_dict,
        T,
        num_dims,
        controller_sym_path_obj,
        sys.min_smt_sample_dist,
        plant_abstraction_type,
        controller_abstraction_type,
        )
    return current_abs, sampler


#def falsify(sut, init_cons, final_cons, plant_sim, controller_sim, init_cons_list, ci, pi, current_abs, sampler):
def falsify(sys, prop, opts, current_abs, sampler):
    # sys
    controller_sim = sys.controller_sim
    plant_sim = sys.plant_sim

    # prop
    init_cons_list = prop.init_cons_list
    init_cons = prop.init_cons
    final_cons = prop.final_cons
    ci = prop.ci
    pi = prop.pi
    initial_discrete_state = prop.initial_discrete_state
    initial_controller_state = prop.initial_controller_state
    MAX_ITER = prop.MAX_ITER

    # options
    plot = opts.plot

    initial_discrete_state = tuple(initial_discrete_state)
    initial_controller_state = np.array(initial_controller_state)

    # make a copy of the original initial plant constraints

    original_plant_cons_list = init_cons_list

    i = 1
    while i <= MAX_ITER:

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
            )
        SS.discover(current_abs, system_params)

        if plot:
            #plt.autoscale()
            ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
            plot_hack.LINE_LIST = []
            plt.show()

        if not system_params.final_state_set:
            print('did not find any abstract counter example!', file=SYS.stderr)
            return
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
            return
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
            ph.figure_for_paper(plt.gca(), plot_hack.LINE_LIST)
            plt.show()
        if done:
            print('Concretized', file=SYS.stderr)
            return

        (current_abs, init_cons_list) = SS.refine_init_based(
                current_abs,
                promising_initial_states,
                original_plant_cons_list)
        i += 1

    print('Failed: MAX iterations {} exceeded.format(MAX_ITER)', file=SYS.stderr)


def run_secam(sys, prop, opts):
    MODE = opts.MODE
    plot = opts.plot

    if MODE == 'simulate':
        start_time = time.time()
        trace_list = simulate(sys, prop, opts)
        if plot:
            print('dumping trace[0]')
            trace_list[0].dump_matlab()
            traces.plot_trace_list(trace_list, plt)
    elif MODE == 'falsify':
        # ignore time taken to create_abstraction: mainly to ignore parsing
        # time
        current_abs, sampler = create_abstraction(sys, prop, opts)
        start_time = time.time()
        falsify(sys, prop, opts, current_abs, sampler)
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

    usage = '%(prog)s <filename>'
    parser = argparse.ArgumentParser(description='S3CAM', usage=usage)
    parser.add_argument('-f','--filename', default=None, metavar='file_path.tst')

    #parser.add_argument('--run-benchmarks', action="store_true", default=False,
    #                    help='run pacakged benchmarks')

    parser.add_argument('-s', '--simulate', type=int, metavar='num-sims',
                        help='simulate')
    parser.add_argument('-c', '--ss-concrete', action="store_true",
                        help='scatter & simulate')
    parser.add_argument('--ss-concolic', action="store_true",
                        help='scatter & simulate with concolic execution using KLEE')
    parser.add_argument('-x', '--ss-symex', type=str, metavar='engine', choices=LIST_OF_SYEMX_ENGINES,
                        help='SS + SymEx with static paths')

    parser.add_argument('-r', '--cntrl-rep', type=str, metavar='repr', choices=LIST_OF_CONTROLLER_REPRS,
                        help='Controller Representation')

    parser.add_argument('-p', '--plot', action='store_true',
                        help='enable plotting')

    parser.add_argument('--seed', type=int, metavar='seed_value',
                        help='seed for the random generator')

    # TAG:MSH
    parser.add_argument('--meng', type=str, metavar='engine_name',
                        help='Shared Matlab Engine name')

    parser.add_argument('-t', '--trace-struct', type=str, metavar='struct', default='tree',
                        choices=LIST_OF_TRACE_STRUCTS, help='structure for cntrl-rep')

#    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    #print(args)

    if args.filename is None:
        print('No file to test. Please use --help')
        exit()
        print('No arguments passed. Loading list of packaged benchmarks!')
        example_list = egl.get_example_list()
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

    sys, prop = loadsystem.parse(filepath)
    # TAG:MSH
    matlab_engine = args.meng
    sys.init_sims(plt, psim_args=matlab_engine)

    if opts.plot:
        pass
        #import matplotlib

        # Force GTK3 backend. By default GTK2 gets loaded and conflicts with
        # graph-tool

        #matplotlib.use('GTK3Agg')
        #global plt
        #import matplotlib.pyplot as plt
    sanity_check_input(sys, prop, opts)
    run_secam(sys, prop, opts)
    # ##!!##logger.debug('execution ends')

if __name__ == '__main__':
    main()
