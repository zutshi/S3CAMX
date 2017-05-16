#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import Queue
import numpy as np

import abstraction as AA
import state as st
import err
import sample as SaMpLe
import utils as U
from utils import print
import traces
#from utils import print
import concreteController as cc

logger = logging.getLogger(__name__)

np.set_printoptions(suppress=True)


# TODO: plant state centric....attaches other states to plant states. make it
# neutral, gets touples of ((cons, d), s)

def init(
        A,
        init_cons_list_plant,
        final_cons,
        init_d,
        controller_init_state,
        ):

    PA = A.plant_abs
    CA = A.controller_abs
    plant_initial_state_list = []
    d = init_d
    pvt = (0, )
    n = 0

    for init_cons in init_cons_list_plant:
        plant_initial_state_list += \
            PA.get_abs_state_set_from_ival_constraints(init_cons, n, d, pvt)
    plant_initial_state_set = set(plant_initial_state_list)

    # The below can be very very expensive in time and memory for large final
    # sets!
    # plant_final_state_set = \
    #    set(PA.get_abs_state_set_from_ival_constraints(final_cons, 0, 0, 0))

    # ##!!##logger.debug('{0}initial plant states{0}\n{1}'.format('=' * 10, plant_initial_state_set))

    # set control states for initial states
    # TODO: ideally the initial control states should be supplied by the
    # user and the below initialization should be agnostic to the type

    controller_init_abs_state = \
        CA.get_abs_state_from_concrete_state(controller_init_state)

    initial_state_list = []
    for plant_init_state in plant_initial_state_set:
        initial_state_list.append(AA.TopLevelAbs.get_abs_state(plant_state=plant_init_state,
                                  controller_state=controller_init_abs_state))

    final_state_list = []

#    for plant_final_state in plant_final_state_set:
#        final_state_list.append(AA.TopLevelAbs.get_abs_state(
#            plant_state=plant_final_state,
#            controller_state=controller_init_abs_state))

    # print('='*80)
    # print('all final states')
    # for ps in plant_final_state_set:
    #    print(ps)
    # print('='*80)

    def is_final(_A, abs_state):

        #print('----------isfinal-----------')
        #print(abs_state.plant_state.cell_id == ps.cell_id)
        #print(abs_state.plant_state in plant_final_state_set)
        #print(hash(abs_state.plant_state), hash(ps))
        #print(abs_state.plant_state == ps)
        #if abs_state.plant_state.cell_id == ps.cell_id:
            #exit()

        # return abs_state.plant_state in plant_final_state_set

        #print('---------------------------------------------')
        #print(_A.plant_abs.get_ival_constraints(abs_state.ps))
        #print('---------------------------------------------')
        return _A.plant_abs.get_ival_cons_abs_state(abs_state.plant_state) & final_cons \
            is not None

    # ##!!##logger.debug('{0}initial{0}\n{1}'.format('=' * 10, plant_initial_state_set))

    return (set(initial_state_list), set(final_state_list), is_final)


# TODO: move set_n, get_n here, because no other exploration process might want to use it?
# Calls the simulator for each abstract state

def discover(A, system_params, budget=None):
    Q = Queue.Queue(maxsize=0)
    examined_state_set = set()

    # initialize the Q with initial states

    # ##!!##logger.debug('Adding initial states to Q')

    for init_state in system_params.initial_state_set:
        Q.put(init_state)

    while not Q.empty():
        abs_state = Q.get(False)

        # ##!!##logger.debug('{} = Q.get()'.format(abs_state))

        #print('retrieving from Q:', abs_state, abs_state in examined_state_set, A.is_terminal(abs_state))
        if not (A.is_terminal(abs_state) or abs_state in examined_state_set):

            # ##!!##logger.debug('decided to process abs_state')

            # Mark it as examined

            examined_state_set.add(abs_state)

            # Find all reachable abstract states using simulations

            abs2rch_abs_state_dict = get_reachable_abs_states(A, system_params, [abs_state])

            # add the new reached states only if they have not been
            # processed before

            # ##!!##logger.debug('abs2rch_abs_state_dict.values()\n{}'.format(abs2rch_abs_state_dict.values()))

            rchd_abs_state_set = abs2rch_abs_state_dict[abs_state]

            # TODO: abstract away the graph maybe??
            # Hide the call behind add_relation(A1, A2)

            for rchd_abs_state in rchd_abs_state_set:

                # ##!!##logger.debug('reached abstract state {}'.format(rchd_abs_state))

                # query if the reached state is a final state or not?
                # If yes, tag it so

                #print('rchd:', rchd_abs_state)
                if system_params.is_final(A, rchd_abs_state):
                    system_params.final_state_set.add(rchd_abs_state)
                    print('tagging as final')
                else:

                    # print('found a final state')
                    # exit()

                    Q.put(rchd_abs_state, False)

                # moving below to the abstraction itself
                # A.add_relation(abs_state, rchd_abs_state)

                # A.G.add_edge(abs_state, rchd_abs_state)
