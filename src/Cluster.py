import numpy as np


class Cluster:
    """
    Class to hold clusters of data for statistical analysis
    """


    def __init__(self, names, *args):
        """
        Initializes Cluster object with list or collection of lists

        Args: 
            *args (List): Lists of data elements of the same length

        Returns
        """
        self.cluster = []
        self.names = [names]
        for arg in args:
            print(arg)
            self.cluster.append(arg)


    def __repr__(self):
        return f"Rows: {len(self.cluster)}"

    
    def merge(self, merge_cluster):
        """
        Merges the current cluster with another cluster.

        Args:
            merge_cluster (Cluster): The cluster to merge with.
        """
        for c in merge_cluster.cluster:
            self.cluster.append(c)
        for n in merge_cluster.names:
            self.names.append(n)
    

    def avg_features(self):
        """
        Calculates the average feature values across all data points in the cluster.

        Returns:
            numpy.ndarray: An array containing the average feature values.

        """
        # turn current cluster into numpy array
        np_cluster = np.array(self.cluster)
        # sum columns
        sums = np.sum(np_cluster, axis=0)
        # divide each element by the length of the cluster
        sums /= len(self.cluster)
        return sums  


    def min_features(self):
        mins = []
        np_cluster = np.array(self.cluster).T
        for row in np_cluster:
            mins.append(float(min(row)))
        return (np.array(mins))


    def max_features(self):
        maxs = []
        np_cluster = np.array(self.cluster).T
        for row in np_cluster:
            maxs.append(float(max(row)))
        return (np.array(maxs))

    def linkage(self, link_select: str='average'):
        if link_select == 'average':
            res = self.avg_features()
        elif link_select == 'min':
            res = self.min_features()
        elif link_select == 'max':
            res = self.max_features()
        else:
            print("Invalid Linkage Selection. Options: average, min, max")
        return res

    def to_numpy(self):
        return np.array(self.cluster)