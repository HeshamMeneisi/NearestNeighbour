import time
class StopWatch:
    def __init__(self):
        self.start_time = time.clock()

    def start(self):
        self.start_time = time.clock()

    def elapsed(self):
        return time.clock() - self.start_time

    def lap(self, msg=None):
        t = str(self.elapsed())
        if msg is None:
            msg = 'Elapsed time: '
        else:
            msg += ': '
        print msg + t + " seconds."

    def reset(self, msg=None):
        self.lap(msg)
        self.start()