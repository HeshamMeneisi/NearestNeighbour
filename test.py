# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from kdfinder import KDFinder
import numpy as np
import matplotlib.pyplot as plt
import helper as h
from stopwatch import StopWatch
from kdtree import BucketedKDTree, KDTree

a = np.random.rand(5000, 2)

sw = StopWatch()
BucketedKDTree(a, bsize=50)
sw.reset()
KDTree(a)
sw.lap()
# a = np.asarray([[8,3],[9,2],[10,1],[7,4],[6,5],[5,6],[4,7],[3,8],[2,9],[1,10]])
# b = np.copy(a)
# c = np.copy(a)
# sw = StopWatch()
# print 'Distribute'
# sw.start()
# h.fast_distribute_around(a, 0, len(a), len(a)/2, lambda x: x[0])
# sw.reset()
# print 'Sort'
# b=b.tolist()
# sw.start()
# b.sort(key=lambda x:x[0])
# sw.reset()
# b[len(b)/2]
# print "MoM"
# sw.start()
# med =  h.med_of_meds(np.copy(c[:,0]), 0, len(c), len(c)/2)
# k=0
# j=len(c)-1
# s_flag = False
# while k < j:
#     while c[k][0] < med and k < j:
#         s_flag = False
#         k += 1
#     while c[j][0] > med and k < j:
#         s_flag = False
#         j -= 1
#     # Handle pivot duplicate
#     if s_flag:
#         if k < len(c) - j:
#             k += 1
#         else:
#             j -= 1
#     else:
#         s_flag = True
#         h.swap(c, k, j)
# sw.lap()
# m = len(a)/2
# print a[m], b[m], c[m]
# xa = a[:,0]
# ya = a[:,1]
# xlim = np.asarray([xa.min(),xa.max()])
# ylim = np.asarray([ya.min(), ya.max()])
#
# exp = (xlim[1] - xlim[0]) * 0.1
# xlim += [-exp, exp]
# exp = (ylim[1] - ylim[0]) * 0.1
# ylim += [-exp, exp]
#
# plt.xlim(xlim)
# plt.ylim(ylim)
#
# plt.plot(xa, ya, 'go', alpha=0.7, zorder=0, markersize=2)
#
# kdf = KDFinder(a)
# kdf.setup_plot(xlim, ylim, True)
# kdf.find_closest_m(np.random.rand(2) ,5)
#
# plt.show()