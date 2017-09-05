import matplotlib.pyplot as plt
import numpy as np
import measurer as h
from naive import NaiveFinder
from kdfinder import KDFinder, BKDFinder
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
n = 200
a_style = 'go'
a_size = 4
a_order = 0

# The set to use for searching
m = 5000
b_style = 'bs'
b_size = 4
b_order = 1

ground_truth_col = 'green'
test_col = 'orange'
set_opacity = 0.6
s_min = -10
s_max = 10
s_range = s_max - s_min


def run():
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
    total_bkd = 0
    total_obkd = 0

    print "Initializing naive module..."
    sw.start()
    nf = NaiveFinder(a)
    bt_nv = sw.elapsed()
    total_nv += bt_nv
    sw.reset()

    print "Initializing K-D Tree module..."
    sw.start()
    kdf = KDFinder(a)
    bt_kd = sw.elapsed()
    total_kd += bt_kd
    sw.lap()

    print "Initializing Bucketed K-D Tree module..."
    sw.start()
    bkdf = BKDFinder(a)
    bt_bkd = sw.elapsed()
    total_bkd += bt_bkd
    sw.lap()

    print "Initializing Optimized Bucketed K-D Tree module..."
    sw.start()
    obkdf = BKDFinder(a)
    bt_obkd = sw.elapsed()
    total_obkd += bt_obkd
    sw.lap()

    for i in range(m):
        print i
        p1 = b[i, :]

        sw.start()
        found = nf.find_closest_m(p1, K)
        total_nv += sw.elapsed()

        def check_mismatch(h_f, finder):
            # If there's a mismatch with ground-truth values, save K-D search steps for debugging
            if not (np.asarray(found)[:, 1] == np.asarray(h_f)[:, 1]).all():
                print "Mismatch", np.asarray(found)[:, 1], np.asarray(h_f)[:, 1]
                for element in found:
                    p2 = element[0]
                    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=ground_truth_col, zorder=2, linewidth=2)
                finder.setup_plot(xlim, ylim, True)
                finder.find_closest_m(p1, 5)
                sw.start()
                finder.find_closest_m(p1, 5)
                for element in h_f:
                    p2 = element[0]
                    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=test_col, zorder=3, linewidth=1.5)
                print "Done"
                plt.show()

        sw.start()
        kdfound = kdf.find_closest_m(p1, K)
        total_kd += sw.elapsed()

        check_mismatch(kdfound, kdf)

        sw.start()
        bkdfound = bkdf.find_closest_m(p1, K)
        total_bkd += sw.elapsed()

        check_mismatch(bkdfound, bkdf)

        sw.start()
        obkdfound = obkdf.find_closest_m(p1, K)
        total_obkd += sw.elapsed()

        check_mismatch(obkdfound, obkdf)

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

    print ''
    print 'Doing', m, 'queries in', n, 'records for', K, 'closest'
    print ''
    print 'Method\t\t\tTotal Time\t\t\tBuild Time\t\t\tMean per-query'
    print 'Naive\t\t\t', total_nv, '\t\t', bt_nv, '\t\t', (total_nv-bt_nv)/m
    print 'KD Tree\t\t\t', total_kd, '\t\t', bt_kd, '\t\t', (total_kd - bt_kd) / m
    print 'BKD Tree\t\t', total_bkd, '\t\t', bt_bkd, '\t\t', (total_bkd - bt_bkd) / m
    print 'OBKD Tree\t\t', total_obkd, '\t\t', bt_obkd, '\t\t', (total_obkd - bt_obkd) / m

    plt.show()

if __name__ == '__main__':
    run()