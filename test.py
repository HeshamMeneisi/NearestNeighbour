# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from finder import Element
from heap import Heap
import numpy as np

h = Heap()

mx = 0
for i in range(100000):
    n = np.random.randint(0, 100000)
    if n > mx:
        mx = n
    h.push(Element(0, i, n))

assert h.peek().current_dis == mx
