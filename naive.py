from measurer import SquareDistMeasurer
from finder import Finder


class NaiveFinder(Finder):
    def __init__(self, p_set, measurer=SquareDistMeasurer(2)):
        super(NaiveFinder, self).__init__(p_set, measurer)
        assert self.p_set is not None and self.count > 0

    def find_closest_m(self, point, m):
        self.begin(m)
        for i in range(0, self.count):
            d = self.measurer.measure(point, self.p_set[i].value)
            if self.pq.count() < m or d < self.pq.peek().current_dis:
                self.p_set[i].current_dis = d
                self.add_candidate(self.p_set[i])
        return [[self.pq.peek().value, self.pq.peek().index, self.pq.pop().current_dis] for i in range(m)]
