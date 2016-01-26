from __future__ import print_function
from collections import defaultdict
import itertools
from utils import print
import cellmanager as CM


class WMap_old(object):
    def __init__(self, plant_abs, pi_cons):
        self.pa = plant_abs
        # should never be changed after initialized!
        self.pi_cons = pi_cons
        self.pi_dim = self.pa.num_dims.pi
        # s2p: state_to_pi_map
        self.s2p = defaultdict(set)
        # refined or not
        self.refine_ = False
        return

    def update_from_path(self, path, pi_seq):
        for abs_state, pi in zip(path, pi_seq):
            self.add(abs_state.plant_state, pi)
        return

    # pabs: plant_abs_state
    def add(self, pabs, pi_cell):
        #self.s2p[hash(pabs)].add(pi_cell)
        self.s2p[pabs.cell_id].add(pi_cell)
        return

    # observed pi_cells associated with abs_state
    def obs_pi_cells(self, pabs):
        if self.refine_:
            pi_cells = self.refined_get(pabs)
        else:
            #pi_cells = self.s2p.get(hash(pabs))
            pi_cells = self.s2p.get(pabs.cell_id)
        if not pi_cells:
            pi_cells = self.get_all_pi_cells()
        return pi_cells

    # TODO: memoize this!
    def get_all_pi_cells(self):
        pa = self.pa
        #print(self.pi_cons, pa.pi_eps)
        pi_cells = CM.get_pi_cells_from_ival_constraints(self.pi_cons, pa.pi_eps)
        #print(pi_cells)
        #raw_input('..')
        #return [c for c in zip(*pi_cells)]
        return pi_cells

    # TODO: memoize this!
    def refined_get(self, pabs):
        parent_hash = self.get_parent_hash(pabs)
        parent_pi_cells = self.s2p.get(parent_hash, self.get_all_pi_cells())
        #for i in self.s2p:
        #    print(i)
        #print('query:', pabs.cell_id, parent_hash)
#         if self.s2p.get(parent_hash):
#             print('parent_pi_cells NON EMPTY!')
        #pi_cells = set(self.get_children(cell) for cell in parent_pi_cells)
        pi_cells = set(ccell for pcell in parent_pi_cells for ccell in self.get_children(pcell))
        #pi_cells = set(ccell for ccell in self.get_children(pcell) for pcell in parent_pi_cells)
        return pi_cells

    def refine(self):
        self.refine_ = True
        #self.pi_eps = self.pi_eps/2.0

    def cleanup(self, pa):
        self.refine_ = False
        self.s2p = defaultdict(set)

    def get_children(self, parent_cell_id, lvl=1):
        #print(parent_cell_id)
        l = [[coord, coord+1] for coord in parent_cell_id]
        #print(list(itertools.product(*l)))
        return list(itertools.product(*l))

    #TODO: Direct Format manipulation of abstract state
    def get_parent_hash(self, abs_state, lvl=1):
        cell_id = abs_state.cell_id
        # as i is an int, i/2 is equivalent to int(floor(i/2.0))
        # return tuple(int(floor(i/2.0)) for i in cell_id) # for clarity
        return tuple(i/2 for i in cell_id) # same as above


class WMap(object):
    # abs is either plant or controller abs
    def __init__(self, i_cons, eps):
        self.eps = eps
        # should never be changed after initialized!
        self.i_cons = i_cons
        # s2p: state_to_pi_map
        self.s2p = defaultdict(set)
        # refined or not
        self.refine_ = False
        return

    def update_from_path(self, path, i_seq):
        for abs_state, i_cell in zip(path, i_seq):
            cell_id = abs_state.plant_state.cell_id
            self.s2p[cell_id].add(i_cell)
        return

    # observed i_cells associated with abs_state
    def obs_i_cells(self, abs_state):
        if self.refine_:
            i_cells = self.refined_get(abs_state)
        else:
            i_cells = self.s2p.get(abs_state.cell_id)
        if not i_cells:
            i_cells = self.get_all_i_cells()
        return i_cells

    # TODO: memoize this!
    def get_all_i_cells(self):
        eps = self.eps
        #i_cells = CM.get_i_cells_from_ival_constraints(self.i_cons, eps)
        i_cells = CM.get_cells_from_ival_constraints(self.i_cons, eps)
        return i_cells

    # TODO: memoize this!
    def refined_get(self, abs_state):
        parent_hash = self.get_parent_hash(abs_state)
        parent_i_cells = self.s2p.get(parent_hash, self.get_all_i_cells())
        i_cells = set(ccell for pcell in parent_i_cells for ccell in self.get_children(pcell))
        return i_cells

    def refine(self):
        self.refine_ = True
        self.eps = self.eps/2.0

    def cleanup(self):
        self.refine_ = False
        self.s2p = defaultdict(set)

    def get_children(self, parent_cell_id):
        return CM.get_children(parent_cell_id)

    def get_parent_hash(self, abs_state):
        return CM.get_parent_hash(abs_state)
