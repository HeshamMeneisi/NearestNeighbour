# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from kdfinder import KDFinder
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)
ax2 = fig.add_axes(ax1.get_position(), frameon=False)

ax1.plot(range(50), 'r-')
ax2.plot(range(10), 'g-')

ax1.set_xlim([0,50])
ax1.set_ylim([0,50])
ax2.set_xlim([0,50])
ax2.set_ylim([0,50])

plt.show()