#                    n = self.get_n_for(abs_state) + 1
#                    self.set_n_for(rchd_abs_state, n)
    print('done')
    # end while loop

    # ##!!##logger.debug('Abstraction discovery done')
    # ##!!##logger.debug('Printing Abstraction\n {}'.format(str(A)))

# Same as discover_old, but accumulates all abstract states from the Q before
# calling get_reachable_abs_states() on the entire group
# This makes it potentially faster, because fewer simulator calls are
# needed.


def discover_batch(A, budget=None):
    Q = Queue.Queue(maxsize=0)
    examined_state_set = set()

    abs_state_list_to_examine = []

    # initialize the Q with initial states

    # ##!!##logger.debug('Adding initial states to Q')

    for init_state in A.initial_state_set:
        Q.put(init_state)

    while not Q.empty():
        abs_state_list_to_examine = []

        # Empty the Q

        while not Q.empty():
            abs_state = Q.get(False)

            # ##!!##logger.debug('{} = Q.get()'.format(abs_state))

            if not (A.is_terminal(abs_state) or abs_state
                    in examined_state_set):

                # ##!!##logger.debug('decided to process abs_state')

                # Mark it as examined

                examined_state_set.add(abs_state)

                # Collect all abstract states which need to be examined

                abs_state_list_to_examine.append(abs_state)
            else:

                # ##!!##logger.debug('NOT going to process abstract state')

                pass

        # end inner while

        # ##!!##logger.debug('get_reachable_abs_states() for...\n{}'.format(abs_state_list_to_examine))

        if abs_state_list_to_examine:
            abs2rch_abs_state_dict = get_reachable_abs_states(A, abs_state_list_to_examine)

            # print(abs2rch_abs_state_dict)

            # ##!!##logger.debug('abs2rch_abs_state_dict.values()\n{}'.format(abs2rch_abs_state_dict.values()))

            rchd_abs_state_set = set.union(*abs2rch_abs_state_dict.values())

            # add the new reached states only if they have not been
            # processed before

            for rchd_abs_state in rchd_abs_state_set:

                # ##!!##logger.debug('reached abstract state {}'.format(rchd_abs_state))

                Q.put(rchd_abs_state, False)

            # Add the relation even if state has been seen before,
            # because the edge might
            # not have had been...can check for edge's presence too,
            # but will need to change
            # later when we will add weights...where we will probably
            # update weights in
            # adfition to adding edges.
            # encode the new relations in the graph, no weights for
            # now!
            # TODO: abstract away the graph maybe??
            # Hide the call behind add_relation(A1, A2)

            for (abs_state, rchd_abs_state_set) in abs2rch_abs_state_dict.iteritems():
                for rchd_abs_state in rchd_abs_state_set:
                    A.add_relation(abs_state, rchd_abs_state)

                    # A.G.add_edge(abs_state, rchd_abs_state)
#                        n = self.get_n_for(abs_state) + 1
#                        self.set_n_for(rchd_abs_state, n)

    # end while loop

    # ##!!##logger.debug('Abstraction discovery done')
    # ##!!##logger.debug('Printing Abstraction\n {}'.format(str(A)))


def refine_state(A, RA, abs_state):
    ps = abs_state.ps
    cs = abs_state.cs
    ps_ival = A.plant_abs.get_ival_cons_abs_state(ps)
    refined_ps_set = RA.plant_abs.get_abs_state_set_from_ival_constraints(ps_ival, ps.n, ps.d, ps.pvt)
    abs_state_list = []
    if A.controller_abs.is_symbolic:
        for rps in refined_ps_set:
            x_smt2 = RA.plant_abs.get_smt2_constraints(rps, cs.x)
            cs.C = RA.controller_abs.solver.And(cs.C, x_smt2)
            AA.AbstractState(rps, cs)
            abs_state_list.append(abs_state)
    else:
        for rps in refined_ps_set:
            AA.AbstractState(rps, cs)
            abs_state_list.append(abs_state)
    return abs_state_list


def refine_param_dict(A):
    new_eps = A.eps / A.refinement_factor
    #new_pi_eps = A.pi_eps / A.refinement_factor
    param_dict = {
        'eps': new_eps,
        #'pi_eps': new_pi_eps,
        'refinement_factor': A.refinement_factor,
        'num_samples': A.num_samples,
        'delta_t': A.delta_t,
        'N': A.N,
        'type': 'value',
        }
    return param_dict


