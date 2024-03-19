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

        Returns:
            None

        Modifies:
            Updates the cluster attribute of the current object by appending 
            the cluster attribute of the merge_cluster object.

        Note:
            This method assumes that the merge_cluster parameter is an object 
            of a class with a 'cluster' attribute representing a cluster of data.
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

        Note:
            This method assumes that the cluster attribute of the instance contains
            data points with consistent feature dimensions.

        Example:
            If the cluster attribute contains the following data points:
            [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]

            The returned array would be:
            [4.0, 5.0, 6.0]
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