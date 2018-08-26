import numpy as np

from fragmenter import adjacency
from fragmenter import clusterings
from fragmenter import colormaps

from nibabel import freesurfer

# define clustering options
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

        # make sure method exists in allowed algorithms
        assert method in METHODS
        assert isinstance(size, int)

        # define function dictionary
        clust_funcs = {
            'gmm': clusterings.gmm,
            'k_means': clusterings.k_means,
            'spectral': clusterings.spectral_clustering,
            'ward': clusterings.ward}

        self.vertices = vertices
        n_clusters = self.n_clusters

        # if provided method is spectral,
        # generate adjacency matrix
        if method == 'spectral':
            surf_adj = adjacency.SurfaceAdjacency(vertices, faces)
            surf_adj.generate()

        # if parcels and rois are None, just parcellate the whole cortex
        if not parcels or not rois:
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

            label = clust_funcs[method](n_clusters, samples)

        # otherwise, if parcels AND rois are provided
        # fragment on a region-by-region basis
        else:
            label = np.zeros((vertices.shape[0]))

            # loop over regions
            lmax = 0
            for region in rois:
                print(region)
                # make sure the region has vertices
                if np.any(parcels[region]):
                    # get region indices
                    parcel_idx = parcels[region]

                    # if method == spectral, regional adjacency matrix
                    if method == 'spectral':
                        parcel_samples = surf_adj.filtration(
                            filter_indices=parcel_idx, toArray=True)
                    # otherwise, extract region-specific
                    # vertex coordaintes
                    else:
                        parcel_samples = vertices[parcel_idx, :]

                    # make sure that the desired number of clusters does not
                    # exceed the number of samples to cluster
                    if size:
                        n_clusters = np.int32(np.ceil(
                            parcel_samples.shape[0]/size))

                    if n_clusters > parcel_samples.shape[0]:
                        n_clusters = 1

                    # apply clustering
                    clusters = clust_funcs[method](
                        n_clusters, parcel_samples)

                    # ensure that cluster ID is += by current cluster count
                    clusters += lmax

                    lmax += len(np.unique(clusters))
                    label[parcel_idx] = clusters

        self.label_ = np.int32(label)

    def write(self, output_name, use_pretty_colors=True):
        """
        Write the fragmented label file to FreeSurfer annotation file.

        Parameters:
        - - - - -
        output_name: string
            name of save file to
        """

        [keys, ctab, names, remapped] = colormaps.get_ctab_and_names(
            self.vertices, self.label_, use_pretty_colors=use_pretty_colors)

        freesurfer.io.write_annot(output_name, remapped, ctab, names)
