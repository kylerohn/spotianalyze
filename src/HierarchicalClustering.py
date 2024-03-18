import numpy as np
from pandas import DataFrame
from Cluster import Cluster
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

class HierarchicalCluster:
    def __init__(self, cluster_data: DataFrame, features: list):

        
        feature_matrix: np.array = cluster_data[features].to_numpy()
        self.clusters: list[Cluster] = []
        for row in feature_matrix:
            self.clusters.append(Cluster(row))
    

    def _euclidian_distance(self, arr1, arr2):
        sum: float = 0
        for idx, val in enumerate(arr1):
            sum += np.power(val - arr2[idx], 2)
        return np.sqrt(sum)
    
    def _manhattan_distance(self, arr1, arr2):
        sum: float = 0
        for idx, val in enumerate(arr1):
            sum += np.fabs(val - arr2[idx])
        return sum


    def euclidian_cluster(self):
        while len(self.clusters ) > 1:
            for idxc, cluster in enumerate(self.clusters):
                print(len(self.clusters))
                min_distance = 1000
                curr_idx = 0
                for idx in range(idxc+1, len(self.clusters)):
                    # print(len(self.clusters[idx].cluster), idx)
                    curr_dist =  self._euclidian_distance(cluster.avg_features(), self.clusters[idx].avg_features())
                    if curr_dist < min_distance:
                        min_distance = curr_dist
                        curr_idx = idx
                cluster.merge(self.clusters[curr_idx])
                del self.clusters[curr_idx]
    

    def manhattan_cluster(self):
        while len(self.clusters ) > 1:
            for idxc, cluster in enumerate(self.clusters):
                print(len(self.clusters))
                min_distance = 1000
                curr_idx = 0
                for idx in range(idxc+1, len(self.clusters)):
                    # print(len(self.clusters[idx].cluster), idx)
                    curr_dist = self._manhattan_distance(cluster.avg_features(), self.clusters[idx].avg_features())
                    if curr_dist < min_distance:
                        min_distance = curr_dist
                        curr_idx = idx
                cluster.merge(self.clusters[curr_idx])
                del self.clusters[curr_idx]


    def heatmap(self):
        heatmap_arr = self.clusters[0].to_numpy()
        plt.imshow(heatmap_arr, interpolation='nearest', aspect=0.05, cmap='hot')
        plt.show()




            
    
