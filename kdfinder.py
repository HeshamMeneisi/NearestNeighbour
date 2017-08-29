from measurer import SquareDistMeasurer
from finder import Finder, Element
from kdtree import KDTree


class KDFinder(Finder):
    def __init__(self, p_set, measurer=SquareDistMeasurer(2)):
        super(KDFinder, self).__init__(None, measurer)
        assert p_set is not None
        self.count = len(p_set)
        assert self.count > 0
        self.tree = KDTree(None, 'value')
        for i in range(len(p_set)):
            self.tree.insert(Element(p_set[i], i))

    def find_closest_m(self, point, m):
        self.begin(m)
        self.search(self.tree.get_root(), point, m)
        return [[self.pq.peek().value, self.pq.peek().index, self.pq.pop().current_dis] for i in range(m)]

    def begin(self, m):
        super(KDFinder, self).begin(m)
        self._b_upper = [float('inf')] * self.measurer.k
        self._b_lower = [float('-inf')] * self.measurer.k
        self.counter = 0

    def search(self, node, point, m):
        self.counter += 1
        dim = self.tree.d_order[node.discriminator]
        p = node.value[dim]
        dis = self.measurer.measure(point, node.value)
        if self.pq.count() < m or dis < self.pq.peek().current_dis:
            node.obj.current_dis = dis
            self.add_candidate(node.obj)
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
                    if self.pq.count() < m or self.bounds_overlap(self.pq.peek().current_dis, point):
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
                    if self.pq.count() < m or self.bounds_overlap(self.pq.peek().current_dis, point):
                        if self.search(node.left, point, m):
                            return True
                    self._b_upper[dim] = temp
        # Instant termination condition while backtracking
        return self.pq.count() == m and self.within_bounds(self.pq.peek().current_dis, point)

    def bounds_overlap(self, r, point):
        s = 0
        r_inv = self.measurer.F_inv(r)
        for d in range(self.measurer.k):
            if point[d] < self._b_lower[d]:
                s += self.measurer.f(point[d], self._b_lower[d])
                if s > r_inv:  # Same as self.measurer.F(s) > r
                    return True
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
