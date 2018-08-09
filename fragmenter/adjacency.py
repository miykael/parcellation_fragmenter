# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:31:06 2016

@author: kristianeschenburg
"""

import networkx as nx
import numpy as np


class SurfaceAdjacency(object):
    """
    Class to generate an adjacency list  of a surface mesh representation
    of the brain.

    Initialize SurfaceAdjacency object.

    Parameters:
    - - - - -
    vertices : array
        vertex coordinates
    faces : list
        list of faces in surface
    """

    def __init__(self, vertices, faces):

        self.vertices = vertices
        self.faces = faces

    def generate(self, indices=None):

        """
        Method to create surface adjacency list.
        """

        # Get faces attribute
        faces = self.faces.tolist()
        accepted = np.zeros((self.vertices.shape[0]))

        # get indices of interest
        if not indices:
            indices = list(np.unique(np.concatenate(faces)))
        indices = np.sort(indices)

        # create array of whether indices are included
        # cancels out search time in loop
        accepted[indices] = 1
        accepted = accepted.astype(bool)

        # Initialize adjacency list
        adjacency = {k: [] for k in indices}

        # loop over faces in mesh
        for face in faces:
            nbs = [n for n in face[1:] if accepted[n]]
            adjacency[face[0]].append(nbs)

        for k in adjacency.keys():
            adjacency[k] = list(set(np.concatenate(adjacency[k])))

        # Set adjacency list field
        self.adj = adjacency

    def filtration(self, filter_indices=None, toArray=False, remap=False):
        """
        Generate a local adjacency list, constrained to a subset of vertices on
        the surface.  For each vertex in 'vertices', retain neighbors
        only if they also exist in 'vertices'.

        Parameters:
        - - - - -
        fitler_indices : array
            indices to include in sub-graph.  If none, returns original graph.
        to_array : bool
            return adjacency matrix of filter_indices
        remap : bool
            remap indices to 0-len(filter_indices)
        Returns:
        - - - -
        G : array / dictionary
            down-sampled adjacency list / matrix
        """

        assert hasattr(self, 'adjacency')

        if not np.any(filter_indices):
            G = self.adj.copy()

        else:
            filter_indices = np.sort(filter_indices)

            G = {}.fromkeys(filter_indices)

            for v in filter_indices:
                G[v] = list(set(self.adj[v]).intersection(set(filter_indices)))

            ind2sort = dict(zip(
                filter_indices,
                np.arange(len(filter_indices))))

        if remap:
            remapped = {
                ind2sort[fi]: [ind2sort[nb] for nb in G[fi]]
                for fi in filter_indices}

            G = remapped

        if toArray:
            G = nx.from_dict_of_lists(G)
            nodes = G.nodes()
            nodes = np.argsort(nodes)
            G = nx.to_numpy_array(G)
            G = G[nodes, :][:, nodes]

        return G
