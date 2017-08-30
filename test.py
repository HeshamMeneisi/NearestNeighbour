# This file is used solely for quick tests. It can be, at any time, completely omitted from the project.

from kdfinder import KDFinder
import numpy as np
import matplotlib.pyplot as plt

a = np.random.rand(500, 2)
xa = a[:,0]
ya = a[:,1]
xlim = np.asarray([xa.min(),xa.max()])
ylim = np.asarray([ya.min(), ya.max()])

exp = (xlim[1] - xlim[0]) * 0.1
xlim += [-exp, exp]
exp = (ylim[1] - ylim[0]) * 0.1
ylim += [-exp, exp]

plt.xlim(xlim)
plt.ylim(ylim)

plt.plot(xa, ya, 'go', alpha=0.7, zorder=0, markersize=2)

kdf = KDFinder(a)
kdf.setup_plot(xlim, ylim, True)
kdf.find_closest_m(np.random.rand(2) ,5)

plt.show()