def refine_trace_based(A, error_paths, system_params):

    # ##!!##logger.debug('executing trace based refinement')

    traversed_state_set = set()
    sap = A.states_along_paths(error_paths)
    for path in sap:
        traversed_state_set.update(path)

    param_dict = refine_param_dict(A)

    RA = AA.abstraction_factory(
        param_dict,
        A.T,
        A.num_dims,
        A.controller_sym_path_obj,
        A.min_smt_sample_dist,
        A.plant_abstraction_type,
        A.controller_abstraction_type
        )

    # split the traversed states

    # construct a list of sets and then flatten
    #refined_ts_list = U.flatten( [refine_state(A, RA, ts) for ts in traversed_state_set])

    #abs2rch_abs_state_dict = get_reachable_abs_states(RA, system_params, refined_ts_list)

    return RA


# refine using init states
def refine_init_based(A, promising_initial_abs_states,
                      original_plant_cons_list):#, pi_ref, ci_ref):

    # ##!!##logger.debug('executing init based refinement')

    # checks if the given constraint has a non empty intersection with the
    # given plant initial states. These are the actual initial plant sets
    # specified in the tst file.

    def in_origianl_initial_plant_cons(ic):
        for oic in original_plant_cons_list:
            if oic & ic:
                return True
        assert('Should never happen. Should be caught by SS.filter_invalid_abs_states')
        return False

    init_cons_list = []

    # ignore cells which have no overlap with the initial state

    for init_state in promising_initial_abs_states:
        ic = A.plant_abs.get_ival_cons_abs_state(init_state.plant_state)
        if in_origianl_initial_plant_cons(ic):
            init_cons_list.append(ic)

    param_dict = refine_param_dict(A)

#    AA.AbstractState.clear()

    refined_abs = AA.abstraction_factory(
        param_dict,
        A.T,
        A.num_dims,
        A.controller_sym_path_obj,
        #A.ci_grid_eps/2,
        A.min_smt_sample_dist,
        A.plant_abstraction_type,
        A.controller_abstraction_type,
        )

    # TODO: what a hack!
    #pi_ref = A.plant_abs.pi_ref
#     pi_ref.refine()
#     ci_ref.refine()
#     refined_abs.plant_abs.pi_ref = pi_ref
#     refined_abs.controller_abs.ci_ref = ci_ref

#    refined_abs = AA.GridBasedAbstraction(param_dict,
#                                          A.plant_sim,
#                                          A.T,
#                                          A.sample,
#                                          init_cons_list,
#                                          A.final_cons,
#                                          A.controller_sim,
#                                          A.num_dims,
#                                          prog_bar=True)

    return (refined_abs, init_cons_list)


# samples a list of abstract states and collates the resulting samples

def sample_abs_state_list(A, system_params, abs_state_list):

    # ##!!##logger.debug(U.decorate('sampling begins'))

    # List to store reachble concrete states:
    # stores number of samples in the same order as abstract states in
    # abs_state_list and of course
    # len(abs_state_list) =  abs_state2samples_list

    abs_state2samples_list = []

    consolidated_samples = SaMpLe.Samples()

    for abs_state in abs_state_list:

        # scatter the continuous states

        # ##!!##logger.debug('sampling({})'.format(abs_state))

        samples = system_params.sampler.sample(abs_state, A, system_params, A.num_samples)

        # ##!!##logger.debug('{}'.format(samples))

        abs_state2samples_list.append(samples.n)
        consolidated_samples.append(samples)

#    # ##!!##logger.debug('{}'.format(consolidated_samples))

    #total_num_samples = consolidated_samples.n

    # ##!!##logger.debug('num_samples = {}'.format(total_num_samples))
    # ##!!##logger.debug('samples = \n{}'.format(samples))
    # ##!!##logger.debug(U.decorate('sampling done'))

    return (abs_state2samples_list, consolidated_samples)


# Returns abs2rchd_abs_state_map: a mapping
# abstract_state |-> set(reached abstract states)
# It is debatable if this is the best return format! ;)

def get_reachable_abs_states(A, system_params, abs_state_list):

    # Dictionary mapping: abstract state |-> set(reached abstract state)

    abs2rchd_abs_state_map = {}

    for abs_state in abs_state_list:
        abs2rchd_abs_state_map[abs_state] = A.get_reachable_states(abs_state, system_params)

    return abs2rchd_abs_state_map


