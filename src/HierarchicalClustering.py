import numpy as np
from pandas import DataFrame

class HierarchicalCluster:
    def __init__(self, cluster_data: DataFrame, features: list):

        self.feature_matrix = cluster_data[features].to_numpy()
        self._cluster()

    
    def _cluster(self):
        for idxs in range(0, self.feature_matrix.shape[0], 2):
            min_distance = 1000
            for idxc in range(idxs + 1, self.feature_matrix.shape[0]):
                distance = self._euclidian_distance(self.feature_matrix[idxs], self.feature_matrix[idxc])
                if min_distance > distance:
                    min_distance = distance
                    min_idx = idxc

            self.feature_matrix[idxs+1], self.feature_matrix[min_idx] = self.feature_matrix[min_idx], self.feature_matrix[idxs+1]
            pass
    
    def _euclidian_distance(self, arr, arr2):
        sum = 0
        for idx, val in enumerate(arr):
            sum +=np.power(val-arr2[idx], 2)
        return np.sqrt(sum)

