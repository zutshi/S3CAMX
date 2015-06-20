#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import logging
import controlifc as cifc
import utils as U

logger = logging.getLogger(__name__)


def compute_concrete_controller_output(
    A,
    controller_sim,
    ci_array,
    x_array,
    s_array,
    total_num_samples,
    ):

    # ##!!##logger.debug(U.decorate('simulating controller'))

    n = total_num_samples

    # This step can be redundant when using concolic execution, because
    # klee replay library can be used, though its not clear how efficient
    # it is! Hence using the actual execution of the controller to obtain
    # its output

    u_array = np.empty((n, A.num_dims.u))
    s_array_ = np.empty((n, A.num_dims.s))

    idx = 0

#    print 's', s_array
#    print 'x', x_array

    for (ci, s, x) in zip(ci_array, s_array, x_array):

        # Execute controller

        controller_ret_val = controller_sim.compute(cifc.ToController(ci,
                s, x))

        # ##!!##logger.debug('s\':{}, u:{} = controller output(s:{}, x:{})'.format(controller_ret_val.state_array, controller_ret_val.output_array, s, x))

        s_array_[idx, :] = controller_ret_val.state_array
        u_array[idx, :] = controller_ret_val.output_array
        idx += 1

    return (s_array_, u_array)


    # t_array, x_array, d_array, p_array, u_array, pi_array,
