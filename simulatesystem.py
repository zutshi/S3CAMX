#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import controlifc as cifc
import state as st
import traces
import err
#import progBar as pb
#import utils

import logging
import numpy as np

# import matplotlib.pyplot as plt


# from guppy import hpy

# hp=hpy()

logger = logging.getLogger(__name__)


# Helper function for simulating a system from 0 to T
# TODO: Does not handle error states of the controller or the plant simulator..
# Must include provision for states which can not be simulated for some
# reasons...
def simulate(system_sim, concrete_state, T):
    (t, x, s, d, pvt, u, ci_array, pi) = get_individual_states(concrete_state)
    t0 = t
    tf = t + T
    trace = system_sim(x, s, d, pvt, t0, tf, ci_array)
    return trace


# arguements must be numpy arrays
# Uses the dimension info to correctly create the state array
def get_concrete_state_obj(t0, x0, d0, pvt0, s0, ci, u):
    if x0.ndim == 1:
        concrete_states = st.StateArray(
            t=np.array([t0]),
            x=np.array([x0]),
            d=np.array([d0]),
            pvt=np.array([pvt0]),
            u=np.array([u]),
            s=np.array([s0]),
            pi=0,
            ci=np.array([ci]),
            )
    elif x0.ndim == 2:

        concrete_states = st.StateArray(
            t=t0,
            x=x0,
            d=d0,
            pvt=pvt0,
            u=u,
            s=s0,
            pi=0,
            ci=ci,
            )
    else:
        raise err.Fatal('dimension must be 1 or 2...: {}!'.format(x0.ndim))
    return concrete_states


def get_individual_states(concrete_states):
    t = concrete_states.t
    x = concrete_states.cont_states
    s = concrete_states.controller_states
    d = concrete_states.discrete_states
    pvt = concrete_states.pvt_states
    u = concrete_states.controller_outputs
    ci = concrete_states.controller_extraneous_inputs
    pi = concrete_states.plant_extraneous_inputs

    return (t, x, s, d, pvt, u, ci, pi)


def get_system_simulator(sys):
    step_sim = get_step_simulator(sys.controller_sim,
                                  sys.plant_sim,
                                  sys.delta_t)

    def system_simulator(
            x, s,
            d, pvt,
            t0, tf,
            ci_array
            ):

        T = tf - t0
        num_segments = int(np.ceil(T / sys.delta_t))
        # num_points = num_segments + 1
        trace = traces.Trace(sys.num_dims, num_segments + 1)
        t = t0

        for i in xrange(num_segments):
            ci = ci_array[i]
            (t_, x_, s_, d_, pvt_, u_) = step_sim(t, x, s, d, pvt, ci)
            trace.append(t=t, x=x, s=s, d=d, u=u_, ci=ci)
            (t, x, s, d, pvt) = (t_, x_, s_, d_, pvt_)

        trace.append(t=t, x=x, s=s, d=d, u=u_, ci=ci)
        return trace
    return system_simulator


def get_step_simulator(csim, psim, delta_t):

    def simulate_basic(t0, x0, s0, d0, pvt0, ci):

        controller_ret_val = csim.compute(cifc.ToController(ci, s0, x0))
        s_, u = controller_ret_val.state_array, controller_ret_val.output_array

        concrete_states = get_concrete_state_obj(t0, x0, d0, pvt0, s_, ci, u)

        concrete_states_ = psim.simulate(concrete_states, delta_t)

        (t, x, s, d, pvt, u, _, _) = get_individual_states(concrete_states_)
        return (t[0], x[0], s[0], d[0], pvt[0], u[0])
    return simulate_basic


def simulate_basic(csim, psim, x0, s0, t0, tf, ci, d0, pvt0):

    controller_ret_val = csim(cifc.ToController(ci, s0, x0))
    s_, u = controller_ret_val.state_array, controller_ret_val.output_array

    concrete_states = get_concrete_state_obj(t0, x0, d0, pvt0, s_, ci, u)

    concrete_states_ = psim(concrete_states, tf)

    return concrete_states_
