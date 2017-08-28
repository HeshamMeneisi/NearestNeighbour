from abc import abstractmethod
from measurer import SquareDistMeasurer
from heap import Heap


class Finder(object):
    @abstractmethod
    def __init__(self, p_set=None, measurer=SquareDistMeasurer(2)):
        if p_set is not None:
            self.count = len(p_set)
            self.p_set = [Element(p_set[i], i) for i in range(self.count)]
        self.measurer = measurer
        self.pq = Heap()

    def find_closest(self, x):
        """Same as find_closest_m(x, 1)"""
        return self.find_closest_m(x, 1)[0]

    def find_closest_m(self, x, m):
        """
        Find the closest m points in the current set using the current measurer.
        :param x: Target
        :param m: Output count
        :return: Returns [value, index, dissimilarity] for each result
        """
        pass

    def begin(self, m):
        assert m < self.count
        self.pq.clear()
        self.m = m

    def add_candidate(self, p):
        self.pq.push(p)
        if self.pq.size() > self.m:
            self.pq.pop()


class Element(object):
    def __init__(self, value, index, current_dis=None):
        self.index = index
        self.value = value
        self.current_dis = current_dis

    def __cmp__(self, other):
        return self.current_dis < other.current_dis
