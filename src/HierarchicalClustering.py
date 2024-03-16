import numpy as np
from pandas import DataFrame
from Cluster import Cluster

class HierarchicalCluster:
    def __init__(self, cluster_data: DataFrame, features: list):

        
        feature_matrix: np.array = cluster_data[features].to_numpy()
        self.clusters: list[Cluster] = []
        for row in feature_matrix:
            self.clusters.append(Cluster(row))
    

    def euclidian_cluster(self):
        for cluster in (self.clusters):
            

    def _euclidian_distance(self, arr1: list, arr2: list):
        sum: float = 0
        for idx: int, val: float in arr1:
            sum += np.power(val - arr2[idx], 2)
        return np.sqrt(sum)

            
    
