from fragmenter import adjacency
from fragmenter import clusterings
import numpy as np

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
            self, vertices, faces, parcels=None, rois=None, size=False,
            method='k_means'):

        """
        Main surface fragmentation wrapper.

        Parameters:
        - - - - -
        vertices : array
            vertex coordinates
        faces : array
            list of faces
        parcels : dictionary
            mapping between region names and region indices
        rois : list of strings
            specific regions to fragment.  If None, fragment all regions.
        size : int
            desired size of generated framents.  If specified, overrides
            n_clusters.
        method : string
            algorithm to use for generating parcels
        """

        # define function dictionary
        clust_funcs = {
            'gmm': clusterings.gmm,
            'k_means': clusterings.k_means,
            'spectral': clusterings.spectral_clustering,
            'ward': clusterings.ward}

        # make sure method exists in allowed algorithms
        assert method in METHODS
        assert isinstance(size, int)

        n_clusters = self.n_clusters

        # if provided method is spectral,
        # generate adjacency matrix
        if method == 'spectral':
            surf_adj = adjacency.SurfaceAdjacency(vertices, faces)
            surf_adj.generate()

        # if parcels and rois are None, just parcellate the whole cortex
        if not parcels and not rois:
            # if method is spectral, convert whole adjacency list to
            # adjacency matrix
            if method == 'spectral':
                samples = surf_adj.filtration(
                    filter_indices=None, toArray=True)
            else:
                samples = vertices

            if size:
                n_clusters = np.int32(np.floor(
                    samples.shape[0]/size))

            # fragment whole brain
            label = clust_funcs[method](n_clusters, samples)

        # otherwise, if parcels AND rois are provided
        # fragment on a region-by-region basis
        else:
            label = np.zeros((vertices.shape[0]))

            # loop over regions
            for region in rois:
                print(region)
                # make sure the region has vertices
                if np.any(parcels[region]):
                    # get region indices
                    parcel_idx = parcels[region]
                    # if method is spectral, extract intra-region
                    # adjacency matrix
                    if method == 'spectral':
                        parcel_samples = surf_adj.filtration(
                            filter_indices=parcel_idx, toArray=True)
                    # otherwise, extract region-specific
                    # vertex coordaintes
                    else:
                        parcel_samples = vertices[parcel_idx, :]

                    if size:
                        n_clusters = np.int32(np.floor(
                            parcel_samples.shape[0]/size))

                    # fragment
                    clusters = clust_funcs[method](
                        n_clusters, parcel_samples)

                    label[parcel_idx] = clusters

        # Increase labels by one to prevent transparent mesh
        label += 1

        self.label_ = label
