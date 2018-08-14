import numpy as np

"""
Methods to generate 3D rotation matrices.
Code converted from original Matlab version:
 * https://github.com/petercorke/robotics-toolbox-matlab

"""


def rotx(t):

    """
    Computes rotation matrix around the x-axis.

    Parameters:
    - - - - -
        t : input angle in radians
    """

    ct = np.cos(t)
    st = np.sin(t)

    R = np.asarray(
        [[1, 0, 0],
         [0, ct, -st],
         [0, st, ct]])

    return R


def roty(t):

        """
        Computes rotation matrix around the y-axis.

        Parameters:
        - - - - -
            t : input angle in radians
        """

        ct = np.cos(t)
        st = np.sin(t)

        R = np.asarray(
            [[ct, 0, st],
             [0, 1, -st],
             [-st, 0, ct]])

        return R


def rotz(t):

    """
    Computes rotation matrix around the z-axis.

    Parameters:
    - - - - -
        t : input angle in radians
    """

    ct = np.cos(t)
    st = np.sin(t)

    R = np.asarray(
        [[ct, -st, 0],
         [st, ct, 0],
         [0, 0, 1]])

    return R
