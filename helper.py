import numpy as np


# This is an O(n) algorithm, but the python sort is run natively so it performs much better even though it's O(nlog(n))
def fast_distribute_around(a, low, high, i, key):
    if high - low <= 5:
        a[low:high, :] = sorted(np.copy(a[low:high, :]), key=key)
        return a[i]

    medians = np.asarray([five[len(five)/2] for five in
                          [sorted(a[j:min([j+5, high])], key=key) for j in range(low, high, 5)]])

    i_h = int(float(i-low)/(high-low) * len(medians))
    pivot = key(fast_distribute_around(medians, 0, len(medians), i_h, key))

    k = low
    j = high - 1
    s_flag = False

    while k < j:
        while key(a[k]) < pivot and k < j:
            s_flag = False
            k += 1
        while key(a[j]) > pivot and k < j:
            s_flag = False
            j -= 1
            # Handle pivot duplicates
        if s_flag:
            s_flag = False
            if k - low < high - j:
                k += 1
            else:
                j -= 1
        else:
            s_flag = True
            swap(a, k, j)
    if i < k:
        return fast_distribute_around(a, low, k, i, key)
    if i > k:
        return fast_distribute_around(a, k+1, high, i, key)
    return a[i]


def med_of_meds(a, low, high, i):
    if high - low <= 5:
        return sorted(a[low:high])[i-low]

    medians = [five[len(five)/2] for five in
                          [sorted(a[j:min(j+5, high)]) for j in range(low, high, 5)]]
    l = len(medians)
    i_h = int(float(i-low)/(high-low) * l)
    pivot = med_of_meds(medians, 0, l, i_h)

    k = low
    j = high - 1
    s_flag = False

    while k < j:
        while a[k] < pivot and k < j:
            s_flag = False
            k += 1
        while a[j] > pivot and k < j:
            s_flag = False
            j -= 1
        # Handle pivot duplicate
        if s_flag:
            s_flag = False
            if k - low < high - j:
                k += 1
            else:
                j -= 1
        else:
            s_flag = True
            swap(a, k, j)
    if i < k:
        return med_of_meds(a, low, k, i)
    if i > k:
        return med_of_meds(a, k+1, high, i)
    return a[i]


def swap(a, i, j):
    temp = np.copy(a[i])
    a[i] = a[j]
    a[j] = temp