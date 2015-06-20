#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import numpy as np

import constraints as cons
import err
import concreteController as cc
import utils as U
import state as st
import sample as S

logger = logging.getLogger(__name__)


class ControllerCollectionAbstraction:

#    get_abs_state\
#        = collections.namedtuple('abs_state_control', ['s'], verbose=False)

    @staticmethod
    def get_abs_state(s):
        return ControllerCollectionsAbstractState(s)

    def __init__(self, num_dims):

        # super(Abstraction, self).__init__()

        self.num_dim = num_dims

    # \alpha()

    def get_abs_state_from_concrete_state(self, concrete_state):

        # return self.get_abs_state(s=tuple(concrete_state))

        return self.get_abs_state(s=concrete_state)

    # \gamma()

    def get_concrete_states_from_abs_state(self, a):

        # return [i for i in a]

        return a.s

    def get_ival_constraints(self, abs_state):
        ival_l = np.array(abs_state.s)
        ival_h = np.array(abs_state.s)
        return cons.IntervalCons(ival_l, ival_h)

    def get_reachable_abs_states(
        self,
        abs_state,
        A,
        system_params,
        ):
        ci_ival_cons = system_params.ci
        pi_ival_cons = system_params.pi
        samples = system_params.sampler.sample(abs_state, A, system_params,
                A.num_samples)

        total_num_samples = samples.n

        # ##!!##logger.debug('num_samples = {}'.format(total_num_samples))
        # ##!!##logger.debug('samples = \n{}'.format(samples))
        # ##!!##logger.debug(U.decorate('sampling done'))

        x_array = samples.x_array
        s_array = samples.s_array

        # print s_array

        t_array = samples.t_array
        pi_array = samples.pi_array
        if ci_ival_cons is None:
            ci_array = np.zeros((total_num_samples, 1))
        else:
            ci_array = samples.ci_array

            # ci_array = S.sample_ival_constraints(ci_ival_cons, total_num_samples)

        # TODO: knows that d is an np array

        d = np.array([abs_state.plant_state.d])
        pvt = np.array([abs_state.plant_state.pvt])

        d_array = np.repeat(d, samples.n, axis=0)
        pvt_array = np.repeat(pvt, samples.n, axis=0)

        total_num_samples = samples.n

        # sanity check

        if len(d_array) == total_num_samples and len(pvt_array) \
            == total_num_samples and len(x_array) == total_num_samples \
            and len(s_array) == total_num_samples and len(t_array) \
            == total_num_samples:
            pass
        else:
            raise err.Fatal('sanity_check fails')

        # print x_array, s_array

        (s_array_, u_array) = cc.compute_concrete_controller_output(
            A,
            system_params.controller_sim,
            ci_array,
            x_array,
            s_array,
            total_num_samples,
            )

        # print s_array_, u_array
        # print samples.ci_array

        state = st.StateArray(
            t=t_array,
            x=x_array,
            d=d_array,
            pvt=p_array,
            s=s_array_,
            u=u_array,
            pi=pi_array,
            ci=ci_array,
            )

        return state


class ControllerCollectionsAbstractState(object):

    def __init__(self, s):
        self.s = s
        return

    def __eq__(self, x):

        # print 'controller_eq_invoked'

        return hash(self) == hash(x)

    def __hash__(self):

        # print 'controller_hash_invoked'

        return hash(tuple(self.s))

    def __repr__(self):
        return str(self.s)


