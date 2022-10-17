from sklearn.metrics import silhouette_score,silhouette_samples


class LoadClusteringProgram:

    @staticmethod
    def __call__(cluster_program_name):
        if cluster_program_name is not None:
            cluster_program_name = cluster_program_name.replace('_', '').replace(' ', '').lower()

        if cluster_program_name in ['dbscan', None]:
            from sklearn.cluster import DBSCAN
            return DBSCAN

        if cluster_program_name in ['hdbscan']:
            from hdbscan.hdbscan_ import HDBSCAN
            return HDBSCAN

        if cluster_program_name in ['kmeans', 'kmean']:
            from sklearn.cluster import KMeans
            return KMeans


class UnsupervisedLearning:

    def __init__(self, cluster_program_name, dict_param=None):
        self.cluster_program = LoadClusteringProgram()(cluster_program_name)

        self.dict_param = dict_param
        if self.dict_param is None:
            self.dict_param = {}

    def fit(self, data):
        self.cluster_program(**self.dict_param).fit(data)

    def fit_predict(self, data):
        labels = self.cluster_program(**self.dict_param).fit_predict(data)
        return labels

    @staticmethod
    def silhouette_score(data, labels):
        """
            Compute the mean Silhouette Coefficient of all samples.

            This measure has a range of [-1, 1].
            Silhouette coefficients (as these values are referred to as) near +1 indicate that the sample is far away
            from the neighboring clusters. A value of 0 indicates that the sample is on or very close to the decision
            boundary between two neighboring clusters and negative values indicate that those samples might have been
            assigned to the wrong cluster.
        """
        return silhouette_score(data, labels)

    @staticmethod
    def silhouette_samples(self, data, labels):
        """
            Compute the silhouette scores for each sample.

            #
        """
        return silhouette_samples(data, labels)



