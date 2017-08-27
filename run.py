import matplotlib.pyplot as plt
import numpy as np
import naive as nv

x_exp = 1.1
y_exp = 1.1

n = 20
a_style = 'bs'

m = 20
b_style = 'ro'

ground_truth_col = 'green'
test_col = 'orange'
set_opacity = 0.6

a = np.random.randn(n, 2)
b = np.random.randn(m, 2)

xa = a[:, 0]
ya = a[:, 1]

xb = b[:, 0]
yb = b[:, 1]

plt.xlim([np.min([xa,xb]) * x_exp, np.max([xa, xb]) * x_exp])
plt.ylim([np.min([ya,yb]) * y_exp, np.max([ya, yb]) * y_exp])

plt.plot(xa, ya, a_style, alpha=set_opacity)
plt.plot(xb, yb, b_style, alpha=set_opacity)

p1 = a[np.random.randint(0,n), :]
p2 = nv.find_closest(p1, b)

plt.plot(np.asarray([p1[0], p2[0]]), np.asarray([p1[1], p2[1]]), color=ground_truth_col)

plt.show()
