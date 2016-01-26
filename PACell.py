#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import numpy as np

from utils import print

# import matplotlib.pyplot as plt

import err
#TAG:Z3_IND
# Comment out below import
#import smtSolver as smt
import concretePlant as cp
import cellmanager as CM

logger = logging.getLogger(__name__)


# Abstraction is a grid parameterized by eps.
# It is defined by cells, each represented by
# \vec(x) = [l, h), where x = (x1, x3, ..., xn) and xi = [li, hi)

class PlantAbstraction:

    @staticmethod
    def get_abs_state(
            cell_id,
            #pi_cells_id,
            n,
            d,
            pvt,
            ):

        #return PlantAbstractState(cell_id, pi_cells_id, n, d, pvt)
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

        #pi_cells = self.ival_cons_to_cell_list(pi_cons, self.pi_eps)

    # ================== MANIPULATES FORMAT =============== of abs_state
    # Assumes abstract state is represented by a tuple t(x1, x2, x3, ... xn) of
    # ints
    # where X \in \R^n
    # The cell is then C: (t) <= c <= (t + eps)

    # TODO: tied to z3! should be using Solver class instead!

    def get_smt2_constraints(self, abs_state, x):
        ic = self.get_ival_cons_abs_state(abs_state)

        # cons.ic2smt returns a function which needs to be instantiated for a
        # z3 array

        smt_cons = self.solver.ic2smt(ic, x)
        return smt_cons

    def get_ival_cons_cell(self, cell, eps):
        return CM.ival_constraints(cell, eps)

    def get_ival_cons_abs_state(self, abs_state):
        return CM.ival_constraints(abs_state.cell_id, self.eps)


    def get_abs_state_set_from_ival_constraints(
            self,
            x_cons,
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
        cell_list = CM.get_cells_from_ival_constraints(x_cons, self.eps)
        abs_state_list = [PlantAbstraction.get_abs_state(cell, n, d, pvt) for cell in cell_list]

        return abs_state_list

    def get_abs_state_set_from_ival_constraints_old(
            self,
            x_cons,
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

        #pi_cells = self.ival_cons_to_cell_list(pi_cons, self.pi_eps)
        x_list = self.ival_cons_to_cell_list(x_cons, self.eps)
        #print(x_list)

        # zip them to iterate over all genereted elements

        abs_state_list = [PlantAbstraction.get_abs_state(
                get_abs_tuple(abs_state_array_repr),
                n, d, pvt) for abs_state_array_repr in zip(*x_list)]
#         abs_state_list = []
#         for abs_state_array_repr in zip(*x_list):
#             abs_state = \
#                 PlantAbstraction.get_abs_state(cell_id=get_abs_tuple(abs_state_array_repr), n=n, d=d, pvt=pvt)
#             abs_state_list.append(abs_state)

        # ##!!##logger.debug('get_abs_state_set_from_constraints()\ncons {} |-> abs_state_list {}'.format(cons, abs_state_list))

        return abs_state_list

#     def get_cell_id_from_concrete_pi(self, pi):
#         return self.cell_id_from_concrete(pi, self.pi_eps)

#     def get_cell_id_from_concrete_state(self, X):
#         return self.cell_id_from_concrete(X, self.eps)

    # ================== MANIPULATES FORMAT =============== of abs_state
    # Assumes abstract state is represented by a tuple t(x1, x2, x3, ... xn)
    # gets in concrete state as a pure continuous component and not the enitre
    # concrete state...maybe change later to entire concrete state for
    # uniformity?

    def cell_id_from_concrete(self, X, eps):
        # the cell is same as cell_id so...
        return CM.cell_from_concrete(X, eps)
        # And also, an abstract state is a tuple of integers!

    def get_abs_state_from_concrete_state(self, concrete_state):
        X = concrete_state.x
        t = concrete_state.t
        n = int(np.round(t / self.delta_t))
        d = concrete_state.d
        pvt = concrete_state.pvt
        #pi = concrete_state.pi

        cell_id = self.cell_id_from_concrete(X, self.eps)
        #pi_cell_id = self.cell_id_from_concrete(pi, self.pi_eps)

        abs_state = PlantAbstraction.get_abs_state(
                cell_id=cell_id,
                #pi_cells_id=[pi_cell_id],
                n=n,
                d=d,
                pvt=pvt)

        # ##!!##logger.debug('{} = get_abs_state_from_concrete_state({})'.format(abs_state, concrete_state))

        return abs_state

    def get_reachable_abs_states_sym(
            self,
            sampled_state,
            A,
            system_params,
            ):
        
        pi_ref = system_params.pi_ref
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

        abs2rchd_abs_state_ci_pi_list = []
        for rchd_concrete_state in rchd_concrete_state_array.iterable():

            rchd_abs_state = \
                self.get_abs_state_from_concrete_state(rchd_concrete_state)

            # A.get_abs_state_from_concrete_state(rchd_concrete_state)

            ci = rchd_concrete_state.ci
            pi = rchd_concrete_state.pi
            pi_cell = self.cell_id_from_concrete(pi, pi_ref.eps)

            # TODO: which state becomes none?? Verfiy

            if rchd_abs_state is not None:

                # abs2rchd_abs_state_set.add(rchd_abs_state)

                abs2rchd_abs_state_ci_pi_list.append((rchd_abs_state, ci, pi_cell))

                # # ##!!##logger.debug('abs_state obtained {} from concrete_state {}'.format(rchd_abs_state, rchd_concrete_state))
        # return abs2rchd_abs_state_set

        return abs2rchd_abs_state_ci_pi_list

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
        #print(rchd_concrete_state_array)
        #exit()

        # ================= DIRECT MANIPULATION ===================
        # of StateArray object
        # rchd_cont_state_array = rchd_concrete_state_array.cont_states

        # for each reached state, get the abstract state
        pi_ref = system_params.pi_ref
        ci_ref = system_params.ci_ref

        abs2rchd_abs_state_ci_pi_list = []
        for rchd_concrete_state in rchd_concrete_state_array.iterable():

            rchd_abs_state = \
                A.get_abs_state_from_concrete_state(rchd_concrete_state)
            ci = rchd_concrete_state.ci
            pi = rchd_concrete_state.pi
            pi_cell = self.cell_id_from_concrete(pi, pi_ref.eps)
            ci_cell = self.cell_id_from_concrete(ci, ci_ref.eps)

            if rchd_concrete_state.x in system_params.final_cons:
                if not system_params.is_final(A, rchd_abs_state):
                    print(rchd_concrete_state)
                    print(self.get_ival_cons_abs_state(rchd_abs_state.ps))
                    print(rchd_concrete_state.x)
                    print(system_params.final_cons)
                    raise err.Fatal('cant happen!')

            if rchd_abs_state is not None:
                abs2rchd_abs_state_ci_pi_list.append((rchd_abs_state, ci_cell, pi_cell))

                # ##!!##logger.debug('abs_state obtained {} from concrete_state {}'.format(rchd_abs_state, rchd_concrete_state))

        return abs2rchd_abs_state_ci_pi_list

    # Process the state only if the shortest simulation trace
    # TODO: <= or < ?

    def is_terminal(self, abs_state):

        # print(abs_state.n)

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
#             pi_cells_id,
            n,
            d,
            pvt,
            ):

        self.cell_id = cell_id
#         self.pi_cells_id = pi_cells_id
        self.n = n
        self.d = d
        self.pvt = pvt
        return

    def __eq__(self, x):

        # return hash((self.cell_id, self.n))
        # print('plant_eq_invoked')

        return hash(self) == hash(x)

    def __hash__(self):

        # return hash((self.cell_id, self.n))
        # print('plant_hash_invoked')

        # return hash((self.cell_id, self.n))

        return hash(self.cell_id)

    def __repr__(self):
        return 'cell={}, n={}, d={}'.format(self.cell_id, self.n, self.d)
