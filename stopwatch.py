import time
class StopWatch:
    def __init__(self):
        self.start_time = False

    def start(self):
        self.start_time = time.clock()

    def lap(self):
        import time
        if self.start_time:
            print "Elapsed time: " + str(time.clock() - self.start_time) + " seconds."
        else:
            print "Stopwatch was never started"

    def reset(self):
        self.lap()
        self.start()