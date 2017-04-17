#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

# S: Controller States
# X: Plant states
# U: controller outputs

# import time

import logging
import numpy as np

# import matplotlib
# matplotlib.use('GTK3Agg')
# import matplotlib.pyplot as plt

import utils as U
from utils import print
import err
import graph as g

logger = logging.getLogger(__name__)


# def abstraction_factory(des, plant_sim, T, sampler, init_cons, final_cons):
#    return GridBasedAbstraction(des, plant_sim, T, sampler, init_cons, final_cons)
    # return GridBasedAbstraction(*args, **kwargs)

def abstraction_factory(*args, **kwargs):
    return TopLevelAbs(*args, **kwargs)


# mantains a graph representing the abstract relation
# Each state is a tuple (abstract_plant_state, abstract_controller_state)
# Each relation is A1 -> A2, and is annotated by the concrete states
# abstraction states are a tuple (plant_state, controller_state)

class TopLevelAbs:

    # get_abs_state = collections.namedtuple('tpl_abs_state', ['plant_state', 'controller_state'], verbose=False)

    @staticmethod
    def get_abs_state(plant_state, controller_state):
        return AbstractState(plant_state, controller_state)

    # takes in the plant and the controller abstraction objects which are
    # instatiation of their respective parameterized abstract classes

    #TODO: split this ugly init function into smaller ones
    def __init__(
        self,
        config_dict,
        T,
        num_dims,
        controller_sym_path_obj,
        min_smt_sample_dist,
        plant_abstraction_type,
        controller_abstraction_type,
        plant_abs=None,
        controller_abs=None,
        prog_bar=False,
        ):

        # super(Abstraction, self).__init__()

        self.num_dims = num_dims
        self.G = g.graph_factory('nx')
        self.T = T
        self.N = None
        self.state = None
        self.scale = None
        self.controller_sym_path_obj = controller_sym_path_obj
        self.min_smt_sample_dist = min_smt_sample_dist
        self.plant_abstraction_type = plant_abstraction_type
        self.controller_abstraction_type = controller_abstraction_type

        # The list of init_cons is interpreted as [ic0 \/ ic1 \/ ... \/ icn]
#        self.init_cons_list = init_cons_list
#        self.final_cons_list = final_cons_list

        self.eps = None

#        self.refinement_factor = 0.5

        self.delta_t = None
        self.num_samples = None

        # TODO: replace this type checking by passing dictionaries and parsing
        # outside the class. This will also avoid parsing code duplication.
        # Keep a single configuration format.

        self.parse_config(config_dict)

        # TAG:Z3_IND - default init
        smt_solver = None

        # TAG:Z3_IND - shuffled the plant abstraction creation after controller
        # abstraction. This lets us get the smt_solver depending upon the
        # requeseted controller abstraction

        if controller_abstraction_type == 'symbolic_pathcrawler':
            import smtSolver as smt
            smt_solver = smt.smt_solver_factory('z3')
            import CASymbolicPCrawler as CA
            controller_abs = CA.ControllerSymbolicAbstraction(self.num_dims,
                    controller_sym_path_obj, min_smt_sample_dist, smt_solver)
        elif controller_abstraction_type == 'symbolic_klee':
            import CASymbolicKLEE as CA
            controller_abs = CA.ControllerSymbolicAbstraction(self.num_dims,
                    controller_sym_path_obj, min_smt_sample_dist)
        #elif controller_abstraction_type == 'concolic':
        #    import CAConcolic as CA
        #    controller_abs = CA.ControllerCollectionAbstraction(self.num_dims)
        elif controller_abstraction_type == 'concrete':
            import CAConcolic as CA
            controller_abs = CA.ControllerCollectionAbstraction(self.num_dims)
        else:
            print(controller_abstraction_type)
            raise NotImplementedError

        if plant_abstraction_type == 'cell':
            #from PACell import *
            import PACell as PA
        else:
            raise NotImplementedError
        # Overriding the passed in plant and conctroller abstractions
        plant_abs = PA.PlantAbstraction(
            self.T,
            self.N,
            self.num_dims,
            self.delta_t,
            self.eps,
            self.refinement_factor,
            self.num_samples,
            smt_solver, #TAG:Z3_IND - Add solver param
            )


        print(U.decorate('new abstraction created'))
        print('eps:', self.eps)
        print('num_samples:', self.num_samples)
        print('refine:', self.refinement_factor)
        print('deltaT:', self.delta_t)
        print('TH:', self.T)
        print('num traces:', self.N)
        print('=' * 50)

        # ##!!##logger.debug('==========abstraction parameters==========')
        # ##!!##logger.debug('eps: {}, refinement_factor: {}, num_samples: {},delta_t: {}'.format(str(self.eps), self.refinement_factor, self.num_samples, self.delta_t))

        initial_state_list = []

        # WHy was this needed in the first place?