# TODO: ugly...should it be another function?
# Only reason its been pulled out from random_test is to ease the detection of
# the case when no valid abstract state is left!
# VERY INEFFICIENT
# Repeats some work done in random_test...
def filter_invalid_abs_states(state_list, pi_seq_list, ci_seq_list, A, init_cons):
    valid_idx_list = []

    for idx, abs_state in enumerate(state_list):
        ival_cons = A.plant_abs.get_ival_cons_abs_state(abs_state.plant_state)

        # ##!!##logger.debug('ival_cons: {}'.format(ival_cons))

        # find the intersection b/w the cell and the initial cons
        # print('init_cons', init_cons)

        ic = ival_cons & init_cons
        if ic is not None:
            valid_idx_list.append(idx)
            #valid_state_list.append(abs_state)

    # TODO: this should be logged and not printed
    if valid_idx_list == []:
        for abs_state in state_list:
            ival_cons = A.plant_abs.get_ival_cons_abs_state(abs_state.plant_state)
            print(ival_cons)

    valid_state_list = []
    respective_pi_seq_list = []
    respective_ci_seq_list = []
    for i in valid_idx_list:
        valid_state_list.append(state_list[i])
        respective_pi_seq_list.append(pi_seq_list[i])
        respective_ci_seq_list.append(ci_seq_list[i])
    return valid_state_list, respective_pi_seq_list, respective_ci_seq_list


def random_test(
        A,
        system_params,
        initial_state_list,
        ci_seq_list,
        pi_seq_list,
        init_cons,
        init_d,
        initial_controller_state,
        sample_ci
        ):

    # ##!!##logger.debug('random testing...')

    A.prog_bar = False

    res = []
    # initial_state_set = set(initial_state_list)

    if A.num_dims.ci != 0:
        if sample_ci:
            ci_seq_array = np.array([np.array(ci_seq_list).T]).T
        else:
            ci_seq_array = np.array(ci_seq_list)

        # print('ci_seq_array', ci_seq_array)
        # print('ci_seq_array.shape', ci_seq_array.shape)

    if A.num_dims.pi != 0:
        pi_seq_array = np.array([np.array(pi_seq_list).T]).T

    #print(ci_seq_array.shape)
    #print(pi_seq_array.shape)
    x_array = np.empty((0, A.num_dims.x), dtype=float)

    print('checking initial states')

    # for abs_state in initial_state_set:

    for abs_state in initial_state_list:
        ival_cons = A.plant_abs.get_ival_cons_abs_state(abs_state.plant_state)

        # ##!!##logger.debug('ival_cons: {}'.format(ival_cons))

        # find the intersection b/w the cell and the initial cons
        # print('init_cons', init_cons)

        ic = ival_cons & init_cons
        if ic is not None:

            # scatter the continuous states

            x_samples = SaMpLe.sample_ival_constraints(ic, A.num_samples)

            # ##!!##logger.debug('ic: {}'.format(ic))
            # ##!!##logger.debug('samples: {}'.format(x_samples))

            x_array = np.concatenate((x_array, x_samples))
        else:
            raise err.Fatal('Can not happen! Invalid states have already been filtered out by filter_invalid_abs_states()')

            # # ##!!##logger.debug('{}'.format(samples.x_array))

            # ##!!##logger.debug('ignoring abs states: {}'.format(ival_cons))

            # ignore the state as it is completely outside the initial
            # constraints

    # print(x_array)
    # print(x_array.shape)

    print(x_array.shape)
    num_samples = len(x_array)
    if num_samples == 0:
        print(initial_state_list)
        print('no valid sample found during random testing. STOP')
        return False
    else:

        # ##!!##logger.debug('num_samples = 0')

        print('simulating {} samples'.format(num_samples))

    trace_list = [traces.Trace(A.num_dims, A.N) for i in range(num_samples)]

    s_array = np.tile(initial_controller_state, (num_samples, 1))

