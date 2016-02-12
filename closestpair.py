import scipy.spatial.KDTree as kdt
# Implemented in C
import scipy.spatial.cKDTree as cktd

import numpy as np

# TODO: Fix this!
NUM_DIMS = 3

class CPERROR(Exception):
    pass

class CP(object):
    def __init__(self, g1, g2):
        num_dims = NUM_DIMS
        raise CPERROR('Fix NUM DIMS! Communicate dimensions some how!')

        a1 = np.zeros((len(g1), num_dims), dtype=int)
        for idx, s in enumerate(g1):
            a1[idx] = s

        a2 = np.zeros((len(g2), num_dims), dtype=int)
        for idx, s in enumerate(g2):
            a2[idx] = s

    def get_closest(self):
        raise NotImplementedError
        # make two trees and generate sparse_distance_matrix?
        # kdt.sparse_distance_matrix(other, max_distance)

        # query all pairs within r distance
        # query_pairs(self, r[, p, eps])
