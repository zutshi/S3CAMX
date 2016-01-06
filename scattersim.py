#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import Queue
import numpy as np

import abstraction as AA
import state as st
import err
import sample as SaMpLe
import utils as U
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

    # print '='*80
    # print 'all final states'
    # for ps in plant_final_state_set:
    #    print ps
    # print '='*80

    def is_final(abs_state):

#        print '----------isfinal-----------'
#        print abs_state.plant_state.cell_id == ps.cell_id
#        print abs_state.plant_state in plant_final_state_set
#        print hash(abs_state.plant_state), hash(ps)
#        print abs_state.plant_state == ps
#        if abs_state.plant_state.cell_id == ps.cell_id:
#            exit()

        # return abs_state.plant_state in plant_final_state_set

        return PA.get_ival_constraints(abs_state.plant_state) & final_cons \
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

        if not (A.is_terminal(abs_state) or abs_state in examined_state_set):

            # ##!!##logger.debug('decided to process abs_state')

            pass

            # Mark it as examined

            examined_state_set.add(abs_state)

            # Find all reachable abstract states using simulations

            abs2rch_abs_state_dict = get_reachable_abs_states(A,
                    system_params, [abs_state])

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

                if system_params.is_final(rchd_abs_state):
                    system_params.final_state_set.add(rchd_abs_state)
                else:

                    # print 'found a final state'
                    # exit()

                    Q.put(rchd_abs_state, False)


                # moving below to the abstraction itself
                # A.add_relation(abs_state, rchd_abs_state)

                # A.G.add_edge(abs_state, rchd_abs_state)
#                    n = self.get_n_for(abs_state) + 1
#                    self.set_n_for(rchd_abs_state, n)

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
            abs2rch_abs_state_dict = get_reachable_abs_states(A,
                    abs_state_list_to_examine)

            # print abs2rch_abs_state_dict

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

            for (abs_state, rchd_abs_state_set) in \
                abs2rch_abs_state_dict.iteritems():
                for rchd_abs_state in rchd_abs_state_set:
                    A.add_relation(abs_state, rchd_abs_state)


                    # A.G.add_edge(abs_state, rchd_abs_state)
#                        n = self.get_n_for(abs_state) + 1
#                        self.set_n_for(rchd_abs_state, n)

    # end while loop

    # ##!!##logger.debug('Abstraction discovery done')
    # ##!!##logger.debug('Printing Abstraction\n {}'.format(str(A)))

def refine_state(A, RA, abs_state):
    c = A.get_concrete_state_constraints(abs_state)
    return RA.get_abs_state_set_from_ival_constraints(c)


# refine using entire traces
# TODO: unattended for long......make sure its same before using it!

def refine_trace_based(A):

    # ##!!##logger.debug('executing trace based refinement')

    # eps

    new_eps = A.eps / A.refinement_factor

    error_paths = A.compute_error_paths()

    traversed_state_list = []
    for path in error_paths:
        print 'p:', path
        traversed_state_list += path
    if not traversed_state_list:
        print 'No error path found!'
        exit()
    traversed_state_set = set(traversed_state_list)
    print 'traversed_state_set:', traversed_state_set

    init_cons_list = []
    initial_abs_states = A.get_initial_states_from_error_paths()
    for init_state in initial_abs_states:
        c = A.get_concrete_state_constraints(init_state)
        init_cons_list.append(c)

    param_dict = {
        'eps': new_eps,
        'refinement_factor': A.refinement_factor,
        'num_samples': A.num_samples,
        'delta_t': A.delta_t,
        'N': A.N,
        'type': 'value',
        }

    AA.AbstractState.clear()
    RA = AA.GridBasedAbstraction(  # A.T,
        param_dict,
        A.plant_sim,
        A.delta_t,
        A.sample,
        init_cons_list,
        A.final_cons,
        A.controller_sim,
        A.num_dims,
        prog_bar=False,
        )

    # split the traversed states

    refined_ts_list = []
    for ts in traversed_state_set:
        rs = refine_state(A, RA, ts)
        refined_ts_list += list(rs)

    for a in refined_ts_list:

        # set it to 0, so never will get updated

        RA.set_n_for(a, 0)

    abs2rch_abs_state_dict = get_reachable_abs_states(RA, refined_ts_list)

    rchd_abs_state_set = set.union(*abs2rch_abs_state_dict.values())

    for (abs_state, rchd_abs_state_set) in abs2rch_abs_state_dict.iteritems():
        for rchd_abs_state in rchd_abs_state_set:

            # RA.G.add_edge(abs_state, rchd_abs_state)

            RA.add_relation(abs_state, rchd_abs_state)

    # restore sanity ;)

    RA.T = (A.T, )
    return RA


# refine using init states

