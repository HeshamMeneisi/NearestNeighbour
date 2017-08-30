import matplotlib.pyplot as plt
import numpy as np
import measurer as h
from naive import NaiveFinder
from kdfinder import KDFinder
from stopwatch import StopWatch

# View settings
x_exp = 0.1
y_exp = 0.2
save_steps = False
zoom_in = False
full_screen = False

# The number of closest points to find
K = 1

# The set to search through
n = 5000
a_style = 'go'
a_size = 4
a_order = 0

# The set to use for searching
m = 200
b_style = 'bs'
b_size = 4
b_order = 1

ground_truth_col = 'green'
test_col = 'orange'
set_opacity = 0.6
s_min = -10
s_max = 10
s_range = s_max - s_min

sw = StopWatch()

a = np.random.rand(n, 2) * s_range + s_min
b = np.random.rand(m, 2) * s_range + s_min

xa = a[:, 0]
ya = a[:, 1]

xb = b[:, 0]
yb = b[:, 1]

xlim = np.asarray([np.min([xa.min(), xb.min()]), np.max([xa.max(), xb.max()])])
ylim = np.asarray([np.min([ya.min(), yb.min()]), np.max([ya.max(), yb.max()])])

exp = (xlim[1] - xlim[0]) * x_exp
xlim += [-exp, exp]
exp = (ylim[1] - ylim[0]) * y_exp
ylim += [-exp, exp]

plt.xlim(xlim)
plt.ylim(ylim)

plt.plot(xa, ya, a_style, alpha=set_opacity, zorder=a_order, markersize=a_size)
plt.plot(xb, yb, b_style, alpha=set_opacity, zorder=b_order, markersize=b_size)

total_nv = 0
total_kd = 0

print "Initializing naive module..."
sw.start()
nf = NaiveFinder(a)
total_nv += sw.elapsed()
sw.reset()

print "Initializing K-D Tree module..."
kdf = KDFinder(a)
total_kd += sw.elapsed()
sw.lap()

for i in range(m):
    print i
    p1 = b[i, :]

    sw.start()
    found = nf.find_closest_m(p1, K)
    total_nv += sw.elapsed()

    sw.reset()
    kdfound = kdf.find_closest_m(p1, K)
    total_kd += sw.elapsed()
    sw.reset()

    # If there's a mismatch with ground-truth values, save K-D search steps for debugging
    if not (np.asarray(found)[:, 1] == np.asarray(kdfound)[:, 1]).all():
        print "Mismatch", np.asarray(found)[:, 1], np.asarray(kdfound)[:, 1]
        for element in found:
            p2 = element[0]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=ground_truth_col, zorder=2, linewidth=2)
        kdf.setup_plot(xlim, ylim, True)
        kdf.find_closest_m(p1, 5)
        sw.start()
        found = kdf.find_closest_m(p1, 5)
        for element in kdfound:
            p2 = element[0]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=test_col, zorder=3, linewidth=1.5)
        print "Done"
        plt.show()

found = nf.find_closest_m(p1, 5)
for element in found:
    p2 = element[0]
    h1 = plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=ground_truth_col, zorder=2, linewidth=2)

kdf.setup_plot(xlim, ylim, save_steps)
kdfound = kdf.find_closest_m(p1, 5)
for element in kdfound:
    p2 = element[0]
    h2 = plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=test_col, zorder=3, linewidth=1.5)

if zoom_in:
    points = np.asarray(kdfound)[:, 0]
    xs = np.asarray([p[0] for p in points])
    ys = np.asarray([p[1] for p in points])

    xlim = np.asarray([xs.min(), xs.max()])
    ylim = np.asarray([ys.min() , ys.max()])

    exp = (xlim[1] - xlim[0]) * x_exp
    xlim += [-exp, exp]
    exp = (ylim[1] - ylim[0]) * y_exp
    ylim += [-exp, exp]
    
    for ax in plt.gcf().axes:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

if full_screen:
    mng = plt.get_current_fig_manager()
    print mng.full_screen_toggle()

print ""
print "Total Time for Naive Approach:", total_nv
print "Total Time for K-D Tree:", total_kd

plt.show()