#        for node in self.initial_state_set:
#            self.G.add_node(node)
#        for node in self.final_state_set:
#            self.G.add_node(node)

        # Not very useful when the graph is discovered incrementally from the
        # intial states!

        self.final_augmented_state_set = set()

        # self.sanity_check()

        self.plant_abs = plant_abs
        self.controller_abs = controller_abs

        #if self.controller_abstraction_type.startswith('symbolic'):
        if self.controller_abs.is_symbolic:
            self.get_reachable_states = self.get_reachable_states_sym
        else:
            self.get_reachable_states = self.get_reachable_states_conc
        return

    def parse_config(self, config_dict):

        # ##!!##logger.debug('parsing abstraction parameters')

        if config_dict['type'] == 'string':
            try:
                grid_eps_str = config_dict['grid_eps']
                # remove braces
                grid_eps_str = grid_eps_str[1:-1]
                self.eps = np.array([float(eps) for eps in grid_eps_str.split(',')])

                pi_grid_eps_str = config_dict['pi_grid_eps']
                # remove braces
                pi_grid_eps_str = pi_grid_eps_str[1:-1]
                #self.pi_eps = np.array([float(pi_eps) for pi_eps in pi_grid_eps_str.split(',')])

                self.refinement_factor = float(config_dict['refinement_factor'])
                self.num_samples = int(config_dict['num_samples'])
                self.delta_t = float(config_dict['delta_t'])
                self.N = int(np.ceil(self.T / self.delta_t))

                # Make the accessed data as None, so presence of spurious data can be detected in a
                # sanity check

                config_dict['grid_eps'] = None
                config_dict['pi_grid_eps'] = None
                config_dict['refinement_factor'] = None
                config_dict['num_samples'] = None
                config_dict['delta_t'] = None
            except KeyError, key:
                raise err.Fatal('expected abstraction parameter undefined: {}'.format(key))
        else:
            for attr in config_dict:
                setattr(self, attr, config_dict[attr])
            self.N = int(np.ceil(self.T / self.delta_t))
            self.refinement_factor = 2.0

        return

    # TODO: remove this eventually...

    def is_terminal(self, abs_state):
        return self.plant_abs.is_terminal(abs_state.plant_state)

    # Add the relation(abs_state_src, rchd_abs_state)
    # and update the abstraction function

    def add_relation(
            self,
            abs_state_src,
            rchd_abs_state,
            ci,
            pi
            ):

        # get new distance/position from the initial state
        # THINK:
        # n can be calculated in two ways
        #   - only in the abstraction world: [current implementation]
        #       Completely independant of the simulated times
        #       i.e. if A1->A2, then A2.n = A1.n + 1
        #   - get it from simulation trace:
        #       n = int(np.floor(t/self.delta_t))

        self.G.add_edge(abs_state_src, rchd_abs_state, ci, pi)
        return

    # TODO: does not have access to step plant and step controller!

    def get_reachable_states_sym(self, abs_state, system_params):
        abs2rchd_abs_state_set = set()
        reachable_state_list = \
            self.controller_abs.get_reachable_abs_states(abs_state, self, system_params)
        for (cs, c) in reachable_state_list:
            print(cs)
            U.pause()

            # reachable_plant_state_set = self.plant_abs.get_reachable_abs_states_sym(c, self, system_params)

            reachable_plant_state_ci_pi_list = self.plant_abs.get_reachable_abs_states_sym(
                c,
                self,
                system_params)
            for (ps, ci, pi_cell) in reachable_plant_state_ci_pi_list:
                reachable_abs_state = AbstractState(ps, cs)
                abs2rchd_abs_state_set.add(reachable_abs_state)

                # why making a tuple?
                # edge_attr = (ci,)

                self.add_relation(abs_state, reachable_abs_state, ci, pi_cell)
        return abs2rchd_abs_state_set

    def get_reachable_states_conc(self, abs_state, system_params):
        abs2rchd_abs_state_set = set()

        # TODO: RECTIFY the below GIANT MESS
        # Sending in self and the total abstract_state to plant and controller
        # abstraction!!

        intermediate_state = \
            self.controller_abs.get_reachable_abs_states(abs_state, self, system_params)
        abs2rchd_abs_state_ci_pi_list = \
            self.plant_abs.get_reachable_abs_states(intermediate_state, self, system_params)

        for (rchd_abs_state, ci_cell, pi_cell) in abs2rchd_abs_state_ci_pi_list:

            # print(ci)

            self.add_relation(abs_state, rchd_abs_state, ci_cell, pi_cell)
            abs2rchd_abs_state_set.add(rchd_abs_state)
        return abs2rchd_abs_state_set