def refine_init_based(A, promising_initial_abs_states,
                      original_plant_cons_list):

    # ##!!##logger.debug('executing init based refinement')
    # eps

    new_eps = A.eps / A.refinement_factor

    # checks if the given constraint has a non empty intersection with the
    # given plant initial states. These are the actual initial plant sets
    # specified in the tst file.

    def in_origianl_initial_plant_cons(ic):
        for oic in original_plant_cons_list:
            if oic & ic:
                return True
        return False

    init_cons_list = []

    # ignore cells which have no overlap with the initial state

    for init_state in promising_initial_abs_states:
        ic = A.plant_abs.get_ival_constraints(init_state.plant_state)
        if in_origianl_initial_plant_cons(ic):
            init_cons_list.append(ic)

    param_dict = {
        'eps': new_eps,
        'refinement_factor': A.refinement_factor,
        'num_samples': A.num_samples,
        'delta_t': A.delta_t,
        'N': A.N,
        'type': 'value',
        }

#    AA.AbstractState.clear()

    refined_abs = AA.abstraction_factory(
        param_dict,
        A.T,
        A.num_dims,
        A.controller_sym_path_obj,
        A.min_smt_sample_dist,
        A.plant_abstraction_type,
        A.controller_abstraction_type,
        )

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

        samples = system_params.sampler.sample(abs_state, A, system_params,
                A.num_samples)

        # ##!!##logger.debug('{}'.format(samples))

        abs_state2samples_list.append(samples.n)
        consolidated_samples.append(samples)

#    # ##!!##logger.debug('{}'.format(consolidated_samples))

    total_num_samples = consolidated_samples.n

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
def filter_invalid_abs_states(state_list, A, init_cons):
    valid_state_list = []
    for abs_state in state_list:
        ival_cons = A.plant_abs.get_ival_constraints(abs_state.plant_state)

        # ##!!##logger.debug('ival_cons: {}'.format(ival_cons))

        # find the intersection b/w the cell and the initial cons
        # print 'init_cons', init_cons

        ic = ival_cons & init_cons
        if ic is not None:
            valid_state_list.append(abs_state)

    # TODO: this should be logged and not printed
    if valid_state_list == []:
        for abs_state in state_list:
            ival_cons = A.plant_abs.get_ival_constraints(abs_state.plant_state)
            print ival_cons
    return valid_state_list


def random_test(
        A,
        system_params,
        initial_state_list,
        ci_seq_list,
        init_cons,
        init_d,
        initial_controller_state,
        ):

    # ##!!##logger.debug('random testing...')

    A.prog_bar = False

    # initial_state_set = set(initial_state_list)

    if A.num_dims.ci == 0:
        pass
    else:
        ci_seq_array = np.array(ci_seq_list)

        # print 'ci_seq_array', ci_seq_array
        # print 'ci_seq_array.shape', ci_seq_array.shape

    x_array = np.empty((0.0, A.num_dims.x), dtype=float)
    print 'checking initial states'

    # for abs_state in initial_state_set:

    for abs_state in initial_state_list:
        ival_cons = A.plant_abs.get_ival_constraints(abs_state.plant_state)

        # ##!!##logger.debug('ival_cons: {}'.format(ival_cons))

        # find the intersection b/w the cell and the initial cons
        # print 'init_cons', init_cons

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

            pass

    # print x_array
    # print x_array.shape

    num_samples = len(x_array)
    if num_samples == 0:
        print initial_state_list
        print 'no valid sample found during random testing. STOP'
        return False
    else:

        # ##!!##logger.debug('num_samples = 0')

        print 'simulating {} samples'.format(num_samples)

    s_array = np.tile(initial_controller_state, (num_samples, 1))

    if system_params.pi is not None:
        pi_array = SaMpLe.sample_ival_constraints(system_params.pi,
                num_samples)
    else:
        pi_array = None

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

    sim_num = 0
    simTime = 0.0
    i = 0

    # while(simTime < A.T):

    while sim_num < A.N:

        if A.num_dims.ci == 0:
            ci_array = np.zeros((num_samples, 0))
        else:
            ci_array = ci_seq_array[:, i, :]
            ci_array = np.repeat(ci_array, A.num_samples, axis=0)

            # print 'ci_array', ci_array
            # print 'shape(ci_array) =', ci_array.shape
            # print 'shape(x_array) =', x_array.shape
            # print ci_seq_array
            # print ci_array
        # ##!!##logger.debug('{}'.format(ci_array))

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

        # print concrete_states

        property_violated_flag = [False]
        property_checker = lambda t, Y: Y in system_params.final_cons

        rchd_concrete_state_array = \
            system_params.plant_sim.simulate(concrete_states, A.delta_t,
                property_checker, property_violated_flag)

        if property_violated_flag[0]:
            print U.decorate('concretized!')
            for (idx, xf) in enumerate(rchd_concrete_state_array.iterable()):
                if xf.x in system_params.final_cons:
                    print x0_array[idx, :], d0_array[idx, :], '->', '\t', xf.x, xf.d
                    if A.num_dims.ci != 0:
                        print 'ci:', ci_array[idx]
            res = True
            break
        else:

            # print 'failed to concretize'

            res = False
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

    return res


def check_sat_any(x_array, cons):
    return cons.any_sat(x_array)
