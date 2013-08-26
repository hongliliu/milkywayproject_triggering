import numpy as np
from sklearn.neighbors import KDTree

from calc_corr import fast_histogram

def test_fast_histogram():

    xy = np.random.normal(0, 1, (1000, 2))
    uv = np.array([[0, 0]])
    t = KDTree(xy)
    dist = np.hypot(xy[:, 0], xy[:, 1])

    bins = np.linspace(0, 3, 100)

    #baseline
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)

    #bins don't start at 0
    bins += .3
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)

    # test point not at origin
    uv = np.array([[0, 1]])
    dist = np.hypot(xy[:, 0] - uv[0, 0],
                     xy[:, 1] - uv[0, 1])
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)

    #unequal bin widths
    bins = np.logspace(-2, 1, 5)
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)

    #counts all 0
    bins = np.logspace(8, 9, 3)
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)
    assert ct.max() == 0

    #uv an exact match
    uv = xy[0:1]
    dist = np.hypot(xy[:, 0] - uv[0, 0],
                     xy[:, 1] - uv[0, 1])
    bins = np.linspace(0, 2, 5)
    ct, bins = np.histogram(dist, bins=bins)
    ct2 = fast_histogram(t, uv, bins)
    np.testing.assert_array_equal(ct, ct2)
