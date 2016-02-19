from scipy.spatial import KDTree
# Implemented in C
from scipy.spatial import cKDTree
import numpy as np

class CPerror(Exception):
    pass

class ClosestPairs():
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def get_closest_pairs(self, max_dist):
        self.kdt1 = KDTree(self.data1)
        self.kdt2 = KDTree(self.data2)
        spm = self.kdt1.sparse_distance_matrix(self.kdt2, max_dist)
        return spm
