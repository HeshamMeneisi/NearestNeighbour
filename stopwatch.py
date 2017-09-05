import time
class StopWatch:
    def __init__(self):
        self.start_time = time.clock()

    def start(self):
        self.start_time = time.clock()

    def elapsed(self):
        return time.clock() - self.start_time

    def lap(self):
        print "Elapsed time: " + str(self.elapsed()) + " seconds."

    def reset(self):
        self.lap()
        self.start()