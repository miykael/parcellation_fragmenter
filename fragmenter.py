import numpy as np
from nibabel import freesurfer
from nilearn.plotting import plot_surf_roi
from sklearn import cluster, mixture, neighbors


def get_equally_spaced_colors(n):
    """
    Returns a color table with N elements, equally spaced throughout RGB-space
    """

    max_value = 256**3 - 1
    equal_spaced = np.linspace(0, max_value, n, endpoint=True, dtype='int')
    colors = [hex(i)[2:].zfill(6) for i in equal_spaced]

    color_table = np.array(
        [[int(i[:2], 16), int(i[2:4], 16), int(i[4:], 16)] for i in colors])

    return color_table


def get_ctab_and_names(n_parcel, coords, labels, use_pretty_colors=True):
    """
    Returns color table and names - pretty color gradient order optional
    """

    # Create color table (first element = [0, 0, 0] for 'unknown' region)
    n_colors = n_parcel + 1
    ctab = np.hstack((get_equally_spaced_colors(n_colors), [[0]] * n_colors))

    # Create name list for new regions
    names = [np.bytes_('unknown')] + \
        [np.bytes_('parc%05d' % (i + 1)) for i in range(n_parcel)]

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


def fragment_parcel(coords, n_parcel, algorithm='kmeans', mask=None,
                    use_pretty_colors=True, output_file='_h.fragment.annot'):
    """
    Fragments specified region according to a given clustering algorithm
    """

    # Mask coordinates with roi_mask
    roi_coords = coords[mask]

    if algorithm == 'kmeans':

        # Run Mini Batch KMeans algorithm
        k_means = cluster.MiniBatchKMeans(
            n_clusters=n_parcel, init='k-means++', max_iter=1000,
            batch_size=10000, verbose=True, compute_labels=True,
            max_no_improvement=100, n_init=5, reassignment_ratio=0.1)
        k_means.fit(roi_coords)

        # Extract labels for each vertex and increase values by 1
        labels = np.copy(k_means.labels_).astype(np.int) + 1

    elif algorithm == 'gmm':

        # Run Gaussian Mixture Model algorithm
        gmm = mixture.GaussianMixture(
            n_components=n_parcel, covariance_type='tied', max_iter=1000,
            init_params='kmeans', verbose=1)
        gmm.fit(roi_coords)

        # Extract labels for each vertex and increase values by 1
        labels = np.copy(gmm.predict(roi_coords)).astype(np.int) + 1

    elif algorithm == 'ward':

        # Run AgglomerativeClustering and Ward algorithm
        knn_graph = neighbors.kneighbors_graph(
            roi_coords, n_neighbors=20, mode='connectivity',
            metric='minkowski', p=2, include_self=False, n_jobs=-1)

        model = cluster.AgglomerativeClustering(
            n_clusters=n_parcel, affinity='euclidean', connectivity=knn_graph,
            linkage='ward')

        model.fit(roi_coords)

        # Extract labels for each vertex and increase values by 1
        labels = np.copy(model.labels_).astype(np.int) + 1

    # Create color table and region names for annotation file
    ctab, names, labels = get_ctab_and_names(
        n_parcel, roi_coords, labels, use_pretty_colors)

    # Extend labels to whole spherical surface mesh
    surface_labels = np.zeros(mask.shape, dtype='int')
    surface_labels[mask] = labels

    # Create annotation file
    freesurfer.write_annot(
        output_file, surface_labels, ctab, names, fill_ctab=True)

    return output_file


def get_roi_mask(roi_idx, fpath_annot):
    """
    Creates a region mask specifying which vertexes to consider
    """

    # Load annotation file
    roi_labels, _, roi_names = freesurfer.read_annot(fpath_annot)

    # Get index of rois to consider
    roi_index = [roi_names.index(np.bytes_(n)) for n in roi_idx]

    # Create vertex mask
    roi_mask = np.isin(roi_labels, np.array(roi_index))

    # Take all regions if none specified
    if roi_mask.sum() == 0:
        roi_mask = np.invert(roi_mask)

    return roi_mask


def plot_fragment(frag_file, filename, fpath_sphere, surface):
    """
    Plot fragmented region on specific surface
    """

    # Load labels of new fragmented annotation
    labels, _, _ = freesurfer.read_annot(frag_file)

    # Specify on which surface to plot
    surf_type = fpath_sphere.replace('.sphere', '.%s' % surface)

    # Plot fragmented region on surface with colored annotation
    plot_surf_roi(
        surf_type, roi_map=labels, hemi='left', view='lateral',
        cmap='Spectral', output_file=filename)


if __name__ == '__main__':

    # Specify name of subject and hemisphere to work on
    sub_id = 'fsaverage'
    hemi = 'lh'

    # Specify location of subject specific sphere mesh and annotation file
    fpath_sphere = 'freesurfer/%s/surf/%s.sphere' % (sub_id, hemi)
    fpath_annot = 'freesurfer/%s/label/%s.aparc.annot' % (sub_id, hemi)

    # Load vertex coordinates
    coords, _ = freesurfer.read_geometry(fpath_sphere)

    # Specify number of fragments requested in annotation region
    n_parcel = 2**4

    # Specify name of regions to consider (empty = all regions)
    roi_idx = ['superiortemporal', 'transversetemporal']
    roi_mask = get_roi_mask(roi_idx, fpath_annot)

    # Create fragmented annotation file
    algorithm = 'kmeans'
    fpath_out = 'freesurfer/%s/label/lh.%s.annot' % (
        sub_id, '%s_%05d' % (algorithm, n_parcel))

    fragment_file = fragment_parcel(
        coords, n_parcel, algorithm=algorithm, mask=roi_mask,
        use_pretty_colors=True, output_file=fpath_out)

    # Plot fragmented parcellation
    surfaces_to_plot = ['sphere', 'inflated', 'pial']
    for surface in surfaces_to_plot:
        plot_fragment(fpath_out,
                      'plot_%s_%s_%05d.png' % (
                          algorithm, surface, n_parcel),
                      fpath_sphere,
                      surface)
