from fragmenter import adjacency
import numpy as np

FACES = np.asarray([
    [0, 1, 2], [0, 1, 3], [1, 0, 2], [1, 3, 0],
    [1, 2, 4], [1, 2, 5], [2, 0, 1], [2, 1, 4],
    [2, 1, 5], [3, 0, 1], [4, 1, 2], [5, 1, 2]])

VERTICES = np.zeros((6, 3))

ADJ_LIST = {
    0: [1, 2, 3],
    1: [0, 2, 3, 4, 5],
    2: [0, 1, 4, 5],
    3: [0, 1],
    4: [1, 2],
    5: [1, 2]}


def test_adjacency_construction():

    """
    Test that the correct adjacency structure is produced from a list faces.
    """

    S = adjacency.SurfaceAdjacency(VERTICES, FACES)
    S.generate()

    assert S.adj == ADJ_LIST


def test_adjacency_filtration():

    """
    Test that the filtration of adjacency lists works properly.
    """

    expected_adj = {
        0: [1, 2, 3],
        1: [0, 2, 3, 4],
        2: [0, 1, 4],
        3: [0, 1],
        4: [1, 2]}

    fvs = list(np.arange(5))

    S = adjacency.SurfaceAdjacency(VERTICES, FACES)
    S.generate()
    generated_adj = S.filtration(filter_indices=fvs)

    assert generated_adj == expected_adj
