import math
from abc import abstractmethod


class DissimilarityMeasurer(object):
    def __init__(self, k):
        self.k = k

    @abstractmethod
    def F(self, x): pass

    @abstractmethod
    def F_inv(self, x): pass

    @abstractmethod
    def f(self, x, y): pass

    def measure(self, X, Y):
        assert len(X) == self.k and len(Y) == self.k
        return self.F(sum([self.f(X[i], Y[i]) for i in range(self.k)]))


class SquareDistMeasurer(DissimilarityMeasurer):
    def F(self, x): return x

    def F_inv(self, x): return x

    def f(self, x, y):
        diff = x - y
        return diff * diff


class EuclideanDistMeasurer(SquareDistMeasurer):
    def F(self, x): return math.sqrt(x)

    def F_inv(self, x): return x*x
