# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from kdfinder import KDFinder
import numpy as np

a = np.random.rand(10000, 2) * 1000 - 500

print a.min(axis=0)

kd = KDFinder(a)

print kd.find_closest([1,1])