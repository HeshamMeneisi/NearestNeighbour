from measurer import SquareDistMeasurer
from finder import Finder, Element
from kdtree import KDTree, Node, BucketedKDTree, Bucket

# Debugging setup #################################
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import os
import numpy as np
WORKDIR = "C:\Figs"
CLABELS = ['X', 'Y']
################################################


class KDFinder(Finder):
    def __init__(self, p_set, measurer=SquareDistMeasurer(2)):
        super(KDFinder, self).__init__(None, measurer)
        assert p_set is not None
        self.count = len(p_set)
        assert self.count > 0
        self.tree = KDTree(None, 'value', measurer.k)
        for i in range(len(p_set)):
            self.tree.insert(Element(p_set[i], i))
        self.debug = False

    def find_closest_m(self, point, m):
        self.begin(m)
        self.search(self.tree.get_root(), point, m)
        if self.debug:
            self.do_all(point, 'F', 'Final Result', True, True)
        return [[self.pq.peek().value, self.pq.peek().index, self.pq.pop().current_dis] for i in range(m)]

    def begin(self, m):
        super(KDFinder, self).begin(m)
        self._b_upper = [float('inf')] * self.measurer.k
        self._b_lower = [float('-inf')] * self.measurer.k
        if self.debug:
            self.counter = 0
            self.visited = []

    def check_node(self, node, point, m):
        dis = self.measurer.measure(point, node.value)
        if self.pq.count() < m or dis < self.pq.peek().current_dis:
            node.obj.current_dis = dis
            self.add_candidate(node.obj)
        if self.debug:
            msg = 'Entering Node'
            self.visited.append(node.value)
            if node.left is not None:
                msg += '~HasLeft'
            if node.right is not None:
                msg += '~HasRight'
            else:
                msg += '~Discriminator: ' + CLABELS[self.tree.d_order[node.discriminator]]
            self.do_all(point, 'A', msg)

    def search(self, node, point, m):
        bol = False
        self.check_node(node, point, m)
        if type(node) is Node:
            dim = self.tree.d_order[node.discriminator]
            p = node.value[dim]
            if point[dim] < p:
                if node.left is not None:
                    # Search left subtree
                    temp = self._b_upper[dim]
                    self._b_upper[dim] = p
                    if self.search(node.left, point, m):
                        return True
                    self._b_upper[dim] = temp
                # Backtracking
                if node.right is not None:
                    temp = self._b_lower[dim]
                    self._b_lower[dim] = p
                    bol = self.bounds_overlap(self.pq.peek().current_dis, point)
                    if self.debug:
                        self.do_all(point, "B", "Bounds Overlap: " + str(bol))
                    if self.pq.count() < m or bol:
                        if self.search(node.right, point, m):
                            return True
                    self._b_lower[dim] = temp
            else:
                if node.right is not None:
                    # Search right subtree
                    temp = self._b_lower[dim]
                    self._b_lower[dim] = p
                    if self.search(node.right, point, m):
                        return True
                    self._b_lower[dim] = temp
                # Backtracking
                if node.left is not None:
                    temp = self._b_upper[dim]
                    self._b_upper[dim] = p
                    bol = self.bounds_overlap(self.pq.peek().current_dis, point)
                    if self.debug:
                        self.do_all(point, "B", "Bounds Overlap: " + str(bol))
                    if self.pq.count() < m or bol:
                        if self.search(node.left, point, m):
                            return True
                    self._b_upper[dim] = temp

        # Instant termination condition while backtracking
        wb = not bol and self.within_bounds(self.pq.peek().current_dis, point)
        if self.debug:
            self.do_all(point, "C", "Within Bounds: " + str(wb))
        return self.pq.count() == m and wb

    def bounds_overlap(self, r, point):
        s = 0
        r_inv = self.measurer.F_inv(r)
        for d in range(self.measurer.k):
            if point[d] < self._b_lower[d]:
                s += self.measurer.f(point[d], self._b_lower[d])
                if s > r_inv:  # Same as self.measurer.F(s) > r
                    return False
            elif point[d] > self._b_upper[d]:
                s += self.measurer.f(point[d], self._b_upper[d])
                if s > r_inv:  # Same as self.measurer.F(s) > r
                    return False
            # If at the boundary the partial distance is zero, there's no need to alter the sum or check
            return True

    def within_bounds(self, r, point):
        for d in range(self.measurer.k):
            r_inv = self.measurer.F_inv(r)
            if point[d] < self._b_lower[d] or point[d] > self._b_upper[d] \
                    or self.measurer.f(point[d], self._b_lower[d]) < r_inv \
                    or self.measurer.f(point[d], self._b_upper[d]) < r_inv:
                return False
        return True

    # Debugging functions #################################
    def setup_plot(self, xlim, ylim, save=False):
        ca = plt.gca()
        self.overlay_ax = plt.gcf().add_axes(ca.get_position(), frameon=False)
        self.xlim = xlim
        self.ylim = ylim
        self.overlay_ax.set_xlim(xlim)
        self.overlay_ax.set_ylim(ylim)
        if save:
            if os.path.exists(WORKDIR):
                import shutil
                shutil.rmtree(WORKDIR)
            os.makedirs(WORKDIR)
        self.save = save
        self.debug = True

    def do_all(self, point, label, msg, force_save=False, legend=False):
        if self.save or force_save:
            self.overlay_ax.clear()
            self.overlay_ax.set_xlim(self.xlim)
            self.overlay_ax.set_ylim(self.ylim)
            self.plot_bounds()
            self.plot_range(point)
            self.plot_visited()
            self.plot_found(point)
            self.overlay_ax.text(self.xlim[0], self.ylim[0], msg)
            if legend:
                plt.legend()
            self.save_plot(label)
            self.counter += 1

    def plot_bounds(self):
        self.overlay_ax.axvline(x=self._b_lower[0], color='r', label='Lower Search Bound')
        self.overlay_ax.axvline(x=self._b_upper[0], color='g', label='Upper Search Bound')
        self.overlay_ax.axhline(y=self._b_lower[1], color='r')
        self.overlay_ax.axhline(y=self._b_upper[1], color='g')

    def plot_range(self, point):
        # NOTE: Using square distance
        if self.pq.count() > 0:
            r = math.sqrt(self.pq.peek().current_dis)
            c = Circle(point, r, fill=False, color='black', label='Candidates Region')
            self.overlay_ax.add_patch(c)

    def plot_visited(self):
        for p in self.visited:
            self.overlay_ax.plot(p[0], p[1], 'ro', markersize=3)
        if self.visited.count > 0:
            self.overlay_ax.plot(self.visited[-1][0], self.visited[-1][1], 'ro', markersize=5, label='Visited')

    def plot_found(self, p1):
        found = self.pq.h
        for element in found:
            p2 = element.value
            self.overlay_ax.plot([p1[0],p2[0]],[p1[1],p2[1]], color='orange', linewidth=1.2)

    def save_plot(self, label):
        path = os.path.join(WORKDIR, str(self.counter)+'_'+label+'.png')
        plt.savefig(path)


class BKDFinder(KDFinder):
    def __init__(self, p_set, measurer=SquareDistMeasurer(2), optimize=False):
        super(KDFinder, self).__init__(None, measurer)
        assert p_set is not None
        self.count = len(p_set)
        assert self.count > 0
        self.tree = BucketedKDTree([Element(p_set[i], i) for i in range(len(p_set))], 'value', \
                                   measurer.k, optimized=optimize)
        self.debug = False

    def check_node(self, node, point, m):
        if type(node) is Bucket:
            for n in node.data:
                super(BKDFinder, self).check_node(n, point, m)
        else:
            super(BKDFinder, self).check_node(node, point, m)