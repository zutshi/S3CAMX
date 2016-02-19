from __future__ import print_function

import numpy as np
#from operator import itemgetter as itmgr

from closestpair import ClosestPairs
#import utils as U
import err
from utils import print
import utils as U
#import dbg

MAX_ABS_DIST = 1.5
MAX_CONC_DIST = 0.8


def search_final_abs_states(current_abs_list):
    '''
    Use this function when the property is a function of the states of
    multiple constituent systems.
    @type current_abs_list: list
    '''
    # deals with only 2 systems for now
    assert(len(current_abs_list) == 2)
    #for current_abs in current_abs_list:
    #    print current_abs.G

    #current_abs = current_abs_list[0]
    #print current_abs.G.nodes()[0].ps.cell_id
    grid_eps = current_abs_list[0].plant_abs.eps
    print(grid_eps, type(grid_eps))
    cp = GCP(current_abs_list[0].G, current_abs_list[1].G, grid_eps*0.001)
    closest_nodes = cp.get_closest_pairs(MAX_ABS_DIST)
    print(closest_nodes)
    if closest_nodes:
        return zip(*closest_nodes)
    else:
        return closest_nodes


# tom: trace offset map
# idx of the state w.r.t. the stacked traces
# tom format: [0 len(t1) len(t1)+len(t2) ... len(t1)+len(t2)+..+len(tn)]
def trace_lookup(idx, tom, traces):
    '''returns the trace using the idx and the offset table'''
    # trace id
    # argmax of bools returns the first True value
    tmp = np.greater(tom, idx)
    # atleast one element should be True and one should be False
    assert(any(tmp) and not all(tmp))
    # adjust for the 0 in the tom
    tid = np.argmax(tmp) - 1
    # get the element id by subtracting the previous cumsum from the idx
    eid = idx - tom[tid]
    # tid is the what we are looking for
    # eid is the exact state which in the trace tid which comes the
    # closest. It can be used for debugging
    return tid


def search_final_concrete_states(l_traces):
    # deals with only 2 systems for now
    assert(len(l_traces) == 2)

    def data(x): return x[1]

    if __debug__:
        import traces
        import matplotlib.pyplot as plt
        traces.plot_trace_list(l_traces[0]+l_traces[1], plt)

    # get all the states: x from the traces of system 0
    traces1 = l_traces[0]
    traces_offset_map1 = np.cumsum([0] + [trace.n for trace in traces1])
    x_traces1 = np.vstack([trace.x_array for trace in traces1])

    traces2 = l_traces[1]
    traces_offset_map2 = np.cumsum([0] + [trace.n for trace in traces2])
    x_traces2 = np.vstack([trace.x_array for trace in traces2])

    cp = ClosestPairs(x_traces1, x_traces2)
    spm = cp.get_closest_pairs(MAX_CONC_DIST)
    if spm.nnz == 0:
        return False
    sorted_spm = sorted(spm.items(), key=data)
    if __debug__:
        print(sorted_spm)
    l_idx1_idx2, l_data = zip(*sorted_spm)

    #unique_traces1
    #unique_traces2
    trace_idx_pairs = [(trace_lookup(idx1, traces_offset_map1, traces1),
                        trace_lookup(idx2, traces_offset_map2, traces2))
                       for idx1, idx2 in l_idx1_idx2]
    if __debug__:
        print(trace_idx_pairs)
        U.pause('trace_idx_pairs')
    trace_pairs = [(traces1[idx1], traces2[idx2]) for idx1, idx2 in trace_idx_pairs]

    if __debug__:
        print(trace_pairs)
        U.pause('trace_pairs')
    return trace_pairs


class GCP(object):
    '''Graph closest pairs'''
    def __init__(self, g1, g2, eps=0.0):
        '''
        @type g1: networkx.Graph
        @type g2: netowrkx.Graph
        '''

        # l_cells1
        # create a generator to get all cell_ids which are exactly the
        # cell coordinates. These will be given to the spatial data
        # structure for a k-NN search
        #
        # l_abs_states1
        # Keep a back reference to get back the original abstract
        # states/graph nodes from cell idx returned from the spatial
        # data structure
        gn1 = ((n, n.ps.cell_id) for n in g1.nodes_iter())
        self.l_abs_states1, self.l_cells1 = zip(*gn1)

        gn2 = ((n, n.ps.cell_id) for n in g2.nodes_iter())
        self.l_abs_states2, self.l_cells2 = zip(*gn2)

        # Perturbation is required to get overlapping cells. Because
        # the result of the KDTree.sparse_distance_matrix() is a
        # sparse() matrix whenever the distance between two points is
        # more than the max_distance. Hence, if the data exactly
        # matches with distance = 0 or is > max_dist, the results is
        # the same 0!. Perturbation helps resolve this issue in some
        # way.
        err.warn('perturbing the cells by an arbitrary eps')
        self.cp = ClosestPairs(self.l_cells1,
                               np.asarray(self.l_cells2) + eps)
        #self.kdt1 = KDTree(self.l_cells1)
        #self.kdt2 = KDTree(np.asarray(self.l_cells2)+0.0001)

        self.g1 = g1
        self.g2 = g2

#         print k1.data
#         U.pause()
#         print k2.data
#         U.pause()

    # make two trees and generate sparse_distance_matrix?
    # kdt.sparse_distance_matrix(other, max_distance)

    # query all pairs within r distance
    # query_pairs(self, r[, p, eps])
    def get_closest_pairs(self, max_dist=np.inf):
        def data(x): return x[1]
        spm = self.cp.get_closest_pairs(max_dist)
        if spm.nnz == 0:
            return False
        if __debug__:
            print(spm)
            print(spm.nnz)

        # verify if values are nodes
        #for n1, n2 in cp_graph_nodes:
            #print self.g1.G[n1], self.g2.G[n2]

        # unsorted values
        #cp_graph_nodes = [(self.l_abs_states1[k1], self.l_abs_states2[k2])
        #                  for k1, k2 in sorted_spm.iterkeys()]

        # sorted values
        sorted_spm = sorted(spm.items(), key=data)
        if __debug__:
            print(sorted_spm)
        l_idx1_idx2, l_data = zip(*sorted_spm)
        # More clearer but perhaps slower
        #l_idx1, l_idx2 = zip(*l_idx1_idx2)
        #l_n1 = itmgr(*l_idx1)(self.l_abs_states1)
        #l_n2 = itmgr(*l_idx2)(self.l_abs_states2)
        #cp_graph_nodes = zip(l_n1, l_n2)

        # More efficient?
        cp_graph_nodes = [(self.l_abs_states1[i[0]], self.l_abs_states2[i[1]])
                          for i in l_idx1_idx2]

        if __debug__:
            for d in l_data:
                print(d)

#         for k, d in spm.iteritems():
#             print self.kdt1.data[k[0], :], self.kdt2.data[k[1], :]-0.0001, d-0.0001

        return cp_graph_nodes

# def check_cell_id_is_hashed(g):
#     # get a node, lets say the first one
#     n = g.nodes_iter().next()
#     print n, hash(n), hash((n.ps.cell_id, tuple(n.cs.s)))
#     print n.ps.cell_id, tuple(n.cs.s)
#     assert(hash(n) == n.ps.cell_id)
