import time
class StopWatch:
    def __init__(self):
        self.start_time = False

    def start(self):
        self.start_time = time.clock()

    def elapsed(self):
        return time.clock() - self.start_time

    def lap(self):
        import time
        if self.start_time:
            print "Elapsed time: " + str(self.elapsed()) + " seconds."
        else:
            print "Stopwatch was never started"

    def reset(self):
        self.lap()
        self.start()