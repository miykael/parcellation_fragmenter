import numpy as np


def get_equally_spaced_colors(n):
    """
    Returns a color table with N elements, equally spaced throughout RGB-space.

    Parameters:
    - - - - -
    n : int
        number of parcels
    """

    max_value = 256**3 - 1
    equal_spaced = np.linspace(0, max_value, n, endpoint=True, dtype='int')
    colors = [hex(i)[2:].zfill(6) for i in equal_spaced]

    color_table = np.array(
        [[int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)] for i in colors])

    return color_table


def get_ctab_and_names(n_clusters, coords, labels, use_pretty_colors=True):
    """
    Returns color table and names - pretty color gradient order optional.

    Parameters:
    - - - - -
    n_clusters : int
        number of parcels
    coords : array
        vertex coordinates
    labels : array
        cluster map
    use_pretty_colors : bool
        generate pretty colors
    """

    # Create color table (first element = [0, 0, 0] for 'unknown' region)
    n_colors = n_clusters + 1
    ctab = np.hstack((get_equally_spaced_colors(n_colors), [[0]] * n_colors))

    # Create name list for new regions
    names = [np.bytes_('unknown')] + \
        [np.bytes_('parc%05d' % (i + 1)) for i in range(n_clusters)]

    # Reorder table and names according distance to sphere "bottom"
    if use_pretty_colors:

        # Compute mean height (on z-axis) per label to resort color table
        label_centers = np.array(
            [np.mean(coords[labels == l], axis=0) for l in np.unique(labels)])

        # Find new order of labels
        sphere_bottom = [0, 0, -100]
        label_order = np.argsort(np.linalg.norm(
            label_centers - sphere_bottom, axis=1)) + 1

        # Relabels labels accordingly
        labels = np.array(
            [np.where(label_order == l)[0][0] + 1 for l in labels])

    return ctab, names, labels