#     def states_along_paths(self, paths):
#         MAX_ERROR_PATHS = 2
#         bounded_paths = U.bounded_iter(paths, MAX_ERROR_PATHS)

#         ret_list = []
#         for path in bounded_paths:
#             ret_list.append(path)
#         return ret_list

    def compute_error_paths(self, initial_state_set, final_state_set, MAX_ERROR_PATHS):
        # length of path is num nodes, whereas N = num segments
        max_len = self.N + 1
        return self.G.get_path_generator(initial_state_set, final_state_set, max_len, MAX_ERROR_PATHS)

    # memoized because the same function is called twice for ci and pi
    # FIXME: Need to fix it
    #@U.memodict
    def get_seq_of_ci_pi(self, path):
        attr_map = self.G.get_path_attr_list(path, ['ci', 'pi'])
        #print('attr_map:', attr_map)
        return attr_map['ci'], attr_map['pi']

    def get_initial_states_from_error_paths(self, initial_state_set,
                                            final_state_set, pi_ref,
                                            ci_ref, pi_cons, ci_cons):
        '''
        @type pi_cons: constraints.IntervalCons
        @type ci_cons: constraints.IntervalCons
        '''

        MAX_ERROR_PATHS = 100
        ci_dim = self.num_dims.ci
        pi_dim = self.num_dims.pi
#         init_set = set()
        init_list = []
        ci_seq_list = []
        pi_seq_list = []

        error_paths = self.compute_error_paths(initial_state_set, final_state_set, MAX_ERROR_PATHS)
        #bounded_error_paths = U.bounded_iter(error_paths, MAX_ERROR_PATHS)
        bounded_error_paths = error_paths

        def get_ci_seq(path):
            return self.get_seq_of_ci_pi(path)[0]

        def get_pi_seq(path):
            return self.get_seq_of_ci_pi(path)[1]

        def get_empty(_):
            return []

        get_ci = get_ci_seq if ci_dim != 0 else get_empty
        get_pi = get_pi_seq if pi_dim != 0 else get_empty

#         if ci_dim == 0:
#             for path in bounded_error_paths:
#                 ci_seq = []
#                 ci_seq_list.append(ci_seq)
#                 init_set.add(path[0])

#             return (list(init_set), ci_seq_list)
#         else:
        max_len = -np.inf
        min_len = np.inf
        unique_paths = set()
        for path in bounded_error_paths:
#             ci_seq = self.get_seq_of_ci(path)
            pi_seq_cells = get_pi(path)
            pi_ref.update_from_path(path, pi_seq_cells)
            # convert pi_cells to ival constraints
            #pi_seq = map(self.plant_abs.get_ival_cons_pi_cell, get_pi(path))
            pi_seq = [self.plant_abs.get_ival_cons_cell(pi_cell, pi_ref.eps) for pi_cell in pi_seq_cells]
            if ci_ref is not None:
                ci_seq_cells = get_ci(path)
                ci_ref.update_from_path(path, ci_seq_cells)
                ci_seq = [self.controller_abs.get_ival_cons_cell(ci_cell, ci_ref.eps) for ci_cell in ci_seq_cells]
            else:
                ci_seq = get_ci(path)

            #print(pi_seq)

            #FIXME: Why are uniqe paths found only for the case when dim(ci) != 0?
            plant_states_along_path = tuple(state.plant_state for state in path)
            if plant_states_along_path not in unique_paths:
                unique_paths.add(plant_states_along_path)

                if ci_dim != 0:
                    assert(len(ci_seq) == len(path) - 1)
                else:
                    assert(len(ci_seq) == 0)
                if pi_dim != 0:
                    assert(len(pi_seq) == len(path) - 1)
                else:
                    assert(len(pi_seq) == 0)

#                 max_len = max(len(ci_seq), max_len)
#                 min_len = min(len(ci_seq), min_len)

                max_len = max(len(path), max_len)
                min_len = min(len(path), min_len)

                ci_seq_list.append(ci_seq)
                pi_seq_list.append(pi_seq)
                init_list.append(path[0])

        assert(max_len <= self.N + 1)

        # normalize list lens by appending 0

#         if max_len != min_len or max_len < self.N:

