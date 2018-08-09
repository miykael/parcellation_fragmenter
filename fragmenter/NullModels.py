from fragmenter import rotations
import numpy as np
from scipy.spatial import KDTree


class NullModel(object):
    """
    Class to generate null models of parcellations by perturbing an existing
    map using KD-Trees for the nearest neighor search.

    Parameters:
    - - - - -
        sphere: (N, 3) array
            vertex coordinates of a spherical mesh
        label: (N, 1) array
            vertex labels
        mask: (N, 1) array
            list of non-midline vertices
    """

    def __init__(self, sphere, label, mask=None):

        self.label = label
        self.sphere = sphere

        if not np.any(mask):
            mask = np.arange(label.shape[0])

        self.mask = mask

    def fit(self):
        """
        Wrapper method for generating null models.
        """

        rotated = self._rotate()

        print('Fitting KD-Tree')
        K = KDTree(rotated)

        print('Querying tree for nearest neighbors.')
        kdnn = K.query(self.sphere[self.mask, :], k=1)
        kd_label = self.label[kdnn[1]]

        return kd_label

    def _rotate(self, maxd_x=10, maxd_y=10, maxd_z=10):
        """
        Randomly rotate the original spherical mesh.

        Parameters:
        - - - - -
            maxd_x, maxd_y, maxd_z : float
                maximum range of angle to sample for each direction
        """

        x = np.deg2rad(np.random.uniform(-maxd_x, maxd_x, 1))
        y = np.deg2rad(np.random.uniform(-maxd_y, maxd_y, 1))
        z = np.deg2rad(np.random.uniform(-maxd_z, maxd_z, 1))

        rx = rotations.rotx(x)
        ry = rotations.roty(y)
        rz = rotations.rotz(z)

        composed = rx.dot(ry.dot(rz))

        rotated = self.sphere.dot(composed)

        return rotated
