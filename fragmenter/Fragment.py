import adjacency
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

    def fit(
            self, vertices, faces, method='kmeans', rois=None, mask=None):

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

        # make sure method exists in allowed algorithms
        assert method in METHODS
        n_clusters = self.n_clusters

        # if provided method is spectral clustering,
        # generate adjacency matrix
        if method == 'spectral':
            surf_adj = adjacency.SurfaceAdjacency(vertices, faces)
            surf_adj.generate()
            samples = surf_adj.filtration(filter_indices=mask, to_array=True)
        else:
            samples = vertices

        # define function dictionary
        clust_funcs = {
            'gmm': clusterings.gmm(),
            'kmeans': clusterings.kmeans(),
            'spectral': clusterings.spectral_clustering(),
            'ward': clusterings.ward()}

        # generate fragmentation
        label = clust_funcs[method](n_clusters, samples)

        self.label_ = label
