import numpy as np
from pandas import DataFrame
from Cluster import Cluster
import matplotlib.pyplot as plt
from const import CONST as C
import plotly.express as px

class AgglomerativeCluster:
    def __init__(self, cluster_data: DataFrame, features: list, identifier_key: str):
        """
        Initializes a HierarchicalClustering object.

        Args:
            cluster_data (DataFrame): DataFrame containing the data for clustering.
            features (list): List of feature names to be used for clustering.
            identifier_key (str): name of column to be used as the identifier for each sample

        Returns:
            None
        """
        # Extract song names from the DataFrame
        song_names = cluster_data[identifier_key]

        #set features as class variable
        self.features = features

        # Extract feature matrix from the DataFrame and convert it to a NumPy array
        feature_matrix: np.array = cluster_data[features].to_numpy()

        # Normalize feature values
        feature_matrix = feature_matrix.T  # Transpose the feature matrix
        for r, row_t in enumerate(feature_matrix):
            min_val = np.min(row_t)
            max_val = np.max(row_t)
            for c, val_t in enumerate(row_t):
                feature_matrix[r][c] = ((val_t - min_val) / (max_val - min_val))
        feature_matrix = feature_matrix.T  # Transpose the feature matrix back to its original orientation

        # Initialize an empty list to store Cluster objects
        self.clusters: list[Cluster] = []

        # Create Cluster objects and append them to the clusters list
        for idx, row in enumerate(feature_matrix):
            self.clusters.append(Cluster(song_names[idx], row))
    

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


    def hierarchical_cluster(self, n: int=1, linkage: str='average', distance: str='euclidian'):

        # distance function assignment
        if distance == 'euclidian':
            dist_func = self._euclidian_distance
        elif distance == 'manhattan':
            dist_func = self._manhattan_distance
        else:
            print("Invalid value for distance. Options: euclidian, manhattan")
        # loop through all iterations of cluster combinations
        while len(self.clusters ) > n:
            # loop through each cluster for each cluster combination
            for cluster in (self.clusters):
                print(len(self.clusters))
                min_distance = 1000
                curr_idx = 0
                # loop through clusters to compare to current cluster
                for idx in range(len(self.clusters)):
                    # if comparing to self, skip to next iteration
                    if cluster == self.clusters[idx]:
                        continue
                    curr_dist =  dist_func(cluster.linkage(linkage), self.clusters[idx].linkage(linkage))
                    if curr_dist < min_distance:
                        min_distance = curr_dist
                        curr_idx = idx
                # merge "most similar" cluster and remove merged cluster from collection
                cluster.merge(self.clusters[curr_idx])
                del self.clusters[curr_idx]


    def heatmap(self):
        heatmap_arr = self.clusters[0].to_numpy()
        names_arr = self.clusters[0].names
        print(self.clusters[0].names)
        print()
        for cluster in (self.clusters[1:]):
            heatmap_arr = np.concatenate((heatmap_arr, cluster.to_numpy()))
            for name in cluster.names:
                names_arr.append(name)
            print(cluster.names)
            print()
        
        df = DataFrame(data=heatmap_arr, index=names_arr, columns=self.features)

        fig = px.imshow(df, aspect='auto')
        fig.show()




            
    
