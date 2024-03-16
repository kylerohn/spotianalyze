import numpy as np
from pandas import DataFrame
from Cluster import Cluster

class HierarchicalCluster:
    def __init__(self, cluster_data: DataFrame, features: list):

        
        self.feature_matrix: np.array = cluster_data[features].to_numpy()
        self.clusters: list[Cluster] = []
        for row in self.feature_matrix:
            self.clusters.append(Cluster(row))
        
    
