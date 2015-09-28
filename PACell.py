#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import numpy as np

# import matplotlib.pyplot as plt

import err
import constraints as cons
#TAG:Z3_IND
# Comment out below import
#import smtSolver as smt
import concretePlant as cp

logger = logging.getLogger(__name__)


# Abstraction is a grid parameterized by eps.
# It is defined by cells, each represented by
# \vec(x) = [l, h), where x = (x1, x3, ..., xn) and xi = [li, hi)

class PlantAbstraction:

    @staticmethod
    def get_abs_state(
            cell_id,
            n,
            d,
            pvt,
            ):

        return PlantAbstractState(cell_id, n, d, pvt)

    def __init__(
            self,
            T,
            N,
            num_dims,
            delta_t,
            eps,
            refinement_factor,
            num_samples,
            smt_solver, #TAG:Z3_IND - Add solver param
            ):

            # init_cons_list, final_cons, controller_sim, num_dims, delta_t, prog_bar=False):
        # super(Abstraction, self).__init__()

        self.num_dims = num_dims

        # self.G = g.Graph()

        self.T = T
        self.N = N
        self.scale = None
        self.eps = eps
        self.delta_t = delta_t
        self.refinement_factor = refinement_factor
        self.num_samples = num_samples
        # TAG:Z3_IND - get the solver from the passed in args
        #self.solver = smt.smt_solver_factory('z3')
        self.solver = smt_solver

        # ##!!##logger.debug('==========abstraction parameters==========')
        # ##!!##logger.debug('eps: {}, refinement_factor: {}, num_samples: {},delta_t: {}'.format(str(self.eps), self.refinement_factor, self.num_samples, self.delta_t))

    # ================== MANIPULATES FORMAT =============== of abs_state
    # Assumes abstract state is represented by a tuple t(x1, x2, x3, ... xn) of
    # ints
    # where X \in \R^n
    # The cell is then C: (t) <= c <= (t + eps)

    # TODO: tied to z3! should be using Solver class instead!

    def get_smt2_constraints(self, abs_state, x):
        ic = self.get_ival_constraints(abs_state)

        # cons.ic2smt returns a function which needs to be instantiated for a
        # z3 array

        smt_cons = self.solver.ic2smt(ic, x)
        return smt_cons

    def get_ival_constraints(self, abs_state):
        cell_coordinates = np.array(abs_state.cell_id) * self.eps
        ival_l = cell_coordinates
        ival_h = cell_coordinates + self.eps
        return cons.IntervalCons(ival_l, ival_h)

    # TODO: change cons to cons_object which has cons in addition to all states
    # a concrete state has

    def get_abs_state_set_from_ival_constraints(
            self,
            cons,
            n,
            d,
            pvt,
            ):

        # ================== MANIPULATES FORMAT =============== of abs_state
        # Assumes abs_state_format as tuple
        # takes in a tuple with each element as numpy array and converts them to a
        # tuple with ints
        # This is done because numpy arrays are not hashable and can not be stored
        # in a set
        # Best advise to sort it out is to use objects for abstract states instead
        # of rudimentary tuples!

        def get_abs_tuple(abs_state_array):
            return tuple(map(int, abs_state_array))

            # return tuple(map(int, abs_state_array))

        abs_state_list = []

        Al = self.get_cell_id_from_concrete_state(cons.l)
        Ah = self.get_cell_id_from_concrete_state(cons.h)

        x_range_list = []
        for i in range(self.num_dims.x):

            # x_range_list.append(np.arange(cons.l[i], cons.h[i], eps[i]))

            x_range = range(Al[i], Ah[i], 1)

            # make the range inclusive of the last element,  because we want things to be sound

            x_range.append(Ah[i])
            x_range_list.append(x_range)

        # construct a grid

        # sometimes fails with memory errors
        try:
            grid = np.meshgrid(*x_range_list)
        except MemoryError as e:
            print 'meshgrid with the below x_cons failed'
            print cons
            raise e

        # create iterators which iterate over each element of the dim. array

        x_iter_list = []
        for i in range(self.num_dims.x):
            x_iter_list.append(np.nditer(grid[i]))

        # zip them to iterate over all genereted elements

        abs_state_list = []
        for abs_state_array_repr in zip(*x_iter_list):
            abs_state = \
                PlantAbstraction.get_abs_state(cell_id=get_abs_tuple(abs_state_array_repr), n=n, d=d, pvt=pvt)
            abs_state_list.append(abs_state)

        # ##!!##logger.debug('get_abs_state_set_from_constraints()\ncons {} |-> abs_state_list {}'.format(cons, abs_state_list))

        return abs_state_list

    # ================== MANIPULATES FORMAT =============== of abs_state
    # Assumes abstract state is represented by a tuple t(x1, x2, x3, ... xn)
    # gets in concrete state as a pure continuous component and not the enitre
    # concrete state...maybe change later to entire concrete state for
    # uniformity?

    def get_cell_id_from_concrete_state(self, X):
        if any(np.isinf(c) for c in X):
            return None
        eps = self.eps
        cell = np.floor(X / eps)

        # get the cell into integers...easier to do operations!
        # And also, an abstract state is a tuple of integers!

        cell_id = map(int, cell)
        return cell_id

    def get_abs_state_from_concrete_state(self, concrete_state):
        X = concrete_state.x
        t = concrete_state.t
        n = int(np.round(t / self.delta_t))
        d = concrete_state.d
        pvt = concrete_state.pvt

        cell_id = self.get_cell_id_from_concrete_state(X)

        abs_state = PlantAbstraction.get_abs_state(cell_id=tuple(cell_id), n=n, d=d, pvt=pvt)

        # ##!!##logger.debug('{} = get_abs_state_from_concrete_state({})'.format(abs_state, concrete_state))

        return abs_state

    def get_reachable_abs_states_sym(
            self,
            sampled_state,
            A,
            system_params,
            ):

        state = sampled_state
        total_num_samples = state.n

        property_checker = lambda t, Y: Y in system_params.final_cons
        rchd_concrete_state_array = cp.compute_concrete_plant_output(
                A,
                system_params.plant_sim,
                state,
                total_num_samples,
                property_checker)

        # ================= DIRECT MANIPULATION ===================
        # of StateArray object
        # rchd_cont_state_array = rchd_concrete_state_array.cont_states

        # for each reached state, get the abstract state

        # abs2rchd_abs_state_set = set()

        abs2rchd_abs_state_ci_list = []
        for rchd_concrete_state in rchd_concrete_state_array.iterable():

            rchd_abs_state = \
                self.get_abs_state_from_concrete_state(rchd_concrete_state)

            # A.get_abs_state_from_concrete_state(rchd_concrete_state)

            ci = rchd_concrete_state.ci

            # TODO: which state becomes none?? Verfiy

            if rchd_abs_state is not None:

                # abs2rchd_abs_state_set.add(rchd_abs_state)

                abs2rchd_abs_state_ci_list.append((rchd_abs_state, ci))

                # # ##!!##logger.debug('abs_state obtained {} from concrete_state {}'.format(rchd_abs_state, rchd_concrete_state))
        # return abs2rchd_abs_state_set

        return abs2rchd_abs_state_ci_list

    # Process the state only if the shortest simulation trace
    # TODO: <= or < ?

    def get_reachable_abs_states(
            self,
            intermediate_state,
            A,
            system_params,
            ):

        state = intermediate_state
        total_num_samples = state.n

        property_checker = lambda t, Y: Y in system_params.final_cons
        rchd_concrete_state_array = cp.compute_concrete_plant_output(
                A,
                system_params.plant_sim,
                state,
                total_num_samples,
                property_checker)

        # ================= DIRECT MANIPULATION ===================
        # of StateArray object
        # rchd_cont_state_array = rchd_concrete_state_array.cont_states

        # for each reached state, get the abstract state

        abs2rchd_abs_state_ci_list = []
        for rchd_concrete_state in rchd_concrete_state_array.iterable():

            rchd_abs_state = \
                A.get_abs_state_from_concrete_state(rchd_concrete_state)
            ci = rchd_concrete_state.ci

            if rchd_concrete_state.x in system_params.final_cons:
                if not system_params.is_final(rchd_abs_state):
                    print 'cant happen!'
                    exit()

            if rchd_abs_state is not None:

                abs2rchd_abs_state_ci_list.append((rchd_abs_state, ci))

                # ##!!##logger.debug('abs_state obtained {} from concrete_state {}'.format(rchd_abs_state, rchd_concrete_state))

        return abs2rchd_abs_state_ci_list

    # Process the state only if the shortest simulation trace
    # TODO: <= or < ?

    def is_terminal(self, abs_state):

        # print abs_state.n

        return abs_state.n >= self.N

    def draw(self, fig):
        raise err.Fatal('unimplemented')

    def draw_2d(self):
        raise err.Fatal('unimplemented')


# Abs state is an object  (cell_id, n, d, p)

class PlantAbstractState(object):

    def __init__(
            self,
            cell_id,
            n,
            d,
            pvt,
            ):

        self.cell_id = cell_id
        self.n = n
        self.d = d
        self.pvt = pvt
        return

    def __eq__(self, x):

        # return hash((self.cell_id, self.n))
        # print 'plant_eq_invoked'

        return hash(self) == hash(x)

    def __hash__(self):

        # return hash((self.cell_id, self.n))
        # print 'plant_hash_invoked'

        # return hash((self.cell_id, self.n))

        return hash(self.cell_id)

    def __repr__(self):
        return 'cell={}, n={}, d={}'.format(self.cell_id, self.n, self.d)


class GridEps(object):
    def __init__(self, eps):
        self.eps = eps

    def __add__(self, x):
        return

    def __sub__(self, x):
        return

    def __mult__(self, x):
        return

    def __div__(self, x):
        return
