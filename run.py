import matplotlib.pyplot as plt
import numpy as np
import measurer as h
from naive import NaiveFinder

x_exp = 1.1
y_exp = 1.1

n = 50
a_style = 'ro'
a_size = 4
a_order = 0

m = 20
b_style = 'bs'
b_size = 4
b_order = 1

ground_truth_col = 'green'
test_col = 'orange'
set_opacity = 0.6
s_min = -1000000
s_max = 1000000
s_range = s_max - s_min

a = np.random.randn(n, 2) * s_range + s_min
b = np.random.randn(m, 2) * s_range + s_min

xa = a[:, 0]
ya = a[:, 1]

xb = b[:, 0]
yb = b[:, 1]

plt.xlim([np.min([xa.min(),xb.min()]) * x_exp, np.max([xa.max(), xb.max()]) * x_exp])
plt.ylim([np.min([ya.min(),yb.min()]) * y_exp, np.max([ya.max(), yb.max()]) * y_exp])

plt.plot(xa, ya, a_style, alpha=set_opacity, zorder=a_order, markersize=a_size)
plt.plot(xb, yb, b_style, alpha=set_opacity, zorder=b_order, markersize=b_size)

nf = NaiveFinder(a)
p1 = b[np.random.randint(0, m), :]

for element in nf.find_closest_m(p1, 5):
    p2 = element[0]
    plt.plot(np.asarray([p1[0], p2[0]]), np.asarray([p1[1], p2[1]]), color=ground_truth_col, zorder=2)

plt.show()