#             # TODO: many a times we find paths, s.t. len(path) > self.N
#             # How should those paths be handled?
#             #   - Should they be ignored, shortened, or what?
#             #   - or should nothing be done about them?

#             for (idx, ci_seq) in enumerate(ci_seq_list):
#                 # instead of zeros, use random!
#                 num_of_missing_ci_tail = max(max_len, self.N) - len(ci_seq)
#                 ci_seq_list[idx] = ci_seq \
#                     + list(np.random.random((num_of_missing_ci_tail, ci_dim)))

#             for (idx, pi_seq) in enumerate(pi_seq_list):
#                 num_of_missing_pi_tail = max(max_len, self.N) - len(pi_seq)
#                 pi_seq_list[idx] = pi_seq \
#                     + list(np.random.random((num_of_missing_pi_tail, pi_dim)))

        for (idx, (ci_seq, pi_seq)) in enumerate(zip(ci_seq_list, pi_seq_list)):
            missing_ci_len = self.N - len(ci_seq)
            missing_pi_len = self.N - len(pi_seq)
            # row, column
            r, c_ci = missing_ci_len, ci_dim
            #FIXME: default random values
            if ci_ref is not None:
                ci_seq_list[idx] = ci_seq + [ci_cons] * missing_ci_len
            else:
                ci_seq_list[idx] = ci_seq + list(np.random.uniform(ci_cons.l, ci_cons.h, (r, c_ci)))
            #pi_seq_list[idx] = pi_seq + list(np.random.uniform(pi_cons.l, pi_cons.h, (r, c_pi)))
            pi_seq_list[idx] = pi_seq + [pi_cons] * missing_pi_len

        print('path states, min_len:{}, max_len:{}'.format(min_len, max_len))

        # ##!!##logger.debug('init_list:{}\n'.format(init_list))
        # ##!!##logger.debug('ci_seq_list:{}\n'.format(ci_seq_list))
        # print('len(init_list)', len(init_list))
        # print('len(ci_seq_list)', len(ci_seq_list))

#         for ci_seq in ci_seq_list:
#             print(ci_seq)
#         for pi_seq in pi_seq_list:
#             print(pi_seq)

        return (init_list, ci_seq_list, pi_seq_list)

    def get_abs_state_from_concrete_state(self, concrete_state):

        # ##!!##logger.debug(U.decorate('get_abs_state_from_concrete_state'))

        abs_plant_state = \
            self.plant_abs.get_abs_state_from_concrete_state(concrete_state)
        abs_controller_state = \
            self.controller_abs.get_abs_state_from_concrete_state(concrete_state.s)
        if abs_plant_state is None or abs_controller_state is None:
            return None
        else:
            abs_state = TopLevelAbs.get_abs_state(abs_plant_state,
                    abs_controller_state)

        # ##!!##logger.debug('concrete state = {}'.format(concrete_state))
        # ##!!##logger.debug('abstract state = {}'.format(abs_state))
        # ##!!##logger.debug(U.decorate('get_abs_state_from_concrete_state done'))

        return abs_state

    def get_concrete_states_from_abs_state(self, abstract_state):
        raise NotImplementedError

#    def get_ival_cons_from_abs_state(self, abstract_state):
#        return (PlantAbstraction.get_concrete_state_constraints(abstract_state.plant_state, ))

    def __repr__(self):
        return ''

        # return self.G.__repr__()

    def draw_2d(self):
        pos_dict = {}
        for n in self.G.nodes():
            if len(n.plant_state.cell_id) != 2:
                raise err.Fatal('only 2d abstractions can be drawn, with each node representing the coordinates (x,y)!. Was given {}-d'.format(len(n.plant_state.cell_id)))
            pos_dict[n] = n.plant_state.cell_id
        self.G.draw(pos_dict)


        # nx.draw_networkx(self.G, pos=pos_dict, labels=pos_dict, with_labels=True)
        # TODO: whats the use of draw?
        # plt.draw()

class AbstractState(object):

    def __init__(self, plant_state, controller_state):
        self.plant_state = plant_state
        self.controller_state = controller_state
        return

    # rename/shorten name hack

    @property
    def ps(self):
        return self.plant_state

    @property
    def cs(self):
        return self.controller_state

    def __eq__(self, x):

        # print('abstraction_eq_invoked')
#        return hash((self.plant_state, self.controller_state)) == hash(as)

        return hash(self) == hash(x)

    def __hash__(self):

        # print('abstraction_hash_invoked')

        return hash((self.plant_state, self.controller_state))

    def __repr__(self):
        return 'p={' + self.plant_state.__repr__() + '},c={' \
            + self.controller_state.__repr__() + '}'
