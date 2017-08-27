import helper as h


def find_closest(point, p_list, k=2, dist_f=h.sq_dist):
    return p_list[find_closest_idx(point, p_list, k=2, dist_f=h.sq_dist)]


def find_closest_idx(point, p_list, k=2, dist_f=h.sq_dist):
    assert len(point) == k and len(p_list) > 0 and len(p_list[0]) == k
    min_idx = 0
    min_d = dist_f(point, p_list[0], k)
    for i in range(1, len(p_list)):
        d = dist_f(point, p_list[i], k)
        if d < min_d:
            min_idx = i
            min_d = d
    return min_idx
