import numpy as np


class Cluster:
    """
    Class to hold clusters of data for statistical analysis
    """


    def __init__(self, *args):
        """
        Initializes Cluster object with list or collection of lists

        Args: 
            *args (List): Lists of data elements of the same length

        Returns
        """
        self.cluster = []
        for arg in args:
            print(arg)
            # normalize values between 0 and 1
            arg[2] = arg[2] / 11
            arg[-1] = (arg[-1] - 60) / 180
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
    

    def to_numpy(self):

        return np.array(self.cluster)