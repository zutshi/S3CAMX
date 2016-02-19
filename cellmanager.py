from __future__ import print_function

import numpy as np
import constraints as cons
import itertools

from utils import print


# TODO: change cons to cons_object which has cons in addition to all states
# a concrete state has
def ival_cons_to_cell_list(cons, eps):
    num_dims = cons.dim

    Al = cell_from_concrete(cons.l, eps)
    Ah = cell_from_concrete(cons.h, eps)

    x_range_list = []
    for i in range(num_dims):

        # x_range_list.append(np.arange(cons.l[i], cons.h[i], eps[i]))

        x_range = range(Al[i], Ah[i], 1)

        # make the range inclusive of the last element,  because we want things to be sound

        x_range.append(Ah[i])
        x_range_list.append(x_range)

    # construct a grid
        #grid = np.meshgrid(*x_range_list, copy=False)
        grid = np.meshgrid(*x_range_list)

#         # sometimes fails with memory errors
#         try:
#             grid = np.meshgrid(*x_range_list)
#         except MemoryError as e:
#             print('meshgrid with the below x_cons failed')
#             print(cons)
#             raise e

    # create iterators which iterate over each element of the dim. array

#         x_iter_list = []
#         for i in range(self.num_dims.x):
#             x_iter_list.append(np.nditer(grid[i]))
    x_iter_list = [np.nditer(grid[i]) for i in range(num_dims)]

    return x_iter_list


def get_cells_from_ival_constraints(x_cons, eps):

    x_list = ival_cons_to_cell_list(x_cons, eps)
    cell_list = [tuple(map(int, abs_state_array_repr)) for abs_state_array_repr in zip(*x_list)]

    return cell_list


def get_pi_cells_from_ival_constraints(cons, pi_eps):
    pi_list = ival_cons_to_cell_list(cons, pi_eps)
    pi_cells = [tuple(map(int, abs_state_array_repr)) for abs_state_array_repr in zip(*pi_list)]
    return pi_cells


def cell_from_concrete(X, eps):
    if any(np.isinf(c) for c in X):
        return None
    cell = np.floor(X / eps)

    # get the cell into integers...easier to do operations!

    cell_id = map(int, cell)
    return tuple(cell_id)


def ival_constraints(cell, eps):
    cell_coordinates = np.array(cell) * eps
    ival_l = cell_coordinates
    ival_h = cell_coordinates + eps
    return cons.IntervalCons(ival_l, ival_h)


def get_children(parent_cell_id, lvl=1):
    #print(parent_cell_id)
    l = [[coord, coord+1] for coord in parent_cell_id]
    #print(list(itertools.product(*l)))
    return list(itertools.product(*l))


#TODO: Direct Format manipulation of abstract state
def get_parent_hash(abs_state, lvl=1):
    cell_id = abs_state.cell_id
    # as i is an int, i/2 is equivalent to int(floor(i/2.0))
    # return tuple(int(floor(i/2.0)) for i in cell_id) # for clarity
    return tuple(i/2 for i in cell_id) # same as above
