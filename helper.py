import math


def sq_dist(p1, p2, k=2):
    assert len(p1) == len(p2) == k
    s = 0
    for i in range(k):
        diff = p1[i] - p2[i]
        s += diff * diff
    return s


def euc_dist(p1, p2, k=2):
    return math.sqrt(sq_dist(p1, p2, k))
