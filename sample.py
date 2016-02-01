#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
sample.py
----------
Provides different sampling functions.
'''

import err

import numpy as np
import logging
import state

logger = logging.getLogger(__name__)


# TODO!

def sampler_factory():
    return


def sample_init_UR(sys, prop, num_samples):
    num_segments = int(np.ceil(prop.T / sys.delta_t))
    init_cons = prop.init_cons
    init_controller_state = prop.initial_controller_state
    # eliminate by removing u and removing dummu pvt...use real pvt
    num_dims = sys.num_dims
    dummy_pvt = np.zeros((num_samples, num_dims.pvt))
    dummy_u = np.zeros((num_samples, num_dims.u))
    ci_lb = prop.ci.l
    ci_ub = prop.ci.h

    s_array = np.tile(np.array([init_controller_state]), (num_samples, 1))

    x_array = sample_ival_constraints(init_cons, num_samples)
    ci_array = ci_lb + (ci_ub - ci_lb) * np.random.random((num_samples, num_segments, num_dims.ci))
    pi_array = np.zeros((num_samples, num_dims.pi))

    p_array = dummy_pvt
    d_array = np.tile(np.array(prop.initial_discrete_state), (num_samples, 1))
    u_array = dummy_u
    t_array = np.zeros((num_samples, 1))

    init_conrete_states = state.StateArray(t=t_array, x=x_array, d=d_array, pvt=p_array, s=s_array, u=u_array, pi=pi_array, ci=ci_array)
    return init_conrete_states


def sample_ival_constraints(ival_cons, n):

    # ##!!##logger.debug('sampling cons: {}'.format(ival_cons))

    # print '='*40,'sampler','='*40
    # print ival_cons

    random_arr = np.random.rand(n, ival_cons.dim)
    x_array = ival_cons.l + random_arr * (ival_cons.h - ival_cons.l)

    # print x_array
    # TODO: assumes state_arry size to be 1
    # print '='*40,'samplerEND','='*40

    return x_array


class Sampler(object):

    def __init__(self, num_dims):
        self.num_dims = num_dims
        self.sampling_scheme = None

    def sample(
        self,
        abstract_state,
        A,
        system_params,
        num_samples,
        ):

        pass

    def sample_new(self, abs_state, num_samples):
        raise NotImplementedError


# gets ival_cons: interval constraints
# n: number of samples to be generated
# TODO: control state samples are 0!!
# Change to concrete states found in A.contoller_abs?

class IntervalSampler(Sampler):

    def __init__(self):
        super(IntervalSampler, self).__init__(None)

    # def sample(self, ival_cons, ignore, n):

    def sample(
        self,
        abstract_state,
        A,
        system_params,
        num_samples,
        ):

        n = num_samples
        plant_state_ival_cons = \
            A.plant_abs.get_ival_constraints(abstract_state.plant_state)
        random_arr = np.random.rand(n, A.num_dims.x)
        x_array = plant_state_ival_cons.l + random_arr \
            * (plant_state_ival_cons.h - plant_state_ival_cons.l)
        t_array = np.tile(abstract_state.plant_state.n * A.delta_t, (n, 1))

        if A.num_dims.ci != 0:
            random_arr = np.random.rand(n, A.num_dims.ci)  # np.zeros((n, A.num_dims.ci))
            ci_array = system_params.ci.l + random_arr * (system_params.ci.h - system_params.ci.l)
        else:
            ci_array = np.empty((n, A.num_dims.ci))

        # ci_array = np.zeros((n, A.num_dims.ci))

        pi_array = np.zeros((n, A.num_dims.pi))

        s = \
            A.controller_abs.get_concrete_states_from_abs_state(abstract_state.controller_state)
        s_array = np.tile(s, (n, 1))

        return Samples(s_array=s_array, x_array=x_array, ci_array=ci_array,
                       pi_array=pi_array, t_array=t_array)


class IntervalConcolic(Sampler):

    def __init__(self, concolic_engine):

        super(IntervalConcolic, self).__init__(None)
        self.CE = concolic_engine
        self.interval_sampler = IntervalSampler().sample

    # TODO: remove dependence on A and remove it as a parameter and either
    # - make abstract states objects instead of tuples
    # - or make abstract states contain references to their manipulating
    # functions

    def get_samples_from_test_cases(
        self,
        abstract_state,
        A,
        system_params,
        ):

        plant_state_ival_cons = \
            A.plant_abs.get_ival_constraints(abstract_state.plant_state)

        # ##!!##logger.debug('sampling cons: {}'.format(plant_state_ival_cons))

        controller_state_ival_cons = \
            A.controller_abs.get_ival_constraints(abstract_state.controller_state)
        ci_ival_cons = system_params.ci

        test_cases = self.CE.get_test_cases(plant_state_ival_cons,
                controller_state_ival_cons, ci_ival_cons)
        t_array = np.tile(abstract_state.plant_state.n * A.delta_t,
                          (test_cases.n, 1))

        # TODO: get this from reg sampler

        test_cases.pi_array = np.zeros((test_cases.n, A.num_dims.pi))

        # convert test cases to samples

        samples = Samples(s_array=test_cases.s_array,
                          x_array=test_cases.x_array,
                          ci_array=test_cases.ci_array,
                          pi_array=test_cases.pi_array, t_array=t_array)

        return samples

    def sample(
        self,
        abstract_state,
        A,
        system_params,
        num_samples,
        ):

        concolic_samples = self.get_samples_from_test_cases(abstract_state, A,
                system_params)

        uniform_random_samples = self.interval_sampler(abstract_state, A,
                system_params, num_samples)

        # print concolic_samples
        # print uniform_random_samples
        # print '='*20

        uniform_random_samples.append(concolic_samples)

        # print uniform_random_samples

        return uniform_random_samples


# Selects plant states based solely on the controller's path coverage.
# Not recommended!

class Concolic(Sampler):

    def __init__(self, concolic_engine):

        super(Concolic, self).__init__(None)
        self.CE = concolic_engine

    # TODO: remove dependence on A and remove it as a parameter and either
    # - make abstract states objects instead of tuples
    # - or make abstract states contain references to their manipulating
    # functions

    def sample(
        self,
        abstract_state,
        A,
        system_params,
        ignore,
        ):

        plant_state_ival_cons = \
            A.plant_abs.get_ival_constraints(abstract_state.plant_state)

        # ##!!##logger.debug('sampling cons: {}'.format(plant_state_ival_cons))

        controller_state_ival_cons = \
            A.controller_abs.get_ival_constraints(abstract_state.controller_state)
        ci_ival_cons = system_params.ci

        test_cases = self.CE.get_test_cases(plant_state_ival_cons,
                controller_state_ival_cons, ci_ival_cons)
        t_array = np.tile(abstract_state.plant_state.n * A.delta_t,
                          (test_cases.n, 1))

        # TODO: get this from reg sampler

        test_cases.pi_array = np.zeros((test_cases.n, A.num_dims.pi))

        # convert test cases to samples

        samples = Samples(s_array=test_cases.s_array,
                          x_array=test_cases.x_array,
                          ci_array=test_cases.ci_array,
                          pi_array=test_cases.pi_array, t_array=t_array)
        return samples

    def sampleOLD(
        self,
        ival_cons,
        controller_states,
        ignore,
        ):

        ival_cons = 0
        controller_states = 0
        consolidated_samples = Samples()

        # TODO: remove this loop by making a unique abstract state for each
        # combination of (x,s,d,pvt,etc) instead of unique x

        for s in controller_states:
            test_cases = self.CE.get_test_cases(s, ival_cons)
            test_cases.d_array = d_array
            sample = test_case2sample(test_cases)
            consolidated_samples.append(sample)
        print consolidated_samples
        return consolidated_samples


# Like concolic, but treats the controller state as symbolic, unlike Concolic(); which uses concrete
# values for controller states

class Symbolic(Sampler):

    def __init__(self, symbolic_engine):
        super(Symbolic, self).__init__(None)
        self.SE = symbolic_engine

    def sample(
        self,
        abstract_state,
        A,
        system_params,
        num_samples,
        ):

        plant_state_cons = \
            A.plant_abs_get_ival_constraints(abstract_state.plant_state)
        controller_state_cons = A.controller_abs.get_symbolic_constraints


# Converts test case(s) into sample(s)

def test_case2sample(test_case):
    return Samples(s_array=test_case.s_array, x_array=test_case.x_array,
                   ci_array=test_case.ci_array, d_array=test_case.d_array)


# TODO: rename this to concrete state!

class Samples(object):

    def __init__(
        self,
        s_array=None,
        x_array=None,
        ci_array=None,
        pi_array=None,
        t_array=None,
        ):

        # s: controller states

        self.s_array = s_array

        # x: plant states

        self.x_array = x_array

        # ci: controller disturbances/extraneous inputs

        self.ci_array = ci_array

        # pi: plant disturbances/extraneous inputs

        self.pi_array = pi_array

        # t_array

        self.t_array = t_array

        logger.warn('sanity_check() off!!')

        # self.sanity_check()

    def sanity_check():
        raise NotImplementedError

    @property
    def n(self):

        # return self.s_array.shape[0]

        return self.x_array.shape[0]

    def append(self, sample):
        if self.t_array is None:
            self.t_array = sample.t_array
        else:
            self.t_array = np.concatenate((self.t_array, sample.t_array))

        if self.s_array is None:
            self.s_array = sample.s_array
        else:
            self.s_array = np.concatenate((self.s_array, sample.s_array))

        if self.x_array is None:
            self.x_array = sample.x_array
        else:
            self.x_array = np.concatenate((self.x_array, sample.x_array))

        if self.ci_array is None:
            self.ci_array = sample.ci_array
        else:
            self.ci_array = np.concatenate((self.ci_array, sample.ci_array))

        if self.pi_array is None:
            self.pi_array = sample.pi_array
        else:
            self.pi_array = np.concatenate((self.pi_array, sample.pi_array))

    def __repr__(self):
        return '''samples
s_array={}
x_array={}
ci_array={}
pi_array={}
t_array={}'''.format(self.s_array,
                self.x_array, self.ci_array, self.pi_array, self.t_array)


