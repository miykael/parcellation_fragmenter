import numpy as np
from nibabel import freesurfer
from nilearn.plotting import plot_surf_roi
from sklearn import cluster, mixture, neighbors
from time import time

"""
# Notes:
 - Can perhaps be optimized with something like
   https://github.com/NeuroanatomyAndConnectivity/surfdist/
 - perhaps better with dijkstra algorithm, but computation takes forever
 - perhaps better with something like `import gdist` - but it all takes way too long
"""


def get_spaced_colors(n):
    """
    Returns a colortable with N elements, equally spaced throughout RGB-space
    """

    max_value = 256**3 - 1
    equal_spaced = np.linspace(0, max_value, n, endpoint=True, dtype='int')
    colors = [hex(i)[2:].zfill(6) for i in equal_spaced]

    color_table = np.array(
        [[int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)] for i in colors])

    return color_table


def get_equally_spaced_points(coords, num_pts=100):
    """Return indices of vertices that cover the spherical mesh equally"""

    indices = np.arange(0, num_pts, dtype=float) + 0.5

    phi = np.arccos(1 - 2 * indices / num_pts)
    theta = np.pi * (1 + 5**0.5) * indices

    # Compute location of equally spaced points on a sphere
    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)

    # Compute sphere radius
    sphere_radius = np.mean(np.linalg.norm(coords, axis=1))

    # Adjust equally spaced points to requested sphere radius
    equal_points = np.vstack((x, y, z)).T * sphere_radius

    return np.array(equal_points)


def get_ctab_and_names(parcel_N, coords):

    # Create color table
    color_N = parcel_N + 1  # one more to keep 0 0 0 for color 'unknown'
    ctab = np.hstack((get_spaced_colors(color_N), [[0]] * color_N))

    # Create name list for parcellations
    names = [np.bytes_('unknown')] + [np.bytes_('parc%04d' % (i + 1))
                                      for i in range(parcel_N)]

    # Get center points
    center_points = get_equally_spaced_points(coords, num_pts=parcel_N)

    return ctab, names, center_points


def reorder_ctab_and_names(coords, labels, parcel_N, ctab, names):

    # Compute mean height (on z-axis) per label to resort color table
    label_centers = np.array(
        [np.mean(coords[labels == l], axis=0) for l in np.unique(labels)])
    label_order = np.argsort(label_centers[:, 2])

    # Verify that no label is missing from the data
    assert len(np.unique(label_order)) == parcel_N

    # Create the reordered color table
    ctab = np.vstack((ctab[0], ctab[1:][label_order]))
    names = [names[0]] + np.array(names)[1:][label_order].tolist()

    return ctab, names


def parcel_spherically(coords, parcel_N):

    ctab, names, center_points = get_ctab_and_names(parcel_N, coords)

    # Compute distance to center points
    center_distances = np.linalg.norm(
        np.array([coords - c for c in center_points]), axis=2)

    # Compute the labels for each vertex
    labels = np.argmin(center_distances, axis=0) + 1

    ctab, names = reorder_ctab_and_names(coords, labels, parcel_N, ctab, names)

    out_filename = 'freesurfer/fsaverage/label/lh.parc_sphere_%04d.annot' % parcel_N

    freesurfer.write_annot(out_filename, labels, ctab, names, fill_ctab=True)

    return out_filename


def parcel_KMeans(coords, parcel_N):

    ctab, names, center_points = get_ctab_and_names(parcel_N, coords)

    # Run Mini Batch KMeans algorithm
    k_means = cluster.MiniBatchKMeans(
        n_clusters=parcel_N, max_iter=1000, batch_size=50000,
        init=center_points, n_init=1, reassignment_ratio=0.1)
    k_means.fit(coords)

    # Compute the labels for each vertex
    labels = k_means.labels_.astype(np.int) + 1

    ctab, names = reorder_ctab_and_names(coords, labels, parcel_N, ctab, names)

    out_filename = 'freesurfer/fsaverage/label/lh.parc_kmeans_%04d.annot' % parcel_N

    freesurfer.write_annot(out_filename, labels, ctab, names, fill_ctab=True)

    return out_filename