#     if system_params.pi is not None:
#         pi_array = SaMpLe.sample_ival_constraints(system_params.pi, num_samples)
#         print(pi_array)
#         exit()
#     else:
#         pi_array = None

    t_array = np.tile(0.0, (num_samples, 1))

    d_array = np.tile(init_d, (num_samples, 1))

    # TODO: initializing pvt states to 0

    p_array = np.zeros((num_samples, 1))

    # save x_array to print x0 in case an error is found
    # TODO: need to do something similar for u,ci,pi

    x0_array = x_array
    d0_array = d_array

    # sanity check

    if len(x_array) != len(s_array):
        raise err.Fatal('internal: how is len(x_array) != len(s_array)?')

    def property_checker(t, Y): return Y in system_params.final_cons

    # while(simTime < A.T):
    sim_num = 0
    simTime = 0.0
    i = 0
    while sim_num < A.N:
        if A.num_dims.ci == 0:
            ci_array = np.zeros((num_samples, 0))
        else:
            if sample_ci:
                ci_cons_list = list(ci_seq_array[:, i, :])
                ci_cons_list = [ci_cons.tolist()[0] for ci_cons in ci_cons_list]

                ci_lb_list = [np.tile(ci_cons.l, (A.num_samples, 1)) for ci_cons in ci_cons_list]
                ci_ub_list = [np.tile(ci_cons.h, (A.num_samples, 1)) for ci_cons in ci_cons_list]

                ci_cons_lb = reduce(lambda acc_arr, arr: np.concatenate((acc_arr, arr)), ci_lb_list)
                ci_cons_ub = reduce(lambda acc_arr, arr: np.concatenate((acc_arr, arr)), ci_ub_list)

                random_arr = np.random.rand(num_samples, A.num_dims.ci)

                ci_array = ci_cons_lb + random_arr * (ci_cons_ub - ci_cons_lb)
            else:
                ci_array = ci_seq_array[:, i, :]
                ci_array = np.repeat(ci_array, A.num_samples, axis=0)

        if A.num_dims.pi == 0:
            pi_array = np.zeros((num_samples, 0))
        else:
            pi_cons_list = list(pi_seq_array[:, i, :])
            pi_cons_list = [pi_cons.tolist()[0] for pi_cons in pi_cons_list]
            #print(pi_cons_list)
            #pi_cons_list = map(A.plant_abs.get_ival_cons_pi_cell, pi_cells)

            pi_lb_list = [np.tile(pi_cons.l, (A.num_samples, 1)) for pi_cons in pi_cons_list]
            pi_ub_list = [np.tile(pi_cons.h, (A.num_samples, 1)) for pi_cons in pi_cons_list]

            pi_cons_lb = reduce(lambda acc_arr, arr: np.concatenate((acc_arr, arr)), pi_lb_list)
            pi_cons_ub = reduce(lambda acc_arr, arr: np.concatenate((acc_arr, arr)), pi_ub_list)

            random_arr = np.random.rand(num_samples, A.num_dims.pi)

#             print('pi_cons_lb.shape:', pi_cons_lb.shape)
#             print('pi_cons_ub.shape:', pi_cons_ub.shape)
#             print('num_samples', num_samples)
            pi_array = pi_cons_lb + random_arr * (pi_cons_ub - pi_cons_lb)

        (s_array_, u_array) = cc.compute_concrete_controller_output(
            A,
            system_params.controller_sim,
            ci_array,
            x_array,
            s_array,
            num_samples,
            )

        concrete_states = st.StateArray(  # t
                                        # cont_state_array
                                        # abs_state.discrete_state
                                        # abs_state.pvt_stat
                                        t_array,
                                        x_array,
                                        d_array,
                                        p_array,
                                        s_array_,
                                        u_array,
                                        pi_array,
                                        ci_array,
                                        )

        # print(concrete_states)

        property_violated_flag = [False]

        rchd_concrete_state_array = system_params.plant_sim.simulate(
                concrete_states,
                A.delta_t,
                property_checker,
                property_violated_flag)

        for kdx, rchd_state in enumerate(rchd_concrete_state_array.iterable()):
            trace = trace_list[kdx]
            trace.append(rchd_state.s, rchd_state.u, rchd_state.x, rchd_state.ci, rchd_state.pi, rchd_state.t, rchd_state.d)

        if property_violated_flag[0]:
            print(U.decorate('concretized!'))
            for (idx, xf) in enumerate(rchd_concrete_state_array.iterable()):
                if xf.x in system_params.final_cons:
                    res.append(idx)
                    print(x0_array[idx, :], d0_array[idx, :], '->', '\t', xf.x, xf.d)
                    #if A.num_dims.ci != 0:
                    #    print('ci:', ci_array[idx])
                    #if A.num_dims.pi != 0:
                    #    print('pi:', pi_array[idx])
            break
        i += 1
        sim_num += 1

        # increment simulation time

        simTime += A.delta_t
        t_array += A.delta_t
        concrete_states = rchd_concrete_state_array
        x_array = concrete_states.cont_states
        s_array = concrete_states.controller_states
        d_array = concrete_states.discrete_states
        p_array = concrete_states.pvt_states

        # u_array =

    return map(trace_list.__getitem__, res)


def check_sat_any(x_array, cons):
    return cons.any_sat(x_array)
