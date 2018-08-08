import numpy as np
from sklearn import cluster, mixture, neighbors


def spectral_clustering(n_clusters, samples):

    """
    Run k-means clustering on vertex coordinates.

    Parameters:
    - - - - -
    n_clusters : int
        number of clusters to generate
    samples : array
        adjacency matrix of surface or region
    """

    spectral = cluster.SpectralClustering(
        n_clusters=n_clusters, affinity='precomputed')
    spectral.fit(samples)

    labels = spectral.labels_.copy()
    labels = labels.astype(np.int32)+1

    return labels


def k_means(n_clusters, samples):

    """
    Run k-means clustering on vertex coordinates.

    Parameters:
    - - - - -
    n_clusters : int
        number of clusters to generate
    samples : array
        Euclidean-space coordinates of vertices
    """

    # Run Mini Batch KMeans algorithm
    k_means = cluster.MiniBatchKMeans(
        n_clusters=n_clusters, init='k-means++', max_iter=1000,
        batch_size=10000, verbose=True, compute_labels=True,
        max_no_improvement=100, n_init=5, reassignment_ratio=0.1)
    k_means.fit(samples)

    labels = k_means.labels_.copy()
    labels = labels.astype(np.int32)+1

    return labels


def gmm(n_clusters, samples):

    """
    Run GMM clustering on vertex coordinates.

    Parameters:
    - - - - -
    n_clusters : int
        number of clusters to generate
    samples : array
        Euclidean-space coordinates of vertices
    """

    # Run Gaussian Mixture Model algorithm
    gmm = mixture.GaussianMixture(
        n_components=n_clusters, covariance_type='tied', max_iter=1000,
        init_params='kmeans', verbose=1)
    gmm.fit(samples)

    gmm.fit(samples)
    labels = ward.labels_.copy()
    labels = labels.astype(np.int32)+1

    return labels


def ward(n_clusters, samples):

    """
    Run Ward clustering on vertex coordinates.

    Parameters:
    - - - - -
    n_clusters : int
        number of clusters to generate
    samples : array
        Euclidean-space coordinates of vertices
    """

    # Run AgglomerativeClustering and Ward algorithm
    knn_graph = neighbors.kneighbors_graph(
        n_clusters, n_neighbors=20, mode='connectivity',
        metric='minkowski', p=2, include_self=False, n_jobs=-1)

    ward = cluster.AgglomerativeClustering(
        n_clusters=n_clusters, affinity='euclidean', connectivity=knn_graph,
        linkage='ward')

    ward.fit(samples)
    labels = ward.labels_.copy()
    labels = labels.astype(np.int32)+1

    return labels
