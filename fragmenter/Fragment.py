import clusterings

METHODS = ['gmm', 'k_means', 'spectral', 'ward']


class Fragment(object):

    """
    Class to fragment the cortical surface into equal sized parcels.

    Parameters:
    - - - - -
    n_clusters : int
        number of parcels to generate
    use_pretty_colors : bool
        use gradient color scheme for viewing map
    """

    def __init__(self, n_clusters, use_pretty_colors=True):

        self.n_clusters = n_clusters
        self.use_pretty_colors = use_pretty_colors

    def fit(self, vertices, faces, method='kmeans', rois=None):

        """
        Main surface fragmentation wrapper.

        Parameters:
        - - - - -
        vertices : array
            vertex coordinates
        faces : array
            list of faces
        method : string
            algorithm to use for generating parcels
        rois : list of strings
            specific regions to fragment.  If None, fragment all regions.
        """

        assert method in METHODS

        if method == 'spectral':
            pass

        clust_funcs = {
            'gmm': clusterings.gmm(),
            'kmeans': clusterings.kmeans(),
            'spectral': clusterings.spectral_clustering(),
            'ward': clusterings.ward()}

        label = clust_funcs[method]()

        self.label_ = label
