from NullBase import NullBase
from fragmenter import adjacency
import numpy as np


class Sampler(NullBase.NullBase):

    """
    Class to generate parcellation null models through resampling of
    neighborhood labels.  Using a Gibb's sampling approach, resamples the
    current label of a vertex with probability according to how many
    directly adjacent vertices have are assigned a label.

    Parameters:
    - - - - -
    vertices: (N, 3) array
        vertex coordinates of a spherical mesh
    faces: list
        all faces on surface mesh
    label: (N, 1) array
        vertex labels
    mask: list
        list of non-midline vertices
    """

    def __init__(self, vertices, faces, label, mask=None):

        self.vertices = vertices
        self.faces = faces
        self.label = label

        if not np.any(mask):
            mask = np.arange(label.shape[0])

        self.mask = mask

    def fit(self, iterations=1):

        """
        Wrapper method to generate resampled null model.

        Parameters:
        - - - - -
        iterations : int
            how many iterations of resampling to do
        """

        label = self.label.copy()

        surf_adj = adjacency.SurfaceAdjacency(self.vertices, self.faces)
        surf_adj.generate()
        surf_adj = surf_adj.filtration(filter_indices=self.mask)

        resampled = np.zeros((self.label.shape[0],))
        for iters in np.arange(iterations):
            for v in surf_adj.keys():
                neighbors = surf_adj[v]
                resampled[v] = np.random.choice(label[neighbors])
            label = resampled

        return resampled
