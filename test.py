# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from finder import Element
from kdtree import KDTree
import numpy as np

# Tree consistency test
# print "Testing raw data."
# a = np.random.randn(10000, 2)
# t = KDTree(a)
#
# for i in range(0, len(a)):
#     assert t.has(a[i])

print "Testing wrapped data."
a = np.random.randn(10000, 2)
t = KDTree(partitioner='value')
for i in range(len(a)):
    t.insert(Element(a[i], i))

for i in range(len(a)):
    assert t.has(Element(a[i], i))