def parcel_GMM(coords, parcel_N):

    ctab, names, center_points = get_ctab_and_names(parcel_N, coords)

    # Run Gaussian Mixture algorithm
    gmm = mixture.GaussianMixture(
        n_components=parcel_N, covariance_type='tied')
    gmm.fit(coords)

    # Compute the labels for each vertex
    labels = gmm.predict(coords).astype(np.int) + 1

    ctab, names = reorder_ctab_and_names(coords, labels, parcel_N, ctab, names)

    out_filename = 'freesurfer/fsaverage/label/lh.parc_gmm_%04d.annot' % parcel_N

    freesurfer.write_annot(out_filename, labels, ctab, names, fill_ctab=True)

    return out_filename


def parcel_Ward(coords, parcel_N):

    ctab, names, center_points = get_ctab_and_names(parcel_N, coords)

    # AgglomerativeClustering with ward
    knn_graph = neighbors.kneighbors_graph(
        coords, 50, include_self=False, n_jobs=-1,
        mode='connectivity', metric='minkowski', p=2)

    model = cluster.AgglomerativeClustering(
        linkage='ward', connectivity=knn_graph, n_clusters=parcel_N)

    model.fit(coords)

    labels = model.labels_.astype(np.int) + 1

    ctab, names = reorder_ctab_and_names(coords, labels, parcel_N, ctab, names)

    out_filename = 'freesurfer/fsaverage/label/lh.parc_ward_%04d.annot' % parcel_N

    freesurfer.write_annot(out_filename, labels, ctab, names, fill_ctab=True)

    return out_filename


def plot_parcellation(parc_filename, out_filename, surface):

    parcellation = freesurfer.read_annot(parc_filename)

    surf = 'freesurfer/fsaverage/surf/lh.%s' % surface

    plot_surf_roi(
        surf, roi_map=parcellation[0], hemi='left', view='lateral',
        cmap='Spectral', output_file=out_filename)


if __name__ == '__main__':

    filename = 'freesurfer/fsaverage/surf/lh.sphere'

    coords, _ = freesurfer.read_geometry(filename)

    """
    for parcel_N in [2**4, 2**6, 2**8, 2**10, 2**12]:

        t = time()
        parc_file_spherically = parcel_spherically(coords, parcel_N)
        print('spherically\t%04d\t%.03f' % (parcel_N, time() - t))

    for parcel_N in [2**4, 2**6, 2**8, 2**10, 2**12]:

        t = time()
        parc_file_KMeans = parcel_KMeans(coords, parcel_N)
        print('KMeans\t\t%04d\t%.03f' % (parcel_N, time() - t))

        for surface in ['inflated', 'sphere', 'pial']:
                plot_parcellation(
                    parc_file_KMeans, 'plot_kmeans_%s_%04d.png' % (surface, parcel_N), surface)

    for parcel_N in [2**4, 2**6, 2**8, 2**10, 2**12]:

        t = time()
        parc_file_GMM = parcel_GMM(coords, parcel_N)
        print('GMM\t\t%04d\t%.03f' % (parcel_N, time() - t))

        for surface in ['inflated', 'sphere', 'pial']:
                plot_parcellation(
                    parc_file_GMM, 'plot_gmm_%s_%04d.png' % (surface, parcel_N), surface)

    """

    for parcel_N in [2**4, 2**6, 2**8, 2**10, 2**12]:

        t = time()
        parc_file_Ward = parcel_Ward(coords, parcel_N)
        print('Ward\t\t%04d\t%.03f' % (parcel_N, time() - t))

        for surface in ['inflated', 'sphere', 'pial']:

                plot_parcellation(
                    parc_file_Ward, 'plot_ward_%s_%04d.png' % (surface, parcel_N), surface)


    # For validation
    # mri_segstats --annot fsaverage lh parc_Ward --sum summary_file.txt


"""
spherically 0016     0.238
spherically 0016     0.224
spherically 0064     0.736
spherically 0256     2.648
spherically 1024    10.304
spherically 4096    49.146
KMeans      0016     0.919
KMeans      0064     1.314
KMeans      0256     4.232
KMeans      1024    19.433
KMeans      4096    91.256
GMM         0016     4.755
GMM         0064    25.177
GMM         0256    78.734
GMM         1024   241.126
GMM         4096   730.494
Ward        0016    82.463
Ward        0064
Ward        0256
Ward        1024
Ward        4096
"""
