from heapq import heappush, heappop


class Heap:
    def __init__(self):
        self.h = []

    def clear(self):
        self.h = []

    def count(self):
        return len(self.h)

    def push(self, element):
        heappush(self.h, element)

    def pop(self):
        if len(self.h):
            return heappop(self.h)
        return None

    def peek(self):
        if len(self.h):
            return self.h[0]
        return None

    def clone(self):
        from copy import deepcopy
        target = Heap()
        target.h = deepcopy(self.h)
        return target
