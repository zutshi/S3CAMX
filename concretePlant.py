#!/usr/bin/python
# -*- coding: utf-8 -*-
import err
import utils as U

import logging

logger = logging.getLogger(__name__)


def compute_concrete_plant_output(
    A,
    plant_sim,
    states,
    total_num_samples,
    property_checker,
    ):

    # ##!!##logger.debug(U.decorate('simulating plant'))

    concrete_states = states

#    concrete_states = st.StateArray(
#        t_array,
#        x_array,                      # cont_state_array
#        d_array,                      # abs_state.discrete_state,
#        p_array,  # abs_state.pvt_state
#        None,   # don't need it
#        u_array)

    # simulate to get reached concrete states

    # ##!!##logger.debug('input concrete states\n{}'.format(concrete_states))

#    rchd_concrete_state_array = plant_sim.simulate(concrete_states,
#                                                     A.delta_t,
#                                                     property_checker=None)

    rchd_concrete_state_array = plant_sim.simulate(concrete_states, A.delta_t,
            property_checker, [False])

    # ##!!##logger.debug('output concrete states\n{}'.format(rchd_concrete_state_array))

    # ASSUMES:
    #   simulation was successful for each sample
    # This implies
    #   - The plant_sim returned a valid concrete state for each supplied
    #   sample
    #   - \forall i. output_array[i] = SIM(input_array[i]) is valid
    #     and len(output_array) = len(input_arra)
    # This need not be true always and we need to add plant_sim errors,
    # like returning (inf, inf, inf,...) ?
    # Some indication that simulation failed for the given state, without
    # destroying the assumed direct correspondance between
    # input array and output array

    if rchd_concrete_state_array.n != concrete_states.n:

        print rchd_concrete_state_array
        print
        print concrete_states

        raise err.Fatal('Internal')

    # ##!!##logger.debug(U.decorate('simulating plant done'))

    return rchd_concrete_state_array


